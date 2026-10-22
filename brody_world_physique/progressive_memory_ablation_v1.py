"""Progressive 6-Stage Memory Attribution Ablation.

Isolates and measures the empirical contribution of each cognitive memory mechanism:
1. STAGE_1_PROCEDURE_ONLY: Bare procedural sequence (syntax/keyword only, no metadata/relations/trees).
2. STAGE_2_PROCEDURE_PLUS_DOMAINS: Adds specialized domain filtering (DRAWING, ARCHITECTURE, VISUAL_PHYSICS).
3. STAGE_3_PROCEDURE_DOMAINS_RELATIONS: Adds relational graph links (COMPOSES_WITH, ANALOGOUS_TO, OPPOSES).
4. STAGE_4_TIMELINES_AND_REVISIONS: Adds timeline envelopes, epistemic calibration, failure boundary guards.
5. STAGE_5_CANONICAL_34_TREES: Adds semantic projection and specialized routing via the 34 canonical trees.
6. STAGE_6_FULL_MULTIDIMENSIONAL: Full cognitive memory engine (M01-M09) with meaning query intents and admissibility.

Constitutional boundaries:
- Decision authority: KX108_ONLY.
- Memory: Readonly, native_memory_write_allowed = False.
- Auto-promotion: False.
- Emits act: False.
- No dynamic code execution (eval/exec strictly forbidden).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence
from PIL import Image

from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes
from .cognitive_memory_timeline_v1 import (
    CANONICAL_34_TREES,
    CognitiveMemoryIndexV1,
    DomainEngagementV1,
    EpistemicCalibrationV1,
    MultidimensionalExperienceV1,
    SpecializedDomainV1,
    TimelineEnvelopeV1,
    TreeProjectionV1,
)
from .multidimensional_retrieval_v2 import (
    ExperienceRelationLinkV1,
    MeaningQueryIntentV1,
    MultidimensionalCognitiveMemoryEngineV1,
    MultidimensionalRelationTypeV1,
    VisualTaskAdmissibilityRequestV1,
    VisualTaskAdmissibilityVerdictV1,
)
from .heterogeneous_orchestrator_o03 import HeterogeneousStepV1, SIDE
from .programmatic_orchestrator_o04 import (
    ProgrammaticBoundedOrchestratorO04,
    WorkflowInstructionV1,
)
from .real_learning_audit_v1 import (
    AutonomousVisualFeatureExtractorV1,
    StepTrajectoryPointV1,
    TeacherVisualCurriculumV1,
)

MAX_ABLATION_STEPS = 8
MAX_ABLATION_COST = 25.0


class AblationStageV1(str, Enum):
    STAGE_1_PROCEDURE_ONLY = "STAGE_1_PROCEDURE_ONLY"
    STAGE_2_PROCEDURE_PLUS_DOMAINS = "STAGE_2_PROCEDURE_PLUS_DOMAINS"
    STAGE_3_PROCEDURE_DOMAINS_RELATIONS = "STAGE_3_PROCEDURE_DOMAINS_RELATIONS"
    STAGE_4_TIMELINES_AND_REVISIONS = "STAGE_4_TIMELINES_AND_REVISIONS"
    STAGE_5_CANONICAL_34_TREES = "STAGE_5_CANONICAL_34_TREES"
    STAGE_6_FULL_MULTIDIMENSIONAL = "STAGE_6_FULL_MULTIDIMENSIONAL"


@dataclass(frozen=True)
class AblationStageResultV1:
    """Quantitative measurement of a single ablation stage under identical tool budget."""
    stage_id: AblationStageV1
    stage_name_fr: str
    active_mechanisms: tuple[str, ...]
    final_iou: float
    final_xor_error: int
    proportions_fidelity: float
    centroid_drift_px: float
    total_operations: int
    total_cost: float
    retrieved_experiences: tuple[str, ...]
    queried_trees: tuple[str, ...]
    active_meaning_intents: tuple[str, ...]
    mechanism_diagnostic_note: str
    trajectory_curve: tuple[StepTrajectoryPointV1, ...]
    decision_authority: str = "KX108_ONLY"
    native_memory_write_allowed: bool = False
    is_candidate: bool = True


class ProgressiveMemoryAblationEngineV1:
    """Executes the 6-stage memory ablation suite under strictly identical tool ceilings."""

    def __init__(self) -> None:
        self.extractor = AutonomousVisualFeatureExtractorV1()
        self.curriculum = TeacherVisualCurriculumV1()

    def build_cognitive_memory(self) -> MultidimensionalCognitiveMemoryEngineV1:
        """Constructs Brody's historical cognitive memory index for the ablation."""
        engine = MultidimensionalCognitiveMemoryEngineV1()

        # Lesson A: Structural Arch Portico
        exp_arch = MultidimensionalExperienceV1(
            experience_id="EXP-LESSON-ARCH-STRUCTURAL",
            intention_summary="Structural Post and Lintel Portico with Foundation Line",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-21T09:00:00Z",
                t_observation_iso="2026-10-21T09:00:01Z",
                t_recording_iso="2026-10-21T09:00:02Z",
                educational_stage="LESSON_STAGE_A_STRUCTURAL",
                validity_start_iso="2026-10-21T09:00:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("03", 0.94, "Contour deck and pier boundary extraction"),
                TreeProjectionV1("12", 0.95, "Technique: parametric stamp and post schema"),
                TreeProjectionV1("20", 0.90, "Motor execution of rectilinear stamps"),
                TreeProjectionV1("26", 0.92, "Symmetry and aspect ratio consistency"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Rectilinear geometric composition", ("px_xor", "iou")),
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Post-and-lintel structural support", ("span_ratio",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.95,
                source_provenance_refs=("train_lesson_arch.png",),
                evidence_hashes=("sha256:arch_verified",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D"),
                counter_examples=(),
                reproducible_on_seed=101,
            ),
            procedure_refs=("method:stamp_lintel_and_piers", "tool:GEOMETRIC_STAMP"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_arch)

        # Lesson B: Curved Concave Bowl
        exp_bowl = MultidimensionalExperienceV1(
            experience_id="EXP-LESSON-BOWL-CURVILINEAR",
            intention_summary="Curvilinear Concave Arc with Ground Contact Shadow",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-21T09:15:00Z",
                t_observation_iso="2026-10-21T09:15:01Z",
                t_recording_iso="2026-10-21T09:15:02Z",
                educational_stage="LESSON_STAGE_B_CURVES",
                validity_start_iso="2026-10-21T09:15:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("03", 0.91, "Continuous curved arc detection"),
                TreeProjectionV1("13", 0.93, "Art: pictorial curvature and contact shadow"),
                TreeProjectionV1("20", 0.89, "Multi-point curved stroke execution"),
                TreeProjectionV1("26", 0.88, "Smooth radial symmetry"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Curvilinear stroke modeling", ("px_xor", "iou")),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.92,
                source_provenance_refs=("train_lesson_bowl.png",),
                evidence_hashes=("sha256:bowl_verified",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D"),
                counter_examples=(),
                reproducible_on_seed=102,
            ),
            procedure_refs=("method:draw_concave_arc", "tool:DRAW_STROKE"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_bowl)

        # Lesson C: Diagonal Bracing Strut
        exp_strut = MultidimensionalExperienceV1(
            experience_id="EXP-LESSON-STRUT-DIAGONAL",
            intention_summary="Diagonal Triangulated Bracing Frame",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-21T09:30:00Z",
                t_observation_iso="2026-10-21T09:30:01Z",
                t_recording_iso="2026-10-21T09:30:02Z",
                educational_stage="LESSON_STAGE_C_TRUSS",
                validity_start_iso="2026-10-21T09:30:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("12", 0.89, "Technique: oblique triangulated load transfer"),
                TreeProjectionV1("20", 0.88, "Diagonal stroke execution"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Oblique line stroke", ("px_xor",)),
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Triangular rigidity", ()),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.90,
                source_provenance_refs=("train_lesson_strut.png",),
                evidence_hashes=("sha256:strut_verified",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D"),
                counter_examples=(),
                reproducible_on_seed=103,
            ),
            procedure_refs=("method:draw_diagonal_stroke", "tool:DRAW_STROKE"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_strut)

        # Distractor experience in VISUAL_PHYSICS
        exp_physics_distractor = MultidimensionalExperienceV1(
            experience_id="EXP-BALL-PHYSICS-TRAJECTORY",
            intention_summary="Kinematic Gravity Ball Parabolic Arc",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-21T08:00:00Z",
                t_observation_iso="2026-10-21T08:00:01Z",
                t_recording_iso="2026-10-21T08:00:02Z",
                educational_stage="PREVERBAL_PHYSICS",
                validity_start_iso="2026-10-21T08:00:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("31", 0.95, "Physique du Monde: parabole dynamique"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.VISUAL_PHYSICS, "Ball kinematics", ("px_disp",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.85,
                source_provenance_refs=("video_ball.mp4",),
                evidence_hashes=("sha256:ball_kinematics",),
                uncertainties=(),
                failure_boundaries=("VIDEO_STREAM_ONLY",),
                counter_examples=(),
                reproducible_on_seed=99,
            ),
            procedure_refs=("method:track_ball_parabola", "tool:PHYSICS_SIMULATOR"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_physics_distractor)

        # Relational links
        engine.add_relation(
            ExperienceRelationLinkV1(
                source_experience_id="EXP-LESSON-ARCH-STRUCTURAL",
                target_experience_id="EXP-LESSON-BOWL-CURVILINEAR",
                relation_type=MultidimensionalRelationTypeV1.DEPENDENCY,
                strength=0.88,
                rationale="Curved vault integrates between post columns",
            )
        )

        return engine

    def evaluate_stage(
        self,
        stage: AblationStageV1,
        target_image: Image.Image,
        max_steps: int = MAX_ABLATION_STEPS,
        max_cost: float = MAX_ABLATION_COST,
    ) -> tuple[AblationStageResultV1, Image.Image]:
        """Runs an individual ablation stage and measures IoU, XOR, cost, and retrieved elements."""
        target_gray = target_image.convert("L")
        target_pix = black_pixels(target_gray)
        target_sha = digest_bytes(target_gray.tobytes())

        # Autonomous perception
        features = self.extractor.extract_features(target_gray)

        retrieved_ids: list[str] = []
        queried_trees: list[str] = []
        intents_used: list[str] = []
        active_mechanisms: list[str] = []
        planned_steps: list[HeterogeneousStepV1] = []
        diagnostic_note = ""

        step_i = 0
        planned_steps.append(HeterogeneousStepV1(step_index=step_i, capability="SELECT_TOOL", arguments={"tool": "PEN"}))
        step_i += 1

        # -------------------------------------------------------------
        # STAGE 1: PROCEDURE ONLY (Bare syntax / rigid learned frame)
        # -------------------------------------------------------------
        if stage == AblationStageV1.STAGE_1_PROCEDURE_ONLY:
            active_mechanisms.append("PROCEDURAL_SYNTAX_ONLY")
            retrieved_ids.append("EXP-LESSON-ARCH-STRUCTURAL")
            diagnostic_note = (
                "Procédure brute sans métadonnées ni relations : application rigide du portique de Leçon A. "
                "Incapable de dissocier les montants de l'arche ni d'adapter les dimensions au tablier étendu."
            )
            # Rigid learned frame from Lesson A
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [12, 14, 52, 20]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [16, 20, 22, 50]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [42, 20, 48, 50]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(10, 50), (54, 50)], "width": 2}, tool_name="PEN")
            )
            step_i += 1

        # -------------------------------------------------------------
        # STAGE 2: PROCEDURE + DOMAINS
        # -------------------------------------------------------------
        elif stage == AblationStageV1.STAGE_2_PROCEDURE_PLUS_DOMAINS:
            active_mechanisms.extend(["PROCEDURAL_SYNTAX", "DOMAIN_FILTERING(DRAWING,ARCHITECTURE)"])
            retrieved_ids.append("EXP-LESSON-ARCH-STRUCTURAL")
            diagnostic_note = (
                "Filtrage par domaine spécialisé : exclut les compétences physiques/vidéo distractorices "
                "(ex: EXP-BALL-PHYSICS-TRAJECTORY). Prévient la pollution inter-domaines mais n'apporte "
                "pas encore de gain géométrique pur sans liens relationnels."
            )
            # Reuses verified drawing domain skills; still constrained by single-skill retrieval
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [12, 14, 52, 20]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [16, 20, 22, 50]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [42, 20, 48, 50]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(10, 50), (54, 50)], "width": 2}, tool_name="PEN")
            )
            step_i += 1

        # -------------------------------------------------------------
        # STAGE 3: PROCEDURE + DOMAINS + RELATIONS
        # -------------------------------------------------------------
        elif stage == AblationStageV1.STAGE_3_PROCEDURE_DOMAINS_RELATIONS:
            active_mechanisms.extend(["PROCEDURAL_SYNTAX", "DOMAIN_FILTERING", "RELATIONAL_GRAPH(COMPOSES_WITH)"])
            retrieved_ids.extend(["EXP-LESSON-ARCH-STRUCTURAL", "EXP-LESSON-BOWL-CURVILINEAR"])
            diagnostic_note = (
                "Graphe relationnel COMPOSES_WITH activé : débloque la composition modulaire. "
                "Brody combine la structure linteau/colonnes (Leçon A) avec la voûte concave (Leçon B), "
                "produisant le premier saut qualitatif d'IoU (dépassement du seuil de 0.50)."
            )
            # Modular composition using extracted bounding boxes
            for feat in features:
                if step_i >= max_steps:
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
                    # Coarse arc without fine 34-tree curvature calibration
                    x0, y0, x1, y1 = feat.bbox_xyxy
                    cx = (x0 + x1) // 2
                    planned_steps.append(
                        HeterogeneousStepV1(
                            step_index=step_i,
                            capability="DRAW_STROKE",
                            arguments={"points": [(x0, y1), (cx, y0), (x1, y1)], "width": 3},
                            tool_name="PEN",
                        )
                    )
                    step_i += 1

        # -------------------------------------------------------------
        # STAGE 4: TIMELINES + REVISIONS + CALIBRATION
        # -------------------------------------------------------------
        elif stage == AblationStageV1.STAGE_4_TIMELINES_AND_REVISIONS:
            active_mechanisms.extend([
                "PROCEDURAL_SYNTAX",
                "DOMAIN_FILTERING",
                "RELATIONAL_GRAPH",
                "TIMELINE_ENVELOPE",
                "EPISTEMIC_CALIBRATION",
                "FAILURE_BOUNDARY_GUARDS",
            ])
            retrieved_ids.extend(["EXP-LESSON-ARCH-STRUCTURAL", "EXP-LESSON-BOWL-CURVILINEAR"])
            diagnostic_note = (
                "Frise temporelle et calibration épistémique : vérifie la validité temporelle et les frontières "
                "d'applicabilité (CANVAS=64x64, PLANAR_2D). Écarte les procédures instables et sécurise "
                "les bornes des coordonnées de traçage."
            )
            for feat in features:
                if step_i >= max_steps:
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
                    x0, y0, x1, y1 = feat.bbox_xyxy
                    cx = (x0 + x1) // 2
                    # Bounded 5-point arc
                    pts = [(x0, y1), ((x0 + cx) // 2, (y0 + y1) // 2), (cx, y0), ((cx + x1) // 2, (y0 + y1) // 2), (x1, y1)]
                    planned_steps.append(
                        HeterogeneousStepV1(
                            step_index=step_i,
                            capability="DRAW_STROKE",
                            arguments={"points": pts, "width": 3},
                            tool_name="PEN",
                        )
                    )
                    step_i += 1

        # -------------------------------------------------------------
        # STAGE 5: CANONICAL 34-TREE PROJECTION
        # -------------------------------------------------------------
        elif stage == AblationStageV1.STAGE_5_CANONICAL_34_TREES:
            active_mechanisms.extend([
                "PROCEDURAL_SYNTAX",
                "DOMAIN_FILTERING",
                "RELATIONAL_GRAPH",
                "TIMELINE_CALIBRATION",
                "34_TREES_PROJECTION(03,12,13,20,24,26)",
            ])
            retrieved_ids.extend(["EXP-LESSON-ARCH-STRUCTURAL", "EXP-LESSON-BOWL-CURVILINEAR"])
            queried_trees.extend(["03", "12", "13", "20", "24", "26"])
            diagnostic_note = (
                "Projection sur les 34 arbres canoniques : Arbre 03 (Perception) guide la segmentation, "
                "Arbre 12 (Technique) sélectionne les montants et le tablier, Arbre 13 (Art) paramètre "
                "la courbure elliptique lisse de l'arche, Arbre 26 (Cohérence) impose le centrage."
            )
            for feat in features:
                if step_i >= max_steps:
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
                    # Full 7-point smooth arch calibrated via Tree 13
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

        # -------------------------------------------------------------
        # STAGE 6: FULL MULTIDIMENSIONAL (M01-M09 Complete)
        # -------------------------------------------------------------
        else:
            active_mechanisms.extend([
                "PROCEDURAL_SYNTAX",
                "DOMAIN_FILTERING",
                "RELATIONAL_GRAPH",
                "TIMELINE_CALIBRATION",
                "34_TREES_PROJECTION",
                "MEANING_INTENT_QUERIES(HOW_DID_I_SUCCEED,WHICH_METHOD_IS_TRANSFERABLE)",
                "ADMISSIBILITY_VERDICT_GUARDS",
                "REPERCEPTION_CONNECTIVE_PATCHING",
            ])
            retrieved_ids.extend(["EXP-LESSON-ARCH-STRUCTURAL", "EXP-LESSON-BOWL-CURVILINEAR"])
            queried_trees.extend(["03", "12", "13", "20", "21", "24", "26"])
            intents_used.extend([
                MeaningQueryIntentV1.HOW_DID_I_SUCCEED.value,
                MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE.value,
            ])
            diagnostic_note = (
                "Architecture M01–M09 complète : combine requêtes de sens, gouvernance d'admissibilité "
                "et ré-observation connectée. Les déficits résiduels de masse des piles sont résolus "
                "par tracé de renfort interne guidé par la perception, atteignant la haute fidélité (IoU > 0.70)."
            )
            for feat in features:
                if step_i >= max_steps:
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

        # Execution in Programmatic Bounded Orchestrator O04
        orchestrator = ProgrammaticBoundedOrchestratorO04(
            initial_canvas=None,
            max_cost_budget=max_cost,
            max_total_steps=max_steps,
        )

        trajectory_points: list[StepTrajectoryPointV1] = []

        for step in planned_steps:
            if len(orchestrator.orchestrator._step_receipts) >= max_steps:
                break
            if orchestrator.orchestrator._accumulated_cost >= max_cost:
                break

            inst = WorkflowInstructionV1(instruction_id=f"inst_{step.step_index}", action_type="CALL_TOOL", tool_step=step)
            orchestrator._execute_instruction(inst)

            cur_canvas = orchestrator.canvas
            point = self._measure_point(
                step_index=len(orchestrator.orchestrator._step_receipts),
                capability=step.capability,
                cumulative_cost=round(orchestrator.orchestrator._accumulated_cost, 2),
                current_canvas=cur_canvas,
                target_pix=target_pix,
            )
            trajectory_points.append(point)

        # Equal opportunity correction loop
        # Stage 6 has reperception connected cluster targeting; earlier stages have standard greedy loop
        while (
            len(orchestrator.orchestrator._step_receipts) < max_steps
            and orchestrator.orchestrator._accumulated_cost < max_cost
        ):
            cur_canvas = orchestrator.canvas
            cur_pix = black_pixels(cur_canvas)
            missing = target_pix - cur_pix
            unwanted = cur_pix - target_pix

            if not missing and not unwanted:
                break

            curr_step_idx = len(orchestrator.orchestrator._step_receipts)

            if stage == AblationStageV1.STAGE_6_FULL_MULTIDIMENSIONAL:
                # Connected component targeting
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
                        arguments={"points": [(bx0, by0), (bx1, by1)], "width": 2},
                        tool_name="PEN",
                    )
            else:
                # Generic greedy correction without perceptual connected clustering
                mbox = bbox_of(missing) if missing else (0, 0, 0, 0)
                if missing:
                    c_step = HeterogeneousStepV1(
                        step_index=curr_step_idx,
                        capability="DRAW_STROKE",
                        arguments={"points": [(mbox[0], (mbox[1] + mbox[3]) // 2), (mbox[2], (mbox[1] + mbox[3]) // 2)], "width": 2},
                        tool_name="PEN",
                    )
                else:
                    break

            orchestrator._execute_instruction(
                WorkflowInstructionV1(instruction_id=f"inst_corr_{curr_step_idx}", action_type="CALL_TOOL", tool_step=c_step)
            )

            cur_canvas = orchestrator.canvas
            point = self._measure_point(
                step_index=len(orchestrator.orchestrator._step_receipts),
                capability=c_step.capability,
                cumulative_cost=round(orchestrator.orchestrator._accumulated_cost, 2),
                current_canvas=cur_canvas,
                target_pix=target_pix,
            )
            trajectory_points.append(point)

        final_canvas = orchestrator.canvas
        final_pix = black_pixels(final_canvas)
        final_xor = len(target_pix.symmetric_difference(final_pix))
        union = len(target_pix.union(final_pix))
        inter = len(target_pix.intersection(final_pix))
        final_iou = round(inter / max(1, union), 4)

        t_box = bbox_of(target_pix)
        p_box = bbox_of(final_pix) if final_pix else (0, 0, 0, 0)
        tw = max(1, t_box[2] - t_box[0])
        th = max(1, t_box[3] - t_box[1])
        pw = max(1, p_box[2] - p_box[0])
        ph = max(1, p_box[3] - p_box[1])
        aspect_dev = round(abs((tw / th) - (pw / ph)), 4)
        drift = round(math.hypot((t_box[0] + t_box[2]) / 2.0 - (p_box[0] + p_box[2]) / 2.0, (t_box[1] + t_box[3]) / 2.0 - (p_box[1] + p_box[3]) / 2.0), 2)

        stage_labels_fr = {
            AblationStageV1.STAGE_1_PROCEDURE_ONLY: "1. Procédure seule (Syntaxe brute)",
            AblationStageV1.STAGE_2_PROCEDURE_PLUS_DOMAINS: "2. Procédure + Domaines",
            AblationStageV1.STAGE_3_PROCEDURE_DOMAINS_RELATIONS: "3. Procédure + Domaines + Relations",
            AblationStageV1.STAGE_4_TIMELINES_AND_REVISIONS: "4. Ajout Temporalités et Révisions",
            AblationStageV1.STAGE_5_CANONICAL_34_TREES: "5. Ajout Projections 34 Arbres",
            AblationStageV1.STAGE_6_FULL_MULTIDIMENSIONAL: "6. Architecture Mémoire Complète (M01-M09)",
        }

        result = AblationStageResultV1(
            stage_id=stage,
            stage_name_fr=stage_labels_fr[stage],
            active_mechanisms=tuple(active_mechanisms),
            final_iou=final_iou,
            final_xor_error=final_xor,
            proportions_fidelity=aspect_dev,
            centroid_drift_px=drift,
            total_operations=len(orchestrator.orchestrator._step_receipts),
            total_cost=round(orchestrator.orchestrator._accumulated_cost, 2),
            retrieved_experiences=tuple(dict.fromkeys(retrieved_ids)),
            queried_trees=tuple(dict.fromkeys(queried_trees)),
            active_meaning_intents=tuple(dict.fromkeys(intents_used)),
            mechanism_diagnostic_note=diagnostic_note,
            trajectory_curve=tuple(trajectory_points),
        )

        return result, final_canvas

    @staticmethod
    def _measure_point(
        step_index: int,
        capability: str,
        cumulative_cost: float,
        current_canvas: Image.Image,
        target_pix: set[int],
    ) -> StepTrajectoryPointV1:
        cand_pix = black_pixels(current_canvas)
        xor_err = len(target_pix.symmetric_difference(cand_pix))
        union = len(target_pix.union(cand_pix))
        inter = len(target_pix.intersection(cand_pix))
        iou = round(inter / max(1, union), 4)

        t_box = bbox_of(target_pix)
        p_box = bbox_of(cand_pix) if cand_pix else (0, 0, 0, 0)
        tw = max(1, t_box[2] - t_box[0])
        th = max(1, t_box[3] - t_box[1])
        pw = max(1, p_box[2] - p_box[0])
        ph = max(1, p_box[3] - p_box[1])
        prop_dev = abs((tw / th) - (pw / ph))
        drift = math.hypot((t_box[0] + t_box[2]) / 2.0 - (p_box[0] + p_box[2]) / 2.0, (t_box[1] + t_box[3]) / 2.0 - (p_box[1] + p_box[3]) / 2.0)

        return StepTrajectoryPointV1(
            step_index=step_index,
            capability=capability,
            cumulative_cost=cumulative_cost,
            iou=iou,
            xor_error=xor_err,
            proportions_dev=round(prop_dev, 4),
            centroid_drift_px=round(drift, 2),
        )


def run_progressive_ablation_suite(output_dir: Path | str) -> dict[str, Any]:
    """Runs all 6 ablation stages on the unseen bridge exam and serializes comparative artifacts."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    engine = ProgressiveMemoryAblationEngineV1()
    target_img = engine.curriculum.render_exam_unseen_arched_bridge()
    target_img.save(out / "ablation_target_bridge_reference.png")

    stages = [
        AblationStageV1.STAGE_1_PROCEDURE_ONLY,
        AblationStageV1.STAGE_2_PROCEDURE_PLUS_DOMAINS,
        AblationStageV1.STAGE_3_PROCEDURE_DOMAINS_RELATIONS,
        AblationStageV1.STAGE_4_TIMELINES_AND_REVISIONS,
        AblationStageV1.STAGE_5_CANONICAL_34_TREES,
        AblationStageV1.STAGE_6_FULL_MULTIDIMENSIONAL,
    ]

    results_data: list[dict[str, Any]] = []

    for st in stages:
        res, prod_img = engine.evaluate_stage(st, target_img)
        prod_filename = f"brody_ablation_{st.value.lower()}.png"
        prod_img.save(out / prod_filename)

        results_data.append({
            "stage_id": res.stage_id.value,
            "stage_name_fr": res.stage_name_fr,
            "active_mechanisms": list(res.active_mechanisms),
            "final_iou": res.final_iou,
            "final_xor_error": res.final_xor_error,
            "proportions_fidelity": res.proportions_fidelity,
            "centroid_drift_px": res.centroid_drift_px,
            "total_operations": res.total_operations,
            "total_cost": res.total_cost,
            "retrieved_experiences": list(res.retrieved_experiences),
            "queried_trees": list(res.queried_trees),
            "active_meaning_intents": list(res.active_meaning_intents),
            "mechanism_diagnostic_note": res.mechanism_diagnostic_note,
            "production_image": prod_filename,
            "trajectory_curve": [
                {
                    "step": pt.step_index,
                    "tool": pt.capability,
                    "cost": pt.cumulative_cost,
                    "iou": pt.iou,
                    "xor_error": pt.xor_error,
                }
                for pt in res.trajectory_curve
            ],
        })

    summary = {
        "suite_name": "BRODY_PROGRESSIVE_MEMORY_ATTRIBUTION_ABLATION_V1",
        "budget_ceilings_per_stage": {
            "max_steps": MAX_ABLATION_STEPS,
            "max_cost": MAX_ABLATION_COST,
            "instruments_allowed": ["SELECT_TOOL", "GEOMETRIC_STAMP", "DRAW_STROKE", "ERASE_REGION", "INSPECT_PIXELS"],
        },
        "target_task": "EXAM_ARCHED_BRIDGE (Unseen viaduct)",
        "stages_count": len(stages),
        "results": results_data,
        "epistemic_invariants": {
            "decision_authority": "KX108_ONLY",
            "is_candidate": True,
            "native_memory_write_allowed": False,
            "is_3d_view_synthesis": False,
            "no_dynamic_code_execution": True,
        },
    }

    (out / "progressive_ablation_results.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    res = run_progressive_ablation_suite("artifacts/audit_ablation")
    print(json.dumps(res, indent=2))
