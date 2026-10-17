"""Unit tests for M01-M03, M07, M08 cognitive memory, timeline, trees, and domains."""
import pytest

from brody_world_physique.cognitive_memory_timeline_v1 import (
    CANONICAL_34_TREES,
    CognitiveMemoryIndexV1,
    DomainEngagementV1,
    EpistemicCalibrationV1,
    HistoricalBeliefRevisionV1,
    MultidimensionalExperienceV1,
    NativeMemoryAdmissibilityReportV1,
    SpecializedDomainV1,
    TimelineEnvelopeV1,
    TreeDefinitionV1,
    TreeFamilyV1,
    TreeProjectionV1,
)
from brody_world_physique.contracts_v0 import DECISION_AUTHORITY


def test_canonical_34_trees_completeness_and_families():
    assert len(CANONICAL_34_TREES) == 34
    
    # Check 8 families
    families = {tree.family for tree in CANONICAL_34_TREES.values()}
    assert len(families) == 8
    assert families == {
        TreeFamilyV1.I_FONDAMENTAUX,
        TreeFamilyV1.II_COGNITIFS,
        TreeFamilyV1.III_CONNAISSANCE,
        TreeFamilyV1.IV_RELATIONNELS_SOCIAUX,
        TreeFamilyV1.V_ACTION_TRANSFORMATION,
        TreeFamilyV1.VI_TEMPORELS_MEMORIELS,
        TreeFamilyV1.VII_META_STRUCTURELS,
        TreeFamilyV1.VIII_OBSIDIA_AGI,
    }

    # All trees must have non_decision = True
    for tree_id, tree in CANONICAL_34_TREES.items():
        assert tree.non_decision is True
        assert len(tree.tree_id) == 2
        assert tree.folder.startswith(f"ARBRE_{tree_id}__")


def test_tree_projection_validation():
    # Valid projection
    p = TreeProjectionV1(
        tree_id="03",
        weight=0.85,
        projection_rationale="Visual observation of contour and curvature",
    )
    assert p.tree_name == "Arbre de la Perception"
    assert p.family == TreeFamilyV1.I_FONDAMENTAUX

    # Invalid tree_id
    with pytest.raises(ValueError, match="unknown tree_id"):
        TreeProjectionV1(tree_id="99", weight=0.5, projection_rationale="test")

    # Invalid weights
    with pytest.raises(ValueError, match="weight must be between"):
        TreeProjectionV1(tree_id="01", weight=-0.1, projection_rationale="test")
    with pytest.raises(ValueError, match="weight must be between"):
        TreeProjectionV1(tree_id="01", weight=1.1, projection_rationale="test")

    # Empty rationale
    with pytest.raises(ValueError, match="projection_rationale is required"):
        TreeProjectionV1(tree_id="01", weight=0.5, projection_rationale="  ")


def test_domain_engagement():
    d = DomainEngagementV1(
        domain=SpecializedDomainV1.GEOMETRY,
        proof_criterion="Euclidean metric invariance under 90 degree rotation",
        measurement_units=("px", "rad"),
    )
    assert d.domain == SpecializedDomainV1.GEOMETRY
    assert d.validation_status == "PENDING"

    with pytest.raises(ValueError, match="proof_criterion is required"):
        DomainEngagementV1(domain=SpecializedDomainV1.PHYSICS, proof_criterion="")


def test_timeline_envelope_and_revisions():
    rev1 = HistoricalBeliefRevisionV1(
        revision_id="REV-001",
        t_revision_iso="2026-10-09T14:30:00Z",
        prior_belief_claim="Inverted components are classified as NEAR",
        revised_belief_claim="Inverted components are classified as INVERTED_ORIENTATION (orientation sensitive)",
        contradiction_evidence_ref="sha256:abcd1234exam_inverted_orientation",
        correction_rule_or_procedure="world_orientation_school_v4_2.py:test_adversarial_order",
    )

    timeline = TimelineEnvelopeV1(
        t_event_iso="2026-10-09T10:00:00Z",
        t_observation_iso="2026-10-09T10:00:02Z",
        t_recording_iso="2026-10-09T10:01:00Z",
        educational_stage="BRODY_STAGE_V4_2",
        validity_start_iso="2026-10-09T10:01:00Z",
        revisions=(rev1,),
    )

    assert timeline.t_event_iso != timeline.t_observation_iso
    assert timeline.t_observation_iso != timeline.t_recording_iso
    assert timeline.educational_stage == "BRODY_STAGE_V4_2"
    assert len(timeline.revisions) == 1


def test_multidimensional_experience_creation_and_integrity():
    rev1 = HistoricalBeliefRevisionV1(
        revision_id="REV-001",
        t_revision_iso="2026-10-09T14:30:00Z",
        prior_belief_claim="Circle stroke is formed by single tangent",
        revised_belief_claim="Circle requires closed continuous radial curvature",
        contradiction_evidence_ref="sha256:circlerev001",
        correction_rule_or_procedure="correct_drawing_curvature",
    )

    timeline = TimelineEnvelopeV1(
        t_event_iso="2026-10-08T12:00:00Z",
        t_observation_iso="2026-10-08T12:00:01Z",
        t_recording_iso="2026-10-08T12:00:10Z",
        educational_stage="BRODY_DRAWING_V1",
        validity_start_iso="2026-10-08T12:00:10Z",
        revisions=(rev1,),
    )

    projections = (
        TreeProjectionV1("03", 0.9, "Visual raster perception of curves"),
        TreeProjectionV1("13", 0.7, "Artistic motor gesture rendering"),
        TreeProjectionV1("24", 0.8, "Episodic skill retrieval from drawing school"),
    )

    domains = (
        DomainEngagementV1(
            SpecializedDomainV1.DRAWING,
            "Pixel XOR error strictly decreases per stroke iteration",
            measurement_units=("px_xor",),
        ),
        DomainEngagementV1(
            SpecializedDomainV1.GEOMETRY,
            "Radial symmetry invariant check",
            measurement_units=("px",),
        ),
    )

    calibration = EpistemicCalibrationV1(
        confidence_score=0.88,
        source_provenance_refs=("teacher_images/cours_cercle.png",),
        evidence_hashes=("sha256:cercle_teacher_evidence",),
        uncertainties=("HEURISTIC_THINNING_APPROXIMATION",),
        failure_boundaries=("CANVAS_SIZE=64x64", "NO_OCCLUSION"),
        counter_examples=("cross_exam_negative_transfer",),
        reproducible_on_seed=42,
    )

    exp = MultidimensionalExperienceV1(
        experience_id="EXP-DRAWING-CIRCLE-01",
        intention_summary="Reproduce curved circle stroke under teacher supervision",
        timeline=timeline,
        tree_projections=projections,
        domains=domains,
        calibration=calibration,
        procedure_refs=("brody_world_physique.drawing_school_v1:render",),
    )

    # Check that Brody can retrieve what he believed before revision
    prior = exp.get_belief_prior_to_revision("REV-001")
    assert prior == "Circle stroke is formed by single tangent"
    assert exp.get_belief_prior_to_revision("NON_EXISTENT") is None

    # Check non-sovereignty invariants
    assert exp.readonly is True
    assert exp.decision_authority == DECISION_AUTHORITY
    assert exp.allowed_to_decide is False
    assert exp.allowed_to_act is False
    assert exp.kernel_mutation is False

    # Check digest is stable
    digest = exp.content_digest()
    assert len(digest) == 64
    assert digest == exp.content_digest()


def test_experience_rejects_duplicate_tree_projection():
    timeline = TimelineEnvelopeV1(
        t_event_iso="2026-10-08T12:00:00Z",
        t_observation_iso="2026-10-08T12:00:01Z",
        t_recording_iso="2026-10-08T12:00:10Z",
        educational_stage="STAGE_1",
        validity_start_iso="2026-10-08T12:00:10Z",
    )
    # Projecting to tree 03 twice must be rejected
    projections = (
        TreeProjectionV1("03", 0.5, "First aspect"),
        TreeProjectionV1("03", 0.7, "Duplicate aspect"),
    )
    domains = (DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Invariant check"),)
    calibration = EpistemicCalibrationV1(
        confidence_score=0.8,
        source_provenance_refs=("source",),
        evidence_hashes=("hash",),
        uncertainties=(),
        failure_boundaries=(),
    )

    with pytest.raises(ValueError, match="duplicate tree_id projection"):
        MultidimensionalExperienceV1(
            experience_id="EXP-DUP",
            intention_summary="test",
            timeline=timeline,
            tree_projections=projections,
            domains=domains,
            calibration=calibration,
            procedure_refs=(),
        )


def test_native_memory_admissibility_evaluation():
    timeline = TimelineEnvelopeV1(
        t_event_iso="2026-10-08T12:00:00Z",
        t_observation_iso="2026-10-08T12:00:01Z",
        t_recording_iso="2026-10-08T12:00:10Z",
        educational_stage="STAGE_1",
        validity_start_iso="2026-10-08T12:00:10Z",
    )
    projections = (TreeProjectionV1("05", 0.8, "Identity tracking"),)
    domains = (DomainEngagementV1(SpecializedDomainV1.VIDEO, "Temporal tracking continuity"),)

    # 1. Eligible experience
    calib_good = EpistemicCalibrationV1(
        confidence_score=0.92,
        source_provenance_refs=("video_frame_01.png",),
        evidence_hashes=("sha256:frame01_hash",),
        uncertainties=(),
        failure_boundaries=("CAMERA_STATIONARY",),
    )
    exp_good = MultidimensionalExperienceV1(
        experience_id="EXP-ELIGIBLE",
        intention_summary="Track ball",
        timeline=timeline,
        tree_projections=projections,
        domains=domains,
        calibration=calib_good,
        procedure_refs=(),
    )
    report_good = exp_good.evaluate_native_memory_admissibility()
    assert report_good.is_eligible is True
    assert report_good.candidate_status == "CANDIDATE_ONLY"
    assert report_good.memory_write_allowed is False
    assert report_good.auto_promotion_allowed is False
    assert report_good.decision_authority == "KX108_ONLY"
    assert len(report_good.rejection_flags) == 0

    # 2. Ineligible experience: confidence too low and no provenance
    calib_bad = EpistemicCalibrationV1(
        confidence_score=0.05,
        source_provenance_refs=(),
        evidence_hashes=(),
        uncertainties=("INVENTED_CLAIM_ABOUT_REALITY",),
        failure_boundaries=(),
    )
    exp_bad = MultidimensionalExperienceV1(
        experience_id="EXP-INELIGIBLE",
        intention_summary="Untrusted hallucination",
        timeline=timeline,
        tree_projections=projections,
        domains=domains,
        calibration=calib_bad,
        procedure_refs=(),
    )
    report_bad = exp_bad.evaluate_native_memory_admissibility()
    assert report_bad.is_eligible is False
    assert report_bad.candidate_status == "INELIGIBLE"
    assert "CONFIDENCE_TOO_LOW" in report_bad.rejection_flags
    assert "NO_SOURCE_PROVENANCE" in report_bad.rejection_flags
    assert "NO_CRYPTOGRAPHIC_EVIDENCE" in report_bad.rejection_flags
    assert "INVENTED_CLAIM_DETECTED" in report_bad.rejection_flags


def test_cognitive_memory_index_multidimensional_retrieval():
    index = CognitiveMemoryIndexV1()

    timeline_v1 = TimelineEnvelopeV1(
        t_event_iso="2026-10-08T10:00:00Z",
        t_observation_iso="2026-10-08T10:00:01Z",
        t_recording_iso="2026-10-08T10:01:00Z",
        educational_stage="DESSIN_V1",
        validity_start_iso="2026-10-08T10:01:00Z",
    )
    timeline_v4 = TimelineEnvelopeV1(
        t_event_iso="2026-10-09T10:00:00Z",
        t_observation_iso="2026-10-09T10:00:01Z",
        t_recording_iso="2026-10-09T10:01:00Z",
        educational_stage="ORIENTATION_V4_2",
        validity_start_iso="2026-10-09T10:01:00Z",
    )

    exp1 = MultidimensionalExperienceV1(
        experience_id="EXP-01",
        intention_summary="Drawing curve",
        timeline=timeline_v1,
        tree_projections=(
            TreeProjectionV1("03", 0.9, "Perception"),
            TreeProjectionV1("13", 0.6, "Art"),
        ),
        domains=(DomainEngagementV1(SpecializedDomainV1.DRAWING, "XOR delta"),),
        calibration=EpistemicCalibrationV1(
            confidence_score=0.8,
            source_provenance_refs=("src1",),
            evidence_hashes=("h1",),
            uncertainties=(),
            failure_boundaries=(),
            counter_examples=("cross_bad_recall",),
        ),
        procedure_refs=("proc1",),
    )

    exp2 = MultidimensionalExperienceV1(
        experience_id="EXP-02",
        intention_summary="Orientation reciprocity test",
        timeline=timeline_v4,
        tree_projections=(
            TreeProjectionV1("03", 0.7, "Perception"),
            TreeProjectionV1("22", 0.85, "Transformation"),
        ),
        domains=(
            DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Direction vector"),
            DomainEngagementV1(SpecializedDomainV1.PHYSICS, "Spatial frame"),
        ),
        calibration=EpistemicCalibrationV1(
            confidence_score=0.9,
            source_provenance_refs=("src2",),
            evidence_hashes=("h2",),
            uncertainties=(),
            failure_boundaries=(),
            counter_examples=("inverted_order_false_positive",),
        ),
        procedure_refs=("proc2",),
    )

    index.register_experience(exp1)
    index.register_experience(exp2)

    assert index.count() == 2

    # Query by tree
    p_exp = index.query_by_tree("03")
    assert len(p_exp) == 2
    art_exp = index.query_by_tree("13")
    assert len(art_exp) == 1
    assert art_exp[0].experience_id == "EXP-01"

    # Query by family
    action_fam = index.query_by_family(TreeFamilyV1.V_ACTION_TRANSFORMATION)
    assert len(action_fam) == 1
    assert action_fam[0].experience_id == "EXP-02"

    # Query by domain
    physics_exp = index.query_by_domain(SpecializedDomainV1.PHYSICS)
    assert len(physics_exp) == 1
    assert physics_exp[0].experience_id == "EXP-02"
    drawing_exp = index.query_by_domain(SpecializedDomainV1.DRAWING)
    assert len(drawing_exp) == 1
    assert drawing_exp[0].experience_id == "EXP-01"

    # Query by educational stage
    v4_stage = index.query_by_educational_stage("ORIENTATION_V4_2")
    assert len(v4_stage) == 1
    assert v4_stage[0].experience_id == "EXP-02"

    # Query counter-examples
    counter_examples = index.query_counter_examples()
    assert len(counter_examples) == 2
    assert counter_examples[0] == ("EXP-01", ("cross_bad_recall",))
    assert counter_examples[1] == ("EXP-02", ("inverted_order_false_positive",))
