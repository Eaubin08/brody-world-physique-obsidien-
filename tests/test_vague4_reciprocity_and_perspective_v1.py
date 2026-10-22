"""Tests for Vague 4:
- V03/V04: Multi-perspective vantage transformation, discrete rotations, object permanence, and non-3D boundary.
- E04: Perspective multi-angle curriculum school with sealed precommitments.
- R01/R02: Reciprocal loop (World -> Representation -> Generation -> Re-perception -> Discrepancy).
- O03: Heterogeneous instrument orchestrator with compute costs, budgets, and localized correction.
- G02 Workstation configuration: Neural vs procedural distinction.
"""

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from PIL import Image, ImageDraw

from brody_world_physique.diffusion_generator_adapter_v1 import (
    DiffusionGeneratorAdapterV1,
    WorkstationNeuralConfigV1,
)
from brody_world_physique.drawing_school_v0 import black_pixels
from brody_world_physique.heterogeneous_orchestrator_o03 import (
    HeterogeneousInstrumentOrchestratorO03,
    HeterogeneousStepV1,
)
from brody_world_physique.multi_perspective_view_v03_v04 import (
    MultiPerspectiveTransformerV03V04,
    ObjectPermanenceRecordV04,
    VantageTransform2DV03,
)
from brody_world_physique.perspective_curriculum_school_e04 import (
    run_school as run_school_e04,
    verify_school as verify_school_e04,
)
from brody_world_physique.reciprocal_world_loop_v1 import (
    ReciprocalReconciliationReceiptV1,
    ReciprocalWorldReconcilerV1,
)
from brody_world_physique.visual_intent_contracts_v1 import (
    ConstraintKindV1,
    RegionConstraintV1,
    RigorProfileV1,
    VisualEditIntentCandidateV1,
)
from brody_world_physique.visual_reperceiver_evaluator_v1 import (
    ErrorPatchV1,
    VisualReperceiverEvaluatorV1,
)


class TestV03V04MultiPerspective:
    """Validation of V03/V04 vantage transformation and object permanence."""

    def test_discrete_rotations_and_object_permanence(self):
        transformer = MultiPerspectiveTransformerV03V04()

        img = Image.new("L", (64, 64), 255)
        # Asymmetric shape: L-junction
        ImageDraw.Draw(img).line([(32, 16), (32, 48)], fill=0, width=3)
        ImageDraw.Draw(img).line([(32, 32), (48, 32)], fill=0, width=3)

        # 90-degree rotation
        trans90 = VantageTransform2DV03(rotation_degrees=90)
        img90, rec90 = transformer.transform_vantage(img, trans90)

        assert rec90.rotation_degrees == 90
        assert rec90.visible_pixel_count > 0
        assert rec90.shape_invariance_preserved is True
        assert rec90.is_partially_occluded is False
        assert rec90.transformed_sha256 != rec90.source_sha256

        # 180-degree rotation
        trans180 = VantageTransform2DV03(rotation_degrees=180)
        img180, rec180 = transformer.transform_vantage(img, trans180)
        assert rec180.rotation_degrees == 180
        assert rec180.shape_invariance_preserved is True

    def test_rejection_of_false_3d_claims(self):
        with pytest.raises(ValueError, match="3D view synthesis cannot be claimed"):
            VantageTransform2DV03(rotation_degrees=90, is_3d_view_synthesis=True)

    def test_boundary_clipping_detection(self):
        transformer = MultiPerspectiveTransformerV03V04()
        img = Image.new("L", (64, 64), 255)
        ImageDraw.Draw(img).rectangle([2, 2, 20, 20], fill=0)

        # Shift far to the left to cause severe boundary occlusion
        trans_shifted = VantageTransform2DV03(rotation_degrees=0, translation_dx=-40)
        _, rec = transformer.transform_vantage(img, trans_shifted)

        assert rec.is_partially_occluded is True
        assert rec.in_bounds_ratio < 0.98


class TestE04PerspectiveCurriculumSchool:
    """Validation of E04 perspective curriculum school."""

    def test_perspective_school_run_and_verify(self):
        with TemporaryDirectory() as tmp_dir:
            out_path = Path(tmp_dir) / "e04_run"
            result = run_school_e04(out_path, training_lessons=3)

            assert result["status"] == "PASS_PERSPECTIVE_ROTATION_SCHOOL_E04"
            assert result["lessons"] == 3
            assert result["exams"] == 3

            verified = verify_school_e04(out_path)
            assert verified["status"] == "VERIFIED_PERSPECTIVE_ROTATION_E04"
            assert verified["lessons_verified"] == 3
            assert verified["exams_verified"] == 3
            assert verified["decision_authority"] == "KX108_ONLY"


class TestR01R02ReciprocalWorldLoop:
    """Validation of R01/R02 perception <-> generation closed loop."""

    def test_closed_reciprocal_loop_execution(self):
        reconciler = ReciprocalWorldReconcilerV1()

        # World observation: a circle centered in 64x64
        obs_img = Image.new("L", (64, 64), 255)
        ImageDraw.Draw(obs_img).ellipse([18, 18, 46, 46], outline=0, width=3)

        receipt = reconciler.run_reciprocal_loop("LOOP-TEST-01", obs_img)

        assert isinstance(receipt, ReciprocalReconciliationReceiptV1)
        assert receipt.reconstructed_from_representation is True
        assert receipt.decision_authority == "KX108_ONLY"
        assert receipt.native_memory_write_allowed is False

        # Verify discrepancy report
        disc = receipt.discrepancy_report
        assert disc.pixel_iou >= 0.70
        assert disc.bbox_drift_px <= 2.0
        assert "HIGH_PIXEL_COINCIDENCE_IOU_GE_70" in receipt.preserved_invariants
        assert "CENTROID_ALIGNMENT_PRESERVED" in receipt.preserved_invariants


class TestO03HeterogeneousOrchestrator:
    """Validation of O03 Heterogeneous Instrument Orchestrator."""

    def test_heterogeneous_plan_with_cost_and_stamps(self):
        orch = HeterogeneousInstrumentOrchestratorO03(max_cost_budget=20.0)

        steps = [
            HeterogeneousStepV1(0, "INSPECT_PIXELS"),
            HeterogeneousStepV1(1, "SELECT_TOOL", {"tool": "PENCIL"}),
            HeterogeneousStepV1(2, "GEOMETRIC_STAMP", {"shape": "CIRCLE", "bbox": (14, 14, 46, 46)}),
            HeterogeneousStepV1(3, "INSPECT_PIXELS"),
        ]

        receipt = orch.execute_plan("PLAN-STAMP-PENCIL", steps)
        assert receipt.total_steps_executed == 4
        assert receipt.successful_steps == 4
        assert receipt.total_cost_incurred > 0.0
        assert receipt.budget_remaining < 20.0

        # Canvas must contain pixels
        ink = black_pixels(orch.canvas)
        assert len(ink) > 50

    def test_budget_exhaustion_stops_execution(self):
        # Strict low budget: 3.0 units
        orch = HeterogeneousInstrumentOrchestratorO03(max_cost_budget=3.0)

        steps = [
            HeterogeneousStepV1(0, "GEOMETRIC_STAMP", {"shape": "BOX"}),  # costs 3.0
            HeterogeneousStepV1(1, "GEOMETRIC_STAMP", {"shape": "CIRCLE"}),  # would cost +3.0 -> exceeds 3.0
        ]

        receipt = orch.execute_plan("PLAN-OVERBUDGET", steps)
        assert receipt.successful_steps == 1
        assert len(receipt.step_receipts) == 2
        assert receipt.step_receipts[1].status == "BUDGET_EXHAUSTED"

    def test_localized_correction_from_error_patch(self):
        orch = HeterogeneousInstrumentOrchestratorO03()

        # Canvas with illegal ink in top-left
        canvas = Image.new("L", (64, 64), 255)
        ImageDraw.Draw(canvas).rectangle([5, 5, 12, 12], fill=0)
        orch = HeterogeneousInstrumentOrchestratorO03(initial_canvas=canvas)

        patch = ErrorPatchV1(
            patch_id="ERR-TL",
            error_kind="UNWANTED_INK_IN_LOCK_ZONE",
            bbox_xyxy=(5, 5, 12, 12),
            pixel_count=64,
            severity=0.8,
            suggested_action="ERASE_REGION",
            suggested_arguments={"x0": 5, "y0": 5, "x1": 13, "y1": 13},
        )

        step = HeterogeneousInstrumentOrchestratorO03.create_step_from_error_patch(patch, 0)
        receipt = orch.execute_plan("PLAN-CORRECT", [step])

        assert receipt.successful_steps == 1
        # Target area must be erased (clean white)
        cur_ink = black_pixels(orch.canvas)
        assert len(cur_ink) == 0


class TestG02WorkstationNeuralConfiguration:
    """Validation of G02 PC Fixe / Workstation neural configuration."""

    def test_workstation_configuration_standby(self):
        adapter = DiffusionGeneratorAdapterV1()

        config = WorkstationNeuralConfigV1(
            workstation_node_id="NODE-WORKSTATION-FIXE-01",
            target_gpu_model="NVIDIA GeForce RTX 4090",
            dedicated_vram_gb=24.0,
            local_weights_present=True,
            local_weights_dir="/models/diffusion_verified",
        )

        status = adapter.configure_workstation_neural_environment(config)
        assert status["status"] == "WORKSTATION_NEURAL_STANDBY"
        assert status["vram_gb"] == 24.0
        assert status["hold_active"] is False
