"""P134 reciprocal perception/generation: learned masks, teacher feedback and holdout.

Training extracts connected foreground components from RGB images; a primitive
shape memory is built from actual example masks, not hardcoded draw commands.
Exam predictions are frozen before truth is scored; unknown geometries HOLD.
No autonomous semantics, 3D, or proven physical understanding.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from collections import deque
from pathlib import Path
from PIL import Image
from .fusion_f9_intensive_education_v0 import digest

W=64
def save(p,obj):Path(p).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def scene(path):
    with Image.open(path) as input_image:
        im=input_image.convert("RGB").resize((W,W))
    px=im.load();fg={(x,y) for y in range(W) for x in range(W) if min(px[x,y])<220}
    components=[]
    while fg:
        start=min(fg);fg.remove(start);q=deque([start]);pts=[]
        while q:
            x,y=q.popleft();pts.append((x,y))
            for v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if v in fg:fg.remove(v);q.append(v)
        if len(pts)<4:continue
        x0=min(x for x,y in pts);y0=min(y for x,y in pts)
        x1=max(x for x,y in pts);y1=max(y for x,y in pts)
        w=x1-x0+1;h=y1-y0+1
        cols=[px[x,y] for x,y in pts]
        rgb=tuple(round(sum(c[i] for c in cols)/len(cols)) for i in range(3))
        mask=sorted([[x-x0,y-y0] for x,y in pts])
        components.append({"bbox":[x0,y0,x1,y1],"size":[w,h],"rgb":rgb,"mask":mask,
                           "area":len(pts)})
    components.sort(key=lambda p:(p["bbox"][0],p["bbox"][1]))
    return {"components":components,"count":len(components),
            "file_sha256":hashlib.sha256(Path(path).read_bytes()).hexdigest()}
def shape_signature(part):
    w,h=part["size"]
    return {"aspect":round(w/h,3),"fill":round(part["area"]/(w*h),3)}
def distance(a,b):
    x=shape_signature(a);y=shape_signature(b)
    return abs(math.log(x["aspect"]/y["aspect"]))+abs(x["fill"]-y["fill"])
def paint(parts,output):
    im=Image.new("RGB",(W,W),"white");pixels=im.load()
    for obj in parts:
        x0,y0,x1,y1=obj["bbox"];rgb=tuple(obj["rgb"])
        w,h=obj["size"];seen=set()
        for x,y in obj["mask"]:
            xx=x0+x;yy=y0+y
            if 0<=xx<W and 0<=yy<W and xx<=x1 and yy<=y1:
                pixels[xx,yy]=rgb;seen.add((xx,yy))
    im.save(output)
def compare(pred,actual):
    with Image.open(pred) as ip,Image.open(actual) as it:
        a=ip.convert("RGB").resize((W,W));b=it.convert("RGB").resize((W,W))
    ap=a.tobytes();bp=b.tobytes()
    return {"mae_rgb":round(sum(abs(x-y) for x,y in zip(ap,bp))/len(ap),5),
            "identical_pixel_ratio":round(sum(ap[i:i+3]==bp[i:i+3] for i in range(0,len(ap),3))/(W*W),5)}
def memory_fresh():
    return {"schema":"BRODY_RECIPROCAL_SHAPE_MEMORY_P134","prototypes":[],
     "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
def learn(mem,part,group):
    sig=shape_signature(part)
    # At most one exemplar per physical source group per signature.
    if any(q["group"]==group and q["signature"]==sig for q in mem["prototypes"]):return False
    mem["prototypes"].append({"group":group,"signature":sig,"part":part})
    return True
def hypothesize(mem,obs,group):
    items=[];confidence=[]
    for part in obs["components"]:
        ranked=sorted([(distance(part,e["part"]),e) for e in mem["prototypes"] if e["group"]!=group],key=lambda x:x[0])
        if not ranked:
            return {"mode":"DOUBT","reason":"NO_SOURCE_INDEPENDENT_EXEMPLARS","parts":[]}
        cost,best=ranked[0]
        # Matching is shape-only; target geometry/position is observed but mask comes from memory.
        eligible=[e for val,e in ranked if val<=0.12 and e["signature"]==best["signature"]]
        if cost>0.12 or len({e["group"] for e in eligible})<2:
            return {"mode":"DOUBT","reason":"SHAPE_NOT_REPLICATED","parts":[]}
        proto=best["part"]
        ow,oh=proto["size"];nw,nh=part["size"]
        mask=sorted(set((min(nw-1,round(x*(nw-1)/max(ow-1,1))),
                         min(nh-1,round(y*(nh-1)/max(oh-1,1)))) for x,y in proto["mask"]))
        items.append({**part,"mask":[list(p) for p in mask]})
        confidence.append(round(cost,5))
    return {"mode":"CANDIDATE","reason":"MULTISOURCE_SHAPE_MEMORY",
        "parts":items,"matching_costs":confidence}
def run(manifest,out):
    target=Path(out)
    if target.exists():raise ValueError("PRESERVE_EVIDENCE")
    rows=json.loads(Path(manifest).read_text(encoding="utf-8-sig"))
    if not isinstance(rows,list) or not rows:raise ValueError("EMPTY_CORPUS")
    train=[r for r in rows if r.get("split")=="train"]
    exams=[r for r in rows if r.get("split")=="exam"]
    if not train or not exams:raise ValueError("TWO_SPLITS_REQUIRED")
    if {r["group"] for r in train}&{r["group"] for r in exams}:raise ValueError("SOURCE_GROUP_LEAK")
    observed=[(r,scene(r["file"])) for r in rows]
    hashes={}
    for r,obs in observed:
        h=obs["file_sha256"]
        if h in hashes and hashes[h]!=r["split"]:raise ValueError("EXACT_IMAGE_LEAK")
        hashes[h]=r["split"]
    target.mkdir(parents=True)
    mem=memory_fresh();training=[]
    for r,obs in observed:
        if r["split"]!="train":continue
        # Teacher feedback here is the training image itself, always disclosed.
        baseline=target/f"train_{len(training):03d}_initial.png"
        paint([{"bbox":p["bbox"],"size":p["size"],"rgb":p["rgb"],
                "mask":[[x,y] for x in range(p["size"][0]) for y in range(p["size"][1])]} for p in obs["components"]],baseline)
        initial=compare(baseline,r["file"])
        corrected=target/f"train_{len(training):03d}_corrected.png"
        paint(obs["components"],corrected)
        final=compare(corrected,r["file"])
        for part in obs["components"]:learn(mem,part,r["group"])
        training.append({"group":r["group"],"initial_mae":initial["mae_rgb"],"corrected_mae":final["mae_rgb"],"source":"teacher_image_mask"})
    results=[]
    for r,obs in observed:
        if r["split"]!="exam":continue
        prediction=hypothesize(mem,obs,r["group"])
        record={"group":r["group"],"mode":prediction["mode"],"reason":prediction["reason"]}
        if prediction["mode"]=="CANDIDATE":
            generated=target/f"heldout_{len(results):03d}.png"
            paint(prediction["parts"],generated)
            record["quality"]=compare(generated,r["file"])
            record["image"]=str(generated)
        else:record["quality"]=None
        results.append(record)
    snapshot={**mem,"digest":digest(mem)}
    save(target/"candidate_shape_memory.json",snapshot)
    report={"schema":"BRODY_RECIPROCAL_LEARNING_P134","training":training,"exam":results,
     "train_count":len(train),"exam_count":len(exams),
     "exam_candidates":sum(e["mode"]=="CANDIDATE" for e in results),
     "exam_holds":sum(e["mode"]=="DOUBT" for e in results),
     "correction_applied_before_exam":False,
     "independent_real_world_proven":False,"source_groups_self_declared":True,
     "native_memory_write":False,"canonical_promotion":False,"decision_authority":"KX108_ONLY"}
    save(target/"MASTER_REPORT.json",report);return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--manifest",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();print(json.dumps(run(a.manifest,a.out),indent=2))
if __name__=="__main__":main()
