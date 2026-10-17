"""Unit tests for M04-M06, M09 multidimensional navigation and meaning-driven retrieval."""
import pytest

from brody_world_physique.cognitive_memory_timeline_v1 import (
    CognitiveMemoryIndexV1,
    DomainEngagementV1,
    EpistemicCalibrationV1,
    HistoricalBeliefRevisionV1,
    MultidimensionalExperienceV1,
    SpecializedDomainV1,
    TimelineEnvelopeV1,
    TreeProjectionV1,
)
from brody_world_physique.contracts_v0 import DECISION_AUTHORITY
from brody_world_physique.multidimensional_retrieval_v2 import (
    ExperienceRelationLinkV1,
    MeaningQueryIntentV1,
    MultidimensionalCognitiveMemoryEngineV1,
    MultidimensionalRelationTypeV1,
    VisualTaskAdmissibilityRequestV1,
)


@pytest.fixture
def populated_engine() -> MultidimensionalCognitiveMemoryEngineV1:
    index = CognitiveMemoryIndexV1()

    # Exp 1: Success on drawing circles (DESSIN_V1)
    rev1 = HistoricalBeliefRevisionV1(
        revision_id="REV-CIRCLE-01",
        t_revision_iso="2026-10-08T12:30:00Z",
        prior_belief_claim="Circle is tangent lines only",
        revised_belief_claim="Circle is radial closed continuous curve",
        contradiction_evidence_ref="sha256:circle_evidence_01",
        correction_rule_or_procedure="correct_drawing",
    )
    exp1 = MultidimensionalExperienceV1(
        experience_id="EXP-CIRCLE-SUCCESS",
        intention_summary="Mastered drawing closed radial circle",
        timeline=TimelineEnvelopeV1(
            t_event_iso="2026-10-08T12:00:00Z",
            t_observation_iso="2026-10-08T12:00:01Z",
            t_recording_iso="2026-10-08T12:05:00Z",
            educational_stage="DESSIN_V1",
            validity_start_iso="2026-10-08T12:05:00Z",
            revisions=(rev1,),
        ),
        tree_projections=(
            TreeProjectionV1("03", 0.95, "Perception"),
            TreeProjectionV1("13", 0.85, "Art and gestures"),
            TreeProjectionV1("24", 0.80, "Memory replay"),
        ),
        domains=(
            DomainEngagementV1(SpecializedDomainV1.DRAWING, "Pixel XOR strictly decreases"),
            DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Radial symmetry"),
        ),
        calibration=EpistemicCalibrationV1(
            confidence_score=0.92,
            source_provenance_refs=("teacher_images/cours_cercle.png",),
            evidence_hashes=("sha256:teacher_cercle_hash",),
            uncertainties=(),
            failure_boundaries=("CANVAS_SIZE=64x64",),
            counter_examples=(),
            reproducible_on_seed=42,
        ),
        procedure_refs=("brody_world_physique.drawing_school_v1:render",),
    )

    # Exp 2: Failure on adversarial inverted layout (V4.1)
    exp2 = MultidimensionalExperienceV1(
        experience_id="EXP-INVERTED-FAILURE",
        intention_summary="Proximity classified inverted order as near (adversarial false positive)",
        timeline=TimelineEnvelopeV1(
            t_event_iso="2026-10-09T08:00:00Z",
            t_observation_iso="2026-10-09T08:00:02Z",
            t_recording_iso="2026-10-09T08:01:00Z",
            educational_stage="ORIENTATION_V4_1",
            validity_start_iso="2026-10-09T08:01:00Z",
        ),
        tree_projections=(
            TreeProjectionV1("03", 0.8, "Perception"),
            TreeProjectionV1("26", 0.9, "Coherence"),
        ),
        domains=(
            DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Euclidean component distance"),
        ),
        calibration=EpistemicCalibrationV1(
            confidence_score=0.45,
            source_provenance_refs=("images/exam_inverted.png",),
            evidence_hashes=("sha256:exam_inverted_hash",),
            uncertainties=("ORIENTATION_BLINDNESS_IN_PROXIMITY",),
            failure_boundaries=("CANVAS_SIZE=64x64", "TWO_COMPONENTS_ONLY"),
            counter_examples=("INVERTED_ORDER_CONFUSION",),
        ),
        procedure_refs=("brody_world_physique.world_relations_school_v4_1:classify",),
    )

    # Exp 3: Reciprocal orientation success (V4.2)
    exp3 = MultidimensionalExperienceV1(
        experience_id="EXP-ORIENTATION-RECIPROCAL",
        intention_summary="Orientation LEFT-RIGHT reciprocity confirmed",
        timeline=TimelineEnvelopeV1(
            t_event_iso="2026-10-09T16:00:00Z",
            t_observation_iso="2026-10-09T16:00:01Z",
            t_recording_iso="2026-10-09T16:05:00Z",
            educational_stage="ORIENTATION_V4_2",
            validity_start_iso="2026-10-09T16:05:00Z",
        ),
        tree_projections=(
            TreeProjectionV1("03", 0.85, "Perception"),
            TreeProjectionV1("22", 0.90, "Transformation"),
            TreeProjectionV1("07", 0.75, "Organisation"),
        ),
        domains=(
            DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Opposite direction vector"),
            DomainEngagementV1(SpecializedDomainV1.PHYSICS, "Relative 2D reference frame"),
        ),
        calibration=EpistemicCalibrationV1(
            confidence_score=0.95,
            source_provenance_refs=("images/train_orientation_01.png",),
            evidence_hashes=("sha256:orientation_reciprocal_hash",),
            uncertainties=(),
            failure_boundaries=("CANVAS_SIZE=64x64", "CARDINAL_DIRECTIONS_ONLY"),
            counter_examples=(),
        ),
        procedure_refs=("brody_world_physique.world_orientation_school_v4_2:derive_reciprocal",),
    )

    index.register_experience(exp1)
    index.register_experience(exp2)
    index.register_experience(exp3)

    engine = MultidimensionalCognitiveMemoryEngineV1(index)
    return engine


def test_relation_link_validation():
    # Valid similarity relation
    link1 = ExperienceRelationLinkV1(
        source_experience_id="EXP-01",
        target_experience_id="EXP-02",
        relation_type=MultidimensionalRelationTypeV1.SIMILARITY,
        strength=0.75,
        rationale="Shared 8-neighbor connected component segmentation",
    )
    assert link1.relation_type == MultidimensionalRelationTypeV1.SIMILARITY

    # CAUSAL_PROVEN without evidence_refs must raise ValueError
    with pytest.raises(ValueError, match="CAUSAL_PROVEN requires explicit independent evidence_refs"):
        ExperienceRelationLinkV1(
            source_experience_id="EXP-01",
            target_experience_id="EXP-02",
            relation_type=MultidimensionalRelationTypeV1.CAUSAL_PROVEN,
            strength=0.9,
            rationale="Asserted gravity caused fall",
            evidence_refs=(),
        )

    # CAUSAL_PROVEN with evidence_refs is allowed
    link_causal = ExperienceRelationLinkV1(
        source_experience_id="EXP-01",
        target_experience_id="EXP-02",
        relation_type=MultidimensionalRelationTypeV1.CAUSAL_PROVEN,
        strength=0.9,
        rationale="Controlled actuator collision verified by dual high-speed cameras",
        evidence_refs=("sha256:cam0_hash", "sha256:cam1_hash"),
    )
    assert link_causal.relation_type == MultidimensionalRelationTypeV1.CAUSAL_PROVEN


def test_meaning_search_how_did_i_succeed(populated_engine):
    res = populated_engine.search_by_meaning(MeaningQueryIntentV1.HOW_DID_I_SUCCEED)
    assert res.query_intent == MeaningQueryIntentV1.HOW_DID_I_SUCCEED
    assert res.causality_asserted is False
    assert res.matched_count == 2
    # EXP-ORIENTATION-RECIPROCAL (0.95) and EXP-CIRCLE-SUCCESS (0.92)
    ids = [item.experience_id for item in res.results]
    assert "EXP-ORIENTATION-RECIPROCAL" in ids
    assert "EXP-CIRCLE-SUCCESS" in ids
    assert "EXP-INVERTED-FAILURE" not in ids


def test_meaning_search_why_did_i_fail(populated_engine):
    res = populated_engine.search_by_meaning(MeaningQueryIntentV1.WHY_DID_I_FAIL)
    assert res.query_intent == MeaningQueryIntentV1.WHY_DID_I_FAIL
    assert res.matched_count >= 1
    # EXP-INVERTED-FAILURE must be returned with its counter-example
    fail_item = res.results[0]
    assert fail_item.experience_id == "EXP-INVERTED-FAILURE"
    assert "INVERTED_ORDER_CONFUSION" in fail_item.counter_examples


def test_meaning_search_what_did_i_believe_before(populated_engine):
    res = populated_engine.search_by_meaning(
        MeaningQueryIntentV1.WHAT_DID_I_BELIEVE_BEFORE,
        revision_id="REV-CIRCLE-01",
    )
    assert res.matched_count == 1
    item = res.results[0]
    assert item.experience_id == "EXP-CIRCLE-SUCCESS"
    assert item.prior_belief_retained == "Circle is tangent lines only"


def test_meaning_search_what_does_this_resemble(populated_engine):
    # Query resemblance by tree 13 (Arbre de l'Art)
    res_art = populated_engine.search_by_meaning(
        MeaningQueryIntentV1.WHAT_DOES_THIS_RESEMBLE,
        target_tree_id="13",
    )
    assert res_art.matched_count == 1
    assert res_art.results[0].experience_id == "EXP-CIRCLE-SUCCESS"

    # Query resemblance by domain PHYSICS
    res_phys = populated_engine.search_by_meaning(
        MeaningQueryIntentV1.WHAT_DOES_THIS_RESEMBLE,
        target_domain=SpecializedDomainV1.PHYSICS,
    )
    assert res_phys.matched_count == 1
    assert res_phys.results[0].experience_id == "EXP-ORIENTATION-RECIPROCAL"


def test_meaning_search_which_knowledge_is_verified(populated_engine):
    res = populated_engine.search_by_meaning(MeaningQueryIntentV1.WHICH_KNOWLEDGE_IS_VERIFIED)
    assert res.matched_count == 2
    for item in res.results:
        assert len(item.evidence_hashes) > 0


def test_visual_task_admissibility_cases(populated_engine):
    # 1. Admissible task
    req_good = VisualTaskAdmissibilityRequestV1(
        task_id="TASK-CIRCLE-TEST",
        target_domain=SpecializedDomainV1.DRAWING,
        required_invariants=("Radial symmetry",),
        canvas_dimensions=(64, 64),
    )
    verdict_good = populated_engine.check_task_admissibility("EXP-CIRCLE-SUCCESS", req_good)
    assert verdict_good.is_admissible is True
    assert verdict_good.status == "ADMISSIBLE"
    assert verdict_good.code_execution_permitted is False  # Memory never authorizes arbitrary exec
    assert verdict_good.suggested_procedure == "brody_world_physique.drawing_school_v1:render"

    # 2. Reject domain mismatch
    req_wrong_domain = VisualTaskAdmissibilityRequestV1(
        task_id="TASK-WRONG-DOM",
        target_domain=SpecializedDomainV1.VIDEO,
        required_invariants=(),
        canvas_dimensions=(64, 64),
    )
    verdict_dom = populated_engine.check_task_admissibility("EXP-CIRCLE-SUCCESS", req_wrong_domain)
    assert verdict_dom.is_admissible is False
    assert verdict_dom.status == "DOMAIN_MISMATCH"

    # 3. Reject negative transfer clash
    req_negative_transfer = VisualTaskAdmissibilityRequestV1(
        task_id="TASK-INVERTED",
        target_domain=SpecializedDomainV1.GEOMETRY,
        required_invariants=("INVERTED_ORDER_CONFUSION",),
        canvas_dimensions=(64, 64),
    )
    verdict_neg = populated_engine.check_task_admissibility("EXP-INVERTED-FAILURE", req_negative_transfer)
    assert verdict_neg.is_admissible is False
    assert verdict_neg.status == "REJECTED_NEGATIVE_TRANSFER"

    # 4. Reject failure boundary violation (Canvas 128x128 vs 64x64)
    req_wrong_canvas = VisualTaskAdmissibilityRequestV1(
        task_id="TASK-BIG-CANVAS",
        target_domain=SpecializedDomainV1.DRAWING,
        required_invariants=(),
        canvas_dimensions=(128, 128),
    )
    verdict_bound = populated_engine.check_task_admissibility("EXP-CIRCLE-SUCCESS", req_wrong_canvas)
    assert verdict_bound.is_admissible is False
    assert verdict_bound.status == "FAILURE_BOUNDARY_VIOLATION"
