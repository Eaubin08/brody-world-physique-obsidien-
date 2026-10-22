"""O03: Heterogeneous Instrument Orchestrator with Budgets, Permissions, and Cost Tracking.

Extends bounded instrument orchestration (O01/O02) with:
- Multiple heterogeneous instruments: PENCIL, PEN, NIB, ERASER, GEOMETRIC_STAMP, REGION_TRANSFORM.
- Explicit compute/execution cost accounting per step.
- Cumulative budget enforcement (cost units and step limits).
- Permission gating on specialized capabilities.
- Direct localized correction driven by G04 ErrorPatchV1 recommendations.
- Deterministic execution receipts.

Constitutional boundary:
- Decision authority: KX108_ONLY.
- Memory: Readonly, native_memory_write_allowed = False.
- No dynamic code execution (eval/exec strictly forbidden).
- Emits act: False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from types import MappingProxyType
from typing import Any, Mapping, Sequence
from PIL import Image, ImageDraw

from .drawing_school_v0 import black_pixels, digest_bytes
from .drawing_school_v1 import GestureV1
from .instrument_school_v2 import render_instrument, TOOLS
from .visual_intent_contracts_v1 import VisualEditIntentCandidateV1
from .visual_reperceiver_evaluator_v1 import ErrorPatchV1

SIDE = 64

CAPABILITY_COSTS: Mapping[str, float] = MappingProxyType({
    "SELECT_TOOL": 0.5,
    "DRAW_STROKE": 1.5,
    "ERASE_REGION": 1.0,
    "GEOMETRIC_STAMP": 3.0,
    "APPLY_INSTRUMENT": 2.0,
    "INSPECT_PIXELS": 0.5,
    "REVERT_STEP": 1.0,
})

HETEROGENEOUS_CAPABILITIES = frozenset(CAPABILITY_COSTS.keys())


@dataclass(frozen=True)
class HeterogeneousStepV1:
    """A single step in a heterogeneous instrument plan."""
    step_index: int
    capability: str
    arguments: Mapping[str, Any] = field(default_factory=dict)
    tool_name: str = "PEN"

    def __post_init__(self) -> None:
        if self.capability not in HETEROGENEOUS_CAPABILITIES:
            raise ValueError(f"Unauthorized capability: {self.capability}. Must be in {HETEROGENEOUS_CAPABILITIES}")
        if self.step_index < 0:
            raise ValueError("step_index must be non-negative")


@dataclass(frozen=True)
class HeterogeneousStepReceiptV1:
    """Receipt for a single heterogeneous instrument step."""
    step_index: int
    capability: str
    tool_used: str
    status: str
    step_cost: float
    canvas_before_sha256: str
    canvas_after_sha256: str
    reverted: bool = False
    failure_reason: str | None = None
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class HeterogeneousOrchestrationReceiptV1:
    """Cumulative receipt certifying the heterogeneous execution run."""
    plan_id: str
    total_steps_executed: int
    successful_steps: int
    reverted_steps: int
    total_cost_incurred: float
    budget_remaining: float
    final_canvas_sha256: str
    step_receipts: tuple[HeterogeneousStepReceiptV1, ...]
    decision_authority: str = "KX108_ONLY"
    native_memory_write_allowed: bool = False


class HeterogeneousInstrumentOrchestratorO03:
    """Bounded heterogeneous instrument executor with strict cost budgeting."""

    def __init__(
        self,
        initial_canvas: Image.Image | None = None,
        *,
        max_cost_budget: float = 60.0,
        max_steps_budget: int = 32,
        allowed_capabilities: frozenset[str] | None = None,
    ) -> None:
        if initial_canvas is None:
            self._canvas = Image.new("L", (SIDE, SIDE), 255)
        else:
            self._canvas = initial_canvas.convert("L").copy()

        self.max_cost = max_cost_budget
        self.max_steps = max_steps_budget
        self.allowed = allowed_capabilities or HETEROGENEOUS_CAPABILITIES

        self._checkpoints: list[Image.Image] = [self._canvas.copy()]
        self._current_tool = "PEN"
        self._current_strokes: list[GestureV1] = []
        self._accumulated_cost = 0.0
        self._step_receipts: list[HeterogeneousStepReceiptV1] = []

    @property
    def canvas(self) -> Image.Image:
        return self._canvas.copy()

    @property
    def canvas_sha256(self) -> str:
        return digest_bytes(self._canvas.tobytes())

    def execute_plan(
        self,
        plan_id: str,
        steps: Sequence[HeterogeneousStepV1],
        intent: VisualEditIntentCandidateV1 | None = None,
    ) -> HeterogeneousOrchestrationReceiptV1:
        success = 0
        reverted = 0

        for step in steps:
            # Check budgets
            if len(self._step_receipts) >= self.max_steps:
                break
            cost = CAPABILITY_COSTS.get(step.capability, 1.0)
            if self._accumulated_cost + cost > self.max_cost:
                # Budget exhaustion
                self._step_receipts.append(
                    HeterogeneousStepReceiptV1(
                        step_index=step.step_index,
                        capability=step.capability,
                        tool_used=step.tool_name,
                        status="BUDGET_EXHAUSTED",
                        step_cost=0.0,
                        canvas_before_sha256=self.canvas_sha256,
                        canvas_after_sha256=self.canvas_sha256,
                        failure_reason=f"Exceeded max cost budget: {self._accumulated_cost + cost} > {self.max_cost}",
                    )
                )
                break

            receipt = self._execute_step(step, cost, intent)
            self._step_receipts.append(receipt)

            if receipt.status == "SUCCESS":
                success += 1
                self._accumulated_cost += cost
            elif receipt.reverted:
                reverted += 1

        remaining = max(0.0, self.max_cost - self._accumulated_cost)
        return HeterogeneousOrchestrationReceiptV1(
            plan_id=plan_id,
            total_steps_executed=len(self._step_receipts),
            successful_steps=success,
            reverted_steps=reverted,
            total_cost_incurred=round(self._accumulated_cost, 2),
            budget_remaining=round(remaining, 2),
            final_canvas_sha256=self.canvas_sha256,
            step_receipts=tuple(self._step_receipts),
        )

    def _execute_step(
        self,
        step: HeterogeneousStepV1,
        cost: float,
        intent: VisualEditIntentCandidateV1 | None,
    ) -> HeterogeneousStepReceiptV1:
        before_sha = self.canvas_sha256
        before_img = self._canvas.copy()

        # Permission check
        if step.capability not in self.allowed:
            return HeterogeneousStepReceiptV1(
                step_index=step.step_index,
                capability=step.capability,
                tool_used=step.tool_name,
                status="PERMISSION_DENIED",
                step_cost=0.0,
                canvas_before_sha256=before_sha,
                canvas_after_sha256=before_sha,
                failure_reason=f"Capability {step.capability} not in allowed permissions",
            )

        # Dispatch
        try:
            details = self._dispatch(step)
        except Exception as exc:
            return HeterogeneousStepReceiptV1(
                step_index=step.step_index,
                capability=step.capability,
                tool_used=step.tool_name,
                status="EXECUTION_ERROR",
                step_cost=0.0,
                canvas_before_sha256=before_sha,
                canvas_after_sha256=before_sha,
                failure_reason=str(exc),
            )

        after_sha = self.canvas_sha256

        # Intent violation check (LOCK boundary enforcement)
        if intent is not None:
            comp = intent.check_compliance(before_img, self._canvas)
            if comp.lock_violations:
                self._canvas = before_img
                return HeterogeneousStepReceiptV1(
                    step_index=step.step_index,
                    capability=step.capability,
                    tool_used=step.tool_name,
                    status="REJECTED_LOCK_VIOLATION",
                    step_cost=cost,  # Cost is incurred even if rolled back
                    canvas_before_sha256=before_sha,
                    canvas_after_sha256=before_sha,
                    reverted=True,
                    failure_reason="; ".join(comp.lock_violations),
                    details=details,
                )

        self._checkpoints.append(self._canvas.copy())
        return HeterogeneousStepReceiptV1(
            step_index=step.step_index,
            capability=step.capability,
            tool_used=step.tool_name,
            status="SUCCESS",
            step_cost=cost,
            canvas_before_sha256=before_sha,
            canvas_after_sha256=after_sha,
            reverted=False,
            details=details,
        )

    def _dispatch(self, step: HeterogeneousStepV1) -> dict[str, Any]:
        cap = step.capability
        args = step.arguments

        if cap == "SELECT_TOOL":
            t = str(args.get("tool", "PEN")).upper()
            if t not in TOOLS:
                raise ValueError(f"Invalid tool {t}. Must be in {TOOLS}")
            self._current_tool = t
            return {"selected_tool": t}

        elif cap == "DRAW_STROKE":
            raw_pts = args.get("points", ())
            pts = tuple(tuple(int(c) for c in p) for p in raw_pts)
            kind = "STRAIGHT_STROKE" if len(pts) <= 2 else "CURVED_STROKE"
            gesture = GestureV1(points=pts, kind=kind)
            self._current_strokes.append(gesture)
            draw = ImageDraw.Draw(self._canvas)
            if len(pts) >= 2:
                draw.line(pts, fill=0, width=int(args.get("width", 3)), joint="curve")
            return {"points_drawn": len(pts), "kind": kind}

        elif cap == "ERASE_REGION":
            x0 = int(args.get("x0", 0))
            y0 = int(args.get("y0", 0))
            x1 = int(args.get("x1", SIDE))
            y1 = int(args.get("y1", SIDE))
            ImageDraw.Draw(self._canvas).rectangle([x0, y0, x1, y1], fill=255)
            return {"erased_bbox": [x0, y0, x1, y1]}

        elif cap == "GEOMETRIC_STAMP":
            shape = str(args.get("shape", "BOX")).upper()
            x0, y0, x1, y1 = [int(v) for v in args.get("bbox", (16, 16, 48, 48))]
            draw = ImageDraw.Draw(self._canvas)
            if shape == "BOX":
                draw.rectangle([x0, y0, x1, y1], outline=0, width=3)
            elif shape == "CIRCLE":
                draw.ellipse([x0, y0, x1, y1], outline=0, width=3)
            elif shape == "CROSS":
                cx = (x0 + x1) // 2
                cy = (y0 + y1) // 2
                draw.line([(cx, y0), (cx, y1)], fill=0, width=3)
                draw.line([(x0, cy), (x1, cy)], fill=0, width=3)
            return {"stamp_shape": shape, "bbox": [x0, y0, x1, y1]}

        elif cap == "APPLY_INSTRUMENT":
            if self._current_strokes:
                rendered = render_instrument(tuple(self._current_strokes), self._current_tool)
                self._canvas = rendered.convert("L")
            return {"instrument_applied": self._current_tool, "strokes": len(self._current_strokes)}

        elif cap == "INSPECT_PIXELS":
            pixels = black_pixels(self._canvas)
            return {"black_pixels_count": len(pixels)}

        elif cap == "REVERT_STEP":
            if len(self._checkpoints) > 1:
                self._checkpoints.pop()
                self._canvas = self._checkpoints[-1].copy()
                return {"reverted_to": len(self._checkpoints) - 1}
            return {"reverted_to": 0}

        raise ValueError(f"Unhandled capability: {cap}")

    @staticmethod
    def create_step_from_error_patch(patch: ErrorPatchV1, step_index: int) -> HeterogeneousStepV1:
        """Translates a G04 ErrorPatchV1 into an executable instrument step."""
        if patch.suggested_action == "ERASE_REGION":
            return HeterogeneousStepV1(
                step_index=step_index,
                capability="ERASE_REGION",
                arguments=dict(patch.suggested_arguments),
                tool_name="ERASER",
            )
        elif patch.suggested_action == "DRAW_STROKE":
            return HeterogeneousStepV1(
                step_index=step_index,
                capability="DRAW_STROKE",
                arguments=dict(patch.suggested_arguments),
                tool_name="PEN",
            )
        else:
            return HeterogeneousStepV1(
                step_index=step_index,
                capability="REVERT_STEP",
            )
