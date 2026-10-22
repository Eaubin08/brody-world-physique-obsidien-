"""Unit & Integrated Tests for Stack Connection Audit, Multi-Clip Video, and Novel Situation Transfer.

Fulfills all requirements of AGY Brody World Physique Image:
1. Real Stack Connection Audit (distinguishing INTEGRATED, CONTRACTUAL_COMPATIBILITY, LOCAL_SIMULATION, UNCONNECTED_STANDBY).
2. Video multi-clip evaluation across 5 distinct scenarios (trajectory, camera pan, occlusion, morphology, noise/UNKNOWN).
3. Educational sequence: learn on Exercise 1, transfer to novel Exercise 2 (with & without memory ablation).
4. Answers the core question: Brody can use newly acquired visual experience to immediately succeed on an unseen situation.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from brody_world_physique.contracts_v0 import DECISION_AUTHORITY
from brody_world_physique.real_stack_connection_audit_v1 import (
    RealStackConnectionAuditorV1,
    StackConnectionAuditReportV1,
    SubsystemConnectionStatusV1,
)
from brody_world_physique.temporal_multiclip_evaluation_v1 import (
    ClipEvaluationReportV1,
    MultiClipVideoEvaluatorV1,
)
from brody_world_physique.novel_situation_transfer_loop_v1 import (
    EmpiricalTransferProofReportV1,
    NovelSituationTransferHarnessV1,
)


class TestRealStackConnectionAudit(unittest.TestCase):
    """Section 1: Verifies honest classification of all subsystems without inflated claims."""

    def test_audit_subsystem_connection_statuses(self):
        report = RealStackConnectionAuditorV1.audit_stack_connections()
        self.assertIsInstance(report, StackConnectionAuditReportV1)
        self.assertEqual(report.decision_authority, "KX108_ONLY")
        self.assertTrue(report.sovereign_gate_intact)

        # Total subsystems audited
        self.assertEqual(len(report.subsystems), 8)

        status_by_id = {s.subsystem_id: s.connection_status for s in report.subsystems}

        # 1. Truly integrated subsystems in local execution
        self.assertEqual(status_by_id["MMONDE_F12_TEMPORAL"], SubsystemConnectionStatusV1.INTEGRATED)
        self.assertEqual(status_by_id["OBSIDIA_34_TREES"], SubsystemConnectionStatusV1.INTEGRATED)
        self.assertEqual(status_by_id["FRISE_CHRONOLOGIQUE_M01"], SubsystemConnectionStatusV1.INTEGRATED)
        self.assertEqual(status_by_id["RELATIONS_MULTIDIMENSIONNELLES_M04"], SubsystemConnectionStatusV1.INTEGRATED)
        self.assertEqual(status_by_id["INSTRUMENTS_ORCHESTRATOR_O04"], SubsystemConnectionStatusV1.INTEGRATED)

        # 2. Contractual compatibility / guarded gate (no remote socket / no live kernel mutation)
        self.assertEqual(status_by_id["JARVIS_F16_VISION"], SubsystemConnectionStatusV1.CONTRACTUAL_COMPATIBILITY)
        self.assertEqual(status_by_id["NATIVE_MEMORY_SOVEREIGN_GATE_M08"], SubsystemConnectionStatusV1.CONTRACTUAL_COMPATIBILITY)

        # 3. Unconnected standby (PC Fixe GPU neural generator bridge)
        self.assertEqual(status_by_id["NEURAL_GENERATOR_PC_FIXE_G02"], SubsystemConnectionStatusV1.UNCONNECTED_STANDBY)

        # Counts check
        self.assertEqual(report.integrated_count, 5)
        self.assertEqual(report.contractual_compat_count, 2)
        self.assertEqual(report.unconnected_standby_count, 1)


class TestMultiClipVideoEvaluation(unittest.TestCase):
    """Section 2: Verifies multi-clip temporal tracking, preverbal prediction, and hypothesis infirmer."""

    def test_multi_clip_video_scenarios(self):
        evaluator = MultiClipVideoEvaluatorV1()
        with TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "video_reports"
            suite = evaluator.run_full_suite(output_dir=out_dir)

            self.assertEqual(len(suite), 5)

            # 1. Clip 01: Parabolic trajectory with fixed anchor
            c1 = suite["CLIP_01_PARABOLIC_BALLISTIC"]
            self.assertEqual(c1.clip_verdict, "PREVERBAL_TRAJECTORY_ACCURACY_PROVEN")
            self.assertIsNotNone(c1.mean_spatial_error_px)
            self.assertLess(c1.mean_spatial_error_px, 2.0)
            self.assertGreater(c1.confrontation_success_rate, 0.60)

            # 2. Clip 02: Camera pan displacement
            c2 = suite["CLIP_02_CAMERA_PAN_DISPLACEMENT"]
            self.assertEqual(c2.clip_verdict, "CAMERA_MOTION_PROVEN_AND_HELD")
            self.assertTrue(any("Stationary camera" in h for h in c2.infirmed_hypotheses))

            # 3. Clip 03: Occlusion and reemergence
            c3 = suite["CLIP_03_OCCLUSION_AND_REEMERGENCE"]
            self.assertEqual(c3.clip_verdict, "OCCLUSION_AND_REEMERGENCE_PROVEN")
            self.assertTrue(any("Continuous optical visibility" in h for h in c3.infirmed_hypotheses))

            # 4. Clip 04: Morphology deformation
            c4 = suite["CLIP_04_MORPHOLOGY_DEFORMATION"]
            self.assertTrue(any("Rigid-body" in h for h in c4.infirmed_hypotheses))

            # 5. Clip 05: Ambiguous / noisy signal
            c5 = suite["CLIP_05_NOISY_AMBIGUOUS_SIGNAL"]
            self.assertEqual(c5.clip_verdict, "RIGOROUS_UNKNOWN_PRESERVED")
            self.assertGreater(c5.unknown_count, 0)
            self.assertIsNone(c5.mean_spatial_error_px)


class TestNovelSituationTransferLoop(unittest.TestCase):
    """Section 3 & 4: Educational learning on Ex 1 and empirical transfer to unseen Ex 2."""

    def test_novel_situation_transfer_experiment(self):
        harness = NovelSituationTransferHarnessV1()
        with TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "transfer_experiment"
            report = harness.execute_complete_transfer_experiment(output_dir=out_dir)

            self.assertIsInstance(report, EmpiricalTransferProofReportV1)
            self.assertTrue(report.transfer_hypothesis_confirmed)
            self.assertEqual(report.decision_authority, "KX108_ONLY")
            self.assertEqual(report.reused_experience_id, "EXP-LEARNED-ANGULAR-CHEVRON-V1")

            # Exercise 1: Naive start followed by successful angled learning
            ex1 = report.exercise_1_learning_receipt
            self.assertEqual(ex1.exercise_id, "EXERCISE_1_CHEVRON_TRUSS")
            self.assertLess(ex1.initial_iou, 0.30)
            self.assertGreater(ex1.final_iou, 0.75)
            self.assertGreaterEqual(ex1.corrective_steps_applied, 4)

            # Exercise 2 Control (Memory OFF): Naive box fallback with poor performance
            ex2_off = report.exercise_2_memory_off_control
            self.assertEqual(ex2_off.exercise_id, "EXERCISE_2_GABLE_ROOF_OVERHANG")
            self.assertLess(ex2_off.initial_iou, 0.30)
            self.assertGreater(ex2_off.corrective_steps_applied, 0)

            # Exercise 2 Transfer (Memory ON): Immediate high-fidelity reuse of acquired chevron experience
            ex2_on = report.exercise_2_memory_on_transfer
            self.assertEqual(ex2_on.exercise_id, "EXERCISE_2_GABLE_ROOF_OVERHANG")
            self.assertGreater(ex2_on.initial_iou, 0.70)
            self.assertEqual(ex2_on.corrective_steps_applied, 0)
            self.assertEqual(ex2_on.retrieved_experience_id, "EXP-LEARNED-ANGULAR-CHEVRON-V1")

            # Comparative metrics proving memory efficacy
            self.assertGreater(report.initial_iou_jump, 0.40)
            self.assertGreater(report.cost_reduction_percent, 35.0)

            # Artifacts inspection
            self.assertTrue((out_dir / "ex1_target_chevron.png").exists())
            self.assertTrue((out_dir / "ex1_produced_chevron.png").exists())
            self.assertTrue((out_dir / "ex2_target_gable_roof.png").exists())
            self.assertTrue((out_dir / "ex2_produced_memory_off.png").exists())
            self.assertTrue((out_dir / "ex2_produced_memory_on.png").exists())
            self.assertTrue((out_dir / "brody_novel_generated_scene.png").exists())
            self.assertTrue((out_dir / "transfer_experiment_report.json").exists())


if __name__ == "__main__":
    unittest.main()
