"""Preverbal World Experiment V0: predict a measurable change *before* the word.

A small experiment adapter ABOVE existing Obsidia F12/MMonde contracts. It
doesn't replace their time/state/trajectory types, recognize objects, infer
physics laws, train a general world model, or write memory. It consumes
explicit position observations with source / spatial frame / units and
compares a prediction against an UNSEEN future measurement.

The constant-acceleration candidate is a mathematical benchmark, not proof
that acceleration is caused by gravity, wind, an object, or camera movement.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
import json
from math import hypot, isfinite
from pathlib import Path
from typing import Any, Iterable


SOURCE_KINDS = frozenset(("OBSERVED_CLAIM", "SIMULATED", "GENERATED"))
MAX_INPUT_BYTES = 1024 * 1024


def _finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)


@dataclass(frozen=True)
class PositionMeasurementV0:
    """Measurement VIEW of one upstream MMonde/F12 sample; not a new WorldState."""
    entity_ref: str
    source_ref: str
    frame_ref: str
    time_s: float
    x: float
    y: float
    unit: str = "px"
    source_kind: str = "OBSERVED_CLAIM"
    uncertainty_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in ("entity_ref", "source_ref", "frame_ref", "unit"):
            field_value = getattr(self, field_name)
            if not isinstance(field_value, str) or not field_value.strip():
                raise ValueError(f"{field_name} is required")
        if self.frame_ref == "UNKNOWN":
            raise ValueError("unknown spatial reference frame: cannot compare trajectories")
        for name in ("time_s", "x", "y"):
            _finite_number(getattr(self, name), name)
        if self.source_kind not in SOURCE_KINDS:
            raise ValueError("source_kind must be OBSERVED_CLAIM, SIMULATED or GENERATED")
        object.__setattr__(self, "uncertainty_refs", tuple(self.uncertainty_refs))


def measurement_from_mmonde_world_observation(world_observation: Any) -> PositionMeasurementV0:
    """Read only upstream WorldObservationV0-shaped fields; fail rather than guess.

    Expected upstream state["position"] = {x, y, unit}; space["frame_ref"].
    This is a documented optional view, NOT an upstream F12 schema change.
    """
    if getattr(world_observation, "readonly", None) is not True:
        raise ValueError("upstream world observation must be readonly")
    if getattr(world_observation, "decision_authority", None) != "KX108_ONLY":
        raise ValueError("upstream decision authority mismatch")
    state = getattr(world_observation, "state", None)
    space = getattr(world_observation, "space", None)
    refs = getattr(world_observation, "source_refs", ())
    if not isinstance(state, dict) or not isinstance(space, dict):
        raise ValueError("upstream observation missing state/space maps")
    position = state.get("position")
    if not isinstance(position, dict):
        raise ValueError("upstream observation has no measured position")
    if not refs or not all(isinstance(s, str) and s.strip() for s in refs):
        raise ValueError("upstream observation lacks source references")
    observed_at = getattr(world_observation, "observed_at", "")
    if not isinstance(observed_at, str):
        raise ValueError("upstream observed_at must be ISO8601")
    try:
        dt = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("upstream observed_at must be ISO8601") from exc
    if dt.tzinfo is None:
        raise ValueError("observed_at needs a timezone")
    return PositionMeasurementV0(
        entity_ref=getattr(world_observation, "entity_ref", ""),
        source_ref=refs[0],
        frame_ref=space.get("frame_ref", ""),
        time_s=dt.timestamp(),
        x=position["x"],
        y=position["y"],
        unit=position.get("unit", ""),
        source_kind="OBSERVED_CLAIM",
        uncertainty_refs=tuple(getattr(world_observation, "uncertainty", ())),
    )


def _compatible(samples: Iterable[PositionMeasurementV0]) -> tuple[PositionMeasurementV0, ...]:
    items = tuple(samples)
    if not items:
        raise ValueError("no samples")
    reference = items[0]
    for sample in items:
        if (sample.entity_ref, sample.frame_ref, sample.unit, sample.source_kind) != (
            reference.entity_ref, reference.frame_ref, reference.unit, reference.source_kind
        ):
            raise ValueError("entity, spatial frame, units and source kind must match")
    for earlier, later in zip(items, items[1:]):
        if later.time_s <= earlier.time_s:
            raise ValueError("timestamps must be strictly increasing")
    return items


@dataclass(frozen=True)
class PredictionCandidateV0:
    entity_ref: str
    frame_ref: str
    unit: str
    source_kind: str
    history_source_refs: tuple[str, ...]
    future_time_s: float
    candidate_xy: tuple[float, float]
    linear_baseline_xy: tuple[float, float]
    stationary_baseline_xy: tuple[float, float]
    route: str = "FINITE_DIFFERENCE_CONSTANT_ACCELERATION_CANDIDATE"
    source_kind_verified_real: bool = False
    causal_proof: bool = False
    physical_law_proven: bool = False
    uncertainty_calibrated: bool = False
    readonly: bool = True
    memory_write_allowed: bool = False
    auto_promotion_allowed: bool = False
    decision_authority: str = "KX108_ONLY"
    allowed_to_act: bool = False


def predict_from_three(
    history: Iterable[PositionMeasurementV0], future_time_s: float
) -> PredictionCandidateV0:
    """Predict numerically from 3 past points; no use of the future's position."""
    items = _compatible(history)
    if len(items) != 3:
        raise ValueError("exactly three prior measurements are required")
    t0, t1, t2 = (p.time_s for p in items)
    t3 = _finite_number(future_time_s, "future_time_s")
    if t3 <= t2:
        raise ValueError("prediction target must be in the future")
    delta01 = t1 - t0
    delta12 = t2 - t1
    horizon = t3 - t2

    def _project(axis: str) -> tuple[float, float, float]:
        a, b, c = (getattr(p, axis) for p in items)
        v01 = (b - a) / delta01
        v12 = (c - b) / delta12
        accel = 2 * (v12 - v01) / (t2 - t0)
        end_velocity = v12 + .5 * accel * delta12
        proposed = c + end_velocity * horizon + .5 * accel * horizon * horizon
        linear = c + v12 * horizon
        if not all(isfinite(v) for v in (proposed, linear)):
            raise ValueError("predicted trajectory overflows; hold")
        return proposed, linear, c

    x = _project("x")
    y = _project("y")
    return PredictionCandidateV0(
        entity_ref=items[0].entity_ref,
        frame_ref=items[0].frame_ref,
        unit=items[0].unit,
        source_kind=items[0].source_kind,
        history_source_refs=tuple(p.source_ref for p in items),
        future_time_s=t3,
        candidate_xy=(x[0], y[0]),
        linear_baseline_xy=(x[1], y[1]),
        stationary_baseline_xy=(x[2], y[2]),
    )


def evaluate_with_heldout(
    prediction: PredictionCandidateV0, actual: PositionMeasurementV0
) -> dict[str, Any]:
    """Independent withheld measurement is supplied *after* prediction."""
    if (actual.entity_ref, actual.frame_ref, actual.unit, actual.source_kind) != (
        prediction.entity_ref, prediction.frame_ref,
        prediction.unit, prediction.source_kind
    ):
        raise ValueError("held-out measurement is incompatible with the forecast")
    if abs(actual.time_s - prediction.future_time_s) > 1e-6:
        raise ValueError("held-out timestamp doesn't match prediction horizon")
    if actual.source_ref in prediction.history_source_refs:
        raise ValueError("held-out observation must have a distinct source reference")
    def err(pos: tuple[float, float]) -> float:
        return hypot(pos[0] - actual.x, pos[1] - actual.y)
    proposed_error = err(prediction.candidate_xy)
    linear_error = err(prediction.linear_baseline_xy)
    static_error = err(prediction.stationary_baseline_xy)
    margin = max(1e-9, 1e-9 * max(proposed_error, linear_error))
    if proposed_error + margin < linear_error:
        outcome = "BETTER_THAN_LINEAR_BASELINE"
    elif linear_error + margin < proposed_error:
        outcome = "WORSE_THAN_LINEAR_BASELINE"
    else:
        outcome = "TIED_WITH_LINEAR_BASELINE"
    return {
        "schema_version": "BRODY_PREVERBAL_EPISODE_EVALUATION_V0",
        "prediction": asdict(prediction),
        "heldout_source_ref": actual.source_ref,
        "heldout_xy": [actual.x, actual.y],
        "error": {
            "proposed": proposed_error,
            "linear_baseline": linear_error,
            "stationary_baseline": static_error,
            "unit": actual.unit,
        },
        "comparison": outcome,
        "physics_causality": "UNKNOWN",
        "frame_stability_external_verification": "NOT_RUN",
        "generalization_test": "NOT_RUN",
        "epistemic_status": "ONE_EPISODE_CANDIDATE_ONLY",
        "world_knowledge_validated": False,
        "real_world_proven": False,
        "model_weight_update": False,
        "memory_write_allowed": False,
        "auto_promotion_allowed": False,
        "decision_authority": "KX108_ONLY",
        "allowed_to_act": False,
    }


def evaluate_four_measurements(
    measurements: Iterable[PositionMeasurementV0],
) -> dict[str, Any]:
    items = _compatible(measurements)
    if len(items) != 4:
        raise ValueError("four timestamped samples required: 3 history + 1 held-out")
    return evaluate_with_heldout(predict_from_three(items[:3], items[3].time_s), items[3])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Brody pre-verbal prediction: three source-tagged positions -> unseen fourth"
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    inp = args.input.resolve(strict=True)
    out = args.out.resolve()
    if out == inp:
        parser.error("output cannot overwrite input")
    if not 0 < inp.stat().st_size <= MAX_INPUT_BYTES:
        parser.error("input JSON must be nonempty and <=1MiB")
    payload = json.loads(inp.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("measurements"), list):
        parser.error("input JSON must contain measurements list")
    measurements = [PositionMeasurementV0(**p) for p in payload["measurements"]]
    evaluation = evaluate_four_measurements(measurements)
    evaluation["experiment_input_sha256"] = sha256(inp.read_bytes()).hexdigest()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(evaluation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "comparison": evaluation["comparison"],
        "error": evaluation["error"],
        "physical_knowledge_validated": False,
        "receipt": str(out),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
