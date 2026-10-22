"""Tests for Generic Transfer, Out-of-Process Restart, Obsidia Stack Audit, Filmed Video, Observation-to-Creation, and Neural Generator Audit (V1).

Validates all 7 Mission Points:
1. Generic transfer across 3 unseen task families without hardcoded scenario tricks.
2. Memory persistence and transfer across real independent process reboot (Phase 1 PID != Phase 2 PID).
3. Live trace of 6 Obsidia subsystems under 5-tier classification.
4. Filmed video evaluation with SYNTHETIC, RECORDED_REAL, and LIVE streams + UNKNOWN preservation.
5. Observation to creation loop (curved extraction from real photo -> novel bridge design).
6. Workstation hardware audit and seeded neural generation under LOCK/FLEX intent boundaries.
"""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from brody_world_physique.generic_transfer_benchmark_v1 import (
    GenericTransferBenchmarkHarnessV1,
    GenericTransferBenchmarkReportV1,
)
from brody_world_physique.persistent_process_restart_test_v1 import (
    PersistentProcessRestartHarnessV1,
    ProcessRestartProofReceiptV1,
)
from brody_world_physique.obsidia_interstack_connection_tracer_v1 import (
    InterstackTraceAuditReportV1,
    ObsidiaConnectionTierV1,
    ObsidiaInterstackConnectionTracerV1,
)
from brody_world_physique.filmed_video_evaluation_v1 import (
    FilmedVideoEvaluationReportV1,
    FilmedVideoEvaluatorV1,
    VideoProvenanceV1,
)
from brody_world_physique.observation_to_creation_loop_v1 import (
    ObservationToCreationLoopV1,
    ObservationToCreationReportV1,
)
from brody_world_physique.workstation_neural_generation_auditor_v1 import (
    NeuralGenerationAuditAndExecutionReportV1,
    WorkstationNeuralGenerationAuditorV1,
)


class TestGenericTransferBenchmark(unittest.TestCase):
    """Point 1: Generic transfer without scenario-specific names."""

    def test_generic_transfer_benchmark(self):
        harness = GenericTransferBenchmarkHarnessV1()
        with TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "generic_transfer"
            report = harness.run_complete_benchmark(output_dir=out_dir)

            self.assertIsInstance(report, GenericTransferBenchmarkReportV1)
            self.assertEqual(report.decision_authority, "KX108_ONLY")
            self.assertTrue(report.multidimensional_outperforms_flat)
            self.assertTrue(report.multidimensional_outperforms_no_memory)

            # Check conditions
            multi_agg = report.condition_aggregates["MULTIDIMENSIONAL_MEMORY"]
            flat_agg = report.condition_aggregates["FLAT_PROCEDURAL_MEMORY"]
            none_agg = report.condition_aggregates["NO_MEMORY"]

            self.assertGreater(multi_agg.average_final_iou, 0.70)
            self.assertGreater(multi_agg.average_final_iou, flat_agg.average_final_iou)
            self.assertGreater(multi_agg.average_final_iou, none_agg.average_final_iou)
            self.assertEqual(multi_agg.average_corrective_steps, 0.0)
            self.assertEqual(multi_agg.success_rate_percent, 100.0)

            # Verify artifacts generated
            self.assertTrue((out_dir / "generic_transfer_benchmark_report.json").exists())


class TestPersistentProcessRestart(unittest.TestCase):
    """Point 2: True memory persistence and transfer across independent process reboot."""

    def test_cross_process_persistence_and_restart(self):
        harness = PersistentProcessRestartHarnessV1()
        with TemporaryDirectory() as tmp_dir:
            receipt = harness.execute_cross_process_persistence_study(working_dir=tmp_dir)

            self.assertIsInstance(receipt, ProcessRestartProofReceiptV1)
            self.assertEqual(receipt.decision_authority, "KX108_ONLY")
            self.assertTrue(receipt.different_pids_verified)
            self.assertNotEqual(receipt.phase1_pid, receipt.phase2_pid)

            # Check that all multidimensional fields survived process termination
            self.assertTrue(receipt.timeline_intact)
            self.assertTrue(receipt.tree_projections_intact)
            self.assertTrue(receipt.calibration_intact)
            self.assertTrue(receipt.storage_provenance_intact)

            # Check transfer performance in the rebooted process
            self.assertTrue(receipt.transfer_success)
            self.assertGreater(receipt.transfer_task_iou, 0.70)


class TestObsidiaInterstackConnectionTracer(unittest.TestCase):
    """Point 3: Real call traces across the 6 Obsidia subsystems under 5-tier classification."""

    def test_interstack_connection_traces(self):
        tracer = ObsidiaInterstackConnectionTracerV1()
        with TemporaryDirectory() as tmp_dir:
            report = tracer.execute_complete_stack_trace_audit(output_dir=tmp_dir)

            self.assertIsInstance(report, InterstackTraceAuditReportV1)
            self.assertEqual(report.sovereign_authority, "KX108_ONLY")
            self.assertTrue(report.no_unjustified_integrated_declaration)
            self.assertEqual(len(report.traces), 6)

            subsystems = {t.subsystem_id: t for t in report.traces}
            self.assertIn("JARVIS_F16", subsystems)
            self.assertIn("F12_MMONDE", subsystems)
            self.assertIn("NATIVE_MEMORY_GATE", subsystems)
            self.assertIn("SENS_ENGINE", subsystems)
            self.assertIn("BINDER_ORCHESTRATOR", subsystems)
            self.assertIn("BRODY_COGNITIVE_CORE", subsystems)

            # Verify that native memory write was strictly blocked
            self.assertTrue(subsystems["NATIVE_MEMORY_GATE"].native_memory_write_blocked)

            # Verify classifications
            self.assertEqual(subsystems["JARVIS_F16"].connection_tier, ObsidiaConnectionTierV1.CONTRAT_COMPATIBLE)
            self.assertEqual(subsystems["F12_MMONDE"].connection_tier, ObsidiaConnectionTierV1.CONTRAT_COMPATIBLE)
            self.assertEqual(subsystems["BINDER_ORCHESTRATOR"].connection_tier, ObsidiaConnectionTierV1.LIVE_VERIFIED)
            self.assertEqual(subsystems["BRODY_COGNITIVE_CORE"].connection_tier, ObsidiaConnectionTierV1.LIVE_VERIFIED)


class TestFilmedVideoEvaluation(unittest.TestCase):
    """Point 4: Multi-frame video evaluation with 3 provenances and UNKNOWN preservation."""

    def test_filmed_video_evaluation(self):
        evaluator = FilmedVideoEvaluatorV1()
        with TemporaryDirectory() as tmp_dir:
            report = evaluator.evaluate_all_clips(output_dir=tmp_dir)

            self.assertIsInstance(report, FilmedVideoEvaluationReportV1)
            self.assertEqual(report.decision_authority, "KX108_ONLY")
            self.assertTrue(report.unknown_preservation_verified)
            self.assertTrue(report.tracking_accuracy_acceptable)

            # Check that all 3 provenance types were evaluated
            self.assertIn(VideoProvenanceV1.SYNTHETIC.value, report.provenance_distribution)
            self.assertIn(VideoProvenanceV1.RECORDED_REAL.value, report.provenance_distribution)
            self.assertIn(VideoProvenanceV1.LIVE.value, report.provenance_distribution)


class TestObservationToCreationLoop(unittest.TestCase):
    """Point 5: Connects observation of a real photo to a distinct creative creation task."""

    def test_observation_to_creation_sequence(self):
        loop = ObservationToCreationLoopV1()
        with TemporaryDirectory() as tmp_dir:
            report = loop.execute_observation_to_creation_sequence(output_dir=tmp_dir)

            self.assertIsInstance(report, ObservationToCreationReportV1)
            self.assertEqual(report.decision_authority, "KX108_ONLY")
            self.assertTrue(report.transfer_hypothesis_confirmed)
            self.assertGreater(report.iou_jump, 0.30)
            self.assertGreater(report.memory_on_transfer.final_iou, 0.90)
            self.assertLess(report.memory_off_control.final_iou, 0.70)
            self.assertEqual(report.memory_on_transfer.corrective_steps_applied, 0)


class TestWorkstationNeuralGenerationAuditor(unittest.TestCase):
    """Point 6: Hardware audit and seeded neural generation under LOCK/FLEX intent boundaries."""

    def test_neural_generation_workstation_audit_and_execution(self):
        auditor = WorkstationNeuralGenerationAuditorV1()
        with TemporaryDirectory() as tmp_dir:
            report = auditor.audit_and_execute(output_dir=tmp_dir, seed=42)

            self.assertIsInstance(report, NeuralGenerationAuditAndExecutionReportV1)
            self.assertEqual(report.decision_authority, "KX108_ONLY")

            # Hardware audit checks
            hw = report.hardware_model_audit
            self.assertTrue(hw.is_zero_download_enforced)
            self.assertTrue(hw.hardware_compatible)

            # Seeded execution checks
            exec_rec = report.execution_receipt
            self.assertEqual(exec_rec.seed, 42)
            self.assertEqual(exec_rec.lock_violations_count, 0)
            self.assertTrue(exec_rec.intent_compliant)
            self.assertGreater(exec_rec.reperceived_ink_pixels, 0)


if __name__ == "__main__":
    unittest.main()
