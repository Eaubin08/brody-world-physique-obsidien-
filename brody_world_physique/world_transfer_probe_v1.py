"""Brody visual transfer stress test over synthesized video observations.

Learn from TRAIN clips without movement-class labels / physical laws. On TEST:
- identify saturated target despite color/shape changes (bounded scene prior);
- anchor image-plane coordinates to a stationary synthetic scene fiducial;
- abstain when visual evidence or outcome agreement is missing;
- precommit forecast BEFORE reading the held-out future frame;
- compare true model prediction against unseen measurement, including shocks.

The segmentation, static-fiducial assumption, thresholds, and nearest-neighbor
association are *given engineering biases*, NOT discoveries by the system.
Simulation does not establish real-world physical knowledge, causality, 3D,
general object understanding or true independent truth verification.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json
from math import hypot, isfinite
from pathlib import Path
from statistics import mean
from typing import Any, Iterator

from .experiential_video_v0 import (
    ExperienceV0, MAX_MEMORIES, acquire_experiences,
    propose_from_experiences, signature_from_three,
)
from .preverbal_prediction_v0 import PositionMeasurementV0, predict_from_three
from .video_observation_v0 import video_sha256

VIDEO_BYTES_LIMIT = 35 * 1024 * 1024
FRAMES = 72
FPS = 24.0
STRIDE = 6


def locate_object_and_anchor(bgr_frame: Any) -> tuple[tuple[float,float] | None, tuple[float,float]]:
    """Synthetic-specific high-saturation connected components and cyan anchor.

    Different color/shape are tolerated *within* this controlled contrast
    prior; missing/ambiguous target returns None rather than guessed coords.
    """
    import cv2
    if bgr_frame is None or bgr_frame.shape[:2] != (320, 480):
        raise ValueError("unexpected video dimensions")
    hsv=cv2.cvtColor(bgr_frame,cv2.COLOR_BGR2HSV)
    # Cyan squares are fixed scene landmarks (when camera itself is fixed).
    anchor_mask=cv2.inRange(hsv,(83,105,105),(104,255,255))
    _, _, anchor_stats, anchor_centers=cv2.connectedComponentsWithStats(anchor_mask,8)
    anchors=[
        tuple(map(float,anchor_centers[i]))
        for i in range(1,len(anchor_stats))
        if 120<=int(anchor_stats[i,cv2.CC_STAT_AREA])<=400
        and 30<anchor_centers[i][0]<195
        and 200<anchor_centers[i][1]<312
    ]
    if len(anchors)!=1:
        raise ValueError("HOLD_SPATIAL_REFERENCE_UNAVAILABLE")
    # Saturated target can be ORANGE / BLUE / GREEN, but no world-semantic
    # detector is claimed. Subtract cyan fiducials.
    saturation=cv2.inRange(hsv,(0,120,115),(179,255,255))
    target_mask=cv2.bitwise_and(saturation,cv2.bitwise_not(anchor_mask))
    n, _, stats, centers=cv2.connectedComponentsWithStats(target_mask,8)
    candidates=[]
    for i in range(1,n):
        area=int(stats[i,cv2.CC_STAT_AREA])
        w,h=int(stats[i,cv2.CC_STAT_WIDTH]),int(stats[i,cv2.CC_STAT_HEIGHT])
        if 140<=area<=1200 and 0.60<=w/max(1,h)<=1.52 and 12<=min(w,h):
            candidates.append(tuple(map(float,centers[i])))
    if len(candidates)>1:
        raise ValueError("HOLD_AMBIGUOUS_SATURATED_OBJECT")
    return (candidates[0] if candidates else None),anchors[0]


def iter_video_points(video:Path, sha:str, *, camera_mode:str="anchored") -> Iterator[PositionMeasurementV0 | None]:
    if camera_mode not in ("anchored","raw_diagnostic"):
        raise ValueError("unsupported camera mode")
    if not video.is_file() or not 0 < video.stat().st_size<=VIDEO_BYTES_LIMIT:
        raise ValueError("invalid input video")
    if video_sha256(video)!=sha:
        raise ValueError("video does not match declared hash")
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("OpenCV is required to read local videos, no AI model installation") from exc
    cap=cv2.VideoCapture(str(video))
    try:
        if not cap.isOpened():raise ValueError("cannot open video")
        if not(abs(cap.get(cv2.CAP_PROP_FPS)-FPS)<.01
               and int(cap.get(cv2.CAP_PROP_FRAME_COUNT))==FRAMES
               and int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))==480
               and int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==320):
            raise ValueError("unsupported video time/geometry")
        for idx in range(FRAMES):
            ok,frame=cap.read()
            if not ok or frame is None:
                raise ValueError("decoder missing frame")
            if idx%STRIDE:continue
            target,anchor=locate_object_and_anchor(frame)
            if target is None:
                yield None
                continue
            # The detector does not get a trajectory or physical-rule label.
            # The 70,270 anchor reference is a *known fixture constant*.
            x,y=(target[0]-anchor[0]+70,target[1]-anchor[1]+270) if camera_mode=="anchored" else target
            if not isfinite(x) or not isfinite(y):
                raise ValueError("nonfinite visual position")
            yield PositionMeasurementV0(
                entity_ref="simulated:foreground-object",
                source_ref=f"sha256:{sha}#frame:{idx}#visual_candidate",
                frame_ref=f"scene-fiducial:{sha}:{camera_mode}",
                time_s=idx/FPS,x=x,y=y,unit="px",source_kind="SIMULATED",
                uncertainty_refs=("SATURATED_OBJECT_DETECTION_CANDIDATE",
                                  "FIXTURE_FIDUCIAL_ASSUMED_STATIC","NO_REAL_WORLD_PROOF"),
            )
    finally:
        cap.release()


def propose_with_conflict_gate(memory:tuple[ExperienceV0,...],
                               history:list[PositionMeasurementV0],
                               *, conflict_distance:float=2.0,
                               conflict_gap_px:float=15.0) -> dict:
    """Reject mutually inconsistent next steps from near-identical histories."""
    sig=signature_from_three(history)
    distances=sorted(((sum((x-y)**2 for x,y in zip(sig,item.signature))**.5,item)
                      for item in memory),key=lambda x:x[0])
    if distances and distances[0][0]<=conflict_distance:
        neighbors=[entry for distance,entry in distances if distance<=conflict_distance]
        provenance={e.source_sha256 for e in neighbors}
        for i,a in enumerate(neighbors):
            for b in neighbors[i+1:]:
                disagreement=hypot(
                    a.outcome_displacement[0]-b.outcome_displacement[0],
                    a.outcome_displacement[1]-b.outcome_displacement[1]
                )
                if a.source_sha256!=b.source_sha256 and disagreement>=conflict_gap_px:
                    return {
                        "status":"HOLD_CONFLICTING_EXPERIENCES",
                        "candidate_xy":None,
                        "evidence_source_count":len(provenance),
                        "max_pair_difference_px":disagreement,
                        "physical_law_proven":False,
                    }
    result=propose_from_experiences(memory,history)
    result["physical_law_proven"]=False
    return result


def _load_probe_suite(path:Path):
    path=path.resolve(strict=True)
    if path.stat().st_size>256*1024:raise ValueError("oversized manifest")
    manifest=json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("schema_version")!="BRODY_TRANSFER_PROBE_V1" or manifest.get("source_kind")!="SIMULATED":
        raise ValueError("unexpected probe manifest")
    paths=[]; all_hashes=set()
    for split in ("train","test"):
        entries=manifest.get(split)
        if not isinstance(entries,list) or len(entries)<1 or len(entries)>40:
            raise ValueError("invalid split")
        current=[]
        for item in entries:
            filename=item.get("file")
            digest=item.get("sha256")
            if (not isinstance(filename,str) or
                filename!=Path(filename).name or not filename.endswith(".mp4")
                or filename.startswith(".") or
                not isinstance(digest,str) or len(digest)!=64 or
                any(c not in "0123456789abcdef" for c in digest) or
                digest in all_hashes or
                item.get("split")!=split.upper() or
                item.get("source_kind")!="SIMULATED"):
                raise ValueError("invalid, duplicate, or cross-split source")
            all_hashes.add(digest)
            location=(path.parent/filename).resolve(strict=True)
            if path.parent not in location.parents:raise ValueError("unsafe source path")
            current.append((filename,location,digest))
        paths.append(current)
    return paths


def run_probe_suite(suite: str | Path, out: str | Path,
                    *, camera_mode:str="anchored") -> dict:
    if camera_mode not in ("anchored","raw_diagnostic"):
        raise ValueError("unsupported camera mode")
    train,test=_load_probe_suite(Path(suite))
    root=Path(out).resolve()
    if root.exists() and any(root.iterdir()):
        raise ValueError("output directory must be fresh")
    memory=[]
    for name,video,digest in train:
        samples=list(iter_video_points(video,digest,camera_mode=camera_mode))
        if any(sample is None for sample in samples):
            raise ValueError("TRAIN clip cannot contain missing observations")
        assert all(x is not None for x in samples)
        memory.extend(acquire_experiences(samples,digest))
    if len(memory)>MAX_MEMORIES:
        raise ValueError("too much candidate experience")
    frozen=tuple(memory)
    root.mkdir(parents=True,exist_ok=True)
    with (root/"candidate_memory.json").open("w",encoding="utf-8") as f:
        json.dump({"source_kind":"SIMULATED","candidate_experiences":len(frozen),
                   "training_source_hashes":[p[2] for p in train],
                   "canonical_memory":False,"memory_write_allowed":False},f,indent=2)
    measurements=[]
    with (root/"forecasts_precommitted.jsonl").open("w",encoding="utf-8") as receipt:
        for name,video,digest in test:
            history=[];pending=None;errs=[];missing=0;conflict=0;unknown=0;surprise=0
            raw_frames=0
            for observation in iter_video_points(video,digest,camera_mode=camera_mode):
                raw_frames+=1
                if pending is not None:
                    if observation is None:
                        missing+=1
                    else:
                        proposal=pending["proposal"]
                        if proposal["candidate_xy"] is not None:
                            error=hypot(proposal["candidate_xy"][0]-observation.x,
                                        proposal["candidate_xy"][1]-observation.y)
                            linear=hypot(2*history[-1].x-history[-2].x-observation.x,
                                         2*history[-1].y-history[-2].y-observation.y)
                            surprise+=int(error>15)
                            errs.append({"heldout_ref":observation.source_ref,
                                         "error_px":error,"linear_baseline_px":linear,
                                         "status":"SURPRISE" if error>15 else "OBSERVED",
                                         "method":proposal["status"]})
                    pending=None
                if observation is None:
                    history.clear()
                    continue
                history.append(observation)
                if len(history)>=3 and raw_frames<12:
                    proposal=propose_with_conflict_gate(frozen,history[-3:])
                    if proposal["status"]=="HOLD_CONFLICTING_EXPERIENCES":conflict+=1
                    elif proposal["status"].startswith("HOLD_"):unknown+=1
                    pending={
                        "proposal":proposal,"history_refs":[x.source_ref for x in history[-3:]],
                        "next_frame_index":raw_frames*STRIDE,
                        "source_kind":"SIMULATED",
                        "camera_mode":camera_mode,
                    }
                    # No future frame decoded before the corresponding receipt.
                    receipt.write(json.dumps({"clip":name,**pending},ensure_ascii=False)+"\n")
                    receipt.flush()
            if pending is not None:
                raise ValueError("dangling unseen future frame")
            measurements.append({
                "file":name,"source_sha256":digest,
                "predictions":len(errs),"holds_conflict":conflict,
                "holds_novel":unknown,"missing_heldout":missing,
                "surprises":surprise,
                "mean_prediction_error_px":mean(x["error_px"] for x in errs) if errs else None,
                "matched_linear_error_px":mean(x["linear_baseline_px"] for x in errs) if errs else None,
                "measured_future_cases":errs,
            })
    report={
        "schema":"BRODY_TRANSFER_STRESS_EVALUATION_V1",
        "train_videos":len(train),"test_videos":len(test),
        "training_candidate_experiences":len(frozen),
        "camera_mode":camera_mode,
        "measurements":measurements,
        "test_memory_mutations":0,
        "source_kind":"SIMULATED",
        "pretrained_physical_laws_used":False,
        "perception_known_fixture_assumptions":True,
        "learned_3d_world":False,
        "physical_causality_proven":False,
        "world_knowledge_validated":False,
        "memory_write_allowed":False,
        "decision_authority":"KX108_ONLY",
    }
    (root/"evaluation.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return {"evaluation":str(root/"evaluation.json"),
            "camera_mode":camera_mode,
            "probes":[{k:r[k] for k in (
                "file","predictions","holds_conflict","holds_novel",
                "missing_heldout","surprises","mean_prediction_error_px",
            )} for r in measurements],
            "world_knowledge_validated":False}


def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(description="Brody next-stage video transfer: appearance, camera, unknown and contradiction")
    parser.add_argument("--suite",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--camera-mode",default="anchored",
                        choices=["anchored","raw_diagnostic"])
    args=parser.parse_args(argv)
    print(json.dumps(run_probe_suite(args.suite,args.out,camera_mode=args.camera_mode),
                     indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
