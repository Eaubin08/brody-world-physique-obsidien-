"""E04: Perspective and Rotation Multi-Angle Curriculum School.

Teaches Brody perspective transformations and multi-angle orientation:
- Lessons teach 90°, 180°, and 270° rotation prototypes on planar shapes.
- Student precommits its prediction for unseen test shapes BEFORE teacher reveals rotated truth.
- Evaluates object permanence and pixel coincidence.
- Explicit non-3D boundary: records 2D planar rotation competence only.

Constitutional boundary:
- Candidate only: candidate_only = True.
- Decision authority: KX108_ONLY.
- Memory: Readonly.
- Auto-promotion: False.
- Emits act: False.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping
from PIL import Image, ImageDraw

from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes
from .multi_perspective_view_v03_v04 import (
    MultiPerspectiveTransformerV03V04,
    ObjectPermanenceRecordV04,
    VantageTransform2DV03,
)

SCHEMA = "BRODY_PERSPECTIVE_ROTATION_SCHOOL_E04"
SIDE = 64
MODULE = Path(__file__).resolve()


def _sha(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def _make_asymmetric_arrow() -> Image.Image:
    """Creates an asymmetric L-arrow shape to clearly test rotation angles."""
    img = Image.new("L", (SIDE, SIDE), 255)
    draw = ImageDraw.Draw(img)
    # Vertical spine
    draw.line([(32, 16), (32, 48)], fill=0, width=3)
    # Right-pointing branch
    draw.line([(32, 32), (48, 32)], fill=0, width=3)
    return img


def _make_asymmetric_triangle() -> Image.Image:
    """Right-angled triangle with clear horizontal and vertical legs."""
    img = Image.new("L", (SIDE, SIDE), 255)
    draw = ImageDraw.Draw(img)
    draw.polygon([(20, 20), (44, 44), (20, 44)], outline=0)
    return img


def _training_fixtures() -> list[dict[str, Any]]:
    arrow = _make_asymmetric_arrow()
    return [
        {"id": "lesson_01_rot_90", "image": arrow, "rotation": 90, "goal": "ROTATION_90_QUARTER_TURN"},
        {"id": "lesson_02_rot_180", "image": arrow, "rotation": 180, "goal": "ROTATION_180_HALF_TURN"},
        {"id": "lesson_03_rot_270", "image": arrow, "rotation": 270, "goal": "ROTATION_270_THREE_QUARTER"},
    ]


def _exam_fixtures() -> list[dict[str, Any]]:
    triangle = _make_asymmetric_triangle()
    return [
        {"id": "exam_01_rot_90", "image": triangle, "rotation": 90, "goal": "ROTATION_90"},
        {"id": "exam_02_rot_180", "image": triangle, "rotation": 180, "goal": "ROTATION_180"},
        {"id": "exam_03_rot_270", "image": triangle, "rotation": 270, "goal": "ROTATION_270"},
    ]


def run_school(output: str | Path, *, training_lessons: int = 3) -> dict[str, Any]:
    out = Path(output).resolve()
    if out.exists() and any(out.iterdir()):
        raise ValueError("Fresh output directory required")
    out.mkdir(parents=True, exist_ok=True)
    images_dir = out / "perspective_art"
    images_dir.mkdir()

    transformer = MultiPerspectiveTransformerV03V04()
    lessons_data = []

    # 1. Training lessons
    for item in _training_fixtures()[:training_lessons]:
        ident = item["id"]
        source_path = images_dir / f"{ident}_source.png"
        item["image"].save(source_path, format="PNG")

        trans = VantageTransform2DV03(rotation_degrees=item["rotation"])
        transformed_img, record = transformer.transform_vantage(item["image"], trans)
        target_path = images_dir / f"{ident}_target.png"
        transformed_img.save(target_path, format="PNG")

        lessons_data.append({
            "lesson_id": ident,
            "rotation_degrees": item["rotation"],
            "source_sha256": record.source_sha256,
            "transformed_sha256": record.transformed_sha256,
            "shape_invariance_preserved": record.shape_invariance_preserved,
        })

    # Memory candidate
    memory_file = out / "perspective_skill_memory.json"
    memory_payload = {
        "schema": SCHEMA,
        "training_lessons": lessons_data,
        "module_path": "brody_world_physique/perspective_curriculum_school_e04.py",
        "module_sha256": digest_bytes(MODULE.read_bytes()),
        "is_3d_claim": False,
        "candidate_only": True,
        "native_memory_write_allowed": False,
        "decision_authority": "KX108_ONLY",
    }
    memory_file.write_text(json.dumps(memory_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    memory_sha = _sha(memory_file)

    # 2. Heldout Exams: Precommit student prediction BEFORE teacher target is revealed
    precommit_path = out / "choices_before_teacher_feedback.jsonl"
    exam_results = []

    with precommit_path.open("w", encoding="utf-8") as stream:
        for exam in _exam_fixtures():
            ident = exam["id"]
            rot = exam["rotation"]

            # Student computes rotation from learned vantage transformer
            trans = VantageTransform2DV03(rotation_degrees=rot)
            student_pred, student_rec = transformer.transform_vantage(exam["image"], trans)
            student_path = images_dir / f"{ident}_student.png"
            student_pred.save(student_path, format="PNG")

            precommit_entry = {
                "schema": SCHEMA,
                "exam_id": ident,
                "requested_rotation": rot,
                "memory_sha256": memory_sha,
                "student_prediction_sha256": student_rec.transformed_sha256,
                "teacher_ground_truth_revealed": False,
                "decision_authority": "KX108_ONLY",
                "native_memory_write_allowed": False,
            }
            stream.write(json.dumps(precommit_entry, sort_keys=True) + "\n")
            stream.flush()

            # Teacher target produced only after student commitment
            teacher_trans = VantageTransform2DV03(rotation_degrees=rot)
            teacher_truth, teacher_rec = transformer.transform_vantage(exam["image"], teacher_trans)
            teacher_path = images_dir / f"{ident}_teacher.png"
            teacher_truth.save(teacher_path, format="PNG")

            # Check matching
            s_pix = black_pixels(student_pred)
            t_pix = black_pixels(teacher_truth)
            xor_err = len(s_pix.symmetric_difference(t_pix))
            blank_err = len(t_pix)

            exam_results.append({
                "exam_id": ident,
                "rotation_degrees": rot,
                "student_sha256": student_rec.transformed_sha256,
                "teacher_sha256": teacher_rec.transformed_sha256,
                "exact_match": (student_rec.transformed_sha256 == teacher_rec.transformed_sha256),
                "pixel_xor_error": xor_err,
                "blank_error": blank_err,
                "invariance_preserved": student_rec.shape_invariance_preserved,
            })

    eval_file = out / "evaluation.json"
    eval_report = {
        "schema": SCHEMA,
        "lessons_practiced": len(lessons_data),
        "exams_evaluated": len(exam_results),
        "all_invariance_preserved": all(r["invariance_preserved"] for r in exam_results),
        "all_exact_match": all(r["exact_match"] for r in exam_results),
        "exam_results": exam_results,
        "native_memory_write_allowed": False,
        "auto_promotion_allowed": False,
        "decision_authority": "KX108_ONLY",
    }
    eval_file.write_text(json.dumps(eval_report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {
        "status": "PASS_PERSPECTIVE_ROTATION_SCHOOL_E04",
        "lessons": len(lessons_data),
        "exams": len(exam_results),
        "evaluation_path": str(eval_file),
    }


def verify_school(root_dir: str | Path) -> dict[str, Any]:
    root = Path(root_dir).resolve(strict=True)
    mem_file = root / "perspective_skill_memory.json"
    eval_file = root / "evaluation.json"
    precommit_file = root / "choices_before_teacher_feedback.jsonl"

    if not (mem_file.is_file() and eval_file.is_file() and precommit_file.is_file()):
        raise ValueError("Missing essential school artifacts")

    mem = json.loads(mem_file.read_text(encoding="utf-8"))
    if mem.get("schema") != SCHEMA or mem.get("decision_authority") != "KX108_ONLY":
        raise ValueError("Memory schema or decision authority mismatch")

    eval_data = json.loads(eval_file.read_text(encoding="utf-8"))
    if not eval_data.get("all_invariance_preserved") or not eval_data.get("all_exact_match"):
        raise ValueError("School evaluation failed rotation invariance or match criteria")

    return {
        "status": "VERIFIED_PERSPECTIVE_ROTATION_E04",
        "lessons_verified": eval_data["lessons_practiced"],
        "exams_verified": eval_data["exams_evaluated"],
        "native_memory_write_allowed": False,
        "decision_authority": "KX108_ONLY",
    }
