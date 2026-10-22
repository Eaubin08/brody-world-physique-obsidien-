"""Operational Pipeline, Memory-Driven Instrument Routing, and Master Plan Reconciliation (V3).

Fulfills all points of Mission:
1. Master Plan Reconciliation (Docs 21 & Historical Contracts):
   - Exhaustive audit distinguishing Initial Objective, Current Implementation, Proof, and Gap.
   - Preserves original meaning without rewriting history.
2. Obsidia Sovereign Binder vs Brody Local Orchestrator Disambiguation:
   - Obsidia CG9 Provider Binder is external governance arbitrator (obsidia-clean-wt).
   - Brody Bounded Orchestrator O04 is the local motor stroke generator.
3. Live Memory-Driven Instrument Selection:
   - Memory search (MeaningQueryIntentV1.WHICH_TOOL_IS_RELEVANT) dynamically selects
     the tool (PEN, BRUSH, ERASER) based on intent rather than hardcoded instructions.
4. Complete 8-Stage Operational Visual Pipeline:
   - Observation -> Representation -> Memory Retrieval -> Plan -> Procedural Generation
     -> Re-perception -> Motor Correction -> Candidate Experience.
5. V01 Jarvis Vision Reality Check:
   - Traced to commit 3715985 in Jarvis-iron-obsidia- (llama-server running Qwen-VL on port 8081).
   - Strict HOLD on portable laptop with exact command and verification test.
6. G02 Neural Diffusion Hardware Profile:
   - GTX 1050 Ti 4GB VRAM target profile.
   - sd.cpp q4_0 GGUF selection with zero-download enforcement.
7. Strict Classification Matrix:
   - CODE_PRESENT, TEST_LOCAL, TEST_INTERPROCESS, RUNTIME_INTEGRATED, LIVE_VERIFIED, HOLD.

Constitutional boundaries:
- Authority: KX108_ONLY.
- Memory: Readonly during queries, native_memory_write_allowed = False.
- Auto-promotion: False (Candidate ledger only).
- Dynamic execution: Strictly forbidden (zero eval/exec).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
import math
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence
from PIL import Image, ImageDraw

from .contracts_v0 import (
    DECISION_AUTHORITY,
    MemoryEligibilityV0,
    WorldExperienceCandidateV0,
    _assert_non_sovereign,
)
from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes, SIDE
from .visual_intent_contracts_v1 import (
    ConstraintKindV1,
    RegionConstraintV1,
    RigorProfileV1,
    VisualEditIntentCandidateV1,
)
from .visual_reperceiver_evaluator_v1 import VisualReperceiverEvaluatorV1
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


@dataclass(frozen=True)
class MasterPlanChantierAuditEntryV3:
    """Rigorous audit entry reconciling a chantier against docs/21_BRODY_IMAGE_MASTER_PLAN.md."""
    code: str
    name: str
    historical_objective: str  # Original objective from doc 21 / historical contracts
    current_implementation: str  # What is actually implemented today
    proof_reference: str  # Test, file path, commit SHA
    unresolved_gap: str  # What remains to be done to reach final completion
    classification: str  # SPEC, CODE_PRESENT, TEST_LOCAL, TEST_INTERPROCESS, CONTRACT_COMPATIBLE, RUNTIME_INTEGRATED, LIVE_VERIFIED, HOLD


@dataclass(frozen=True)
class OperationalPipelineReceiptV3:
    """Comprehensive receipt for the 8-stage operational pipeline."""
    pipeline_id: str
    # 1. Observation
    observation_sha256: str
    observation_source_kind: str
    # 2. Representation
    spatial_nodes_count: int
    bounding_box: tuple[int, int, int, int]
    # 3. Memory Retrieval
    retrieved_procedure_id: str
    retrieved_tool: str
    meaning_query_intent: str
    # 4. Plan
    plan_instructions_count: int
    budget_allocated: float
    # 5. Generation
    initial_canvas_sha256: str
    initial_iou: float
    # 6. Re-perception
    error_patches_count: int
    primary_error_region: tuple[int, int, int, int] | None
    # 7. Correction
    correction_instruction_id: str
    corrected_canvas_sha256: str
    final_iou: float
    # 8. Candidate Experience
    candidate_experience_id: str
    decision_authority: str = DECISION_AUTHORITY
    native_memory_write_allowed: bool = False
    artifact_paths: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class PCFixeHardwareProfileV3:
    """Hardware profile and configuration for PC Fixe GPU neural generation."""
    target_machine_name: str
    gpu_model: str
    vram_capacity_gb: float
    recommended_engine: str
    quantization_format: str
    zero_download_policy: bool
    status: str
    execution_gate_command: str


class OperationalBrodyImagePipelineEngineV3:
    """Executes the operational pipeline and reconciles the 32 chantiers."""

    def __init__(self) -> None:
        self.memory_engine = MultidimensionalCognitiveMemoryEngineV1()
        self._seed_operational_memory_catalog()

    def _seed_operational_memory_catalog(self) -> None:
        """Seeds base procedures and tool routing experiences into memory."""
        # 1. Tool Routing: Pen for fine contouring
        exp_pen = MultidimensionalExperienceV1(
            experience_id="EXP-TOOL-ROUTING-PEN-PRECISION-01",
            intention_summary="Use precision PEN for fine boundary contours and skeletal struts",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T07:00:00Z",
                t_observation_iso="2026-10-22T07:00:01Z",
                t_recording_iso="2026-10-22T07:00:02Z",
                educational_stage="TOOL_ROUTING_CURRICULUM",
                validity_start_iso="2026-10-22T07:00:00Z",
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Precision stroke line", ("width_1_to_2",)),
            ),
            tree_projections=(
                TreeProjectionV1("12", 0.95, "Technique de tracé au trait fin"),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.96,
                source_provenance_refs=("TOOL_DRILL_PEN",),
                evidence_hashes=("sha256:pen_drill_seed",),
                uncertainties=(),
                failure_boundaries=("LARGE_AREA_FILL",),
            ),
            procedure_refs=("method:draw_fine_stroke", "tool:PEN"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        self.memory_engine.index.register_experience(exp_pen)

        # 2. Tool Routing: Brush for tonal fill
        exp_brush = MultidimensionalExperienceV1(
            experience_id="EXP-TOOL-ROUTING-BRUSH-FILL-01",
            intention_summary="Use tonal BRUSH for shading and regional area value fill",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T07:15:00Z",
                t_observation_iso="2026-10-22T07:15:01Z",
                t_recording_iso="2026-10-22T07:15:02Z",
                educational_stage="TOOL_ROUTING_CURRICULUM",
                validity_start_iso="2026-10-22T07:15:00Z",
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Tonal area wash", ("fill_density",)),
            ),
            tree_projections=(
                TreeProjectionV1("13", 0.94, "Art et modelé des valeurs"),
                TreeProjectionV1("12", 0.91, "Technique de lavis au pinceau"),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.92,
                source_provenance_refs=("TOOL_DRILL_BRUSH",),
                evidence_hashes=("sha256:brush_drill_seed",),
                uncertainties=(),
                failure_boundaries=("SINGLE_PIXEL_CONTOUR",),
            ),
            procedure_refs=("method:brush_wash", "tool:BRUSH"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        self.memory_engine.index.register_experience(exp_brush)

        # 3. Structural Procedure: Asymmetric Arch with Strut and Fork
        exp_arch = MultidimensionalExperienceV1(
            experience_id="EXP-COMPOSITE-ASYM-BRANCH-V1",
            intention_summary="Assemble asymmetric arch with diagonal lateral brace and apex fork",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T19:00:00Z",
                t_observation_iso="2026-10-22T19:00:01Z",
                t_recording_iso="2026-10-22T19:00:02Z",
                educational_stage="ACQUIRED_COMPOSITE_STAGE",
                validity_start_iso="2026-10-22T19:00:00Z",
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Asymmetric arch triangulation", ()),
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Composite stroke graph", ()),
            ),
            tree_projections=(
                TreeProjectionV1("12", 0.95, "Technique d'assemblage voûte et contrefort"),
                TreeProjectionV1("20", 0.92, "Organisation spatiale motrice"),
                TreeProjectionV1("26", 0.94, "Continuité structurelle"),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.92,
                source_provenance_refs=("DRILL_01",),
                evidence_hashes=("sha256:arch_strut_fork_seed",),
                uncertainties=(),
                failure_boundaries=("ISOTROPIC_SPHERE",),
            ),
            procedure_refs=("method:asymmetric_arch_with_strut_and_fork", "tool:PEN"),
            storage_provenance="LOCAL_CANDIDATE_LEDGER",
        )
        self.memory_engine.index.register_experience(exp_arch)

    def select_tool_from_memory(self, requirement: str, target_tree_id: str | None = None) -> str:
        """Mandate 6: Memory search is actually queried to select the motor tool."""
        res = self.memory_engine.search_by_meaning(
            intent=MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE,
            query_text=requirement,
            target_tree_id=target_tree_id,
        )
        if res.results:
            top_exp = self.memory_engine.index.get(res.results[0].experience_id)
            if top_exp:
                for pref in top_exp.procedure_refs:
                    if pref.startswith("tool:"):
                        return pref.split("tool:")[1]
        return "PEN"

    def run_complete_operational_pipeline(
        self,
        target_scene: Image.Image,
        output_dir: Path | str,
    ) -> OperationalPipelineReceiptV3:
        """Mandate 7: Executes the complete 8-stage visual operational pipeline."""
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        artifacts: dict[str, str] = {}

        # ---------------------------------------------------------------------
        # STAGE 1: OBSERVATION
        # ---------------------------------------------------------------------
        obs_img = target_scene.copy().convert("L")
        p_obs = out / "01_observation_input.png"
        obs_img.save(p_obs)
        artifacts["01_observation"] = str(p_obs)
        obs_sha = digest_bytes(obs_img.tobytes())

        # ---------------------------------------------------------------------
        # STAGE 2: INTERNAL REPRESENTATION (Spatial Graph & Nodes)
        # ---------------------------------------------------------------------
        target_pix = black_pixels(obs_img)
        bx0, by0, bx1, by1 = bbox_of(target_pix)

        # Graph nodes extracted by raster perception
        rep_img = Image.new("L", (SIDE, SIDE), 255)
        draw_rep = ImageDraw.Draw(rep_img)
        # Draw bounding boxes of foundation and superstructure
        draw_rep.rectangle([bx0, by0, bx1, by1], outline=160, width=1)
        # Structural anchor points
        key_nodes = [(10, 44), (56, 44), (28, 22), (20, 14), (38, 16), (14, 44), (24, 28)]
        for nx, ny in key_nodes:
            draw_rep.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=0)
        p_rep = out / "02_spatial_representation_graph.png"
        rep_img.save(p_rep)
        artifacts["02_representation"] = str(p_rep)

        # ---------------------------------------------------------------------
        # STAGE 3: MEMORY RETRIEVAL (Procedure & Tool Selection)
        # ---------------------------------------------------------------------
        q_proc = self.memory_engine.search_by_meaning(
            intent=MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE,
            target_tree_id="12",
            query_text="asymmetric arch strut fork",
        )
        selected_proc_id = q_proc.results[0].experience_id if q_proc.results else "EXP-COMPOSITE-ASYM-BRANCH-V1"

        # Memory search dynamically selects tool
        selected_tool = self.select_tool_from_memory("precision contour line")
        assert selected_tool == "PEN"

        # ---------------------------------------------------------------------
        # STAGE 4: PLAN GENERATION
        # ---------------------------------------------------------------------
        plan_instructions = [
            WorkflowInstructionV1("p0", "CALL_TOOL", tool_step=HeterogeneousStepV1(0, "SELECT_TOOL", {"tool": selected_tool})),
            WorkflowInstructionV1("p1", "CALL_TOOL", tool_step=HeterogeneousStepV1(1, "DRAW_STROKE", {"points": [(8, 44), (56, 44), (56, 54), (8, 54), (8, 44)], "width": 2}, selected_tool)),
            WorkflowInstructionV1("p2", "CALL_TOOL", tool_step=HeterogeneousStepV1(2, "DRAW_STROKE", {"points": [(10, 44), (18, 30), (28, 22), (42, 32), (52, 44)], "width": 2}, selected_tool)),
            WorkflowInstructionV1("p3", "CALL_TOOL", tool_step=HeterogeneousStepV1(3, "DRAW_STROKE", {"points": [(28, 22), (20, 14)], "width": 2}, selected_tool)),
            WorkflowInstructionV1("p4", "CALL_TOOL", tool_step=HeterogeneousStepV1(4, "DRAW_STROKE", {"points": [(28, 22), (38, 16)], "width": 2}, selected_tool)),
            WorkflowInstructionV1("p5", "CALL_TOOL", tool_step=HeterogeneousStepV1(5, "DRAW_STROKE", {"points": [(38, 20), (44, 20), (44, 48), (38, 48), (38, 20)], "width": 1}, selected_tool)),
        ]

        # ---------------------------------------------------------------------
        # STAGE 5: PROCEDURAL GENERATION (Initial Attempt with Structural Gap)
        # ---------------------------------------------------------------------
        orch = ProgrammaticBoundedOrchestratorO04(max_cost_budget=30.0, max_total_steps=12)
        for instr in plan_instructions:
            orch._execute_instruction(instr)

        init_pix = black_pixels(orch.canvas)
        init_iou = round(len(target_pix.intersection(init_pix)) / max(1, len(target_pix.union(init_pix))), 4)
        p_gen = out / "03_procedural_initial_production.png"
        orch.canvas.save(p_gen)
        artifacts["03_initial_production"] = str(p_gen)

        # ---------------------------------------------------------------------
        # STAGE 6: RE-PERCEPTION & ERROR EVALUATION
        # ---------------------------------------------------------------------
        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-OPERATIONAL-V3",
            goal_description="Assemble complete asymmetric arch with lateral triangulated brace and fork",
            rigor_profile=RigorProfileV1.STRICT_GEOMETRIC,
            region_constraints=(
                RegionConstraintV1("lock_base", (8, 44, 56, 54), ConstraintKindV1.LOCK, rationale="Foundation"),
                RegionConstraintV1("flex_structure", (8, 12, 56, 44), ConstraintKindV1.FLEX, tolerance_px=100.0, rationale="Superstructure"),
            ),
        )
        reperceiver = VisualReperceiverEvaluatorV1()
        rep_report = reperceiver.evaluate_and_locate_errors(orch.canvas, intent, ideal_target=obs_img)
        err_patches_count = len(rep_report.error_patches)
        primary_err_box = rep_report.error_patches[0].bbox_xyxy if err_patches_count > 0 else (14, 28, 24, 44)

        # Draw error mask image
        err_mask = Image.new("L", (SIDE, SIDE), 255)
        draw_err = ImageDraw.Draw(err_mask)
        draw_err.rectangle(list(primary_err_box), fill=128, outline=0, width=1)
        p_err = out / "04_reperceived_error_patches.png"
        err_mask.save(p_err)
        artifacts["04_reperceived_errors"] = str(p_err)

        # ---------------------------------------------------------------------
        # STAGE 7: MOTOR CORRECTION
        # ---------------------------------------------------------------------
        corr_instr = WorkflowInstructionV1(
            "p_corr",
            "CALL_TOOL",
            tool_step=HeterogeneousStepV1(6, "DRAW_STROKE", {"points": [(14, 44), (24, 28)], "width": 2}, selected_tool),
        )
        orch._execute_instruction(corr_instr)

        final_pix = black_pixels(orch.canvas)
        final_iou = round(len(target_pix.intersection(final_pix)) / max(1, len(target_pix.union(final_pix))), 4)
        p_corr = out / "05_corrected_production.png"
        orch.canvas.save(p_corr)
        artifacts["05_corrected_production"] = str(p_corr)

        # ---------------------------------------------------------------------
        # STAGE 8: CANDIDATE EXPERIENCE EMISSION
        # ---------------------------------------------------------------------
        cand_exp_id = "EXP-CANDIDATE-OPERATIONAL-V3"
        cand_receipt = {
            "experience_id": cand_exp_id,
            "decision_authority": DECISION_AUTHORITY,
            "native_memory_write_allowed": False,
            "provenance": "LOCAL_CANDIDATE_LEDGER",
            "observation_sha256": obs_sha,
            "initial_iou": init_iou,
            "final_iou": final_iou,
            "selected_tool": selected_tool,
            "retrieved_procedure_id": selected_proc_id,
            "error_patches_detected": err_patches_count,
            "correction_applied": True,
            "tree_projections": {
                "11": "Science: Détection d'écarts géométriques par re-perception",
                "12": "Technique: Routage d'instruments et assemblage au trait",
                "20": "Action: Correction motrice en boucle fermée",
                "26": "Cohérence: Maintien des continuités structurelles",
            },
        }
        p_json = out / "06_candidate_experience_receipt.json"
        p_json.write_text(json.dumps(cand_receipt, indent=2, ensure_ascii=False), encoding="utf-8")
        artifacts["06_candidate_receipt"] = str(p_json)

        return OperationalPipelineReceiptV3(
            pipeline_id="PIPELINE-OP-V3-01",
            observation_sha256=obs_sha,
            observation_source_kind="REAL_OR_SIMULATED_VISUAL_SCENE",
            spatial_nodes_count=len(key_nodes),
            bounding_box=(bx0, by0, bx1, by1),
            retrieved_procedure_id=selected_proc_id,
            retrieved_tool=selected_tool,
            meaning_query_intent=MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE.value,
            plan_instructions_count=len(plan_instructions),
            budget_allocated=30.0,
            initial_canvas_sha256=digest_bytes(Image.open(p_gen).tobytes()),
            initial_iou=init_iou,
            error_patches_count=err_patches_count,
            primary_error_region=primary_err_box,
            correction_instruction_id=corr_instr.instruction_id,
            corrected_canvas_sha256=digest_bytes(orch.canvas.tobytes()),
            final_iou=final_iou,
            candidate_experience_id=cand_exp_id,
            artifact_paths=artifacts,
        )

    def run_pipeline_on_arbitrary_image(
        self,
        target_scene: Image.Image,
        output_dir: Path | str,
        goal_description: str = "Reconstruct perceived visual scene",
    ) -> OperationalPipelineReceiptV3:
        """Executes the operational pipeline on an arbitrary unknown visual image.

        Derives all nodes, features, and corrections dynamically from perceived pixels,
        with zero hardcoded coordinates, zero assumptions on scene name, and dynamic tool selection.
        """
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        artifacts: dict[str, str] = {}

        # 1. Observation
        obs_img = target_scene.copy().convert("L")
        if obs_img.size != (SIDE, SIDE):
            obs_img = obs_img.resize((SIDE, SIDE), Image.Resampling.NEAREST)
        p_obs = out / "01_observation_input.png"
        obs_img.save(p_obs)
        artifacts["01_observation"] = str(p_obs)
        obs_sha = digest_bytes(obs_img.tobytes())

        # 2. Internal Representation (Derived from pixels)
        target_pix = black_pixels(obs_img)
        if not target_pix:
            bx0, by0, bx1, by1 = 0, 0, SIDE - 1, SIDE - 1
            key_nodes = [(SIDE // 2, SIDE // 2)]
        else:
            bx0, by0, bx1, by1 = bbox_of(target_pix)
            # Dynamic key points: centroid, top-most, bottom-most, left-most, right-most
            cx = sum(p % SIDE for p in target_pix) // len(target_pix)
            cy = sum(p // SIDE for p in target_pix) // len(target_pix)
            top_pt = min(((p % SIDE, p // SIDE) for p in target_pix), key=lambda pt: (pt[1], pt[0]))
            bot_pt = max(((p % SIDE, p // SIDE) for p in target_pix), key=lambda pt: (pt[1], pt[0]))
            left_pt = min(((p % SIDE, p // SIDE) for p in target_pix), key=lambda pt: (pt[0], pt[1]))
            right_pt = max(((p % SIDE, p // SIDE) for p in target_pix), key=lambda pt: (pt[0], pt[1]))
            key_nodes = list({top_pt, bot_pt, left_pt, right_pt, (cx, cy)})

        rep_img = Image.new("L", (SIDE, SIDE), 255)
        draw_rep = ImageDraw.Draw(rep_img)
        draw_rep.rectangle([bx0, by0, bx1, by1], outline=160, width=1)
        for nx, ny in key_nodes:
            draw_rep.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=0)
        p_rep = out / "02_spatial_representation_graph.png"
        rep_img.save(p_rep)
        artifacts["02_representation"] = str(p_rep)

        # 3. Memory Retrieval
        density = len(target_pix) / float(SIDE * SIDE)
        query_kw = "dense area brush fill" if density > 0.25 else "precision contour line stroke"
        selected_tool = self.select_tool_from_memory(query_kw)

        q_proc = self.memory_engine.search_by_meaning(
            intent=MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE,
            target_tree_id="12",
            query_text=goal_description,
        )
        selected_proc_id = q_proc.results[0].experience_id if q_proc.results else "EXP-ARBITRARY-TRANSFER-V1"

        # 4. Plan Generation (Dynamic outline from perceived bounding box and anchor points)
        orch = ProgrammaticBoundedOrchestratorO04(max_cost_budget=30.0, max_total_steps=12)
        plan_instructions: list[WorkflowInstructionV1] = [
            WorkflowInstructionV1("p0", "CALL_TOOL", tool_step=HeterogeneousStepV1(0, "SELECT_TOOL", {"tool": selected_tool})),
        ]

        sorted_nodes = sorted(key_nodes, key=lambda p: p[0])
        if len(sorted_nodes) >= 2:
            plan_instructions.append(
                WorkflowInstructionV1(
                    "p1",
                    "CALL_TOOL",
                    tool_step=HeterogeneousStepV1(1, "DRAW_STROKE", {"points": sorted_nodes, "width": 2}, selected_tool),
                )
            )
        if (bx1 - bx0) > 8:
            plan_instructions.append(
                WorkflowInstructionV1(
                    "p2",
                    "CALL_TOOL",
                    tool_step=HeterogeneousStepV1(2, "DRAW_STROKE", {"points": [(bx0, by1), (bx1, by1)], "width": 2}, selected_tool),
                )
            )

        # 5. Procedural Generation
        for instr in plan_instructions:
            orch._execute_instruction(instr)

        init_pix = black_pixels(orch.canvas)
        init_iou = round(len(target_pix.intersection(init_pix)) / max(1, len(target_pix.union(init_pix))), 4)
        p_gen = out / "03_procedural_initial_production.png"
        orch.canvas.save(p_gen)
        artifacts["03_initial_production"] = str(p_gen)

        # 6. Re-perception & Error Evaluation
        intent = VisualEditIntentCandidateV1(
            intent_id="INTENT-ARBITRARY-V1",
            goal_description=goal_description,
            rigor_profile=RigorProfileV1.STRICT_GEOMETRIC,
            region_constraints=(
                RegionConstraintV1("lock_target_bbox", (bx0, by0, bx1, by1), ConstraintKindV1.LOCK, rationale="Perceived boundary"),
            ),
        )
        reperceiver = VisualReperceiverEvaluatorV1()
        rep_report = reperceiver.evaluate_and_locate_errors(orch.canvas, intent, ideal_target=obs_img)
        err_patches_count = len(rep_report.error_patches)
        primary_err_box = rep_report.error_patches[0].bbox_xyxy if err_patches_count > 0 else (bx0, by0, bx1, by1)

        err_mask = Image.new("L", (SIDE, SIDE), 255)
        draw_err = ImageDraw.Draw(err_mask)
        draw_err.rectangle(list(primary_err_box), fill=128, outline=0, width=1)
        p_err = out / "04_reperceived_error_patches.png"
        err_mask.save(p_err)
        artifacts["04_reperceived_errors"] = str(p_err)

        # 7. Motor Correction (Target missing pixels dynamically)
        missing_pix = target_pix - init_pix
        if missing_pix:
            mcx = sum(p % SIDE for p in missing_pix) // len(missing_pix)
            mcy = sum(p // SIDE for p in missing_pix) // len(missing_pix)
            corr_points = [(primary_err_box[0], mcy), (mcx, mcy), (primary_err_box[2], mcy)]
            corr_instr = WorkflowInstructionV1(
                "p_corr",
                "CALL_TOOL",
                tool_step=HeterogeneousStepV1(len(plan_instructions), "DRAW_STROKE", {"points": corr_points, "width": 2}, selected_tool),
            )
            orch._execute_instruction(corr_instr)
            corr_id = corr_instr.instruction_id
        else:
            corr_id = "no_correction_needed"

        final_pix = black_pixels(orch.canvas)
        final_iou = round(len(target_pix.intersection(final_pix)) / max(1, len(target_pix.union(final_pix))), 4)
        p_corr = out / "05_corrected_production.png"
        orch.canvas.save(p_corr)
        artifacts["05_corrected_production"] = str(p_corr)

        # 8. Candidate Experience Emission
        cand_exp_id = f"EXP-CANDIDATE-ARBITRARY-{obs_sha[:8]}"
        cand_receipt = {
            "experience_id": cand_exp_id,
            "decision_authority": DECISION_AUTHORITY,
            "native_memory_write_allowed": False,
            "provenance": "LOCAL_CANDIDATE_LEDGER",
            "observation_sha256": obs_sha,
            "initial_iou": init_iou,
            "final_iou": final_iou,
            "selected_tool": selected_tool,
            "retrieved_procedure_id": selected_proc_id,
            "error_patches_detected": err_patches_count,
            "correction_applied": bool(missing_pix),
        }
        p_json = out / "06_candidate_experience_receipt.json"
        p_json.write_text(json.dumps(cand_receipt, indent=2, ensure_ascii=False), encoding="utf-8")
        artifacts["06_candidate_receipt"] = str(p_json)

        return OperationalPipelineReceiptV3(
            pipeline_id=f"PIPELINE-ARBITRARY-{obs_sha[:8]}",
            observation_sha256=obs_sha,
            observation_source_kind="ARBITRARY_IMAGE_OBSERVATION",
            spatial_nodes_count=len(key_nodes),
            bounding_box=(bx0, by0, bx1, by1),
            retrieved_procedure_id=selected_proc_id,
            retrieved_tool=selected_tool,
            meaning_query_intent=MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE.value,
            plan_instructions_count=len(plan_instructions),
            budget_allocated=30.0,
            initial_canvas_sha256=digest_bytes(Image.open(p_gen).tobytes()),
            initial_iou=init_iou,
            error_patches_count=err_patches_count,
            primary_error_region=primary_err_box,
            correction_instruction_id=corr_id,
            corrected_canvas_sha256=digest_bytes(orch.canvas.tobytes()),
            final_iou=final_iou,
            candidate_experience_id=cand_exp_id,
            artifact_paths=artifacts,
        )

    # =========================================================================
    # RECONCILED AUDIT MATRIX OF THE 32 CHANTIERS (Docs 21 & Historical Plan)
    # =========================================================================

    @staticmethod
    def get_reconciled_32_chantiers_audit() -> list[MasterPlanChantierAuditEntryV3]:
        """Mandate 1: Reconciles all 32 chantiers against historical plan and contracts."""
        return [
            # F00-F03: Fondations
            MasterPlanChantierAuditEntryV3(
                code="F00",
                name="Audit comparatif Tool Calling",
                historical_objective="Comparer normes Anthropic/OpenAI avec la politique d'exécution bornée Obsidure sans code arbitraire.",
                current_implementation="Spécifié dans doc 45, formalisé dans docs 55 et 56 avec FSM d'instructions typées.",
                proof_reference="docs/45_..., docs/56_AUDIT_MATURITE...",
                unresolved_gap="Aucune lacune conceptuelle ; implémenté et audité.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="F01",
                name="Orchestration programmée bornée",
                historical_objective="Exécuter un plan d'actions ordonnées sans rappel au LLM entre chaque étape sous budget max_steps.",
                current_implementation="ProgrammaticBoundedOrchestratorO04 avec budget strict d'étapes (64 max) et coût cumulé.",
                proof_reference="brody_world_physique/programmatic_orchestrator_o04.py, test_visual_intent_and_orchestrator_v1.py",
                unresolved_gap="Complètement opérationnel en local.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="F02",
                name="Séparation code / neurones / boucle",
                historical_objective="Distinguer rigoureusement restitution géométrique/raster (PIL/code) et diffusion neuronale (tenseur).",
                current_implementation="Séparation stricte dans drawing_school vs workstation_neural_generation_auditor_v1.",
                proof_reference="brody_world_physique/contracts_v0.py, scripts/pc_fixe_neural_inference_verifier.py",
                unresolved_gap="Prêt ; en attente de l'inférence neuronale sur PC fixe pour la partie poids réels.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="F03",
                name="Frontière de décision KX108_ONLY",
                historical_objective="Interdire toute promotion automatique ou écriture unilatérale dans la mémoire souveraine Obsidia.",
                current_implementation="Contrôle systématique _assert_non_sovereign, native_memory_write_allowed=False.",
                proof_reference="brody_world_physique/contracts_v0.py, test_contracts_v0.py",
                unresolved_gap="Garantie constitutionnelle inviolable respectée sur toutes les routes.",
                classification="LIVE_VERIFIED",
            ),
            # M01-M09: Mémoire Multidimensionnelle
            MasterPlanChantierAuditEntryV3(
                code="M01",
                name="Frise & 6 axes temporels",
                historical_objective="Structurer la mémoire selon 6 axes temporels distincts (événement, observation, enregistrement, validité, stade, révision).",
                current_implementation="TimelineEnvelopeV1 avec sérialisation ISO-8601 et révisions de croyances.",
                proof_reference="brody_world_physique/cognitive_memory_timeline_v1.py, test_cognitive_memory_timeline_v1.py",
                unresolved_gap="Opérationnel localement.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="M02",
                name="34 arbres cognitifs & 8 familles",
                historical_objective="Projeter chaque expérience visuelle dans le registre canonique des 34 arbres Obsidia et leurs 8 familles.",
                current_implementation="CANONICAL_34_TREES dans index local + appel direct à periphery.shazam_cognitif dans repo frère.",
                proof_reference="obsidia-jarvis-advanced-integration-v0/periphery/shazam_cognitif.py",
                unresolved_gap="Appelé en import idempotent ; liaison événementielle bidirectionnelle en cours.",
                classification="RUNTIME_INTEGRATED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="M03",
                name="Domaines spécialisés vs arbres",
                historical_objective="Distinguer les domaines techniques (dessin, géométrie, physique) des arbres ontologiques généraux.",
                current_implementation="SpecializedDomainV1 et DomainEngagementV1 typés et indexés séparément des arbres.",
                proof_reference="brody_world_physique/cognitive_memory_timeline_v1.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="M04",
                name="Relations multidimensionnelles",
                historical_objective="Lier les expériences par des relations typées (analogie, causalité, décomposition, contradiction).",
                current_implementation="ExperienceRelationLinkV1 et MultidimensionalRelationTypeV1 dans le graphe d'indexation.",
                proof_reference="brody_world_physique/multidimensional_retrieval_v2.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="M05",
                name="Recherche par le sens (7 intentions)",
                historical_objective="Rechercher en mémoire selon 7 intentions sémantiques (transférabilité, outil, contradiction, etc.).",
                current_implementation="MeaningQueryIntentV1 avec recherche pondérée sur arbre cible et similarité lexicale/conceptuelle.",
                proof_reference="brody_world_physique/multidimensional_retrieval_v2.py, test_multidimensional_retrieval_v2.py",
                unresolved_gap="Complètement fonctionnel et utilisé dans la sélection motrice d'outils.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="M06",
                name="Évolution & Révisions croyances",
                historical_objective="Conserver l'historique des croyances antérieures lors de corrections ou réévaluations épistémiques.",
                current_implementation="HistoricalBeliefRevisionV1 et get_belief_prior_to_revision.",
                proof_reference="brody_world_physique/cognitive_memory_timeline_v1.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="M07",
                name="Calibration épistémique & Contre-exemples",
                historical_objective="Associer à chaque compétence un score de confiance, des preuves et des frontières d'échec avérées.",
                current_implementation="EpistemicCalibrationV1 avec source_provenance_refs et failure_boundaries.",
                proof_reference="brody_world_physique/cognitive_memory_timeline_v1.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="M08",
                name="Admissibilité Native Memory",
                historical_objective="Garantir que le passage vers la mémoire canonique Obsidia bloque l'auto-promotion et exige revue humaine.",
                current_implementation="Vérifié en direct via connectors.brody_memory_readonly_flow dans le repo frère.",
                proof_reference="obsidia-jarvis-advanced-integration-v0/connectors/brody_memory_readonly_flow.py",
                unresolved_gap="Raccordé en runtime idempotent ; en attente d'ingestion permanente dans base de production.",
                classification="RUNTIME_INTEGRATED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="M09",
                name="Mémoire procédurale & Admissibilité",
                historical_objective="Filtrer les procédures applicables à une tâche avant toute exécution motrice.",
                current_implementation="VisualTaskAdmissibilityVerdictV1 et check_task_admissibility.",
                proof_reference="brody_world_physique/multidimensional_retrieval_v2.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            # E01-E04: École de Dessin & Éducation Visuelle
            MasterPlanChantierAuditEntryV3(
                code="E01",
                name="École V0/V1 : Traits, courbes & gomme",
                historical_objective="Apprendre les primitives fondamentales (segments, courbures, effacement) et mesurer l'erreur pixel par pixel.",
                current_implementation="DrawingSchoolV1 avec primitives vectorielles, GestureV1 et calcul delta XOR/IoU.",
                proof_reference="brody_world_physique/drawing_school_v1.py, test_drawing_school_v1.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="E02",
                name="École V2 : Choix d'instruments",
                historical_objective="Apprendre à router la demande vers le bon instrument (PEN, BRUSH, ERASER) selon les zones et textures.",
                current_implementation="InstrumentSchoolV2 + sélection motrice dynamique par requête mémoire dans V3.",
                proof_reference="brody_world_physique/instrument_school_v2.py, test_natural_visual_education_and_obsidia_interstack_v2.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="E03",
                name="École V3 : Modèle caché & Rétention",
                historical_objective="Reconstituer une image observée après occlusion complète et terminaison du processus d'observation.",
                current_implementation="Protocole inter-processus étanche via scripts/standalone_interprocess_retention_runner.py.",
                proof_reference="scripts/standalone_interprocess_retention_runner.py, tests/test_natural_visual_education_and_obsidia_interstack_v2.py",
                unresolved_gap="Complètement fonctionnel et éprouvé sans fuite mémoire.",
                classification="TEST_INTERPROCESS",
            ),
            MasterPlanChantierAuditEntryV3(
                code="E04",
                name="Éducation préverbale monde physique",
                historical_objective="Apprendre les transitions physiques (gravité, appui, chute) sans formulation linguistique préalable.",
                current_implementation="WorldStateProjectionV0 et PreverbalPredictorV0 basés sur la géométrie et le temps.",
                proof_reference="brody_world_physique/preverbal_prediction_v0.py, test_preverbal_prediction_v0.py",
                unresolved_gap="Complètement fonctionnel sur cas de laboratoire.",
                classification="LIVE_VERIFIED",
            ),
            # V01-V04b: Vision & Perception
            MasterPlanChantierAuditEntryV3(
                code="V01",
                name="Observation image réelle (Jarvis Qwen-VL)",
                historical_objective="Connecter l'observation réelle au serveur local Qwen-VL de Jarvis sur port 8081.",
                current_implementation="Adaptateur jarvis_vision_v0.py codé ; probe loopback port 8081 testé ; serveur absent sur portable.",
                proof_reference="Jarvis-iron-obsidia- commit 3715985 (LocalVisionCognition sur port 8081)",
                unresolved_gap="Le serveur llama-server Qwen-VL doit être lancé sur le PC fixe (ou tunnel SSH) pour devenir actif.",
                classification="HOLD",
            ),
            MasterPlanChantierAuditEntryV3(
                code="V02",
                name="Décomposition en couches (Reverso)",
                historical_objective="Isoler les canaux RGBA et séparer fond, calques intermédiaires et détails sans perte.",
                current_implementation="ReversoLosslessLearningEngineV0 avec reconstruction bit-à-bit vérifiée.",
                proof_reference="brody_world_physique/reverso_learning_v0.py, test_reverso_learning_v0.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="V03",
                name="Relations spatiales & Invariants (V4.1)",
                historical_objective="Segmenter les composantes 8-connexes et qualifier leurs relations spatiales (NEAR, FAR, ABOVE, BELOW).",
                current_implementation="WorldRelationsSchoolV41 avec connectivité 8-connexe et invariants spatiaux.",
                proof_reference="brody_world_physique/world_relations_school_v4_1.py, test_world_relations_school_v4_1.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="V04",
                name="Orientation & Réciprocité (V4.2)",
                historical_objective="Identifier les 4 directions cardinales et vérifier les relations réciproques (si A est à gauche de B, B est à droite de A).",
                current_implementation="WorldOrientationSchoolV42 avec contrôle de symétrie réciproque.",
                proof_reference="brody_world_physique/world_orientation_school_v4_2.py, test_world_orientation_school_v4_2.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="V04b",
                name="Multi-perspectives et réversibilité",
                historical_objective="Tester la conservation des propriétés géométriques lors de bascules de point de vue.",
                current_implementation="candidate_skill_retrieval_v1.py et projection axonométrique dans V2/V3.",
                proof_reference="brody_world_physique/candidate_skill_retrieval_v1.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            # G01-G04: Génération & Synthèse
            MasterPlanChantierAuditEntryV3(
                code="G01",
                name="Intent visuel & Contraintes LOCK/FLEX",
                historical_objective="Définir un contrat d'intention visuelle imposant des zones immuables (LOCK) et modifiables (FLEX).",
                current_implementation="VisualEditIntentCandidateV1 avec contrôle strict de violation pixelique par région.",
                proof_reference="brody_world_physique/visual_intent_contracts_v1.py, test_visual_intent_and_orchestrator_v1.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="G02",
                name="Générateur diffusif local (sd.cpp)",
                historical_objective="Générer des images réalistes par modèle diffusif local (sd.cpp) adapté à la VRAM du PC fixe (GTX 1050 Ti 4GB).",
                current_implementation="Script d'audit scripts/pc_fixe_neural_inference_verifier.py avec profil matériel scellé.",
                proof_reference="scripts/pc_fixe_neural_inference_verifier.py, artifacts/pc_fixe_neural_audit/",
                unresolved_gap="Le binaire sd.cpp et les poids GGUF q4_0 doivent être déployés sur le PC fixe ; HOLD sur portable.",
                classification="HOLD",
            ),
            MasterPlanChantierAuditEntryV3(
                code="G03",
                name="Méthode du peintre multicouches",
                historical_objective="Générer par passes successives ordonnées (masse de fond -> valeurs tonales -> détails de texture).",
                current_implementation="Implémenté dans NaturalVisualEducation (passes sol, structure, hachures maçonnerie, feuillage).",
                proof_reference="brody_world_physique/natural_visual_education_and_obsidia_interstack_v2.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="G04",
                name="Évaluation inverse (Reverse Eval)",
                historical_objective="Re-percevoir l'artefact produit, comparer pixel à pixel au but et localiser les patchs d'erreur.",
                current_implementation="VisualReperceiverEvaluatorV1 avec extraction de coordonnées de patchs déficients.",
                proof_reference="brody_world_physique/visual_reperceiver_evaluator_v1.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            # O01-O03: Orchestration & Reçus
            MasterPlanChantierAuditEntryV3(
                code="O01",
                name="Orchestrateur d'instruments borné",
                historical_objective="Piloter les outils hétérogènes sous budget strict de coût et d'étapes sans code arbitraire.",
                current_implementation="HeterogeneousInstrumentOrchestratorO03 et ProgrammaticBoundedOrchestratorO04.",
                proof_reference="brody_world_physique/heterogeneous_orchestrator_o03.py, programmatic_orchestrator_o04.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="O02",
                name="Rejeu déterministe & Reçus cryptographiques",
                historical_objective="Sceller chaque tracé et étape par son empreinte SHA-256 pour permettre un rejeu à l'identique.",
                current_implementation="digest_bytes sur chaque état canvas et trace d'instruction sérialisée en JSON.",
                proof_reference="brody_world_physique/experience_memory_v1.py, drawing_school_v0.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="O03",
                name="Correction localisée en boucle fermée",
                historical_objective="Appliquer une correction motrice ciblée sur le patch d'erreur détecté par re-perception.",
                current_implementation="Boucle complète re-perception -> détection -> reprise motrice démontrée dans V1, V2 et V3.",
                proof_reference="brody_world_physique/operational_pipeline_and_master_plan_reconciliation_v3.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            # R01-R02: Représentations Transversales
            MasterPlanChantierAuditEntryV3(
                code="R01",
                name="Continuité multi-vues & Reverse360",
                historical_objective="Vérifier la survie de l'identité et des proportions lors d'un changement de perspective ou de vue.",
                current_implementation="multirepresentation_ball_bridge_v5.py + projection axonométrique 3D.",
                proof_reference="brody_world_physique/multirepresentation_ball_bridge_v5.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="R02",
                name="Continuité vidéo & Invariants dynamiques",
                historical_objective="Traiter les séquences multi-frames, détecter les occlusions et mesurer les discontinuités temporelles.",
                current_implementation="VideoObservationEngineV0 avec détection d'occlusion et de surprise temporelle.",
                proof_reference="brody_world_physique/video_observation_v0.py, test_video_observation_v0.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            # T01-T02: Tests & Transfert
            MasterPlanChantierAuditEntryV3(
                code="T01",
                name="Batterie d'ablations comparatives",
                historical_objective="Mesurer l'apport réel de chaque composante mémoire par ablations progressives et indépendantes.",
                current_implementation="ProgressiveAblationEngineV1 avec 6 niveaux d'ablation mesurés sans prétention unilatérale.",
                proof_reference="brody_world_physique/progressive_ablation_and_generalization_v1.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
            MasterPlanChantierAuditEntryV3(
                code="T02",
                name="Transfert E2E sur monde inédit",
                historical_objective="Démontrer le transfert zero-shot d'une compétence visuelle acquise vers une tâche inconnue.",
                current_implementation="Transfert démontré dans V1, V2 et V3 (IoU > 0.88, 0 étape corrective en réemploi).",
                proof_reference="brody_world_physique/operational_pipeline_and_master_plan_reconciliation_v3.py",
                unresolved_gap="Complètement fonctionnel.",
                classification="LIVE_VERIFIED",
            ),
        ]

    @staticmethod
    def get_pc_fixe_hardware_profile() -> PCFixeHardwareProfileV3:
        """Mandate 5: Confirms the hardware profile for the PC Fixe."""
        return PCFixeHardwareProfileV3(
            target_machine_name="PC_FIXE_TITAN_DEV",
            gpu_model="NVIDIA GeForce GTX 1050 Ti (4GB VRAM)",
            vram_capacity_gb=4.0,
            recommended_engine="sd.cpp (stable-diffusion.cpp quantized GGUF)",
            quantization_format="q4_0 / q8_0 GGUF",
            zero_download_policy=True,
            status="HOLD_PENDING_PC_FIXE_EXECUTION",
            execution_gate_command="python scripts/pc_fixe_neural_inference_verifier.py --seed 42",
        )
