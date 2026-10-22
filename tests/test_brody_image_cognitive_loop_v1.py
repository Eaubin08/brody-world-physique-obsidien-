"""Tests for BrodyImageCognitiveLoopV1 (T01: End-to-End Perception ↔ Memory ↔ Generation ↔ Evaluation)."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import pytest
from PIL import Image, ImageDraw

from brody_world_physique.brody_image_cognitive_loop_v1 import (
    BrodyCognitiveCycleReceiptV1,
    BrodyImageCognitiveLoopV1,
)
from brody_world_physique.cognitive_memory_timeline_v1 import (
    CognitiveMemoryIndexV1,
    MultiSessionMemoryJournalV1,
)
from brody_world_physique.multidimensional_retrieval_v2 import (
    MultidimensionalCognitiveMemoryEngineV1,
)
from brody_world_physique.multi_object_composer_v1 import ObjectComponentV1
from brody_world_physique.visual_intent_contracts_v1 import (
    ConstraintKindV1,
    RegionConstraintV1,
    RigorProfileV1,
    VisualEditIntentCandidateV1,
)
from brody_world_physique.v1_v4_experience_loader import (
    build_and_load_integrated_v1_v4_memory,
)

SIDE = 64


@pytest.fixture
def tmp_session_journal(tmp_path: Path) -> MultiSessionMemoryJournalV1:
    return MultiSessionMemoryJournalV1(root_dir=tmp_path)


@pytest.fixture
def populated_memory_engine() -> MultidimensionalCognitiveMemoryEngineV1:
    engine = MultidimensionalCognitiveMemoryEngineV1()
    build_and_load_integrated_v1_v4_memory(engine)
    return engine


def test_brody_cognitive_loop_full_e2e_cycle(
    populated_memory_engine: MultidimensionalCognitiveMemoryEngineV1,
    tmp_session_journal: MultiSessionMemoryJournalV1,
) -> None:
    # 1. Create target image with a box and a circle
    target_img = Image.new("L", (SIDE, SIDE), 255)
    draw = ImageDraw.Draw(target_img)
    draw.rectangle([10, 10, 26, 26], outline=0, width=3)
    draw.ellipse([34, 34, 52, 52], outline=0, width=3)

    box_img = Image.new("L", (SIDE, SIDE), 255)
    ImageDraw.Draw(box_img).rectangle([10, 10, 26, 26], outline=0, width=3)
    comp_box = ObjectComponentV1.from_image("comp_box", box_img)

    circle_img = Image.new("L", (SIDE, SIDE), 255)
    ImageDraw.Draw(circle_img).ellipse([34, 34, 52, 52], outline=0, width=3)
    comp_circle = ObjectComponentV1.from_image("comp_circle", circle_img)

    components = [comp_box, comp_circle]

    facade = BrodyImageCognitiveLoopV1(
        memory_engine=populated_memory_engine,
        journal=tmp_session_journal,
        session_id="session_e2e_test_01",
    )

    receipt = facade.execute_cycle(
        task_id="e2e_task_box_and_circle",
        target_image=target_img,
        components=components,
        max_cost_budget=50.0,
        max_correction_steps=3,
    )

    # Assertions on receipt
    assert isinstance(receipt, BrodyCognitiveCycleReceiptV1)
    assert receipt.task_id == "e2e_task_box_and_circle"
    assert receipt.decision_authority == "KX108_ONLY"
    assert receipt.is_candidate is True
    assert receipt.native_memory_write_allowed is False
    assert receipt.emits_act is False

    # Check Memory Retrieval Phase
    assert receipt.admissibility_verdict.is_admissible is True
    assert receipt.memory_retrieval_summary["meaning_results_count"] > 0
    assert "meaning_results_digest" in receipt.memory_retrieval_summary

    # Check Intent Formulation
    assert receipt.visual_intent.rigor_profile == RigorProfileV1.STRICT_GEOMETRIC
    assert len(receipt.visual_intent.region_constraints) >= 2

    # Check Heterogeneous Orchestration
    orch_receipt = receipt.initial_orchestration_receipt
    assert orch_receipt.total_steps_executed >= 2
    assert orch_receipt.successful_steps >= 2
    assert orch_receipt.total_cost_incurred > 0
    assert orch_receipt.budget_remaining >= 0

    # Check Discrepancy & Re-perception
    assert receipt.initial_discrepancy.pixel_iou > 0.0
    assert receipt.final_discrepancy.pixel_iou >= 0.50

    # Check Vantage & Object Permanence
    assert len(receipt.permanence_records) == 4  # 0, 90, 180, 270 deg
    for perm in receipt.permanence_records:
        assert perm.shape_invariance_preserved is True
        assert perm.decision_authority == "KX108_ONLY"

    # Check Crystallized Experience
    exp = receipt.crystallized_experience
    assert exp.experience_id == "exp_e2e_task_box_and_circle"
    tree_ids = [p.tree_id for p in exp.tree_projections]
    assert "03" in tree_ids
    assert "13" in tree_ids
    assert "24" in tree_ids
    assert exp.domains[0].domain.value == "DRAWING"
    assert exp.calibration.confidence_score == receipt.final_discrepancy.pixel_iou

    # Check Journal Multi-session persistence
    sessions = tmp_session_journal.load_session_history()
    assert len(sessions) == 1
    assert sessions[0]["session_id"] == "session_e2e_test_01"
    assert "exp_e2e_task_box_and_circle" in sessions[0]["experience_ids"]
    assert sessions[0]["metadata"]["success"] is True


def test_brody_cognitive_loop_localized_correction_triggered(
    populated_memory_engine: MultidimensionalCognitiveMemoryEngineV1,
) -> None:
    # Target image with a box and a circle
    target_img = Image.new("L", (SIDE, SIDE), 255)
    draw = ImageDraw.Draw(target_img)
    draw.rectangle([16, 16, 48, 48], outline=0, width=3)

    # Initial component gives a circle (which will create high discrepancy with target box)
    circle_img = Image.new("L", (SIDE, SIDE), 255)
    ImageDraw.Draw(circle_img).ellipse([16, 16, 48, 48], outline=0, width=3)
    components = [
        ObjectComponentV1.from_image("comp_circle", circle_img),
    ]

    facade = BrodyImageCognitiveLoopV1(
        memory_engine=populated_memory_engine,
        session_id="session_correction_test",
    )

    receipt = facade.execute_cycle(
        task_id="correction_task_mismatch",
        target_image=target_img,
        components=components,
        max_cost_budget=60.0,
        max_correction_steps=4,
    )

    assert receipt.correction_applied is True
    assert receipt.correction_orchestration_receipt is not None
    assert receipt.correction_orchestration_receipt.total_steps_executed > 0
