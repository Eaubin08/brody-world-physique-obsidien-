"""F0 learning-loop contracts for Brody World Physique Obsidia.

These contracts fill only the gaps isolated by the F0 cross-audit.

They deliberately DO NOT reimplement upstream Obsidia contracts such as:
- WorldObservationV0
- WorldStateV0
- TimeEnvelopeV0
- SpatialFrameRefV0
- TransitionV0
- TrajectoryV0
- MemoryCandidate

The external/upstream objects are accepted structurally (duck typing) so this
repository can remain dependency-light while preserving the canonical Obsidia
type ownership.

Constitutional boundary:
- representation only
- readonly
- no decision authority
- no action authority
- no kernel mutation
- no automatic memory promotion
- KX108_ONLY remains the decision authority
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping


DECISION_AUTHORITY = "KX108_ONLY"


class TransformationEpistemicClassV0(str, Enum):
    OBSERVED = "OBSERVED"
    PROPOSED = "PROPOSED"
    SIMULATED = "SIMULATED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"


class ProjectionKindV0(str, Enum):
    PREDICTED = "PREDICTED"
    SIMULATED = "SIMULATED"
    COUNTERFACTUAL = "COUNTERFACTUAL"


class ExperienceValidationStatusV0(str, Enum):
    CANDIDATE = "CANDIDATE"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    REPLAYED = "REPLAYED"


class MemoryEligibilityV0(str, Enum):
    INELIGIBLE = "INELIGIBLE"
    CANDIDATE_ONLY = "CANDIDATE_ONLY"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


def _require_nonempty(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} is required")


def _require_upstream_id(value: Any, attribute: str, contract_name: str) -> str:
    """Require the identifying attribute of an upstream canonical object.

    We do not import/copy the upstream type here. This keeps ownership of the
    actual MMonde/world contract in obsidia-x108-proofs.
    """
    identifier = getattr(value, attribute, None)
    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError(
            f"{contract_name} must expose non-empty upstream attribute {attribute}"
        )
    return identifier


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


def _normalize_tuple(values: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    if values is None:
        return ()
    return tuple(str(v) for v in values)


def _assert_non_sovereign(
    *,
    readonly: bool,
    decision_authority: str,
    allowed_to_decide: bool,
    allowed_to_act: bool,
    kernel_mutation: bool,
) -> None:
    if not readonly:
        raise ValueError("learning-loop contracts must remain readonly")
    if decision_authority != DECISION_AUTHORITY:
        raise ValueError("decision authority must remain KX108_ONLY")
    if allowed_to_decide:
        raise ValueError("learning-loop contracts cannot decide")
    if allowed_to_act:
        raise ValueError("learning-loop contracts cannot act")
    if kernel_mutation:
        raise ValueError("learning-loop contracts cannot mutate the kernel")


@dataclass(frozen=True)
class WorldTransformationV0:
    """Descriptive world transformation, never an execution authorization.

    This is intentionally NOT named ActionV0/WorldActionV0 because Obsidia
    already reserves WorldAction semantics for governed execution/readiness.
    """

    transformation_id: str
    transformation_kind: str
    time: Any
    schema_version: str = field(default="WORLD_TRANSFORMATION_V0", init=False)
    actor_ref: str | None = None
    target_refs: tuple[str, ...] = ()
    parameters: Mapping[str, Any] = field(default_factory=dict)
    spatial_frame: Any | None = None
    provenance_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    epistemic_class: TransformationEpistemicClassV0 = (
        TransformationEpistemicClassV0.UNKNOWN
    )
    uncertainty: tuple[str, ...] = ()
    readonly: bool = True
    decision_authority: str = DECISION_AUTHORITY
    allowed_to_decide: bool = False
    allowed_to_act: bool = False
    execution_authority: bool = False
    kernel_mutation: bool = False

    def __post_init__(self) -> None:
        _require_nonempty(self.transformation_id, "transformation_id")
        _require_nonempty(self.transformation_kind, "transformation_kind")
        _require_upstream_id(self.time, "observed_at", "TimeEnvelopeV0-compatible object")
        if self.spatial_frame is not None:
            _require_upstream_id(
                self.spatial_frame,
                "frame_ref",
                "SpatialFrameRefV0-compatible object",
            )
        if self.execution_authority:
            raise ValueError(
                "WorldTransformationV0 is descriptive and cannot hold WorldAction execution authority"
            )
        _assert_non_sovereign(
            readonly=self.readonly,
            decision_authority=self.decision_authority,
            allowed_to_decide=self.allowed_to_decide,
            allowed_to_act=self.allowed_to_act,
            kernel_mutation=self.kernel_mutation,
        )
        object.__setattr__(self, "target_refs", _normalize_tuple(self.target_refs))
        object.__setattr__(self, "parameters", _freeze_mapping(self.parameters))
        object.__setattr__(
            self, "provenance_refs", _normalize_tuple(self.provenance_refs)
        )
        object.__setattr__(self, "evidence_refs", _normalize_tuple(self.evidence_refs))
        object.__setattr__(self, "uncertainty", _normalize_tuple(self.uncertainty))
        if not isinstance(self.epistemic_class, TransformationEpistemicClassV0):
            object.__setattr__(
                self,
                "epistemic_class",
                TransformationEpistemicClassV0(str(self.epistemic_class)),
            )


@dataclass(frozen=True)
class WorldStateProjectionV0:
    """Predicted/simulated/counterfactual wrapper around upstream WorldStateV0."""

    projection_id: str
    base_state_ref: str
    projected_state: Any
    projection_kind: ProjectionKindV0
    model_or_rule_ref: str
    generated_at: str
    schema_version: str = field(default="WORLD_STATE_PROJECTION_V0", init=False)
    transformation_ref: str | None = None
    prediction_horizon: str | None = None
    assumptions: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    readonly: bool = True
    decision_authority: str = DECISION_AUTHORITY
    allowed_to_decide: bool = False
    allowed_to_act: bool = False
    kernel_mutation: bool = False

    def __post_init__(self) -> None:
        _require_nonempty(self.projection_id, "projection_id")
        _require_nonempty(self.base_state_ref, "base_state_ref")
        _require_nonempty(self.model_or_rule_ref, "model_or_rule_ref")
        _require_nonempty(self.generated_at, "generated_at")
        _require_upstream_id(
            self.projected_state,
            "world_state_id",
            "WorldStateV0-compatible object",
        )
        if not isinstance(self.projection_kind, ProjectionKindV0):
            object.__setattr__(
                self, "projection_kind", ProjectionKindV0(str(self.projection_kind))
            )
        _assert_non_sovereign(
            readonly=self.readonly,
            decision_authority=self.decision_authority,
            allowed_to_decide=self.allowed_to_decide,
            allowed_to_act=self.allowed_to_act,
            kernel_mutation=self.kernel_mutation,
        )
        object.__setattr__(self, "assumptions", _normalize_tuple(self.assumptions))
        object.__setattr__(self, "uncertainty", _normalize_tuple(self.uncertainty))
        object.__setattr__(
            self, "provenance_refs", _normalize_tuple(self.provenance_refs)
        )
        object.__setattr__(self, "evidence_refs", _normalize_tuple(self.evidence_refs))


@dataclass(frozen=True)
class WorldStateDeltaV0:
    """Difference between expected/baseline state and an observed world state.

    A delta is discrepancy evidence. It never proves why the discrepancy exists.
    """

    delta_id: str
    observed_world_state_ref: str
    schema_version: str = field(default="WORLD_STATE_DELTA_V0", init=False)
    projected_state_ref: str | None = None
    baseline_state_ref: str | None = None
    matched_invariant_refs: tuple[str, ...] = ()
    violated_invariant_refs: tuple[str, ...] = ()
    expected_changes: tuple[str, ...] = ()
    unexpected_changes: tuple[str, ...] = ()
    missing_expected_changes: tuple[str, ...] = ()
    metric_deltas: Mapping[str, Any] = field(default_factory=dict)
    continuity_status: str = "UNKNOWN"
    explanation_candidates: tuple[str, ...] = ()
    uncertainty: tuple[str, ...] = ()
    contradictions: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    causal_proof: bool = False
    readonly: bool = True
    decision_authority: str = DECISION_AUTHORITY
    allowed_to_decide: bool = False
    allowed_to_act: bool = False
    kernel_mutation: bool = False

    def __post_init__(self) -> None:
        _require_nonempty(self.delta_id, "delta_id")
        _require_nonempty(
            self.observed_world_state_ref, "observed_world_state_ref"
        )
        if not self.projected_state_ref and not self.baseline_state_ref:
            raise ValueError(
                "WorldStateDeltaV0 requires projected_state_ref or baseline_state_ref"
            )
        if self.causal_proof:
            raise ValueError(
                "WorldStateDeltaV0 cannot promote discrepancy to causal proof"
            )
        _assert_non_sovereign(
            readonly=self.readonly,
            decision_authority=self.decision_authority,
            allowed_to_decide=self.allowed_to_decide,
            allowed_to_act=self.allowed_to_act,
            kernel_mutation=self.kernel_mutation,
        )
        for name in (
            "matched_invariant_refs",
            "violated_invariant_refs",
            "expected_changes",
            "unexpected_changes",
            "missing_expected_changes",
            "explanation_candidates",
            "uncertainty",
            "contradictions",
            "provenance_refs",
        ):
            object.__setattr__(self, name, _normalize_tuple(getattr(self, name)))
        object.__setattr__(self, "metric_deltas", _freeze_mapping(self.metric_deltas))


@dataclass(frozen=True)
class WorldExperienceCandidateV0:
    """Compact learning episode; explicitly not canonical memory."""

    experience_id: str
    state_before_ref: str
    state_after_ref: str
    outcome: str
    schema_version: str = field(default="WORLD_EXPERIENCE_CANDIDATE_V0", init=False)
    context_refs: tuple[str, ...] = ()
    transformation_ref: str | None = None
    projection_ref: str | None = None
    delta_ref: str | None = None
    replay_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    repeat_count: int = 1
    validation_status: ExperienceValidationStatusV0 = (
        ExperienceValidationStatusV0.CANDIDATE
    )
    candidate_skill_refs: tuple[str, ...] = ()
    candidate_invariant_refs: tuple[str, ...] = ()
    memory_eligibility: MemoryEligibilityV0 = MemoryEligibilityV0.CANDIDATE_ONLY
    canonical_memory: bool = False
    memory_write_allowed: bool = False
    auto_promotion_allowed: bool = False
    readonly: bool = True
    decision_authority: str = DECISION_AUTHORITY
    allowed_to_decide: bool = False
    allowed_to_act: bool = False
    kernel_mutation: bool = False

    def __post_init__(self) -> None:
        _require_nonempty(self.experience_id, "experience_id")
        _require_nonempty(self.state_before_ref, "state_before_ref")
        _require_nonempty(self.state_after_ref, "state_after_ref")
        _require_nonempty(self.outcome, "outcome")
        if self.repeat_count < 1:
            raise ValueError("repeat_count must be >= 1")
        if self.canonical_memory:
            raise ValueError(
                "WorldExperienceCandidateV0 is not canonical memory"
            )
        if self.memory_write_allowed:
            raise ValueError(
                "WorldExperienceCandidateV0 cannot write canonical memory"
            )
        if self.auto_promotion_allowed:
            raise ValueError(
                "WorldExperienceCandidateV0 cannot auto-promote to memory"
            )
        if not isinstance(self.validation_status, ExperienceValidationStatusV0):
            object.__setattr__(
                self,
                "validation_status",
                ExperienceValidationStatusV0(str(self.validation_status)),
            )
        if not isinstance(self.memory_eligibility, MemoryEligibilityV0):
            object.__setattr__(
                self,
                "memory_eligibility",
                MemoryEligibilityV0(str(self.memory_eligibility)),
            )
        _assert_non_sovereign(
            readonly=self.readonly,
            decision_authority=self.decision_authority,
            allowed_to_decide=self.allowed_to_decide,
            allowed_to_act=self.allowed_to_act,
            kernel_mutation=self.kernel_mutation,
        )
        for name in (
            "context_refs",
            "replay_refs",
            "evidence_refs",
            "provenance_refs",
            "candidate_skill_refs",
            "candidate_invariant_refs",
        ):
            object.__setattr__(self, name, _normalize_tuple(getattr(self, name)))
