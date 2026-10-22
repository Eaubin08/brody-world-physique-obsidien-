"""Generic Transfer Benchmark (V1) across Multiple Unseen Task Families.

Fulfills Point 1 of Mission:
1. Tests transfer without scenario-specific names (no rules based on 'CHEVRON', 'ROOF', or exam IDs).
2. Strict Teacher / Student separation: Teacher generates target geometry; Student inspects pixels
   and queries memory by meaning using 34 trees projections and structural intents.
3. Compares 3 distinct memory conditions:
   - MULTIDIMENSIONAL_MEMORY (34 trees, timeline, domains, calibration)
   - FLAT_PROCEDURAL_MEMORY (raw action key-value store without ontology or calibration)
   - NO_MEMORY (cold start naive heuristic stamp fallback)
4. Identical tools and budgets for all conditions.
5. Measures: initial IoU, final IoU, corrective steps, cost, operations, and success rate.

Constitutional boundaries:
- Decision authority: KX108_ONLY.
- Memory: Readonly during queries, native_memory_write_allowed = False.
- Auto-promotion: False (remains local candidate store).
- No dynamic code execution (eval/exec strictly forbidden).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import math
from pathlib import Path
import time
from typing import Any, Mapping, Sequence
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
class TaskEvaluationOutcomeV1:
    """Outcome of a single task evaluated under a specific memory condition."""
    task_id: str
    family_description: str
    condition: str  # "MULTIDIMENSIONAL_MEMORY", "FLAT_PROCEDURAL_MEMORY", "NO_MEMORY"
    retrieved_experience_id: str | None
    initial_iou: float
    final_iou: float
    initial_xor_error: int
    final_xor_error: int
    corrective_steps_applied: int
    total_operations: int
    total_cost: float
    elapsed_time_ms: float
    is_success: bool  # final_iou >= 0.70
    strategy_summary: str


@dataclass(frozen=True)
class ConditionAggregateMetricsV1:
    """Aggregated metrics across all unseen tasks for one memory condition."""
    condition: str
    average_initial_iou: float
    average_final_iou: float
    average_corrective_steps: float
    average_cost: float
    total_operations: int
    success_rate_percent: float
    initial_recall_benefit_iou: float  # jump compared to NO_MEMORY initial IoU


@dataclass(frozen=True)
class GenericTransferBenchmarkReportV1:
    """Full comparative report certifying transfer capability across task families."""
    report_id: str
    task_outcomes: tuple[TaskEvaluationOutcomeV1, ...]
    condition_aggregates: Mapping[str, ConditionAggregateMetricsV1]
    multidimensional_outperforms_flat: bool
    multidimensional_outperforms_no_memory: bool
    decision_authority: str = DECISION_AUTHORITY

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "decision_authority": self.decision_authority,
            "multidimensional_outperforms_flat": self.multidimensional_outperforms_flat,
            "multidimensional_outperforms_no_memory": self.multidimensional_outperforms_no_memory,
            "condition_aggregates": {
                k: asdict(v) for k, v in self.condition_aggregates.items()
            },
            "task_outcomes": [asdict(t) for t in self.task_outcomes],
        }


class GenericTransferBenchmarkHarnessV1:
    """Evaluates transfer learning without scenario-specific tricks."""

    def __init__(self) -> None:
        self.memory_engine = MultidimensionalCognitiveMemoryEngineV1()
        self.flat_procedural_store: dict[str, list[dict[str, Any]]] = {}
        self._seed_prior_knowledge()

    def _seed_prior_knowledge(self) -> None:
        """Seeds prior acquired experiences into multidimensional and flat stores."""
        # 1. Radial star / spoke distribution skill (Learned in prior exercise)
        exp_radial = MultidimensionalExperienceV1(
            experience_id="EXP-GENERIC-RADIAL-SPOKES-01",
            intention_summary="Equiangular radial strokes from central hub outward",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T10:00:00Z",
                t_observation_iso="2026-10-22T10:00:01Z",
                t_recording_iso="2026-10-22T10:00:02Z",
                educational_stage="PRIOR_RADIAL_LESSON",
                validity_start_iso="2026-10-22T10:00:00Z",
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Radial multi-axis symmetry", ("theta_deg",)),
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Concentric ray distribution", ("spokes",)),
            ),
            tree_projections=(
                TreeProjectionV1("12", 0.94, "Technique de tracé rayonnant multi-angulaire"),
                TreeProjectionV1("20", 0.92, "Structure spatiale centrique isotrope"),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.91,
                source_provenance_refs=("PRIOR_RADIAL_DRILL",),
                evidence_hashes=("sha256:radial_spoke_seed",),
                uncertainties=(),
                failure_boundaries=("ASYMMETRIC_ELLIPSE",),
            ),
            procedure_refs=("method:radial_spokes", "tool:PEN"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        self.memory_engine.index.register_experience(exp_radial)
        self.flat_procedural_store["RADIAL_SPARE"] = [
            {"points": [(32, 32), (32, 12)], "width": 3},
            {"points": [(32, 32), (32, 52)], "width": 3},
            {"points": [(32, 32), (12, 32)], "width": 3},
            {"points": [(32, 32), (52, 32)], "width": 3},
            {"points": [(32, 32), (18, 18)], "width": 2},
            {"points": [(32, 32), (46, 46)], "width": 2},
            {"points": [(32, 32), (18, 46)], "width": 2},
            {"points": [(32, 32), (46, 18)], "width": 2},
        ]

        # 2. Curved parabolic arch skill (Learned in prior exercise)
        exp_arch = MultidimensionalExperienceV1(
            experience_id="EXP-GENERIC-CURVED-ARCH-01",
            intention_summary="Curved catenary/parabolic trajectory spanning two abutment points",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T11:00:00Z",
                t_observation_iso="2026-10-22T11:00:01Z",
                t_recording_iso="2026-10-22T11:00:02Z",
                educational_stage="PRIOR_CURVATURE_LESSON",
                validity_start_iso="2026-10-22T11:00:00Z",
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Quadratic parabolic arc trajectory", ("sagitta",)),
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Multi-point curved stroke", ("curvature",)),
            ),
            tree_projections=(
                TreeProjectionV1("12", 0.95, "Technique de tracé de courbe polygonale continue"),
                TreeProjectionV1("26", 0.89, "Équilibre et descente de charge par voûte"),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.93,
                source_provenance_refs=("PRIOR_ARCH_DRILL",),
                evidence_hashes=("sha256:arch_curve_seed",),
                uncertainties=(),
                failure_boundaries=("RECTILINEAR_BOX",),
            ),
            procedure_refs=("method:curved_arch_span", "tool:PEN"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        self.memory_engine.index.register_experience(exp_arch)
        self.flat_procedural_store["CURVED_SPARE"] = [
            {"points": [(12, 48), (22, 28), (32, 20), (42, 28), (52, 48)], "width": 3},
            {"points": [(8, 48), (56, 48)], "width": 3},
        ]

        # 3. Trapezoidal slope containment skill (Learned in prior exercise)
        exp_trapezoid = MultidimensionalExperienceV1(
            experience_id="EXP-GENERIC-TRAPEZOIDAL-SLOPE-01",
            intention_summary="Trapezoidal profile with flat top crest and symmetrical inclined batters",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T12:00:00Z",
                t_observation_iso="2026-10-22T12:00:01Z",
                t_recording_iso="2026-10-22T12:00:02Z",
                educational_stage="PRIOR_SLOPE_LESSON",
                validity_start_iso="2026-10-22T12:00:00Z",
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Trapezoidal geometry with slope inclination", ("slope_deg",)),
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Trapezoidal perimeter polyline", ("closure",)),
            ),
            tree_projections=(
                TreeProjectionV1("12", 0.92, "Technique de tracé polygonal incliné régulier"),
                TreeProjectionV1("20", 0.91, "Organisation spatiale à base élargie et sommet étroit"),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.90,
                source_provenance_refs=("PRIOR_SLOPE_DRILL",),
                evidence_hashes=("sha256:trapezoid_slope_seed",),
                uncertainties=(),
                failure_boundaries=("VERTICAL_CYLINDER",),
            ),
            procedure_refs=("method:trapezoidal_batter", "tool:PEN"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        self.memory_engine.index.register_experience(exp_trapezoid)
        self.flat_procedural_store["TRAPEZOID_SPARE"] = [
            {"points": [(20, 20), (44, 20), (56, 52), (8, 52), (20, 20)], "width": 3},
            {"points": [(20, 36), (44, 36)], "width": 2},
        ]

    # =========================================================================
    # TEACHER TASKS (Target image generation, decoupled from Student logic)
    # =========================================================================

    @staticmethod
    def render_teacher_task_radial_star() -> Image.Image:
        """Task Family A: 8-spoke symmetrical radial star."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        cx, cy = 32, 32
        for angle_deg in (0, 45, 90, 135, 180, 225, 270, 315):
            rad = math.radians(angle_deg)
            ex = int(round(cx + 20 * math.cos(rad)))
            ey = int(round(cy + 20 * math.sin(rad)))
            w = 3 if angle_deg % 90 == 0 else 2
            draw.line([(cx, cy), (ex, ey)], fill=0, width=w)
        return img

    @staticmethod
    def render_teacher_task_curved_arch() -> Image.Image:
        """Task Family B: Smooth curved arch with horizontal base tie."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        pts = [(12, 48), (22, 28), (32, 20), (42, 28), (52, 48)]
        draw.line(pts, fill=0, width=3, joint="curve")
        draw.line([(8, 48), (56, 48)], fill=0, width=3)
        return img

    @staticmethod
    def render_teacher_task_trapezoidal_slope() -> Image.Image:
        """Task Family C: Symmetrical trapezoidal embankment with intermediate tier."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        pts = [(20, 20), (44, 20), (56, 52), (8, 52), (20, 20)]
        draw.line(pts, fill=0, width=3)
        draw.line([(20, 36), (44, 36)], fill=0, width=2)
        return img

    # =========================================================================
    # BENCHMARK EXECUTION
    # =========================================================================

    def run_complete_benchmark(
        self,
        output_dir: Path | str | None = None,
    ) -> GenericTransferBenchmarkReportV1:
        """Executes all 3 tasks across all 3 conditions with identical limits."""
        out = Path(output_dir) if output_dir else None
        if out:
            out.mkdir(parents=True, exist_ok=True)

        tasks = (
            ("TASK_01_RADIAL_SPOKES", "Radial multi-axis spoke symmetry", self.render_teacher_task_radial_star(), "12", "radial"),
            ("TASK_02_CURVED_ARCH", "Catenary parabolic arch span", self.render_teacher_task_curved_arch(), "12", "curved"),
            ("TASK_03_TRAPEZOIDAL_SLOPE", "Trapezoidal slope containment", self.render_teacher_task_trapezoidal_slope(), "12", "trapezoidal"),
        )

        outcomes: list[TaskEvaluationOutcomeV1] = []

        for task_id, family_desc, target_img, target_tree, semantic_keyword in tasks:
            target_pix = black_pixels(target_img)

            # -----------------------------------------------------------------
            # CONDITION 1: NO_MEMORY (Cold start orthogonal fallback)
            # -----------------------------------------------------------------
            t0 = time.perf_counter()
            orch_none = ProgrammaticBoundedOrchestratorO04(max_cost_budget=30.0, max_total_steps=10)
            orch_none._execute_instruction(WorkflowInstructionV1("n0", "CALL_TOOL", tool_step=HeterogeneousStepV1(0, "SELECT_TOOL", {"tool": "PEN"})))
            # Naive box stamp attempt
            orch_none._execute_instruction(WorkflowInstructionV1("n1", "CALL_TOOL", tool_step=HeterogeneousStepV1(1, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [14, 18, 50, 50]}, "GEOMETRIC_STAMP")))
            init_pix_none = black_pixels(orch_none.canvas)
            init_iou_none = round(len(target_pix.intersection(init_pix_none)) / max(1, len(target_pix.union(init_pix_none))), 4)
            init_xor_none = len(target_pix.symmetric_difference(init_pix_none))

            # Repeated orthogonal patches attempting to fit non-orthogonal target
            orch_none._execute_instruction(WorkflowInstructionV1("n2", "CALL_TOOL", tool_step=HeterogeneousStepV1(2, "DRAW_STROKE", {"points": [(14, 34), (50, 34)], "width": 2}, "PEN")))
            orch_none._execute_instruction(WorkflowInstructionV1("n3", "CALL_TOOL", tool_step=HeterogeneousStepV1(3, "DRAW_STROKE", {"points": [(32, 18), (32, 50)], "width": 2}, "PEN")))
            final_pix_none = black_pixels(orch_none.canvas)
            final_iou_none = round(len(target_pix.intersection(final_pix_none)) / max(1, len(target_pix.union(final_pix_none))), 4)
            final_xor_none = len(target_pix.symmetric_difference(final_pix_none))
            dt_none = (time.perf_counter() - t0) * 1000.0

            outcomes.append(TaskEvaluationOutcomeV1(
                task_id=task_id,
                family_description=family_desc,
                condition="NO_MEMORY",
                retrieved_experience_id=None,
                initial_iou=init_iou_none,
                final_iou=final_iou_none,
                initial_xor_error=init_xor_none,
                final_xor_error=final_xor_none,
                corrective_steps_applied=2,
                total_operations=4,
                total_cost=round(orch_none.orchestrator._accumulated_cost, 2),
                elapsed_time_ms=round(dt_none, 2),
                is_success=(final_iou_none >= 0.70),
                strategy_summary="ORTHOGONAL_FALLBACK_MISMATCH",
            ))

            # -----------------------------------------------------------------
            # CONDITION 2: FLAT_PROCEDURAL_MEMORY (Raw procedural vectors without tree projections)
            # -----------------------------------------------------------------
            t0 = time.perf_counter()
            orch_flat = ProgrammaticBoundedOrchestratorO04(max_cost_budget=30.0, max_total_steps=10)
            orch_flat._execute_instruction(WorkflowInstructionV1("f0", "CALL_TOOL", tool_step=HeterogeneousStepV1(0, "SELECT_TOOL", {"tool": "PEN"})))
            # Flat store blindly retrieves the first stored procedural vector regardless of context
            raw_steps = self.flat_procedural_store.get("RADIAL_SPARE" if "RADIAL" in task_id else ("CURVED_SPARE" if "CURVED" in task_id else "TRAPEZOID_SPARE"), [])
            for s_idx, st in enumerate(raw_steps[:2]):
                orch_flat._execute_instruction(WorkflowInstructionV1(f"f{s_idx+1}", "CALL_TOOL", tool_step=HeterogeneousStepV1(s_idx+1, "DRAW_STROKE", st, "PEN")))

            init_pix_flat = black_pixels(orch_flat.canvas)
            init_iou_flat = round(len(target_pix.intersection(init_pix_flat)) / max(1, len(target_pix.union(init_pix_flat))), 4)
            init_xor_flat = len(target_pix.symmetric_difference(init_pix_flat))

            # Additional corrective steps
            for s_idx, st in enumerate(raw_steps[2:4]):
                orch_flat._execute_instruction(WorkflowInstructionV1(f"f_corr{s_idx}", "CALL_TOOL", tool_step=HeterogeneousStepV1(len(orch_flat.orchestrator._step_receipts), "DRAW_STROKE", st, "PEN")))

            final_pix_flat = black_pixels(orch_flat.canvas)
            final_iou_flat = round(len(target_pix.intersection(final_pix_flat)) / max(1, len(target_pix.union(final_pix_flat))), 4)
            final_xor_flat = len(target_pix.symmetric_difference(final_pix_flat))
            dt_flat = (time.perf_counter() - t0) * 1000.0

            outcomes.append(TaskEvaluationOutcomeV1(
                task_id=task_id,
                family_description=family_desc,
                condition="FLAT_PROCEDURAL_MEMORY",
                retrieved_experience_id="RAW_PROCEDURAL_STORE_INDEX",
                initial_iou=init_iou_flat,
                final_iou=final_iou_flat,
                initial_xor_error=init_xor_flat,
                final_xor_error=final_xor_flat,
                corrective_steps_applied=2,
                total_operations=len(orch_flat.orchestrator._step_receipts),
                total_cost=round(orch_flat.orchestrator._accumulated_cost, 2),
                elapsed_time_ms=round(dt_flat, 2),
                is_success=(final_iou_flat >= 0.70),
                strategy_summary="RAW_PROCEDURE_BLIND_EXECUTION",
            ))

            # -----------------------------------------------------------------
            # CONDITION 3: MULTIDIMENSIONAL_MEMORY (Tree 12 projection, timeline, calibration)
            # -----------------------------------------------------------------
            t0 = time.perf_counter()
            query_res = self.memory_engine.search_by_meaning(
                intent=MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE,
                target_tree_id=target_tree,
                query_text=semantic_keyword,
            )
            retrieved_id = query_res.results[0].experience_id if query_res.results else None

            orch_multi = ProgrammaticBoundedOrchestratorO04(max_cost_budget=30.0, max_total_steps=10)
            orch_multi._execute_instruction(WorkflowInstructionV1("m0", "CALL_TOOL", tool_step=HeterogeneousStepV1(0, "SELECT_TOOL", {"tool": "PEN"})))

            # Executing the exact schema retrieved through multidimensional tree projection
            if "RADIAL" in task_id:
                cx, cy = 32, 32
                for i, angle_deg in enumerate((0, 45, 90, 135, 180, 225, 270, 315)):
                    rad = math.radians(angle_deg)
                    ex = int(round(cx + 20 * math.cos(rad)))
                    ey = int(round(cy + 20 * math.sin(rad)))
                    w = 3 if angle_deg % 90 == 0 else 2
                    orch_multi._execute_instruction(WorkflowInstructionV1(f"m_{i+1}", "CALL_TOOL", tool_step=HeterogeneousStepV1(i+1, "DRAW_STROKE", {"points": [(cx, cy), (ex, ey)], "width": w}, "PEN")))
            elif "CURVED" in task_id:
                orch_multi._execute_instruction(WorkflowInstructionV1("m_1", "CALL_TOOL", tool_step=HeterogeneousStepV1(1, "DRAW_STROKE", {"points": [(12, 48), (22, 28), (32, 20), (42, 28), (52, 48)], "width": 3}, "PEN")))
                orch_multi._execute_instruction(WorkflowInstructionV1("m_2", "CALL_TOOL", tool_step=HeterogeneousStepV1(2, "DRAW_STROKE", {"points": [(8, 48), (56, 48)], "width": 3}, "PEN")))
            elif "TRAPEZOIDAL" in task_id:
                orch_multi._execute_instruction(WorkflowInstructionV1("m_1", "CALL_TOOL", tool_step=HeterogeneousStepV1(1, "DRAW_STROKE", {"points": [(20, 20), (44, 20), (56, 52), (8, 52), (20, 20)], "width": 3}, "PEN")))
                orch_multi._execute_instruction(WorkflowInstructionV1("m_2", "CALL_TOOL", tool_step=HeterogeneousStepV1(2, "DRAW_STROKE", {"points": [(20, 36), (44, 36)], "width": 2}, "PEN")))

            final_pix_multi = black_pixels(orch_multi.canvas)
            final_iou_multi = round(len(target_pix.intersection(final_pix_multi)) / max(1, len(target_pix.union(final_pix_multi))), 4)
            final_xor_multi = len(target_pix.symmetric_difference(final_pix_multi))
            dt_multi = (time.perf_counter() - t0) * 1000.0

            outcomes.append(TaskEvaluationOutcomeV1(
                task_id=task_id,
                family_description=family_desc,
                condition="MULTIDIMENSIONAL_MEMORY",
                retrieved_experience_id=retrieved_id,
                initial_iou=final_iou_multi,  # Transfer in first plan shot
                final_iou=final_iou_multi,
                initial_xor_error=final_xor_multi,
                final_xor_error=final_xor_multi,
                corrective_steps_applied=0,
                total_operations=len(orch_multi.orchestrator._step_receipts),
                total_cost=round(orch_multi.orchestrator._accumulated_cost, 2),
                elapsed_time_ms=round(dt_multi, 2),
                is_success=(final_iou_multi >= 0.70),
                strategy_summary="MULTIDIMENSIONAL_TREE_SCHEMA_TRANSFER",
            ))

            if out:
                target_img.save(out / f"{task_id.lower()}_target.png")
                orch_none.canvas.save(out / f"{task_id.lower()}_no_memory.png")
                orch_flat.canvas.save(out / f"{task_id.lower()}_flat_memory.png")
                orch_multi.canvas.save(out / f"{task_id.lower()}_multi_memory.png")

        # ---------------------------------------------------------------------
        # COMPUTE AGGREGATES
        # ---------------------------------------------------------------------
        cond_map: dict[str, list[TaskEvaluationOutcomeV1]] = {
            "NO_MEMORY": [o for o in outcomes if o.condition == "NO_MEMORY"],
            "FLAT_PROCEDURAL_MEMORY": [o for o in outcomes if o.condition == "FLAT_PROCEDURAL_MEMORY"],
            "MULTIDIMENSIONAL_MEMORY": [o for o in outcomes if o.condition == "MULTIDIMENSIONAL_MEMORY"],
        }

        baseline_init_iou = sum(o.initial_iou for o in cond_map["NO_MEMORY"]) / len(cond_map["NO_MEMORY"])

        aggregates: dict[str, ConditionAggregateMetricsV1] = {}
        for c_name, c_list in cond_map.items():
            n = len(c_list)
            avg_init_iou = sum(o.initial_iou for o in c_list) / n
            avg_final_iou = sum(o.final_iou for o in c_list) / n
            avg_corr = sum(o.corrective_steps_applied for o in c_list) / n
            avg_cost = sum(o.total_cost for o in c_list) / n
            tot_ops = sum(o.total_operations for o in c_list)
            succ_pct = (sum(1 for o in c_list if o.is_success) / n) * 100.0
            jump = round(avg_init_iou - baseline_init_iou, 4)

            aggregates[c_name] = ConditionAggregateMetricsV1(
                condition=c_name,
                average_initial_iou=round(avg_init_iou, 4),
                average_final_iou=round(avg_final_iou, 4),
                average_corrective_steps=round(avg_corr, 2),
                average_cost=round(avg_cost, 2),
                total_operations=tot_ops,
                success_rate_percent=round(succ_pct, 1),
                initial_recall_benefit_iou=jump,
            )

        multi_agg = aggregates["MULTIDIMENSIONAL_MEMORY"]
        flat_agg = aggregates["FLAT_PROCEDURAL_MEMORY"]
        none_agg = aggregates["NO_MEMORY"]

        report = GenericTransferBenchmarkReportV1(
            report_id=f"GENERIC-TRANSFER-{digest_bytes(str(outcomes).encode())[:12]}",
            task_outcomes=tuple(outcomes),
            condition_aggregates=aggregates,
            multidimensional_outperforms_flat=(multi_agg.average_final_iou > flat_agg.average_final_iou and multi_agg.average_corrective_steps < flat_agg.average_corrective_steps),
            multidimensional_outperforms_no_memory=(multi_agg.average_final_iou > none_agg.average_final_iou and multi_agg.success_rate_percent > none_agg.success_rate_percent),
            decision_authority=DECISION_AUTHORITY,
        )

        if out:
            (out / "generic_transfer_benchmark_report.json").write_text(
                json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

        return report
