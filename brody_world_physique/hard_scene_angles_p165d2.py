"""P165-D2 HARD+++ adversarial camera/scene test suite.

Image-only evaluator does NOT receive condition labels. This is a test
harness, not a proven world model. Synthetic PIL inputs, no real sensors.
"""
import argparse,hashlib,json,math,random,time
from pathlib import Path
from PIL import Image,ImageDraw
from .image_identity_occlusion_p164 import candidates

W,H=168,96
ANGLES=(-50,-25,0,25,50)
MOTIONS=("still","linear","reverse","jump","accelerate")
OCCLUSIONS=("none","partial","full")
APPEARANCES=("red","blue","change")
BACKGROUNDS=("plain","two_planes","parallax")
# 5*5*3*3*3 = 675 conditions, 2+ seeds each; 1350 exams baseline.
def spec_from_index(i):
    sizes=(len(ANGLES),len(MOTIONS),len(OCCLUSIONS),
           len(APPEARANCES),len(BACKGROUNDS))
    values=[]
    for size in reversed(sizes):
        values.append(i%size);i//=size
    a,m,o,c,b=reversed(values)
    return dict(angle=ANGLES[a],motion=MOTIONS[m],occlusion=OCCLUSIONS[o],
                appearance=APPEARANCES[c],background=BACKGROUNDS[b])
def draw(spec,seed):
    rng=random.Random(seed);frames=[];truth=[]
    start=35+rng.randint(-3,3)
    for t in range(7):
        x=start
        if spec["motion"]=="linear":x+=5*t
        elif spec["motion"]=="reverse":x+=5*t if t<4 else 5*(8-t)
        elif spec["motion"]=="jump":x+=4*t+(20 if t>=4 else 0)
        elif spec["motion"]=="accelerate":x+=t*t
        camera=round(t*spec["angle"]/25)
        x+=camera
        # Independent decoy identical to target in some frames.
        decoy=121-4*t
        im=Image.new("RGB",(W,H),(233,228,216));d=ImageDraw.Draw(im)
        if spec["background"]!="plain":
            d.rectangle((0,65,W,95),fill=(183,197,179))
            d.rectangle((0,21,W,31),fill=(140,163,177))
            for landmark in (12,91,148):
                bgshift=(camera if spec["background"]=="two_planes"
                         else round(.4*camera))
                k=landmark+bgshift
                if 1<=k<W-1:d.rectangle((k-1,10,k+1,14),fill=(54,190,65))
        tint=(215,40,50)
        if spec["appearance"]=="blue" or (spec["appearance"]=="change" and t>=4):
            tint=(28,120,220)
        # y differs with apparent perspective; no 3D truth supplied to model.
        y=48+round(spec["angle"]/20)
        d.ellipse((x-5,y-5,x+5,y+5),fill=tint)
        if t in (2,3,4):
            d.ellipse((decoy-5,48-5,decoy+5,48+5),fill=(215,40,50))
        if spec["occlusion"]=="partial" and t in (3,4):
            d.rectangle((x-5,y-6,x,y+6),fill=(116,117,118))
        elif spec["occlusion"]=="full" and t in (3,4):
            d.rectangle((x-9,y-9,x+9,y+9),fill=(116,117,118))
        frames.append(im);truth.append(float(x))
    return frames,truth

def image_only_evaluate(frames):
    # No condition label, oracle trajectory, or hidden camera value accepted.
    sets=[candidates(im) for im in frames]
    counts=[len(s) for s in sets]
    positions=[s[0][0] if len(s)==1 else None for s in sets]
    missing=sum(v is None for v in positions)
    # Detect visible discontinuities, not auto-label physics.
    visible=[(i,x) for i,x in enumerate(positions) if x is not None]
    jumps=[]
    for (ta,xa),(tb,xb) in zip(visible,visible[1:]):
        if tb==ta+1 and abs(xb-xa)>14:jumps.append(tb)
    if missing>=2:status="HOLD";reason="MULTIPLE_OR_MISSING_CANDIDATES"
    elif jumps:status="NOVELTY_CANDIDATE";reason="VISIBLE_DISCONTINUITY"
    else:status="HOLD";reason="NOT_ENOUGH_CAUSAL_EVIDENCE"
    # A causal world interpretation is *never* promoted by this image-only lab.
    return dict(status=status,reason=reason,counts=counts,
                positions=positions,visible_jumps=jumps,
                unique_identity_proven=False,camera_cause_proven=False)
def run(out,seeds=2,limit=0):
    if not 1<=seeds<=20 or not 0<=limit<=675:raise ValueError("INVALID_BOUNDS")
    target=675 if limit==0 else limit
    root=Path(out)
    if root.exists():raise ValueError("PRESERVE_EVIDENCE")
    root.mkdir(parents=True);start=time.monotonic();groups={}
    with (root/"EXAMS.jsonl").open("w",encoding="utf8") as evidence:
        for j in range(target):
            spec=spec_from_index(j)
            for k in range(seeds):
                images,truth=draw(spec,1009+104729*j+k)
                try:outcome=image_only_evaluate(images)
                finally:
                    for im in images:im.close()
                # truth strictly in evaluation record; never passed to evaluator
                family=spec["occlusion"]+"/"+spec["appearance"]+"/"+spec["background"]
                stats=groups.setdefault(family,dict(n=0,hold=0,novelty=0,
                       unsafe_claim=0,pixel_abs_sum=0.,pixel_pairs=0))
                stats["n"]+=1;stats["hold"]+=int(outcome["status"]=="HOLD")
                stats["novelty"]+=int(outcome["status"]=="NOVELTY_CANDIDATE")
                stats["unsafe_claim"]+=int(outcome["unique_identity_proven"] or
                                           outcome["camera_cause_proven"])
                known=[(a,b) for a,b in zip(outcome["positions"],truth) if a is not None]
                stats["pixel_pairs"]+=len(known)
                stats["pixel_abs_sum"]+=sum(abs(a-b) for a,b in known)
                evidence.write(json.dumps(dict(spec=spec,seed=k,decision=outcome,
                         truth_exam_only=truth))+"\n")
    report=dict(schema="BRODY_P165D2_HARD_PLUS_PLUS_PLUS",
       conditions=target,exams=target*seeds,expected_full_conditions=675,
       groups=groups,run_complete=(target==675),
       inference_receives_fixture_label=False,
       oracle_used_for_inference=False,
       inferred_unique_identity=False,
       synthetic_image_only=True,
       full_contextual_graph_from_pixels=False,
       physical_reasoning_proven=False,
       historical_77_and_p165a_not_replayed=True,
       runtime_seconds=round(time.monotonic()-start,3),
       native_memory_write=False,canonical_promotion=False,
       decision_authority="KX108_ONLY")
    (root/"MASTER_REPORT.json").write_text(json.dumps(report,indent=2),encoding="utf8")
    return report
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True)
    p.add_argument("--seeds",type=int,default=2)
    p.add_argument("--limit",type=int,default=0)
    a=p.parse_args();r=run(a.out,a.seeds,a.limit)
    print(json.dumps({k:v for k,v in r.items() if k!="groups"},indent=2))
    print("Report:",str(Path(a.out)/"MASTER_REPORT.json"))
if __name__=="__main__":main()
