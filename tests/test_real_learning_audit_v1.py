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


def test_controlled_comparative_budget_equal_ceilings() -> None:
    teacher = TeacherVisualCurriculumV1()
    auditor = RealLearningAuditorV1()

    bridge_img = teacher.render_exam_unseen_arched_bridge()
    res_full, _ = auditor.run_controlled_exam(
        "EXAM_ARCHED_BRIDGE", "VISIBLE_REPRODUCTION", "FULL_MULTIDIMENSIONAL_MEMORY", target_image=bridge_img
    )
    res_flat, _ = auditor.run_controlled_exam(
        "EXAM_ARCHED_BRIDGE", "VISIBLE_REPRODUCTION", "FLAT_PROCEDURAL_MEMORY", target_image=bridge_img
    )
    res_off, _ = auditor.run_controlled_exam(
        "EXAM_ARCHED_BRIDGE", "VISIBLE_REPRODUCTION", "MEMORY_DISABLED", target_image=bridge_img
    )

    # 1. Budget Ceilings strictly equal
    assert res_full.total_operations_count <= 8
    assert res_flat.total_operations_count <= 8
    assert res_off.total_operations_count <= 8
    assert res_full.total_cost_incurred <= 25.0
    assert res_flat.total_cost_incurred <= 25.0
    assert res_off.total_cost_incurred <= 25.0

    # 2. Performance hierarchy: Full M01-M09 > Flat Procedural > Memory Disabled
    assert res_full.final_iou > res_flat.final_iou
    assert res_full.final_iou > res_off.final_iou
    assert res_full.final_iou >= 0.70  # High fidelity

    # 3. Trajectory curves isolate initial recall from iterative compute
    full_curve = res_full.trajectory_curve
    off_curve = res_off.trajectory_curve
    assert len(full_curve) >= 4
    assert len(off_curve) >= 4

    # Recall advantage is already clear at step 4 before re-perception finishes
    assert full_curve[3].iou > off_curve[3].iou


def test_three_distinct_educational_evaluations() -> None:
    teacher = TeacherVisualCurriculumV1()
    auditor = RealLearningAuditorV1()

    # Exam 1: Visible reproduction (Bridge)
    bridge_img = teacher.render_exam_unseen_arched_bridge()
    res_vis, prod_vis = auditor.run_controlled_exam(
        "EXAM_ARCHED_BRIDGE", "VISIBLE_REPRODUCTION", "FULL_MULTIDIMENSIONAL_MEMORY", target_image=bridge_img
    )
    assert res_vis.evaluation_mode == "VISIBLE_REPRODUCTION"
    assert res_vis.final_iou >= 0.70
    assert prod_vis.size == (64, 64)

    # Exam 2: Occluded retention (Chalice)
    # Target image is inspected during perception, then completely removed during execution
    chalice_img = teacher.render_exam_unseen_chalice()
    res_ret, prod_ret = auditor.run_controlled_exam(
        "EXAM_CHALICE", "OCCLUDED_RETENTION", "FULL_MULTIDIMENSIONAL_MEMORY", target_image=chalice_img
    )
    assert res_ret.evaluation_mode == "OCCLUDED_RETENTION"
    assert res_ret.final_iou >= 0.60
    assert prod_ret.size == (64, 64)

    # Exam 3: Intent-only creation (Monumental Portal)
    # Zero target image provided to Brody!
    res_create, prod_create = auditor.run_controlled_exam(
        "EXAM_MONUMENTAL_PORTAL",
        "INTENT_ONLY_CREATION",
        "FULL_MULTIDIMENSIONAL_MEMORY",
        creation_intent_text="Create an architectural portal with a solid horizontal lintel spanning two vertical pillars and a curved vault",
    )
    assert res_create.evaluation_mode == "INTENT_ONLY_CREATION"
    assert res_create.target_sha256 == "INTENT_ONLY_NO_IMAGE_PROVIDED"
    assert res_create.final_iou == 1.0  # Intent satisfaction criterion
    assert len(black_pixels(prod_create)) > 100


def test_canonical_tree_associations_and_meaning_routing() -> None:
    from brody_world_physique.cognitive_memory_timeline_v1 import CANONICAL_34_TREES

    # Verify that Tree 12 is Technique and Tree 13 is Art in the canonical Obsidia stack
    assert "Technique" in CANONICAL_34_TREES["12"].name
    assert "Art" in CANONICAL_34_TREES["13"].name
    assert "Perception" in CANONICAL_34_TREES["03"].name
    assert "Action" in CANONICAL_34_TREES["20"].name
    assert "Création" in CANONICAL_34_TREES["21"].name
    assert "Mémoire" in CANONICAL_34_TREES["24"].name
    assert "Cohérence" in CANONICAL_34_TREES["26"].name

    auditor = RealLearningAuditorV1()
    teacher = TeacherVisualCurriculumV1()
    res, _ = auditor.run_controlled_exam(
        "EXAM_ARCHED_BRIDGE", "VISIBLE_REPRODUCTION", "FULL_MULTIDIMENSIONAL_MEMORY", target_image=teacher.render_exam_unseen_arched_bridge()
    )

    # Queried canonical trees must match architectural and artistic competence
    assert "03" in res.canonical_trees_queried  # Perception
    assert "12" in res.canonical_trees_queried  # Technique / tools
    assert "13" in res.canonical_trees_queried  # Art / hatching / modeling
    assert "21" in res.canonical_trees_queried  # Création
    assert "24" in res.canonical_trees_queried  # Mémoire
    assert "26" in res.canonical_trees_queried  # Cohérence

    # Meaning intents must be actively queried
    assert "HOW_DID_I_SUCCEED" in res.meaning_intents_used
    assert "WHICH_METHOD_IS_TRANSFERABLE" in res.meaning_intents_used
