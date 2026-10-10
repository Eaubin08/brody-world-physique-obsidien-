"""10k adversarial, combinatorial visual probes against archived image sources.

This is a stress harness, not learned semantic/physical perception.
It deliberately exposes errors and scores against independent transformations.
No teacher label provided to proposal, and unseen target is revealed after seal.
"""
from __future__ import annotations
import argparse,hashlib,json,random
from pathlib import Path
from collections import defaultdict
from statistics import mean
from PIL import Image,ImageOps,ImageFilter,ImageEnhance,ImageDraw,ImageChops
from .image_external_source_school_v0 import load_sources,reference
from .drawing_school_v1 import suggest_gestures_from_reference
from .instrument_school_v2 import render_instrument,_gray_pixel_loss
from .fusion_f9_intensive_education_v0 import digest,verify_chain

AXES=("rotate","mirror","scale","translate","blur","contrast","noise","occlude","invert","crop",
      "compound","partial","shifted_background","unknown")
def shift(im,dx,dy):
    return im.transform(im.size,Image.Transform.AFFINE,(1,0,-dx,0,1,-dy),fillcolor=255)
def perturb(im,axis,rng):
    a=im.copy()
    if axis=="rotate":return a.rotate(rng.randint(5,175),fillcolor=255)
    if axis=="mirror":return ImageOps.mirror(a)
    if axis=="scale":
        side=rng.randint(36,56);return ImageOps.pad(a.resize((side,side)),(64,64),color=255)
    if axis=="translate":return shift(a,rng.randint(-12,12),rng.randint(-12,12))
    if axis=="blur":return a.filter(ImageFilter.GaussianBlur(rng.uniform(.5,3)))
    if axis=="contrast":return ImageEnhance.Contrast(a).enhance(rng.uniform(.1,1.8))
    if axis=="noise":
        vals=bytearray(a.convert("L").tobytes())
        for i in range(len(vals)):vals[i]=max(0,min(255,vals[i]+rng.randint(-70,70)))
        return Image.frombytes("L",a.size,bytes(vals))
    if axis=="occlude":
        d=ImageDraw.Draw(a);x=rng.randint(5,40);y=rng.randint(5,40)
        d.rectangle((x,y,x+rng.randint(8,22),y+rng.randint(8,22)),fill=255);return a
    if axis=="invert":return ImageOps.invert(a)
    if axis=="crop":
        x=rng.randint(1,12);y=rng.randint(1,12)
        return ImageOps.fit(a.crop((x,y,64-x,64-y)),(64,64))
    if axis=="compound":
        return perturb(perturb(perturb(a,"rotate",rng),"noise",rng),"occlude",rng)
    if axis=="partial":
        return perturb(perturb(a,"blur",rng),"occlude",rng)
    if axis=="shifted_background":
        return ImageEnhance.Contrast(a).enhance(.3).point(lambda p:max(0,p-35))
    if axis=="unknown":return Image.new("L",(64,64),rng.randint(20,220))
    raise ValueError(axis)

def probe(source,axis,seed):
    rng=random.Random(seed)
    target=perturb(source,axis,rng)
    # Proposal from image pixels only. Neither axis nor target class is input.
    strokes=suggest_gestures_from_reference(target)
    candidate=render_instrument(strokes,"PEN") if strokes else Image.new("L",(64,64),255)
    sealed=hashlib.sha256(candidate.tobytes()).hexdigest()
    loss=_gray_pixel_loss(candidate,target)
    blank=_gray_pixel_loss(Image.new("L",(64,64),255),target)
    # Detect lack of trace but do not claim an unknown scene was identified.
    status="HOLD_NO_TRACE" if not strokes else "DRAWING_CANDIDATE"
    return {"axis_evaluator_only":axis,"status":status,
       "proposal_sha256":sealed,"pixel_loss":loss,"blank_loss":blank,
       "beats_blank":bool(loss<blank),"trace_count":len(strokes),
       "target_present_to_tracer":True,
       "teacher_axis_hidden_from_tracer":True,
       "native_memory_write":False,"canonical_promotion":False,
       "decision_authority":"KX108_ONLY"}

def run(images,out,cases=10000,seed=20261010):
    if cases<140 or cases%len(AXES):raise ValueError("CASES_MUST_BE_MULTIPLE_OF_14")
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EXISTING_EVIDENCE")
    paths=load_sources(images)
    originals=[(p,reference(p),hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]
    rng=random.Random(seed)
    tasks=list(AXES)*(cases//len(AXES));rng.shuffle(tasks)
    # Nonconstant source, vary independently of transformation category.
    root.mkdir(parents=True)
    prev=None;rows=[]
    with (root/"receipts.jsonl").open("x",encoding="utf-8") as f:
        for i,axis in enumerate(tasks,1):
            p,im,sha=originals[rng.randrange(len(originals))]
            result=probe(im,axis,rng.getrandbits(64))
            row={"index":i,"previous":prev,"source_file":p.name,"source_sha256":sha,**result}
            row["digest"]=digest(row);prev=row["digest"]
            f.write(json.dumps(row,sort_keys=True)+"\n");rows.append(row)
    n,tip=verify_chain(root/"receipts.jsonl")
    by={}
    for a in AXES:
        items=[r for r in rows if r["axis_evaluator_only"]==a]
        by[a]={"cases":len(items),"holds":sum(r["status"].startswith("HOLD") for r in items),
               "mean_loss":mean(r["pixel_loss"] for r in items),
               "mean_blank":mean(r["blank_loss"] for r in items),
               "beats_blank":sum(r["beats_blank"] for r in items)}
    report={"schema":"BRODY_IMAGE_ADVERSARIAL_MULTIDIRECTION_10K_V0",
      "cases":n,"source_images":len(paths),"receipt_tip":tip,"axes":by,
      "image_source":"ARCHIVED_INPUTS_NOT_AUTHENTICATED",
      "adversarial_transformations_synthetic":True,
      "visible_reference_supervised_trace":True,
      "tool_fixed":"PEN","learning_updates":False,
      "geometry_3d_proven":False,"physical_prediction_proven":False,
      "semantics_proven":False,"blind_visual_generation_proven":False,
      "native_memory_write":False,"canonical_promotion":False,
      "kernel_mutation":False,"decision_authority":"KX108_ONLY",
      "status":"MULTIDIRECTION_STRESS_TEST_NOT_WORLD_UNDERSTANDING"}
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2)+"\n")
    return report

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--images",required=True);ap.add_argument("--out",required=True)
    ap.add_argument("--cases",type=int,default=10010)
    args=ap.parse_args()
    print(json.dumps(run(args.images,args.out,args.cases),indent=2))
if __name__=="__main__":main()
