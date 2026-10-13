"""P147: occlusion epistemics with paired visible and hidden physical scenes.

An object behind a fully opaque screen is NOT identifiable from its front image.
The hidden label is never supplied to inference. Scoring distinguishes valid
abstentions from successes on visible properties. Synthetic demonstration only.
"""
from __future__ import annotations
import argparse,json,random,time
from pathlib import Path
from PIL import Image,ImageDraw
from .image_background_adaptation_p146 import robust_features
from .image_transfer_stress_p141 import centroid_predict
SHAPES=("rectangle","ellipse","triangle")
COLOURS=((220,40,45),(25,75,220),(30,165,55))
def render(rng,occlusion):
    s=rng.randrange(3);c=rng.randrange(3);x=rng.randrange(16,27);y=rng.randrange(16,27)
    im=Image.new("RGB",(96,96),(245,245,245));d=ImageDraw.Draw(im)
    box=(x,y,x+25,y+25)
    if s==0:d.rectangle(box,fill=COLOURS[c])
    elif s==1:d.ellipse(box,fill=COLOURS[c])
    else:d.polygon(((x+12,y),(x,y+25),(x+25,y+25)),fill=COLOURS[c])
    if occlusion=="partial":
        d.rectangle((x+12,y-2,x+20,y+28),fill=(95,95,95))
    elif occlusion=="full":
        d.rectangle((x-3,y-3,x+28,y+28),fill=(95,95,95))
    return im,SHAPES[s],c
def guess(memory,im):
    vec=robust_features(im,"shape")
    if not memory:return "HOLD"
    return centroid_predict(memory,vec,SHAPES)
def run(out,minutes=10,seed=147,lessons=150,exam_per_condition=1500):
    if not 2<=minutes<=60 or not 30<=lessons<=1000 or not 20<=exam_per_condition<=20000:raise ValueError("INVALID_BOUNDS")
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_EVIDENCE")
    dest.mkdir(parents=True)
    t=time.monotonic();deadline=t+minutes*60
    rng_train=random.Random(seed);rng_exam=random.Random(seed+10101)
    memory=[]
    for i in range(lessons):
        im,label,c=render(rng_train,"none")
        memory.append((robust_features(im,"shape"),label));im.close()
    (dest/"SEALED_COURSE.json").write_text(json.dumps({"course_examples":lessons,
      "exam_seed":seed+10101,"memory_frozen_before_exam":True},indent=2),encoding="utf8")
    stats={}
    with (dest/"EXAMS.jsonl").open("w",encoding="utf8") as log:
        for condition in ("none","partial","full"):
            entry={"n":0,"answered":0,"correct":0,"holds":0,"counterfactual_collisions":None}
            for i in range(exam_per_condition):
                if time.monotonic()>=deadline:break
                im,label,col=render(rng_exam,condition)
                # A fully occluded object has exactly the same visible image
                # for many latent shapes. It is therefore not identifiable.
                if condition=="full":response="HOLD";reason="FULLY_HIDDEN_OBJECT"
                else:response=guess(memory,im);reason="LEARNED_VISIBLE_SHAPE"
                # Counterfactual pixel equality requires a separate paired
                # renderer with fixed location; not measured in this run.
                entry["n"]+=1;entry["holds"]+=int(response=="HOLD")
                entry["answered"]+=int(response!="HOLD")
                entry["correct"]+=int(response==label)
                log.write(json.dumps({"condition":condition,"i":i,"actual":label,
                    "prediction":response,"reason":reason,"correct":response==label})+"\n")
                im.close()
            stats[condition]=entry
    report={"schema":"BRODY_P147_OCCLUSION_EPISTEMICS",
      "elapsed_seconds":round(time.monotonic()-t,3),"condition_scores":stats,
      "exam_count":sum(v["n"] for v in stats.values()),
      "fully_hidden_shape_must_hold":True,
      "partial_occlusion_reconstruction_proven":False,
      "external_physical_sources":False,"native_memory_write":False,
      "canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    (dest/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--minutes",type=int,default=10);p.add_argument("--seed",type=int,default=147)
    p.add_argument("--lessons",type=int,default=150);p.add_argument("--exam-per-condition",type=int,default=1500)
    a=p.parse_args();print(json.dumps(run(a.out,a.minutes,a.seed,a.lessons,a.exam_per_condition),indent=2))
if __name__=="__main__":main()
