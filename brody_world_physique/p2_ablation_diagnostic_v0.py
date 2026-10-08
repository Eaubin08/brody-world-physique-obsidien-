"""P2 retrospective ablation diagnostic on P1's sealed stream.

Only methods that can be recomputed from *past references* are scored.
This is NOT an independent multi-view fusion experiment: future-score
evaluation is retrospective, source is synthetic and correlated.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import hypot, isfinite
from pathlib import Path
from statistics import mean, median

from .world_transfer_probe_v1 import _load_probe_suite, iter_video_points
from .video_observation_v0 import video_sha256

SCHEMA = "BRODY_P2_PRECOMMIT_BASELINE_DIAGNOSTIC_V0"


def _hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _finite_xy(value):
    return (isinstance(value, (list, tuple)) and len(value) == 2
            and all(type(x) in (int, float) and isfinite(x) for x in value))


def evaluate(suite: Path, receipts: Path) -> dict:
    """Independent scoring of existing P1 learner and two strict baselines.

    NOTE: The upstream forecast producer, not this evaluator, guarantees that
    its receipt was emitted before decoding the future frame.
    """
    suite = suite.resolve(strict=True)
    receipts = receipts.resolve(strict=True)
    _train, test = _load_probe_suite(suite)
    if receipts.stat().st_size > 2_000_000:
        raise ValueError("oversized receipt")
    rows = [json.loads(line) for line in receipts.read_text(encoding="utf-8").splitlines()]
    if len(rows) > 1000 or not rows:
        raise ValueError("empty or excessive receipts")
    by_clip = {}
    for row in rows:
        name = row.get("clip")
        if name is None or row.get("camera_mode") != "anchored":
            raise ValueError("invalid receipt provenance")
        by_clip.setdefault(name, []).append(row)
    if set(by_clip) != {name for name, _, _ in test}:
        raise ValueError("receipt clips differ from manifest test split")
    outcomes = []
    for name, video, digest in test:
        if video_sha256(video) != digest:
            raise ValueError("source mismatch")
        observed = list(iter_video_points(video, digest, camera_mode="anchored"))
        points = {p.source_ref: p for p in observed if p is not None}
        seen_futures = set()
        for receipt in by_clip[name]:
            refs = receipt.get("history_refs")
            future_index = receipt.get("next_frame_index")
            if not isinstance(refs, list) or len(refs) != 3 or len(set(refs)) != 3:
                raise ValueError("invalid history")
            if type(future_index) is not int or future_index not in range(6,72,6):
                raise ValueError("invalid future index")
            if future_index in seen_futures:
                raise ValueError("duplicate prediction horizon")
            seen_futures.add(future_index)
            if any(ref not in points for ref in refs):
                raise ValueError("unrecognized or unavailable historical observation")
            history = [points[ref] for ref in refs]
            if any(p.frame_ref != history[0].frame_ref for p in history):
                raise ValueError("incompatible reference frames")
            if any(p.source_kind != "SIMULATED" for p in history):
                raise ValueError("unsupported source")
            if not history[0].time_s < history[1].time_s < history[2].time_s < future_index/24:
                raise ValueError("future leakage or temporal mismatch")
            if any(f"#frame:{future_index}#" in ref for ref in refs):
                raise ValueError("future included in history")
            target = points.get(f"sha256:{digest}#frame:{future_index}#visual_candidate")
            proposal = receipt.get("proposal")
            if not isinstance(proposal, dict):
                raise ValueError("missing precommit proposal")
            status = proposal.get("status")
            xy = proposal.get("candidate_xy")
            if xy is not None and not _finite_xy(xy):
                raise ValueError("invalid sealed prediction")
            if status is None or not isinstance(status, str):
                raise ValueError("missing status")
            dt = history[2].time_s-history[1].time_s
            horizon = future_index/24-history[2].time_s
            if dt <= 0 or horizon <= 0:
                raise ValueError("invalid cadence")
            linear = [history[2].x + (history[2].x-history[1].x)*horizon/dt,
                      history[2].y + (history[2].y-history[1].y)*horizon/dt]
            scores = {"A0_last_observation": [history[2].x, history[2].y],
                      "A1_linear_kinematics": linear,
                      "P1_experiential_candidate": xy}
            for arm, prediction in scores.items():
                outcome = {"clip":name,"source_sha256":digest,
                           "heldout_frame_index":future_index,
                           "arm":arm,"status":"NOT_SCORED" if prediction is None else "PRECOMMITTED_OR_DETERMINISTIC_PAST_ONLY",
                           "hold":prediction is None, "error_px":None}
                if target is None:
                    outcome["status"] = "TARGET_OCCLUDED"
                    outcome["hold"] = True
                elif prediction is not None:
                    outcome["error_px"] = hypot(prediction[0]-target.x,prediction[1]-target.y)
                outcomes.append(outcome)
    summary = {}
    for arm in ("A0_last_observation","A1_linear_kinematics","P1_experiential_candidate"):
        subset = [x for x in outcomes if x["arm"] == arm]
        vals = [x["error_px"] for x in subset if x["error_px"] is not None]
        summary[arm] = {"evaluated":len(vals),"total":len(subset),
                        "coverage":len(vals)/len(subset) if subset else 0,
                        "mean_error_px":mean(vals) if vals else None,
                        "median_error_px":median(vals) if vals else None}
    return {"schema":SCHEMA, "suite_sha256":_hash(suite),
            "precommit_file_sha256":_hash(receipts),
            "source_kind":"SIMULATED","independent_view_sources":False,
            "new_fusion_predictor_implemented":False,
            "ablation_gain_proven":False,"p2_verdict":"P2_INCONCLUSIVE",
            "limitation":"retrospective scoring of prior precommits; A2-A7 not implemented",
            "summary":summary,"per_episode":outcomes,
            "native_memory_write_allowed":False,"decision_authority":"KX108_ONLY"}


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("--suite",required=True,type=Path)
    parser.add_argument("--forecasts",required=True,type=Path)
    parser.add_argument("--out",required=True,type=Path)
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args(argv)
    report=evaluate(args.suite,args.forecasts)
    serial=json.dumps(report,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
    if args.verify:
        if args.out.read_text(encoding="utf-8")!=serial:
            raise ValueError("P2 diagnostic replay mismatch")
    else:
        if args.out.exists():
            raise ValueError("refuse overwrite")
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(serial,encoding="utf-8")
    print(json.dumps({"verdict":report["p2_verdict"],"summary":report["summary"],
                      "verified":args.verify},ensure_ascii=False))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
