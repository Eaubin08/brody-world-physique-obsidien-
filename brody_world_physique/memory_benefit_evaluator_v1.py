"""Quantitative Evaluation of Multidimensional Memory Benefit across 4 Conditions.

Evaluates and isolates the exact empirical contribution of memory on unseen visual tasks:
- C1: Sans mémoire / Sans correction (pure blank baseline)
- C2: Sans mémoire / Avec correction (cold-start search under revision budget)
- C3: Avec mémoire / Sans correction (zero-shot memory recall without motor tuning)
- C4: Avec mémoire / Avec correction (memory recall + motor tuning under identical budget)

Measures:
- Initial and final errors (pixel XOR).
- Number of applied revisions and operations breakdown (ADD, ERASE, REPLACE).
- Compute cost units (evaluations + revisions).
- Execution time in milliseconds.
- Success rate against tolerance threshold.
- Explicit decomposition: Recall benefit (C1 -> C3) vs Correction benefit (C3 -> C4).

Constitutional boundary:
- Decision authority: KX108_ONLY.
- Memory: Readonly.
- No dynamic code execution or kernel mutation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Mapping, Sequence
from PIL import Image

from .drawing_school_v0 import black_pixels
from .drawing_school_v1 import GestureV1, correct_drawing


@dataclass(frozen=True)
class ConditionEvaluationResultV1:
    """Metrics recorded for a single condition on a visual exercise."""
    condition_id: str  # C1, C2, C3, C4
    initial_error: int
    final_error: int
    revisions_count: int
    operations_count: Mapping[str, int]
    cost_units: float
    execution_time_ms: float
    success: bool
    memory_rejected: bool = False


@dataclass(frozen=True)
class ExerciseAblationBenchmarkV1:
    """Comprehensive benchmark comparing all 4 conditions on an exercise."""
    exercise_name: str
    blank_error: int
    tolerance_threshold: int
    c1_sans_mem_sans_corr: ConditionEvaluationResultV1
    c2_sans_mem_avec_corr: ConditionEvaluationResultV1
    c3_avec_mem_sans_corr: ConditionEvaluationResultV1
    c4_avec_mem_avec_corr: ConditionEvaluationResultV1
    recall_benefit_px: int  # C1 initial - C3 initial
    correction_benefit_with_mem_px: int  # C3 initial - C4 final
    correction_benefit_without_mem_px: int  # C1 initial - C2 final
    cost_reduction_units: float  # C2 cost - C4 cost
    iterations_saved: int  # C2 revisions - C4 revisions


def _evaluate_single_condition(
    condition_id: str,
    target: Image.Image,
    initial: tuple[GestureV1, ...],
    max_revisions: int,
    tolerance_threshold: int,
) -> ConditionEvaluationResultV1:
    t0 = time.perf_counter()
    outcome = correct_drawing(target, initial=initial, max_revisions=max_revisions)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    changes = outcome.get("changes", [])
    ops: dict[str, int] = {"ADD": 0, "ERASE": 0, "REPLACE": 0}
    evaluations_total = outcome.get("rejected_alternative_evaluations", 0)

    for ch in changes:
        action = ch.get("action", "")
        if action in ops:
            ops[action] += 1
        evaluations_total += ch.get("alternatives_evaluated", 0)

    # Cost model: 1.0 unit per evaluated alternative, 4.0 units per applied revision
    cost = float(evaluations_total) * 1.0 + float(len(changes)) * 4.0

    raw_err = outcome.get("raw_recall_error")
    if raw_err is None:
        raw_err = outcome.get("blank_error", 0)
    final_err = outcome["final_error"]
    success = final_err <= tolerance_threshold

    return ConditionEvaluationResultV1(
        condition_id=condition_id,
        initial_error=raw_err,
        final_error=final_err,
        revisions_count=len(changes),
        operations_count=ops,
        cost_units=round(cost, 2),
        execution_time_ms=round(elapsed_ms, 3),
        success=success,
        memory_rejected=outcome.get("memory_rejected", False),
    )


def run_comprehensive_memory_ablation(
    exercise_name: str,
    target_image: Image.Image,
    recalled_skill_gestures: tuple[GestureV1, ...],
    *,
    revision_budget: int = 12,
    tolerance_threshold: int = 50,
) -> ExerciseAblationBenchmarkV1:
    """Executes the full 4-condition benchmark on an unseen visual target."""
    truth = black_pixels(target_image.convert("L"))
    blank_err = len(truth)

    # C1: Sans mémoire / Sans correction
    c1 = _evaluate_single_condition("C1", target_image, (), 0, tolerance_threshold)
    # C2: Sans mémoire / Avec correction
    c2 = _evaluate_single_condition("C2", target_image, (), revision_budget, tolerance_threshold)
    # C3: Avec mémoire / Sans correction
    c3 = _evaluate_single_condition("C3", target_image, recalled_skill_gestures, 0, tolerance_threshold)
    # C4: Avec mémoire / Avec correction
    c4 = _evaluate_single_condition("C4", target_image, recalled_skill_gestures, revision_budget, tolerance_threshold)

    recall_benefit = c1.initial_error - c3.initial_error
    corr_benefit_with_mem = c3.initial_error - c4.final_error
    corr_benefit_without_mem = c1.initial_error - c2.final_error
    cost_saved = c2.cost_units - c4.cost_units
    iter_saved = c2.revisions_count - c4.revisions_count

    return ExerciseAblationBenchmarkV1(
        exercise_name=exercise_name,
        blank_error=blank_err,
        tolerance_threshold=tolerance_threshold,
        c1_sans_mem_sans_corr=c1,
        c2_sans_mem_avec_corr=c2,
        c3_avec_mem_sans_corr=c3,
        c4_avec_mem_avec_corr=c4,
        recall_benefit_px=recall_benefit,
        correction_benefit_with_mem_px=corr_benefit_with_mem,
        correction_benefit_without_mem_px=corr_benefit_without_mem,
        cost_reduction_units=cost_saved,
        iterations_saved=iter_saved,
    )
