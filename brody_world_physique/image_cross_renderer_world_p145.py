"""P145: held-out scene-ENGINE test. New drawing pipeline, not P140 transforms.

Training/validation: P140. Examination: independent drawing code with
different canvas/positions/compositing/background/outline. No test labels
feed either predictor or router. Per-family paired control-vs-shift report.
"""
from __future__ import annotations
import argparse,json,random,time,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
from .image_long_curriculum_p140 import FAMILIES,LABELS,SHAPES,COLORS,make,features
from .image_blind_router_p144 import context_features,predictions,pick_router
from .image_geometric_transfer_p142 import feat_for
from .image_transfer_stress_p141 import SHIFTS,shift_image

WORLD_TYPES=("reference","new_engine_light","new_engine_dark","new_engine_outlined","new_engine_occluded")
def alternative_scene(rng,family,world):
    """Original renderer. Truth is from curriculum, never predicted features."""
    shape=rng.choice(SHAPES)
    color_idx=rng.randrange(4)
    n=3 if family=="arrangement" else rng.randint(1,3)
    arrangement=rng.choice(LABELS["arrangement"])
    orient=rng.choice(LABELS["orientation"])
    background=(250,246,235) if world!="new_engine_dark" else (55,59,69)
    im=Image.new("RGB",(96,96),background)
    dr=ImageDraw.Draw(im)
    for i in range(n):
        if arrangement=="horizontal":cx=19+i*28;cy=47
        elif arrangement=="vertical":cx=46;cy=19+i*28
        else:cx=19+i*28;cy=19+i*28
        cx+=rng.randint(-4,4);cy+=rng.randint(-4,4)
        w,h={"wide":(24,12),"tall":(12,24),"balanced":(19,19)}[orient]
        box=(cx-w//2,cy-h//2,cx+w//2,cy+h//2)
        rgb=COLORS[color_idx]
        if shape=="triangle":
            dr.polygon(((cx,box[1]),(box[0],box[3]),(box[2],box[3])),fill=rgb)
        elif shape=="rectangle":
            dr.rounded_rectangle(box,radius=2,fill=rgb)
        else:
            dr.ellipse(box,fill=rgb)
        if world=="new_engine_outlined":
            dr.rectangle((box[0],box[1],box[2],box[3]),outline=(35,35,35),width=1)
        if world=="new_engine_occluded":
            # Actual pixel occluder, never described in test feature input.
            x=cx+rng.randint(-2,2)
            dr.rectangle((x,box[1]-2,x+4,box[3]+2),fill=background)
    if world=="new_engine_light":
        im=im.filter(ImageFilter.GaussianBlur(0.65))
    target={"shape":shape,"colour":LABELS["colour"][color_idx],
            "count":LABELS["count"][n-1],
            "arrangement":arrangement,"orientation":orient}[family]
    return im,target
def run(out,minutes=15,seed=145,train_each=300,validation_each=90,exam_each=1000):
    if not (2<=minutes<=60 and 30<=train_each<=1000 and 20<=validation_each<=1000 and 20<=exam_each<=20000):
        raise ValueError("RESOURCE_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    started=time.monotonic();deadline=started+minutes*60
    tr=random.Random(seed);vr=random.Random(seed+1113);er=random.Random(seed+28119)
    mem={f:{"rgb":[],"geo":[]} for f in FAMILIES}
    for fam in FAMILIES:
        for i in range(train_each):
            im,answer=make(tr,fam,1+i%3)
            mem[fam]["rgb"].append((features(im),answer))
            mem[fam]["geo"].append((feat_for(im,fam),answer));im.close()
    validation={f:[] for f in FAMILIES}
    for shift in SHIFTS:
        for fam in FAMILIES:
            for i in range(validation_each):
                im,answer=make(vr,fam,1+i%3)
                altered=shift_image(im,shift);im.close()
                ctx=context_features(altered);options=predictions(mem,fam,altered);altered.close()
                for model,guess in options.items():
                    validation[fam].append((ctx,model,int(guess==answer)))
    (dest/"FROZEN_BEFORE_EXAM.json").write_text(json.dumps({
        "train_origin":"P140_renderer","validation_origin":"P140_renderer_transformed",
        "exam_origin":"P145_independently_implemented_renderer",
        "train_seed":seed,"validation_seed":seed+1113,"exam_seed":seed+28119,
        "no_exam_labels_in_training":True,"question_family_known":True},indent=2),encoding="utf8")
    cells={};stop=False
    with (dest/"EXAM.jsonl").open("w",encoding="utf8") as log:
        for world in WORLD_TYPES:
            for fam in FAMILIES:
                counts={"n":0,"correct":0,"holds":0,"rgb_correct":0,"geo_correct":0,"majority_correct":0}
                for i in range(exam_each):
                    if time.monotonic()>=deadline:stop=True;break
                    if world=="reference":im,answer=make(er,fam,1+i%3)
                    else:im,answer=alternative_scene(er,fam,world)
                    ctx=context_features(im);options=predictions(mem,fam,im)
                    is_achromatic=all(max(pixel)-min(pixel)<2 for pixel in im.resize((12,12)).getdata())
                    im.close()
                    selected=pick_router(validation,fam,ctx)
                    guess="HOLD" if fam=="colour" and is_achromatic else options[selected]
                    counts["n"]+=1;counts["correct"]+=int(guess==answer)
                    counts["holds"]+=int(guess=="HOLD")
                    for m in ("rgb","geo","majority"):counts[m+"_correct"]+=int(options[m]==answer)
                    log.write(json.dumps({"world":world,"family":fam,"chosen":selected,"prediction":guess,
                        "teacher":answer,"right":guess==answer},sort_keys=True)+"\n")
                cells[fam+"/"+world]=counts
                if stop:break
            if stop:break
    (dest/"CELL_REPORT.json").write_text(json.dumps(cells,indent=2),encoding="utf8")
    grouped={}
    for world in WORLD_TYPES:
        group=[r for name,r in cells.items() if name.endswith("/"+world)]
        n=sum(r["n"] for r in group)
        grouped[world]={"n":n,"correct":sum(r["correct"] for r in group),
             "accuracy":round(sum(r["correct"] for r in group)/n,4) if n else None,
             "coverage":round(sum(r["n"]-r["holds"] for r in group)/n,4) if n else None}
    summary={"schema":"BRODY_P145_CROSS_RENDERER_WORLD_SHIFT",
      "cases":sum(s["n"] for s in cells.values()),"cells_completed":sum(s["n"]==exam_each for s in cells.values()),
      "cells_expected":25,"elapsed_seconds":round(time.monotonic()-started,3),
      "world_scores":grouped,"stop_reason":"TIME_BUDGET" if stop else "EXAM_CAP",
      "separate_renderer_implementation":True,"independent_real_world_sources":False,
      "real_world_generalization_proven":False,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(summary,indent=2),encoding="utf8")
    return summary
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=15);p.add_argument("--seed",type=int,default=145)
    p.add_argument("--train-each",type=int,default=300)
    p.add_argument("--validation-each",type=int,default=90)
    p.add_argument("--exam-each",type=int,default=1000)
    a=p.parse_args();print(json.dumps(run(a.out,a.minutes,a.seed,a.train_each,a.validation_each,a.exam_each),indent=2))
if __name__=="__main__":main()
