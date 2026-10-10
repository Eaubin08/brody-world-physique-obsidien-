"""P2.8b pixel-level reversal diagnostic. Synthetic render, real pixel detection.

Five visual fiducials and a ball, two captured frames each. The camera displacement
is NEVER exposed to the predictor before its prediction receipt is appended.
Delayed supervisory truth is simulator-only. No B8 transition or memory writing.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
from statistics import mean, median
import random

from .p26_adversarial_pixels_v0 import detect
from .p28_epistemic_reversal_v0 import WorkingKnowledge, decide

SCHEMA = "BRODY_P28B_PIXEL_REVERSAL_V0"
ARMS = ("fixed_history", "observed_majority", "scoped_revisable")


def fixture(index):
    rng = random.Random(88211 + index * 437)
    phase = 0 if index < 40 else (1 if index < 90 else 2)
    anchor = (4, 0, 2)[phase]
    return {
        "id": index, "regime": phase, "anchor": anchor,
        "camera": rng.randint(-6, 6), "world": rng.randint(-8, 8),
        "false_delta": 24 if index % 2 else -24,
        "illumination": (0, 0, 0, 0, 0, 8, -8)[index % 7],
        "jitter": (0, 0, 1)[index % 3],
        "occluded": index % 17 == 0,
        "feedback_available": index % 9 != 0,
    }


def draw(spec, step):
    import cv2
    import numpy as np
    rng = random.Random(spec["id"] * 77 + step)
    img = np.full((190, 340, 3), (24, 27, 31), dtype=np.uint8)
    for _ in range(24):
        x, y = rng.randrange(340), rng.randrange(190)
        img[y, x] = tuple(rng.randrange(256) for _ in range(3))
    for i, x in enumerate((40, 90, 140, 190, 240)):
        false_shift = 0 if i == spec["anchor"] else spec["false_delta"]
        jitter = rng.randint(-spec["jitter"], spec["jitter"]) if step else 0
        center = x + step * (spec["camera"] + false_shift) + jitter
        cv2.rectangle(img, (center-4, 45), (center+4, 53),
                      (25, 215, 245), -1)
    if not (step and spec["occluded"]):
        ball = 88 + step * (spec["world"] + spec["camera"])
        cv2.circle(img, (ball, 133), 10, (40, 100, 245), -1)
    if step and spec["illumination"]:
        img = cv2.convertScaleAbs(img, alpha=1, beta=spec["illumination"])
    return img


def observe(spec):
    frame_a, frame_b = draw(spec, 0), draw(spec, 1)
    ball_a, marks_a = detect(frame_a)
    ball_b, marks_b = detect(frame_b)
    if ball_a is None or ball_b is None:
        return None, "HOLD_OBJECT"
    if len(marks_a) != 5 or len(marks_b) != 5:
        return None, "HOLD_REFERENCES"
    return {"apparent": ball_b - ball_a,
            "shifts": [b-a for a,b in zip(marks_a, marks_b)]}, "MEASURED_PIXELS"


def execute(count=120, delay=2):
    if not 100 <= count <= 2000 or not 1 <= delay <= 10:
        raise ValueError("count 100..2000, delay 1..10")
    ledger = WorkingKnowledge()
    pending = []
    predictions, scored, changes = [], [], []
    for idx in range(count):
        # The fixture lives in the simulator; only observe() output is sent
        # to decide(). It has no access to camera, world, anchor, or regime.
        spec = fixture(idx)
        measured, status = observe(spec)
        if measured is None:
            result = {"predictions": {a: None for a in ARMS},
                      "reason": status, "goal_route": "NO_VISUAL_PREDICTION",
                      "best_historical_id": ledger.rank()[0][1] if ledger.rank() else None,
                      "knowledge_status": "WORKING_EXPERIMENTAL_ONLY",
                      "memory_write": False, "decision_authority": "KX108_ONLY"}
        else:
            result = decide(measured, ledger,
                            intent=("generate", "explore", "explain")[idx % 3])
        record = {"id": idx, "measurement": measured,
                  "prediction": result, "feedback_seen": len(ledger.group_ids)}
        predictions.append(record)  # pre-feedback commitment
        scored.append({
            "id": idx, "regime": spec["regime"],
            "illumination": spec["illumination"], "occluded": spec["occluded"],
            "prediction_status": result["reason"],
            "errors": {a: abs(v-spec["world"]) if v is not None else None
                       for a,v in result["predictions"].items()},
        })
        pending.append((spec, measured))
        if len(pending) >= delay:
            older, observed = pending.pop(0)
            if older["feedback_available"] and observed is not None:
                previous = ledger.rank()[0][1] if ledger.rank() else None
                ledger.apply_feedback(
                    episode_id=older["id"], group_id="image-pair-" + str(older["id"]),
                    observed_shifts=observed["shifts"], verified_camera=older["camera"])
                current = ledger.rank()[0][1] if ledger.rank() else None
                if previous != current:
                    changes.append({"after_episode": older["id"], "from": previous, "to": current})
    summary = {}
    for a in ARMS:
        vals = [r["errors"][a] for r in scored if r["errors"][a] is not None]
        summary[a] = {"evaluated": len(vals), "coverage": len(vals)/count,
                      "mean_error_px": mean(vals) if vals else None,
                      "catastrophic_over_10px": sum(v>10 for v in vals)}
    regimes = {}
    for regime in range(3):
        rows = [r for r in scored if r["regime"] == regime]
        good = [r["errors"]["scoped_revisable"] for r in rows
                if r["errors"]["scoped_revisable"] is not None]
        regimes[str(regime)] = {"count": len(rows),
            "coverage": len(good)/len(rows) if rows else 0,
            "mean_error_px": mean(good) if good else None,
            "catastrophic_over_10px": sum(v>10 for v in good)}
    return {"schema": SCHEMA, "source_kind": "SYNTHETIC_RENDERED_PIXELS",
            "count": count, "delay": delay, "summary": summary, "regimes": regimes,
            "changes": changes, "prediction_receipts": predictions, "score_rows": scored,
            "delayed_supervised_feedback": True, "detector_engineered": True,
            "learned_physics": False, "autonomous_world_learning": False,
            "native_memory_write": False, "b8_promotion": False,
            "decision_authority": "KX108_ONLY", "verdict": "EXPERIMENTAL_ONLY"}


def encode(data):
    return (json.dumps(data, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False) + "\n").encode("utf-8")


def run(out, count=120, delay=2):
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("output directory is not empty")
    result = execute(count, delay)
    out.mkdir(parents=True, exist_ok=True)
    pre = encode(result["prediction_receipts"])
    (out/"predictions_pre_feedback.json").write_bytes(pre)
    result["precommit_sha256"] = sha256(pre).hexdigest()
    (out/"evaluation.json").write_bytes(encode(result))
    return result


def verify(out):
    out = Path(out)
    existing = json.loads((out/"evaluation.json").read_text(encoding="utf-8"))
    observed = (out/"predictions_pre_feedback.json").read_bytes()
    if sha256(observed).hexdigest() != existing["precommit_sha256"]:
        raise ValueError("pre-feedback digest mismatch")
    expected = execute(existing["count"], existing["delay"])
    expected["precommit_sha256"] = existing["precommit_sha256"]
    if encode(existing) != encode(expected) or observed != encode(expected["prediction_receipts"]):
        raise ValueError("replay mismatch")
    return {"verified": True, "count": existing["count"]}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--count", type=int, default=120)
    parser.add_argument("--delay", type=int, default=2)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args(argv)
    result = verify(args.out) if args.verify else run(args.out, args.count, args.delay)
    print(json.dumps({k: result[k] for k in
        ("verified", "count", "summary", "regimes", "changes") if k in result}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
