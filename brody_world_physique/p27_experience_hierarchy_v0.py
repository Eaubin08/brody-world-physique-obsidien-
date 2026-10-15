"""P2.7 same-pixel ablation: consensus, hierarchy, TRAIN-calibrated experience.

Synthetic and supervised TRAIN camera displacement. NOT self-learning world physics.
TEST truth is scored only after all TEST predictions have been committed.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
import random
from statistics import mean, median

from .p26_adversarial_pixels_v0 import render, detect

SCHEMA="BRODY_P27_EXPERIENCE_HIERARCHY_V0"
ARMS=("majority","hierarchy","experience","hierarchy_experience")


def make_scene(idx:int, *, train:bool):
    rng=random.Random(77191+idx*331)
    cam=rng.randint(-8,8)
    world=rng.randint(-10,10)
    # Earlier marker IDs are less trustworthy across scenes; final marker
    # remains reliable. The TEST pattern differs from TRAIN but shares this
    # intentionally learnable regularity.
    corrupt=rng.choice([0,1,2,3,4] if train else [0,2,3,4,4,4])
    return {"id":idx,"world":world,"camera":cam,"corrupted":corrupt,
            "illumination":0,"jitter":rng.choice([0,1]),"occlude":False}


def measure(spec):
    a=render(spec,0);b=render(spec,1)
    ball0,marks0=detect(a)
    ball1,marks1=detect(b)
    if ball0 is None or ball1 is None or len(marks0)!=5 or len(marks1)!=5:
        return None
    return {"apparent":ball1-ball0,
            "landmarks":[y-x for x,y in zip(marks0,marks1)]}


def train_reliability(train):
    residual=[[] for _ in range(5)]
    for spec in train:
        measured=measure(spec)
        if measured is None:
            continue
        # Explicitly supervised calibration: simulator camera truth provided
        # for TRAIN only. NO claim of autonomous physical discovery.
        for i,d in enumerate(measured["landmarks"]):
            residual[i].append(abs(d-spec["camera"]))
    return [median(r) if r else 1e9 for r in residual]


def predict(measurement, reliability):
    if measurement is None:
        return {arm:None for arm in ARMS}
    apparent=measurement["apparent"]
    shifts=measurement["landmarks"]
    center=median(shifts)
    agree=sum(abs(x-center)<=2 for x in shifts)>=4
    majority=apparent-center if agree else None
    # The hierarchy is the previous frozen assumption that the last marker
    # has the highest fixed rank. No retrospective truth may influence it.
    hierarchy=apparent-shifts[-1]
    # Experience alone uses learned reliability, no fixed ID priority.
    best=min(range(5),key=lambda i:(reliability[i],i))
    experiential=apparent-shifts[best]
    # Combined: evidence needs at least two reliable landmarks, else HOLD.
    usable=[i for i,x in enumerate(reliability) if x<=1.0]
    combined=apparent-median([shifts[i] for i in usable]) if len(usable)>=2 else None
    return {"majority":majority,"hierarchy":hierarchy,
            "experience":experiential,"hierarchy_experience":combined}


def run(out:Path,train_count:int=120,test_count:int=240):
    from .p26_adversarial_pixels_v0 import render
    import cv2,numpy as np
    if not (20<=train_count<=1000 and 20<=test_count<=2000):
        raise ValueError("counts out of permitted range")
    out=Path(out).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("new output directory required")
    out.mkdir(parents=True,exist_ok=True)
    (out/"images").mkdir()
    train=[make_scene(i,train=True) for i in range(train_count)]
    reliability=train_reliability(train)
    tests=[make_scene(100000+i,train=False) for i in range(test_count)]
    receipts=out/"predictions_pre_scoring.jsonl"
    pairs=[];sealed=[]
    with receipts.open("w",encoding="utf-8") as handle:
        for spec in tests:
            measurement=measure(spec)
            predictions=predict(measurement,reliability)
            record={"id":spec["id"],"prediction":predictions,
                    "observed":measurement}
            handle.write(json.dumps(record,sort_keys=True)+"\n")
            sealed.append((spec,predictions))
            if len(pairs)<8:
                pairs.append(np.hstack((render(spec,0),render(spec,1))))
        handle.flush()
    # Scoring reads synthetic TEST truth only after closing the prediction file.
    receipt_sha=sha256(receipts.read_bytes()).hexdigest()
    rows=[]
    for spec,predictions in sealed:
        rows.append({"id":spec["id"],"corrupted":spec["corrupted"],
                     "truth_world_dx":spec["world"],
                     "errors":{arm:abs(v-spec["world"]) if v is not None else None
                               for arm,v in predictions.items()}})
    summary={}
    for arm in ARMS:
        vals=[r["errors"][arm] for r in rows if r["errors"][arm] is not None]
        summary[arm]={"coverage":len(vals)/len(rows),
                      "evaluated":len(vals),
                      "mean_error_px":mean(vals) if vals else None,
                      "catastrophic_over_10px":sum(x>10 for x in vals)}
    matched=[r for r in rows if all(r["errors"][arm] is not None for arm in ARMS)]
    matched_summary={arm:mean(r["errors"][arm] for r in matched) if matched else None for arm in ARMS}
    if pairs:
        if not cv2.imwrite(str(out/"images"/"train_test_pairs.png"),np.vstack(pairs)):
            raise ValueError("failed image")
    report={"schema":SCHEMA,"source_kind":"SIMULATED",
            "train_count":train_count,"test_count":test_count,
            "training_supervised_camera_truth":True,
            "reliability_by_landmark":reliability,
            "test_prediction_sha256":receipt_sha,
            "arm_summary":summary,"matched_all_arm_count":len(matched),
            "matched_all_arm_error":matched_summary,"rows":rows,
            "learned_visual_perception":False,"learned_physics":False,
            "same_source_generator":True,"independent_real_world_validation":False,
            "verdict":"EXPERIMENTAL_DIAGNOSTIC_ONLY",
            "native_memory_write_allowed":False,"decision_authority":"KX108_ONLY"}
    (out/"evaluation.json").write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return report


def verify(out:Path):
    from tempfile import TemporaryDirectory
    out=Path(out).resolve(strict=True)
    original=json.loads((out/"evaluation.json").read_text(encoding="utf-8"))
    if original["test_prediction_sha256"]!=sha256((out/"predictions_pre_scoring.jsonl").read_bytes()).hexdigest():
        raise ValueError("tampered predictions")
    with TemporaryDirectory() as tmp:
        fresh=run(Path(tmp)/"replay",original["train_count"],original["test_count"])
        for name in ("evaluation.json","predictions_pre_scoring.jsonl"):
            if (Path(tmp)/"replay"/name).read_bytes()!=(out/name).read_bytes():
                raise ValueError("replay mismatch: "+name)
        if (Path(tmp)/"replay"/"images"/"train_test_pairs.png").read_bytes()!=(out/"images"/"train_test_pairs.png").read_bytes():
            raise ValueError("image replay mismatch")
    return {"verified":True,"test_count":original["test_count"]}


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--train",type=int,default=120)
    p.add_argument("--test",type=int,default=240)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args(argv)
    result=verify(args.out) if args.verify else run(args.out,args.train,args.test)
    print(json.dumps({"verified":result.get("verified",False),
      "test_count":result["test_count"],
      "arm_summary":result.get("arm_summary"),
      "matched_all_arm_count":result.get("matched_all_arm_count")}))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
