"""P2.9d: reuse original Brody organs without inventing new authority.

This is a read-only candidate experience bridge from existing typed pixel/spatial
steps to existing WorldStateDelta / WorldExperience and Reverso learning triage.
It does not claim physical verification, durable memory, nor 360-degree geometry.
"""
from __future__ import annotations
from dataclasses import asdict
from hashlib import sha256
import json
from types import MappingProxyType

from .p29_layer_contracts_v0 import PixelObservation, represent, WorkingBelief, route
from .contracts_v0 import WorldStateDeltaV0, WorldExperienceCandidateV0
from .reverso_learning_v0 import LearningEpisodeSignalV0, triage_learning

BRIDGE_SCHEMA = "BRODY_P29D_REUSE_ORGANS_V0"
ORGAN_SOURCES = MappingProxyType({
    "perception": "p29_layer_contracts_v0.PixelObservation",
    "spatial": "p29_layer_contracts_v0.SpatialRelations",
    "epistemic": "p29_layer_contracts_v0.WorkingBelief",
    "delta": "contracts_v0.WorldStateDeltaV0",
    "experience": "contracts_v0.WorldExperienceCandidateV0",
    "learning_triage": "reverso_learning_v0.triage_learning",
    "intent": "p29_layer_contracts_v0.route",
})


def _ref(data):
    return "sha256:" + sha256(json.dumps(data, sort_keys=True,
                      separators=(",", ":"), default=str).encode()).hexdigest()


def reconnect(*, pair_id: str, source_ref: str, measurement: dict | None,
              observation_status: str, frame_ref: str, anchor_id: int | None,
              goal: str, prior_prediction: float | None = None,
              independent_evidence_refs: tuple[str, ...] = (),
              replay_confirmed: bool = False):
    """Build linked *candidate* objects; no truth oracle or memory-write dependency."""
    if not source_ref or not pair_id:
        raise ValueError("source and episode IDs required")
    obs = PixelObservation(
        pair_id=pair_id, source_ref=source_ref,
        ball_apparent_dx=measurement["apparent"] if measurement else None,
        landmark_shifts=tuple(measurement["shifts"]) if measurement else (),
        quality=observation_status)
    rel = represent(obs, coordinate_frame=frame_ref)
    if rel.status == "MEASURED_UNVERIFIED" and anchor_id is not None:
        if not 0 <= anchor_id < len(rel.landmark_shifts):
            raise ValueError("invalid anchor")
        prediction = rel.apparent_dx - rel.landmark_shifts[anchor_id]
    else:
        prediction = None
    belief = WorkingBelief(
        relation_ref=rel.observation_ref, inferred_world_dx=prediction,
        basis="SCOPED_ANCHOR_CANDIDATE" if prediction is not None else "HOLD_UNRESOLVED",
        epistemic_status="WORKING_UNVERIFIED" if prediction is not None else "HOLD",
        evidence_refs=(source_ref,))
    intent = route(goal, belief)
    key = _ref({"source":source_ref, "pair":pair_id, "frame":frame_ref})
    # Reuse the project's original, non-sovereign F0 contracts.
    # This delta describes a prediction disagreement, NOT a causal explanation.
    disagreements = ()
    if prior_prediction is not None and prediction is not None and abs(prior_prediction-prediction)>2:
        disagreements = ("PRIOR_VS_CURRENT_PREDICTION",)
    delta = WorldStateDeltaV0(
        delta_id="delta-"+key, observed_world_state_ref="candidate-observation:"+key,
        baseline_state_ref="candidate-before:"+key,
        contradictions=disagreements, provenance_refs=(source_ref,),
        uncertainty=("NO_PHYSICAL_TRUTH_ORACLE",))
    experience = WorldExperienceCandidateV0(
        experience_id="experience-"+key,
        state_before_ref="candidate-before:"+key,
        state_after_ref="candidate-observation:"+key,
        outcome="UNVERIFIED_WORKING_PREDICTION" if prediction is not None else "HOLD",
        context_refs=(frame_ref,), delta_ref=delta.delta_id,
        evidence_refs=(source_ref,), replay_refs=(pair_id,))
    signal = LearningEpisodeSignalV0(
        kind="HYPOTHESIS", route_ref="P29D_SCOPED_ANCHOR",
        source_ref=source_ref, outcome="UNKNOWN",
        independent_evidence_refs=tuple(independent_evidence_refs),
        replay_confirmed=replay_confirmed)
    proposal = triage_learning(signal)
    return {"schema":BRIDGE_SCHEMA,
            "pixel":asdict(obs), "spatial":asdict(rel),
            "belief":asdict(belief),
            "goal":{"goal":goal, "action_hint":intent.action_hint},
            "delta":{"id":delta.delta_id,"contradictions":list(delta.contradictions),
                     "uncertainty":list(delta.uncertainty),"causal_proof":delta.causal_proof},
            "experience":{"id":experience.experience_id,"outcome":experience.outcome,
                          "memory_write_allowed":experience.memory_write_allowed,
                          "canonical_memory":experience.canonical_memory},
            "learning_triage":proposal,
            "organs":dict(ORGAN_SOURCES),
            "b8_promotion":False,"memory_write":False,
            "decision_authority":"KX108_ONLY"}
