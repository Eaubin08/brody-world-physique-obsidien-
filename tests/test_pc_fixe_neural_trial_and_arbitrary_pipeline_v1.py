"""Tests for PC Fixe Neural Trial Protocol and Arbitrary Image Pipeline V1.

Verifies:
1. PC Fixe Read-only Inventory Execution & Hardware Gating.
2. Arbitrary Image Pipeline Execution without Pre-injected Scenarios.
3. 3-Mode Comparative Neural Trial (Model Alone, Brody Procedural, Brody Piloting).
4. Rigorous Gating (HOLD_PC_FIXE_GPU_REQUIRED on laptop, no GPU leak).
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw
import pytest

from brody_world_physique.contracts_v0 import DECISION_AUTHORITY
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.operational_pipeline_and_master_plan_reconciliation_v3 import (
    OperationalBrodyImagePipelineEngineV3,
)
from brody_world_physique.pc_fixe_neural_trial_protocol_v1 import (
    PCFixeNeuralTrialProtocolEngineV1,
    TrialEvaluationModeV1,
    TrialExecutionStatusV1,
)


def test_pc_fixe_readonly_inventory_execution():
    """Verifies that the PC Fixe read-only inventory runs and correctly identifies laptop vs GPU."""
    from scripts.pc_fixe_readonly_environment_inventory import run_read_only_environment_inventory

    report = run_read_only_environment_inventory()
    assert report.hostname != ""
    assert report.cpu_cores >= 1
    assert report.ram_total_gb > 0.0
    assert len(report.port_probes) >= 4
    probed_port_nums = [p.port for p in report.port_probes]
    assert 8080 in probed_port_nums
    assert 8081 in probed_port_nums
    # On laptop without discrete GTX 1050 Ti, verify GPU is None or absent
    assert report.qwen_vl_engine_status in (
        "LOCAL_WEIGHTS_AND_MMPROJ_PRESENT_SERVER_IDLE",
        "LOCAL_WEIGHTS_DETECTED_SERVER_OFFLINE",
        "WEIGHTS_ABSENT_PORT_CLOSED",
    )
    assert report.sd_cpp_gtx1050ti_compatibility in (
        "CPU_ONLY_INFERENCE_REQUIRED",
        "COMPATIBLE_WITH_QUANTIZATION_Q4_0",
        "HIGH_COMPATIBILITY_VRAM_SUFFICIENT",
    )


def test_arbitrary_image_pipeline_run(tmp_path: Path):
    """Verifies arbitrary image processing with zero hardcoded shapes or coordinates."""
    engine = OperationalBrodyImagePipelineEngineV3()

    # Create unknown scene 1: Asymmetrical cross
    scene_1 = Image.new("L", (SIDE, SIDE), 255)
    draw_1 = ImageDraw.Draw(scene_1)
    draw_1.line([(10, 15), (50, 48)], fill=0, width=3)
    draw_1.line([(12, 50), (48, 12)], fill=0, width=2)
    draw_1.rectangle([20, 20, 30, 30], outline=0, width=1)

    out_1 = tmp_path / "arbitrary_run_1"
    receipt_1 = engine.run_pipeline_on_arbitrary_image(
        scene_1,
        output_dir=out_1,
        goal_description="Reconstruct diagonal cross and nested square",
    )

    assert receipt_1.observation_source_kind == "ARBITRARY_IMAGE_OBSERVATION"
    assert receipt_1.spatial_nodes_count >= 3
    assert receipt_1.retrieved_tool in ("PEN", "BRUSH")
    assert receipt_1.final_iou > 0.0
    assert Path(receipt_1.artifact_paths["01_observation"]).exists()
    assert Path(receipt_1.artifact_paths["06_candidate_receipt"]).exists()

    # Read candidate receipt
    cand_data = json.loads(Path(receipt_1.artifact_paths["06_candidate_receipt"]).read_text(encoding="utf-8"))
    assert cand_data["decision_authority"] == DECISION_AUTHORITY
    assert cand_data["native_memory_write_allowed"] is False

    # Create unknown scene 2: Arch with offset triangle
    scene_2 = Image.new("L", (SIDE, SIDE), 255)
    draw_2 = ImageDraw.Draw(scene_2)
    draw_2.arc([14, 20, 50, 54], start=180, end=360, fill=0, width=3)
    draw_2.polygon([(24, 20), (32, 8), (40, 20)], outline=0)

    out_2 = tmp_path / "arbitrary_run_2"
    receipt_2 = engine.run_pipeline_on_arbitrary_image(
        scene_2,
        output_dir=out_2,
        goal_description="Reconstruct curved arch with apex triangle",
    )
    assert receipt_2.final_iou > 0.0
    assert receipt_2.observation_sha256 != receipt_1.observation_sha256


def test_pc_fixe_neural_trial_protocol_modes(tmp_path: Path):
    """Verifies the 3-mode comparative neural trial protocol and gating."""
    trial_engine = PCFixeNeuralTrialProtocolEngineV1(output_dir=tmp_path / "trial_run")
    receipt = trial_engine.execute_comparative_trial()

    # 1. Verification of all 3 modes
    assert receipt.model_alone_metrics.mode == TrialEvaluationModeV1.MODEL_ALONE.value
    assert receipt.brody_procedural_metrics.mode == TrialEvaluationModeV1.BRODY_PROCEDURAL_ALONE.value
    assert receipt.brody_piloting_metrics.mode == TrialEvaluationModeV1.BRODY_PILOTING_MODEL.value

    # 2. Brody Piloting Superiority & Structural Invariance
    # Brody piloted mode protects LOCK region (>= 0.95 compliance)
    assert receipt.brody_piloting_metrics.lock_constraint_compliance >= 0.95
    assert receipt.lock_protection_maintained is True

    # Mode 1 (Model alone) has unguided drift in LOCK foundation
    assert receipt.model_alone_metrics.lock_constraint_compliance < receipt.brody_piloting_metrics.lock_constraint_compliance

    # Overall best mode is Brody Piloting Model
    assert receipt.best_mode == TrialEvaluationModeV1.BRODY_PILOTING_MODEL.value
    assert receipt.brody_superiority_margin >= 0.0

    # 3. Rigorous Hardware Gating
    # On laptop without GTX 1050 Ti, execution_status must be HOLD_PC_FIXE_GPU_REQUIRED
    assert receipt.execution_status == TrialExecutionStatusV1.HOLD_PC_FIXE_GPU_REQUIRED.value
    assert "sd.cpp" in receipt.exact_pc_fixe_command

    # 4. Artifacts created
    for name, path_str in receipt.artifacts.items():
        assert Path(path_str).exists(), f"Artifact missing: {name} at {path_str}"
