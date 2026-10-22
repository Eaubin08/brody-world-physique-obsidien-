"""Standalone Inter-Process Retention Runner (V2).

Executed in an independent Python OS process with zero access to the teacher
target image or private teacher variables.
Reads only a sanitized spatial working memory schema JSON file, renders the production
on a blank canvas, and writes out the resulting image and receipt.

Constitutional boundaries:
- KX108_ONLY decision authority.
- Candidate-only memory ledger.
- Zero eval/exec.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

# Ensure brody_world_physique is in sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from PIL import Image
from brody_world_physique.contracts_v0 import DECISION_AUTHORITY
from brody_world_physique.drawing_school_v0 import SIDE, digest_bytes
from brody_world_physique.heterogeneous_orchestrator_o03 import HeterogeneousStepV1
from brody_world_physique.programmatic_orchestrator_o04 import (
    ProgrammaticBoundedOrchestratorO04,
    WorkflowInstructionV1,
)


def run_standalone_retention(schema_path: str | Path, output_image_path: str | Path) -> dict:
    p_schema = Path(schema_path)
    if not p_schema.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    schema = json.loads(p_schema.read_text(encoding="utf-8"))

    # Strictly verify that NO target pixels or teacher parameters leaked into the schema
    forbidden_keys = {"target_pixels", "teacher_scene", "target_img", "target_bytes", "ground_truth"}
    leaked = forbidden_keys.intersection(schema.keys())
    if leaked:
        raise ValueError(f"Contamination error: Forbidden keys detected in working memory schema: {leaked}")

    strokes = schema.get("strokes", [])
    max_budget = float(schema.get("max_cost_budget", 30.0))

    orch = ProgrammaticBoundedOrchestratorO04(max_cost_budget=max_budget, max_total_steps=len(strokes) + 2)
    orch._execute_instruction(
        WorkflowInstructionV1("r0", "CALL_TOOL", tool_step=HeterogeneousStepV1(0, "SELECT_TOOL", {"tool": "PEN"}))
    )

    t0 = time.perf_counter()
    for idx, stroke in enumerate(strokes):
        pts = [tuple(p) for p in stroke["points"]]
        width = int(stroke.get("width", 2))
        step_id = f"r_{idx + 1}"
        orch._execute_instruction(
            WorkflowInstructionV1(
                step_id,
                "CALL_TOOL",
                tool_step=HeterogeneousStepV1(idx + 1, "DRAW_STROKE", {"points": pts, "width": width}, "PEN"),
            )
        )
    dt_ms = (time.perf_counter() - t0) * 1000.0

    p_out = Path(output_image_path)
    p_out.parent.mkdir(parents=True, exist_ok=True)
    orch.canvas.save(p_out)

    receipt = {
        "status": "RETENTION_PROCESS_COMPLETED",
        "decision_authority": DECISION_AUTHORITY,
        "operations_count": len(orch.orchestrator._step_receipts),
        "compute_cost": round(orch.orchestrator._accumulated_cost, 2),
        "execution_time_ms": round(dt_ms, 2),
        "generated_image_sha256": digest_bytes(orch.canvas.tobytes()),
        "output_image_path": str(p_out.resolve()),
    }
    return receipt


def main():
    parser = argparse.ArgumentParser(description="Standalone Interprocess Retention Runner")
    parser.add_argument("--schema", required=True, help="Path to sanitized working memory JSON schema")
    parser.add_argument("--output", required=True, help="Path to save generated PNG image")
    args = parser.parse_args()

    rec = run_standalone_retention(args.schema, args.output)
    print(json.dumps(rec, indent=2))


if __name__ == "__main__":
    main()
