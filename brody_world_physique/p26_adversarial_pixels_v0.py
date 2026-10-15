"""P2.6 adversarial pixel benchmark: 480 independent synthetic two-frame scenarios.

Engineered color detectors, fixed median gate, NO learning and NO world proof.
Prediction reads PNG pixels; manifest truth is used only by the scorer AFTER
predictions have been written and closed. Evidence includes sample mosaic only.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
import random
from statistics import mean,median

SCHEMA="BRODY_P26_ADVERSARIAL_PIXELS_V0"
TOTAL_DEFAULT=480


def scenario(seed:int):
    r=random.Random(seed*1699+37)
    world=r.randint(-12,12)
    camera=r.randint(-10,10)
    corrupted=r.choice([0,0,0,1,2,3,4])
    illumination=r.choice([0,0,0,10,25,-10])
    jitter=r.choice([0,0,0,1,2])
    occlude=r.random()<.08
    return {"id":seed,"world":world,"camera":camera,"corrupted":corrupted,
            "illumination":illumination,"jitter":jitter,"occlude":occlude}


def render(spec,step):
    import cv2,numpy as np
    image=np.full((190,340,3),(24,27,31),dtype=np.uint8)
    # independent nuisance pixels; never use simulation labels to score
    r=random.Random(spec["id"]*71+step)
    for _ in range(30):
        x=r.randint(0,339);y=r.randint(0,189)
        image[y,x]=(r.randint(0,255),r.randint(0,255),r.randint(0,255))
    x_base=[40,90,140,190,240]
    for i,x in enumerate(x_base):
        shift=(26 if i<spec["corrupted"] else 0)*step
        j=(r.randint(-spec["jitter"],spec["jitter"]) if step else 0)
        px=x+(spec["camera"]+shift)*step+j
        cv2.rectangle(image,(px-4,45),(px+4,53),(25,215,245),-1)
    ballx=88+(spec["world"]+spec["camera"])*step
    if not (step and spec["occlude"]):
        cv2.circle(image,(ballx,133),10,(40,100,245),-1)
    if step and spec["illumination"]:
        # Intentionally broad illumination shift: can break strict detectors.
        image=cv2.convertScaleAbs(image,alpha=1,beta=spec["illumination"])
    return image


def detect(frame):
    import cv2
    ballmask=cv2.inRange(frame,(35,90,235),(45,110,255))
    landmarkmask=cv2.inRange(frame,(20,210,240),(30,220,250))
    def positions(mask,minarea,maxarea):
        n,_,stats,centers=cv2.connectedComponentsWithStats(mask,8)
        xs=[float(centers[k][0]) for k in range(1,n)
            if minarea<=int(stats[k,cv2.CC_STAT_AREA])<=maxarea]
        return sorted(xs)
    ball=positions(ballmask,280,360)
    landmarks=positions(landmarkmask,65,95)
    return (ball[0] if len(ball)==1 else None),landmarks


def predict(a,b):
    ball0,refs0=detect(a);ball1,refs1=detect(b)
    if ball0 is None or ball1 is None:
        return {"baseline":None,"contextual":None,"status":"HOLD_OBJECT"}
    apparent=ball1-ball0
    if len(refs0)!=5 or len(refs1)!=5:
        return {"baseline":apparent,"contextual":None,"status":"HOLD_REFERENCES"}
    shifts=[y-x for x,y in zip(refs0,refs1)]
    central=median(shifts)
    inliers=sum(abs(x-central)<=2.0 for x in shifts)
    if inliers<4:
        return {"baseline":apparent,"contextual":None,"status":"HOLD_CONFLICT"}
    return {"baseline":apparent,"contextual":apparent-central,
            "status":"CANDIDATE","measured_shifts":shifts}


def _hash(b):
    return sha256(b).hexdigest()


def run(out:Path,count:int=TOTAL_DEFAULT):
    import cv2,numpy as np
    if not 20<=count<=2000:raise ValueError("count outside 20..2000")
    out=Path(out).resolve()
    if out.exists() and any(out.iterdir()):raise ValueError("output must be new")
    out.mkdir(parents=True,exist_ok=True)
    (out/"images").mkdir()
    # Deterministic family split: early cases are dev observations,
    # latter cases are evaluation fixtures, not independent external data.
    specs=[scenario(i) for i in range(count)]
    receipts=out/"predictions_pre_scoring.jsonl"
    # No truths written into receipt; each image pair is processed independently.
    results=[]; examples=[]
    with receipts.open("w",encoding="utf-8") as handle:
        for spec in specs:
            a=render(spec,0);b=render(spec,1)
            proposal=predict(a,b)
            prediction={"id":spec["id"],**proposal}
            handle.write(json.dumps(prediction,sort_keys=True)+"\n")
            # Record a few real visual samples rather than hundreds of PNGs.
            if len(examples)<12 and (spec["id"]%max(1,count//12)==0):
                examples.append(np.hstack((a,b)))
            results.append((spec,proposal))
        handle.flush()
    import os
    # File closed (sealed) before reading any reference target for scoring.
    forecast_hash=_hash(receipts.read_bytes())
    rows=[]
    for spec,proposal in results:
        truth=spec["world"]
        baseline=proposal["baseline"];context=proposal["contextual"]
        rows.append({"id":spec["id"],"group":"DEV" if spec["id"]<count//4 else "TEST",
                     "condition":{"corrupted":spec["corrupted"],"illumination":spec["illumination"],
                                  "jitter":spec["jitter"],"occluded":spec["occlude"]},
                     "truth_world_dx":truth,"status":proposal["status"],
                     "baseline_abs_error":abs(baseline-truth) if baseline is not None else None,
                     "context_abs_error":abs(context-truth) if context is not None else None})
    if examples:
        # Rows are concatenated along Y; each pair along X.
        mosaic=np.vstack(examples)
        cv2.imwrite(str(out/"images"/"sample_pairs.png"),mosaic)
    test=[x for x in rows if x["group"]=="TEST"]
    matched=[x for x in test if x["baseline_abs_error"] is not None and x["context_abs_error"] is not None]
    accepted=[x for x in test if x["context_abs_error"] is not None]
    def avg(name,part):
        vals=[x[name] for x in part if x[name] is not None]
        return mean(vals) if vals else None
    report={"schema":SCHEMA,"count":count,"test_count":len(test),
            "pre_scoring_predictions_sha256":forecast_hash,
            "source_kind":"SIMULATED","pixels_extracted":True,
            "detector_engineered":True,"learned":False,
            "source_independent":False,"fresh_generators_held_out":False,
            "test_context_coverage":len(accepted)/len(test),
            "test_mean_baseline_on_all_baseline_cases":avg("baseline_abs_error",test),
            "test_matched_n":len(matched),
            "test_matched_baseline_error":avg("baseline_abs_error",matched),
            "test_matched_context_error":avg("context_abs_error",matched),
            "test_mean_context_accepted":avg("context_abs_error",accepted),
            "rows":rows,"verdict":"DIAGNOSTIC_ONLY",
            "native_memory_write_allowed":False,"decision_authority":"KX108_ONLY"}
    (out/"evaluation.json").write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return report


def verify(out:Path):
    from tempfile import TemporaryDirectory
    out=Path(out).resolve(strict=True)
    original=json.loads((out/"evaluation.json").read_text(encoding="utf-8"))
    if original["pre_scoring_predictions_sha256"]!=_hash((out/"predictions_pre_scoring.jsonl").read_bytes()):
        raise ValueError("prediction receipts changed")
    with TemporaryDirectory() as tmp:
        recreated=run(Path(tmp)/"replay",int(original["count"]))
        if original!=recreated:raise ValueError("P2.6 report replay mismatch")
        if _hash((out/"images"/"sample_pairs.png").read_bytes())!=_hash((Path(tmp)/"replay"/"images"/"sample_pairs.png").read_bytes()):
            raise ValueError("P2.6 sample image mismatch")
        if (out/"predictions_pre_scoring.jsonl").read_bytes()!=(Path(tmp)/"replay"/"predictions_pre_scoring.jsonl").read_bytes():
            raise ValueError("P2.6 prediction replay mismatch")
    return {"verified":True,"count":original["count"]}


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--count",type=int,default=TOTAL_DEFAULT)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args(argv)
    report=verify(args.out) if args.verify else run(args.out,args.count)
    print(json.dumps({k:report[k] for k in ("verified","count","test_count","test_matched_n",
             "test_matched_baseline_error","test_matched_context_error",
             "test_context_coverage","verdict") if k in report}))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
