"""Regenerate a controlled SIMULATED no-physics-label video suite locally.

Uses only existing OpenCV+NumPy to DRAW videos. Its trajectory formulas are
known to the FIXTURE CREATOR, NOT imported/read by the experiential learner.
Never present generated scenes as external physical evidence.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import sin
from pathlib import Path


def position_for_fixture(case: str, t: float) -> tuple[float, float]:
    """Hidden to learner: synthetic scenario construction, not physics truth."""
    if case=="train_01": return 78+13*t, 45+25*t+19*t*t
    if case=="train_02": return 65+72*t, 188+6*t
    if case=="train_03":
        if t<1.4: y=49+94*t+23*t*t
        else:
            s=t-1.4
            y=49+94*1.4+23*1.4**2-109*s+37*s*s
        return 152+14*t,y
    if case=="train_04": return 260+48*sin(1.35*t),110+30*sin(1.9*t)
    if case=="test_01": return 231+9*t,62+16*t+21*t*t
    if case=="test_02": return 95+63*t,225+5*t
    if case=="test_03":
        if t<1.55: y=55+77*t+26*t*t
        else:
            s=t-1.55
            y=55+77*1.55+26*1.55**2-99*s+36*s*s
        return 222+8*t,y
    if case=="test_04": return 320+45*sin(1.8*t),100+31*sin(2.25*t)
    raise ValueError("unknown fixture case")


def build_suite(out_dir: str | Path) -> dict:
    try:
        import cv2
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("OpenCV/NumPy not in current Python; no new AI model required") from exc
    out=Path(out_dir).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("use a fresh output directory")
    out.mkdir(parents=True,exist_ok=True)
    width,height,fps,frames=480,320,24,72
    manifest={
        "schema_version":"BRODY_SELF_SUPERVISED_VIDEO_SUITE_V1",
        "source_kind":"SIMULATED","fps":fps,"width":width,
        "height":height,"frame_count":frames,
        "detector_target":"single orange circular marker on dark background",
        "physics_truth_claim":False,"training_truth_labels":False,
        "train":[],"test":[],
    }
    for group in ("train","test"):
        for n in (1,2,3,4):
            ident=f"{group}_{n:02d}"
            filename=ident+".mp4"
            video=out/filename
            writer=cv2.VideoWriter(str(video),cv2.VideoWriter_fourcc(*"mp4v"),
                                   fps,(width,height))
            if not writer.isOpened():
                raise RuntimeError("MP4 codec unavailable; use a Python/OpenCV with MP4v encoding")
            try:
                for index in range(frames):
                    t=index/fps
                    frame=np.zeros((height,width,3),dtype=np.uint8)
                    frame[:]=(48,43,28)
                    for x in range(0,width,60):
                        cv2.line(frame,(x,0),(x,height),(64,59,40),1)
                    for y in range(0,height,40):
                        cv2.line(frame,(0,y),(width,y),(64,59,40),1)
                    cv2.line(frame,(10,height-20),(width-10,height-20),(88,88,88),2)
                    px,py=position_for_fixture(ident,t)
                    x,y=round(px),round(py)
                    if not 14<x<width-14 or not 14<y<height-14:
                        raise ValueError(f"fixture out of frame: {ident}/{index}")
                    cv2.circle(frame,(x,y),13,(35,148,252),-1,cv2.LINE_AA)
                    cv2.circle(frame,(x-3,y-3),3,(104,208,255),-1,cv2.LINE_AA)
                    writer.write(frame)
            finally:
                writer.release()
            file_hash=sha256(video.read_bytes()).hexdigest()
            manifest[group].append({
                "file":filename,"sha256":file_hash,"split":group.upper(),
                "source_kind":"SIMULATED",
            })
    (out/"suite.json").write_text(
        json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8"
    )
    (out/"LISEZMOI.txt").write_text(
        "Simulated Brody world video suite; no labels or physical laws "+
        "are supplied to the learner. See docs/32 in GitHub.\n",
        encoding="utf-8",
    )
    return {"output":str(out),"train":4,"test":4,"provenance":"SIMULATED"}


def main() -> int:
    parser=argparse.ArgumentParser(description="Create eight no-label simulated experience videos")
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(build_suite(args.out),ensure_ascii=False,indent=2))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
