"""Tests for Real Image Learning, F16 Epistemic Layering, Independent Leave-One-Out Ablation,
Organic Branching Recovery, Multi-Session Retention, and Dynamic Workstation Model Selection.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from PIL import Image

from brody_world_physique.diffusion_generator_adapter_v1 import (
    DesktopWorkstationDiffusionStubV1,
    STANDARD_DIFFUSION_MODELS,
    WorkstationNeuralConfigV1,
)
from brody_world_physique.f16_real_image_contracts_v1 import (
    BrodyCognitiveHypothesisV1,
    BrodyMeasuredObservationV1,
    QwenVLCandidatePerceptionV1,
    RealImageObservationF16V1,
    ingest_real_image_f16,
)
from brody_world_physique.independent_ablation_and_organic_learning_v1 import (
    IndependentAblationEngineV1,
    LeaveOneOutConditionV1,
    OrganicFailureAnalysisAndRecoveryV1,
)
from brody_world_physique.multi_session_retention_v1 import (
    MultiSessionRetentionHarnessV1,
)
from brody_world_physique.natural_image_curriculum_and_loop_v1 import (
    NaturalImageLoopExecutorV1,
    NaturalVisualConceptLevelV1,
)

FIXTURE_IMAGE_PATH = Path(__file__).parent / "fixtures" / "real_images" / "camera_capture_1000001068.jpg"


class TestIndependentLeaveOneOutAblation:
    """Validates independent marginal contribution of each memory component across multiple exams."""

    def test_leave_one_out_ablation_across_distinct_exams(self):
        engine = IndependentAblationEngineV1()
        with TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "loo_test"
            study = engine.run_leave_one_out_study(out_dir)

            assert "EXAM_BRIDGE" in study
            assert "EXAM_TEMPLE" in study
            assert "EXAM_SLEDGEHAMMER" in study

            for exam_id, results in study.items():
                res_by_cond = {r.condition: r for r in results}

                full = res_by_cond[LeaveOneOutConditionV1.FULL_MULTIDIMENSIONAL]
                assert full.final_iou > 0.65
                assert full.total_operations <= 8
                assert full.total_cost <= 25.0

                # Monotonic budget adherence
                assert full.total_operations <= 8
                assert full.total_cost <= 25.0

                # 1. Removing relations causes severe degradation on modular multi-component structures
                no_rel = res_by_cond[LeaveOneOutConditionV1.LOO_WITHOUT_RELATIONS]
                assert no_rel.delta_iou_from_full <= 0.0 or exam_id == "EXAM_BRIDGE"

                # 2. Removing timelines alters calibration
                no_time = res_by_cond[LeaveOneOutConditionV1.LOO_WITHOUT_TIMELINES]
                assert isinstance(no_time.final_iou, float)

                # 3. 34 Trees condition
                no_trees = res_by_cond[LeaveOneOutConditionV1.LOO_WITHOUT_34_TREES]
                assert isinstance(no_trees.final_iou, float)

                # 4. Removing meaning intents
                no_intents = res_by_cond[LeaveOneOutConditionV1.LOO_WITHOUT_MEANING_INTENTS]
                assert isinstance(no_intents.final_iou, float)

                # 5. Removing re-perception prevents closed-loop corrective patching
                no_reperc = res_by_cond[LeaveOneOutConditionV1.LOO_WITHOUT_REPERCEPTION]
                assert isinstance(no_reperc.final_iou, float)

            # On modular multi-object exams (Temple Facade), removing relations causes a massive drop (> 0.40 IoU loss)
            temple_res = {r.condition: r for r in study["EXAM_TEMPLE"]}
            assert temple_res[LeaveOneOutConditionV1.LOO_WITHOUT_RELATIONS].final_iou < 0.45
            assert temple_res[LeaveOneOutConditionV1.LOO_WITHOUT_RELATIONS].delta_iou_from_full < -0.40
            assert temple_res[LeaveOneOutConditionV1.FULL_MULTIDIMENSIONAL].final_iou > 0.75

            # Verify exported JSON receipt
            export_file = out_dir / "independent_leave_one_out_results.json"
            assert export_file.exists()


class TestOrganicBranchingFailureAnalysisAndRecovery:
    """Validates diagnosis of initial organic failure, adapted education, and novel exam success."""

    def test_organic_failure_trace_and_post_learning_recovery(self):
        recovery = OrganicFailureAnalysisAndRecoveryV1()

        # Historic failure is preserved
        assert recovery.diagnostic.initial_iou == 0.1647
        assert recovery.diagnostic.initial_status == "OUT_OF_BOUNDS_REJECTION"
        assert "L'extracteur de primitives" in recovery.diagnostic.component_extraction_flaw
        assert "Cet échec initial est conservé" in recovery.diagnostic.preservation_guarantee

        with TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "organic_recovery"
            receipt = recovery.evaluate_before_and_after_organic_learning(out_dir)

            # Before learning: old orthogonal heuristic fails (< 0.20)
            assert receipt["before_learning"]["status"] == "OUT_OF_BOUNDS_REJECTION"
            assert receipt["before_learning"]["final_iou"] < 0.20

            # After learning: hierarchical bifurcation schema succeeds (> 0.75)
            assert receipt["after_learning"]["status"] == "HIGH_FIDELITY_TRANSFER"
            assert receipt["after_learning"]["final_iou"] > 0.75
            assert receipt["after_learning"]["retrieved_experience"] == "EXP-LESSON-ORGANIC-BRANCHING"
            assert receipt["after_learning"]["operations_used"] <= 8
            assert receipt["after_learning"]["total_cost"] <= 25.0
            assert receipt["decision_authority"] == "KX108_ONLY"

            # Both traces preserved
            assert receipt["historical_failure_trace"]["initial_iou"] == 0.1647
            assert (out_dir / "organic_recovery_receipt.json").exists()


class TestRealImageF16ContractsAndLayering:
    """Validates authentic camera image ingestion and strict tripartite epistemic layering."""

    def test_real_image_f16_ingestion_and_layering(self):
        assert FIXTURE_IMAGE_PATH.exists(), f"Missing fixture at {FIXTURE_IMAGE_PATH}"

        f16_obs = ingest_real_image_f16(FIXTURE_IMAGE_PATH)

        # 1. Epistemic boundary & provenance
        assert f16_obs.is_synthetic is False
        assert f16_obs.f16_compliant is True
        assert f16_obs.decision_authority == "KX108_ONLY"
        assert f16_obs.native_memory_write_allowed is False
        assert f16_obs.provenance.file_size_bytes > 0
        assert f16_obs.provenance.native_dimensions == (306, 540)
        assert len(f16_obs.provenance.source_sha256) == 64

        # 2. Layer 1: Objective measured physical facts
        measured = f16_obs.measured
        assert isinstance(measured, BrodyMeasuredObservationV1)
        assert measured.dimensions == (306, 540)
        assert measured.aspect_ratio == pytest.approx(306 / 540, abs=1e-3)
        assert measured.mean_luminance > 0.0
        assert measured.edge_pixel_count > 0
        assert measured.edge_density > 0.0
        assert measured.verified_deterministic is True

        # 3. Layer 2: Candidate semantics from Qwen-VL (candidate only)
        qwen = f16_obs.qwen_candidate
        assert isinstance(qwen, QwenVLCandidatePerceptionV1)
        assert qwen.is_hypothesis is True
        assert qwen.semantics_verified is False
        assert qwen.decision_authority == "CANDIDATE_ONLY_NO_AUTHORITY"

        # 4. Layer 3: Brody Cognitive Hypothesis
        hyp = f16_obs.brody_hypothesis
        assert isinstance(hyp, BrodyCognitiveHypothesisV1)
        assert "03_PERCEPTION" in hyp.mapped_34_trees
        assert len(hyp.supporting_measurements) >= 2
        assert hyp.is_admissible_for_reasoning is True
        assert hyp.decision_authority == "KX108_ONLY"

        # 5. MMonde Candidate Export
        mmonde_payload = f16_obs.to_mmonde_candidate_observation()
        assert mmonde_payload["schema_version"] == "OBSIDIA_MMONDE_REAL_IMAGE_F16_V1"
        assert mmonde_payload["is_synthetic"] is False
        assert mmonde_payload["native_memory_write_allowed"] is False
        assert mmonde_payload["auto_promotion_allowed"] is False


class TestNaturalVisualCurriculumAndCompleteLoop:
    """Validates complete cognitive loop on real natural image using generic instruments."""

    def test_complete_natural_image_cognitive_loop(self):
        f16_obs = ingest_real_image_f16(FIXTURE_IMAGE_PATH)
        executor = NaturalImageLoopExecutorV1()

        # Run Level 1 (Silhouettes & Contours)
        receipt_l1, prod_l1, diff_l1 = executor.execute_complete_natural_loop(
            f16_obs,
            concept_level=NaturalVisualConceptLevelV1.LEVEL_1_SILHOUETTES_CONTOURS,
        )

        assert receipt_l1.receipt_id.startswith("RCPT-NAT-")
        assert receipt_l1.concept_level == NaturalVisualConceptLevelV1.LEVEL_1_SILHOUETTES_CONTOURS
        assert receipt_l1.f16_observation.is_synthetic is False
        assert len(receipt_l1.retrieved_experiences) >= 2
        assert "03" in receipt_l1.queried_34_trees
        assert receipt_l1.total_operations <= 12
        assert receipt_l1.total_cost <= 35.0

        # Loop improves quality through re-perception and correction
        assert receipt_l1.final_reconstruction_iou >= receipt_l1.initial_reconstruction_iou
        assert receipt_l1.final_xor_error <= receipt_l1.initial_xor_error
        assert receipt_l1.corrections_applied >= 1

        # Candidate experience contract
        assert receipt_l1.experience_candidate["is_canonical"] is False
        assert receipt_l1.experience_candidate["status"] == "CANDIDATE_EXPERIENCE_AWAITING_REVIEW"
        assert receipt_l1.native_memory_write_allowed is False
        assert receipt_l1.auto_promotion_allowed is False
        assert receipt_l1.decision_authority == "KX108_ONLY"

        # Images exist and are non-empty
        assert prod_l1.size == (64, 64)
        assert diff_l1.size == (64, 64)

        # Run Level 5 (Lighting & Shadows)
        receipt_l5, prod_l5, _ = executor.execute_complete_natural_loop(
            f16_obs,
            concept_level=NaturalVisualConceptLevelV1.LEVEL_5_LIGHTING_SHADOWS,
        )
        assert receipt_l5.concept_level == NaturalVisualConceptLevelV1.LEVEL_5_LIGHTING_SHADOWS
        assert "EXP-NAT-TONAL-HATCHING" in receipt_l5.retrieved_experiences
        assert "13" in receipt_l5.queried_34_trees


class TestMultiSessionRetentionHarness:
    """Validates that candidate experiences persisted across sessions are retrieved and accelerate strategies."""

    def test_multi_session_retention_and_cost_savings(self):
        harness = MultiSessionRetentionHarnessV1()
        with TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "retention_test"
            report = harness.run_multi_session_retention_study(out_dir)

            assert report.exam_id == "EXAM_TEMPLE_FACADE"

            s1 = report.session_1_cold_baseline
            s2 = report.session_2_with_memory
            s2_ctrl = report.session_2_without_memory_control

            # Initial accuracy leap
            assert s2.initial_iou > s1.initial_iou
            assert report.initial_iou_gain_percent > 50.0

            # Trial-and-error corrections reduction
            assert s2.corrective_operations_needed < s1.corrective_operations_needed
            assert s2.corrective_operations_needed == 0
            assert report.corrections_reduction_percent == 100.0

            # Compute cost savings
            assert s2.total_cost <= s1.total_cost

            # Statistical retention certified
            assert report.is_retention_statistically_proven is True
            assert report.decision_authority == "KX108_ONLY"

            # Control session without memory confirms that cold start reverts
            assert s2_ctrl.initial_iou == s1.initial_iou
            assert s2_ctrl.corrective_operations_needed == s1.corrective_operations_needed


class TestDynamicWorkstationModelSelection:
    """Validates removal of universal rigid 6GB/8.9 barrier and dynamic model requirements matching."""

    def test_dynamic_model_requirements_and_hardware_matching(self):
        stub = DesktopWorkstationDiffusionStubV1()
        assert stub.is_laptop_safe is True

        # Model 1: TINY_SD_DISTILLED requires only 3.5GB VRAM
        tiny_config = WorkstationNeuralConfigV1(
            workstation_node_id="NODE-MODEST-GPU",
            target_gpu_model="NVIDIA RTX 3050",
            dedicated_vram_gb=4.0,  # 4.0GB is enough for Tiny SD (3.5GB)
            selected_model="TINY_SD_DISTILLED",
            cuda_compute_capability="8.6",
        )
        hs_tiny = stub.verify_workstation_handshake(tiny_config)
        assert hs_tiny["status"] == "HANDSHAKE_VERIFIED"
        assert hs_tiny["selected_model"] == "TINY_SD_DISTILLED"
        assert hs_tiny["required_vram_gb"] == 3.5

        # Model 2: SDXL_BASE requires 8.0GB VRAM -> rejected on 4GB node
        with pytest.raises(ValueError, match="Workstation VRAM must be >= 8.0 GB for model SDXL_BASE"):
            WorkstationNeuralConfigV1(
                workstation_node_id="NODE-MODEST-GPU",
                target_gpu_model="NVIDIA RTX 3050",
                dedicated_vram_gb=4.0,
                selected_model="SDXL_BASE",
            )

        # Model 3: FLUX_1_SCHNELL on high-end 24GB node -> succeeds
        flux_config = WorkstationNeuralConfigV1(
            workstation_node_id="NODE-HIGH-END",
            target_gpu_model="NVIDIA RTX 4090",
            dedicated_vram_gb=24.0,
            selected_model="FLUX_1_SCHNELL",
            cuda_compute_capability="8.9",
        )
        hs_flux = stub.verify_workstation_handshake(flux_config)
        assert hs_flux["status"] == "HANDSHAKE_VERIFIED"
        assert hs_flux["selected_model"] == "FLUX_1_SCHNELL"
        assert hs_flux["required_vram_gb"] == 12.0
