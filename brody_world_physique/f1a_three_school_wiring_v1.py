"""F1A evidence-preserving integration harness for three F0-B schools.

This executes genuine legacy APIs against a common local image corpus.
P156 remains an independent synthetic curriculum: this is NOT a unified learner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from .image_unified_continuous_school_v1 import curriculum, learn, exam
from .image_cumulative_education_p156 import run as cumulative_run
from .image_reciprocal_generation_school_v1 import (
    encode_training, reconstruct, assess,
)

def _hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _write_new(path, value):
    path = Path(path)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())

def _seal_sources(train_root, labels, exam_root):
    tasks = curriculum(train_root, labels)
    train_hashes = {task["source_sha256"] for task in tasks}
    exam_root = Path(exam_root)
    if not exam_root.is_dir():
        raise ValueError("MISSING_EXAM_DIRECTORY")
    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    exam_files = sorted(
        p for p in exam_root.rglob("*")
        if p.is_file() and p.suffix.lower() in extensions
    )
    if not exam_files:
        raise ValueError("NO_EXAM_IMAGES")
    exams = [{"relative": p.relative_to(exam_root).as_posix(),
              "sha256": _hash(p)} for p in exam_files]
    if any(item["sha256"] in train_hashes for item in exams):
        raise ValueError("TRAIN_EXAM_SOURCE_LEAK")
    return tasks, exams

def run_f1a(train_root, labels, exam_root, out, seed=156):
    """Bounded F1A smoke: actual legacy engines, separate candidate memories."""
    destination = Path(out)
    if destination.exists():
        raise ValueError("PRESERVE_PRIOR_EVIDENCE")
    # Preflight entirely precedes first output directory.
    tasks, exams = _seal_sources(train_root, labels, exam_root)
    if not isinstance(seed, int):
        raise ValueError("INVALID_SEED")
    destination.mkdir(parents=True)
    _write_new(destination / "INPUT_MANIFEST.json", {
        "train": [{"relative": x["relative"], "sha256": x["source_sha256"],
                   "teacher_identity": x["teacher_identity"]} for x in tasks],
        "exam": exams,
        "source_split_checked": True,
    })
    # Shared training observations, not shared internal state.
    courses = {}
    for item in tasks:
        courses.setdefault(item["teacher_identity"], []).append(item["file"])
    _write_new(destination / "RECIPROCAL_COURSES.json", [
        {"identity": identity, "examples": paths}
        for identity, paths in sorted(courses.items())
    ])

    local_school = learn(train_root, labels, destination / "continuous")
    recall = exam(
        destination / "continuous" / "identity_memory_candidate.json",
        exam_root, destination / "continuous_exam"
    )
    reciprocal_train = encode_training(
        destination / "RECIPROCAL_COURSES.json",
        destination / "reciprocal_memory.json"
    )
    generated = reconstruct(
        destination / "reciprocal_memory.json",
        destination / "reciprocal_prototypes"
    )
    reciprocal_exam = assess(
        destination / "reciprocal_memory.json",
        Path(exam_root), destination / "reciprocal_exam"
    )
    synthetic = cumulative_run(
        destination / "cumulative", minutes=3, seed=seed,
        lessons_each=8, feedback_each=8, validation_each=8, exam_each=20
    )
    engines = (local_school, recall, reciprocal_exam, synthetic)
    if any(x.get("native_memory_write") is not False
           or x.get("canonical_promotion") is not False
           or x.get("decision_authority") != "KX108_ONLY"
           for x in engines):
        raise ValueError("ENGINE_BOUNDARY_VIOLATION")
    if synthetic.get("learning_is_synthetic") is not True:
        raise ValueError("P156_SCOPE_UNEXPECTED")
    report = {
        "schema": "BRODY_F1A_THREE_SCHOOL_WIRING_V1",
        "continuous": local_school,
        "continuous_exam": recall,
        "reciprocal_train": reciprocal_train,
        "reciprocal_generate": generated,
        "reciprocal_exam": reciprocal_exam,
        "p156": {
            "cycles_completed": synthetic["cycles_completed"],
            "full_curriculum_completed": synthetic["full_curriculum_completed"],
            "exam_cases": synthetic["exam_cases"],
            "final_mean_error": synthetic["final_mean_error"],
        },
        "shared_visual_training_sources": True,
        "shared_physical_competence": False,
        "ball_trajectory_prediction_tested": False,
        "interruption_resume_cross_engine_tested": False,
        "unified_education_e2e": False,
        "f1_green": False,
        "verdict": "F1A_WIRING_SMOKE_ONLY",
        "native_memory_write": False,
        "canonical_promotion": False,
        "decision_authority": "KX108_ONLY",
    }
    _write_new(destination / "MASTER_REPORT.json", report)
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True)
    parser.add_argument("--labels", required=True)
    parser.add_argument("--test", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=156)
    args = parser.parse_args()
    report = run_f1a(args.train, args.labels, args.test, args.out, args.seed)
    print(json.dumps({
        "verdict": report["verdict"],
        "f1_green": report["f1_green"],
        "output": args.out,
    }, indent=2))

if __name__ == "__main__":
    main()
