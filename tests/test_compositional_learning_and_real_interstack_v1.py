"""Unit tests for Compositional Generalization, Educational Protocols, and Real Interstack Integration (V1).

Constitutional boundaries:
- KX108_ONLY decision authority.
- Candidate-only memory ledger.
- Zero eval/exec.
"""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image
import pytest

from brody_world_physique.contracts_v0 import DECISION_AUTHORITY
from brody_world_physique.drawing_school_v0 import SIDE, black_pixels
from brody_world_physique.visual_intent_contracts_v1 import (
    ConstraintKindV1,
    RegionConstraintV1,
    RigorProfileV1,
    VisualEditIntentCandidateV1,
)
from brody_world_physique.compositional_learning_and_real_interstack_v1 import (
    CompositionalLearningHarnessV1,
    EducationalProtocolV1,
    LearningVsRecallProofReceiptV1,
    ProtocolExecutionReceiptV1,
    RealInterstackAuditReportV1,
)
from scripts.pc_fixe_neural_inference_verifier import (
    PCFixeNeuralAuditReportV1,
    verify_pc_fixe_neural_inference,
)


@pytest.fixture
def harness() -> CompositionalLearningHarnessV1:
    return CompositionalLearningHarnessV1()


def test_compositional_teacher_scene_rendering(harness: CompositionalLearningHarnessV1):
    scene = harness.render_compositional_teacher_scene(asymmetry_offset=4, scale_factor=1.0)
    assert isinstance(scene, Image.Image)
    assert scene.size == (SIDE, SIDE)
    pixels = black_pixels(scene)
    assert len(pixels) > 50


def test_protocol_copie_execution(harness: CompositionalLearningHarnessV1, tmp_path: Path):
    target = harness.render_compositional_teacher_scene(asymmetry_offset=4, scale_factor=1.0)
    receipt = harness.run_protocol_copie(target, output_dir=tmp_path)

    assert isinstance(receipt, ProtocolExecutionReceiptV1)
    assert receipt.protocol == EducationalProtocolV1.COPIE
    assert receipt.is_success is True
    assert receipt.final_iou >= 0.70
    assert receipt.operations_count == 7
    assert receipt.compute_cost > 0.0
    assert receipt.lock_violations == 0
    assert "production" in receipt.artifact_paths
    assert Path(receipt.artifact_paths["production"]).exists()


def test_protocol_retention_execution(harness: CompositionalLearningHarnessV1, tmp_path: Path):
    target = harness.render_compositional_teacher_scene(asymmetry_offset=4, scale_factor=1.0)
    receipt = harness.run_protocol_retention(target, output_dir=tmp_path)

    assert isinstance(receipt, ProtocolExecutionReceiptV1)
    assert receipt.protocol == EducationalProtocolV1.RETENTION
    assert receipt.is_success is True
    assert receipt.final_iou >= 0.70
    assert receipt.operations_count == 7
    assert receipt.compute_cost > 0.0
    assert receipt.lock_violations == 0
    assert "production" in receipt.artifact_paths
    assert Path(receipt.artifact_paths["production"]).exists()


def test_protocol_creation_execution(harness: CompositionalLearningHarnessV1, tmp_path: Path):
    base_canvas = Image.new("L", (SIDE, SIDE), 255)
    # Base foundation in LOCK region
    from PIL import ImageDraw
    ImageDraw.Draw(base_canvas).rectangle([8, 44, 56, 54], outline=0, width=2)

    intent = VisualEditIntentCandidateV1(
        intent_id="INTENT-COMPOSITION-CREATION-TEST",
        goal_description="Synthesize composite arch with strut and fork in FLEX without violating LOCK base",
        rigor_profile=RigorProfileV1.STRICT_GEOMETRIC,
        region_constraints=(
            RegionConstraintV1("lock_base", (8, 44, 56, 54), ConstraintKindV1.LOCK, rationale="Immutable foundation"),
            RegionConstraintV1("flex_canopy", (8, 12, 56, 44), ConstraintKindV1.FLEX, rationale="Synthesis zone"),
        ),
    )

    receipt = harness.run_protocol_creation(intent, base_canvas, output_dir=tmp_path)

    assert isinstance(receipt, ProtocolExecutionReceiptV1)
    assert receipt.protocol == EducationalProtocolV1.CREATION
    assert receipt.is_success is True
    assert receipt.lock_violations == 0
    assert receipt.final_iou == 1.0
    assert receipt.operations_count == 5
    assert "production" in receipt.artifact_paths
    assert Path(receipt.artifact_paths["production"]).exists()


def test_learning_vs_recall_two_phase_experiment(harness: CompositionalLearningHarnessV1, tmp_path: Path):
    receipt = harness.run_learning_vs_recall_experiment(output_dir=tmp_path)

    assert isinstance(receipt, LearningVsRecallProofReceiptV1)
    assert receipt.phase1_initial_iou < receipt.phase1_final_iou
    assert receipt.phase1_errors_detected_count > 0
    assert receipt.phase1_correction_applied is True
    assert receipt.learned_experience_id == "EXP-COMPOSITE-ASYM-BRANCH-V1"
    assert "12" in receipt.learned_tree_projections
    assert receipt.phase2_zero_shot_iou >= 0.75
    assert receipt.phase2_corrective_steps == 0
    assert receipt.subsequent_transfer_confirmed is True
    assert receipt.decision_authority == DECISION_AUTHORITY


def test_obsidia_interprocess_integration_matrix(harness: CompositionalLearningHarnessV1, tmp_path: Path):
    report = harness.run_obsidia_interprocess_audit(output_dir=tmp_path)

    assert isinstance(report, RealInterstackAuditReportV1)
    assert len(report.entries) == 6
    assert report.decision_authority == DECISION_AUTHORITY

    subsystem_ids = {e.subsystem_id: e for e in report.entries}
    assert "OBSIDIA_CG9_PROVIDER_BINDER" in subsystem_ids
    assert "JARVIS_VISUAL_OPERATOR" in subsystem_ids
    assert "INSTRUMENT_ORCHESTRATOR_O04" in subsystem_ids
    assert "JARVIS_F16_MMONDE_F12" in subsystem_ids
    assert "NATIVE_MEMORY_GATE" in subsystem_ids
    assert "REMOTE_SOCKET_DAEMON_8081" in subsystem_ids

    # Provider binder and Jarvis visual operator should be integrated with real workspace repos
    assert subsystem_ids["OBSIDIA_CG9_PROVIDER_BINDER"].classification_tier == "INTERPROCESS_INTEGRATED"
    assert subsystem_ids["OBSIDIA_CG9_PROVIDER_BINDER"].commit_sha == "7ff43655"

    assert subsystem_ids["JARVIS_VISUAL_OPERATOR"].classification_tier == "INTERPROCESS_INTEGRATED"
    assert subsystem_ids["JARVIS_VISUAL_OPERATOR"].commit_sha == "f29664a"

    # Instrument orchestrator is live verified
    assert subsystem_ids["INSTRUMENT_ORCHESTRATOR_O04"].classification_tier == "LIVE_VERIFIED"

    # Daemon port 8081 must be marked HOLD with explicit hold reason
    assert subsystem_ids["REMOTE_SOCKET_DAEMON_8081"].classification_tier == "HOLD"
    assert "8081" in str(subsystem_ids["REMOTE_SOCKET_DAEMON_8081"].hold_reason)

    assert (tmp_path / "obsidia_interprocess_matrix_report.json").exists()


def test_pc_fixe_neural_verifier_run(tmp_path: Path):
    report = verify_pc_fixe_neural_inference(output_dir=tmp_path, seed=42)

    assert isinstance(report, PCFixeNeuralAuditReportV1)
    assert report.decision_authority == DECISION_AUTHORITY
    assert report.lock_violations_count == 0
    assert report.reproducible_seed == 42
    assert (tmp_path / "pc_fixe_neural_generated_canvas.png").exists()
    assert (tmp_path / "pc_fixe_neural_audit_report.json").exists()


def test_visual_demonstration_artifacts_present(harness: CompositionalLearningHarnessV1, tmp_path: Path):
    artifacts = harness.generate_complete_visual_demonstration(output_dir=tmp_path)

    expected_keys = [
        "01_source_scene",
        "02_observation_masked",
        "03_internal_representation",
        "04_initial_production",
        "05_reperceived_errors",
        "06_corrected_production",
        "07_candidate_experience",
    ]
    for k in expected_keys:
        assert k in artifacts
        p = Path(artifacts[k])
        assert p.exists()
        assert p.stat().st_size > 0

    json_path = Path(artifacts["07_candidate_experience"])
    cand_data = json.loads(json_path.read_text(encoding="utf-8"))
    assert cand_data["decision_authority"] == "KX108_ONLY"
    assert cand_data["native_memory_write_allowed"] is False
    assert cand_data["initial_iou"] < cand_data["final_iou"]
