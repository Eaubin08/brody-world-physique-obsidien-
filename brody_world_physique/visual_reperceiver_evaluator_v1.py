"""G04: Visual Re-perceiver, Error Localizer, and Correction Proposer.

Closes the perception ↔ representation ↔ generation ↔ evaluation loop:
1. Re-observes a created / generated / edited canvas.
2. Evaluates LOCK / FLEX / IGNORE constraints.
3. Detects and isolates localized error patches (diff mask, unwanted ink in locked zones, missing ink).
4. Proposes bounded corrective tool actions (ERASE_REGION, DRAW_STROKE) without executing unverified code.

Constitutional boundary:
- Candidate only: is_candidate = True.
- Decision authority: KX108_ONLY.
- Memory: readonly = True, native_memory_write_allowed = False.
- Emits act: False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from types import MappingProxyType
from typing import Any, Mapping, Sequence
from PIL import Image

from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes
from .visual_intent_contracts_v1 import (
    ConstraintKindV1,
    VisualComplianceReportV1,
    VisualEditIntentCandidateV1,
)


@dataclass(frozen=True)
class ErrorPatchV1:
    """Localized spatial error patch discovered during re-perception."""
    patch_id: str
    error_kind: str  # "UNWANTED_INK_IN_LOCK_ZONE", "MISSING_INK_IN_REQUIRED_ZONE", "FLEX_TOLERANCE_EXCEEDED"
    bbox_xyxy: tuple[int, int, int, int]
    pixel_count: int
    severity: float  # [0.0, 1.0]
    suggested_action: str  # "ERASE_REGION", "DRAW_STROKE", "REVERT_STEP"
    suggested_arguments: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not (0.0 <= self.severity <= 1.0):
            raise ValueError("severity must be between 0.0 and 1.0")


@dataclass(frozen=True)
class ReperceptionEvaluationReportV1:
    """Audit report from re-observing a canvas against intent and reference."""
    report_id: str
    canvas_sha256: str
    reference_sha256: str | None
    total_ink_pixels: int
    compliance_report: VisualComplianceReportV1
    error_patches: tuple[ErrorPatchV1, ...]
    requires_correction: bool
    suggested_correction_steps: tuple[dict[str, Any], ...]
    decision_authority: str = "KX108_ONLY"
    native_memory_write_allowed: bool = False
    is_candidate: bool = True


class VisualReperceiverEvaluatorV1:
    """Re-perceives created images, localizes errors, and formulates correction proposals."""

    def evaluate_and_locate_errors(
        self,
        current_canvas: Image.Image,
        intent: VisualEditIntentCandidateV1,
        *,
        reference_before: Image.Image | None = None,
        ideal_target: Image.Image | None = None,
    ) -> ReperceptionEvaluationReportV1:
        cur_gray = current_canvas.convert("L")
        w, h = cur_gray.size
        cur_ink = black_pixels(cur_gray)
        cur_sha = digest_bytes(cur_gray.tobytes())

        ref_img = reference_before.convert("L") if reference_before else Image.new("L", (w, h), 255)
        ref_sha = digest_bytes(ref_img.tobytes()) if reference_before else None

        # 1. Evaluate compliance against declared intent
        compliance = intent.check_compliance(ref_img, cur_gray)

        error_patches: list[ErrorPatchV1] = []
        correction_steps: list[dict[str, Any]] = []

        cur_pix = cur_gray.load()
        ref_pix = ref_img.load()

        # 2. Localize errors in region constraints
        for idx, rc in enumerate(intent.region_constraints):
            x0, y0, x1, y1 = rc.bbox_xyxy
            unwanted_pixels: list[tuple[int, int]] = []

            for y in range(y0, y1):
                for x in range(x0, x1):
                    # Check intruder ink where reference was clean
                    if rc.constraint_kind == ConstraintKindV1.LOCK:
                        if cur_pix[x, y] < 128 and ref_pix[x, y] >= 128:
                            unwanted_pixels.append((x, y))

            if rc.constraint_kind == ConstraintKindV1.LOCK and unwanted_pixels:
                unwanted_indices = {y * w + x for (x, y) in unwanted_pixels}
                p_box = bbox_of(unwanted_indices)
                patch = ErrorPatchV1(
                    patch_id=f"ERR-LOCK-{rc.region_id}-{idx}",
                    error_kind="UNWANTED_INK_IN_LOCK_ZONE",
                    bbox_xyxy=p_box,
                    pixel_count=len(unwanted_pixels),
                    severity=min(1.0, len(unwanted_pixels) / 50.0),
                    suggested_action="ERASE_REGION",
                    suggested_arguments={
                        "x0": p_box[0],
                        "y0": p_box[1],
                        "x1": p_box[2] + 1,
                        "y1": p_box[3] + 1,
                    },
                )
                error_patches.append(patch)
                correction_steps.append({
                    "step_index": len(correction_steps),
                    "capability": "ERASE_REGION",
                    "arguments": patch.suggested_arguments,
                    "target_patch_id": patch.patch_id,
                })

        # 3. If ideal target is provided, inspect for missing strokes
        if ideal_target:
            target_gray = ideal_target.convert("L")
            tgt_ink = black_pixels(target_gray)
            missing = tgt_ink - cur_ink
            if len(missing) > 10:
                m_box = bbox_of(missing)
                patch = ErrorPatchV1(
                    patch_id="ERR-MISSING-TARGET-INK",
                    error_kind="MISSING_INK_IN_REQUIRED_ZONE",
                    bbox_xyxy=m_box,
                    pixel_count=len(missing),
                    severity=min(1.0, len(missing) / 100.0),
                    suggested_action="DRAW_STROKE",
                    suggested_arguments={
                        "points": [
                            ((m_box[0] + m_box[2]) // 2, m_box[1]),
                            ((m_box[0] + m_box[2]) // 2, m_box[3]),
                        ],
                        "kind": "STRAIGHT_STROKE",
                        "width": 3,
                    },
                )
                error_patches.append(patch)
                correction_steps.append({
                    "step_index": len(correction_steps),
                    "capability": "DRAW_STROKE",
                    "arguments": patch.suggested_arguments,
                    "target_patch_id": patch.patch_id,
                })

        needs_corr = len(error_patches) > 0 or not compliance.compliant

        return ReperceptionEvaluationReportV1(
            report_id=f"REPERC-{intent.intent_id}",
            canvas_sha256=cur_sha,
            reference_sha256=ref_sha,
            total_ink_pixels=len(cur_ink),
            compliance_report=compliance,
            error_patches=tuple(error_patches),
            requires_correction=needs_corr,
            suggested_correction_steps=tuple(correction_steps),
        )
