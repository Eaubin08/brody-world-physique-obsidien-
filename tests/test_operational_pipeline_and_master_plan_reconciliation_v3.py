"""Unit tests for Operational Visual Pipeline, Memory-Driven Routing, and Master Plan Reconciliation (V3).

Constitutional boundaries:
- KX108_ONLY authority.
- Candidate-only memory ledger.
- Zero eval/exec.
"""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image
import pytest

from brody_world_physique.contracts_v0 import DECISION_AUTHORITY
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.natural_visual_education_and_obsidia_interstack_v2 import (
    NaturalVisualEducationAndObsidiaInterstackV2,
)
from brody_world_physique.operational_pipeline_and_master_plan_reconciliation_v3 import (
    MasterPlanChantierAuditEntryV3,
    OperationalBrodyImagePipelineEngineV3,
    OperationalPipelineReceiptV3,
    PCFixeHardwareProfileV3,
)


@pytest.fixture
def op_engine() -> OperationalBrodyImagePipelineEngineV3:
    return OperationalBrodyImagePipelineEngineV3()


def test_memory_driven_tool_selection(op_engine: OperationalBrodyImagePipelineEngineV3):
    # Requirement: Memory search dynamically determines the motor tool
    tool_pen = op_engine.select_tool_from_memory("precision contour line")
    tool_brush = op_engine.select_tool_from_memory("shading regional area value fill")

    assert tool_pen == "PEN"
    assert tool_brush == "BRUSH"


def test_operational_8stage_pipeline_execution(op_engine: OperationalBrodyImagePipelineEngineV3, tmp_path: Path):
    target = NaturalVisualEducationAndObsidiaInterstackV2.render_scene_asymmetric_arch(asymmetry_offset=4)
    receipt = op_engine.run_complete_operational_pipeline(target, output_dir=tmp_path)

    assert isinstance(receipt, OperationalPipelineReceiptV3)
    assert receipt.decision_authority == DECISION_AUTHORITY
    assert receipt.native_memory_write_allowed is False

    # 1. Observation
    assert len(receipt.observation_sha256) == 64
    assert Path(receipt.artifact_paths["01_observation"]).exists()

    # 2. Representation
    assert receipt.spatial_nodes_count >= 5
    assert Path(receipt.artifact_paths["02_representation"]).exists()

    # 3. Memory Retrieval
    assert receipt.retrieved_tool == "PEN"
    assert "EXP-" in receipt.retrieved_procedure_id

    # 4. Plan
    assert receipt.plan_instructions_count == 6
    assert receipt.budget_allocated == 30.0

    # 5. Procedural Generation (Initial attempt)
    assert receipt.initial_iou >= 0.75
    assert Path(receipt.artifact_paths["03_initial_production"]).exists()

    # 6. Re-perception
    assert receipt.error_patches_count > 0
    assert receipt.primary_error_region is not None
    assert Path(receipt.artifact_paths["04_reperceived_errors"]).exists()

    # 7. Correction
    assert receipt.final_iou > receipt.initial_iou
    assert receipt.final_iou >= 0.85
    assert Path(receipt.artifact_paths["05_corrected_production"]).exists()

    # 8. Candidate Experience Receipt
    assert receipt.candidate_experience_id == "EXP-CANDIDATE-OPERATIONAL-V3"
    receipt_json_path = Path(receipt.artifact_paths["06_candidate_receipt"])
    assert receipt_json_path.exists()
    cand_data = json.loads(receipt_json_path.read_text(encoding="utf-8"))
    assert cand_data["provenance"] == "LOCAL_CANDIDATE_LEDGER"
    assert cand_data["decision_authority"] == "KX108_ONLY"
    assert cand_data["native_memory_write_allowed"] is False


def test_reconciled_32_chantiers_audit(op_engine: OperationalBrodyImagePipelineEngineV3):
    chantiers = op_engine.get_reconciled_32_chantiers_audit()
    assert len(chantiers) == 33  # Includes F00-F03, M01-M09, E01-E04, V01-V04, V04b, G01-G04, O01-O03, R01-R02, T01-T02

    codes = [c.code for c in chantiers]
    for required_code in [
        "F00", "F01", "F02", "F03",
        "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09",
        "E01", "E02", "E03", "E04",
        "V01", "V02", "V03", "V04", "V04b",
        "G01", "G02", "G03", "G04",
        "O01", "O02", "O03",
        "R01", "R02",
        "T01", "T02",
    ]:
        assert required_code in codes

    # Strict classification discipline:
    for c in chantiers:
        assert isinstance(c, MasterPlanChantierAuditEntryV3)
        assert len(c.historical_objective) > 10
        assert len(c.current_implementation) > 10
        assert len(c.proof_reference) > 5
        assert len(c.unresolved_gap) > 5
        assert c.classification in {
            "SPEC", "CODE_PRESENT", "TEST_LOCAL", "TEST_INTERPROCESS",
            "CONTRACT_COMPATIBLE", "RUNTIME_INTEGRATED", "LIVE_VERIFIED", "HOLD",
        }

    by_code = {c.code: c for c in chantiers}
    # V01 and G02 must be HOLD on portable laptop
    assert by_code["V01"].classification == "HOLD"
    assert by_code["G02"].classification == "HOLD"

    # M02 and M08 must be RUNTIME_INTEGRATED (called via sibling repo without 24/7 daemon)
    assert by_code["M02"].classification == "RUNTIME_INTEGRATED"
    assert by_code["M08"].classification == "RUNTIME_INTEGRATED"

    # E03 must be TEST_INTERPROCESS (tested via real OS subprocess)
    assert by_code["E03"].classification == "TEST_INTERPROCESS"


def test_pc_fixe_hardware_profile(op_engine: OperationalBrodyImagePipelineEngineV3):
    profile = op_engine.get_pc_fixe_hardware_profile()
    assert isinstance(profile, PCFixeHardwareProfileV3)
    assert "GTX 1050 Ti" in profile.gpu_model
    assert profile.vram_capacity_gb == 4.0
    assert "sd.cpp" in profile.recommended_engine
    assert "q4_0" in profile.quantization_format
    assert profile.zero_download_policy is True
    assert profile.status == "HOLD_PENDING_PC_FIXE_EXECUTION"
