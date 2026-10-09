"""P2.5 pixel-first contextual motion challenge.

Paired rendered frames have identical ball image displacement, but different
landmark motion. Neither method reads fixture movement labels before prediction.
OpenCV color detection is engineered, not learned perception.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from hashlib import sha256
from math import hypot
from statistics import median
from .p24_contextual_fluctuation_v0 import interpret, SCHEMA as P24_SCHEMA

SCHEMA="BRODY_P25_PIXEL_CONTEXT_V0"
CASES=(
 ("object_only",10,0,0),
 ("camera_only",0,10,0),
 ("both",6,4,0),
 ("one_corrupt_landmark",6,4,1),
 ("three_corrupt_landmarks",6,4,3),
)
# All five fixtures have the same apparent ball displacement (+10 px).
# Context shifts are measured from images, never supplied by fixture labels.


def render(case, ball_world_dx, camera_dx, corrupted, root):
    import cv2
    import numpy as np
    root.mkdir(parents=True,exist_ok=True)
    files=[]
    for step in (0,1):
        image=np.zeros((220,360,3),dtype=np.uint8)
        image[:]=(24,27,31)
        for i in range(5):
            x=35+i*58+camera_dx*step+(25*step if i<corrupted else 0)
            cv2.rectangle(image,(x-5,45),(x+5,55),(25,215,245),-1)
        ball_x=80+(ball_world_dx+camera_dx)*step
        cv2.circle(image,(ball_x,145),11,(40,100,245),-1)
        file=root/f"{case}_frame_{step}.png"
        if not cv2.imwrite(str(file),image): raise ValueError("image write failed")
        files.append(file)
    return files


def detect(file):
    import cv2
    frame=cv2.imread(str(file))
    if frame is None or frame.shape!=(220,360,3):
        raise ValueError("frame shape unsupported")
    # Saturated orange ball and yellow landmarks, constrained fixture colors.
    ball_mask=cv2.inRange(frame,(35,90,235),(45,110,255))
    landmark_mask=cv2.inRange(frame,(20,210,240),(30,220,250))
    def components(mask,low,high):
        n,_,stats,centers=cv2.connectedComponentsWithStats(mask,8)
        return sorted([float(centers[i][0]) for i in range(1,n)
                       if low<=int(stats[i,cv2.CC_STAT_AREA])<=high])
    balls=components(ball_mask,300,450)
    landmarks=components(landmark_mask,90,145)
    return (balls[0] if len(balls)==1 else None),landmarks


def evaluate_one(files):
    a,land_a=detect(files[0])
    b,land_b=detect(files[1])
    if a is None or b is None:
        return {"object_only":None,"contextual":None,"status":"HOLD_BALL_MISSING"}
    apparent=b-a
    if len(land_a)!=5 or len(land_b)!=5:
        return {"object_only":apparent,"contextual":None,"status":"HOLD_LANDMARKS_MISSING"}
    # Sorted landmark identity is valid only while landmarks do not cross.
    deltas=[y-x for x,y in zip(land_a,land_b)]
    obs={"schema":P24_SCHEMA,"source_kind":"SIMULATED",
         "object_image_displacement":apparent,
         "background_displacements":deltas,"time_delta_s":.25,
         "view_frame":"CAMERA_X","alignment_known":True}
    prediction=interpret(obs)
    return {"object_only":apparent,
            "contextual":prediction["world_displacement"],
            "status":prediction["status"],"measured_context_deltas":deltas}


def run(out):
    out=Path(out).resolve()
    if out.exists() and any(out.iterdir()):raise ValueError("fresh output required")
    out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for name,world,camera,corrupted in CASES:
        files=render(name,world,camera,corrupted,out/"images")
        # Evaluate measured pixels, only then compare against fixture truth.
        response=evaluate_one(files)
        candidate=response["contextual"]
        rows.append({"case":name,"expected_world_dx":world,
                     **response,"ball_only_error":abs(response["object_only"]-world)
                       if response["object_only"] is not None else None,
                     "contextual_error":abs(candidate-world) if candidate is not None else None,
                     "image_sha256":[sha256(p.read_bytes()).hexdigest() for p in files]})
    good=[r for r in rows if r["contextual_error"] is not None]
    report={"schema":SCHEMA,"source_kind":"SIMULATED",
            "raw_pixels_tested":True,"image_detector_preprogrammed":True,
            "learned_vision":False,"world_physics_learned":False,
            "dataset_independent":False,"per_case":rows,
            "context_coverage":len(good)/len(rows),
            "paired_improvement_not_claimed":True,
            "memory_write_allowed":False,"decision_authority":"KX108_ONLY"}
    (out/"evaluation.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return report


def verify(out):
    from tempfile import TemporaryDirectory
    out=Path(out).resolve(strict=True)
    original=json.loads((out/"evaluation.json").read_text(encoding="utf-8"))
    for row in original.get("per_case",[]):
        for index,expected in enumerate(row["image_sha256"]):
            frame=out/"images"/f"{row['case']}_frame_{index}.png"
            if not frame.is_file() or sha256(frame.read_bytes()).hexdigest()!=expected:
                raise ValueError("published pixel evidence mutated")
    with TemporaryDirectory() as tmp:
        fresh=run(Path(tmp)/"replay")
        if fresh!=original:raise ValueError("evaluation replay mismatch")
    return {"verified":True,"cases":len(original["per_case"])}


def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--verify",action="store_true")
    args=p.parse_args(argv)
    print(json.dumps(verify(args.out) if args.verify else {
        "cases":len(run(args.out)["per_case"]),"verified":False}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
