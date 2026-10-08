"""Reverso-style preview of a precommitted predicted next video image.

Only the future XY originates in Brody's experience learner. Pixel decoding,
foreground isolation, movement, background inpainting, PNG export and image
difference reuse OpenCV's known routines. This is NOT a generative visual model,
3D physics simulation, source identity proof or native memory update.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re

from brody_world_physique.video_observation_v0 import video_sha256


def create_preview(suite: str|Path, forecasts: str|Path, out_dir: str|Path,
                   *, clip_name: str="test_01.mp4") -> dict:
    import cv2
    import numpy as np
    manifest_path=Path(suite).resolve(strict=True)
    data=json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("schema_version")!="BRODY_TRANSFER_PROBE_V1" or data.get("source_kind")!="SIMULATED":
        raise ValueError("only synthetic transfer suite is eligible")
    clips={item["file"]:item for item in data.get("test",[])}
    if clip_name not in clips or not re.fullmatch(r"test_\d{2}\.mp4",clip_name):
        raise ValueError("test clip not found")
    record=clips[clip_name]
    if record.get("source_kind")!="SIMULATED":
        raise ValueError("source kind must remain simulated")
    video=(manifest_path.parent/clip_name).resolve(strict=True)
    if manifest_path.parent not in video.parents or video_sha256(video)!=record["sha256"]:
        raise ValueError("video provenance failed")
    lines=Path(forecasts).resolve(strict=True).read_text(encoding="utf-8").splitlines()
    if len(lines)>1000:raise ValueError("too many forecast receipts")
    selections=[]
    for line in lines:
        item=json.loads(line)
        if item.get("clip")==clip_name and item.get("camera_mode")=="anchored":
            proposed=item.get("proposal",{})
            if proposed.get("status")=="PREDICTION_CANDIDATE" and proposed.get("candidate_xy") is not None:
                selections.append(item)
    if not selections:
        raise ValueError("no learned precommitted prediction in specified clip")
    chosen=selections[0]
    future=int(chosen["next_frame_index"])
    past=future-6
    if future<=past or not 0<=past<future<72:
        raise ValueError("forecast time invalid")
    if any(f"#frame:{future}#" in r for r in chosen["history_refs"]):
        raise ValueError("future frame leaked into history")
    target=Path(out_dir).resolve()
    if target.exists() and any(target.iterdir()):
        raise ValueError("use new preview output")
    cap=cv2.VideoCapture(str(video))
    try:
        if not cap.isOpened():raise ValueError("could not open source clip")
        def fetch(index):
            cap.set(cv2.CAP_PROP_POS_FRAMES,index)
            ok,frame=cap.read()
            if not ok or frame is None:raise ValueError("frame decode failed")
            return frame
        previous=fetch(past)
        actual=fetch(future)
    finally:
        cap.release()
    hsv=cv2.cvtColor(previous,cv2.COLOR_BGR2HSV)
    cyan=cv2.inRange(hsv,(83,105,105),(104,255,255))
    saturated=cv2.inRange(hsv,(0,120,115),(179,255,255))
    foreground=cv2.bitwise_and(saturated,cv2.bitwise_not(cyan))
    n, labels, stats, centroids=cv2.connectedComponentsWithStats(foreground,8)
    candidates=[i for i in range(1,n) if 140<=int(stats[i,cv2.CC_STAT_AREA])<=1200]
    if len(candidates)!=1:
        raise ValueError("cannot safely isolate source object")
    chosen_id=candidates[0]
    object_mask=np.uint8(labels==chosen_id)*255
    # Restore only the pixels occluded by last known target. This tool
    # does not claim the inpainting is physically or semantically accurate.
    background=cv2.inpaint(previous,object_mask,3,cv2.INPAINT_TELEA)
    predicted=background.copy()
    x0,y0=centroids[chosen_id]
    x1,y1=map(float,chosen["proposal"]["candidate_xy"])
    tx,ty=int(round(x1-x0)),int(round(y1-y0))
    mat=np.float32([[1,0,tx],[0,1,ty]])
    new_mask=cv2.warpAffine(object_mask,mat,(previous.shape[1],previous.shape[0]))
    new_object=cv2.warpAffine(previous,mat,(previous.shape[1],previous.shape[0]))
    predicted[new_mask>0]=new_object[new_mask>0]
    delta=cv2.absdiff(predicted,actual)
    metric=float(np.mean(delta))
    target.mkdir(parents=True,exist_ok=True)
    for name,frame in [
        ("last_observed.png",previous),
        ("predicted_reverso_candidate.png",predicted),
        ("heldout_frame.png",actual),
        ("difference.png",delta),
    ]:
        if not cv2.imwrite(str(target/name),frame):
            raise ValueError("failed to write visualization")
    report={
        "schema":"BRODY_REVERSE_FUTURE_IMAGE_CANDIDATE_V1",
        "source_kind":"SIMULATED",
        "video_sha256":record["sha256"],
        "forecast_receipt_sha256":sha256(Path(forecasts).read_bytes()).hexdigest(),
        "past_index":past,"future_index":future,
        "candidate_center_xy":[x1,y1],
        "full_frame_mean_absolute_pixel_difference":metric,
        "method":"PAST_FRAME_ISOLATE_AND_MOVE_WITH_OPENCV_INPAINT",
        "future_coordinates_learned_from_experiences":True,
        "pixel_reproduction_exact":False,
        "image_generation_model_trained":False,
        "physical_causality_proven":False,
        "real_world_knowledge_validated":False,
        "native_memory_write_allowed":False,
    }
    (target/"evaluation.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report | {"output":str(target)}


def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(description="Render a predicted future image using prior image and learned XY only")
    p.add_argument("--suite",required=True,type=Path)
    p.add_argument("--forecasts",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    p.add_argument("--clip",default="test_01.mp4")
    a=p.parse_args(argv)
    print(json.dumps(create_preview(a.suite,a.forecasts,a.out,clip_name=a.clip),
                     indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
