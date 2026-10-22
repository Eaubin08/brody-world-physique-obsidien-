"""Unit tests for Natural Visual Education, Educational Protocols, and Real Obsidia Interstack (V2).

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
from brody_world_physique.drawing_school_v0 import SIDE, black_pixels
from brody_world_physique.visual_intent_contracts_v1 import (
    ConstraintKindV1,
    RegionConstraintV1,
    RigorProfileV1,
    VisualEditIntentCandidateV1,
)
from brody_world_physique.natural_visual_education_and_obsidia_interstack_v2 import (
    CreationMetricsV2,
    ExamReceiptV2,
    LearningAblationComparisonReceiptV2,
    NaturalVisualEducationAndObsidiaInterstackV2,
    ObsidiaInterstackAuditReportV2,
)


@pytest.fixture
def engine() -> NaturalVisualEducationAndObsidiaInterstackV2:
    return NaturalVisualEducationAndObsidiaInterstackV2()


def test_natural_landscape_generation_and_viewpoints(engine: NaturalVisualEducationAndObsidiaInterstackV2):
    elevation = engine.render_natural_landscape_scene(view_mode="ELEVATION", add_textures=True)
    axonometric = engine.render_natural_landscape_scene(view_mode="AXONOMETRIC", add_textures=True)

    assert isinstance(elevation, Image.Image)
    assert isinstance(axonometric, Image.Image)
    assert elevation.size == (SIDE, SIDE)
    assert axonometric.size == (SIDE, SIDE)

    # Elevation and axonometric should differ in pixel structure
    assert elevation.tobytes() != axonometric.tobytes()


def test_temporal_light_evolution(engine: NaturalVisualEducationAndObsidiaInterstackV2):
    t_morning = engine.render_natural_landscape_scene(light_angle_deg=25.0)
    t_midday = engine.render_natural_landscape_scene(light_angle_deg=55.0)
    t_zenith = engine.render_natural_landscape_scene(light_angle_deg=80.0)

    # Different sun angles should produce different cast shadow profiles
    bytes_m = t_morning.tobytes()
    bytes_mid = t_midday.tobytes()
    bytes_z = t_zenith.tobytes()

    assert bytes_m != bytes_mid
    assert bytes_mid != bytes_z


def test_novel_scene_and_documented_failure(engine: NaturalVisualEducationAndObsidiaInterstackV2, tmp_path: Path):
    tower = engine.render_scene_stepped_tower()
    occlusion = engine.render_scene_severe_occlusion()

    assert len(black_pixels(tower)) > 40
    assert len(black_pixels(occlusion)) > 40

    # Overconstrained dense truss must fail under a 4-step capped budget
    receipt_fail = engine.run_exam_overconstrained_failure(output_dir=tmp_path)
    assert isinstance(receipt_fail, ExamReceiptV2)
    assert receipt_fail.is_success is False
    assert receipt_fail.failure_reason == "BUDGET_EXHAUSTED_TRUSS_INCOMPLETE"
    assert receipt_fail.operations_count == 4
    assert receipt_fail.final_iou < 0.60


def test_exam_copie_verified(engine: NaturalVisualEducationAndObsidiaInterstackV2, tmp_path: Path):
    target = engine.render_scene_asymmetric_arch(asymmetry_offset=4)
    receipt = engine.run_exam_copie(target, output_dir=tmp_path)

    assert isinstance(receipt, ExamReceiptV2)
    assert receipt.protocol == "COPIE"
    assert receipt.is_success is True
    assert receipt.final_iou >= 0.70
    assert receipt.lock_violations == 0
    assert "production" in receipt.artifact_paths
    assert Path(receipt.artifact_paths["production"]).exists()


def test_exam_retention_real_interprocess_subprocess(engine: NaturalVisualEducationAndObsidiaInterstackV2, tmp_path: Path):
    target = engine.render_scene_asymmetric_arch(asymmetry_offset=4)
    receipt = engine.run_exam_retention_interprocess(target, scratch_dir=tmp_path)

    assert isinstance(receipt, ExamReceiptV2)
    assert receipt.protocol == "RETENTION_INTERPROCESS"
    assert receipt.is_success is True
    assert receipt.final_iou >= 0.70
    assert receipt.lock_violations == 0

    # Verify that working memory schema has NO target pixels
    schema_path = Path(receipt.artifact_paths["schema"])
    assert schema_path.exists()
    schema_data = json.loads(schema_path.read_text(encoding="utf-8"))
    assert "strokes" in schema_data
    assert "target_pixels" not in schema_data
    assert "target_img" not in schema_data


def test_exam_creation_disentangled_metrics(engine: NaturalVisualEducationAndObsidiaInterstackV2, tmp_path: Path):
    base_canvas = Image.new("L", (SIDE, SIDE), 255)
    from PIL import ImageDraw
    ImageDraw.Draw(base_canvas).rectangle([8, 44, 56, 54], outline=0, width=2)

    intent = VisualEditIntentCandidateV1(
        intent_id="INTENT-CREATION-DISENTANGLED-TEST",
        goal_description="Synthesize arch superstructure in FLEX while preserving foundation in LOCK",
        rigor_profile=RigorProfileV1.STRICT_GEOMETRIC,
        region_constraints=(
            RegionConstraintV1("lock_foundation", (8, 44, 56, 54), ConstraintKindV1.LOCK, rationale="Anchor"),
            RegionConstraintV1("flex_canopy", (8, 12, 56, 44), ConstraintKindV1.FLEX, tolerance_px=100.0, rationale="Synthesis"),
        ),
    )

    receipt = engine.run_exam_creation(intent, base_canvas, output_dir=tmp_path)

    assert isinstance(receipt, ExamReceiptV2)
    assert receipt.protocol == "CREATION"
    assert receipt.is_success is True
    assert receipt.lock_violations == 0

    metrics = receipt.creation_metrics
    assert isinstance(metrics, CreationMetricsV2)
    assert metrics.intent_compliance_ratio == 1.0
    assert metrics.structural_fidelity_iou >= 0.70
    assert metrics.visual_novelty_distance >= 0.30
    assert metrics.decision_authority == DECISION_AUTHORITY


def test_learning_vs_recall_preexistence_and_3way_ablation(engine: NaturalVisualEducationAndObsidiaInterstackV2, tmp_path: Path):
    receipt = engine.run_learning_drill_and_3way_ablation(output_dir=tmp_path)

    assert isinstance(receipt, LearningAblationComparisonReceiptV2)
    assert receipt.learned_skill_existed_before is False
    assert receipt.learned_skill_acquired_after_correction is True
    assert receipt.transfer_confirmed is True

    # Under identical budgets (cost cap 30.0, 10 steps max):
    # Full multidimensional memory must strictly outperform flat procedural and zero memory
    assert receipt.full_memory_iou > receipt.flat_procedural_iou
    assert receipt.flat_procedural_iou > receipt.zero_memory_iou
    assert receipt.full_memory_corrections == 0
    assert receipt.flat_procedural_corrections > 0
    assert receipt.zero_memory_corrections >= receipt.flat_procedural_corrections


def test_obsidia_subsystem_real_interstack_v2(engine: NaturalVisualEducationAndObsidiaInterstackV2, tmp_path: Path):
    report = engine.run_obsidia_subsystem_audit(output_dir=tmp_path)

    assert isinstance(report, ObsidiaInterstackAuditReportV2)
    assert len(report.entries) == 7
    assert report.decision_authority == DECISION_AUTHORITY

    sub_by_id = {e.subsystem_id: e for e in report.entries}
    assert "OBSIDIA_CG9_PROVIDER_BINDER" in sub_by_id
    assert "OBSIDIA_BRODY_ADAPTER" in sub_by_id
    assert "JARVIS_VISUAL_OPERATOR" in sub_by_id
    assert "OBSIDIA_NATIVE_MEMORY_FLOW" in sub_by_id
    assert "OBSIDIA_SHAZAM_34_TREES" in sub_by_id
    assert "REMOTE_SOCKET_DAEMON_8081" in sub_by_id
    assert "INSTRUMENT_ORCHESTRATOR_O04" in sub_by_id

    # Sibling desktop repos must be RUNTIME_INTEGRATED
    assert sub_by_id["OBSIDIA_CG9_PROVIDER_BINDER"].classification == "RUNTIME_INTEGRATED"
    assert sub_by_id["OBSIDIA_BRODY_ADAPTER"].classification == "RUNTIME_INTEGRATED"
    assert sub_by_id["JARVIS_VISUAL_OPERATOR"].classification == "RUNTIME_INTEGRATED"
    assert sub_by_id["OBSIDIA_NATIVE_MEMORY_FLOW"].classification == "RUNTIME_INTEGRATED"
    assert sub_by_id["OBSIDIA_SHAZAM_34_TREES"].classification == "RUNTIME_INTEGRATED"

    # Instrument orchestrator is LIVE_VERIFIED
    assert sub_by_id["INSTRUMENT_ORCHESTRATOR_O04"].classification == "LIVE_VERIFIED"

    # Daemon socket 8081 is HOLD
    assert sub_by_id["REMOTE_SOCKET_DAEMON_8081"].classification == "HOLD"
    assert sub_by_id["REMOTE_SOCKET_DAEMON_8081"].hold_reason is not None

    assert (tmp_path / "obsidia_interstack_v2_report.json").exists()
