"""O04: Programmatic Bounded Orchestrator (Anthropic / OpenAI Programmatic Tool Calling Adaptation).

Fulfills F00-F03 and O01-O03:
- Coordinates heterogeneous tools in multi-step workflows.
- Handles conditional branches (BRANCH_IF) and loops (LOOP_UNTIL) based on intermediate results.
- Manages isolated workflow state and canvas checkpoints without LLM round-trips.
- Strictly enforces step limits and compute budgets.
- Eliminates any dynamic code evaluation (eval/exec strictly forbidden).
- Produces deterministic, cryptographically auditable receipts.

Constitutional boundaries:
- Decision authority: KX108_ONLY.
- Memory: Readonly, native_memory_write_allowed = False.
- Emits act: False.
- No dynamic code execution (eval/exec forbidden).
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence
from PIL import Image

from .drawing_school_v0 import black_pixels, digest_bytes
from .heterogeneous_orchestrator_o03 import (
    CAPABILITY_COSTS,
    HeterogeneousInstrumentOrchestratorO03,
    HeterogeneousStepReceiptV1,
    HeterogeneousStepV1,
    SIDE,
)

MAX_PROGRAMMATIC_STEPS = 48
MAX_WORKFLOW_COST = 80.0


@dataclass(frozen=True)
class WorkflowPredicateV1:
    """Bounded, typed conditional predicate evaluated against workflow state."""
    variable_name: str
    operator: str  # "<", "<=", "==", "!=", ">=", ">"
    threshold: float | int | str | bool

    def evaluate(self, state: Mapping[str, Any]) -> bool:
        val = state.get(self.variable_name)
        if val is None:
            return False
        op = self.operator
        if op == "<":
            return float(val) < float(self.threshold)
        elif op == "<=":
            return float(val) <= float(self.threshold)
        elif op == "==":
            return val == self.threshold
        elif op == "!=":
            return val != self.threshold
        elif op == ">=":
            return float(val) >= float(self.threshold)
        elif op == ">":
            return float(val) > float(self.threshold)
        else:
            raise ValueError(f"Unsupported predicate operator: {op}")


@dataclass(frozen=True)
class WorkflowInstructionV1:
    """A bounded instruction inside a programmatic tool workflow."""
    instruction_id: str
    action_type: str  # "CALL_TOOL", "BRANCH_IF", "LOOP_UNTIL", "CHECKPOINT", "RESTORE"
    tool_step: HeterogeneousStepV1 | None = None
    predicate: WorkflowPredicateV1 | None = None
    then_instructions: tuple[WorkflowInstructionV1, ...] = ()
    else_instructions: tuple[WorkflowInstructionV1, ...] = ()
    loop_body: tuple[WorkflowInstructionV1, ...] = ()
    max_loop_iterations: int = 4
    checkpoint_name: str | None = None


@dataclass(frozen=True)
class ProgrammaticExecutionReceiptO04:
    """Audit receipt certifying programmatic tool coordination."""
    workflow_id: str
    total_instructions_dispatched: int
    total_tool_steps_executed: int
    branches_taken: int
    loops_executed: int
    total_cost_incurred: float
    budget_exhausted: bool
    final_canvas_sha256: str
    final_state_summary: Mapping[str, Any]
    step_receipts: tuple[HeterogeneousStepReceiptV1, ...]
    decision_authority: str = "KX108_ONLY"
    native_memory_write_allowed: bool = False
    emits_act: bool = False


class ProgrammaticBoundedOrchestratorO04:
    """Bounded programmatic orchestrator executing workflows without LLM round-trips."""

    def __init__(
        self,
        initial_canvas: Image.Image | None = None,
        max_cost_budget: float = MAX_WORKFLOW_COST,
        max_total_steps: int = MAX_PROGRAMMATIC_STEPS,
    ) -> None:
        self.orchestrator = HeterogeneousInstrumentOrchestratorO03(
            initial_canvas=initial_canvas,
            max_cost_budget=max_cost_budget,
            max_steps_budget=max_total_steps,
        )
        self.max_cost = max_cost_budget
        self.max_steps = max_total_steps
        self._state: dict[str, Any] = {}
        self._checkpoints: dict[str, Image.Image] = {}
        self._instructions_count = 0
        self._branches_taken = 0
        self._loops_executed = 0

    @property
    def canvas(self) -> Image.Image:
        return self.orchestrator.canvas

    @property
    def state(self) -> Mapping[str, Any]:
        return MappingProxyType(dict(self._state))

    def execute_workflow(
        self,
        workflow_id: str,
        instructions: Sequence[WorkflowInstructionV1],
    ) -> ProgrammaticExecutionReceiptO04:
        """Executes a structured workflow under bounded budgets."""
        budget_exhausted = False

        for inst in instructions:
            if self._instructions_count >= self.max_steps:
                budget_exhausted = True
                break
            if self.orchestrator._accumulated_cost >= self.max_cost:
                budget_exhausted = True
                break

            self._execute_instruction(inst)

        final_sha = self.orchestrator.canvas_sha256
        return ProgrammaticExecutionReceiptO04(
            workflow_id=workflow_id,
            total_instructions_dispatched=self._instructions_count,
            total_tool_steps_executed=len(self.orchestrator._step_receipts),
            branches_taken=self._branches_taken,
            loops_executed=self._loops_executed,
            total_cost_incurred=round(self.orchestrator._accumulated_cost, 2),
            budget_exhausted=budget_exhausted,
            final_canvas_sha256=final_sha,
            final_state_summary=MappingProxyType(dict(self._state)),
            step_receipts=tuple(self.orchestrator._step_receipts),
        )

    def _execute_instruction(self, inst: WorkflowInstructionV1) -> None:
        self._instructions_count += 1

        if inst.action_type == "CALL_TOOL" and inst.tool_step is not None:
            # Execute step through bounded tool orchestrator
            step = inst.tool_step
            cost = CAPABILITY_COSTS.get(step.capability, 1.0)
            if self.orchestrator._accumulated_cost + cost <= self.max_cost:
                receipt = self.orchestrator._execute_step(step, cost, intent=None)
                self.orchestrator._step_receipts.append(receipt)
                if receipt.status == "SUCCESS":
                    self.orchestrator._accumulated_cost += cost
                    # Update state from step details
                    for k, v in receipt.details.items():
                        self._state[k] = v
                    self._state["last_canvas_sha256"] = receipt.canvas_after_sha256
                    self._state["black_pixels_count"] = len(black_pixels(self.orchestrator.canvas))

        elif inst.action_type == "CHECKPOINT" and inst.checkpoint_name:
            self._checkpoints[inst.checkpoint_name] = self.orchestrator.canvas

        elif inst.action_type == "RESTORE" and inst.checkpoint_name:
            if inst.checkpoint_name in self._checkpoints:
                self.orchestrator._canvas = self._checkpoints[inst.checkpoint_name].copy()
                self._state["restored_from"] = inst.checkpoint_name

        elif inst.action_type == "BRANCH_IF" and inst.predicate is not None:
            cond = inst.predicate.evaluate(self._state)
            self._branches_taken += 1
            branch = inst.then_instructions if cond else inst.else_instructions
            for sub_inst in branch:
                if self._instructions_count >= self.max_steps:
                    break
                self._execute_instruction(sub_inst)

        elif inst.action_type == "LOOP_UNTIL" and inst.predicate is not None:
            self._loops_executed += 1
            iterations = 0
            while iterations < inst.max_loop_iterations and self._instructions_count < self.max_steps:
                if inst.predicate.evaluate(self._state):
                    break
                for sub_inst in inst.loop_body:
                    self._execute_instruction(sub_inst)
                iterations += 1
