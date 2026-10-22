"""M04-M06, M09: Multidimensional Navigation, Meaning-Driven Search & Procedural Admissibility.

Constitutional boundaries:
- KX108_ONLY remains the unique decision authority.
- memory_write_allowed = False.
- auto_promotion_allowed = False.
- emits_act = False.
- No eval/exec of memorized code.
- Semantic proximity is NEVER treated as proof of causality.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Any, Callable, Mapping

from .cognitive_memory_timeline_v1 import (
    CognitiveMemoryIndexV1,
    DomainEngagementV1,
    HistoricalBeliefRevisionV1,
    MultidimensionalExperienceV1,
    NativeMemoryAdmissibilityReportV1,
    SpecializedDomainV1,
    TimelineEnvelopeV1,
    TreeDefinitionV1,
    TreeFamilyV1,
    TreeProjectionV1,
)
from .contracts_v0 import DECISION_AUTHORITY, _assert_non_sovereign


# --- M04: Multidimensional Navigation Relations ---

class MultidimensionalRelationTypeV1(str, Enum):
    SIMILARITY = "SIMILARITY"
    DIFFERENCE = "DIFFERENCE"
    OPPOSITION = "OPPOSITION"
    ANALOGY = "ANALOGY"
    TRANSFORMATION = "TRANSFORMATION"
    DEPENDENCY = "DEPENDENCY"
    TEMPORAL = "TEMPORAL"
    CAUSAL_PROVEN = "CAUSAL_PROVEN"
    CAUSALITY_UNKNOWN = "CAUSALITY_UNKNOWN"


@dataclass(frozen=True)
class ExperienceRelationLinkV1:
    source_experience_id: str
    target_experience_id: str
    relation_type: MultidimensionalRelationTypeV1
    strength: float  # [0.0, 1.0]
    rationale: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (0.0 <= self.strength <= 1.0):
            raise ValueError("strength must be between 0.0 and 1.0")
        if self.relation_type == MultidimensionalRelationTypeV1.CAUSAL_PROVEN and not self.evidence_refs:
            raise ValueError("CAUSAL_PROVEN requires explicit independent evidence_refs")
        if not self.rationale.strip():
            raise ValueError("rationale is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_experience_id": self.source_experience_id,
            "target_experience_id": self.target_experience_id,
            "relation_type": self.relation_type.value,
            "strength": self.strength,
            "rationale": self.rationale,
            "evidence_refs": list(self.evidence_refs),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExperienceRelationLinkV1:
        return cls(
            source_experience_id=data["source_experience_id"],
            target_experience_id=data["target_experience_id"],
            relation_type=MultidimensionalRelationTypeV1(data["relation_type"]),
            strength=float(data["strength"]),
            rationale=data["rationale"],
            evidence_refs=tuple(data.get("evidence_refs", ())),
        )


# --- M05: Meaning-Driven Query Intent ---

class MeaningQueryIntentV1(str, Enum):
    HOW_DID_I_SUCCEED = "HOW_DID_I_SUCCEED"
    WHY_DID_I_FAIL = "WHY_DID_I_FAIL"
    WHAT_DID_I_BELIEVE_BEFORE = "WHAT_DID_I_BELIEVE_BEFORE"
    WHAT_DOES_THIS_RESEMBLE = "WHAT_DOES_THIS_RESEMBLE"
    WHICH_METHOD_IS_TRANSFERABLE = "WHICH_METHOD_IS_TRANSFERABLE"
    WHAT_CONTRADICTS_MY_EXPERIENCE = "WHAT_CONTRADICTS_MY_EXPERIENCE"
    WHICH_KNOWLEDGE_IS_VERIFIED = "WHICH_KNOWLEDGE_IS_VERIFIED"


@dataclass(frozen=True)
class MeaningQueryResultItemV1:
    experience_id: str
    score: float
    summary: str
    educational_stage: str
    method_refs: tuple[str, ...]
    evidence_hashes: tuple[str, ...]
    epistemic_flags: tuple[str, ...]
    counter_examples: tuple[str, ...]
    prior_belief_retained: str | None = None


@dataclass(frozen=True)
class MeaningQueryResponseV1:
    query_intent: MeaningQueryIntentV1
    results: tuple[MeaningQueryResultItemV1, ...]
    total_scanned: int
    matched_count: int
    causality_asserted: bool = False
    decision_authority: str = DECISION_AUTHORITY
    memory_write_allowed: bool = False


# --- M09: Visual Task Admissibility ---

@dataclass(frozen=True)
class VisualTaskAdmissibilityRequestV1:
    task_id: str
    target_domain: SpecializedDomainV1
    required_invariants: tuple[str, ...]
    canvas_dimensions: tuple[int, int]
    allowed_tolerance: float = 0.05
    requested_procedure: str | None = None


@dataclass(frozen=True)
class VisualTaskAdmissibilityVerdictV1:
    task_id: str
    experience_id: str
    is_admissible: bool
    status: str  # ADMISSIBLE, REJECTED_NEGATIVE_TRANSFER, INSUFFICIENT_CALIBRATION, UNKNOWN
    rationale: str
    suggested_procedure: str | None
    code_execution_permitted: bool = False  # NEVER True: execution requires governed engine
    decision_authority: str = DECISION_AUTHORITY


# --- Multidimensional Engine ---

class MultidimensionalCognitiveMemoryEngineV1:
    """M04-M06, M09: Multi-tree, multi-temporal, meaning-driven navigation engine."""

    def __init__(self, index: CognitiveMemoryIndexV1 | None = None) -> None:
        self.index = index or CognitiveMemoryIndexV1()
        self._links: list[ExperienceRelationLinkV1] = []

    def add_relation(self, link: ExperienceRelationLinkV1) -> None:
        self._links.append(link)

    def search_by_meaning(
        self,
        intent: MeaningQueryIntentV1,
        *,
        query_text: str = "",
        target_tree_id: str | None = None,
        target_domain: SpecializedDomainV1 | None = None,
        before_timestamp_iso: str | None = None,
        revision_id: str | None = None,
    ) -> MeaningQueryResponseV1:
        """M05: Search adapted to cognitive intent."""
        items: list[MeaningQueryResultItemV1] = []
        total_scanned = self.index.count()

        for exp_id, exp in self.index._experiences.items():
            match = False
            score = 0.0
            prior_belief = None

            if intent == MeaningQueryIntentV1.HOW_DID_I_SUCCEED:
                # High confidence, no failure pattern, clear procedure
                if exp.calibration.confidence_score >= 0.7 and not exp.calibration.counter_examples:
                    match = True
                    score = exp.calibration.confidence_score

            elif intent == MeaningQueryIntentV1.WHY_DID_I_FAIL:
                # Experience documented a counter-example or failure pattern
                if exp.calibration.counter_examples or exp.calibration.failure_boundaries:
                    match = True
                    score = 1.0 - exp.calibration.confidence_score

            elif intent == MeaningQueryIntentV1.WHAT_DID_I_BELIEVE_BEFORE:
                # Retrieve prior beliefs
                if revision_id:
                    prior = exp.get_belief_prior_to_revision(revision_id)
                    if prior:
                        match = True
                        score = 1.0
                        prior_belief = prior
                elif exp.timeline.revisions:
                    match = True
                    score = 0.9
                    prior_belief = exp.timeline.revisions[-1].prior_belief_claim

            elif intent == MeaningQueryIntentV1.WHAT_DOES_THIS_RESEMBLE:
                # Shared trees or shared domain
                tree_match = False
                if target_tree_id:
                    tree_match = any(p.tree_id == target_tree_id for p in exp.tree_projections)
                domain_match = False
                if target_domain:
                    domain_match = any(d.domain == target_domain for d in exp.domains)
                
                if (target_tree_id and tree_match) or (target_domain and domain_match):
                    match = True
                    score = 0.8
                elif not target_tree_id and not target_domain:
                    match = True
                    score = 0.5

            elif intent == MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE:
                # Must have validated procedures, high confidence, and explicit failure boundaries
                if exp.procedure_refs and exp.calibration.confidence_score >= 0.75:
                    match = True
                    score = exp.calibration.confidence_score

            elif intent == MeaningQueryIntentV1.WHAT_CONTRADICTS_MY_EXPERIENCE:
                # Explicit contradictions or counter-examples
                if exp.calibration.counter_examples or any(
                    "CONTRADICTION" in unc for unc in exp.calibration.uncertainties
                ):
                    match = True
                    score = 0.95

            elif intent == MeaningQueryIntentV1.WHICH_KNOWLEDGE_IS_VERIFIED:
                # Validated with cryptographic evidence hashes and reproducible
                if exp.calibration.evidence_hashes and exp.calibration.confidence_score >= 0.85:
                    match = True
                    score = exp.calibration.confidence_score

            if match:
                items.append(
                    MeaningQueryResultItemV1(
                        experience_id=exp.experience_id,
                        score=score,
                        summary=exp.intention_summary,
                        educational_stage=exp.timeline.educational_stage,
                        method_refs=exp.procedure_refs,
                        evidence_hashes=exp.calibration.evidence_hashes,
                        epistemic_flags=exp.calibration.uncertainties,
                        counter_examples=exp.calibration.counter_examples,
                        prior_belief_retained=prior_belief,
                    )
                )

        # Sort by score descending
        items.sort(key=lambda it: it.score, reverse=True)

        return MeaningQueryResponseV1(
            query_intent=intent,
            results=tuple(items),
            total_scanned=total_scanned,
            matched_count=len(items),
            causality_asserted=False,  # Proximity is not proof of causality
            decision_authority=DECISION_AUTHORITY,
            memory_write_allowed=False,
        )

    def check_task_admissibility(
        self,
        experience_id: str,
        request: VisualTaskAdmissibilityRequestV1,
    ) -> VisualTaskAdmissibilityVerdictV1:
        """M09: Rigorous check of skill admissibility for a new visual task."""
        exp = self.index.get(experience_id)
        if exp is None:
            return VisualTaskAdmissibilityVerdictV1(
                task_id=request.task_id,
                experience_id=experience_id,
                is_admissible=False,
                status="UNKNOWN_EXPERIENCE",
                rationale=f"Experience {experience_id} not found in memory index",
                suggested_procedure=None,
                code_execution_permitted=False,
            )

        # Domain match
        has_domain = any(d.domain == request.target_domain for d in exp.domains)
        if not has_domain:
            return VisualTaskAdmissibilityVerdictV1(
                task_id=request.task_id,
                experience_id=experience_id,
                is_admissible=False,
                status="DOMAIN_MISMATCH",
                rationale=f"Experience domain does not include requested {request.target_domain.value}",
                suggested_procedure=None,
                code_execution_permitted=False,
            )

        # Known counter-examples check (negative transfer avoidance)
        for ce in exp.calibration.counter_examples:
            for req_inv in request.required_invariants:
                if req_inv in ce:
                    return VisualTaskAdmissibilityVerdictV1(
                        task_id=request.task_id,
                        experience_id=experience_id,
                        is_admissible=False,
                        status="REJECTED_NEGATIVE_TRANSFER",
                        rationale=f"Negative transfer risk: counter-example '{ce}' clashes with requested '{req_inv}'",
                        suggested_procedure=None,
                        code_execution_permitted=False,
                    )

        # Calibration check
        if exp.calibration.confidence_score < 0.6:
            return VisualTaskAdmissibilityVerdictV1(
                task_id=request.task_id,
                experience_id=experience_id,
                is_admissible=False,
                status="INSUFFICIENT_CALIBRATION",
                rationale="Experience confidence score is below safe threshold (0.6)",
                suggested_procedure=None,
                code_execution_permitted=False,
            )


        # Failure boundary check
        requested_canvas_str = f"CANVAS_SIZE={request.canvas_dimensions[0]}x{request.canvas_dimensions[1]}"
        for boundary in exp.calibration.failure_boundaries:
            if boundary.startswith("CANVAS_SIZE=") and boundary != requested_canvas_str:
                return VisualTaskAdmissibilityVerdictV1(
                    task_id=request.task_id,
                    experience_id=experience_id,
                    is_admissible=False,
                    status="FAILURE_BOUNDARY_VIOLATION",
                    rationale=f"Task canvas {requested_canvas_str} violates experience boundary {boundary}",
                    suggested_procedure=None,
                    code_execution_permitted=False,
                )

        suggested = exp.procedure_refs[0] if exp.procedure_refs else None
        return VisualTaskAdmissibilityVerdictV1(
            task_id=request.task_id,
            experience_id=experience_id,
            is_admissible=True,
            status="ADMISSIBLE",
            rationale="Experience satisfies all domain, calibration, and boundary constraints",
            suggested_procedure=suggested,
            code_execution_permitted=False,  # Memory suggests, governor executes
        )

    def save_to_directory(self, dir_path: Path | str) -> dict[str, Any]:
        """Persists index experiences and relational graph to disk."""
        p = Path(dir_path)
        p.mkdir(parents=True, exist_ok=True)
        idx_res = self.index.save_to_directory(p)
        rel_file = p / "relations.jsonl"
        with rel_file.open("w", encoding="utf-8") as f:
            for link in self._links:
                f.write(json.dumps(link.to_dict(), ensure_ascii=False) + "\n")
        return {
            "saved_count": idx_res["saved_count"],
            "experiences": idx_res,
            "saved_relations_count": len(self._links),
            "relations_path": str(rel_file),
            "relations_sha256": sha256(rel_file.read_bytes()).hexdigest(),
        }

    def load_from_directory(
        self,
        dir_path: Path | str,
        storage_provenance: str = "HISTORICAL_PERSISTED",
    ) -> dict[str, Any]:
        """Loads both experiences and relational links from disk."""
        p = Path(dir_path)
        exp_count = self.index.load_from_directory(p, storage_provenance=storage_provenance)
        rel_file = p / "relations.jsonl"
        rel_count = 0
        if rel_file.is_file():
            with rel_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    d = json.loads(line)
                    self.add_relation(ExperienceRelationLinkV1.from_dict(d))
                    rel_count += 1
        return {
            "loaded_experiences": exp_count,
            "loaded_relations": rel_count,
            "storage_provenance": storage_provenance,
        }
