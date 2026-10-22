"""Tests for Vague 5: Progressive Visual Curriculum (E05), Programmatic Orchestration (O04), SVG, and Negative Transfer."""
from __future__ import annotations

import json
from pathlib import Path
import pytest
from PIL import Image

from brody_world_physique.progressive_visual_curriculum_e05 import (
    SVGVisualPlanV1,
    ShadedVisualObjectV1,
    convert_object_to_svg_plan,
    create_lamp_object,
    create_mug_object,
    create_teapot_object,
    create_vase_object,
    render_shaded_object,
)
from brody_world_physique.programmatic_orchestrator_o04 import (
    ProgrammaticBoundedOrchestratorO04,
    WorkflowInstructionV1,
    WorkflowPredicateV1,
)
from brody_world_physique.heterogeneous_orchestrator_o03 import HeterogeneousStepV1
from brody_world_physique.negative_transfer_detector_v1 import (
    NegativeTransferDetectorV1,
    NegativeTransferDiagnosticV1,
)
from brody_world_physique.cognitive_memory_timeline_v1 import (
    CANONICAL_34_TREES,
    DomainEngagementV1,
    EpistemicCalibrationV1,
    MultidimensionalExperienceV1,
    MultiSessionMemoryJournalV1,
    SpecializedDomainV1,
    TimelineEnvelopeV1,
    TreeProjectionV1,
)
from brody_world_physique.multidimensional_retrieval_v2 import (
    VisualTaskAdmissibilityRequestV1,
)
from brody_world_physique.drawing_school_v0 import black_pixels


def test_progressive_curriculum_complex_objects_and_svg() -> None:
    # 1. Create complex objects with shading
    mug = create_mug_object()
    vase = create_vase_object()
    lamp = create_lamp_object()
    teapot = create_teapot_object()

    # Check epistemic boundary on unobserved surfaces
    assert "BACK_FACING_SURFACE" in mug.unobserved_surfaces
    assert mug.epistemic_surface_status == "UNKNOWN_FOR_OCCLUDED_FACES"
    assert "INTERIOR_BOTTOM" in teapot.unobserved_surfaces

    # 2. Render each object to PIL image
    img_mug = render_shaded_object(mug)
    img_vase = render_shaded_object(vase)
    img_lamp = render_shaded_object(lamp)
    img_teapot = render_shaded_object(teapot)

    assert len(black_pixels(img_mug)) > 100
    assert len(black_pixels(img_vase)) > 80
    assert len(black_pixels(img_lamp)) > 50
    assert len(black_pixels(img_teapot)) > 120

    # 3. SVG vector plan generation
    svg_plan_mug = convert_object_to_svg_plan(mug)
    svg_xml = svg_plan_mug.to_svg_xml()
    assert "<svg" in svg_xml
    assert "</svg>" in svg_xml
    assert "Brody World Physique Image Bounded SVG Export" in svg_xml

    # 4. Rasterization of SVG plan
    rasterized_svg = svg_plan_mug.render_to_pil()
    assert rasterized_svg.size == (64, 64)
    assert len(black_pixels(rasterized_svg)) > 50


def test_programmatic_orchestrator_conditional_workflow() -> None:
    orchestrator = ProgrammaticBoundedOrchestratorO04(
        max_cost_budget=50.0,
        max_total_steps=20,
    )

    instructions = [
        # 1. Initial geometric stamp (box)
        WorkflowInstructionV1(
            instruction_id="inst_stamp",
            action_type="CALL_TOOL",
            tool_step=HeterogeneousStepV1(
                step_index=0,
                capability="GEOMETRIC_STAMP",
                arguments={"shape": "BOX", "bbox": [10, 10, 40, 40]},
                tool_name="GEOMETRIC_STAMP",
            ),
        ),
        # 2. Checkpoint canvas
        WorkflowInstructionV1(
            instruction_id="inst_cp",
            action_type="CHECKPOINT",
            checkpoint_name="cp_box",
        ),
        # 3. Conditional branch: if black_pixels_count > 50, draw an interior stroke
        WorkflowInstructionV1(
            instruction_id="inst_branch",
            action_type="BRANCH_IF",
            predicate=WorkflowPredicateV1(
                variable_name="black_pixels_count",
                operator=">",
                threshold=50,
            ),
            then_instructions=(
                WorkflowInstructionV1(
                    instruction_id="inst_draw_cross",
                    action_type="CALL_TOOL",
                    tool_step=HeterogeneousStepV1(
                        step_index=1,
                        capability="DRAW_STROKE",
                        arguments={"points": [(15, 25), (35, 25)], "width": 2},
                        tool_name="PEN",
                    ),
                ),
            ),
        ),
    ]

    receipt = orchestrator.execute_workflow("workflow_conditional_01", instructions)

    assert receipt.workflow_id == "workflow_conditional_01"
    assert receipt.branches_taken == 1
    assert receipt.total_tool_steps_executed == 2
    assert receipt.budget_exhausted is False
    assert receipt.total_cost_incurred > 0
    assert "black_pixels_count" in receipt.final_state_summary


def test_negative_transfer_and_contradiction_detection() -> None:
    detector = NegativeTransferDetectorV1()

    timeline = TimelineEnvelopeV1(
        t_event_iso="2026-10-22T10:00:00Z",
        t_observation_iso="2026-10-22T10:00:01Z",
        t_recording_iso="2026-10-22T10:01:00Z",
        educational_stage="TEST_STAGE",
        validity_start_iso="2026-10-22T10:00:00Z",
    )
    tree_proj = TreeProjectionV1("03", 0.90, "Form perception projection")
    domain_eng = DomainEngagementV1(
        domain=SpecializedDomainV1.DRAWING,
        proof_criterion="Raster XOR error minimization",
    )
    calibration = EpistemicCalibrationV1(
        confidence_score=0.85,
        source_provenance_refs=("ref_test",),
        evidence_hashes=("sha_test",),
        uncertainties=(),
        failure_boundaries=("CANVAS_SIZE=64x64",),
        counter_examples=("Complex 3D non-planar projections", "Heavy Stippling Over-budget"),
        reproducible_on_seed=101,
    )

    exp = MultidimensionalExperienceV1(
        experience_id="exp_with_counter_examples",
        intention_summary="Test experience with known boundaries and counter examples",
        timeline=timeline,
        tree_projections=(tree_proj,),
        domains=(domain_eng,),
        calibration=calibration,
        procedure_refs=("test_procedure",),
        storage_provenance="HISTORICAL_PERSISTED",
    )

    # 1. Collision with counter-example
    colliding_req = VisualTaskAdmissibilityRequestV1(
        task_id="task_colliding",
        target_domain=SpecializedDomainV1.DRAWING,
        required_invariants=("Complex 3D non-planar projections",),
        canvas_dimensions=(64, 64),
    )
    diag_collision = detector.evaluate_skill_transfer(exp, colliding_req)
    assert diag_collision.is_safe_to_apply is False
    assert diag_collision.transfer_risk_level == "HIGH_RISK_REJECTED"
    assert len(diag_collision.colliding_counter_examples) > 0

    # 2. Domain mismatch
    domain_mismatch_req = VisualTaskAdmissibilityRequestV1(
        task_id="task_mismatch",
        target_domain=SpecializedDomainV1.PHYSICS,
        required_invariants=("Newtonian velocity conservation",),
        canvas_dimensions=(64, 64),
    )
    diag_domain = detector.evaluate_skill_transfer(exp, domain_mismatch_req)
    assert diag_domain.is_safe_to_apply is False
    assert "DOMAIN_MISMATCH" in diag_domain.rejection_reasons[0]

    # 3. Canvas size failure boundary
    canvas_boundary_req = VisualTaskAdmissibilityRequestV1(
        task_id="task_bad_canvas",
        target_domain=SpecializedDomainV1.DRAWING,
        required_invariants=(),
        canvas_dimensions=(128, 128),
    )
    diag_canvas = detector.evaluate_skill_transfer(exp, canvas_boundary_req)
    assert diag_canvas.is_safe_to_apply is False
    assert any("BOUNDARY_VIOLATION" in r for r in diag_canvas.rejection_reasons)

    # 4. Clean safe transfer
    safe_req = VisualTaskAdmissibilityRequestV1(
        task_id="task_safe",
        target_domain=SpecializedDomainV1.DRAWING,
        required_invariants=(),
        canvas_dimensions=(64, 64),
    )
    diag_safe = detector.evaluate_skill_transfer(exp, safe_req)
    assert diag_safe.is_safe_to_apply is True
    assert diag_safe.transfer_risk_level == "NONE"


def test_memory_boundary_sessions_jsonl_does_not_promote_candidates_to_canon(tmp_path: Path) -> None:
    """Verifies that writing to sessions.jsonl is purely local/audit and cannot promote to canon."""
    journal = MultiSessionMemoryJournalV1(root_dir=tmp_path)

    canon_keys_before = set(CANONICAL_34_TREES.keys())

    # Record a session with candidate IDs
    entry = journal.record_session(
        session_id="session_candidate_test",
        started_at_iso="2026-10-22T10:00:00Z",
        closed_at_iso="2026-10-22T10:05:00Z",
        experience_ids=["exp_candidate_01", "exp_candidate_02"],
        relation_count=2,
        metadata={"status": "CANDIDATE_ONLY"},
    )

    # Invariants verification
    assert entry["decision_authority"] == "KX108_ONLY"
    assert entry["native_memory_write_allowed"] is False

    # Canon must remain completely unchanged
    canon_keys_after = set(CANONICAL_34_TREES.keys())
    assert canon_keys_before == canon_keys_after

    # Journal on disk contains the audit record without altering canon
    journal_file = tmp_path / "sessions.jsonl"
    assert journal_file.is_file()
    lines = journal_file.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    stored_entry = json.loads(lines[0])
    assert stored_entry["session_id"] == "session_candidate_test"
    assert stored_entry["native_memory_write_allowed"] is False
