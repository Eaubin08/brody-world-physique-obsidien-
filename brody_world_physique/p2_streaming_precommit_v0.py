"""P2.3 streaming precommit per arm before future-frame decoding.

Synthetic-only. One video source; two engineered perception paths are correlated.
This runner does not claim physical understanding or learned fusion.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import hypot
from pathlib import Path
from statistics import mean

from .world_transfer_probe_v1 import _load_probe_suite, locate_object_and_anchor
from .p2_ablation_diagnostic_v0 import past_only_predictions
from .p2_raster_forecast_v0 import raster_linear_forecast, raster_spatial_agreement
from .video_observation_v0 import video_sha256

SCHEMA="BRODY_P2_STREAMING_PRECOMMIT_V0"
ARMS=("A0_last_observation","A1_linear_kinematics","A2_spatial_acceleration",
      "A3_raster_only","A5_fixed_past_only_blend","A6_raster_spatial_fixed_fusion")


def _raster_frame(frame):
    """Separate raster candidate extractor; no upstream tracked XY accepted."""
    import cv2
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    fid=cv2.inRange(hsv,(83,105,105),(104,255,255))
    mask=cv2.bitwise_and(cv2.inRange(hsv,(0,120,115),(179,255,255)),
                         cv2.bitwise_not(fid))
    n,_,stats,centers=cv2.connectedComponentsWithStats(mask,8)
    objs=[tuple(map(float,centers[k])) for k in range(1,n)
          if 140<=int(stats[k,cv2.CC_STAT_AREA])<=1200
          and 0.6<=int(stats[k,cv2.CC_STAT_WIDTH])/max(1,int(stats[k,cv2.CC_STAT_HEIGHT]))<=1.52
          and min(int(stats[k,cv2.CC_STAT_WIDTH]),int(stats[k,cv2.CC_STAT_HEIGHT]))>=12]
    n,_,stats,centers=cv2.connectedComponentsWithStats(fid,8)
    anchors=[tuple(map(float,centers[k])) for k in range(1,n)
             if 120<=int(stats[k,cv2.CC_STAT_AREA])<=400
             and 30<centers[k][0]<195 and 200<centers[k][1]<312]
    if len(objs)!=1 or len(anchors)!=1:
        return None
    return (objs[0][0]-anchors[0][0]+70,objs[0][1]-anchors[0][1]+270)


def _predictions(spatial, raster, frames):
    """Caller guarantees only three past observed frames are supplied."""
    from .preverbal_prediction_v0 import PositionMeasurementV0
    if len(spatial)!=3 or len(raster)!=3 or len(frames)!=3:
        raise ValueError("invalid history")
    if any(x is None for x in spatial):
        return {arm:None for arm in ARMS}
    hist=[PositionMeasurementV0(
        entity_ref="simulated:foreground-object",source_ref=f"past:{index}",
        frame_ref="anchored-synthetic",time_s=index/24,
        x=p[0],y=p[1],unit="px",source_kind="SIMULATED",
        uncertainty_refs=("ENGINEERED_SEGMENTATION",))
        for index,p in zip(frames,spatial)]
    future=frames[-1]+6
    scores=past_only_predictions(hist,future/24)
    raster_xy=raster_linear_forecast(raster,frames,future) if all(x is not None for x in raster) else None
    scores["A3_raster_only"]=raster_xy
    spatial_linear=scores["A1_linear_kinematics"]
    scores["A6_raster_spatial_fixed_fusion"]=(
        [(a+b)/2 for a,b in zip(raster_xy,spatial_linear)]
        if raster_spatial_agreement(raster_xy,spatial_linear) else None)
    return scores


def run(suite:Path,out:Path)->dict:
    import cv2
    suite=suite.resolve(strict=True)
    _,tests=_load_probe_suite(suite)
    out=out.resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("output must be fresh")
    out.mkdir(parents=True,exist_ok=True)
    receipts=out/"forecasts_precommitted.jsonl"
    scores=[]
    first_visual=None
    # The only operations performed before writing forecasts concern past frames.
    with receipts.open("w",encoding="utf-8") as handle:
        for name,video,digest in tests:
            if video_sha256(video)!=digest:
                raise ValueError("source mismatch")
            cap=cv2.VideoCapture(str(video))
            past_s=[];past_r=[];past_frames=[]
            pending=None
            try:
                if not cap.isOpened():
                    raise ValueError("video open failed")
                for frame_idx in range(72):
                    ok,frame=cap.read()
                    if not ok or frame is None:
                        raise ValueError("video frame missing")
                    if frame_idx%6:
                        continue
                    if pending is not None:
                        if pending["future_index"]!=frame_idx:
                            raise ValueError("pending prediction not at next frame")
                        try:
                            obj,anchor=locate_object_and_anchor(frame)
                            observed=([obj[0]-anchor[0]+70,obj[1]-anchor[1]+270]
                                      if obj is not None else None)
                        except ValueError:
                            observed=None
                        if first_visual is None and observed is not None and name=="test_01.mp4":
                            first_visual=(frame.copy(),observed,pending["predictions"].copy())
                        for arm,proposal in pending["predictions"].items():
                            error=(hypot(proposal[0]-observed[0],proposal[1]-observed[1])
                                   if proposal is not None and observed is not None else None)
                            scores.append({"clip":name,"frame":frame_idx,"arm":arm,
                                           "error_px":error,"hold":proposal is None,
                                           "target_missing":observed is None})
                        pending=None
                    # Only AFTER future evaluation do we add this frame to history.
                    try:
                        obj,anchor=locate_object_and_anchor(frame)
                        pos=([obj[0]-anchor[0]+70,obj[1]-anchor[1]+270]
                             if obj is not None else None)
                    except ValueError:
                        pos=None
                    raster=_raster_frame(frame)
                    if pos is None or raster is None:
                        past_s=[];past_r=[];past_frames=[]
                        continue
                    past_s.append(pos);past_r.append(raster);past_frames.append(frame_idx)
                    past_s=past_s[-3:];past_r=past_r[-3:];past_frames=past_frames[-3:]
                    if len(past_s)==3 and frame_idx+6<72:
                        predictions=_predictions(past_s,past_r,tuple(past_frames))
                        pending={"clip":name,"video_sha256":digest,
                                 "cutoff_frame":frame_idx,"future_index":frame_idx+6,
                                 "history_indices":list(past_frames),
                                 "predictions":predictions,"source_kind":"SIMULATED"}
                        # Flush all arms BEFORE the future frame is decoded.
                        for arm,prediction in predictions.items():
                            handle.write(json.dumps({"clip":name,"video_sha256":digest,
                                 "cutoff_frame":frame_idx,"future_index":frame_idx+6,
                                 "history_indices":list(past_frames),"arm":arm,
                                 "candidate_xy":prediction,"hold":prediction is None},
                                 sort_keys=True)+"\n")
                        handle.flush()
                if pending is not None:
                    raise ValueError("unresolved prediction")
            finally:
                cap.release()
    if first_visual is not None:
        image,observed,forecasts=first_visual
        images=out/"images"
        images.mkdir()
        cv2.circle(image,(round(observed[0]),round(observed[1])),5,(255,255,255),2)
        # Annotate only after prediction receipts were flushed and future seen.
        for index,(arm,xy) in enumerate(forecasts.items()):
            if xy is None:
                continue
            color=((index*59+40)%255,(index*83+70)%255,(index*113+100)%255)
            cv2.circle(image,(round(xy[0]),round(xy[1])),5,color,2)
            cv2.putText(image,arm.split("_")[0],(round(xy[0])+6,round(xy[1])+6),
                        cv2.FONT_HERSHEY_SIMPLEX,.35,color,1)
        if not cv2.imwrite(str(images/"p2_prediction_overlay.png"),image):
            raise ValueError("failed to write prediction overlay")
    metrics={}
    for arm in ARMS:
        rows=[r for r in scores if r["arm"]==arm]
        good=[r["error_px"] for r in rows if r["error_px"] is not None]
        metrics[arm]={"episodes":len(rows),"evaluated":len(good),
                      "mean_error_px":mean(good) if good else None,
                      "coverage":len(good)/len(rows) if rows else 0}
    # Explicitly matched subset: evaluate only future cases scored by ALL arms.
    groups={}
    for r in scores:
        groups.setdefault((r["clip"],r["frame"]),{})[r["arm"]]=r["error_px"]
    common=[g for g in groups.values() if all(g.get(arm) is not None for arm in ARMS)]
    matched={arm:mean(g[arm] for g in common) if common else None for arm in ARMS}
    report={"schema":SCHEMA,"source_kind":"SIMULATED",
            "suite_sha256":sha256(suite.read_bytes()).hexdigest(),
            "precommit_sha256":sha256(receipts.read_bytes()).hexdigest(),
            "summary":metrics,"matched_all_arms_mean_error_px":matched,
            "matched_case_count":len(common),"per_case":scores,
            "streaming_precommit_before_future_decode":True,
            "cross_source_independence":False,
            "genuine_learned_fusion":False,
            "p2_verdict":"P2_INCONCLUSIVE","ablation_gain_proven":False,
            "native_memory_write_allowed":False,"decision_authority":"KX108_ONLY"}
    (out/"evaluation.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return report


def verify(suite:Path,output:Path)->dict:
    # Recompute in fresh directory; preserve original artifacts unmodified.
    from tempfile import TemporaryDirectory
    root=Path(output).resolve(strict=True)
    old=json.loads((root/"evaluation.json").read_text(encoding="utf-8"))
    with TemporaryDirectory() as tmp:
        fresh=run(suite,Path(tmp)/"replay")
        if old!=fresh:
            raise ValueError("non deterministic replay")
        original=(root/"forecasts_precommitted.jsonl").read_bytes()
        replay=(Path(tmp)/"replay"/"forecasts_precommitted.jsonl").read_bytes()
        if original!=replay:
            raise ValueError("forecast receipts mismatch")
    return {"verified":True,"matched_case_count":old["matched_case_count"],
            "p2_verdict":old["p2_verdict"]}


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--suite",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args(argv)
    result=verify(args.suite,args.out) if args.verify else run(args.suite,args.out)
    print(json.dumps({k:result[k] for k in
          ("verified","matched_case_count","p2_verdict") if k in result}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
