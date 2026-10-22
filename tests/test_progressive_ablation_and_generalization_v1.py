"""Tests for Progressive Memory Attribution, Multi-Family Generalization, Intent Creation,
Multi-Object Parallax Occlusion, and Desktop Workstation Diffusion Stub.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from PIL import Image, ImageDraw

from brody_world_physique.diffusion_generator_adapter_v1 import (
    DesktopWorkstationDiffusionStubV1,
    WorkstationNeuralConfigV1,
    WorkstationRemoteDispatchPayloadV1,
    MIN_VRAM_GB_FOR_HEAVY_DIFFUSION,
)
from brody_world_physique.expanded_generalization_curriculum_v1 import (
    AutonomousMultiFamilyAuditorV1,
    GeneralizationExamResultV1,
    TeacherMultiFamilyCurriculumV1,
    run_expanded_curriculum_suite,
)
from brody_world_physique.multi_perspective_view_v03_v04 import (
    DepthLayeredObjectV04,
    MultiPerspectiveTransformerV03V04,
    MultiObjectParallaxSceneResultV04,
    ObserverVantageShiftV04,
    ObjectPermanenceRecordV04,
)
from brody_world_physique.progressive_memory_ablation_v1 import (
    AblationStageV1,
    ProgressiveMemoryAblationEngineV1,
    run_progressive_ablation_suite,
)
from brody_world_physique.visual_intent_contracts_v1 import (
    ConstraintKindV1,
    RegionConstraintV1,
    RigorProfileV1,
    VisualEditIntentCandidateV1,
)


class TestProgressiveMemoryAblation:
    """Rigorous 6-stage progressive ablation test."""

    def test_six_stage_progressive_ablation_attribution(self):
        engine = ProgressiveMemoryAblationEngineV1()
        target_img = engine.curriculum.render_exam_unseen_arched_bridge()

        s1, _ = engine.evaluate_stage(AblationStageV1.STAGE_1_PROCEDURE_ONLY, target_img)
        s2, _ = engine.evaluate_stage(AblationStageV1.STAGE_2_PROCEDURE_PLUS_DOMAINS, target_img)
        s3, _ = engine.evaluate_stage(AblationStageV1.STAGE_3_PROCEDURE_DOMAINS_RELATIONS, target_img)
        s4, _ = engine.evaluate_stage(AblationStageV1.STAGE_4_TIMELINES_AND_REVISIONS, target_img)
        s5, _ = engine.evaluate_stage(AblationStageV1.STAGE_5_CANONICAL_34_TREES, target_img)
        s6, _ = engine.evaluate_stage(AblationStageV1.STAGE_6_FULL_MULTIDIMENSIONAL, target_img)

        # Monotonicity & empirical attribution verification
        # Stage 1: Procedure only (rigid frame)
        assert s1.final_iou < 0.30
        assert s1.total_operations <= 8
        assert s1.total_cost <= 25.0

        # Stage 2: Procedure + Domains
        # Honest attribution: Domain tag excludes physics distractor,
        # but drawing IoU is unchanged without structural relations.
        assert s2.final_iou == pytest.approx(s1.final_iou, abs=1e-3)
        assert "EXP-BALL-PHYSICS-TRAJECTORY" in s2.mechanism_diagnostic_note

        # Stage 3: Procedure + Domains + Relations (COMPOSES_WITH modular leap)
        assert s3.final_iou > s2.final_iou
        assert s3.final_iou > 0.50
        assert "COMPOSES_WITH" in s3.mechanism_diagnostic_note

        # Stage 4: + Timelines & Revisions (calibrated failure boundary)
        assert s4.final_iou >= s3.final_iou
        assert "Frise temporelle" in s4.mechanism_diagnostic_note

        # Stage 5: + 34 Trees Projections (curvilinear smooth arch via Tree 13)
        assert s5.final_iou >= s4.final_iou
        assert "34 arbres" in s5.mechanism_diagnostic_note

        # Stage 6: Full Multidimensional Memory Architecture (M01-M09)
        assert s6.final_iou > 0.70
        assert s6.final_xor_error < s1.final_xor_error
        assert "HOW_DID_I_SUCCEED" in s6.active_meaning_intents

        # Strict budget constraint check across all stages
        for stage_res in [s1, s2, s3, s4, s5, s6]:
            assert stage_res.total_operations <= 8
            assert stage_res.total_cost <= 25.0
            assert stage_res.decision_authority == "KX108_ONLY"


class TestGeneralizationCurriculumAndHonestRejections:
    """Multi-family unseen exams and honest boundary counter-examples."""

    def test_multi_family_transfer_and_counter_examples(self):
        auditor = AutonomousMultiFamilyAuditorV1()
        curr = auditor.curriculum

        # 1. Architecture: Temple Facade -> High transfer
        res_temple, _ = auditor.run_generalization_exam("EXAM_TEMPLE", "ARCHITECTURE", curr.render_exam_temple_facade())
        assert res_temple.competence_status == "HIGH_FIDELITY_TRANSFER"
        assert res_temple.final_iou > 0.80

        # 2. Vessels: Hourglass -> Moderate transfer
        res_vessel, _ = auditor.run_generalization_exam("EXAM_VESSEL", "VESSELS", curr.render_exam_hourglass())
        assert res_vessel.competence_status in ("HIGH_FIDELITY_TRANSFER", "MODERATE_TRANSFER")
        assert res_vessel.final_iou > 0.70

        # 3. Tools: Sledgehammer -> High transfer
        res_tool, _ = auditor.run_generalization_exam("EXAM_TOOL", "TOOLS_MECHANICAL", curr.render_exam_sledgehammer())
        assert res_tool.competence_status == "HIGH_FIDELITY_TRANSFER"
        assert res_tool.final_iou > 0.80

        # 4. Organic Branching Counter-Example -> Honest failure / out of bounds
        res_branch, _ = auditor.run_generalization_exam("EXAM_ORGANIC", "ORGANIC_FRACTAL", curr.render_exam_organic_branching())
        assert res_branch.competence_status == "OUT_OF_BOUNDS_REJECTION"
        assert res_branch.final_iou < 0.25
        assert "PLANAR_ORTHO_CURVILINEAR" in res_branch.failure_boundary_reason

        # 5. Amorphous Blob Counter-Example -> Honest failure / out of bounds
        res_blob, _ = auditor.run_generalization_exam("EXAM_BLOB", "AMORPHOUS_CREVICE", curr.render_exam_amorphous_blob())
        assert res_blob.competence_status == "OUT_OF_BOUNDS_REJECTION"
        assert res_blob.final_iou < 0.20
        assert "PLANAR_ORTHO_CURVILINEAR" in res_blob.failure_boundary_reason

        # Budget equality
        for res in [res_temple, res_vessel, res_tool, res_branch, res_blob]:
            assert res.total_operations <= 8
            assert res.total_cost <= 25.0


class TestIntentOnlyCreationWithReperception:
    """Creation from declarative intention without reference image."""

    def test_intent_creation_and_reperception(self):
        auditor = AutonomousMultiFamilyAuditorV1()
        receipt, img = auditor.run_intent_creation_with_reperception(
            "Create a classical temple facade with triangular pediment, 4 vertical colonnade pillars and stepped base plate"
        )

        assert receipt["mode"] == "INTENT_ONLY_CREATION_WITH_REPERCEPTION"
        assert receipt["target_provided"] is False
        assert receipt["total_operations"] > 0
        assert receipt["rendered_black_pixels"] > 200
        assert receipt["intention_satisfaction_score"] == 1.0
        assert img is not None


class TestMultiPerspectiveParallaxAndOcclusion:
    """Validation of 2.5D multi-object parallax, occlusion, and object permanence."""

    def test_multi_object_parallax_motion_and_permanence(self):
        transformer = MultiPerspectiveTransformerV03V04()

        # Background object (large square at depth z=3.0)
        bg_img = Image.new("L", (64, 64), 255)
        ImageDraw.Draw(bg_img).rectangle([20, 20, 44, 44], fill=0)
        bg_obj = DepthLayeredObjectV04(
            object_id="BG-WALL",
            image=bg_img,
            depth_z=3.0,
            anchor_xy=(0, 0),
            label="Background Wall",
        )

        # Foreground object (vertical pillar at depth z=1.0)
        fg_img = Image.new("L", (64, 64), 255)
        ImageDraw.Draw(fg_img).rectangle([28, 16, 36, 48], fill=0)
        fg_obj = DepthLayeredObjectV04(
            object_id="FG-PILLAR",
            image=fg_img,
            depth_z=1.0,
            anchor_xy=(0, 0),
            label="Foreground Pillar",
        )

        # Vantage A: Center observation (dx = 0)
        vantage_a = ObserverVantageShiftV04(observer_dx=0)
        scene_a = transformer.render_multi_object_parallax([bg_obj, fg_obj], vantage_a)

        assert scene_a.permanence_certified is True
        assert scene_a.is_3d_view_synthesis is False
        assert scene_a.occlusion_fractions["FG-PILLAR"] == 0.0
        # In center view, foreground pillar is right on top of wall, causing partial occlusion
        assert scene_a.occlusion_fractions["BG-WALL"] > 0.0

        # Background object permanence certified despite sensory occlusion
        bg_rec_a = next(r for r in scene_a.object_records if r.object_id == "BG-WALL")
        fg_rec_a = next(r for r in scene_a.object_records if r.object_id == "FG-PILLAR")
        assert bg_rec_a.permanence_certified is True
        assert bg_rec_a.is_partially_occluded is True

        # Vantage B: Shift observer dx = +15 (observer shifts right, objects shift left)
        # Foreground (z=1.0) shifts by round(15/1.0) = 15 px
        # Background (z=3.0) shifts by round(15/3.0) = 5 px
        # Foreground moves 10 px more than background, revealing previously occluded background!
        vantage_b = ObserverVantageShiftV04(observer_dx=15)
        scene_b = transformer.render_multi_object_parallax([bg_obj, fg_obj], vantage_b)

        assert scene_b.permanence_certified is True
        assert scene_b.is_3d_view_synthesis is False

        # Verify that relative parallax displacement occurred
        bg_rec_b = next(r for r in scene_b.object_records if r.object_id == "BG-WALL")
        fg_rec_b = next(r for r in scene_b.object_records if r.object_id == "FG-PILLAR")
        assert bg_rec_b.transformed_bbox != bg_rec_a.transformed_bbox
        assert fg_rec_b.transformed_bbox != fg_rec_a.transformed_bbox
        assert bg_rec_b.permanence_certified is True

    def test_multi_perspective_rejects_false_3d_claims(self):
        with pytest.raises(ValueError, match="3D view synthesis cannot be claimed"):
            ObserverVantageShiftV04(observer_dx=10, is_3d_view_synthesis=True)


class TestDesktopWorkstationDiffusionStub:
    """Validation of Desktop Workstation client stub and hardware barriers."""

    def test_workstation_handshake_and_dispatch_payload(self):
        stub = DesktopWorkstationDiffusionStubV1()

        # Laptop remains strictly protected on HOLD
        assert stub.is_laptop_safe is True

        # Handshake fails if workstation does not have enough VRAM
        with pytest.raises(ValueError, match="Workstation VRAM must be >="):
            WorkstationNeuralConfigV1(
                workstation_node_id="NODE-UNDERPOWERED",
                target_gpu_model="GTX 1650",
                dedicated_vram_gb=4.0,
            )

        # Valid high-end workstation config
        workstation_config = WorkstationNeuralConfigV1(
            workstation_node_id="NODE-WORKSTATION-PC-FIXE",
            target_gpu_model="NVIDIA GeForce RTX 4090",
            dedicated_vram_gb=24.0,
            cuda_compute_capability="8.9",
            local_weights_present=True,
        )

        handshake = stub.verify_workstation_handshake(workstation_config)
        assert handshake["status"] == "HANDSHAKE_VERIFIED"
        assert handshake["target_gpu"] == "NVIDIA GeForce RTX 4090"
        assert handshake["dedicated_vram_gb"] == 24.0
        assert handshake["local_laptop_hold_preserved"] is True

        # Prepare dispatch payload
        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-DESK-DISPATCH-001",
            goal_description="Render photorealistic marble column facade",
            rigor_profile=RigorProfileV1.STRICT_GEOMETRIC,
            region_constraints=[
                RegionConstraintV1(
                    region_id="reg_1",
                    bbox_xyxy=(10, 10, 54, 54),
                    constraint_kind=ConstraintKindV1.FLEX,
                    rationale="Facade Area",
                )
            ],
        )

        base_img = Image.new("L", (64, 64), 255)
        payload = stub.prepare_dispatch_payload(intent, base_img)

        assert isinstance(payload, WorkstationRemoteDispatchPayloadV1)
        assert payload.target_workstation_node == "NODE-WORKSTATION-PC-FIXE"
        assert payload.hold_on_heavy_weights is True
        assert payload.neural_generation_requested is True
        assert payload.base_canvas_sha256 is not None
        assert payload.decision_authority == "KX108_ONLY"
