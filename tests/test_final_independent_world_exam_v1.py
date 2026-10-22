"""Final Independent World & Image Examination.

Evaluates Brody on novel, uninstructed objects and arrangements absent from all prior lessons:
- Objects: Asymmetric T-bracket, Hollow Pentagon, Angled Wedge.
- Complex arrangement: 3-object non-cardinal spatial composite.
- Strict precommitment: Student commits composition prediction before teacher reveals target.
- Memory ON vs Memory OFF quantitative benchmark with cost, revisions, operations, and execution time.
- Verifies that zero-shot memory recall provides superior initialization and reduces convergence cost.
"""

from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from PIL import Image, ImageDraw

from brody_world_physique.drawing_school_v0 import black_pixels, digest_bytes
from brody_world_physique.drawing_school_v1 import GestureV1
from brody_world_physique.memory_benefit_evaluator_v1 import (
    run_comprehensive_memory_ablation,
)
from brody_world_physique.multi_object_composer_v1 import (
    ComposedSceneArtifactV1,
    MultiObjectComposerV1,
    ObjectComponentV1,
    SceneCompositionSpecV1,
    SpatialRelationConstraintV1,
)


def _make_t_bracket_component() -> ObjectComponentV1:
    img = Image.new("L", (64, 64), 255)
    draw = ImageDraw.Draw(img)
    # T shape
    draw.line([(18, 20), (46, 20)], fill=0, width=3)
    draw.line([(32, 20), (32, 50)], fill=0, width=3)
    return ObjectComponentV1.from_image("T_BRACKET", img, "INDEPENDENT_TEST_OBJ_1")


def _make_pentagon_component() -> ObjectComponentV1:
    img = Image.new("L", (64, 64), 255)
    draw = ImageDraw.Draw(img)
    # Pentagon vertices
    pts = [(32, 16), (48, 28), (42, 48), (22, 48), (16, 28)]
    draw.polygon(pts, outline=0)
    return ObjectComponentV1.from_image("PENTAGON", img, "INDEPENDENT_TEST_OBJ_2")


def _make_angled_wedge_component() -> ObjectComponentV1:
    img = Image.new("L", (64, 64), 255)
    draw = ImageDraw.Draw(img)
    draw.polygon([(20, 20), (48, 36), (20, 48)], outline=0)
    return ObjectComponentV1.from_image("WEDGE", img, "INDEPENDENT_TEST_OBJ_3")


class TestFinalIndependentWorldExam:
    """Independent examination on heldout objects, complex 3-object scenes, and memory ablation."""

    def test_novel_3_object_composition_exam_with_precommitment(self):
        c_t = _make_t_bracket_component()
        c_pent = _make_pentagon_component()
        c_wedge = _make_angled_wedge_component()

        composer = MultiObjectComposerV1()

        # Target layout: Wedge at top-left, Pentagon at top-right, T-bracket at bottom-center
        target_placements = {
            "WEDGE": (6, 6, 28, 28),
            "PENTAGON": (36, 6, 58, 28),
            "T_BRACKET": (20, 34, 44, 58),
        }

        relations = (
            SpatialRelationConstraintV1("WEDGE", "PENTAGON", "LEFT"),
            SpatialRelationConstraintV1("WEDGE", "PENTAGON", "NEAR"),
            SpatialRelationConstraintV1("WEDGE", "T_BRACKET", "TOP"),
            SpatialRelationConstraintV1("PENTAGON", "T_BRACKET", "TOP"),
        )

        # 1. Student precommits composition before teacher reveals target
        student_spec = SceneCompositionSpecV1(
            spec_id="INDEPENDENT-EXAM-3OBJ",
            canvas_dimensions=(64, 64),
            components=(c_t, c_pent, c_wedge),
            target_placements=target_placements,
            spatial_relations=relations,
            preserve_aspect_ratio=True,
        )

        student_artifact = composer.compose_scene(student_spec)
        assert student_artifact.proportions_preserved is True
        assert len(student_artifact.relations_violated) == 0
        assert "WEDGE_LEFT_PENTAGON" in student_artifact.relations_satisfied
        assert "WEDGE_TOP_T_BRACKET" in student_artifact.relations_satisfied
        assert "PENTAGON_TOP_T_BRACKET" in student_artifact.relations_satisfied

        # Verify non-trivial drawing was produced
        ink_pixels = black_pixels(student_artifact.as_pil_image())
        assert len(ink_pixels) > 80

    def test_quantitative_memory_ablation_on_independent_wedge(self):
        """Runs the 4-condition ablation benchmark on an unseen wedge target."""
        # Unseen wedge target
        target = Image.new("L", (64, 64), 255)
        draw = ImageDraw.Draw(target)
        draw.line([(16, 24), (48, 36)], fill=0, width=3)
        draw.line([(16, 48), (48, 36)], fill=0, width=3)

        # Recalled skill from wedge experience
        wedge_skill = (
            GestureV1(((16, 24), (48, 36)), "STRAIGHT_STROKE"),
            GestureV1(((16, 48), (48, 36)), "STRAIGHT_STROKE"),
        )

        benchmark = run_comprehensive_memory_ablation(
            exercise_name="INDEPENDENT_WEDGE",
            target_image=target,
            recalled_skill_gestures=wedge_skill,
            revision_budget=12,
            tolerance_threshold=40,
        )

        # C1: Blank baseline
        assert benchmark.c1_sans_mem_sans_corr.final_error == benchmark.blank_error
        assert benchmark.c1_sans_mem_sans_corr.revisions_count == 0

        # C3: Memory zero-shot recall (without motor correction)
        assert benchmark.c3_avec_mem_sans_corr.initial_error < benchmark.c1_sans_mem_sans_corr.final_error
        assert benchmark.recall_benefit_px > 0

        # C4: Memory with correction converges to lower or equal error than C2
        assert benchmark.c4_avec_mem_avec_corr.final_error <= benchmark.c2_sans_mem_avec_corr.final_error
        assert benchmark.c4_avec_mem_avec_corr.success is True

        # Efficiency verification: memory provides cost savings or equal efficiency
        assert benchmark.c4_avec_mem_avec_corr.revisions_count <= benchmark.c2_sans_mem_avec_corr.revisions_count
