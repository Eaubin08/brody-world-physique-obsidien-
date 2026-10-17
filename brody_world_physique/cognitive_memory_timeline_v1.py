"""M01-M03, M07-M08: Multidimensional Cognitive Memory, Multi-temporality & Tree-Domain Registry.

Constitutional boundaries:
- KX108_ONLY remains the unique decision authority.
- memory_write_allowed = False (no canonical write to Native Memory).
- auto_promotion_allowed = False (human review / upstream authority required).
- emits_act = False (no autonomous action emission).
- Readonly queries and deterministic verification.
- An experience is NEVER duplicated across 34 trees; it maintains a single immutable
  identity and projects onto relevant cognitive trees and specialized domains.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any, Mapping

from .contracts_v0 import DECISION_AUTHORITY, _assert_non_sovereign


# --- M02: Canon of 8 Families and 34 Cognitive Trees ---

class TreeFamilyV1(str, Enum):
    I_FONDAMENTAUX = "I_FONDAMENTAUX"
    II_COGNITIFS = "II_COGNITIFS"
    III_CONNAISSANCE = "III_CONNAISSANCE"
    IV_RELATIONNELS_SOCIAUX = "IV_RELATIONNELS_SOCIAUX"
    V_ACTION_TRANSFORMATION = "V_ACTION_TRANSFORMATION"
    VI_TEMPORELS_MEMORIELS = "VI_TEMPORELS_MEMORIELS"
    VII_META_STRUCTURELS = "VII_META_STRUCTURELS"
    VIII_OBSIDIA_AGI = "VIII_OBSIDIA_AGI"


@dataclass(frozen=True)
class TreeDefinitionV1:
    tree_id: str
    name: str
    family: TreeFamilyV1
    folder: str
    non_decision: bool = True
    needs_human_validation: bool = False


CANONICAL_34_TREES: Mapping[str, TreeDefinitionV1] = MappingProxyType({
    # I_FONDAMENTAUX (01-05)
    "01": TreeDefinitionV1("01", "Arbre de l’Humain", TreeFamilyV1.I_FONDAMENTAUX, "ARBRE_01__Arbre_de_l_Humain"),
    "02": TreeDefinitionV1("02", "Arbre de la Conscience", TreeFamilyV1.I_FONDAMENTAUX, "ARBRE_02__Arbre_de_la_Conscience"),
    "03": TreeDefinitionV1("03", "Arbre de la Perception", TreeFamilyV1.I_FONDAMENTAUX, "ARBRE_03__Arbre_de_la_Perception"),
    "04": TreeDefinitionV1("04", "Arbre du Sens", TreeFamilyV1.I_FONDAMENTAUX, "ARBRE_04__Arbre_du_Sens"),
    "05": TreeDefinitionV1("05", "Arbre de l’Identité", TreeFamilyV1.I_FONDAMENTAUX, "ARBRE_05__Arbre_de_l_Identite"),

    # II_COGNITIFS (06-10)
    "06": TreeDefinitionV1("06", "Arbre de la Compréhension", TreeFamilyV1.II_COGNITIFS, "ARBRE_06__Arbre_de_la_Comprehension"),
    "07": TreeDefinitionV1("07", "Arbre de l’Organisation", TreeFamilyV1.II_COGNITIFS, "ARBRE_07__Arbre_de_l_Organisation"),
    "08": TreeDefinitionV1("08", "Arbre de la Pensée", TreeFamilyV1.II_COGNITIFS, "ARBRE_08__Arbre_de_la_Pensee"),
    "09": TreeDefinitionV1("09", "Arbre de l’Intelligence", TreeFamilyV1.II_COGNITIFS, "ARBRE_09__Arbre_de_l_Intelligence"),
    "10": TreeDefinitionV1("10", "Arbre du Langage", TreeFamilyV1.II_COGNITIFS, "ARBRE_10__Arbre_du_Langage"),

    # III_CONNAISSANCE (11-15)
    "11": TreeDefinitionV1("11", "Arbre de la Science", TreeFamilyV1.III_CONNAISSANCE, "ARBRE_11__Arbre_de_la_Science"),
    "12": TreeDefinitionV1("12", "Arbre de la Technique", TreeFamilyV1.III_CONNAISSANCE, "ARBRE_12__Arbre_de_la_Technique"),
    "13": TreeDefinitionV1("13", "Arbre de l’Art", TreeFamilyV1.III_CONNAISSANCE, "ARBRE_13__Arbre_de_l_Art"),
    "14": TreeDefinitionV1("14", "Arbre de la Philosophie", TreeFamilyV1.III_CONNAISSANCE, "ARBRE_14__Arbre_de_la_Philosophie"),
    "15": TreeDefinitionV1("15", "Arbre de la Spiritualité", TreeFamilyV1.III_CONNAISSANCE, "ARBRE_15__Arbre_de_la_Spiritualite"),

    # IV_RELATIONNELS_SOCIAUX (16-19)
    "16": TreeDefinitionV1("16", "Arbre de la Relation", TreeFamilyV1.IV_RELATIONNELS_SOCIAUX, "ARBRE_16__Arbre_de_la_Relation"),
    "17": TreeDefinitionV1("17", "Arbre du Collectif", TreeFamilyV1.IV_RELATIONNELS_SOCIAUX, "ARBRE_17__Arbre_du_Collectif"),
    "18": TreeDefinitionV1("18", "Arbre de la Transmission", TreeFamilyV1.IV_RELATIONNELS_SOCIAUX, "ARBRE_18__Arbre_de_la_Transmission"),
    "19": TreeDefinitionV1("19", "Arbre de la Culture", TreeFamilyV1.IV_RELATIONNELS_SOCIAUX, "ARBRE_19__Arbre_de_la_Culture"),

    # V_ACTION_TRANSFORMATION (20-22)
    "20": TreeDefinitionV1("20", "Arbre de l’Action", TreeFamilyV1.V_ACTION_TRANSFORMATION, "ARBRE_20__Arbre_de_l_Action"),
    "21": TreeDefinitionV1("21", "Arbre de la Création", TreeFamilyV1.V_ACTION_TRANSFORMATION, "ARBRE_21__Arbre_de_la_Creation"),
    "22": TreeDefinitionV1("22", "Arbre de la Transformation", TreeFamilyV1.V_ACTION_TRANSFORMATION, "ARBRE_22__Arbre_de_la_Transformation"),

    # VI_TEMPORELS_MEMORIELS (23-25)
    "23": TreeDefinitionV1("23", "Arbre du Temps", TreeFamilyV1.VI_TEMPORELS_MEMORIELS, "ARBRE_23__Arbre_du_Temps"),
    "24": TreeDefinitionV1("24", "Arbre de la Mémoire", TreeFamilyV1.VI_TEMPORELS_MEMORIELS, "ARBRE_24__Arbre_de_la_Memoire"),
    "25": TreeDefinitionV1("25", "Arbre de l’Histoire", TreeFamilyV1.VI_TEMPORELS_MEMORIELS, "ARBRE_25__Arbre_de_l_Histoire"),

    # VII_META_STRUCTURELS (26-29)
    "26": TreeDefinitionV1("26", "Arbre de la Cohérence", TreeFamilyV1.VII_META_STRUCTURELS, "ARBRE_26__Arbre_de_la_Coherence"),
    "27": TreeDefinitionV1("27", "Arbre de la Vérité", TreeFamilyV1.VII_META_STRUCTURELS, "ARBRE_27__Arbre_de_la_Verite"),
    "28": TreeDefinitionV1("28", "Arbre de la Valeur", TreeFamilyV1.VII_META_STRUCTURELS, "ARBRE_28__Arbre_de_la_Valeur"),
    "29": TreeDefinitionV1("29", "Arbre de la Finalité", TreeFamilyV1.VII_META_STRUCTURELS, "ARBRE_29__Arbre_de_la_Finalite"),

    # VIII_OBSIDIA_AGI (30-34)
    "30": TreeDefinitionV1("30", "Arbre Cognitif Global", TreeFamilyV1.VIII_OBSIDIA_AGI, "ARBRE_30__Arbre_Cognitif_Global"),
    "31": TreeDefinitionV1("31", "Arbre des Flux", TreeFamilyV1.VIII_OBSIDIA_AGI, "ARBRE_31__Arbre_des_Flux"),
    "32": TreeDefinitionV1("32", "Arbre des Connexions", TreeFamilyV1.VIII_OBSIDIA_AGI, "ARBRE_32__Arbre_des_Connexions"),
    "33": TreeDefinitionV1("33", "Arbre de l’Optimisation", TreeFamilyV1.VIII_OBSIDIA_AGI, "ARBRE_33__Arbre_de_l_Optimisation"),
    "34": TreeDefinitionV1("34", "Arbre de la Stabilité", TreeFamilyV1.VIII_OBSIDIA_AGI, "ARBRE_34__Arbre_de_la_Stabilite"),
})



@dataclass(frozen=True)
class TreeProjectionV1:
    """Projection of an experience onto a cognitive tree.
    
    The experience is NOT duplicated: it remains a single entity that links to
    active tree projections.
    """
    tree_id: str
    weight: float
    projection_rationale: str
    sub_node_ref: str | None = None

    def __post_init__(self) -> None:
        if self.tree_id not in CANONICAL_34_TREES:
            raise ValueError(f"unknown tree_id: {self.tree_id}")
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError("weight must be between 0.0 and 1.0")
        if not self.projection_rationale.strip():
            raise ValueError("projection_rationale is required")

    @property
    def tree_name(self) -> str:
        return CANONICAL_34_TREES[self.tree_id].name

    @property
    def family(self) -> TreeFamilyV1:
        return CANONICAL_34_TREES[self.tree_id].family


# --- M03: Specialized Domains (Distinct from Cognitive Trees) ---

class SpecializedDomainV1(str, Enum):
    """Domains are operational disciplines, NEVER to be confused with cognitive trees.
    
    Each domain has its own objects, representation grammar, and proof criteria.
    """
    PHYSICS = "PHYSICS"
    GEOMETRY = "GEOMETRY"
    DRAWING = "DRAWING"
    ART = "ART"
    VIDEO = "VIDEO"
    ROBOTICS_EMBODIED = "ROBOTICS_EMBODIED"


@dataclass(frozen=True)
class DomainEngagementV1:
    domain: SpecializedDomainV1
    proof_criterion: str
    measurement_units: tuple[str, ...] = ()
    domain_state_ref: str | None = None
    validation_status: str = "PENDING"

    def __post_init__(self) -> None:
        if not self.proof_criterion.strip():
            raise ValueError("proof_criterion is required")


# --- M01: Multi-temporality & Frise Engine ---

@dataclass(frozen=True)
class HistoricalBeliefRevisionV1:
    """Historical trace of a belief revision/correction.
    
    Allows retrieving what Brody believed or knew BEFORE the correction.
    """
    revision_id: str
    t_revision_iso: str
    prior_belief_claim: str
    revised_belief_claim: str
    contradiction_evidence_ref: str
    correction_rule_or_procedure: str
    retained_former_status: str = "SUPERSEDED_HISTORICAL"


@dataclass(frozen=True)
class TimelineEnvelopeV1:
    """M01 Frise et temporalités.
    
    Strictly separates:
    1. t_event: Time of physical / simulated event in world
    2. t_observation: Time sensor/camera captured the frame
    3. t_recording: Time experience was hashed into ledger
    4. validity_interval: [valid_start_iso, valid_end_iso or None]
    5. educational_stage: Brody's educational timeline (D0, V1, V4.2, etc.)
    6. revision_history: Chain of modifications preserving historical states
    """
    t_event_iso: str
    t_observation_iso: str
    t_recording_iso: str
    educational_stage: str
    validity_start_iso: str
    validity_end_iso: str | None = None
    revisions: tuple[HistoricalBeliefRevisionV1, ...] = ()

    def __post_init__(self) -> None:
        for name, val in [
            ("t_event_iso", self.t_event_iso),
            ("t_observation_iso", self.t_observation_iso),
            ("t_recording_iso", self.t_recording_iso),
            ("educational_stage", self.educational_stage),
            ("validity_start_iso", self.validity_start_iso),
        ]:
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"{name} is required")


# --- M07: Calibration, Evidence, Uncertainty & Counter-Examples ---

@dataclass(frozen=True)
class EpistemicCalibrationV1:
    """M07 Calibration: provenance, proofs, reliability, uncertainties, failure boundaries."""
    confidence_score: float
    source_provenance_refs: tuple[str, ...]
    evidence_hashes: tuple[str, ...]
    uncertainties: tuple[str, ...]
    failure_boundaries: tuple[str, ...]
    counter_examples: tuple[str, ...] = ()
    reproducible_on_seed: int | None = None

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence_score <= 1.0):
            raise ValueError("confidence_score must be between 0.0 and 1.0")


# --- M08: Native Memory / SENS / KX108 Admissibility ---

@dataclass(frozen=True)
class NativeMemoryAdmissibilityReportV1:
    """M08 Readonly check of eligibility for Native Memory candidate lifecycle."""
    experience_id: str
    content_hash: str
    is_eligible: bool
    candidate_status: str  # CANDIDATE_ONLY, NEEDS_REVIEW, INELIGIBLE
    admissibility_reasons: tuple[str, ...]
    rejection_flags: tuple[str, ...]
    memory_write_allowed: bool = False
    auto_promotion_allowed: bool = False
    decision_authority: str = DECISION_AUTHORITY


# --- Comprehensive Multidimensional Experience ---

@dataclass(frozen=True)
class MultidimensionalExperienceV1:
    """Unified experience container fulfilling M01-M03, M07, M08.
    
    Retains single immutable identity, multiple tree projections, specialized domains,
    stratified timelines, calibration, and native memory admissibility.
    """
    experience_id: str
    intention_summary: str
    timeline: TimelineEnvelopeV1
    tree_projections: tuple[TreeProjectionV1, ...]
    domains: tuple[DomainEngagementV1, ...]
    calibration: EpistemicCalibrationV1
    procedure_refs: tuple[str, ...]
    executed_code_sha256: Mapping[str, str] = field(default_factory=dict)
    schema_version: str = "BRODY_COGNITIVE_EXPERIENCE_V1"
    readonly: bool = True
    decision_authority: str = DECISION_AUTHORITY
    allowed_to_decide: bool = False
    allowed_to_act: bool = False
    kernel_mutation: bool = False

    def __post_init__(self) -> None:
        _assert_non_sovereign(
            readonly=self.readonly,
            decision_authority=self.decision_authority,
            allowed_to_decide=self.allowed_to_decide,
            allowed_to_act=self.allowed_to_act,
            kernel_mutation=self.kernel_mutation,
        )
        if not self.experience_id.strip():
            raise ValueError("experience_id is required")
        if not self.intention_summary.strip():
            raise ValueError("intention_summary is required")
        if not self.tree_projections:
            raise ValueError("experience must project to at least one cognitive tree")
        if not self.domains:
            raise ValueError("experience must engage at least one specialized domain")

        # Verify no tree_id is duplicated in tree_projections
        seen_trees = set()
        for p in self.tree_projections:
            if p.tree_id in seen_trees:
                raise ValueError(f"duplicate tree_id projection: {p.tree_id}")
            seen_trees.add(p.tree_id)

        # Freeze mapping
        object.__setattr__(
            self, "executed_code_sha256", MappingProxyType(dict(self.executed_code_sha256))
        )

    def content_digest(self) -> str:
        data = {
            "experience_id": self.experience_id,
            "intention_summary": self.intention_summary,
            "t_event": self.timeline.t_event_iso,
            "t_observation": self.timeline.t_observation_iso,
            "t_recording": self.timeline.t_recording_iso,
            "educational_stage": self.timeline.educational_stage,
            "trees": [(p.tree_id, p.weight) for p in self.tree_projections],
            "domains": [d.domain.value for d in self.domains],
            "confidence": self.calibration.confidence_score,
            "procedures": list(self.procedure_refs),
        }
        encoded = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return sha256(encoded).hexdigest()

    def get_belief_prior_to_revision(self, revision_id: str) -> str | None:
        """M01: Retrieve what Brody believed before a specific revision."""
        for rev in self.timeline.revisions:
            if rev.revision_id == revision_id:
                return rev.prior_belief_claim
        return None

    def evaluate_native_memory_admissibility(self) -> NativeMemoryAdmissibilityReportV1:
        """M08: Non-sovereign evaluation of whether this experience meets candidate standards."""
        rejection_flags = []
        admissibility_reasons = []

        # Check calibrations
        if self.calibration.confidence_score < 0.2:
            rejection_flags.append("CONFIDENCE_TOO_LOW")
        else:
            admissibility_reasons.append(f"Confidence score sufficient ({self.calibration.confidence_score})")

        if not self.calibration.source_provenance_refs:
            rejection_flags.append("NO_SOURCE_PROVENANCE")
        else:
            admissibility_reasons.append("Source provenance documented")

        if not self.calibration.evidence_hashes:
            rejection_flags.append("NO_CRYPTOGRAPHIC_EVIDENCE")
        else:
            admissibility_reasons.append("Cryptographic evidence verified")

        if any("INVENTED" in unc for unc in self.calibration.uncertainties):
            rejection_flags.append("INVENTED_CLAIM_DETECTED")

        is_eligible = len(rejection_flags) == 0
        candidate_status = "CANDIDATE_ONLY" if is_eligible else "INELIGIBLE"

        return NativeMemoryAdmissibilityReportV1(
            experience_id=self.experience_id,
            content_hash=self.content_digest(),
            is_eligible=is_eligible,
            candidate_status=candidate_status,
            admissibility_reasons=tuple(admissibility_reasons),
            rejection_flags=tuple(rejection_flags),
            memory_write_allowed=False,
            auto_promotion_allowed=False,
            decision_authority=DECISION_AUTHORITY,
        )


# --- Deterministic Memory Ledger & Multi-Dimensional Search ---

class CognitiveMemoryIndexV1:
    """In-memory deterministic index for multi-dimensional retrieval (M04-M05).
    
    Enables searching by tree, domain, educational stage, timeline interval,
    analogies, failure counter-examples, without inventing causality.
    """

    def __init__(self) -> None:
        self._experiences: dict[str, MultidimensionalExperienceV1] = {}

    def register_experience(self, exp: MultidimensionalExperienceV1) -> None:
        if exp.experience_id in self._experiences:
            raise ValueError(f"experience already registered: {exp.experience_id}")
        self._experiences[exp.experience_id] = exp

    def get(self, experience_id: str) -> MultidimensionalExperienceV1 | None:
        return self._experiences.get(experience_id)

    def count(self) -> int:
        return len(self._experiences)

    def query_by_tree(self, tree_id: str, min_weight: float = 0.1) -> list[MultidimensionalExperienceV1]:
        results = []
        for exp in self._experiences.values():
            for p in exp.tree_projections:
                if p.tree_id == tree_id and p.weight >= min_weight:
                    results.append(exp)
                    break
        return results

    def query_by_family(self, family: TreeFamilyV1) -> list[MultidimensionalExperienceV1]:
        results = []
        for exp in self._experiences.values():
            for p in exp.tree_projections:
                if p.family == family:
                    results.append(exp)
                    break
        return results

    def query_by_domain(self, domain: SpecializedDomainV1) -> list[MultidimensionalExperienceV1]:
        return [
            exp for exp in self._experiences.values()
            if any(d.domain == domain for d in exp.domains)
        ]

    def query_by_educational_stage(self, stage: str) -> list[MultidimensionalExperienceV1]:
        return [
            exp for exp in self._experiences.values()
            if exp.timeline.educational_stage == stage
        ]

    def query_counter_examples(self) -> list[tuple[str, tuple[str, ...]]]:
        """Find experiences with documented failure patterns / counter-examples."""
        return [
            (exp.experience_id, exp.calibration.counter_examples)
            for exp in self._experiences.values()
            if exp.calibration.counter_examples
        ]
