"""P130 broad synthetic transition-transfer benchmark: diversity over repetitions.

Training and exam groups are separate; each sequence renders five images.
Corrected training memories are frozen before heldout scoring. Comparisons
include equal-local-velocity baseline, errors, abstention and context family.
"""
from __future__ import annotations
import argparse,json,math,random
from pathlib import Path
from PIL import Image,ImageDraw
from .image_context_transition_transfer_v1 import forecast,correct
from .image_multihypothesis_motion_memory_v1 import read,write

FAMILIES=("steady","speed_up","slow_down","reversal","stop","start")
def sequence(kind,axis,offset):
    if kind=="steady":v=[9,15,21,27,33]
    elif kind=="speed_up":v=[9,12,18,27,39]
    elif kind=="slow_down":v=[7,17,25,31,35]
    elif kind=="reversal":v=[12,20,28,24,18]
    elif kind=="stop":v=[10,17,24,24,24]
    else:v=[20,20,20,24,30]
    v=[max(5,min(58,round(x+offset))) for x in v]
    return [(30,x) if axis=="vertical" else (x,30) for x in v]
def frame(path,xy,nonce):
    im=Image.new("RGB",(64,64),"white")
    x,y=xy;ImageDraw.Draw(im).ellipse((x-3,y-3,x+3,y+3),fill=(25,25,25))
    im.putpixel((0,0),(240+nonce%12,240+nonce%12,240+nonce%12))
    im.save(path)
def run(out,per_family=8,seed=129):
    dest=Path(out)
    if dest.exists():raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    if not (2<=per_family<=100):raise ValueError("INVALID_CASES_PER_FAMILY")
    rng=random.Random(seed)
    dest.mkdir(parents=True)
    definitions=[]
    for family in FAMILIES:
        for axis in ("vertical","horizontal"):
            for n in range(per_family):
                split="train" if n<per_family//2 else "exam"
                group=f"{family}_{axis}_{n:03d}"
                offset=rng.choice((-2,-1,0,1,2))
                trajectory=sequence(family,axis,offset)
                root=dest/"frames"/group;root.mkdir(parents=True)
                paths=[]
                for i,xy in enumerate(trajectory):
                    p=root/f"{i}.png";frame(p,xy,(len(definitions)*5+i)%12);paths.append(str(p.resolve()))
                manifest={"source_group":group,"observations":[{"t":i,"file":paths[i]} for i in range(4)],"predict_t":4}
                definitions.append({"group":group,"split":split,"family":family,"axis":axis,
                   "manifest":manifest,"actual":paths[4]})
    train=[x for x in definitions if x["split"]=="train"]
    exam=[x for x in definitions if x["split"]=="exam"]
    previous=None
    for i,e in enumerate(train):
        spec=dest/f"lesson_{i:03d}.json";write(spec,e["manifest"])
        p=dest/f"train_prediction_{i:03d}";c=dest/f"train_correction_{i:03d}"
        forecast(spec,p,previous)
        correct(p/"sealed_forecast.json",e["actual"],c,previous)
        previous=c/"candidate_transition_memory.json"
    from .image_context_transition_transfer_v1 import analyze,track,propose,load
    memory=load(previous)
    results=[]
    for e in exam:
        obs=track(e["manifest"]);t=e["manifest"]["predict_t"]
        baseline=propose(obs,{"episodes":[]},t,e["group"])
        learned=propose(obs,memory,t,e["group"])
        truth=analyze(e["actual"])
        def err(p):return math.hypot(p["x"]-truth["x"],p["y"]-truth["y"])
        a=err(baseline["proposal"]);b=err(learned["proposal"])
        results.append({"family":e["family"],"axis":e["axis"],"group":e["group"],
            "event":learned["context"]["event"],
            "baseline_error_px":round(a,5),"memory_error_px":round(b,5),
            "advantage_px":round(a-b,5),"memory_mode":learned["mode"],
            "matched_groups":learned["matched_groups"]})
    families={}
    for f in FAMILIES:
        rows=[r for r in results if r["family"]==f]
        families[f]={"cases":len(rows),
           "baseline_mean_px":round(sum(r["baseline_error_px"] for r in rows)/len(rows),5),
           "memory_mean_px":round(sum(r["memory_error_px"] for r in rows)/len(rows),5),
           "improved":sum(r["advantage_px"]>0.01 for r in rows),
           "worsened":sum(r["advantage_px"]< -0.01 for r in rows),
           "equal":sum(abs(r["advantage_px"])<=0.01 for r in rows)}
    report={"schema":"BRODY_SYNTHETIC_CONTEXT_TRANSITION_BENCHMARK_P130",
      "synthetic_only":True,"source_independence_real_world_proven":False,
      "train_cases":len(train),"heldout_cases":len(exam),
      "axis_types":["vertical","horizontal"],"families":families,
      "memory_used":sum(r["memory_mode"]=="CANDIDATE" for r in results),
      "mean_advantage_px":round(sum(r["advantage_px"] for r in results)/len(results),5),
      "native_memory_write":False,"canonical_promotion":False,
      "decision_authority":"KX108_ONLY"}
    write(dest/"EXAM_CASES.json",results)
    write(dest/"MASTER_REPORT.json",report)
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True)
    p.add_argument("--per-family",type=int,default=8);p.add_argument("--seed",type=int,default=129)
    a=p.parse_args();print(json.dumps(run(a.out,a.per_family,a.seed),indent=2))
if __name__=="__main__":main()
