"""P2.9h: same-source, same-horizon precommitted position ablations.

This compares spatial persistence, temporal constant-velocity, and the
original experiential predictor under frozen TRAIN memory. No new model,
no test feedback, no use of future before all proposals are sealed.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from math import hypot
from statistics import mean
from hashlib import sha256
from .world_transfer_probe_v1 import _load_probe_suite,iter_video_points,propose_with_conflict_gate
from .experiential_video_v0 import acquire_experiences
from .video_observation_v0 import video_sha256

SCHEMA="BRODY_P29H_PRECOMMITTED_POSITION_ABLATION_V0"
ARMS=("A0_LAST_POSITION","A1_SPATIAL_DELTA","A2_TEMPORAL_VELOCITY",
      "A4_FROZEN_MEMORY","A5_NO_MEMORY","A6_ONE_EXPERIENCE","A6_FOUR_EXPERIENCES")

def predict(history,memory):
    a,b,c=history
    dt=c.time_s-b.time_s
    horizon=dt
    if dt<=0:raise ValueError("time")
    raw={
       "A0_LAST_POSITION":[c.x,c.y],
       "A1_SPATIAL_DELTA":[c.x+(c.x-b.x),c.y+(c.y-b.y)],
       "A2_TEMPORAL_VELOCITY":[c.x+(c.x-b.x)/dt*horizon,
                               c.y+(c.y-b.y)/dt*horizon],
    }
    for name,mem in (("A4_FROZEN_MEMORY",memory),
                     ("A5_NO_MEMORY",()),
                     ("A6_ONE_EXPERIENCE",memory[:1]),
                     ("A6_FOUR_EXPERIENCES",memory[:4])):
        response=propose_with_conflict_gate(tuple(mem),history)
        raw[name]=response["candidate_xy"]
    return raw

def evaluate(suite):
    train,test=_load_probe_suite(Path(suite))
    frozen=[]
    for _,video,digest in train:
        observations=list(iter_video_points(video,digest,camera_mode="anchored"))
        if any(x is None for x in observations):raise ValueError("missing training evidence")
        frozen.extend(acquire_experiences(observations,digest))
    frozen=tuple(frozen)
    proposals=[];scores=[]
    for name,video,digest in test:
        if video_sha256(video)!=digest:raise ValueError("video hash changed")
        history=[];pending=None;frame_num=0
        for obs in iter_video_points(video,digest,camera_mode="anchored"):
            # Score *only after* all candidate predictions were precommitted
            if pending is not None:
                for arm,xy in pending["predictions"].items():
                    scores.append({"clip":name,"frame":frame_num,"arm":arm,
                        "error_px":hypot(xy[0]-obs.x,xy[1]-obs.y) if xy is not None and obs else None})
                pending=None
            frame_num+=1
            if obs is None:
                history.clear()
                continue
            history.append(obs)
            if len(history)>=3 and frame_num<12:
                previous=history[-3:]
                proposed=predict(previous,frozen)
                receipt={"clip":name,"source_sha256":digest,
                         "history_refs":[p.source_ref for p in previous],
                         "future_frame":frame_num*6,
                         "predictions":proposed}
                proposals.append(receipt)
                pending=receipt
        if pending is not None:raise ValueError("dangling prediction")
    result={}
    for arm in ARMS:
        rows=[x for x in scores if x["arm"]==arm]
        valid=[x["error_px"] for x in rows if x["error_px"] is not None]
        result[arm]={"cases":len(rows),"accepted":len(valid),
                     "coverage":len(valid)/len(rows) if rows else 0,
                     "mae_accepted_px":mean(valid) if valid else None,
                     "errors_over_10px":sum(x>10 for x in valid)}
    return {"schema":SCHEMA,"suite_sha256":sha256(Path(suite).read_bytes()).hexdigest(),
            "train_experience_count":len(frozen),"test_source_count":len(test),
            "shared_test_cases":len(scores)//len(ARMS),
            "arms":result,"precommit":proposals,"scores":scores,
            "image_generation_scored":False,"a3_visual_spatial_implemented":False,
            "a4_joint_multirepresentation_proven":False,
            "time_spatial_same_under_fixed_sampling":True,
            "test_feedback_used_for_learning":False,"native_memory_write":False,
            "decision_authority":"KX108_ONLY"}

def save(out,suite):
    p=Path(out)
    if p.exists():raise ValueError("output exists")
    result=evaluate(suite)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def verify(out,suite):
    saved=json.loads(Path(out).read_text(encoding="utf-8"))
    if saved!=evaluate(suite):raise ValueError("ablation changed on replay")
    return {"verified":True,"cases":saved["shared_test_cases"]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--suite",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    r=verify(args.out,args.suite) if args.verify else save(args.out,args.suite)
    print(json.dumps(r if args.verify else {"cases":r["shared_test_cases"],"arms":r["arms"]}))
if __name__=="__main__":main()
