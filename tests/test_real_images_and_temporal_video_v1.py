"""Comprehensive tests for Real Image Pipeline Audit, Temporal Video Tracking, and Organic Recovery.

Covers User Axes A, B, C, D:
A. Real Image Pipeline Audit & MMonde canonical contract compatibility.
B. Multi-Photo evaluation across all 6 curriculum levels (Perception, Reconstruction, Retention, Transfer, Correction).
C. Both Organic Branching Exam Recovery (original failed exam + new fractal tree).
D. Temporal Video Cognitive Engine:
   - Disambiguation: OBJECT_MOTION, CAMERA_MOTION, OCCLUSION, APPEARANCE_CHANGE, UNKNOWN.
   - Preverbal forecast emitted before held-out frame reveal.
   - Confrontation receipt with spatial error and UNKNOWN preservation.
E. Workstation Bridge Runner, Generation Modes Separation & Tool Selector from memory.
F. Multi-session reboot persistence preserving revisions & contradictions.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from PIL import Image, ImageDraw

from brody_world_physique.contracts_v0 import (
    DECISION_AUTHORITY,
    ExperienceValidationStatusV0,
    MemoryEligibilityV0,
    WorldExperienceCandidateV0,
)
from brody_world_physique.diffusion_generator_adapter_v1 import (
    DesktopWorkstationBridgeRunnerV1,
    DesktopWorkstationDiffusionStubV1,
    GenerationModalityV1,
    ToolSelectorFromIntentAndMemoryV1,
    WorkstationNeuralConfigV1,
)
from brody_world_physique.f16_real_image_contracts_v1 import (
    RealImageObservationF16V1,
    RealImagePipelineAuditReceiptV1,
    audit_real_image_pipeline,
    ingest_real_image_f16,
    measure_image_pixels,
)
from brody_world_physique.independent_ablation_and_organic_learning_v1 import (
    OrganicFailureAnalysisAndRecoveryV1,
)
from brody_world_physique.multi_session_retention_v1 import (
    MultiSessionRetentionHarnessV1,
)
from brody_world_physique.natural_image_curriculum_and_loop_v1 import (
    NaturalCurriculumMultiMetricEvaluatorV1,
    NaturalImageLoopExecutorV1,
    NaturalVisualConceptLevelV1,
)
from brody_world_physique.temporal_video_learning_v1 import (
    MotionAttributionV1,
    TemporalConfrontationReceiptV1,
    TemporalFrameObservationV1,
    TemporalVideoCognitiveEngineV1,
)
from brody_world_physique.visual_intent_contracts_v1 import (
    ConstraintKindV1,
    RegionConstraintV1,
    RigorProfileV1,
    VisualEditIntentCandidateV1,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "real_images"
TRAIN_PHOTO = FIXTURES_DIR / "camera_capture_1000001068.jpg"
EXAM_PHOTO_SEDAN = FIXTURES_DIR / "exam_real_photo_outdoor_sedan.jpg"
EXAM_PHOTO_LOGO = FIXTURES_DIR / "exam_real_graphic_badge_logo.png"


class TestRealImagePipelineAuditAndMMondeCanonical(unittest.TestCase):
    """Section A: Validates exact pipeline path from camera photo to reconstruction and canonical contract."""

    def test_real_image_pipeline_audit_path(self):
        self.assertTrue(TRAIN_PHOTO.exists())
        with TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "pipeline_audit"
            receipt = audit_real_image_pipeline(TRAIN_PHOTO, output_dir=out_dir)

            self.assertIsInstance(receipt, RealImagePipelineAuditReceiptV1)
            self.assertEqual(receipt.source_sha256, "31defdd9a42efa6e7860565fc1c413f5d04ee4582e3095dc7a9b5c359df33411")
            self.assertGreater(receipt.measured_luminance, 0.0)
            self.assertGreater(receipt.measured_edge_density, 0.0)
            self.assertEqual(receipt.decision_authority, "KX108_ONLY")

            # Check that reconstruction achieved positive fidelity on complex real photo
            self.assertGreater(receipt.reconstruction_final_iou, 0.20)
            self.assertLess(receipt.cost_spent, 35.0)

            # Check that artifacts were written and verified
            self.assertTrue(Path(receipt.saved_artifact_paths["raw_input"]).exists())
            self.assertTrue(Path(receipt.saved_artifact_paths["sobel_edges"]).exists())
            self.assertTrue(Path(receipt.saved_artifact_paths["reconstruction"]).exists())
            self.assertTrue(Path(receipt.saved_artifact_paths["diff_mask"]).exists())

            # Check canonical MMonde compatibility
            f16_obs = ingest_real_image_f16(TRAIN_PHOTO)
            canonical = f16_obs.to_canonical_world_experience_candidate()
            self.assertIsInstance(canonical, WorldExperienceCandidateV0)
            self.assertEqual(canonical.decision_authority, "KX108_ONLY")
            self.assertEqual(canonical.validation_status, ExperienceValidationStatusV0.CANDIDATE)
            self.assertEqual(canonical.memory_eligibility, MemoryEligibilityV0.CANDIDATE_ONLY)
            self.assertFalse(canonical.canonical_memory)
            self.assertFalse(canonical.memory_write_allowed)


class TestMultiPhotoEvaluationAndCurriculumSixLevels(unittest.TestCase):
    """Sections A & B: Multi-photo evaluation across all 6 levels with separate metrics."""

    def test_multi_photo_distinct_provenance_and_six_levels(self):
        self.assertTrue(EXAM_PHOTO_SEDAN.exists())
        self.assertTrue(EXAM_PHOTO_LOGO.exists())

        f16_train = ingest_real_image_f16(TRAIN_PHOTO)
        f16_sedan = ingest_real_image_f16(EXAM_PHOTO_SEDAN)
        f16_logo = ingest_real_image_f16(EXAM_PHOTO_LOGO)

        # Strict separation of training vs exam image hashes
        self.assertNotEqual(f16_train.provenance.source_sha256, f16_sedan.provenance.source_sha256)
        self.assertNotEqual(f16_train.provenance.source_sha256, f16_logo.provenance.source_sha256)
        self.assertNotEqual(f16_sedan.provenance.source_sha256, f16_logo.provenance.source_sha256)

        evaluator = NaturalCurriculumMultiMetricEvaluatorV1()

        # Evaluate Sedan outdoor exam photo
        sedan_metrics = evaluator.evaluate_curriculum_on_image(f16_sedan)
        self.assertEqual(len(sedan_metrics), 6)

        for lvl, record in sedan_metrics.items():
            self.assertIsInstance(lvl, NaturalVisualConceptLevelV1)
            # 1. Perception
            self.assertGreater(record.perception_edge_density, 0.0)
            self.assertGreater(record.perception_contrast_ratio, 0.0)
            # 2. Reconstruction
            self.assertGreater(record.reconstruction_initial_iou, 0.0)
            # 3. Retention
            self.assertIn("EXP-NAT-SILHOUETTE-BOUNDARY", record.retention_grounded_lessons)
            # 4. Transfer
            self.assertIn(record.transfer_status, ("TRANSFER_VERIFIED", "MODERATE_TRANSFER"))
            # 5. Correction
            self.assertGreaterEqual(record.correction_error_reduction, 0)
            self.assertGreater(record.final_iou, 0.20)


class TestBothOrganicBranchingExamRecovery(unittest.TestCase):
    """Section B Point 8: Repasser l'ancien examen organique après apprentissage en plus du nouveau."""

    def test_both_organic_exams_recovery_proof(self):
        recovery = OrganicFailureAnalysisAndRecoveryV1()
        with TemporaryDirectory() as tmp_dir:
            receipt = recovery.evaluate_before_and_after_organic_learning(output_dir=tmp_dir)

            # 1. Initial historical failure is faithfully traced
            trace = receipt["historical_failure_trace"]
            self.assertEqual(trace["initial_exam_id"], "EXAM_ORGANIC_ASYMMETRIC_BRANCHING")
            self.assertEqual(trace["initial_iou"], 0.1647)
            self.assertEqual(trace["initial_status"], "OUT_OF_BOUNDS_REJECTION")

            # 2. Novel exam recovery (EXAM_NOVEL_FRACTAL_BRANCHING_TREE)
            self.assertEqual(receipt["novel_exam_id"], "EXAM_NOVEL_FRACTAL_BRANCHING_TREE")
            self.assertGreater(receipt["after_learning"]["final_iou"], 0.75)
            self.assertEqual(receipt["after_learning"]["status"], "HIGH_FIDELITY_TRANSFER")

            # 3. Original historical exam recovery (EXAM_ORGANIC_ASYMMETRIC_BRANCHING)
            orig_rec = receipt["original_failed_exam_recovery"]
            self.assertEqual(orig_rec["exam_id"], "EXAM_ORGANIC_ASYMMETRIC_BRANCHING")
            self.assertEqual(orig_rec["historical_failed_iou"], 0.1647)
            self.assertGreater(orig_rec["post_learning_recovered_iou"], 0.65)
            self.assertTrue(orig_rec["competence_progressed"])
            self.assertGreater(orig_rec["delta_iou_improvement"], 0.45)


class TestTemporalVideoTrackingAndPreverbalConfrontation(unittest.TestCase):
    """Section C: Video temporal frames, disambiguation, preverbal forecast and UNKNOWN handling."""

    def _create_frame(
        self,
        target_xy: tuple[int, int] | None = (32, 32),
        anchor_xy: tuple[int, int] = (8, 8),
        target_radius: int = 4,
    ) -> Image.Image:
        img = Image.new("L", (64, 64), 180)  # Neutral background
        draw = ImageDraw.Draw(img)
        # Static fiducial anchor (bright square in top-left)
        ax, ay = anchor_xy
        draw.rectangle([ax - 3, ay - 3, ax + 3, ay + 3], fill=245)
        # Foreground moving target (dark circle)
        if target_xy is not None:
            tx, ty = target_xy
            draw.ellipse([tx - target_radius, ty - target_radius, tx + target_radius, ty + target_radius], fill=30)
        return img

    def test_temporal_tracking_and_preverbal_forecast(self):
        engine = TemporalVideoCognitiveEngineV1()

        # Feed 3 sequential frames with steady object motion
        # Frame 0: (20, 20), Frame 1: (24, 23), Frame 2: (28, 26)
        f0 = self._create_frame(target_xy=(20, 20), anchor_xy=(8, 8))
        f1 = self._create_frame(target_xy=(24, 23), anchor_xy=(8, 8))
        f2 = self._create_frame(target_xy=(28, 26), anchor_xy=(8, 8))

        obs0 = engine.ingest_frame(f0, frame_index=0, timestamp_s=0.0, source_sha256="a" * 64)
        obs1 = engine.ingest_frame(f1, frame_index=1, timestamp_s=0.1, source_sha256="a" * 64)
        obs2 = engine.ingest_frame(f2, frame_index=2, timestamp_s=0.2, source_sha256="a" * 64)

        self.assertEqual(obs1.attribution, MotionAttributionV1.OBJECT_MOTION)
        self.assertEqual(obs2.attribution, MotionAttributionV1.OBJECT_MOTION)

        # Precommit forecast for Frame 3 BEFORE decoding Frame 3
        forecast = engine.emit_preverbal_forecast(target_frame_index=3, target_timestamp_s=0.3)
        self.assertTrue(forecast.precommitted_before_frame_decode)
        self.assertAlmostEqual(forecast.forecast_xy[0], 32.0, delta=1.5)
        self.assertAlmostEqual(forecast.forecast_xy[1], 29.0, delta=1.5)

        # Now decode held-out Frame 3: actual position is (32, 29)
        f3 = self._create_frame(target_xy=(32, 29), anchor_xy=(8, 8))
        obs3 = engine.ingest_frame(f3, frame_index=3, timestamp_s=0.3, source_sha256="a" * 64)

        # Confrontation
        receipt = engine.confront_and_evaluate(forecast, obs3)
        self.assertEqual(receipt.status, "CONFRONTATION_SUCCESS")
        self.assertLess(receipt.spatial_error_px, 2.0)
        self.assertEqual(receipt.attribution, MotionAttributionV1.OBJECT_MOTION)
        self.assertIsNotNone(receipt.candidate_experience)

    def test_camera_motion_disambiguation_holds_prediction(self):
        engine = TemporalVideoCognitiveEngineV1()
        f0 = self._create_frame(target_xy=(20, 20), anchor_xy=(8, 8))
        f1 = self._create_frame(target_xy=(24, 23), anchor_xy=(8, 8))
        f2 = self._create_frame(target_xy=(28, 26), anchor_xy=(8, 8))

        engine.ingest_frame(f0, 0, 0.0, "b" * 64)
        engine.ingest_frame(f1, 1, 0.1, "b" * 64)
        engine.ingest_frame(f2, 2, 0.2, "b" * 64)
        forecast = engine.emit_preverbal_forecast(3, 0.3)

        # Held-out Frame 3 has CAMERA PAN: anchor moved from (8, 8) to (14, 8)
        f3_cam = self._create_frame(target_xy=(38, 29), anchor_xy=(14, 8))
        obs3_cam = engine.ingest_frame(f3_cam, 3, 0.3, "b" * 64)

        self.assertEqual(obs3_cam.attribution, MotionAttributionV1.CAMERA_MOTION)
        receipt = engine.confront_and_evaluate(forecast, obs3_cam)
        self.assertEqual(receipt.status, "HOLD_CAMERA_MOTION")
        self.assertEqual(receipt.attribution, MotionAttributionV1.CAMERA_MOTION)

    def test_occlusion_disambiguation_holds_prediction(self):
        engine = TemporalVideoCognitiveEngineV1()
        f0 = self._create_frame(target_xy=(20, 20), anchor_xy=(8, 8))
        f1 = self._create_frame(target_xy=(24, 23), anchor_xy=(8, 8))
        f2 = self._create_frame(target_xy=(28, 26), anchor_xy=(8, 8))

        engine.ingest_frame(f0, 0, 0.0, "c" * 64)
        engine.ingest_frame(f1, 1, 0.1, "c" * 64)
        engine.ingest_frame(f2, 2, 0.2, "c" * 64)
        forecast = engine.emit_preverbal_forecast(3, 0.3)

        # Held-out Frame 3 has OCCLUSION: target is behind obstacle (target_xy=None)
        f3_occ = self._create_frame(target_xy=None, anchor_xy=(8, 8))
        obs3_occ = engine.ingest_frame(f3_occ, 3, 0.3, "c" * 64)

        self.assertEqual(obs3_occ.attribution, MotionAttributionV1.OCCLUSION)
        receipt = engine.confront_and_evaluate(forecast, obs3_occ)
        self.assertEqual(receipt.status, "HOLD_OCCLUSION")
        self.assertIsNone(receipt.actual_xy)


class TestWorkstationBridgeRunnerAndToolSelection(unittest.TestCase):
    """Section D: Generation modes separation, workstation bridge runner and grounded tool selection."""

    def test_generation_modality_separation(self):
        self.assertEqual(GenerationModalityV1.PROCEDURAL_VISUAL_GENERATION.value, "PROCEDURAL_VISUAL_GENERATION")
        self.assertEqual(GenerationModalityV1.NEURAL_IMAGE_GENERATION.value, "NEURAL_IMAGE_GENERATION")
        self.assertEqual(GenerationModalityV1.PROGRAMMATIC_TOOL_ORCHESTRATION.value, "PROGRAMMATIC_TOOL_ORCHESTRATION")

    def test_desktop_workstation_bridge_runner(self):
        runner = DesktopWorkstationBridgeRunnerV1()
        valid_cfg = WorkstationNeuralConfigV1(
            workstation_node_id="NODE-TITAN-FIXE",
            target_gpu_model="RTX 4090",
            dedicated_vram_gb=24.0,
            selected_model="SDXL_BASE",
        )

        conn = runner.test_workstation_connection(valid_cfg)
        self.assertEqual(conn["handshake"], "HANDSHAKE_VERIFIED")
        self.assertEqual(conn["bridge_status"], "READY_FOR_REMOTE_EXECUTION")
        self.assertTrue(conn["laptop_hold_active"])

        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-DESKTOP-01",
            goal_description="Render photorealistic arched bridge over water",
            region_constraints=(
                RegionConstraintV1("R0", (0, 0, 64, 30), ConstraintKindV1.FLEX, 5.0, "Upper sky"),
            ),
            rigor_profile=RigorProfileV1.SEMANTIC_SKETCH,
        )

        job = runner.execute_remote_neural_job(valid_cfg, intent)
        self.assertEqual(job.dispatch_status, "DISPATCHED_TO_WORKSTATION")
        self.assertTrue(job.local_laptop_safe)
        self.assertIsNotNone(job.output_artifact_sha256)

    def test_tool_selection_from_intent_and_memory(self):
        class MockExp:
            def __init__(self, tools: tuple[str, ...]):
                self.procedure_refs = tuple(f"tool:{t}" for t in tools)

        # Grounded experiences with PEN and GEOMETRIC_STAMP
        exps = [MockExp(("PEN", "GEOMETRIC_STAMP"))]

        tools = ToolSelectorFromIntentAndMemoryV1.select_tools_for_intent(
            "Draw rectangular foundation box",
            exps,
        )
        self.assertIn("PEN", tools)
        self.assertIn("GEOMETRIC_STAMP", tools)

        # With shading intent
        tools_shading = ToolSelectorFromIntentAndMemoryV1.select_tools_for_intent(
            "Apply directional shading hatch strokes",
            [MockExp(("PEN", "HATCHING"))],
        )
        self.assertIn("HATCHING", tools_shading)


class TestRebootAndReloadPersistence(unittest.TestCase):
    """Section B Point 9: Multi-session reload after restart with revisions and contradictions."""

    def test_reboot_and_reload_persistence(self):
        harness = MultiSessionRetentionHarnessV1()
        with TemporaryDirectory() as tmp_dir:
            persist_file = Path(tmp_dir) / "reboot_experience_ledger.json"
            result = harness.simulate_reboot_and_reload_persistence(persist_file)

            self.assertEqual(result["status"], "REBOOT_RELOAD_SUCCESS")
            self.assertEqual(result["reloaded_experience_id"], "EXP-HIST-PERSISTED-001")
            self.assertEqual(result["revisions_preserved"], 1)
            self.assertEqual(result["contradictions_preserved"], 2)
            self.assertTrue(result["provenance_intact"])
            self.assertEqual(result["decision_authority"], "KX108_ONLY")


if __name__ == "__main__":
    unittest.main()
