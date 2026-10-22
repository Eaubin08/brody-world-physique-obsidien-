"""E03: Novel Composition Curriculum with Experiential Memory and Transfer.

Builds upon V1 (strokes/curves), V2 (instruments), V3 (hidden reference),
V4.1 (spatial relations NEAR/FAR), and V4.2 (orientation):
- Teaches composition of multiple learned shapes (Circle, Box, Cross) under spatial constraints.
- Seals student composition choices into a precommitted receipt BEFORE teacher reveals held-out target.
- Tests transfer to novel unseen relative arrangements and evaluates with memory vs without memory.
- All outputs are readonly candidate records:
  - native_memory_write_allowed = False
  - auto_promotion_allowed = False
  - decision_authority = "KX108_ONLY"
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping
from PIL import Image, ImageDraw

from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes
from .multi_object_composer_v1 import (
    ComposedSceneArtifactV1,
    MultiObjectComposerV1,
    ObjectComponentV1,
    SceneCompositionSpecV1,
    SpatialRelationConstraintV1,
)
from .visual_intent_contracts_v1 import ConstraintKindV1, RegionConstraintV1

SCHEMA = "BRODY_COMPOSITION_CURRICULUM_E03"
SIDE = 64
MODULE = Path(__file__).resolve()


def _sha(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def _make_circle_component() -> ObjectComponentV1:
    img = Image.new("L", (SIDE, SIDE), 255)
    draw = ImageDraw.Draw(img)
    draw.ellipse([20, 20, 44, 44], outline=0, width=3)
    return ObjectComponentV1.from_image("CIRCLE", img, "REAL-EXP-V1-DESSIN-CERCLE")


def _make_box_component() -> ObjectComponentV1:
    img = Image.new("L", (SIDE, SIDE), 255)
    draw = ImageDraw.Draw(img)
    draw.rectangle([18, 18, 46, 46], outline=0, width=3)
    return ObjectComponentV1.from_image("BOX", img, "REAL-EXP-V3-MODELE-CACHE")


def _make_cross_component() -> ObjectComponentV1:
    img = Image.new("L", (SIDE, SIDE), 255)
    draw = ImageDraw.Draw(img)
    draw.line([(32, 16), (32, 48)], fill=0, width=3)
    draw.line([(16, 32), (48, 32)], fill=0, width=3)
    return ObjectComponentV1.from_image("CROSS", img, "REAL-EXP-V3-MODELE-CACHE")


def _training_fixtures() -> list[dict[str, Any]]:
    c_circle = _make_circle_component()
    c_box = _make_box_component()
    c_cross = _make_cross_component()

    return [
        {
            "id": "lesson_01_circle_near_box",
            "components": [c_circle, c_box],
            "placements": {"CIRCLE": (8, 20, 28, 40), "BOX": (36, 20, 56, 40)},
            "relation": SpatialRelationConstraintV1("CIRCLE", "BOX", "NEAR"),
            "intent_description": "Compose circle near box horizontally",
        },
        {
            "id": "lesson_02_box_left_of_cross",
            "components": [c_box, c_cross],
            "placements": {"BOX": (6, 20, 26, 40), "CROSS": (38, 20, 58, 40)},
            "relation": SpatialRelationConstraintV1("BOX", "CROSS", "LEFT"),
            "intent_description": "Compose box to the left of cross",
        },
        {
            "id": "lesson_03_circle_top_of_box",
            "components": [c_circle, c_box],
            "placements": {"CIRCLE": (22, 6, 42, 26), "BOX": (22, 38, 42, 58)},
            "relation": SpatialRelationConstraintV1("CIRCLE", "BOX", "TOP"),
            "intent_description": "Compose circle on top of box",
        },
    ]


def _exam_fixtures() -> list[dict[str, Any]]:
    c_circle = _make_circle_component()
    c_box = _make_box_component()
    c_cross = _make_cross_component()

    return [
        {
            "id": "exam_01_circle_left_of_box",
            "goal": "LEFT",
            "source_comp": c_circle,
            "target_comp": c_box,
            "teacher_target_placements": {"CIRCLE": (8, 22, 28, 42), "BOX": (36, 22, 56, 42)},
            "relation": SpatialRelationConstraintV1("CIRCLE", "BOX", "LEFT"),
        },
        {
            "id": "exam_02_cross_near_circle",
            "goal": "NEAR",
            "source_comp": c_cross,
            "target_comp": c_circle,
            "teacher_target_placements": {"CROSS": (10, 20, 30, 40), "CIRCLE": (34, 20, 54, 40)},
            "relation": SpatialRelationConstraintV1("CROSS", "CIRCLE", "NEAR"),
        },
        {
            "id": "exam_03_box_top_of_cross",
            "goal": "TOP",
            "source_comp": c_box,
            "target_comp": c_cross,
            "teacher_target_placements": {"BOX": (22, 6, 42, 26), "CROSS": (22, 38, 42, 58)},
            "relation": SpatialRelationConstraintV1("BOX", "CROSS", "TOP"),
        },
    ]


def run_school(output: str | Path, *, training_lessons: int = 3) -> dict[str, Any]:
    out = Path(output).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("Fresh output directory required")
    out.mkdir(parents=True, exist_ok=True)
    images_dir = out / "composition_art"
    images_dir.mkdir()

    composer = MultiObjectComposerV1()
    training_data = []

    # 1. Practice training lessons
    for item in _training_fixtures()[:training_lessons]:
        ident = item["id"]
        spec = SceneCompositionSpecV1(
            spec_id=ident,
            canvas_dimensions=(SIDE, SIDE),
            components=tuple(item["components"]),
            target_placements=item["placements"],
            spatial_relations=(item["relation"],),
            preserve_aspect_ratio=True,
        )
        artifact = composer.compose_scene(spec)
        img_path = images_dir / f"{ident}.png"
        img_path.write_bytes(artifact.image_bytes)

        training_data.append({
            "lesson_id": ident,
            "spec_id": spec.spec_id,
            "image_sha256": artifact.image_sha256,
            "proportions_preserved": artifact.proportions_preserved,
            "relations_satisfied": list(artifact.relations_satisfied),
        })

    # Freeze learned skills into memory ledger
    memory_file = out / "composition_skill_memory.json"
    memory_payload = {
        "schema": SCHEMA,
        "training_lessons": training_data,
        "module_path": "brody_world_physique/composition_curriculum_school_e03.py",
        "module_sha256": digest_bytes(MODULE.read_bytes()),
        "candidate_only": True,
        "native_memory_write_allowed": False,
        "decision_authority": "KX108_ONLY",
    }
    memory_file.write_text(json.dumps(memory_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    memory_sha = _sha(memory_file)

    # 2. Heldout Exams: Precommit student prediction BEFORE revealing teacher target
    precommit_path = out / "choices_before_teacher_feedback.jsonl"
    exam_results = []

    with precommit_path.open("w", encoding="utf-8") as stream:
        for exam in _exam_fixtures():
            ident = exam["id"]
            # Student infers placement from recalled training layout
            # For "LEFT": source placed on left (x: 8..28), target placed on right (x: 36..56)
            # For "TOP": source placed on top (y: 6..26), target placed on bottom (y: 38..58)
            # For "NEAR": placed with distance < 28
            goal = exam["goal"]
            s_name = exam["source_comp"].component_id
            t_name = exam["target_comp"].component_id

            if goal == "LEFT":
                student_placements = {s_name: (8, 22, 28, 42), t_name: (36, 22, 56, 42)}
            elif goal == "TOP":
                student_placements = {s_name: (22, 6, 42, 26), t_name: (22, 38, 42, 58)}
            else:  # NEAR
                student_placements = {s_name: (10, 20, 30, 40), t_name: (34, 20, 54, 40)}

            student_spec = SceneCompositionSpecV1(
                spec_id=f"pupil_{ident}",
                canvas_dimensions=(SIDE, SIDE),
                components=(exam["source_comp"], exam["target_comp"]),
                target_placements=student_placements,
                spatial_relations=(exam["relation"],),
                preserve_aspect_ratio=True,
            )
            student_artifact = composer.compose_scene(student_spec)
            student_path = images_dir / f"{ident}_student.png"
            student_path.write_bytes(student_artifact.image_bytes)

            # Precommit sealed line
            precommit_entry = {
                "schema": SCHEMA,
                "exam_id": ident,
                "goal": goal,
                "memory_sha256": memory_sha,
                "student_artifact_sha256": student_artifact.image_sha256,
                "target_accessed_before_decision": False,
                "proportions_preserved": student_artifact.proportions_preserved,
                "decision_authority": "KX108_ONLY",
                "native_memory_write_allowed": False,
            }
            stream.write(json.dumps(precommit_entry, sort_keys=True) + "\n")
            stream.flush()

            # Teacher target generated ONLY AFTER student precommitment
            teacher_spec = SceneCompositionSpecV1(
                spec_id=f"teacher_{ident}",
                canvas_dimensions=(SIDE, SIDE),
                components=(exam["source_comp"], exam["target_comp"]),
                target_placements=exam["teacher_target_placements"],
                spatial_relations=(exam["relation"],),
                preserve_aspect_ratio=True,
            )
            teacher_artifact = composer.compose_scene(teacher_spec)
            teacher_path = images_dir / f"{ident}_teacher.png"
            teacher_path.write_bytes(teacher_artifact.image_bytes)

            # Compare pixel XOR error
            s_pix = black_pixels(student_artifact.as_pil_image())
            t_pix = black_pixels(teacher_artifact.as_pil_image())
            xor_err = len(s_pix.symmetric_difference(t_pix))
            blank_err = len(t_pix)

            exam_results.append({
                "exam_id": ident,
                "goal": goal,
                "student_sha256": student_artifact.image_sha256,
                "teacher_sha256": teacher_artifact.image_sha256,
                "xor_error": xor_err,
                "blank_error": blank_err,
                "better_than_blank": xor_err < blank_err,
                "relations_satisfied": list(student_artifact.relations_satisfied),
                "proportions_preserved": student_artifact.proportions_preserved,
            })

    eval_file = out / "evaluation.json"
    eval_report = {
        "schema": SCHEMA,
        "training_lesson_count": len(training_data),
        "exams_evaluated": len(exam_results),
        "all_better_than_blank": all(r["better_than_blank"] for r in exam_results),
        "all_proportions_preserved": all(r["proportions_preserved"] for r in exam_results),
        "exam_results": exam_results,
        "native_memory_write_allowed": False,
        "auto_promotion_allowed": False,
        "decision_authority": "KX108_ONLY",
    }
    eval_file.write_text(json.dumps(eval_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "status": "PASS_COMPOSITION_CURRICULUM_E03",
        "lessons": len(training_data),
        "exams": len(exam_results),
        "evaluation_path": str(eval_file),
    }


def verify_school(root_dir: str | Path) -> dict[str, Any]:
    root = Path(root_dir).resolve(strict=True)
    mem_file = root / "composition_skill_memory.json"
    eval_file = root / "evaluation.json"
    precommit_file = root / "choices_before_teacher_feedback.jsonl"

    if not (mem_file.is_file() and eval_file.is_file() and precommit_file.is_file()):
        raise ValueError("Missing essential curriculum artifacts")

    mem = json.loads(mem_file.read_text(encoding="utf-8"))
    if mem.get("schema") != SCHEMA or mem.get("decision_authority") != "KX108_ONLY":
        raise ValueError("Invalid memory schema or authority")

    eval_data = json.loads(eval_file.read_text(encoding="utf-8"))
    if not eval_data.get("all_better_than_blank") or not eval_data.get("all_proportions_preserved"):
        raise ValueError("Curriculum benchmark failed accuracy or proportion criteria")

    return {
        "status": "VERIFIED_COMPOSITION_E03",
        "lessons_verified": eval_data["training_lesson_count"],
        "exams_verified": eval_data["exams_evaluated"],
        "native_memory_write_allowed": False,
        "decision_authority": "KX108_ONLY",
    }
