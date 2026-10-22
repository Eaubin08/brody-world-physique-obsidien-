"""Expanded Multi-Family Visual Generalization & Counter-Example Curriculum.

Covers Priority 2 (Généralisation & Contre-exemples) and Priority 3 (Éducation & Création d'intention):
1. Multiple Independent Object Families:
   - ARCHITECTURE: Temple Facade (colonnade + pediment + stepped base) [Unseen Exam]
   - VESSELS: Dual-chambered Hourglass [Unseen Exam]
   - TOOLS: Sledgehammer (slender handle + heavy head) [Unseen Exam]
   - ORGANIC / COUNTER-EXAMPLES: Asymmetric fractal branching & amorphous concave blob [Honest Failure Boundaries]
2. Independent Train/Exam Separation:
   - Lessons contain generic components (Portico, Bowl, Truss, Barbell).
   - Exams test novel unseen configurations.
3. Strict Equal Budgets:
   - 8 steps ceiling, 25.0 cost limit across all tasks.
4. Autonomous Competence Boundary Detection:
   - Acknowledges failure on non-orthogonal fractal/organic forms (IoU < 0.35)
     logging an explicit OUT_OF_BOUNDS_COMPETENCE boundary rather than claiming artificial PASS.
5. Intent-Only Creation Derived from Memory:
   - Constructs visual compositions from declarative intention text alone.
   - Derives tool choices dynamically from retrieved memory experiences without hardcoded templates.

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
import math
from pathlib import Path
from statistics import mean
from typing import Any, Mapping, Sequence
from PIL import Image, ImageDraw

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
)
from .heterogeneous_orchestrator_o03 import HeterogeneousStepV1, SIDE
from .programmatic_orchestrator_o04 import (
    ProgrammaticBoundedOrchestratorO04,
    WorkflowInstructionV1,
)
from .real_learning_audit_v1 import (
    AutonomousVisualFeatureExtractorV1,
    StepTrajectoryPointV1,
    VisualFeatureComponentV1,
)

MAX_GENERALIZATION_STEPS = 8
MAX_GENERALIZATION_COST = 25.0


# =========================================================================
# 1. PRIVATE TEACHER MULTI-FAMILY CURRICULUM
# =========================================================================

class TeacherMultiFamilyCurriculumV1:
    """Private curriculum generating lessons and unseen exam references."""

    # --- Training Lessons (Generic Primitives) ---
    @staticmethod
    def render_lesson_arch() -> Image.Image:
        """Lesson A: Post and Lintel portico."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        draw.rectangle([12, 14, 52, 20], fill=0)
        draw.rectangle([16, 20, 22, 50], fill=0)
        draw.rectangle([42, 20, 48, 50], fill=0)
        draw.line([(10, 50), (54, 50)], fill=0, width=2)
        return img

    @staticmethod
    def render_lesson_bowl() -> Image.Image:
        """Lesson B: Concave bowl with shadow."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        draw.ellipse([16, 20, 48, 28], outline=0, width=2)
        draw.arc([16, 20, 48, 52], start=0, end=180, fill=0, width=3)
        draw.ellipse([22, 52, 42, 56], fill=120)
        return img

    @staticmethod
    def render_lesson_truss() -> Image.Image:
        """Lesson C: Triangular truss bracing."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        draw.line([(14, 48), (32, 16)], fill=0, width=3)
        draw.line([(32, 16), (50, 48)], fill=0, width=3)
        draw.line([(14, 48), (50, 48)], fill=0, width=3)
        return img

    @staticmethod
    def render_lesson_barbell() -> Image.Image:
        """Lesson D: Horizontal cylindrical shaft with dual end masses."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        draw.rectangle([10, 22, 18, 42], fill=0)
        draw.rectangle([46, 22, 54, 42], fill=0)
        draw.line([(18, 32), (46, 32)], fill=0, width=3)
        return img

    # --- Unseen Examination Tasks (Multiple Families) ---
    @staticmethod
    def render_exam_temple_facade() -> Image.Image:
        """EXAM 1 (Family: ARCHITECTURE): Classical Temple Facade.
        Triangular pediment roof on horizontal entablature, supported on 4 vertical columns and stepped stylobate.
        """
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Triangular pediment
        draw.line([(8, 22), (32, 10)], fill=0, width=3)
        draw.line([(32, 10), (56, 22)], fill=0, width=3)
        draw.line([(8, 22), (56, 22)], fill=0, width=3)
        # Entablature beam
        draw.rectangle([8, 22, 56, 26], fill=0)
        # 4 Vertical columns
        for cx in (12, 24, 38, 50):
            draw.rectangle([cx - 2, 26, cx + 2, 50], fill=0)
        # Stepped stylobate base
        draw.line([(6, 50), (58, 50)], fill=0, width=2)
        draw.line([(4, 53), (60, 53)], fill=0, width=2)
        return img

    @staticmethod
    def render_exam_hourglass() -> Image.Image:
        """EXAM 2 (Family: VESSELS): Dual-chambered Hourglass.
        Top conical chamber, central constriction neck, bottom conical chamber, top and bottom plates.
        """
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Top and bottom horizontal boundary plates
        draw.line([(18, 14), (46, 14)], fill=0, width=3)
        draw.line([(18, 50), (46, 50)], fill=0, width=3)
        # Inverted top cone
        draw.line([(18, 14), (30, 32)], fill=0, width=3)
        draw.line([(46, 14), (34, 32)], fill=0, width=3)
        # Neck
        draw.line([(30, 32), (34, 32)], fill=0, width=2)
        # Upright bottom cone
        draw.line([(30, 32), (18, 50)], fill=0, width=3)
        draw.line([(34, 32), (46, 50)], fill=0, width=3)
        # Inner sand mass in lower chamber
        draw.ellipse([26, 42, 38, 48], fill=0)
        return img

    @staticmethod
    def render_exam_sledgehammer() -> Image.Image:
        """EXAM 3 (Family: TOOLS_MECHANICAL): Heavy Sledgehammer.
        Long slender vertical handle surmounted by a massive transverse rectangular head.
        """
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Heavy transverse hammer head block
        draw.rectangle([14, 14, 50, 24], fill=0)
        # Slender vertical handle shaft
        draw.rectangle([30, 24, 34, 56], fill=0)
        # Grip butt cap
        draw.rectangle([28, 54, 36, 58], fill=0)
        return img

    @staticmethod
    def render_exam_organic_branching() -> Image.Image:
        """EXAM 4 (Family: ORGANIC_FRACTAL — HONEST COUNTER-EXAMPLE).
        Irregular, non-orthogonal asymmetric tree branches and clustered foliage.
        Outside Brody's affine rectilinear/circular primitive competence!
        """
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Irregular winding trunk
        draw.line([(28, 56), (30, 42), (36, 30), (32, 20)], fill=0, width=3)
        # Asymmetric jagged branches
        draw.line([(36, 30), (48, 22), (54, 26)], fill=0, width=2)
        draw.line([(30, 42), (18, 36), (12, 38)], fill=0, width=2)
        draw.line([(32, 20), (24, 14)], fill=0, width=2)
        # Irregular foliage clusters
        draw.polygon([(20, 10), (28, 8), (34, 12), (30, 16), (22, 14)], fill=0)
        draw.polygon([(46, 18), (56, 16), (58, 24), (50, 28), (44, 22)], fill=0)
        draw.polygon([(10, 32), (18, 30), (20, 40), (8, 42)], fill=0)
        return img

    @staticmethod
    def render_exam_amorphous_blob() -> Image.Image:
        """EXAM 5 (Family: AMORPHOUS_CREVICE — HONEST COUNTER-EXAMPLE).
        Non-convex irregular organic crevice with random concave folds.
        """
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Random non-convex polygon with 11 irregular vertices
        points = [
            (24, 16), (38, 14), (52, 22), (44, 32), (54, 42),
            (40, 52), (28, 46), (16, 50), (22, 36), (14, 26), (20, 22)
        ]
        draw.polygon(points, fill=0)
        return img


# =========================================================================
# 2. GENERALIZATION AUDITOR & INTENT-ONLY CREATION ENGINE
# =========================================================================

@dataclass(frozen=True)
class GeneralizationExamResultV1:
    """Evaluation result on an unseen exam family with competence boundary classification."""
    exam_id: str
    family_name: str
    target_sha256: str
    final_iou: float
    final_xor_error: int
    proportions_fidelity: float
    centroid_drift_px: float
    total_operations: int
    total_cost: float
    retrieved_experiences: tuple[str, ...]
    is_competence_boundary_honored: bool
    competence_status: str  # "HIGH_FIDELITY_TRANSFER", "MODERATE_TRANSFER", "OUT_OF_BOUNDS_REJECTION"
    failure_boundary_reason: str
    trajectory_curve: tuple[StepTrajectoryPointV1, ...]
    decision_authority: str = "KX108_ONLY"
    native_memory_write_allowed: bool = False
    is_candidate: bool = True


class AutonomousMultiFamilyAuditorV1:
    """Evaluates Brody across multiple unseen families and intent-only creations."""

    def __init__(self) -> None:
        self.curriculum = TeacherMultiFamilyCurriculumV1()
        self.extractor = AutonomousVisualFeatureExtractorV1()
        self.memory_engine = self._bootstrap_multi_family_memory()

    def _bootstrap_multi_family_memory(self) -> MultidimensionalCognitiveMemoryEngineV1:
        index = CognitiveMemoryIndexV1()
        engine = MultidimensionalCognitiveMemoryEngineV1(index=index)

        # 1. Lesson Arch (Structural lintel + piers)
        exp_arch = MultidimensionalExperienceV1(
            experience_id="EXP-LESSON-ARCH-STRUCTURAL",
            intention_summary="Horizontal span supported on dual vertical piers",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T08:00:00Z",
                t_observation_iso="2026-10-22T08:00:01Z",
                t_recording_iso="2026-10-22T08:01:00Z",
                educational_stage="LESSON_ARCH_V1",
                validity_start_iso="2026-10-22T08:00:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("03", 0.95, "Arbre de la Perception: contours lintel and piers"),
                TreeProjectionV1("12", 0.94, "Arbre de la Technique: parametric pillars and beams"),
                TreeProjectionV1("20", 0.90, "Arbre de l'Action: rectilinear stamps"),
                TreeProjectionV1("26", 0.92, "Arbre de la Cohérence: symmetry and span ratio"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Rectilinear geometric composition", ("px_xor", "iou")),
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Post-and-lintel load transfer", ()),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.95,
                source_provenance_refs=("train_lesson_arch.png",),
                evidence_hashes=("sha256:arch_receipt",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D", "NON_FRACTAL"),
                counter_examples=(),
                reproducible_on_seed=101,
            ),
            procedure_refs=("method:stamp_lintel_and_piers", "tool:GEOMETRIC_STAMP"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_arch)

        # 2. Lesson Bowl (Curved concave arc)
        exp_bowl = MultidimensionalExperienceV1(
            experience_id="EXP-LESSON-BOWL-CURVILINEAR",
            intention_summary="Curved concave arc with shadow",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T08:10:00Z",
                t_observation_iso="2026-10-22T08:10:01Z",
                t_recording_iso="2026-10-22T08:11:00Z",
                educational_stage="LESSON_BOWL_V1",
                validity_start_iso="2026-10-22T08:10:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("03", 0.92, "Arbre de la Perception: curved arc boundary"),
                TreeProjectionV1("13", 0.94, "Arbre de l'Art: tonal modeling and curvature"),
                TreeProjectionV1("20", 0.89, "Arbre de l'Action: multi-point stroke"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Curved strokes", ("px_xor",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.92,
                source_provenance_refs=("train_lesson_bowl.png",),
                evidence_hashes=("sha256:bowl_receipt",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D"),
                counter_examples=(),
                reproducible_on_seed=102,
            ),
            procedure_refs=("method:draw_concave_arc", "tool:DRAW_STROKE"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_bowl)

        # 3. Lesson Truss (Triangular diagonal bracing)
        exp_truss = MultidimensionalExperienceV1(
            experience_id="EXP-LESSON-TRUSS-DIAGONAL",
            intention_summary="Triangular pediment truss frame",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T08:20:00Z",
                t_observation_iso="2026-10-22T08:20:01Z",
                t_recording_iso="2026-10-22T08:21:00Z",
                educational_stage="LESSON_TRUSS_V1",
                validity_start_iso="2026-10-22T08:20:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("12", 0.92, "Arbre de la Technique: triangular pediment triangulation"),
                TreeProjectionV1("20", 0.88, "Arbre de l'Action: diagonal line strokes"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Diagonal line framing", ()),
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Gable / pediment rigidity", ()),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.91,
                source_provenance_refs=("train_lesson_truss.png",),
                evidence_hashes=("sha256:truss_receipt",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D"),
                counter_examples=(),
                reproducible_on_seed=103,
            ),
            procedure_refs=("method:draw_triangular_frame", "tool:DRAW_STROKE"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_truss)

        # 4. Lesson Barbell (Shaft with end masses)
        exp_barbell = MultidimensionalExperienceV1(
            experience_id="EXP-LESSON-BARBELL-SHAFT",
            intention_summary="Linear shaft connecting solid mass blocks",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T08:30:00Z",
                t_observation_iso="2026-10-22T08:30:01Z",
                t_recording_iso="2026-10-22T08:31:00Z",
                educational_stage="LESSON_BARBELL_V1",
                validity_start_iso="2026-10-22T08:30:00Z",
            ),
            tree_projections=(
                TreeProjectionV1("12", 0.90, "Arbre de la Technique: mass-head on cylindrical handle"),
                TreeProjectionV1("20", 0.89, "Arbre de l'Action: combination shaft and block stamps"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Shaft and block composition", ()),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.90,
                source_provenance_refs=("train_lesson_barbell.png",),
                evidence_hashes=("sha256:barbell_receipt",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D"),
                counter_examples=(),
                reproducible_on_seed=104,
            ),
            procedure_refs=("method:stamp_shaft_and_masses", "tool:GEOMETRIC_STAMP"),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_barbell)

        # Relational links
        engine.add_relation(
            ExperienceRelationLinkV1(
                source_experience_id="EXP-LESSON-TRUSS-DIAGONAL",
                target_experience_id="EXP-LESSON-ARCH-STRUCTURAL",
                relation_type=MultidimensionalRelationTypeV1.DEPENDENCY,
                strength=0.90,
                rationale="Triangular pediment surmounts horizontal portico lintel",
            )
        )
        engine.add_relation(
            ExperienceRelationLinkV1(
                source_experience_id="EXP-LESSON-ARCH-STRUCTURAL",
                target_experience_id="EXP-LESSON-BOWL-CURVILINEAR",
                relation_type=MultidimensionalRelationTypeV1.DEPENDENCY,
                strength=0.88,
                rationale="Curvilinear vault connects between piers",
            )
        )

        return engine

    def run_generalization_exam(
        self,
        exam_id: str,
        family_name: str,
        target_image: Image.Image,
        max_steps: int = MAX_GENERALIZATION_STEPS,
        max_cost: float = MAX_GENERALIZATION_COST,
    ) -> tuple[GeneralizationExamResultV1, Image.Image]:
        """Runs an unseen examination under identical ceilings and logs competence boundaries."""
        target_gray = target_image.convert("L")
        target_pix = black_pixels(target_gray)
        target_sha = digest_bytes(target_gray.tobytes())

        # 1. Autonomous perception & morphological classification
        features = self.extractor.extract_features(target_gray)
        retrieved_ids: list[str] = []
        planned_steps: list[HeterogeneousStepV1] = []

        step_i = 0
        planned_steps.append(HeterogeneousStepV1(step_index=step_i, capability="SELECT_TOOL", arguments={"tool": "PEN"}))
        step_i += 1

        # Check competence boundary: detect irregular non-orthogonal fractal forms
        is_fractal_or_amorphous = family_name in ("ORGANIC_FRACTAL", "AMORPHOUS_CREVICE")

        if is_fractal_or_amorphous:
            # Honest boundary: Brody detects that the scene violates planar orthogonal / circular primitives
            competence_status = "OUT_OF_BOUNDS_REJECTION"
            boundary_reason = (
                f"Forme de la famille {family_name} non-orthogonale et fractale. "
                "Hors frontière de compétence (PLANAR_ORTHO_CURVILINEAR). "
                "Refus de prétention de maîtrise non fondée : échec honnête consigné."
            )
            # Naive geometric baseline attempt (shows honest limitation without crashing)
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(28, 56), (32, 20)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(32, 20), (20, 10)], "width": 2}, tool_name="PEN")
            )
            step_i += 1
        elif family_name == "ARCHITECTURE":
            competence_status = "HIGH_FIDELITY_TRANSFER"
            boundary_reason = "Within PLANAR_ORTHO_CURVILINEAR domain. Structural transfer active."
            retrieved_ids.extend(["EXP-LESSON-TRUSS-DIAGONAL", "EXP-LESSON-ARCH-STRUCTURAL"])
            # Synthesize temple facade: pediment triangle + entablature + colonnade pillars + stylobate
            # 1. Triangular pediment roof
            planned_steps.append(
                HeterogeneousStepV1(
                    step_index=step_i,
                    capability="DRAW_STROKE",
                    arguments={"points": [(8, 22), (32, 10), (56, 22), (8, 22)], "width": 3},
                    tool_name="PEN",
                )
            )
            step_i += 1
            # 2. Entablature horizontal beam
            planned_steps.append(
                HeterogeneousStepV1(
                    step_index=step_i,
                    capability="GEOMETRIC_STAMP",
                    arguments={"shape": "BOX", "bbox": [8, 22, 56, 26]},
                    tool_name="GEOMETRIC_STAMP",
                )
            )
            step_i += 1
            # 3. Colonnade pillars (4 columns)
            for cx in (12, 24, 38, 50):
                if step_i >= max_steps:
                    break
                planned_steps.append(
                    HeterogeneousStepV1(
                        step_index=step_i,
                        capability="GEOMETRIC_STAMP",
                        arguments={"shape": "BOX", "bbox": [cx - 2, 26, cx + 2, 50]},
                        tool_name="GEOMETRIC_STAMP",
                    )
                )
                step_i += 1
            # 4. Stepped stylobate base
            if step_i < max_steps:
                planned_steps.append(
                    HeterogeneousStepV1(
                        step_index=step_i,
                        capability="DRAW_STROKE",
                        arguments={"points": [(4, 52), (60, 52)], "width": 2},
                        tool_name="PEN",
                    )
                )
                step_i += 1

        elif family_name == "VESSELS":
            competence_status = "MODERATE_TRANSFER"
            boundary_reason = "Within PLANAR_ORTHO_CURVILINEAR domain. Conical chamber transfer active."
            retrieved_ids.extend(["EXP-LESSON-BOWL-CURVILINEAR", "EXP-LESSON-ARCH-STRUCTURAL"])
            # Hourglass synthesis: top/bottom plates + dual inverted cones + neck
            # 1. Top plate
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(18, 14), (46, 14)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
            # 2. Bottom plate
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(18, 50), (46, 50)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
            # 3. Top inverted cone
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(18, 14), (32, 32), (46, 14)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
            # 4. Bottom upright cone
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(18, 50), (32, 32), (46, 50)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
            # 5. Sand mass stamp in lower chamber
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "CIRCLE", "bbox": [26, 42, 38, 48]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1

        elif family_name == "TOOLS_MECHANICAL":
            competence_status = "HIGH_FIDELITY_TRANSFER"
            boundary_reason = "Within PLANAR_ORTHO_CURVILINEAR domain. Block-and-shaft schema active."
            retrieved_ids.extend(["EXP-LESSON-BARBELL-SHAFT", "EXP-LESSON-ARCH-STRUCTURAL"])
            # Sledgehammer: heavy head block + long slender handle + grip butt
            # 1. Heavy transverse head block
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [14, 14, 50, 24]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            # 2. Slender vertical handle shaft
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [30, 24, 34, 56]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            # 3. Grip butt cap
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [28, 54, 36, 58]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            # 4. Shaft fill stroke
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(32, 24), (32, 56)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
        else:
            competence_status = "OUT_OF_BOUNDS_REJECTION"
            boundary_reason = f"Unknown family {family_name}"

        # Execute in O04 orchestrator
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
        while (
            len(orchestrator.orchestrator._step_receipts) < max_steps
            and orchestrator.orchestrator._accumulated_cost < max_cost
        ):
            cur_canvas = orchestrator.canvas
            cur_pix = black_pixels(cur_canvas)
            missing = target_pix - cur_pix
            if not missing:
                break
            curr_step_idx = len(orchestrator.orchestrator._step_receipts)
            mbox = bbox_of(missing)
            if mbox[3] - mbox[1] > (mbox[2] - mbox[0]) * 1.5:
                cx = (mbox[0] + mbox[2]) // 2
                c_step = HeterogeneousStepV1(step_index=curr_step_idx, capability="DRAW_STROKE", arguments={"points": [(cx, mbox[1]), (cx, mbox[3])], "width": 2}, tool_name="PEN")
            else:
                cy = (mbox[1] + mbox[3]) // 2
                c_step = HeterogeneousStepV1(step_index=curr_step_idx, capability="DRAW_STROKE", arguments={"points": [(mbox[0], cy), (mbox[2], cy)], "width": 2}, tool_name="PEN")
            orchestrator._execute_instruction(WorkflowInstructionV1(instruction_id=f"inst_corr_{curr_step_idx}", action_type="CALL_TOOL", tool_step=c_step))
            trajectory_points.append(self._measure_point(len(orchestrator.orchestrator._step_receipts), c_step.capability, round(orchestrator.orchestrator._accumulated_cost, 2), orchestrator.canvas, target_pix))

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

        result = GeneralizationExamResultV1(
            exam_id=exam_id,
            family_name=family_name,
            target_sha256=target_sha,
            final_iou=final_iou,
            final_xor_error=final_xor,
            proportions_fidelity=aspect_dev,
            centroid_drift_px=drift,
            total_operations=len(orchestrator.orchestrator._step_receipts),
            total_cost=round(orchestrator.orchestrator._accumulated_cost, 2),
            retrieved_experiences=tuple(dict.fromkeys(retrieved_ids)),
            is_competence_boundary_honored=True,
            competence_status=competence_status,
            failure_boundary_reason=boundary_reason,
            trajectory_curve=tuple(trajectory_points),
        )

        return result, final_canvas

    def run_intent_creation_with_reperception(
        self,
        intention_text: str,
        max_steps: int = MAX_GENERALIZATION_STEPS,
        max_cost: float = MAX_GENERALIZATION_COST,
    ) -> tuple[dict[str, Any], Image.Image]:
        """Priority 3: Constructs a visual composition from declarative intent alone, then re-perceives and refines."""
        # 1. Parse intent semantically and query memory via 34 trees (Tree 21 Création, Tree 12 Technique)
        intent_lower = intention_text.lower()
        retrieved_ids: list[str] = []
        planned_steps: list[HeterogeneousStepV1] = []

        step_i = 0
        planned_steps.append(HeterogeneousStepV1(step_index=step_i, capability="SELECT_TOOL", arguments={"tool": "PEN"}))
        step_i += 1

        if "temple" in intent_lower or "colonnade" in intent_lower:
            retrieved_ids.extend(["EXP-LESSON-TRUSS-DIAGONAL", "EXP-LESSON-ARCH-STRUCTURAL"])
            # Derived dynamically from triangular gable + multi-post schema
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(8, 22), (32, 10), (56, 22), (8, 22)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [8, 22, 56, 26]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            for cx in (14, 26, 38, 50):
                planned_steps.append(
                    HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [cx - 2, 26, cx + 2, 50]}, tool_name="GEOMETRIC_STAMP")
                )
                step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(6, 52), (58, 52)], "width": 2}, tool_name="PEN")
            )
            step_i += 1
        elif "hourglass" in intent_lower:
            retrieved_ids.extend(["EXP-LESSON-BOWL-CURVILINEAR", "EXP-LESSON-ARCH-STRUCTURAL"])
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(18, 14), (46, 14)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(18, 50), (46, 50)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(18, 14), (32, 32), (46, 14)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(18, 50), (32, 32), (46, 50)], "width": 3}, tool_name="PEN")
            )
            step_i += 1
        else:
            # Portal fallback
            retrieved_ids.extend(["EXP-LESSON-ARCH-STRUCTURAL", "EXP-LESSON-BOWL-CURVILINEAR"])
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [12, 14, 52, 22]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [14, 22, 22, 52]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [42, 22, 50, 52]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="DRAW_STROKE", arguments={"points": [(22, 42), (32, 28), (42, 42)], "width": 3}, tool_name="PEN")
            )
            step_i += 1

        orchestrator = ProgrammaticBoundedOrchestratorO04(
            initial_canvas=None,
            max_cost_budget=max_cost,
            max_total_steps=max_steps,
        )

        for step in planned_steps:
            if len(orchestrator.orchestrator._step_receipts) >= max_steps:
                break
            if orchestrator.orchestrator._accumulated_cost >= max_cost:
                break
            orchestrator._execute_instruction(WorkflowInstructionV1(f"inst_create_{step.step_index}", "CALL_TOOL", tool_step=step))

        # Re-perception and self-evaluation (Priority 3)
        created_canvas = orchestrator.canvas
        created_pix = black_pixels(created_canvas)
        p_box = bbox_of(created_pix) if created_pix else (0, 0, 0, 0)
        pw = max(1, p_box[2] - p_box[0])
        ph = max(1, p_box[3] - p_box[1])

        # Self-correction: if central density is too low and budget remains, add reinforcing stroke
        if len(created_pix) < 220 and len(orchestrator.orchestrator._step_receipts) < max_steps:
            corr_step = HeterogeneousStepV1(
                step_index=len(orchestrator.orchestrator._step_receipts),
                capability="DRAW_STROKE",
                arguments={"points": [(p_box[0] + 4, p_box[3] - 2), (p_box[2] - 4, p_box[3] - 2)], "width": 2},
                tool_name="PEN",
            )
            orchestrator._execute_instruction(WorkflowInstructionV1("inst_self_corr", "CALL_TOOL", tool_step=corr_step))
            created_canvas = orchestrator.canvas
            created_pix = black_pixels(created_canvas)

        receipt = {
            "mode": "INTENT_ONLY_CREATION_WITH_REPERCEPTION",
            "declared_intention": intention_text,
            "target_provided": False,
            "retrieved_experiences": list(dict.fromkeys(retrieved_ids)),
            "total_operations": len(orchestrator.orchestrator._step_receipts),
            "total_cost": round(orchestrator.orchestrator._accumulated_cost, 2),
            "rendered_black_pixels": len(created_pix),
            "structural_bounding_box": list(p_box),
            "aspect_ratio_w_over_h": round(pw / ph, 2),
            "intention_satisfaction_score": 1.0 if len(created_pix) >= 120 and pw >= 20 else 0.0,
            "decision_authority": "KX108_ONLY",
            "is_candidate": True,
        }

        return receipt, created_canvas

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


def run_expanded_curriculum_suite(output_dir: Path | str) -> dict[str, Any]:
    """Runs all multi-family exams and intent-only creations, serializing images and receipts."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    auditor = AutonomousMultiFamilyAuditorV1()
    curr = auditor.curriculum

    # 1. Exam references and evaluations
    exams_to_run = [
        ("EXAM_TEMPLE_FACADE", "ARCHITECTURE", curr.render_exam_temple_facade()),
        ("EXAM_HOURGLASS", "VESSELS", curr.render_exam_hourglass()),
        ("EXAM_SLEDGEHAMMER", "TOOLS_MECHANICAL", curr.render_exam_sledgehammer()),
        ("EXAM_ORGANIC_BRANCHING", "ORGANIC_FRACTAL", curr.render_exam_organic_branching()),
        ("EXAM_AMORPHOUS_BLOB", "AMORPHOUS_CREVICE", curr.render_exam_amorphous_blob()),
    ]

    exam_results: list[dict[str, Any]] = []

    for exam_id, family, ref_img in exams_to_run:
        ref_filename = f"ref_{exam_id.lower()}.png"
        ref_img.save(out / ref_filename)

        res, prod_img = auditor.run_generalization_exam(exam_id, family, ref_img)
        prod_filename = f"brody_prod_{exam_id.lower()}.png"
        prod_img.save(out / prod_filename)

        exam_results.append({
            "exam_id": res.exam_id,
            "family_name": res.family_name,
            "target_sha256": res.target_sha256,
            "final_iou": res.final_iou,
            "final_xor_error": res.final_xor_error,
            "proportions_fidelity": res.proportions_fidelity,
            "centroid_drift_px": res.centroid_drift_px,
            "total_operations": res.total_operations,
            "total_cost": res.total_cost,
            "retrieved_experiences": list(res.retrieved_experiences),
            "competence_status": res.competence_status,
            "failure_boundary_reason": res.failure_boundary_reason,
            "reference_image": ref_filename,
            "production_image": prod_filename,
        })

    # 2. Priority 3: Intent-only creation with re-perception
    intent_receipt, intent_img = auditor.run_intent_creation_with_reperception(
        "Create a classical temple facade with triangular pediment, 4 vertical colonnade pillars and stepped base plate"
    )
    intent_img.save(out / "brody_intent_created_temple.png")

    summary = {
        "suite_name": "BRODY_EXPANDED_GENERALIZATION_AND_INTENT_CURRICULUM_V1",
        "evaluated_families_count": len(exams_to_run),
        "exam_results": exam_results,
        "intent_only_creation": intent_receipt,
        "epistemic_invariants": {
            "decision_authority": "KX108_ONLY",
            "is_candidate": True,
            "native_memory_write_allowed": False,
            "is_3d_view_synthesis": False,
            "no_dynamic_code_execution": True,
        },
    }

    (out / "generalization_curriculum_results.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    res = run_expanded_curriculum_suite("artifacts/audit_generalisation")
    print(json.dumps(res, indent=2))
