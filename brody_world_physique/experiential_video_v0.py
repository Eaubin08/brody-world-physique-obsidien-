"""Brody visual experiences V0: learn from observation, without physics labels.

Cold memory -> HOLD. Training reads only designated TRAIN videos and learns
image-plane displacement transitions by nearest remembered experiences (kNN).
TEST predictions are emitted to disk BEFORE the next frame is decoded.
Only video pixel positions and timestamp deltas are provided to the learner:
NO gravity/bounce/wind formula, physical parameter or movement name.

An algorithmic inductive bias, a hardcoded orange-dot detector and 4 source
videos still exist: "without preloaded physical law" is NOT "from no input".
SIMULATED only; no canonical Native Memory or model weight mutation.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import hypot, isfinite
from pathlib import Path
from statistics import mean
from typing import Any, Iterator

from .preverbal_prediction_v0 import PositionMeasurementV0, predict_from_three
from .video_observation_v0 import video_sha256

MAX_VIDEO_BYTES = 35 * 1024 * 1024
MAX_MEMORIES = 30000


@dataclass(frozen=True)
class ExperienceV0:
    """Source-tagged transition, never a physical truth or canonical memory."""
    signature: tuple[float, float, float, float]
    outcome_displacement: tuple[float, float]
    source_sha256: str
    prior_refs: tuple[str, str, str]
    future_ref: str
    status: str = "CANDIDATE_SIMULATED_EXPERIENCE"


def signature_from_three(samples: list[PositionMeasurementV0] | tuple[PositionMeasurementV0, ...]) -> tuple[float, float, float, float]:
    if len(samples) != 3:
        raise ValueError("need exactly three historical positions")
    a,b,c = samples
    if not (a.entity_ref==b.entity_ref==c.entity_ref and
            a.frame_ref==b.frame_ref==c.frame_ref and
            a.unit==b.unit==c.unit and
            a.source_kind==b.source_kind==c.source_kind=="SIMULATED"):
        raise ValueError("incompatible simulated samples")
    if not a.time_s < b.time_s < c.time_s:
        raise ValueError("nonmonotonic sample timeline")
    if abs((b.time_s-a.time_s)-(c.time_s-b.time_s)) > 1e-5:
        raise ValueError("uneven sampling not supported in this V0")
    return (b.x-a.x, b.y-a.y, c.x-b.x, c.y-b.y)


def acquire_experiences(samples: list[PositionMeasurementV0], video_hash: str) -> list[ExperienceV0]:
    """Experience gained AFTER a fourth observation is available."""
    if len(samples) < 4:
        raise ValueError("training episode too short")
    acquired = []
    for i in range(2,len(samples)-1):
        history = samples[i-2:i+1]
        future = samples[i+1]
        sig = signature_from_three(history)
        if future.time_s <= history[-1].time_s or future.source_ref in (x.source_ref for x in history):
            raise ValueError("invalid future evidence")
        acquired.append(ExperienceV0(
            signature=sig,
            outcome_displacement=(future.x-history[-1].x, future.y-history[-1].y),
            source_sha256=video_hash,
            prior_refs=tuple(p.source_ref for p in history),
            future_ref=future.source_ref,
        ))
    return acquired


def propose_from_experiences(
    memory: list[ExperienceV0] | tuple[ExperienceV0, ...],
    history: list[PositionMeasurementV0],
    *, max_distance: float = 11.0,
    neighbors: int = 3,
) -> dict[str, Any]:
    """Nearest prior transitions. No physical laws; failed novelty -> HOLD."""
    sig = signature_from_three(history)
    if not memory:
        return {"status":"HOLD_NO_EXPERIENCE","candidate_xy":None,"nearest_distance":None,"reused_source_refs":[]}
    if len(memory)>MAX_MEMORIES:
        raise ValueError("too many experience candidates")
    nearest = sorted(
        ((sum((a-b)**2 for a,b in zip(sig,m.signature))**.5, m)
         for m in memory),
        key=lambda x:x[0],
    )[:neighbors]
    if not nearest or nearest[0][0] > max_distance:
        return {"status":"HOLD_UNFAMILIAR_CHANGE","candidate_xy":None,
                "nearest_distance":nearest[0][0] if nearest else None,
                "reused_source_refs":[]}
    weights = [1/(1+distance) for distance,_ in nearest]
    total = sum(weights)
    vx = sum(w*m.outcome_displacement[0] for w,(_,m) in zip(weights,nearest))/total
    vy = sum(w*m.outcome_displacement[1] for w,(_,m) in zip(weights,nearest))/total
    return {"status":"PREDICTION_CANDIDATE",
            "candidate_xy":[history[-1].x+vx,history[-1].y+vy],
            "nearest_distance":nearest[0][0],
            "reused_source_refs":[m.future_ref for _,m in nearest],
            "physical_law_known":False, "knowledge_validated":False}


def _video_points(
    video: Path, video_hash: str, *, stride: int = 6
) -> Iterator[PositionMeasurementV0]:
    """Yield observations in frame order, not a precomputed track from the future.

    This deliberately uses an orange marker for a controlled suite ONLY.
    It does not recognize generic objects, body motion or unseen colors.
    """
    if not video.is_file() or not 0 < video.stat().st_size <= MAX_VIDEO_BYTES:
        raise ValueError("video absent/empty/too large")
    if video_sha256(video) != video_hash:
        raise ValueError("video SHA256 does not match suite manifest")
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("OpenCV video decoder missing; no LLM is needed") from exc
    cap = cv2.VideoCapture(str(video))
    try:
        if not cap.isOpened():
            raise RuntimeError("cannot open video via OpenCV")
        fps = float(cap.get(cv2.CAP_PROP_FPS))
        count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if not (abs(fps-24)<.01 and count==72 and width==480 and height==320):
            raise ValueError("video outside the controlled 24fps/72f/480x320 suite")
        for frame_index in range(count):
            ok, frame = cap.read()
            if not ok or frame is None:
                raise RuntimeError("video decoder returned missing frame")
            if frame_index % stride:
                continue
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv,(4,100,130),(27,255,255))
            components, _, stats, centroids = cv2.connectedComponentsWithStats(mask, 8)
            candidates = [
                i for i in range(1,components)
                if 150 <= int(stats[i,cv2.CC_STAT_AREA]) <= 1000
                and .70 <= (int(stats[i,cv2.CC_STAT_WIDTH]) /
                             max(1,int(stats[i,cv2.CC_STAT_HEIGHT]))) <= 1.30
            ]
            if len(candidates) != 1:
                raise ValueError(f"controlled orange target not unique at frame {frame_index}")
            x,y = map(float,centroids[candidates[0]])
            if not isfinite(x) or not isfinite(y):
                raise ValueError("invalid visual position")
            yield PositionMeasurementV0(
                entity_ref="synthetic:moving-marker",
                source_ref=f"sha256:{video_hash}#frame:{frame_index}#detector:orange-v0",
                frame_ref=f"fixed-camera:sha256:{video_hash}",
                time_s=frame_index/fps, x=x, y=y, unit="px", source_kind="SIMULATED",
                uncertainty_refs=("SIMULATED", "COLOR_THRESHOLD_DETECTOR", "CAMERA_STATIC_BY_DESIGN"),
            )
    finally:
        cap.release()


def _load_suite(path: Path) -> tuple[dict, list[tuple[str,Path,str]], list[tuple[str,Path,str]]]:
    path=path.resolve(strict=True)
    raw=path.read_bytes()
    if len(raw)>256*1024:
        raise ValueError("suite manifest too large")
    manifest=json.loads(raw)
    if manifest.get("schema_version")!="BRODY_SELF_SUPERVISED_VIDEO_SUITE_V1" or manifest.get("source_kind")!="SIMULATED":
        raise ValueError("unsupported suite manifest or non-simulated provenance")
    sets=[]; used_names=set(); used_hashes=set()
    for split in ("train","test"):
        entries=manifest.get(split)
        if not isinstance(entries,list) or len(entries)<1 or len(entries)>64:
            raise ValueError("both train and test need bounded video sets")
        clips=[]
        for item in entries:
            filename=item["file"]
            if not isinstance(filename,str) or not filename.endswith(".mp4") or Path(filename).name!=filename or filename.startswith("."):
                raise ValueError("unsafe video manifest file reference")
            expected=item["sha256"]
            if (not isinstance(expected,str) or len(expected)!=64 or
                any(c not in "0123456789abcdef" for c in expected)):
                raise ValueError("invalid video hash")
            if item.get("split")!=split.upper() or item.get("source_kind")!="SIMULATED":
                raise ValueError("source kind/split contradiction")
            if filename in used_names or expected in used_hashes:
                raise ValueError("train/test video overlap is prohibited")
            used_names.add(filename);used_hashes.add(expected)
            clip=(path.parent/filename).resolve(strict=True)
            if path.parent not in clip.parents or clip.is_symlink():
                raise ValueError("video escaped suite folder")
            clips.append((filename,clip,expected))
        sets.append(clips)
    return manifest,sets[0],sets[1]


def run_suite(
    suite: str | Path, output: str | Path, *, train_videos: int | None = None
) -> dict[str, Any]:
    """Cold start (0), few experiences (1), or all (N), then frozen transfer."""
    meta,train_clips,test_clips=_load_suite(Path(suite))
    if train_videos is None:
        train_videos=len(train_clips)
    if not isinstance(train_videos,int) or isinstance(train_videos,bool) or not 0 <= train_videos <= len(train_clips):
        raise ValueError("train_videos must be 0..number of TRAIN clips")
    train_clips=train_clips[:train_videos]
    root=Path(output).resolve()
    if root.exists() and any(root.iterdir()):
        raise ValueError("output must be a fresh empty directory")
    # Before seeing training clips, this learner does not know how to predict:
    hold="HOLD_NO_EXPERIENCE"
    memory:list[ExperienceV0]=[]
    training=[]
    for filename,video,digest in train_clips:
        observations=list(_video_points(video,digest))
        learned=acquire_experiences(observations,digest)
        if len(memory)+len(learned)>MAX_MEMORIES:
            raise ValueError("too many experience records")
        memory.extend(learned)
        training.append({"file":filename,"source_hash":digest,"samples":len(observations),"experiences":len(learned)})
    frozen_memory=tuple(memory)
    root.mkdir(parents=True,exist_ok=True)
    (root/"learning_candidates.json").write_text(
        json.dumps({"schema":"BRODY_SIMULATED_EXPERIENCE_MEMORY_V0",
                    "canonical_memory":False,"memory_write_allowed":False,
                    "training":training,"experiences":[asdict(x) for x in frozen_memory]},
                   indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    assessments=[]
    with (root/"predictions_before_heldout.jsonl").open("w",encoding="utf-8") as receipt:
        for filename,video,digest in test_clips:
            history=[];pending=None;errors=[];held=0;trials=0
            for observation in _video_points(video,digest):
                if pending is not None:
                    trials += 1
                    proposed=pending["proposal"]
                    actual=(observation.x,observation.y)
                    stationary=hypot(history[-1].x-actual[0],history[-1].y-actual[1])
                    linear=hypot((history[-1].x+(history[-1].x-history[-2].x))-actual[0],
                                 (history[-1].y+(history[-1].y-history[-2].y))-actual[1])
                    # Fixed constant-acceleration formula is a BENCHMARK ONLY:
                    benchmark=predict_from_three(history[-3:],observation.time_s)
                    fixed=hypot(benchmark.candidate_xy[0]-actual[0],
                                benchmark.candidate_xy[1]-actual[1])
                    learned=hypot(proposed["candidate_xy"][0]-actual[0],
                                  proposed["candidate_xy"][1]-actual[1]) if proposed["candidate_xy"] else None
                    if learned is None: held+=1
                    errors.append({"heldout_ref":observation.source_ref,
                                   "learned_error_px":learned,"static_error_px":stationary,
                                   "linear_error_px":linear,"fixed_accel_error_px":fixed,
                                   "proposal_status":proposed["status"]})
                    pending=None
                history.append(observation)
                if len(history)>=3 and len(history)<12:
                    proposal=propose_from_experiences(frozen_memory,history[-3:])
                    pending={"proposal":proposal,"future_frame_index":(len(history)*6),
                             "history_refs":[p.source_ref for p in history[-3:]]}
                    # This line is committed before the generator yields the
                    # future observation. No TEST sample updates the memory.
                    receipt.write(json.dumps({"test_file":filename,**pending},ensure_ascii=False)+"\n")
                    receipt.flush()
            if pending is not None:
                # Only possible if manifest has unexpected timeline length.
                raise ValueError("dangling unobserved future prediction")
            known=[x["learned_error_px"] for x in errors if x["learned_error_px"] is not None]
            assessments.append({
                "file":filename,"source_sha256":digest,"source_kind":"SIMULATED",
                "prediction_trials":trials,
                "learned_predictions":len(known),"unknown_holds":held,
                "learned_mae_px":mean(known) if known else None,
                "static_mae_px":mean(x["static_error_px"] for x in errors),
                "linear_mae_px":mean(x["linear_error_px"] for x in errors),
                "fixed_accel_mae_px":mean(x["fixed_accel_error_px"] for x in errors),
                "errors":errors,
            })
    # No source at TEST is ever added to frozen_memory.
    n_preds=sum(x["learned_predictions"] for x in assessments)
    n_holds=sum(x["unknown_holds"] for x in assessments)
    predicted_cases=[e for a in assessments for e in a["errors"] if e["learned_error_px"] is not None]
    all_learned=[e["learned_error_px"] for e in predicted_cases]
    summary={
        "schema":"BRODY_COLD_START_EXPERIENTIAL_SUITE_V0",
        "cold_start":hold,
        "prior_domain_formulas_loaded":False,
        "prior_labeled_training_data_loaded":False,
        "learning_algorithm":"KNN_ON_OBSERVED_2D_DISPLACEMENT_TRANSITIONS",
        "training_episodes":len(train_clips),
        "training_candidate_transitions":len(frozen_memory),
        "test_episodes_unseen_during_training":len(test_clips),
        "test_predictions":n_preds,"test_holds_unknown":n_holds,
        "mean_learned_error_on_predicted_only_px":mean(all_learned) if all_learned else None,
        "coverage_on_test_trials":n_preds/(n_preds+n_holds) if n_preds+n_holds else None,
        "matched_linear_error_px":mean(e["linear_error_px"] for e in predicted_cases) if predicted_cases else None,
        "matched_fixed_accel_error_px":mean(e["fixed_accel_error_px"] for e in predicted_cases) if predicted_cases else None,
        "matched_stationary_error_px":mean(e["static_error_px"] for e in predicted_cases) if predicted_cases else None,
        "wins_against_matched_linear":sum(e["learned_error_px"]<e["linear_error_px"] for e in predicted_cases),
        "wins_against_matched_fixed_accel":sum(e["learned_error_px"]<e["fixed_accel_error_px"] for e in predicted_cases),
        "test_measures":assessments,
        "test_memory_mutations":0,
        "source_kind":"SIMULATED",
        "physics_understood":False,
        "world_knowledge_validated":False,
        "new_model_weights_trained":False,
        "native_memory_write_allowed":False,
        "decision_authority":"KX108_ONLY",
        "limitations":[
            "Orange object and static camera are preselected perceptual inductive biases",
            "Motion similarity algorithm is given; physics laws are not",
            "Extrapolation baselines are diagnostic only, never used in learner",
            "Simulation does not establish real-world understanding",
            "Low error cannot prove physics/causality or universal transfer",
        ],
    }
    target=root/"evaluation.json"
    target.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return {k:summary[k] for k in (
        "cold_start","training_candidate_transitions","test_predictions",
        "test_holds_unknown","mean_learned_error_on_predicted_only_px",
        "physics_understood","world_knowledge_validated")} | {"evaluation":str(target)}


def main(argv: list[str] | None=None) -> int:
    parser=argparse.ArgumentParser(description="Brody: empty memory -> self-supervised video experience -> unseen transfer")
    parser.add_argument("--suite",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--train-videos",type=int,default=None,
                        help="0=no prior experience; 1=one experience; omit=all TRAIN videos")
    args=parser.parse_args(argv)
    result=run_suite(args.suite,args.out,train_videos=args.train_videos)
    print(json.dumps(result,indent=2,ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
