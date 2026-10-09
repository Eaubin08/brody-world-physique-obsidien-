"""P2.9b: end-to-end typed-layer wiring on unchanged P2.8c pixel scenarios.

Comparison against P2.8c checks parity, not new generalization. Feedback is delayed
supervised simulator truth, confined to the ephemeral epistemic tester only.
"""
from __future__ import annotations
import argparse
from collections import deque
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
from statistics import mean

from . import p28b_pixel_reversal_v0 as pixels
from .p28c_guarded_reversal_v0 import GuardedBelief
from .p29_layer_contracts_v0 import (
    BOUNDARY, PixelObservation, WorkingBelief, represent, route,
)

SCHEMA = "BRODY_P29B_LAYER_WIRING_V0"
GOALS = ("generate", "explore", "explain")


def layered_prediction(pair_id, measurement, observation_status, guard, goal):
    pixel = PixelObservation(
        pair_id=str(pair_id), source_ref="synthetic-rendered-pair:"+str(pair_id),
        ball_apparent_dx=measurement["apparent"] if measurement is not None else None,
        landmark_shifts=tuple(measurement["shifts"]) if measurement is not None else (),
        quality=observation_status)
    spatial = represent(pixel, coordinate_frame="synthetic-camera-relative-v0")
    available = None if spatial.status == "HOLD_PERCEPTION" else {
        "apparent": spatial.apparent_dx, "shifts": list(spatial.landmark_shifts)}
    value, reason = guard.predict(available)
    belief = WorkingBelief(
        relation_ref=spatial.observation_ref,
        inferred_world_dx=value,
        basis=reason,
        epistemic_status="WORKING_UNVERIFIED" if value is not None else "HOLD",
        evidence_refs=(pixel.source_ref,))
    planning = route(goal, belief)
    return {
        "pixel": asdict(pixel), "spatial": asdict(spatial),
        "belief": asdict(belief), "goal_route": asdict(planning),
        "prediction": value,
        "decision_authority": BOUNDARY["decision_authority"],
        "memory_write": BOUNDARY["memory_write"]}


def execute(count=180, delay=2, window=8):
    if not 100 <= count <= 2000 or not 1 <= delay <= 10 or window < 3:
        raise ValueError("invalid counts")
    layered_guard = GuardedBelief(window)
    reference_guard = GuardedBelief(window)
    pending = deque()
    receipts = []
    rows = []
    feedback_groups = set()
    for idx in range(count):
        spec = pixels.fixture(idx)
        measurement, status = pixels.observe(spec)
        goal = GOALS[idx % len(GOALS)]
        typed = layered_prediction(idx, measurement, status, layered_guard, goal)
        reference, ref_reason = reference_guard.predict(measurement)
        if typed["prediction"] != reference:
            raise AssertionError("P2.9b changed P2.8c knowledge inference")
        receipts.append({
            "id": idx, "observation": typed["pixel"],
            "representation": typed["spatial"],
            "belief": typed["belief"], "goal": goal,
            "goal_hint": typed["goal_route"]["action_hint"],
            "p29b_prediction": typed["prediction"], "p28c_reference": reference,
            "reason_reference": ref_reason,
            "feedback_groups_seen": len(feedback_groups),
            "memory_write": False, "decision_authority": "KX108_ONLY"})
        # Simulator truth is accessed after receipt is appended, for scoring
        # and delayed verification only; no B8 or Native Memory writes.
        rows.append({"id": idx, "regime": spec["regime"],
                     "errors": {
                         "p29b_layered": abs(typed["prediction"]-spec["world"])
                                         if typed["prediction"] is not None else None,
                         "p28c_reference": abs(reference-spec["world"])
                                           if reference is not None else None}})
        pending.append((spec, measurement))
        if len(pending) >= delay:
            previous, observed = pending.popleft()
            if previous["feedback_available"] and observed is not None:
                group = "pair-"+str(previous["id"])
                if group not in feedback_groups:
                    feedback_groups.add(group)
                    layered_guard.feedback(group, observed["shifts"], previous["camera"])
                    reference_guard.feedback(group, observed["shifts"], previous["camera"])
    valid = [r["errors"]["p29b_layered"] for r in rows
             if r["errors"]["p29b_layered"] is not None]
    return {
        "schema": SCHEMA, "source_kind": "SYNTHETIC_RENDERED_PIXELS",
        "count": count, "delay": delay, "window": window,
        "prediction_coverage": len(valid)/count,
        "mae_accepted_px": mean(valid) if valid else None,
        "catastrophic_over_10px": sum(x > 10 for x in valid),
        "identical_to_p28c_reference": True, "feedback_groups": len(feedback_groups),
        "receipts": receipts, "rows": rows,
        "no_new_perception_learning": True, "independent_new_generator": False,
        "delayed_supervised_feedback": True, "native_memory_write": False,
        "b8_promotion": False, "decision_authority": "KX108_ONLY",
        "verdict": "LAYERS_WIRED_PARITY_DIAGNOSTIC_ONLY"}


def encode(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"))+"\n").encode("utf-8")


def run(out, count=180, delay=2, window=8):
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("out directory not empty")
    report = execute(count, delay, window)
    out.mkdir(parents=True, exist_ok=True)
    pre = encode(report["receipts"])
    (out/"predictions_pre_feedback.json").write_bytes(pre)
    report["precommit_sha256"] = sha256(pre).hexdigest()
    (out/"evaluation.json").write_bytes(encode(report))
    return report


def verify(out):
    out = Path(out)
    saved = json.loads((out/"evaluation.json").read_text(encoding="utf-8"))
    pre = (out/"predictions_pre_feedback.json").read_bytes()
    if sha256(pre).hexdigest() != saved["precommit_sha256"]:
        raise ValueError("changed pre-feedback receipt")
    expected = execute(saved["count"], saved["delay"], saved["window"])
    expected["precommit_sha256"] = saved["precommit_sha256"]
    if encode(expected) != encode(saved) or encode(expected["receipts"]) != pre:
        raise ValueError("replay mismatch")
    return {"verified": True, "count": saved["count"]}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--count", type=int, default=180)
    p.add_argument("--delay", type=int, default=2)
    p.add_argument("--window", type=int, default=8)
    p.add_argument("--verify", action="store_true")
    args = p.parse_args(argv)
    answer = verify(args.out) if args.verify else run(args.out, args.count, args.delay, args.window)
    print(json.dumps({k: answer[k] for k in
                      ("verified", "count", "prediction_coverage", "mae_accepted_px",
                       "catastrophic_over_10px", "identical_to_p28c_reference") if k in answer}))


if __name__ == "__main__":
    main()
