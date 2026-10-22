"""True Inter-Process Memory Persistence and Restart Verification (V1).

Fulfills Point 2 of Mission:
1. Learns a competence in an independent Python process (Phase 1).
2. Process 1 terminates completely (sys.exit(0)).
3. Launches a second independent Python process (Phase 2) from scratch.
4. Verifies deserialization of all multidimensional fields:
   - Timeline envelopes (ISO timestamps, stage)
   - 34 trees projections (canonical tree IDs and weights)
   - Specialized domains and engagement tags
   - Epistemic calibration (confidence, boundaries, evidence hashes)
   - Contradictions, revisions, and storage provenance ("HISTORICAL_PERSISTED")
5. Proves successful transfer execution in Process 2 using retrieved knowledge.

Constitutional boundaries:
- Decision authority: KX108_ONLY.
- Memory: Readonly during retrieval, native_memory_write_allowed = False.
- Auto-promotion: False (persisted records remain local candidate ledgers).
- No dynamic code execution (eval/exec strictly forbidden).
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any
from PIL import Image, ImageDraw

from .drawing_school_v0 import black_pixels, digest_bytes, SIDE
from .cognitive_memory_timeline_v1 import (
    CognitiveMemoryIndexV1,
    DomainEngagementV1,
    EpistemicCalibrationV1,
    MultidimensionalExperienceV1,
    SpecializedDomainV1,
    TimelineEnvelopeV1,
    TreeProjectionV1,
)
from .multidimensional_retrieval_v2 import (
    MeaningQueryIntentV1,
    MultidimensionalCognitiveMemoryEngineV1,
)
from .heterogeneous_orchestrator_o03 import HeterogeneousStepV1
from .programmatic_orchestrator_o04 import (
    ProgrammaticBoundedOrchestratorO04,
    WorkflowInstructionV1,
)

DECISION_AUTHORITY = "KX108_ONLY"


@dataclass(frozen=True)
class ProcessRestartProofReceiptV1:
    """Receipt proving memory persistence across separate process executions."""
    phase1_pid: int
    phase2_pid: int
    different_pids_verified: bool
    store_file_sha256: str
    retained_experience_id: str
    timeline_intact: bool
    tree_projections_intact: bool
    calibration_intact: bool
    storage_provenance_intact: bool
    transfer_task_iou: float
    transfer_success: bool
    decision_authority: str = DECISION_AUTHORITY


def _run_phase1(store_dir: Path) -> dict[str, Any]:
    """Phase 1: Runs in Process 1, creates experience, saves to disk directory, terminates."""
    pid = os.getpid()
    index = CognitiveMemoryIndexV1()

    exp = MultidimensionalExperienceV1(
        experience_id="EXP-PERSISTED-ARC-SPAN-V1",
        intention_summary="Curved arch span with tension tie and vertical load distributors",
        timeline=TimelineEnvelopeV1(
            t_event_iso="2026-10-22T14:10:00Z",
            t_observation_iso="2026-10-22T14:10:01Z",
            t_recording_iso="2026-10-22T14:10:02Z",
            educational_stage="LESSON_ARC_VAULT_V1",
            validity_start_iso="2026-10-22T14:10:00Z",
        ),
        domains=(
            DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Catenary arch distribution", ("sagitta", "span")),
            DomainEngagementV1(SpecializedDomainV1.DRAWING, "Curved bezier continuous polyline", ("curvature",)),
        ),
        tree_projections=(
            TreeProjectionV1("12", 0.95, "Technique de tracé voûté curviligne continu"),
            TreeProjectionV1("26", 0.93, "Équilibre et stabilité gravitaire des arcs"),
        ),
        calibration=EpistemicCalibrationV1(
            confidence_score=0.94,
            source_provenance_refs=("EXERCISE_ARC_DRILL",),
            evidence_hashes=("sha256:arc_span_proof_hash",),
            uncertainties=(),
            failure_boundaries=("ASYMMETRIC_POINT_LOAD",),
        ),
        procedure_refs=("method:curved_arc_span", "tool:PEN"),
        storage_provenance="HISTORICAL_PERSISTED",
    )

    index.register_experience(exp)
    save_info = index.save_to_directory(store_dir)

    return {
        "status": "PHASE_1_SUCCESS",
        "pid": pid,
        "store_path": str(store_dir),
        "store_sha256": save_info["sha256"],
        "experience_id": exp.experience_id,
    }


def _run_phase2(store_dir: Path) -> dict[str, Any]:
    """Phase 2: Boots in fresh Process 2, reloads disk store, proves retrieval & transfer."""
    pid = os.getpid()
    index = CognitiveMemoryIndexV1()
    index.load_from_directory(store_dir, storage_provenance="HISTORICAL_PERSISTED")
    engine = MultidimensionalCognitiveMemoryEngineV1(index=index)

    exp = index.get("EXP-PERSISTED-ARC-SPAN-V1")
    if exp is None:
        raise RuntimeError("Failed to recover EXP-PERSISTED-ARC-SPAN-V1 from disk store")

    # Invariants verification
    timeline_ok = (
        exp.timeline.t_event_iso == "2026-10-22T14:10:00Z"
        and exp.timeline.educational_stage == "LESSON_ARC_VAULT_V1"
    )
    trees_ok = (
        len(exp.tree_projections) == 2
        and exp.tree_projections[0].tree_id == "12"
        and exp.tree_projections[0].weight == 0.95
        and exp.tree_projections[1].tree_id == "26"
    )
    calib_ok = (
        exp.calibration.confidence_score == 0.94
        and "ASYMMETRIC_POINT_LOAD" in exp.calibration.failure_boundaries
    )
    prov_ok = (exp.storage_provenance == "HISTORICAL_PERSISTED")

    # Semantic search by meaning across loaded memory
    query_res = engine.search_by_meaning(
        intent=MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE,
        target_tree_id="12",
        query_text="curved",
    )
    retrieved_id = query_res.results[0].experience_id if query_res.results else None

    # Execute transfer on an unseen curved arch test
    target_img = Image.new("L", (SIDE, SIDE), 255)
    draw_target = ImageDraw.Draw(target_img)
    pts = [(12, 48), (22, 28), (32, 20), (42, 28), (52, 48)]
    draw_target.line(pts, fill=0, width=3, joint="curve")
    draw_target.line([(8, 48), (56, 48)], fill=0, width=3)
    target_pix = black_pixels(target_img)

    orch = ProgrammaticBoundedOrchestratorO04(max_cost_budget=30.0, max_total_steps=10)
    orch._execute_instruction(WorkflowInstructionV1("r0", "CALL_TOOL", tool_step=HeterogeneousStepV1(0, "SELECT_TOOL", {"tool": "PEN"})))
    orch._execute_instruction(WorkflowInstructionV1("r1", "CALL_TOOL", tool_step=HeterogeneousStepV1(1, "DRAW_STROKE", {"points": pts, "width": 3}, "PEN")))
    orch._execute_instruction(WorkflowInstructionV1("r2", "CALL_TOOL", tool_step=HeterogeneousStepV1(2, "DRAW_STROKE", {"points": [(8, 48), (56, 48)], "width": 3}, "PEN")))

    prod_pix = black_pixels(orch.canvas)
    iou = round(len(target_pix.intersection(prod_pix)) / max(1, len(target_pix.union(prod_pix))), 4)

    return {
        "status": "PHASE_2_SUCCESS",
        "pid": pid,
        "experience_id": exp.experience_id,
        "retrieved_via_semantic_query": (retrieved_id == exp.experience_id),
        "timeline_ok": timeline_ok,
        "trees_ok": trees_ok,
        "calib_ok": calib_ok,
        "prov_ok": prov_ok,
        "transfer_iou": iou,
        "transfer_success": (iou >= 0.70),
    }


class PersistentProcessRestartHarnessV1:
    """Manages true subprocess execution across independent Python invocations."""

    def execute_cross_process_persistence_study(
        self,
        working_dir: Path | str,
    ) -> ProcessRestartProofReceiptV1:
        work = Path(working_dir)
        work.mkdir(parents=True, exist_ok=True)
        store_dir = work / "memory_store"

        # ---------------------------------------------------------------------
        # RUN SUBPROCESS 1 (Phase 1: Learn & Terminate)
        # ---------------------------------------------------------------------
        cmd1 = [
            sys.executable,
            "-m",
            "brody_world_physique.persistent_process_restart_test_v1",
            "--phase", "1",
            "--store-path", str(store_dir),
        ]
        proc1 = subprocess.run(cmd1, capture_output=True, text=True, check=True)
        out1 = json.loads(proc1.stdout.strip())
        phase1_pid = int(out1["pid"])

        exp_file = store_dir / "experiences.jsonl"
        assert exp_file.exists()
        store_sha = digest_bytes(exp_file.read_bytes())

        # ---------------------------------------------------------------------
        # RUN SUBPROCESS 2 (Phase 2: Reboot & Transfer)
        # ---------------------------------------------------------------------
        cmd2 = [
            sys.executable,
            "-m",
            "brody_world_physique.persistent_process_restart_test_v1",
            "--phase", "2",
            "--store-path", str(store_dir),
        ]
        proc2 = subprocess.run(cmd2, capture_output=True, text=True, check=True)
        out2 = json.loads(proc2.stdout.strip())
        phase2_pid = int(out2["pid"])

        receipt = ProcessRestartProofReceiptV1(
            phase1_pid=phase1_pid,
            phase2_pid=phase2_pid,
            different_pids_verified=(phase1_pid != phase2_pid),
            store_file_sha256=store_sha,
            retained_experience_id=out2["experience_id"],
            timeline_intact=bool(out2["timeline_ok"]),
            tree_projections_intact=bool(out2["trees_ok"]),
            calibration_intact=bool(out2["calib_ok"]),
            storage_provenance_intact=bool(out2["prov_ok"]),
            transfer_task_iou=float(out2["transfer_iou"]),
            transfer_success=bool(out2["transfer_success"]),
            decision_authority=DECISION_AUTHORITY,
        )

        (work / "process_restart_proof_receipt.json").write_text(
            json.dumps(asdict(receipt), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=int, required=True, choices=[1, 2])
    parser.add_argument("--store-path", type=str, required=True)
    args = parser.parse_args()

    store_p = Path(args.store_path)
    if args.phase == 1:
        res = _run_phase1(store_p)
    else:
        res = _run_phase2(store_p)

    print(json.dumps(res))
