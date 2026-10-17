"""O01: Bounded Instrument Orchestrator without Arbitrary Code Execution.

Coordinates visual instruments (drawing, erasing, instrument styling, pixel inspection)
through explicit, precommitted declarative steps in Python.
Reuses Obsidure / Binder patterns:
- Static catalog of allowed capabilities.
- Bounded step execution (MAX_STEPS = 64).
- Deterministic receipts for every step with SHA-256 before/after state.
- Rollback mechanism if a LOCK constraint is violated.
- Strictly forbids arbitrary string execution (no eval, no exec, no shell).

Constitutional boundary:
- Decision authority: KX108_ONLY.
- Readonly candidate ledger: native_memory_write_allowed = False.
- Auto promotion: False.
- Emits act: False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence
from PIL import Image, ImageDraw

from .drawing_school_v0 import black_pixels, digest_bytes
from .drawing_school_v1 import GestureV1, render
from .instrument_school_v2 import render_instrument, TOOLS
from .visual_intent_contracts_v1 import (
    ConstraintKindV1,
    VisualComplianceReportV1,
    VisualEditIntentCandidateV1,
)

MAX_STEPS = 64
CANVAS_SIDE = 64

ALLOWED_CAPABILITIES = frozenset({
    "INSPECT_PIXELS",
    "DRAW_STROKE",
    "ERASE_REGION",
    "REPLACE_STROKE",
    "SELECT_TOOL",
    "APPLY_INSTRUMENT",
    "EVALUATE_LOSS",
    "REVERT_STEP",
})


@dataclass(frozen=True)
class ToolExecutionStepV1:
    """A single declarative step in a tool plan."""
    step_index: int
    capability: str
    arguments: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.capability not in ALLOWED_CAPABILITIES:
            raise ValueError(f"Disallowed tool capability: {self.capability}. Must be in {ALLOWED_CAPABILITIES}")
        if self.step_index < 0:
            raise ValueError("step_index must be non-negative")


@dataclass(frozen=True)
class ToolExecutionReceiptV1:
    """Immutable receipt certifying the execution of a bounded step."""
    step_index: int
    capability: str
    status: str
    canvas_before_sha256: str
    canvas_after_sha256: str
    reverted: bool = False
    failure_reason: str | None = None
    details: Mapping[str, Any] = field(default_factory=dict)
    decision_authority: str = "KX108_ONLY"


@dataclass(frozen=True)
class OrchestrationPlanV1:
    """Bounded plan containing an ordered sequence of declarative steps."""
    plan_id: str
    steps: tuple[ToolExecutionStepV1, ...]
    max_steps_allowed: int = MAX_STEPS
    decision_authority: str = "KX108_ONLY"

    def __post_init__(self) -> None:
        if len(self.steps) > self.max_steps_allowed:
            raise ValueError(f"Plan exceeds max steps: {len(self.steps)} > {self.max_steps_allowed}")
        if self.decision_authority != "KX108_ONLY":
            raise ValueError("Decision authority must be KX108_ONLY")


@dataclass(frozen=True)
class OrchestrationReceiptV1:
    """Final summary receipt of the orchestrated plan execution."""
    plan_id: str
    total_steps_executed: int
    successful_steps: int
    reverted_steps: int
    failed_steps: int
    final_canvas_sha256: str
    compliance_report: VisualComplianceReportV1 | None
    step_receipts: tuple[ToolExecutionReceiptV1, ...]
    decision_authority: str = "KX108_ONLY"
    native_memory_write_allowed: bool = False
    auto_promotion_allowed: bool = False


class BoundedInstrumentOrchestratorV1:
    """Bounded executor for visual instruments and drawing steps."""

    def __init__(self, initial_canvas: Image.Image | None = None) -> None:
        if initial_canvas is None:
            self._canvas = Image.new("L", (CANVAS_SIDE, CANVAS_SIDE), 255)
        else:
            self._canvas = initial_canvas.convert("L").copy()
            if self._canvas.size != (CANVAS_SIDE, CANVAS_SIDE):
                raise ValueError(f"Canvas must be {CANVAS_SIDE}x{CANVAS_SIDE}")

        self._checkpoints: list[Image.Image] = [self._canvas.copy()]
        self._step_receipts: list[ToolExecutionReceiptV1] = []
        self._current_strokes: list[GestureV1] = []
        self._current_tool: str = "PEN"

    @property
    def canvas(self) -> Image.Image:
        return self._canvas.copy()

    @property
    def canvas_sha256(self) -> str:
        return digest_bytes(self._canvas.tobytes())

    def execute_plan(
        self,
        plan: OrchestrationPlanV1,
        intent: VisualEditIntentCandidateV1 | None = None,
    ) -> OrchestrationReceiptV1:
        """Executes plan steps within bounds and evaluates compliance against visual intent."""
        successful = 0
        reverted = 0
        failed = 0

        for step in plan.steps:
            if len(self._step_receipts) >= plan.max_steps_allowed:
                self._record_failure(step, "MAX_BUDGET_EXCEEDED")
                failed += 1
                break

            receipt = self._execute_step(step, intent)
            self._step_receipts.append(receipt)

            if receipt.status == "SUCCESS":
                successful += 1
            elif receipt.reverted:
                reverted += 1
            else:
                failed += 1

        compliance = None
        if intent is not None and self._checkpoints:
            compliance = intent.check_compliance(self._checkpoints[0], self._canvas)

        return OrchestrationReceiptV1(
            plan_id=plan.plan_id,
            total_steps_executed=len(self._step_receipts),
            successful_steps=successful,
            reverted_steps=reverted,
            failed_steps=failed,
            final_canvas_sha256=self.canvas_sha256,
            compliance_report=compliance,
            step_receipts=tuple(self._step_receipts),
        )

    def _execute_step(
        self,
        step: ToolExecutionStepV1,
        intent: VisualEditIntentCandidateV1 | None,
    ) -> ToolExecutionReceiptV1:
        before_sha = self.canvas_sha256
        before_img = self._canvas.copy()

        # Execute capability safely
        try:
            details = self._dispatch_capability(step)
        except Exception as exc:
            return ToolExecutionReceiptV1(
                step_index=step.step_index,
                capability=step.capability,
                status="STEP_EXECUTION_EXCEPTION",
                canvas_before_sha256=before_sha,
                canvas_after_sha256=before_sha,
                reverted=False,
                failure_reason=str(exc),
            )

        after_sha = self.canvas_sha256

        # Check for LOCK violations if intent is provided
        if intent is not None:
            compliance = intent.check_compliance(before_img, self._canvas)
            if compliance.lock_violations:
                # Rollback step
                self._canvas = before_img
                return ToolExecutionReceiptV1(
                    step_index=step.step_index,
                    capability=step.capability,
                    status="REJECTED_LOCK_VIOLATION",
                    canvas_before_sha256=before_sha,
                    canvas_after_sha256=before_sha,
                    reverted=True,
                    failure_reason="; ".join(compliance.lock_violations),
                    details=details,
                )

        # Successful step, save checkpoint
        self._checkpoints.append(self._canvas.copy())
        return ToolExecutionReceiptV1(
            step_index=step.step_index,
            capability=step.capability,
            status="SUCCESS",
            canvas_before_sha256=before_sha,
            canvas_after_sha256=after_sha,
            reverted=False,
            details=details,
        )

    def _dispatch_capability(self, step: ToolExecutionStepV1) -> dict[str, Any]:
        cap = step.capability
        args = step.arguments

        if cap == "INSPECT_PIXELS":
            pixels = black_pixels(self._canvas)
            return {
                "black_pixel_count": len(pixels),
                "is_blank": len(pixels) == 0,
            }

        elif cap == "DRAW_STROKE":
            raw_pts = args.get("points", ())
            pts = tuple(tuple(int(c) for c in p) for p in raw_pts)
            raw_kind = str(args.get("kind", "STRAIGHT_STROKE")).upper()
            if raw_kind in ("LINE", "STRAIGHT", "STRAIGHT_STROKE"):
                kind = "STRAIGHT_STROKE"
            elif raw_kind in ("CURVE", "CURVED", "CURVED_STROKE"):
                kind = "CURVED_STROKE"
            else:
                kind = "STRAIGHT_STROKE"
            width = int(args.get("width", 3))
            gesture = GestureV1(points=pts, kind=kind)
            self._current_strokes.append(gesture)

            draw = ImageDraw.Draw(self._canvas)
            if len(pts) >= 2:
                draw.line(pts, fill=0, width=width, joint="curve")
            return {
                "points_count": len(pts),
                "stroke_kind": kind,
                "total_strokes": len(self._current_strokes),
            }

        elif cap == "ERASE_REGION":
            x0 = int(args.get("x0", 0))
            y0 = int(args.get("y0", 0))
            x1 = int(args.get("x1", CANVAS_SIDE))
            y1 = int(args.get("y1", CANVAS_SIDE))
            draw = ImageDraw.Draw(self._canvas)
            draw.rectangle([x0, y0, x1, y1], fill=255)
            return {"erased_bbox": [x0, y0, x1, y1]}

        elif cap == "SELECT_TOOL":
            tool = str(args.get("tool", "PEN")).upper()
            if tool not in TOOLS:
                raise ValueError(f"Unknown tool {tool}. Must be one of {TOOLS}")
            self._current_tool = tool
            return {"selected_tool": tool}

        elif cap == "APPLY_INSTRUMENT":
            if self._current_strokes:
                rendered = render_instrument(tuple(self._current_strokes), self._current_tool)
                self._canvas = rendered.convert("L")
            return {
                "instrument_applied": self._current_tool,
                "strokes_rendered": len(self._current_strokes),
            }

        elif cap == "EVALUATE_LOSS":
            ref_path = args.get("reference_path")
            if ref_path and Path(ref_path).is_file():
                with Image.open(ref_path) as ref_img:
                    ref_px = black_pixels(ref_img.convert("L"))
                    cur_px = black_pixels(self._canvas)
                    xor_loss = len(ref_px.symmetric_difference(cur_px))
                    return {"pixel_xor_loss": xor_loss, "reference_black": len(ref_px)}
            return {"pixel_black_count": len(black_pixels(self._canvas))}

        elif cap == "REVERT_STEP":
            if len(self._checkpoints) > 1:
                self._checkpoints.pop()
                self._canvas = self._checkpoints[-1].copy()
                return {"reverted_to_checkpoint_index": len(self._checkpoints) - 1}
            return {"revert_status": "AT_ROOT_CHECKPOINT"}

        else:
            raise ValueError(f"Unhandled capability {cap}")

    def _record_failure(self, step: ToolExecutionStepV1, reason: str) -> None:
        self._step_receipts.append(
            ToolExecutionReceiptV1(
                step_index=step.step_index,
                capability=step.capability,
                status="STEP_FAILED",
                canvas_before_sha256=self.canvas_sha256,
                canvas_after_sha256=self.canvas_sha256,
                failure_reason=reason,
            )
        )
