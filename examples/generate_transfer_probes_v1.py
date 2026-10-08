"""Controlled synthetic transfer probes. Fixture physics is NOT learner input.

All scenes have one saturated object, a fixed cyan scene fiducial, and a
brown/gray background. Some TEST scenes alter appearance, move the camera,
hide the target, or introduce contradictory/future surprises.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import sin
from pathlib import Path


TRAIN = ("train_01", "train_02", "train_03", "train_04", "train_05", "train_06")
TEST = ("test_01", "test_02", "test_03", "test_04", "test_05", "test_06")
FPS, FRAMES, WIDTH, HEIGHT = 24, 72, 480, 320


def position(case: str, t: float) -> tuple[float, float]:
    """Hidden fixture-generation knowledge, never imported by the learner."""
    if case in ("train_01", "test_01", "test_03"):
        return 92 + 15*t, 43 + 24*t + 18*t*t
    if case in ("train_02", "test_02", "test_04", "test_06"):
        return 80 + 63*t, 214 + 6*t + (65 if case=="test_04" and t >= 1.5 else 0)
    if case=="train_03":
        return 260+35*sin(t*1.45), 115+30*sin(t*1.8)
    if case=="train_04":
        if t<1.3:
            return 170+10*t, 51+82*t+22*t*t
        q=t-1.3
        return 183+10*q, 51+82*1.3+22*1.3**2-83*q+23*q*q
    if case in ("train_05","train_06","test_05"):
        if t <= .5:
            return 100+36*t, 103+12*t
        q=t-.5
        jump=35 if case=="train_05" else (-35 if case=="train_06" else 0)
        return 118+36*q, 109+12*q+jump
    raise ValueError("unknown case")


def appearance(case: str) -> tuple[str, tuple[int,int,int]]:
    if case in ("test_01","test_03","test_04"):
        return "square", (255,95,40)  # BLUE in BGR
    if case in ("test_02","test_05"):
        return "triangle", (60,220,70) # GREEN in BGR
    if case=="test_06":
        return "square", (55,145,252)  # ORANGE
    return "circle", (35,145,253)


def frame_for(case: str, index: int):
    import cv2
    import numpy as np
    t=index/FPS
    frame=np.zeros((HEIGHT,WIDTH,3),dtype=np.uint8)
    frame[:] = (48,43,28)
    for x in range(0,WIDTH,60):
        cv2.line(frame,(x,0),(x,HEIGHT),(64,58,39),1)
    for y in range(0,HEIGHT,40):
        cv2.line(frame,(0,y),(WIDTH,y),(64,58,39),1)
    cv2.line(frame,(5,300),(WIDTH-5,300),(92,88,85),2)
    # Two independent stationary scene landmarks. Their motion in image
    # coordinates is evidence of camera translation, not target movement.
    for cx,cy in ((70,270),(405,45)):
        cv2.rectangle(frame,(cx-8,cy-8),(cx+8,cy+8),(255,225,30),-1)
    if not (case=="test_06" and 1.0 <= t <= 1.25):
        x,y=position(case,t)
        cx,cy=int(round(x)),int(round(y))
        if case=="test_04" and x>WIDTH-15:
            raise ValueError("unknown-jump fixture outside image")
        shape,color=appearance(case)
        if shape=="circle":
            cv2.circle(frame,(cx,cy),12,color,-1,cv2.LINE_AA)
        elif shape=="square":
            cv2.rectangle(frame,(cx-12,cy-12),(cx+12,cy+12),color,-1)
        else:
            pts=np.array([[cx,cy-15],[cx-15,cy+12],[cx+15,cy+12]],np.int32)
            cv2.fillConvexPoly(frame,pts,color,cv2.LINE_AA)
    if case=="test_03":
        # The *whole camera image* shifts in the same coordinate system.
        dx=int(round(11*t))
        dy=int(round(-6*t))
        transform=np.float32([[1,0,dx],[0,1,dy]])
        frame=cv2.warpAffine(frame,transform,(WIDTH,HEIGHT),
                             flags=cv2.INTER_NEAREST,borderValue=(48,43,28))
    return frame


def build_probe_suite(out_dir: str | Path) -> dict:
    import cv2
    out=Path(out_dir).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("output directory must be empty")
    out.mkdir(parents=True,exist_ok=True)
    suite={"schema_version":"BRODY_TRANSFER_PROBE_V1","source_kind":"SIMULATED",
           "fps":FPS,"frames":FRAMES,"width":WIDTH,"height":HEIGHT,
           "train":[],"test":[],
           "test_scenarios_for_evaluation_only":{
               "test_01":"appearance-blue-square",
               "test_02":"appearance-green-triangle",
               "test_03":"camera-pan-reference-frame",
               "test_04":"unforeseeable-position-jump",
               "test_05":"ambiguous-identical-history",
               "test_06":"temporary-target-occlusion",
           }}
    for split,cases in (("train",TRAIN),("test",TEST)):
        for name in cases:
            target=out/(name+".mp4")
            writer=cv2.VideoWriter(str(target),
                                   cv2.VideoWriter_fourcc(*"mp4v"),
                                   FPS,(WIDTH,HEIGHT))
            if not writer.isOpened():
                raise RuntimeError("MP4 writer unavailable")
            try:
                for i in range(FRAMES):
                    writer.write(frame_for(name,i))
            finally:
                writer.release()
            digest=sha256(target.read_bytes()).hexdigest()
            suite[split].append({"file":name+".mp4","sha256":digest,
                                 "source_kind":"SIMULATED","split":split.upper()})
    (out/"suite.json").write_text(
        json.dumps(suite,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return {"videos":len(TRAIN)+len(TEST),"train":len(TRAIN),"test":len(TEST),
            "source_kind":"SIMULATED","suite":str(out/"suite.json")}


def main(argv: list[str] | None=None)->int:
    parser=argparse.ArgumentParser(description="Generate synthetic physical-transfer stress videos")
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args(argv)
    print(json.dumps(build_probe_suite(args.out),ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
