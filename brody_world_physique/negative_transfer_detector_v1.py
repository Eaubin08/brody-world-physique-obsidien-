"""Negative Transfer and Contradiction Detection Engine.

Provides rigorous pre-execution filtering:
1. Rejects negative transfer when candidate procedure is incompatible with task topology or domain.
2. Identifies explicit contradictions between prior beliefs and task constraints.
3. Detects collisions with registered failure boundaries and counter-examples.
4. Generates FAILURE_PATTERN_CANDIDATE to prevent wasteful computation.

Constitutional boundary:
- Candidate only: is_candidate = True.
- Decision authority: KX108_ONLY.
- Memory: Readonly, native_memory_write_allowed = False.
- Emits act: False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from .cognitive_memory_timeline_v1 import (
    MultidimensionalExperienceV1,
    SpecializedDomainV1,
)
from .multidimensional_retrieval_v2 import (
    VisualTaskAdmissibilityRequestV1,
    VisualTaskAdmissibilityVerdictV1,
)


@dataclass(frozen=True)
class NegativeTransferDiagnosticV1:
    """Diagnostic report explaining why a skill transfer was rejected or accepted."""
    task_id: str
    experience_id: str
    transfer_risk_level: str  # "NONE", "MILD_RISK", "HIGH_RISK_REJECTED", "CRITICAL_CONTRADICTION"
    is_safe_to_apply: bool
    rejection_reasons: tuple[str, ...]
    colliding_counter_examples: tuple[str, ...]
    epistemic_recommendation: str
    decision_authority: str = "KX108_ONLY"


class NegativeTransferDetectorV1:
    """Detects and prevents negative skill transfer and epistemic contradictions."""

    def evaluate_skill_transfer(
        self,
        exp: MultidimensionalExperienceV1,
        request: VisualTaskAdmissibilityRequestV1,
    ) -> NegativeTransferDiagnosticV1:
        rejection_reasons: list[str] = []
        colliding_counter_examples: list[str] = []

        # 1. Domain Compatibility Check
        has_domain = any(d.domain == request.target_domain for d in exp.domains)
        if not has_domain:
            rejection_reasons.append(
                f"DOMAIN_MISMATCH: Experience domains ({[d.domain.value for d in exp.domains]}) do not match requested {request.target_domain.value}"
            )

        # 2. Counter-Example Collision Check
        for ce in exp.calibration.counter_examples:
            for req_inv in request.required_invariants:
                if ce.lower() in req_inv.lower() or req_inv.lower() in ce.lower():
                    colliding_counter_examples.append(ce)
                    rejection_reasons.append(f"COUNTER_EXAMPLE_COLLISION: Requested invariant '{req_inv}' collides with known failure '{ce}'")

        # 3. Canvas Size & Scale Failure Boundary Check
        requested_canvas_str = f"CANVAS_SIZE={request.canvas_dimensions[0]}x{request.canvas_dimensions[1]}"
        for boundary in exp.calibration.failure_boundaries:
            if boundary.startswith("CANVAS_SIZE=") and boundary != requested_canvas_str:
                rejection_reasons.append(f"BOUNDARY_VIOLATION: Canvas {requested_canvas_str} violates experience boundary {boundary}")

        # 4. Epistemic Confidence Gate
        if exp.calibration.confidence_score < 0.60:
            rejection_reasons.append(f"INSUFFICIENT_CALIBRATION: Experience confidence ({exp.calibration.confidence_score}) is below safe threshold 0.60")

        is_safe = len(rejection_reasons) == 0
        risk_level = "NONE" if is_safe else ("HIGH_RISK_REJECTED" if colliding_counter_examples else "MILD_RISK")

        recommendation = (
            "Transfer approved: experience invariants and calibration align with task."
            if is_safe
            else "Transfer halted: risk of negative transfer or boundary contradiction detected."
        )

        return NegativeTransferDiagnosticV1(
            task_id=request.task_id,
            experience_id=exp.experience_id,
            transfer_risk_level=risk_level,
            is_safe_to_apply=is_safe,
            rejection_reasons=tuple(rejection_reasons),
            colliding_counter_examples=tuple(colliding_counter_examples),
            epistemic_recommendation=recommendation,
        )
