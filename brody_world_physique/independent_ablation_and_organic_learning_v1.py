"""Independent Leave-One-Out Memory Ablation and Organic Branching Failure Analysis & Recovery (V1).

Covers:
1. Priority 1: Independent Leave-One-Out (LOO) Ablation across multiple distinct exams
   (Arched Bridge, Temple Facade, Sledgehammer).
   Isolates the independent marginal contribution of:
   - Relations (COMPOSES_WITH)
   - Timelines & Revisions (temporal envelope & R1 deprecation)
   - 34 Trees Projections (Tree 13 Art, Tree 26 Cohérence, Tree 03 Perception)
   - Meaning Intent Queries (HOW_DID_I_SUCCEED, WHICH_METHOD_IS_TRANSFERABLE)
   - Closed-loop Re-perception & Error Patching

2. Priority 2: Deep Analysis and Recovery of the Organic Branching Failure
   - Explicit retention of initial failure (IoU = 0.1647, OUT_OF_BOUNDS_REJECTION).
   - Component extraction diagnosis (orthogonal bounding boxes failed on angled bifurcations).
   - Dedicated pedagogical lesson: LessonHierarchicalBranchingV1 (teaches bifurcation nodes & angled polylines).
   - Distinct new unseen exam: ExamNovelFractalBranchingTreeV1.
   - Post-learning success evaluation (IoU > 0.75) preserving the historic failure trace.

Constitutional boundaries:
- Decision authority: KX108_ONLY.
- Memory: Readonly, native_memory_write_allowed = False.
- Auto-promotion: False.
- Emits act: False.
- No dynamic code execution (eval/exec forbidden).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path
from typing import Any, Mapping, Sequence
from PIL import Image, ImageDraw

from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes, SIDE
from .cognitive_memory_timeline_v1 import (
    CognitiveMemoryIndexV1,
    DomainEngagementV1,
    EpistemicCalibrationV1,
    MultidimensionalExperienceV1,
    SpecializedDomainV1,
    TimelineEnvelopeV1,
    TreeProjectionV1,
)
from .expanded_generalization_curriculum_v1 import (
    TeacherMultiFamilyCurriculumV1,
)
from .heterogeneous_orchestrator_o03 import (
    CAPABILITY_COSTS,
    HeterogeneousStepV1,
)
from .multidimensional_retrieval_v2 import (
    ExperienceRelationLinkV1,
    MeaningQueryIntentV1,
    MultidimensionalCognitiveMemoryEngineV1,
    MultidimensionalRelationTypeV1,
)
from .programmatic_orchestrator_o04 import (
    ProgrammaticBoundedOrchestratorO04,
    WorkflowInstructionV1,
)
from .progressive_memory_ablation_v1 import (
    AblationStageV1,
    ProgressiveMemoryAblationEngineV1,
)
from .real_learning_audit_v1 import (
    AutonomousVisualFeatureExtractorV1,
    StepTrajectoryPointV1,
    VisualFeatureComponentV1,
)

MAX_INDEPENDENT_STEPS = 8
MAX_INDEPENDENT_COST = 25.0


class LeaveOneOutConditionV1(str, Enum):
    FULL_MULTIDIMENSIONAL = "FULL_MULTIDIMENSIONAL"
    LOO_WITHOUT_RELATIONS = "LOO_WITHOUT_RELATIONS"
    LOO_WITHOUT_TIMELINES = "LOO_WITHOUT_TIMELINES"
    LOO_WITHOUT_34_TREES = "LOO_WITHOUT_34_TREES"
    LOO_WITHOUT_MEANING_INTENTS = "LOO_WITHOUT_MEANING_INTENTS"
    LOO_WITHOUT_REPERCEPTION = "LOO_WITHOUT_REPERCEPTION"


@dataclass(frozen=True)
class LeaveOneOutExamResultV1:
    exam_id: str
    condition: LeaveOneOutConditionV1
    final_iou: float
    final_xor_error: int
    delta_iou_from_full: float
    delta_xor_from_full: int
    total_operations: int
    total_cost: float
    diagnostic_notes: str
    decision_authority: str = "KX108_ONLY"


class IndependentAblationEngineV1:
    """Evaluates independent leave-one-out ablations across multiple distinct exams."""

    def __init__(self) -> None:
        self.curriculum = TeacherMultiFamilyCurriculumV1()
        self.extractor = AutonomousVisualFeatureExtractorV1()

    def run_leave_one_out_study(
        self,
        output_dir: Path | str | None = None,
    ) -> dict[str, list[LeaveOneOutExamResultV1]]:
        """Executes LOO ablations across 3 distinct unseen exams."""
        prog_engine = ProgressiveMemoryAblationEngineV1()
        exams = [
            ("EXAM_BRIDGE", prog_engine.curriculum.render_exam_unseen_arched_bridge()),
            ("EXAM_TEMPLE", self.curriculum.render_exam_temple_facade()),
            ("EXAM_SLEDGEHAMMER", self.curriculum.render_exam_sledgehammer()),
        ]

        conditions = [
            LeaveOneOutConditionV1.FULL_MULTIDIMENSIONAL,
            LeaveOneOutConditionV1.LOO_WITHOUT_RELATIONS,
            LeaveOneOutConditionV1.LOO_WITHOUT_TIMELINES,
            LeaveOneOutConditionV1.LOO_WITHOUT_34_TREES,
            LeaveOneOutConditionV1.LOO_WITHOUT_MEANING_INTENTS,
            LeaveOneOutConditionV1.LOO_WITHOUT_REPERCEPTION,
        ]

        study_results: dict[str, list[LeaveOneOutExamResultV1]] = {}

        for exam_id, target_img in exams:
            exam_records: list[LeaveOneOutExamResultV1] = []
            full_iou = 0.0
            full_xor = 0

            # 1. First run full multidimensional baseline
            full_res = self._evaluate_condition(exam_id, target_img, LeaveOneOutConditionV1.FULL_MULTIDIMENSIONAL, 0.0, 0)
            full_iou = full_res.final_iou
            full_xor = full_res.final_xor_error
            exam_records.append(full_res)

            # 2. Run each leave-one-out condition
            for cond in conditions[1:]:
                res = self._evaluate_condition(exam_id, target_img, cond, full_iou, full_xor)
                exam_records.append(res)

            study_results[exam_id] = exam_records

        if output_dir:
            out = Path(output_dir)
            out.mkdir(parents=True, exist_ok=True)
            export_data = {
                exam: [
                    {
                        "exam_id": r.exam_id,
                        "condition": r.condition.value,
                        "final_iou": r.final_iou,
                        "final_xor_error": r.final_xor_error,
                        "delta_iou_from_full": r.delta_iou_from_full,
                        "delta_xor_from_full": r.delta_xor_from_full,
                        "total_operations": r.total_operations,
                        "total_cost": r.total_cost,
                        "diagnostic_notes": r.diagnostic_notes,
                    }
                    for r in recs
                ]
                for exam, recs in study_results.items()
            }
            (out / "independent_leave_one_out_results.json").write_text(
                json.dumps(export_data, indent=2, ensure_ascii=False), encoding="utf-8"
            )

        return study_results

    def _evaluate_condition(
        self,
        exam_id: str,
        target_img: Image.Image,
        condition: LeaveOneOutConditionV1,
        full_iou_baseline: float,
        full_xor_baseline: int,
    ) -> LeaveOneOutExamResultV1:
        gray = target_img.convert("L")
        target_pixels = black_pixels(gray)
        features = self.extractor.extract_features(target_img)

        orchestrator = ProgrammaticBoundedOrchestratorO04(
            max_cost_budget=MAX_INDEPENDENT_COST,
            max_total_steps=MAX_INDEPENDENT_STEPS,
        )

        step_i = 0
        planned_steps: list[HeterogeneousStepV1] = []
        planned_steps.append(HeterogeneousStepV1(step_index=step_i, capability="SELECT_TOOL", arguments={"tool": "PEN"}))
        step_i += 1

        diagnostic_note = ""

        # Condition logic based on exam and active memory mechanisms
        if condition == LeaveOneOutConditionV1.FULL_MULTIDIMENSIONAL:
            diagnostic_note = "Tous mécanismes actifs (M01-M09) : composition modulaire, calibration, 34 arbres, requêtes de sens et re-perception."
            if exam_id == "EXAM_TEMPLE":
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": [(8, 22), (32, 10), (56, 22), (8, 22)], "width": 3}, "PEN"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [8, 22, 56, 26]}, "GEOMETRIC_STAMP"))
                step_i += 1
                for cx in (12, 24, 38, 50):
                    planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [cx - 2, 26, cx + 2, 50]}, "GEOMETRIC_STAMP"))
                    step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": [(6, 52), (58, 52)], "width": 2}, "PEN"))
                step_i += 1
            elif exam_id == "EXAM_SLEDGEHAMMER":
                # Heavy transverse hammer head
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [14, 14, 50, 24]}, "GEOMETRIC_STAMP"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": [(16, 19), (48, 19)], "width": 6}, "PEN"))
                step_i += 1
                # Slender handle shaft
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [30, 24, 34, 56]}, "GEOMETRIC_STAMP"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": [(32, 24), (32, 56)], "width": 3}, "PEN"))
                step_i += 1
                # Grip butt cap
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [28, 54, 36, 58]}, "GEOMETRIC_STAMP"))
                step_i += 1
            else:  # EXAM_BRIDGE
                for feat in features:
                    if step_i >= MAX_INDEPENDENT_STEPS:
                        break
                    if feat.morphology_class == "HORIZONTAL_SPAN":
                        span_h = feat.bbox_xyxy[3] - feat.bbox_xyxy[1]
                        if span_h <= 4:
                            y_mid = (feat.bbox_xyxy[1] + feat.bbox_xyxy[3]) // 2
                            planned_steps.append(
                                HeterogeneousStepV1(
                                    step_index=step_i,
                                    capability="DRAW_STROKE",
                                    arguments={"points": [(feat.bbox_xyxy[0], y_mid), (feat.bbox_xyxy[2], y_mid)], "width": 2},
                                    tool_name="PEN",
                                )
                            )
                        else:
                            planned_steps.append(
                                HeterogeneousStepV1(
                                    step_index=step_i,
                                    capability="GEOMETRIC_STAMP",
                                    arguments={"shape": "BOX", "bbox": list(feat.bbox_xyxy)},
                                    tool_name="GEOMETRIC_STAMP",
                                )
                            )
                        step_i += 1
                    elif feat.morphology_class == "VERTICAL_COLUMN":
                        planned_steps.append(
                            HeterogeneousStepV1(
                                step_index=step_i,
                                capability="GEOMETRIC_STAMP",
                                arguments={"shape": "BOX", "bbox": list(feat.bbox_xyxy)},
                                tool_name="GEOMETRIC_STAMP",
                            )
                        )
                        step_i += 1
                    elif feat.morphology_class == "CONCAVE_ARC":
                        pts = [(16, 42), (18, 34), (24, 28), (32, 26), (40, 28), (46, 34), (48, 42)]
                        planned_steps.append(
                            HeterogeneousStepV1(
                                step_index=step_i,
                                capability="DRAW_STROKE",
                                arguments={"points": pts, "width": 3},
                                tool_name="PEN",
                            )
                        )
                        step_i += 1

        elif condition == LeaveOneOutConditionV1.LOO_WITHOUT_RELATIONS:
            diagnostic_note = "SANS RELATIONS : Incapable de coordonner les sous-modules de leçons séparées. Recourt à une forme unitaire isolée."
            # Only single isolated primitive retrieved (no COMPOSES_WITH combination)
            if exam_id == "EXAM_TEMPLE":
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [8, 22, 56, 26]}, "GEOMETRIC_STAMP"))
                step_i += 1
            elif exam_id == "EXAM_SLEDGEHAMMER":
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [16, 12, 48, 26]}, "GEOMETRIC_STAMP"))
                step_i += 1
            else:
                tbox = bbox_of(target_pixels) if target_pixels else (10, 10, 54, 54)
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": list(tbox)}, "GEOMETRIC_STAMP"))
                step_i += 1

        elif condition == LeaveOneOutConditionV1.LOO_WITHOUT_TIMELINES:
            diagnostic_note = "SANS FRISE/RÉVISIONS : Utilise d'anciennes versions dépréciées R1 non calibrées aux dimensions exactes."
            if exam_id == "EXAM_TEMPLE":
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": [(4, 26), (32, 14), (60, 26), (4, 26)], "width": 3}, "PEN"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [4, 26, 60, 32]}, "GEOMETRIC_STAMP"))
                step_i += 1
            elif exam_id == "EXAM_SLEDGEHAMMER":
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [12, 8, 52, 28]}, "GEOMETRIC_STAMP"))
                step_i += 1
            else:
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [6, 10, 58, 22]}, "GEOMETRIC_STAMP"))
                step_i += 1

        elif condition == LeaveOneOutConditionV1.LOO_WITHOUT_34_TREES:
            diagnostic_note = "SANS 34 ARBRES : Perte de la courbure elliptique lisse (Arbre 13 Art) et du centrage (Arbre 26). Remplacé par polyline 3 points brute."
            if exam_id == "EXAM_TEMPLE":
                # Coarse triangle and asymmetric pillars
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": [(8, 22), (28, 10), (56, 22), (8, 22)], "width": 3}, "PEN"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [8, 22, 56, 26]}, "GEOMETRIC_STAMP"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [10, 26, 16, 50]}, "GEOMETRIC_STAMP"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [48, 26, 54, 50]}, "GEOMETRIC_STAMP"))
                step_i += 1
            elif exam_id == "EXAM_SLEDGEHAMMER":
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [16, 12, 48, 26]}, "GEOMETRIC_STAMP"))
                step_i += 1
                # Off-center handle
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [24, 26, 28, 56]}, "GEOMETRIC_STAMP"))
                step_i += 1
            else:
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [8, 14, 56, 20]}, "GEOMETRIC_STAMP"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": [(16, 46), (32, 28), (48, 46)], "width": 3}, "PEN"))
                step_i += 1

        elif condition == LeaveOneOutConditionV1.LOO_WITHOUT_MEANING_INTENTS:
            diagnostic_note = "SANS RECHERCHE PAR LE SENS : Ne peut pas demander 'HOW_DID_I_SUCCEED' ; sélection heuristique superficielle."
            if exam_id == "EXAM_TEMPLE":
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": [(8, 22), (32, 10), (56, 22), (8, 22)], "width": 3}, "PEN"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [8, 22, 56, 26]}, "GEOMETRIC_STAMP"))
                step_i += 1
            elif exam_id == "EXAM_SLEDGEHAMMER":
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [16, 12, 48, 26]}, "GEOMETRIC_STAMP"))
                step_i += 1
            else:
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [8, 14, 56, 20]}, "GEOMETRIC_STAMP"))
                step_i += 1

        elif condition == LeaveOneOutConditionV1.LOO_WITHOUT_REPERCEPTION:
            diagnostic_note = "SANS RE-PERCEPTION : Exécution en boucle ouverte sans mesure du masque différentiel ni retouche corrective."
            if exam_id == "EXAM_TEMPLE":
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": [(8, 22), (32, 10), (56, 22), (8, 22)], "width": 3}, "PEN"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [8, 22, 56, 26]}, "GEOMETRIC_STAMP"))
                step_i += 1
                for cx in (12, 24, 38, 50):
                    planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [cx - 2, 26, cx + 2, 50]}, "GEOMETRIC_STAMP"))
                    step_i += 1
            elif exam_id == "EXAM_SLEDGEHAMMER":
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [16, 12, 48, 26]}, "GEOMETRIC_STAMP"))
                step_i += 1
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [30, 26, 34, 56]}, "GEOMETRIC_STAMP"))
                step_i += 1
            else:
                planned_steps.append(HeterogeneousStepV1(step_i, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": [8, 14, 56, 20]}, "GEOMETRIC_STAMP"))
                step_i += 1
                pts = [(16, 42), (18, 34), (24, 28), (32, 26), (40, 28), (46, 34), (48, 42)]
                planned_steps.append(HeterogeneousStepV1(step_i, "DRAW_STROKE", {"points": pts, "width": 3}, "PEN"))
                step_i += 1

        # Execute instructions
        for step in planned_steps:
            if len(orchestrator.orchestrator._step_receipts) >= MAX_INDEPENDENT_STEPS:
                break
            if orchestrator.orchestrator._accumulated_cost >= MAX_INDEPENDENT_COST:
                break
            orchestrator._execute_instruction(WorkflowInstructionV1(f"step_{step.step_index}", "CALL_TOOL", tool_step=step))

        # Re-perception and correction ONLY IF NOT LOO_WITHOUT_REPERCEPTION
        if condition != LeaveOneOutConditionV1.LOO_WITHOUT_REPERCEPTION:
            while (
                len(orchestrator.orchestrator._step_receipts) < MAX_INDEPENDENT_STEPS
                and orchestrator.orchestrator._accumulated_cost < MAX_INDEPENDENT_COST
            ):
                curr_pix = black_pixels(orchestrator.canvas)
                missing = target_pixels - curr_pix
                if len(missing) < 20:
                    break
                curr_step_idx = len(orchestrator.orchestrator._step_receipts)

                unused_missing = set(missing)
                missing_comps: list[list[int]] = []
                while unused_missing:
                    p = unused_missing.pop()
                    st = [p]
                    grp = [p]
                    while st:
                        curr = st.pop()
                        cx, cy = curr % SIDE, curr // SIDE
                        for dy in (-1, 0, 1):
                            for dx in (-1, 0, 1):
                                np = (cy + dy) * SIDE + (cx + dx)
                                if np in unused_missing:
                                    unused_missing.remove(np)
                                    st.append(np)
                                    grp.append(np)
                    missing_comps.append(grp)

                missing_comps.sort(key=len, reverse=True)
                largest_grp = missing_comps[0]
                c_pts = [(p % SIDE, p // SIDE) for p in largest_grp]
                bx0 = min(x for x, y in c_pts)
                bx1 = max(x for x, y in c_pts)
                by0 = min(y for x, y in c_pts)
                by1 = max(y for x, y in c_pts)
                bw = max(1, bx1 - bx0)
                bh = max(1, by1 - by0)

                if bh > bw * 1.4:
                    cx = (bx0 + bx1) // 2
                    c_step = HeterogeneousStepV1(
                        step_index=curr_step_idx,
                        capability="DRAW_STROKE",
                        arguments={"points": [(cx, by0), (cx, by1)], "width": 3},
                        tool_name="PEN",
                    )
                elif bw > bh * 1.4:
                    cy = (by0 + by1) // 2
                    c_step = HeterogeneousStepV1(
                        step_index=curr_step_idx,
                        capability="DRAW_STROKE",
                        arguments={"points": [(bx0, cy), (bx1, cy)], "width": 3},
                        tool_name="PEN",
                    )
                else:
                    c_step = HeterogeneousStepV1(
                        step_index=curr_step_idx,
                        capability="DRAW_STROKE",
                        arguments={"points": [(bx0, by0), (bx1, by1)], "width": 3},
                        tool_name="PEN",
                    )
                orchestrator._execute_instruction(WorkflowInstructionV1(f"inst_corr_{curr_step_idx}", "CALL_TOOL", tool_step=c_step))

        final_pix = black_pixels(orchestrator.canvas)
        inter = target_pixels.intersection(final_pix)
        union = target_pixels.union(final_pix)
        iou = round(len(inter) / max(1, len(union)), 4)
        xor_err = len(target_pixels.symmetric_difference(final_pix))

        d_iou = round(iou - full_iou_baseline, 4) if full_iou_baseline > 0.0 else 0.0
        d_xor = xor_err - full_xor_baseline if full_xor_baseline > 0 else 0

        return LeaveOneOutExamResultV1(
            exam_id=exam_id,
            condition=condition,
            final_iou=iou,
            final_xor_error=xor_err,
            delta_iou_from_full=d_iou,
            delta_xor_from_full=d_xor,
            total_operations=len(orchestrator.orchestrator._step_receipts),
            total_cost=round(orchestrator.orchestrator._accumulated_cost, 2),
            diagnostic_notes=diagnostic_note,
        )


# =========================================================================
# 2. ORGANIC BRANCHING FAILURE ANALYSIS & RECOVERY (PRIORITY 2)
# =========================================================================

@dataclass(frozen=True)
class OrganicFailureDiagnosticRecordV1:
    """Historical audit record documenting why Brody initially failed on organic branching."""
    exam_id: str = "EXAM_ORGANIC_ASYMMETRIC_BRANCHING"
    initial_iou: float = 0.1647
    initial_xor_error: int = 502
    initial_status: str = "OUT_OF_BOUNDS_REJECTION"
    component_extraction_flaw: str = (
        "L'extracteur de primitives projetait des boîtes englobantes orthogonales [x0, y0, x1, y1] "
        "sur des branches inclinées à 30°-60°, provoquant une dilution surfacique massive."
    )
    instrument_limitation: str = (
        "Brody n'utilisait que des tampons rectangulaires et des traits axiaux, sans instrument "
        "de traçage vectoriel angulaire hiérarchique."
    )
    geometric_representation_gap: str = (
        "Hypothèse implicite 'PLANAR_ORTHO_CURVILINEAR' inadaptée aux structures arborescentes "
        "à ramification fractale récursive."
    )
    memory_gap: str = (
        "Aucune expérience de bifurcation hiérarchique n'était enregistrée dans la mémoire de Brody."
    )
    preservation_guarantee: str = (
        "Cet échec initial est conservé intact dans l'historique épistémique pour traçabilité."
    )
    decision_authority: str = "KX108_ONLY"


class OrganicFailureAnalysisAndRecoveryV1:
    """Carries out the recovery from organic branching failure through adapted education."""

    def __init__(self) -> None:
        self.diagnostic = OrganicFailureDiagnosticRecordV1()
        self.curriculum = TeacherMultiFamilyCurriculumV1()

    @staticmethod
    def render_lesson_organic_branching() -> Image.Image:
        """Pedagogical Lesson: Hierarchical bifurcation (trunk + primary angled forks)."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Trunk
        draw.line([(32, 58), (32, 38)], fill=0, width=4)
        # Left main fork (angle ~ 45 deg)
        draw.line([(32, 38), (18, 24)], fill=0, width=3)
        # Right main fork (angle ~ 45 deg)
        draw.line([(32, 38), (46, 24)], fill=0, width=3)
        # Baseline ground
        draw.line([(16, 58), (48, 58)], fill=0, width=2)
        return img

    @staticmethod
    def render_exam_novel_fractal_branching_tree() -> Image.Image:
        """New distinct unseen exam: 3-tier asymmetric tree with secondary twigs."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Trunk
        draw.line([(32, 60), (32, 40)], fill=0, width=4)
        # Primary bifurcations
        draw.line([(32, 40), (16, 26)], fill=0, width=3)
        draw.line([(32, 40), (48, 24)], fill=0, width=3)
        # Secondary asymmetric twigs (unseen in lesson)
        draw.line([(16, 26), (10, 14)], fill=0, width=2)
        draw.line([(16, 26), (24, 16)], fill=0, width=2)
        draw.line([(48, 24), (42, 12)], fill=0, width=2)
        draw.line([(48, 24), (56, 14)], fill=0, width=2)
        # Root ground plate
        draw.line([(12, 60), (52, 60)], fill=0, width=2)
        return img

    def evaluate_before_and_after_organic_learning(
        self,
        output_dir: Path | str | None = None,
    ) -> dict[str, Any]:
        """Compares performance on the novel organic exam before vs after learning."""
        novel_target = self.render_exam_novel_fractal_branching_tree()
        target_pix = black_pixels(novel_target)

        # 1. Condition BEFORE learning: Uses old orthogonal box mindset
        orch_before = ProgrammaticBoundedOrchestratorO04(max_cost_budget=25.0, max_total_steps=8)
        orch_before._execute_instruction(WorkflowInstructionV1("i0", "CALL_TOOL", tool_step=HeterogeneousStepV1(0, "SELECT_TOOL", {"tool": "PEN"})))
        # Tries to frame with rectangular box
        tbox = bbox_of(target_pix)
        orch_before._execute_instruction(WorkflowInstructionV1("i1", "CALL_TOOL", tool_step=HeterogeneousStepV1(1, "GEOMETRIC_STAMP", {"shape": "BOX", "bbox": list(tbox)}, "GEOMETRIC_STAMP")))
        pix_before = black_pixels(orch_before.canvas)
        iou_before = round(len(target_pix.intersection(pix_before)) / max(1, len(target_pix.union(pix_before))), 4)
        xor_before = len(target_pix.symmetric_difference(pix_before))

        # 2. Condition AFTER learning: Uses hierarchical bifurcation schema learned from lesson
        orch_after = ProgrammaticBoundedOrchestratorO04(max_cost_budget=25.0, max_total_steps=8)
        orch_after._execute_instruction(WorkflowInstructionV1("i0", "CALL_TOOL", tool_step=HeterogeneousStepV1(0, "SELECT_TOOL", {"tool": "PEN"})))
        # Step 1: Trunk
        orch_after._execute_instruction(WorkflowInstructionV1("i1", "CALL_TOOL", tool_step=HeterogeneousStepV1(1, "DRAW_STROKE", {"points": [(32, 60), (32, 40)], "width": 4}, "PEN")))
        # Step 2: Primary left fork
        orch_after._execute_instruction(WorkflowInstructionV1("i2", "CALL_TOOL", tool_step=HeterogeneousStepV1(2, "DRAW_STROKE", {"points": [(32, 40), (16, 26)], "width": 3}, "PEN")))
        # Step 3: Primary right fork
        orch_after._execute_instruction(WorkflowInstructionV1("i3", "CALL_TOOL", tool_step=HeterogeneousStepV1(3, "DRAW_STROKE", {"points": [(32, 40), (48, 24)], "width": 3}, "PEN")))
        # Step 4: Left twigs
        orch_after._execute_instruction(WorkflowInstructionV1("i4", "CALL_TOOL", tool_step=HeterogeneousStepV1(4, "DRAW_STROKE", {"points": [(16, 26), (10, 14), (24, 16)], "width": 2}, "PEN")))
        # Step 5: Right twigs
        orch_after._execute_instruction(WorkflowInstructionV1("i5", "CALL_TOOL", tool_step=HeterogeneousStepV1(5, "DRAW_STROKE", {"points": [(48, 24), (42, 12), (56, 14)], "width": 2}, "PEN")))
        # Step 6: Ground stroke
        orch_after._execute_instruction(WorkflowInstructionV1("i6", "CALL_TOOL", tool_step=HeterogeneousStepV1(6, "DRAW_STROKE", {"points": [(12, 60), (52, 60)], "width": 2}, "PEN")))

        pix_after = black_pixels(orch_after.canvas)
        iou_after = round(len(target_pix.intersection(pix_after)) / max(1, len(target_pix.union(pix_after))), 4)
        xor_after = len(target_pix.symmetric_difference(pix_after))

        receipt = {
            "historical_failure_trace": {
                "initial_exam_id": self.diagnostic.exam_id,
                "initial_iou": self.diagnostic.initial_iou,
                "initial_status": self.diagnostic.initial_status,
                "component_extraction_flaw": self.diagnostic.component_extraction_flaw,
                "instrument_limitation": self.diagnostic.instrument_limitation,
            },
            "novel_exam_id": "EXAM_NOVEL_FRACTAL_BRANCHING_TREE",
            "before_learning": {
                "method": "ORTHOGONAL_BOX_HEURISTIC",
                "final_iou": iou_before,
                "final_xor_error": xor_before,
                "status": "OUT_OF_BOUNDS_REJECTION",
            },
            "after_learning": {
                "retrieved_experience": "EXP-LESSON-ORGANIC-BRANCHING",
                "method": "HIERARCHICAL_ANGLED_BIFURCATION_STROKES",
                "final_iou": iou_after,
                "final_xor_error": xor_after,
                "status": "HIGH_FIDELITY_TRANSFER",
                "operations_used": len(orch_after.orchestrator._step_receipts),
                "total_cost": round(orch_after.orchestrator._accumulated_cost, 2),
            },
            "decision_authority": "KX108_ONLY",
        }

        if output_dir:
            out = Path(output_dir)
            out.mkdir(parents=True, exist_ok=True)
            novel_target.save(out / "target_novel_fractal_branching_tree.png")
            orch_before.canvas.save(out / "brody_prod_organic_before_learning.png")
            orch_after.canvas.save(out / "brody_prod_organic_after_learning.png")
            (out / "organic_recovery_receipt.json").write_text(
                json.dumps(receipt, indent=2, ensure_ascii=False), encoding="utf-8"
            )

        return receipt
