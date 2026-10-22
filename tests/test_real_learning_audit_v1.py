"""Tests for real visual learning audit, transferable competence, and teacher/student separation."""
from __future__ import annotations

import json
from pathlib import Path
import pytest
from PIL import Image

from brody_world_physique.real_learning_audit_v1 import (
    AutonomousVisualFeatureExtractorV1,
    LearningAuditResultV1,
    RealLearningAuditorV1,
    TeacherVisualCurriculumV1,
    generate_learning_audit_artifacts,
)
from brody_world_physique.drawing_school_v0 import black_pixels


def test_teacher_student_separation_and_unseen_heldout_exams() -> None:
    teacher = TeacherVisualCurriculumV1()

    # 1. Private teacher generates references
    arch_img = teacher.render_lesson_arch()
    bowl_img = teacher.render_lesson_bowl()
    bridge_img = teacher.render_exam_unseen_arched_bridge()
    chalice_img = teacher.render_exam_unseen_chalice()

    assert arch_img.size == (64, 64)
    assert bowl_img.size == (64, 64)
    assert bridge_img.size == (64, 64)
    assert chalice_img.size == (64, 64)

    # 2. Brody's autonomous feature extractor inspects raw pixels without templates
    extractor = AutonomousVisualFeatureExtractorV1()
    bridge_feats = extractor.extract_features(bridge_img)

    # Bridge must be decomposed into structural sub-components
    morph_classes = [f.morphology_class for f in bridge_feats]
    assert "HORIZONTAL_SPAN" in morph_classes
    assert "VERTICAL_COLUMN" in morph_classes
    assert "CONCAVE_ARC" in morph_classes


def test_transferable_learning_audit_memory_on_vs_memory_off() -> None:
    teacher = TeacherVisualCurriculumV1()
    auditor = RealLearningAuditorV1()

    # Exam on unseen Chalice
    chalice_img = teacher.render_exam_unseen_chalice()
    res_on, prod_on = auditor.run_exam_audit("EXAM_CHALICE", chalice_img, memory_enabled=True)
    res_off, prod_off = auditor.run_exam_audit("EXAM_CHALICE", chalice_img, memory_enabled=False)

    # Invariants of transferable visual learning:
    # 1. IoU with memory must be significantly higher than memory disabled
    assert res_on.final_iou > res_off.final_iou
    # 2. XOR error with memory must be lower than memory disabled
    assert res_on.final_xor_error < res_off.final_xor_error
    # 3. Proportions error deviation with memory must be lower
    assert res_on.proportions_fidelity < res_off.proportions_fidelity
    # 4. Centroid drift with memory must be lower or equal
    assert res_on.centroid_drift_px <= res_off.centroid_drift_px
    # 5. Active retrieval of past training experiences
    assert "EXP-LESSON-ARCH-STRUCTURAL" in res_on.retrieved_experience_ids or "EXP-LESSON-BOWL-CURVILINEAR" in res_on.retrieved_experience_ids
    assert len(res_off.retrieved_experience_ids) == 0

    # Constitutional check
    assert res_on.decision_authority == "KX108_ONLY"
    assert res_on.native_memory_write_allowed is False
    assert res_on.is_candidate is True


def test_learning_audit_artifacts_generation(tmp_path: Path) -> None:
    artifacts = generate_learning_audit_artifacts(tmp_path)

    assert "training_lessons" in artifacts
    assert "unseen_exams" in artifacts
    assert "comparative_metrics" in artifacts

    # Check generated physical files
    assert (tmp_path / "train_lesson_arch.png").is_file()
    assert (tmp_path / "train_lesson_bowl.png").is_file()
    assert (tmp_path / "exam_unseen_bridge_reference.png").is_file()
    assert (tmp_path / "brody_production_bridge_memory_on.png").is_file()
    assert (tmp_path / "brody_production_bridge_memory_off.png").is_file()
    assert (tmp_path / "diff_mask_bridge_memory_on.png").is_file()
    assert (tmp_path / "audit_comparative_results.json").is_file()

    # Validate JSON content
    summary = json.loads((tmp_path / "audit_comparative_results.json").read_text(encoding="utf-8"))
    bridge_metrics = summary["comparative_metrics"]["EXAM_ARCHED_BRIDGE"]
    assert bridge_metrics["memory_on"]["final_iou"] > bridge_metrics["memory_off"]["final_iou"]
