"""Comprehensive tests for Vague 3:
- G03: Multi-object composer (proportions & relations).
- G04: Visual re-perceiver, error localizer, and correction proposer.
- O02: Deterministic plan replayer with cryptographic integrity check.
- E03: Composition curriculum school with precommitment and heldout exams.
"""

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from PIL import Image, ImageDraw

from brody_world_physique.bounded_orchestrator_v1 import (
    BoundedInstrumentOrchestratorV1,
    OrchestrationPlanV1,
    ToolExecutionStepV1,
)
from brody_world_physique.composition_curriculum_school_e03 import (
    run_school as run_school_e03,
    verify_school as verify_school_e03,
)
from brody_world_physique.deterministic_plan_replay_v1 import (
    DeterministicPlanReplayerV1,
    PlanReplayIntegrityError,
    ReplayVerificationReceiptV1,
)
from brody_world_physique.drawing_school_v0 import black_pixels
from brody_world_physique.multi_object_composer_v1 import (
    ComposedSceneArtifactV1,
    MultiObjectComposerV1,
    ObjectComponentV1,
    SceneCompositionSpecV1,
    SpatialRelationConstraintV1,
)
from brody_world_physique.visual_intent_contracts_v1 import (
    ConstraintKindV1,
    RegionConstraintV1,
    RigorProfileV1,
    VisualEditIntentCandidateV1,
)
from brody_world_physique.visual_reperceiver_evaluator_v1 import (
    ErrorPatchV1,
    ReperceptionEvaluationReportV1,
    VisualReperceiverEvaluatorV1,
)


class TestG03MultiObjectComposer:
    """Validation of G03 Multi-Object Composition."""

    def test_composition_preserves_aspect_ratio_and_relations(self):
        composer = MultiObjectComposerV1()

        # Component 1: Square box (aspect ratio 1.0)
        img_box = Image.new("L", (64, 64), 255)
        ImageDraw.Draw(img_box).rectangle([20, 20, 44, 44], outline=0, width=3)
        comp_box = ObjectComponentV1.from_image("BOX", img_box)

        # Component 2: Circle (aspect ratio 1.0)
        img_circle = Image.new("L", (64, 64), 255)
        ImageDraw.Draw(img_circle).ellipse([20, 20, 44, 44], outline=0, width=3)
        comp_circle = ObjectComponentV1.from_image("CIRCLE", img_circle)

        spec = SceneCompositionSpecV1(
            spec_id="SPEC-NEAR-HORIZONTAL",
            canvas_dimensions=(64, 64),
            components=(comp_box, comp_circle),
            target_placements={
                "BOX": (8, 20, 28, 40),
                "CIRCLE": (36, 20, 56, 40),
            },
            spatial_relations=(
                SpatialRelationConstraintV1("BOX", "CIRCLE", "NEAR"),
                SpatialRelationConstraintV1("BOX", "CIRCLE", "LEFT"),
            ),
            preserve_aspect_ratio=True,
        )

        artifact = composer.compose_scene(spec)
        assert artifact.proportions_preserved is True
        assert "BOX_NEAR_CIRCLE" in artifact.relations_satisfied
        assert "BOX_LEFT_CIRCLE" in artifact.relations_satisfied
        assert len(artifact.relations_violated) == 0

        # Verify image is not blank
        ink = black_pixels(artifact.as_pil_image())
        assert len(ink) > 50


class TestG04VisualReperceiverEvaluator:
    """Validation of G04 Visual Re-perceiver and Error Localizer."""

    def test_detects_lock_violation_and_proposes_erase(self):
        evaluator = VisualReperceiverEvaluatorV1()

        # Canvas with illegal ink drawn inside locked region [0, 0, 20, 20]
        canvas = Image.new("L", (64, 64), 255)
        draw = ImageDraw.Draw(canvas)
        draw.rectangle([5, 5, 12, 12], fill=0)  # intruder ink in locked zone
        draw.line([(30, 30), (50, 50)], fill=0, width=3)  # legal ink outside

        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-GUARD-TOPLEFT",
            goal_description="Protect top-left corner",
            rigor_profile=RigorProfileV1.STRICT_GEOMETRIC,
            region_constraints=(
                RegionConstraintV1("TOP_LEFT", (0, 0, 20, 20), ConstraintKindV1.LOCK),
            ),
        )

        report = evaluator.evaluate_and_locate_errors(canvas, intent)
        assert report.requires_correction is True
        assert len(report.error_patches) >= 1

        lock_patch = report.error_patches[0]
        assert lock_patch.error_kind == "UNWANTED_INK_IN_LOCK_ZONE"
        assert lock_patch.suggested_action == "ERASE_REGION"
        assert lock_patch.bbox_xyxy[0] >= 5 and lock_patch.bbox_xyxy[2] <= 13
        assert len(report.suggested_correction_steps) >= 1
        assert report.suggested_correction_steps[0]["capability"] == "ERASE_REGION"


class TestO02DeterministicPlanReplayer:
    """Validation of O02 Deterministic Plan Replay."""

    def test_replay_passes_when_untampered(self):
        orchestrator = BoundedInstrumentOrchestratorV1()
        plan = OrchestrationPlanV1(
            plan_id="PLAN-VERIFY-01",
            steps=(
                ToolExecutionStepV1(0, "INSPECT_PIXELS"),
                ToolExecutionStepV1(1, "DRAW_STROKE", {
                    "points": [(10, 10), (30, 30)],
                    "kind": "STRAIGHT_STROKE",
                    "width": 3,
                }),
                ToolExecutionStepV1(2, "INSPECT_PIXELS"),
            ),
        )
        original_receipt = orchestrator.execute_plan(plan)
        assert original_receipt.successful_steps == 3

        replayer = DeterministicPlanReplayerV1()
        verify_receipt = replayer.replay_and_verify(original_receipt, plan)

        assert verify_receipt.status == "REPLAY_PASS"
        assert verify_receipt.step_hashes_verified is True
        assert verify_receipt.final_canvas_verified is True
        assert verify_receipt.steps_verified_count == 3

    def test_replay_fails_on_divergence(self):
        orchestrator = BoundedInstrumentOrchestratorV1()
        plan = OrchestrationPlanV1(
            plan_id="PLAN-DIVERGE",
            steps=(
                ToolExecutionStepV1(0, "DRAW_STROKE", {
                    "points": [(10, 10), (30, 30)],
                    "kind": "STRAIGHT_STROKE",
                }),
            ),
        )
        original_receipt = orchestrator.execute_plan(plan)

        # Plan with altered points
        altered_plan = OrchestrationPlanV1(
            plan_id="PLAN-DIVERGE",
            steps=(
                ToolExecutionStepV1(0, "DRAW_STROKE", {
                    "points": [(15, 15), (40, 40)],
                    "kind": "STRAIGHT_STROKE",
                }),
            ),
        )

        replayer = DeterministicPlanReplayerV1()
        with pytest.raises(PlanReplayIntegrityError, match="canvas SHA mismatch"):
            replayer.replay_and_verify(original_receipt, altered_plan)


class TestE03CompositionCurriculumSchool:
    """Validation of E03 Composition Curriculum School."""

    def test_full_curriculum_run_and_verification(self):
        with TemporaryDirectory() as tmp_dir:
            out_path = Path(tmp_dir) / "e03_school_run"

            run_result = run_school_e03(out_path, training_lessons=3)
            assert run_result["status"] == "PASS_COMPOSITION_CURRICULUM_E03"
            assert run_result["lessons"] == 3
            assert run_result["exams"] == 3

            # Verify integrity
            verified = verify_school_e03(out_path)
            assert verified["status"] == "VERIFIED_COMPOSITION_E03"
            assert verified["lessons_verified"] == 3
            assert verified["exams_verified"] == 3
            assert verified["native_memory_write_allowed"] is False
            assert verified["decision_authority"] == "KX108_ONLY"
