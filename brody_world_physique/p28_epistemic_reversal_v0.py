"""P2.8 synthetic sequential epistemic-reversal test, not autonomous world learning.

No native memory, canonical state or B8 writes. Ground truth is never read before
the pre-feedback prediction; delayed simulator feedback remains explicitly supervised.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass, field
from hashlib import sha256
import json
from pathlib import Path
from statistics import mean, median

SCHEMA = "BRODY_P28_EPISTEMIC_REVERSAL_V0"
ARMS = ("fixed_history", "observed_majority", "scoped_revisable")


@dataclass
class WorkingKnowledge:
    """Experimental local belief, NOT B8 PROMOTED nor durable memory."""
    residuals: dict = field(default_factory=lambda: {str(i): [] for i in range(5)})
    history: list = field(default_factory=list)
    group_ids: set = field(default_factory=set)

    def score(self, i):
        vals = self.residuals[str(i)]
        return median(vals) if vals else None

    def rank(self):
        known = [(self.score(i), i) for i in range(5) if self.score(i) is not None]
        return sorted(known)

    def apply_feedback(self, *, episode_id, group_id, observed_shifts, verified_camera):
        # Duplicates of one evidence group MUST NOT improve historical reliability.
        if group_id in self.group_ids:
            return False
        self.group_ids.add(group_id)
        before = self.rank()
        for i, shift in enumerate(observed_shifts):
            self.residuals[str(i)].append(abs(shift - verified_camera))
            self.residuals[str(i)] = self.residuals[str(i)][-12:]
        after = self.rank()
        self.history.append({"episode_id": episode_id, "group_id": group_id,
                             "previous_best": before[0][1] if before else None,
                             "new_best": after[0][1] if after else None,
                             "feedback_kind": "SUPERVISED_SIMULATOR_AFTER_PRECOMMIT"})
        return True


def episode(idx):
    # Deterministic generator whose reliable fiducial changes after epoch 30.
    # Corruptions are correlated: 4 wrong landmarks can agree against the truth.
    regime = 0 if idx < 30 else 1
    camera = (idx * 7) % 13 - 6
    world = (idx * 11) % 17 - 8
    reliable = 4 if regime == 0 else 0
    wrong = camera + (24 if idx % 2 else -24)
    shifts = [wrong] * 5
    shifts[reliable] = camera
    # An independent second reliable marker on some frames allows HOLD detection.
    if idx % 7 == 0:
        shifts[2] = camera
    return {"id": idx, "group_id": "frame-" + str(idx), "regime": regime,
            "world": world, "camera": camera, "apparent": world + camera,
            "shifts": shifts}


def decide(observed, ledger, intent="generate"):
    if intent not in ("generate", "explore", "explain"):
        raise ValueError("unsupported intent")
    shifts = observed["shifts"]
    apparent = observed["apparent"]
    ranked = ledger.rank()
    fixed = apparent - shifts[4]
    majority = apparent - median(shifts)
    # Historical reliability informs hypotheses, but abrupt unexpected
    # disagreement without independent feedback is not resolved as truth.
    if not ranked:
        chosen, reason = None, "HOLD_UNCALIBRATED"
    else:
        best_error, best_id = ranked[0]
        plausible = [i for err, i in ranked if err <= best_error + 1]
        # Explicit HOLD when historically plausible independent fiducials
        # disagree; never force a median that re-admits known bad sources.
        vals = [shifts[i] for i in plausible]
        if max(vals) - min(vals) > 2:
            chosen, reason = None, "HOLD_CONFLICT"
        else:
            chosen, reason = apparent - median(vals), "REUSED_SCOPED_BELIEF"
    # Intent changes effort request, never epistemic decision.
    effort = {"generate": "REUSE_OR_HOLD", "explore": "REQUEST_DISCRIMINATING_EVIDENCE",
              "explain": "REPORT_PROVENANCE_AND_UNCERTAINTY"}[intent]
    return {"predictions": {"fixed_history": fixed, "observed_majority": majority,
                             "scoped_revisable": chosen},
            "reason": reason, "goal_route": effort,
            "best_historical_id": ranked[0][1] if ranked else None,
            "knowledge_status": "WORKING_EXPERIMENTAL_ONLY",
            "decision_authority": "KX108_ONLY", "memory_write": False}


def execute(n=70, feedback_delay=1):
    if n < 50 or feedback_delay < 1 or feedback_delay > 10:
        raise ValueError("invalid experiment parameters")
    ledger = WorkingKnowledge()
    pending = []
    precommit = []
    scored = []
    for idx in range(n):
        item = episode(idx)
        # Only observations, not the 'world' or 'camera' fields, are available.
        observation = {"id": item["id"], "shifts": item["shifts"],
                       "apparent": item["apparent"]}
        prediction = decide(observation, ledger, intent=("generate", "explore", "explain")[idx % 3])
        precommit.append({"id": idx, "observed": observation, "prediction": prediction,
                          "prior_evidence_groups": len(ledger.group_ids)})
        # Evaluation truth is accessible AFTER prediction has been appended.
        scored.append({"id": idx, "regime": item["regime"],
                       "errors": {arm: abs(value - item["world"]) if value is not None else None
                                  for arm, value in prediction["predictions"].items()}})
        pending.append(item)
        if len(pending) >= feedback_delay:
            past = pending.pop(0)
            ledger.apply_feedback(episode_id=past["id"], group_id=past["group_id"],
                                  observed_shifts=past["shifts"], verified_camera=past["camera"])
    summaries = {}
    for arm in ARMS:
        vals = [s["errors"][arm] for s in scored if s["errors"][arm] is not None]
        summaries[arm] = {"coverage": len(vals)/n, "mean_error_px": mean(vals) if vals else None,
                          "catastrophic_over_10px": sum(v > 10 for v in vals)}
    return {"schema": SCHEMA, "source_kind": "SYNTHETIC_SUPERVISED_DELAYED_FEEDBACK",
            "no_native_memory_writes": True, "decision_authority": "KX108_ONLY",
            "learned_physics": False, "autonomous_perception": False,
            "status": "EXPERIMENTAL_DIAGNOSTIC_ONLY",
            "n": n, "feedback_delay": feedback_delay,
            "precommit": precommit, "scoring": scored, "summary": summaries,
            "revision_history": ledger.history,
            "independent_evidence_groups": len(ledger.group_ids)}


def canonical(data):
    return (json.dumps(data, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False) + "\n").encode("utf-8")


def run(out, n=70, feedback_delay=1):
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError("output path must be new or empty")
    result = execute(n, feedback_delay)
    out.mkdir(parents=True, exist_ok=True)
    pre = canonical(result["precommit"])
    (out/"predictions_pre_feedback.json").write_bytes(pre)
    result["precommit_sha256"] = sha256(pre).hexdigest()
    (out/"evaluation.json").write_bytes(canonical(result))
    return result


def verify(out):
    out = Path(out)
    saved = json.loads((out/"evaluation.json").read_text(encoding="utf-8"))
    pre = (out/"predictions_pre_feedback.json").read_bytes()
    if sha256(pre).hexdigest() != saved["precommit_sha256"]:
        raise ValueError("precommit tampered")
    expected = execute(saved["n"], saved["feedback_delay"])
    expected["precommit_sha256"] = saved["precommit_sha256"]
    if canonical(saved) != canonical(expected) or pre != canonical(expected["precommit"]):
        raise ValueError("replay mismatch")
    return True


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--n", type=int, default=70)
    p.add_argument("--delay", type=int, default=1)
    p.add_argument("--verify", action="store_true")
    args = p.parse_args(argv)
    if args.verify:
        print(json.dumps({"verified": verify(args.out)}))
    else:
        report = run(args.out, args.n, args.delay)
        print(json.dumps({"summary": report["summary"], "revisions": sum(
            x["previous_best"] != x["new_best"] for x in report["revision_history"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
