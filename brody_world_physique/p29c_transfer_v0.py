"""P2.9c out-of-generator pixel transfer, with no TEST truth feedback.

Distinct rendered generator geometry/appearance; pixel detector is the existing
engineered P2.6 detector, not a learned vision model. TRAIN camera truth calibrates
a provisional anchor, TEST simulator truth is used for scoring after predictions.
"""
from __future__ import annotations
import argparse
import json
from hashlib import sha256
from pathlib import Path
from statistics import mean, median
import random

from .p26_adversarial_pixels_v0 import detect
from .p29_layer_contracts_v0 import PixelObservation, represent, WorkingBelief, route

SCHEMA="BRODY_P29C_TRANSFER_V0"
ARMS=("fixed_id4","trained_anchor","cold_hold")

def fixture(i, *, split, family):
    rng=random.Random(970001+i*743+(0 if split=="train" else 150001))
    # TEST families differ in shape, scale, geometry and nuisance backgrounds,
    # not just the RNG seed. Reliable anchor is independent of pixel positions.
    reliable = 4 if split=="train" else ((4,0,2)[(i//45)%3] if family=="shifted" else 4)
    return {"id":i,"split":split,"family":family,"reliable":reliable,
        "camera":rng.randint(-6,6),"world":rng.randint(-8,8),
        "wrong":(22 if i%2 else -22),
        "lighting": (0,7,-7,12)[i%4],
        "occlusion":i%19==0}

def draw(s,step):
    import cv2,numpy as np
    rng=random.Random(s["id"]*89+step+(0 if s["split"]=="train" else 9211))
    img=np.full((220,380,3),(19,23,27) if s["family"]=="shifted" else (24,27,31),dtype=np.uint8)
    for _ in range(37 if s["family"]=="shifted" else 20):
        x,y=rng.randrange(380),rng.randrange(220)
        img[y,x]=tuple(rng.randrange(256) for _ in range(3))
    bases=(48,101,154,207,260) if s["family"]=="shifted" else (40,90,140,190,240)
    for k,base in enumerate(bases):
        dx=s["camera"]+(0 if k==s["reliable"] else s["wrong"])
        x=base+(dx if step else 0)
        y=52 if s["family"]=="shifted" else 45
        # Intentionally keep fiducial color/area unchanged so detector
        # compatibility is tested independently of semantic reliability.
        cv2.rectangle(img,(x-4,y),(x+4,y+8),(25,215,245),-1)
    center=102+(s["camera"]+s["world"] if step else 0)
    if not (step and s["occlusion"]):
        cv2.circle(img,(center,160 if s["family"]=="shifted" else 133),10,(40,100,245),-1)
    if step and s["lighting"]:
        img=cv2.convertScaleAbs(img,alpha=1,beta=s["lighting"])
    return img

def observe(s):
    a,ma=detect(draw(s,0));b,mb=detect(draw(s,1))
    if a is None or b is None: return None,"HOLD_OBJECT"
    if len(ma)!=5 or len(mb)!=5: return None,"HOLD_REFERENCES"
    return {"apparent":b-a,"shifts":[y-x for x,y in zip(ma,mb)]},"MEASURED_PIXELS"

def choose(scores):
    if not scores: return None
    return min(range(5),key=lambda i:(median(x[i] for x in scores),i))

def calibrate(train=80):
    scores=[];skipped=0
    for i in range(train):
        s=fixture(i,split="train",family="original")
        observed,_=observe(s)
        if observed is None:
            skipped+=1;continue
        # TRAIN-only supervised camera truth; no claimed self-discovery.
        scores.append([abs(x-s["camera"]) for x in observed["shifts"]])
    return {"anchor":choose(scores),"accepted":len(scores),"skipped":skipped}

def execute(train=80,test=180,family="shifted"):
    if not 40<=train<=1000 or not 90<=test<=2000 or family not in ("shifted","stable"):
        raise ValueError("invalid experiment")
    calibration=calibrate(train)
    receipts=[];rows=[]
    for i in range(test):
        spec=fixture(i,split="test",family=family)
        measured,status=observe(spec)
        px=PixelObservation(pair_id="test-"+str(i),source_ref="synthetic-pair-"+str(i),
            ball_apparent_dx=measured["apparent"] if measured is not None else None,
            landmark_shifts=tuple(measured["shifts"]) if measured is not None else (),
            quality=status)
        relation=represent(px,coordinate_frame="camera-relative/test-generator-v1")
        predictions={}
        for arm,anchor in (("fixed_id4",4),("trained_anchor",calibration["anchor"]),("cold_hold",None)):
            if relation.status!="MEASURED_UNVERIFIED" or anchor is None:
                result=None
            else:
                result=relation.apparent_dx-relation.landmark_shifts[anchor]
            predictions[arm]=result
        belief=WorkingBelief(relation.observation_ref,predictions["trained_anchor"],
            "TRAIN_SUPERVISED_NO_TEST_FEEDBACK","WORKING_UNVERIFIED" if predictions["trained_anchor"] is not None else "HOLD",
            (px.source_ref,))
        goal=("generate","explore","explain")[i%3]
        hint=route(goal,belief)
        receipts.append({"id":i,"quality":status,"frame":relation.coordinate_frame,
            "predictions":predictions,"goal":goal,"hint":hint.action_hint,
            "epistemic_status":belief.epistemic_status,"memory_write":False})
        # Test labels are used exclusively for scoring, never state updates.
        rows.append({"id":i,"regime":i//45,"quality":status,
            "errors":{a:abs(v-spec["world"]) if v is not None else None
                      for a,v in predictions.items()}})
    totals={}
    for a in ARMS:
        errors=[r["errors"][a] for r in rows if r["errors"][a] is not None]
        totals[a]={"evaluated":len(errors),"coverage":len(errors)/test,
            "mae_accepted_px":mean(errors) if errors else None,
            "catastrophic_over_10px":sum(v>10 for v in errors)}
    segments={}
    for phase in sorted(set(x["regime"] for x in rows)):
        subset=[x for x in rows if x["regime"]==phase]
        vals=[x["errors"]["trained_anchor"] for x in subset if x["errors"]["trained_anchor"] is not None]
        segments[str(phase)]={"count":len(subset),"coverage":len(vals)/len(subset),
            "mae_accepted_px":mean(vals) if vals else None,
            "catastrophic_over_10px":sum(x>10 for x in vals)}
    return {"schema":SCHEMA,"train":train,"test":test,"family":family,
        "calibration":calibration,"summary":totals,"segments":segments,
        "receipts":receipts,"score_rows":rows,"test_truth_feedback":False,
        "trained_perception":False,"new_generator_family":family=="shifted",
        "physical_generalization_verified":False,"b8_promotion":False,
        "native_memory_write":False,"decision_authority":"KX108_ONLY",
        "verdict":"TRANSFER_DIAGNOSTIC_ONLY"}

def encode(x):
    return (json.dumps(x,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")

def run(out,train=80,test=180,family="shifted"):
    out=Path(out)
    if out.exists() and any(out.iterdir()): raise ValueError("nonempty evidence path")
    result=execute(train,test,family)
    out.mkdir(parents=True,exist_ok=True)
    pre=encode(result["receipts"])
    (out/"predictions_pre_scoring.json").write_bytes(pre)
    result["precommit_sha256"]=sha256(pre).hexdigest()
    (out/"evaluation.json").write_bytes(encode(result))
    return result

def verify(out):
    out=Path(out)
    report=json.loads((out/"evaluation.json").read_text(encoding="utf-8"))
    pre=(out/"predictions_pre_scoring.json").read_bytes()
    if sha256(pre).hexdigest()!=report["precommit_sha256"]: raise ValueError("tampered predictions")
    fresh=execute(report["train"],report["test"],report["family"])
    fresh["precommit_sha256"]=report["precommit_sha256"]
    if encode(fresh)!=encode(report) or pre!=encode(fresh["receipts"]):
        raise ValueError("replay mismatch")
    return True

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--out",required=True)
    a.add_argument("--train",type=int,default=80)
    a.add_argument("--test",type=int,default=180)
    a.add_argument("--family",choices=["shifted","stable"],default="shifted")
    a.add_argument("--verify",action="store_true")
    args=a.parse_args()
    if args.verify: print(json.dumps({"verified":verify(args.out)}))
    else:
        r=run(args.out,args.train,args.test,args.family)
        print(json.dumps({"calibration":r["calibration"],"summary":r["summary"],"segments":r["segments"]}))
if __name__=="__main__": main()
