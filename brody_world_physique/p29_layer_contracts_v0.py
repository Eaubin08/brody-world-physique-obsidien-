"""P2.9 strict layer contracts: observations, relations, provisional knowledge, intent.

This is a local experimental boundary, never a replacement for B7/B8/B10.
No truth, oracle, user intent or memory authority can flow backward to perception.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PixelObservation:
    pair_id: str
    source_ref: str
    ball_apparent_dx: Optional[float]
    landmark_shifts: tuple[float, ...]
    quality: str
    # Deliberately no simulator truth, physical verdict, goal, confidence or anchor ID.


@dataclass(frozen=True)
class SpatialRelations:
    observation_ref: str
    coordinate_frame: str
    apparent_dx: Optional[float]
    landmark_shifts: tuple[float, ...]
    status: str


@dataclass(frozen=True)
class WorkingBelief:
    relation_ref: str
    inferred_world_dx: Optional[float]
    basis: str
    epistemic_status: str
    evidence_refs: tuple[str, ...]
    # Never B8 ClaimState.PROMOTED.


@dataclass(frozen=True)
class GoalRouting:
    goal: str
    action_hint: str
    belief: WorkingBelief


def represent(obs: PixelObservation, *, coordinate_frame: str) -> SpatialRelations:
    if not coordinate_frame:
        raise ValueError("coordinate frame required")
    if obs.quality != "MEASURED_PIXELS" or obs.ball_apparent_dx is None or len(obs.landmark_shifts) != 5:
        return SpatialRelations(obs.pair_id, coordinate_frame, None, (), "HOLD_PERCEPTION")
    return SpatialRelations(obs.pair_id, coordinate_frame, obs.ball_apparent_dx,
                            obs.landmark_shifts, "MEASURED_UNVERIFIED")


def infer(rel: SpatialRelations, *, historical_anchor_id: Optional[int]) -> WorkingBelief:
    if rel.status != "MEASURED_UNVERIFIED" or historical_anchor_id is None:
        return WorkingBelief(rel.observation_ref, None, "INSUFFICIENT_EVIDENCE",
                             "HOLD", (rel.observation_ref,))
    if not 0 <= historical_anchor_id < len(rel.landmark_shifts):
        raise ValueError("bad historical id")
    return WorkingBelief(rel.observation_ref,
                         rel.apparent_dx - rel.landmark_shifts[historical_anchor_id],
                         "PROVISIONAL_HISTORICAL_LANDMARK",
                         "WORKING_UNVERIFIED", (rel.observation_ref,))


def route(goal: str, belief: WorkingBelief) -> GoalRouting:
    mapping = {"generate": "GENERATE_FROM_AVAILABLE_REPRESENTATIONS",
               "explore": "COLLECT_DISCRIMINATING_OBSERVATIONS",
               "explain": "EXPLAIN_SCOPE_AND_EVIDENCE"}
    if goal not in mapping:
        raise ValueError("unsupported goal")
    hint = mapping[goal]
    if belief.inferred_world_dx is None:
        hint = "REQUEST_MISSING_EVIDENCE"
    return GoalRouting(goal, hint, belief)


BOUNDARY = {"memory_write": False, "b8_promotion": False, "emits_act": False,
            "kernel_mutation": False, "decision_authority": "KX108_ONLY"}
