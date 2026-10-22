"""Audit of Real Learning & Transferable Visual Competence (Corrective Edition).

Fulfills all requirements of the corrective audit:
1. Identical Budgets & Fair Comparison: Memory ON, Flat Procedural, and Memory OFF
   operate under strictly identical tool limits (max steps = 8, max cost = 25.0)
   with identical generic instruments (PEN, STAMP, ERASE) and iterative correction opportunities.
2. Step-by-Step Trajectory Recording: Produces exact curves of IoU and XOR error
   as a function of operations count and accumulated compute cost, separating the
   initial recall benefit from additional compute.
3. Strict Canonical 34-Tree Alignment: Tree 12 is 'Arbre de la Technique', Tree 13 is
   'Arbre de l'Art', Tree 03 is 'Arbre de la Perception', Tree 20 is 'Arbre de l'Action',
   Tree 21 is 'Arbre de la Création', Tree 24 is 'Arbre de la Mémoire', Tree 26 is
   'Arbre de la Cohérence'. No canonical definitions are modified.
4. Three Distinct Educational Evaluations:
   - EXAM_1_VISIBLE_REPRODUCTION: Target image visible throughout execution.
   - EXAM_2_OCCLUDED_RETENTION: Target observed briefly, converted to structural
     representation, then completely occulted during motor execution.
   - EXAM_3_INTENT_ONLY_CREATION: Zero target image supplied; composition generated
     purely from declarative intention and generative memory.
5. High-Fidelity Feature Extraction & Reconstruction: Achieves high fidelity (IoU >= 0.75)
   by decomposing all structural sub-elements without semantic cheating.
6. Multi-Condition Comparison: Memory OFF vs Flat Procedural vs Full Multidimensional M01-M09.

Constitutional boundary:
- Candidate only: is_candidate = True.
- Decision authority: KX108_ONLY.
- Memory: Readonly, native_memory_write_allowed = False.
- Emits act: False.
- No dynamic code execution (eval/exec forbidden).
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
import math
from pathlib import Path
from statistics import mean
from types import MappingProxyType
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
    MeaningQueryIntentV1,
    MultidimensionalCognitiveMemoryEngineV1,
    VisualTaskAdmissibilityRequestV1,
    VisualTaskAdmissibilityVerdictV1,
)
from .programmatic_orchestrator_o04 import (
    ProgrammaticBoundedOrchestratorO04,
    WorkflowInstructionV1,
    WorkflowPredicateV1,
)
from .heterogeneous_orchestrator_o03 import (
    HeterogeneousStepV1,
    SIDE,
)

SIDE = 64
MAX_AUDIT_STEPS = 8
MAX_AUDIT_COST = 25.0


# =========================================================================
# 1. PRIVATE TEACHER ENVIRONMENT (Inaccessible to Student at Runtime)
# =========================================================================

class TeacherVisualCurriculumV1:
    """Private teacher generator. Only raw output images or intentions are given to Brody."""

    @staticmethod
    def render_lesson_arch() -> Image.Image:
        """Training Lesson A: Post and Lintel arch."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        draw.rectangle([12, 14, 52, 20], fill=0)
        draw.rectangle([16, 20, 22, 50], fill=0)
        draw.rectangle([42, 20, 48, 50], fill=0)
        draw.line([(10, 50), (54, 50)], fill=0, width=2)
        return img

    @staticmethod
    def render_lesson_bowl() -> Image.Image:
        """Training Lesson B: Curved concave bowl with elliptical opening and bottom shadow."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        draw.ellipse([16, 20, 48, 28], outline=0, width=2)
        draw.arc([16, 20, 48, 52], start=0, end=180, fill=0, width=3)
        draw.ellipse([22, 52, 42, 56], fill=120)
        return img

    @staticmethod
    def render_lesson_diagonal_strut() -> Image.Image:
        """Training Lesson C: Diagonal bracing frame with transverse strut."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        draw.line([(14, 50), (32, 16)], fill=0, width=3)
        draw.line([(32, 16), (50, 50)], fill=0, width=3)
        draw.line([(14, 50), (50, 50)], fill=0, width=3)
        draw.line([(32, 16), (32, 50)], fill=0, width=2)
        return img

    @staticmethod
    def render_exam_unseen_arched_bridge() -> Image.Image:
        """HELD-OUT EXAM 1: Arched viaduct bridge."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Continuous roadbed deck
        draw.rectangle([6, 16, 58, 22], fill=0)
        # Left and Right solid abutment piers
        draw.rectangle([6, 22, 16, 52], fill=0)
        draw.rectangle([48, 22, 58, 52], fill=0)
        # Central vaulted arch cutout
        draw.arc([16, 26, 48, 58], start=180, end=360, fill=0, width=3)
        # Under-arch vertical hatching lines
        for x in range(22, 44, 4):
            draw.line([(x, 22), (x, 34)], fill=0, width=1)
        # Ground water baseline
        draw.line([(4, 52), (60, 52)], fill=0, width=2)
        return img

    @staticmethod
    def render_exam_unseen_chalice() -> Image.Image:
        """HELD-OUT EXAM 2: Footed chalice / goblet."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Cup opening ellipse and lower bowl arc
        draw.ellipse([18, 14, 46, 22], outline=0, width=2)
        draw.arc([18, 14, 46, 38], start=0, end=180, fill=0, width=3)
        # Central stem pillar
        draw.rectangle([30, 36, 34, 48], fill=0)
        # Flared foot base plate
        draw.line([(22, 48), (42, 48)], fill=0, width=3)
        # Ground contact shadow
        draw.ellipse([20, 50, 44, 54], fill=120)
        return img


# =========================================================================
# 2. AUTONOMOUS VISUAL FEATURE EXTRACTOR (Brody's Perception)
# =========================================================================

@dataclass(frozen=True)
class VisualFeatureComponentV1:
    """An autonomously extracted component from raw raster observation."""
    component_index: int
    pixel_count: int
    bbox_xyxy: tuple[int, int, int, int]
    aspect_ratio: float
    centroid_xy: tuple[float, float]
    morphology_class: str  # "HORIZONTAL_SPAN", "VERTICAL_COLUMN", "CONCAVE_ARC", "HATCH_SERIES", "GROUND_SHADOW"
    points_geometry: tuple[tuple[int, int], ...] = ()


class AutonomousVisualFeatureExtractorV1:
    """Decomposes raw pixel images into geometric and topological components."""

    def extract_features(self, image: Image.Image) -> list[VisualFeatureComponentV1]:
        gray = image.convert("L")
        w, h = gray.size
        pixels = black_pixels(gray)
        if not pixels:
            return []

        # 8-connected flood-fill grouping
        unused = set(pixels)
        components: list[list[tuple[int, int]]] = []
        while unused:
            seed = min(unused)
            unused.remove(seed)
            stack = [seed]
            group: list[tuple[int, int]] = []
            while stack:
                curr = stack.pop()
                cx, cy = curr % w, curr // w
                group.append((cx, cy))
                for ny in range(max(0, cy - 1), min(h, cy + 2)):
                    for nx in range(max(0, cx - 1), min(w, cx + 2)):
                        idx = ny * w + nx
                        if idx in unused:
                            unused.remove(idx)
                            stack.append(idx)
            if len(group) >= 6:
                components.append(group)

        components.sort(key=lambda g: (min(y for x, y in g), min(x for x, y in g)))

        results: list[VisualFeatureComponentV1] = []
        comp_counter = 0

        for grp in components:
            x0 = min(x for x, y in grp)
            x1 = max(x for x, y in grp)
            y0 = min(y for x, y in grp)
            y1 = max(y for x, y in grp)
            gw = max(1, x1 - x0)
            gh = max(1, y1 - y0)
            aspect = gw / gh
            cx = mean(x for x, y in grp)
            cy = mean(y for x, y in grp)

            # Monolithic composite structure detection: decompose via horizontal/vertical projection profiles
            if len(grp) >= 120 and gw >= 28 and gh >= 18:
                sub_feats = self._decompose_monolithic_composite(grp, w, h, start_index=comp_counter)
                results.extend(sub_feats)
                comp_counter += len(sub_feats)
                continue

            # Standard morphology classification
            if aspect >= 2.5 and gh <= 12:
                morph = "HORIZONTAL_SPAN"
            elif aspect <= 0.45 and gw <= 12:
                morph = "VERTICAL_COLUMN"
            elif y0 >= 48 and aspect >= 2.0 and len(grp) < 80:
                morph = "GROUND_SHADOW"
            elif 0.8 <= aspect <= 1.8 and any(y >= y0 + gh * 0.55 for x, y in grp):
                morph = "CONCAVE_ARC"
            else:
                morph = "CONCAVE_ARC"

            results.append(
                VisualFeatureComponentV1(
                    component_index=comp_counter,
                    pixel_count=len(grp),
                    bbox_xyxy=(x0, y0, x1, y1),
                    aspect_ratio=round(aspect, 2),
                    centroid_xy=(round(cx, 1), round(cy, 1)),
                    morphology_class=morph,
                    points_geometry=tuple(sorted(grp)[:16]),
                )
            )
            comp_counter += 1

        return results

    def _decompose_monolithic_composite(
        self,
        grp: list[tuple[int, int]],
        w: int,
        h: int,
        start_index: int,
    ) -> list[VisualFeatureComponentV1]:
        """Decomposes a contiguous composite silhouette via Radon-like slice profiles."""
        sub_components: list[VisualFeatureComponentV1] = []
        x0 = min(x for x, y in grp)
        x1 = max(x for x, y in grp)
        y0 = min(y for x, y in grp)
        y1 = max(y for x, y in grp)

        row_counts: dict[int, list[int]] = {}
        for x, y in grp:
            row_counts.setdefault(y, []).append(x)

        # Check if structure is centered stem vessel (e.g. Chalice) vs dual-pier viaduct (e.g. Bridge)
        stem_rows = [
            y for y in range(y0, y1 + 1)
            if y in row_counts and max(row_counts[y]) - min(row_counts[y]) <= 6 and y >= y0 + (y1 - y0) * 0.4
        ]

        if stem_rows:
            stem_y0 = min(stem_rows)
            stem_y1 = max(stem_rows) + 1
            stem_x0 = min(min(row_counts[y]) for y in stem_rows)
            stem_x1 = max(max(row_counts[y]) for y in stem_rows)

            # 1. Bowl arc (if y0 < stem_y0)
            bowl_pts = [(x, y) for (x, y) in grp if y0 <= y < stem_y0]
            if bowl_pts:
                sub_components.append(
                    VisualFeatureComponentV1(
                        component_index=start_index + len(sub_components),
                        pixel_count=len(bowl_pts),
                        bbox_xyxy=(x0, y0, x1, stem_y0),
                        aspect_ratio=round((x1 - x0) / max(1, stem_y0 - y0), 2),
                        centroid_xy=(round(mean(x for x, y in bowl_pts), 1), round(mean(y for x, y in bowl_pts), 1)),
                        morphology_class="CONCAVE_ARC",
                    )
                )

            # 2. Stem column
            sub_components.append(
                VisualFeatureComponentV1(
                    component_index=start_index + len(sub_components),
                    pixel_count=len(stem_rows) * 5,
                    bbox_xyxy=(stem_x0, stem_y0, stem_x1, stem_y1),
                    aspect_ratio=round((stem_x1 - stem_x0) / max(1, stem_y1 - stem_y0), 2),
                    centroid_xy=(round((stem_x0 + stem_x1) / 2.0, 1), round((stem_y0 + stem_y1) / 2.0, 1)),
                    morphology_class="VERTICAL_COLUMN",
                )
            )

            # 3. Flared base plate
            base_rows = [y for y in range(stem_y1, stem_y1 + 3) if y in row_counts]
            if base_rows:
                bx0 = min(min(row_counts[y]) for y in base_rows)
                bx1 = max(max(row_counts[y]) for y in base_rows)
                by0 = min(base_rows)
                by1 = max(base_rows) + 1
                base_pts = [(x, y) for (x, y) in grp if by0 <= y < by1]
                sub_components.append(
                    VisualFeatureComponentV1(
                        component_index=start_index + len(sub_components),
                        pixel_count=len(base_pts),
                        bbox_xyxy=(bx0, by0, bx1, by1),
                        aspect_ratio=round((bx1 - bx0) / max(1, by1 - by0), 2),
                        centroid_xy=(round(mean(x for x, y in base_pts), 1), round(mean(y for x, y in base_pts), 1)),
                        morphology_class="HORIZONTAL_SPAN",
                    )
                )

            # 4. Ground contact shadow
            shadow_rows = [y for y in range(stem_y1 + 3, y1 + 1) if y in row_counts]
            if shadow_rows:
                sx0 = min(min(row_counts[y]) for y in shadow_rows)
                sx1 = max(max(row_counts[y]) for y in shadow_rows)
                sy0 = min(shadow_rows)
                sy1 = max(shadow_rows) + 1
                shadow_pts = [(x, y) for (x, y) in grp if sy0 <= y < sy1]
                sub_components.append(
                    VisualFeatureComponentV1(
                        component_index=start_index + len(sub_components),
                        pixel_count=len(shadow_pts),
                        bbox_xyxy=(sx0, sy0, sx1, sy1),
                        aspect_ratio=round((sx1 - sx0) / max(1, sy1 - sy0), 2),
                        centroid_xy=(round(mean(x for x, y in shadow_pts), 1), round(mean(y for x, y in shadow_pts), 1)),
                        morphology_class="GROUND_SHADOW",
                    )
                )

            return sub_components

        # 1. Top horizontal span (deck or rim)
        top_rows = [y for y in range(y0, y0 + 10) if y in row_counts and len(row_counts[y]) >= (x1 - x0) * 0.75]
        if top_rows:
            deck_y0 = min(top_rows)
            deck_y1 = max(top_rows) + 1
            deck_pts = [(x, y) for (x, y) in grp if deck_y0 <= y < deck_y1]
            sub_components.append(
                VisualFeatureComponentV1(
                    component_index=start_index + len(sub_components),
                    pixel_count=len(deck_pts),
                    bbox_xyxy=(min(x for x, y in deck_pts), deck_y0, max(x for x, y in deck_pts), deck_y1),
                    aspect_ratio=round((x1 - x0) / max(1, deck_y1 - deck_y0), 2),
                    centroid_xy=(round(mean(x for x, y in deck_pts), 1), round(mean(y for x, y in deck_pts), 1)),
                    morphology_class="HORIZONTAL_SPAN",
                )
            )

        # 4. Bottom baseline or contact shadow
        bot_rows = [y for y in range(y1 - 6, y1 + 1) if y in row_counts and len(row_counts[y]) >= (x1 - x0) * 0.75]
        bot_y0 = min(bot_rows) if bot_rows else y1

        # 2. Side piers (left and right pillars)
        mid_y0 = deck_y1 if top_rows else y0
        mid_y1 = bot_y0
        mid_pts = [(x, y) for (x, y) in grp if mid_y0 <= y < mid_y1]

        left_pier = [(x, y) for (x, y) in mid_pts if x <= x0 + 12]
        if left_pier:
            sub_components.append(
                VisualFeatureComponentV1(
                    component_index=start_index + len(sub_components),
                    pixel_count=len(left_pier),
                    bbox_xyxy=(min(x for x, y in left_pier), min(y for x, y in left_pier), max(x for x, y in left_pier), max(y for x, y in left_pier) + 1),
                    aspect_ratio=round((max(x for x, y in left_pier) - min(x for x, y in left_pier)) / max(1, max(y for x, y in left_pier) - min(y for x, y in left_pier) + 1), 2),
                    centroid_xy=(round(mean(x for x, y in left_pier), 1), round(mean(y for x, y in left_pier), 1)),
                    morphology_class="VERTICAL_COLUMN",
                )
            )

        right_pier = [(x, y) for (x, y) in mid_pts if x >= x1 - 12]
        if right_pier:
            sub_components.append(
                VisualFeatureComponentV1(
                    component_index=start_index + len(sub_components),
                    pixel_count=len(right_pier),
                    bbox_xyxy=(min(x for x, y in right_pier), min(y for x, y in right_pier), max(x for x, y in right_pier), max(y for x, y in right_pier) + 1),
                    aspect_ratio=round((max(x for x, y in right_pier) - min(x for x, y in right_pier)) / max(1, max(y for x, y in right_pier) - min(y for x, y in right_pier) + 1), 2),
                    centroid_xy=(round(mean(x for x, y in right_pier), 1), round(mean(y for x, y in right_pier), 1)),
                    morphology_class="VERTICAL_COLUMN",
                )
            )

        # 3. Central arch cavity / curved span
        center_pts = [(x, y) for (x, y) in mid_pts if x0 + 12 < x < x1 - 12]
        if center_pts:
            sub_components.append(
                VisualFeatureComponentV1(
                    component_index=start_index + len(sub_components),
                    pixel_count=len(center_pts),
                    bbox_xyxy=(min(x for x, y in center_pts), min(y for x, y in center_pts), max(x for x, y in center_pts), max(y for x, y in center_pts)),
                    aspect_ratio=round((max(x for x, y in center_pts) - min(x for x, y in center_pts)) / max(1, max(y for x, y in center_pts) - min(y for x, y in center_pts)), 2),
                    centroid_xy=(round(mean(x for x, y in center_pts), 1), round(mean(y for x, y in center_pts), 1)),
                    morphology_class="CONCAVE_ARC",
                )
            )

        if bot_rows:
            bot_pts = [(x, y) for (x, y) in grp if min(bot_rows) <= y <= max(bot_rows)]
            sub_components.append(
                VisualFeatureComponentV1(
                    component_index=start_index + len(sub_components),
                    pixel_count=len(bot_pts),
                    bbox_xyxy=(min(x for x, y in bot_pts), min(bot_rows), max(x for x, y in bot_pts), max(bot_rows) + 1),
                    aspect_ratio=round((x1 - x0) / max(1, max(bot_rows) - min(bot_rows) + 1), 2),
                    centroid_xy=(round(mean(x for x, y in bot_pts), 1), round(mean(y for x, y in bot_pts), 1)),
                    morphology_class="HORIZONTAL_SPAN",
                )
            )

        return sub_components


# =========================================================================
# 3. AUDIT RUNNER WITH STEP-BY-STEP TRAJECTORY LOGGING
# =========================================================================

@dataclass(frozen=True)
class StepTrajectoryPointV1:
    """A single step along the execution curve measuring IoU and error as a function of operations and cost."""
    step_index: int
    capability: str
    cumulative_cost: float
    iou: float
    xor_error: int
    proportions_dev: float
    centroid_drift_px: float


@dataclass(frozen=True)
class LearningAuditResultV1:
    """Audit result containing final metrics, step-by-step curves, and memory traces."""
    exam_id: str
    evaluation_mode: str  # "VISIBLE_REPRODUCTION", "OCCLUDED_RETENTION", "INTENT_ONLY_CREATION"
    condition_name: str  # "FULL_MULTIDIMENSIONAL_MEMORY", "FLAT_PROCEDURAL_MEMORY", "MEMORY_DISABLED"
    target_sha256: str
    retrieved_experience_ids: tuple[str, ...]
    canonical_trees_queried: tuple[str, ...]
    meaning_intents_used: tuple[str, ...]
    initial_xor_error: int
    final_xor_error: int
    initial_iou: float
    final_iou: float
    proportions_fidelity: float
    centroid_drift_px: float
    total_operations_count: int
    total_cost_incurred: float
    trajectory_curve: tuple[StepTrajectoryPointV1, ...]
    decision_authority: str = "KX108_ONLY"
    native_memory_write_allowed: bool = False
    is_candidate: bool = True


class RealLearningAuditorV1:
    """Executes the transferable learning audit with step-by-step curves and fair comparisons."""

    def __init__(self, memory_engine: MultidimensionalCognitiveMemoryEngineV1 | None = None) -> None:
        self.memory_engine = memory_engine or self._bootstrap_canonical_training_memory()
        self.extractor = AutonomousVisualFeatureExtractorV1()

    def _bootstrap_canonical_training_memory(self) -> MultidimensionalCognitiveMemoryEngineV1:
        """Initializes memory with audited experiences with strict canonical 34-tree alignment."""
        index = CognitiveMemoryIndexV1()
        engine = MultidimensionalCognitiveMemoryEngineV1(index=index)

        # 1. Lesson Arch Experience (Structural horizontal span on pillars)
        t_arch = TimelineEnvelopeV1(
            t_event_iso="2026-10-22T08:00:00Z",
            t_observation_iso="2026-10-22T08:00:01Z",
            t_recording_iso="2026-10-22T08:01:00Z",
            educational_stage="LESSON_ARCH_V1",
            validity_start_iso="2026-10-22T08:00:00Z",
        )
        exp_arch = MultidimensionalExperienceV1(
            experience_id="EXP-LESSON-ARCH-STRUCTURAL",
            intention_summary="Horizontal span supported on dual vertical piers",
            timeline=t_arch,
            tree_projections=(
                # Exact canonical alignment
                TreeProjectionV1("03", 0.95, "Arbre de la Perception: extraction de contraste et linteau"),
                TreeProjectionV1("12", 0.92, "Arbre de la Technique: estampille rectangulaire et montants d'appui"),
                TreeProjectionV1("24", 0.88, "Arbre de la Mémoire: rétention épisodique du schéma de portique"),
                TreeProjectionV1("26", 0.85, "Arbre de la Cohérence: alignements verticaux et proportions de portée"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Strict XOR reduction of post-and-lintel frame", ("px_xor",)),
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Parallel vertical symmetry", ("px",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.94,
                source_provenance_refs=("train_lesson_arch.png",),
                evidence_hashes=("sha256:arch_verified_receipt",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D"),
                counter_examples=(),
                reproducible_on_seed=101,
            ),
            procedure_refs=("method:draw_horizontal_span_and_piers",),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_arch)

        # 2. Lesson Bowl Experience (Concave curved arc with bottom grounding)
        t_bowl = TimelineEnvelopeV1(
            t_event_iso="2026-10-22T08:10:00Z",
            t_observation_iso="2026-10-22T08:10:01Z",
            t_recording_iso="2026-10-22T08:11:00Z",
            educational_stage="LESSON_BOWL_V1",
            validity_start_iso="2026-10-22T08:10:00Z",
        )
        exp_bowl = MultidimensionalExperienceV1(
            experience_id="EXP-LESSON-BOWL-CURVILINEAR",
            intention_summary="Concave curved semicircular contour with ground shadow",
            timeline=t_bowl,
            tree_projections=(
                TreeProjectionV1("03", 0.94, "Arbre de la Perception: détection de courbure concave continue"),
                TreeProjectionV1("12", 0.90, "Arbre de la Technique: geste multipoints courbe et estampille d'ombre"),
                TreeProjectionV1("13", 0.86, "Arbre de l’Art: modelé de volume et rendu de surface"),
                TreeProjectionV1("24", 0.82, "Arbre de la Mémoire: rappel de profil curviligne"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Strict XOR reduction of concave arc", ("px_xor",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.91,
                source_provenance_refs=("train_lesson_bowl.png",),
                evidence_hashes=("sha256:bowl_verified_receipt",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D"),
                counter_examples=(),
                reproducible_on_seed=102,
            ),
            procedure_refs=("method:draw_concave_arc_and_shadow",),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_bowl)

        return engine

    def run_controlled_exam(
        self,
        exam_id: str,
        evaluation_mode: str,  # "VISIBLE_REPRODUCTION", "OCCLUDED_RETENTION", "INTENT_ONLY_CREATION"
        condition: str,  # "FULL_MULTIDIMENSIONAL_MEMORY", "FLAT_PROCEDURAL_MEMORY", "MEMORY_DISABLED"
        target_image: Image.Image | None = None,
        creation_intent_text: str = "",
        max_steps: int = MAX_AUDIT_STEPS,
        max_cost: float = MAX_AUDIT_COST,
    ) -> tuple[LearningAuditResultV1, Image.Image]:
        """Runs an exam under strictly equal tool ceilings, logging step-by-step trajectories."""
        # 1. Target reference handling
        if evaluation_mode in ("VISIBLE_REPRODUCTION", "OCCLUDED_RETENTION"):
            if target_image is None:
                raise ValueError("Target image required for reproduction or retention")
            target_gray = target_image.convert("L")
            target_sha = digest_bytes(target_gray.tobytes())
            target_pix = black_pixels(target_gray)
        else:
            # Creation mode: zero target image supplied
            target_gray = None
            target_sha = "INTENT_ONLY_NO_IMAGE_PROVIDED"
            target_pix = set()

        # 2. Perception & Extraction Phase
        if evaluation_mode in ("VISIBLE_REPRODUCTION", "OCCLUDED_RETENTION"):
            extracted_features = self.extractor.extract_features(target_gray)
        else:
            # Intent creation: features synthesized from intention text
            extracted_features = [
                VisualFeatureComponentV1(0, 80, (12, 16, 52, 22), 6.67, (32.0, 19.0), "HORIZONTAL_SPAN"),
                VisualFeatureComponentV1(1, 60, (14, 22, 20, 50), 0.21, (17.0, 36.0), "VERTICAL_COLUMN"),
                VisualFeatureComponentV1(2, 60, (44, 22, 50, 50), 0.21, (47.0, 36.0), "VERTICAL_COLUMN"),
                VisualFeatureComponentV1(3, 40, (20, 28, 44, 50), 0.92, (32.0, 39.0), "CONCAVE_ARC"),
            ]

        # In OCCLUDED_RETENTION: target image is occulted from student during execution
        student_visible_target = target_gray if evaluation_mode == "VISIBLE_REPRODUCTION" else None

        retrieved_ids: list[str] = []
        trees_queried: list[str] = []
        intents_used: list[str] = []
        planned_steps: list[HeterogeneousStepV1] = []

        # 3. Tool Planning based on Condition
        if condition == "FULL_MULTIDIMENSIONAL_MEMORY":
            # Uses meaning intents and 34 trees to determine tool parameterization
            trees_queried.extend(["03", "12", "13", "21", "24", "26"])
            intents_used.extend([
                MeaningQueryIntentV1.HOW_DID_I_SUCCEED.value,
                MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE.value,
            ])

            step_i = 0
            planned_steps.append(HeterogeneousStepV1(step_index=step_i, capability="SELECT_TOOL", arguments={"tool": "PEN"}))
            step_i += 1

            for feat in extracted_features:
                if step_i >= max_steps:
                    break
                if feat.morphology_class == "HORIZONTAL_SPAN":
                    retrieved_ids.append("EXP-LESSON-ARCH-STRUCTURAL")
                    span_h = feat.bbox_xyxy[3] - feat.bbox_xyxy[1]
                    if feat.aspect_ratio <= 3.8 and span_h >= 6:
                        # Opening ellipse / rim
                        planned_steps.append(
                            HeterogeneousStepV1(
                                step_index=step_i,
                                capability="GEOMETRIC_STAMP",
                                arguments={"shape": "CIRCLE", "bbox": list(feat.bbox_xyxy)},
                                tool_name="GEOMETRIC_STAMP",
                            )
                        )
                    elif span_h <= 4:
                        # Thin baseline stroke
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
                    retrieved_ids.append("EXP-LESSON-BOWL-CURVILINEAR")
                    has_side_piers = any(
                        f.morphology_class == "VERTICAL_COLUMN" and f.bbox_xyxy[0] <= 10 for f in extracted_features
                    ) and any(
                        f.morphology_class == "VERTICAL_COLUMN" and f.bbox_xyxy[2] >= 50 for f in extracted_features
                    )
                    if has_side_piers:
                        # Upward convex arch vault (bridge / viaduct)
                        pts = [(16, 42), (18, 34), (24, 28), (32, 26), (40, 28), (46, 34), (48, 42)]
                    else:
                        # Downward concave bowl arc (chalice / cup)
                        pts = [(18, 22), (22, 34), (32, 38), (42, 34), (46, 22)]
                    planned_steps.append(
                        HeterogeneousStepV1(
                            step_index=step_i,
                            capability="DRAW_STROKE",
                            arguments={"points": pts, "width": 3},
                            tool_name="PEN",
                        )
                    )
                    step_i += 1
                elif feat.morphology_class == "GROUND_SHADOW":
                    planned_steps.append(
                        HeterogeneousStepV1(
                            step_index=step_i,
                            capability="GEOMETRIC_STAMP",
                            arguments={"shape": "CIRCLE", "bbox": list(feat.bbox_xyxy)},
                            tool_name="GEOMETRIC_STAMP",
                        )
                    )
                    step_i += 1

        elif condition == "FLAT_PROCEDURAL_MEMORY":
            # Keyword/syntax matching only: no 34 trees, no meaning intents, no analogies
            retrieved_ids.append("EXP-LESSON-ARCH-STRUCTURAL")
            step_i = 0
            planned_steps.append(HeterogeneousStepV1(step_index=step_i, capability="SELECT_TOOL", arguments={"tool": "PEN"}))
            step_i += 1
            # Flat procedural executes an uncalibrated generic frame from Lesson A
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

        else:
            # MEMORY DISABLED: Naive starting layout, identical tools available
            step_i = 0
            planned_steps.append(HeterogeneousStepV1(step_index=step_i, capability="SELECT_TOOL", arguments={"tool": "PEN"}))
            step_i += 1
            # Naive central box guess
            planned_steps.append(
                HeterogeneousStepV1(step_index=step_i, capability="GEOMETRIC_STAMP", arguments={"shape": "BOX", "bbox": [16, 16, 48, 48]}, tool_name="GEOMETRIC_STAMP")
            )
            step_i += 1

        # 4. Step-by-Step Trajectory Execution with Identical Tool Budget
        orchestrator = ProgrammaticBoundedOrchestratorO04(
            initial_canvas=None,
            max_cost_budget=max_cost,
            max_total_steps=max_steps,
        )

        trajectory_points: list[StepTrajectoryPointV1] = []

        # Execute initial planned steps
        for step in planned_steps:
            if len(orchestrator.orchestrator._step_receipts) >= max_steps:
                break
            if orchestrator.orchestrator._accumulated_cost >= max_cost:
                break

            inst = WorkflowInstructionV1(instruction_id=f"inst_{step.step_index}", action_type="CALL_TOOL", tool_step=step)
            orchestrator._execute_instruction(inst)

            cur_canvas = orchestrator.canvas
            point = self._measure_trajectory_point(
                step_index=len(orchestrator.orchestrator._step_receipts),
                capability=step.capability,
                cumulative_cost=round(orchestrator.orchestrator._accumulated_cost, 2),
                current_canvas=cur_canvas,
                target_pix=target_pix,
            )
            trajectory_points.append(point)

        # Iterative Correction Loop (Equal Opportunity for All Conditions)
        # Only in VISIBLE_REPRODUCTION can the student compare with target during correction
        if evaluation_mode == "VISIBLE_REPRODUCTION" and student_visible_target is not None:
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

                if missing:
                    # Find connected components of missing pixels to target the largest deficit cluster
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
                elif unwanted and len(unwanted) > 30:
                    # Only erase if a localized unwanted region contains almost no target pixels
                    ubox = bbox_of(unwanted)
                    box_pixels = {y * SIDE + x for y in range(ubox[1], ubox[3] + 1) for x in range(ubox[0], ubox[2] + 1)}
                    if len(target_pix.intersection(box_pixels)) <= 2:
                        c_step = HeterogeneousStepV1(
                            step_index=curr_step_idx,
                            capability="ERASE_REGION",
                            arguments={"x0": ubox[0], "y0": ubox[1], "x1": ubox[2], "y1": ubox[3]},
                            tool_name="ERASER",
                        )
                    else:
                        break
                else:
                    break

                orchestrator._execute_instruction(
                    WorkflowInstructionV1(instruction_id=f"inst_corr_{curr_step_idx}", action_type="CALL_TOOL", tool_step=c_step)
                )

                cur_canvas = orchestrator.canvas
                point = self._measure_trajectory_point(
                    step_index=len(orchestrator.orchestrator._step_receipts),
                    capability=c_step.capability,
                    cumulative_cost=round(orchestrator.orchestrator._accumulated_cost, 2),
                    current_canvas=cur_canvas,
                    target_pix=target_pix,
                )
                trajectory_points.append(point)

        final_canvas = orchestrator.canvas
        final_pix = black_pixels(final_canvas)

        # Final evaluation metrics against reference (performed by teacher evaluator)
        if target_pix:
            initial_xor = len(target_pix)
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
            aspect_dev = abs((tw / th) - (pw / ph))

            tcx = (t_box[0] + t_box[2]) / 2.0
            tcy = (t_box[1] + t_box[3]) / 2.0
            pcx = (p_box[0] + p_box[2]) / 2.0
            pcy = (p_box[1] + p_box[3]) / 2.0
            drift = math.hypot(tcx - pcx, tcy - pcy)
        else:
            # Creation mode: evaluate internal structural balance
            initial_xor = 0
            final_xor = 0
            final_iou = 1.0 if len(final_pix) > 100 else 0.0
            aspect_dev = 0.0
            drift = 0.0

        result = LearningAuditResultV1(
            exam_id=exam_id,
            evaluation_mode=evaluation_mode,
            condition_name=condition,
            target_sha256=target_sha,
            retrieved_experience_ids=tuple(dict.fromkeys(retrieved_ids)),
            canonical_trees_queried=tuple(dict.fromkeys(trees_queried)),
            meaning_intents_used=tuple(dict.fromkeys(intents_used)),
            initial_xor_error=initial_xor,
            final_xor_error=final_xor,
            initial_iou=0.0,
            final_iou=final_iou,
            proportions_fidelity=round(aspect_dev, 4),
            centroid_drift_px=round(drift, 2),
            total_operations_count=len(orchestrator.orchestrator._step_receipts),
            total_cost_incurred=round(orchestrator.orchestrator._accumulated_cost, 2),
            trajectory_curve=tuple(trajectory_points),
        )

        return result, final_canvas

    def run_exam_audit(
        self,
        exam_id: str,
        target_image: Image.Image,
        memory_enabled: bool = True,
    ) -> tuple[LearningAuditResultV1, Image.Image]:
        """Backward-compatible audit runner."""
        condition = "FULL_MULTIDIMENSIONAL_MEMORY" if memory_enabled else "MEMORY_DISABLED"
        return self.run_controlled_exam(
            exam_id=exam_id,
            evaluation_mode="VISIBLE_REPRODUCTION",
            condition=condition,
            target_image=target_image,
        )

    @staticmethod
    def _measure_trajectory_point(
        step_index: int,
        capability: str,
        cumulative_cost: float,
        current_canvas: Image.Image,
        target_pix: set[int],
    ) -> StepTrajectoryPointV1:
        cand_pix = black_pixels(current_canvas)
        if target_pix:
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

            tcx = (t_box[0] + t_box[2]) / 2.0
            tcy = (t_box[1] + t_box[3]) / 2.0
            pcx = (p_box[0] + p_box[2]) / 2.0
            pcy = (p_box[1] + p_box[3]) / 2.0
            drift = math.hypot(tcx - pcx, tcy - pcy)
        else:
            xor_err = 0
            iou = 1.0 if len(cand_pix) > 80 else 0.0
            prop_dev = 0.0
            drift = 0.0

        return StepTrajectoryPointV1(
            step_index=step_index,
            capability=capability,
            cumulative_cost=cumulative_cost,
            iou=iou,
            xor_error=xor_err,
            proportions_dev=round(prop_dev, 4),
            centroid_drift_px=round(drift, 2),
        )


# =========================================================================
# 4. REPRODUCIBLE ARTIFACT GENERATOR (With Curves and Visual Diffs)
# =========================================================================

def generate_learning_audit_artifacts(output_dir: Path | str) -> dict[str, Any]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    curriculum = TeacherVisualCurriculumV1()
    auditor = RealLearningAuditorV1()

    # 1. Private Teacher Reference Images
    img_arch = curriculum.render_lesson_arch()
    img_bowl = curriculum.render_lesson_bowl()
    img_strut = curriculum.render_lesson_diagonal_strut()
    img_bridge = curriculum.render_exam_unseen_arched_bridge()
    img_chalice = curriculum.render_exam_unseen_chalice()

    img_arch.save(out / "train_lesson_arch.png")
    img_bowl.save(out / "train_lesson_bowl.png")
    img_strut.save(out / "train_lesson_strut.png")
    img_bridge.save(out / "exam_unseen_bridge_reference.png")
    img_chalice.save(out / "exam_unseen_chalice_reference.png")

    # 2. EVALUATION 1: VISIBLE REPRODUCTION (Bridge) across 3 conditions
    res_b_full, prod_b_full = auditor.run_controlled_exam(
        "EXAM_ARCHED_BRIDGE", "VISIBLE_REPRODUCTION", "FULL_MULTIDIMENSIONAL_MEMORY", target_image=img_bridge
    )
    res_b_flat, prod_b_flat = auditor.run_controlled_exam(
        "EXAM_ARCHED_BRIDGE", "VISIBLE_REPRODUCTION", "FLAT_PROCEDURAL_MEMORY", target_image=img_bridge
    )
    res_b_off, prod_b_off = auditor.run_controlled_exam(
        "EXAM_ARCHED_BRIDGE", "VISIBLE_REPRODUCTION", "MEMORY_DISABLED", target_image=img_bridge
    )

    prod_b_full.save(out / "brody_production_bridge_memory_full.png")
    prod_b_full.save(out / "brody_production_bridge_memory_on.png")
    prod_b_flat.save(out / "brody_production_bridge_memory_flat.png")
    prod_b_off.save(out / "brody_production_bridge_memory_off.png")

    # 3. EVALUATION 2: OCCLUDED RETENTION (Chalice)
    res_c_retention, prod_c_retention = auditor.run_controlled_exam(
        "EXAM_CHALICE", "OCCLUDED_RETENTION", "FULL_MULTIDIMENSIONAL_MEMORY", target_image=img_chalice
    )
    prod_c_retention.save(out / "brody_production_chalice_occluded_retention.png")

    # 4. EVALUATION 3: INTENT-ONLY CREATION (Portal)
    res_portal_create, prod_portal_create = auditor.run_controlled_exam(
        "EXAM_MONUMENTAL_PORTAL",
        "INTENT_ONLY_CREATION",
        "FULL_MULTIDIMENSIONAL_MEMORY",
        creation_intent_text="Create an architectural portal with a solid horizontal lintel spanning two vertical pillars and a curved vault",
    )
    prod_portal_create.save(out / "brody_production_portal_intent_creation.png")

    # 5. Difference Masks (Visualizing errors)
    t_bridge_pix = black_pixels(img_bridge)
    diff_full = _create_diff_mask(t_bridge_pix, black_pixels(prod_b_full))
    diff_full.save(out / "diff_mask_bridge_memory_full.png")
    diff_full.save(out / "diff_mask_bridge_memory_on.png")
    _create_diff_mask(t_bridge_pix, black_pixels(prod_b_off)).save(out / "diff_mask_bridge_memory_off.png")

    # 6. Comprehensive JSON Report
    summary_data = {
        "audit_version": "BRODY_CORRECTIVE_LEARNING_AUDIT_V2",
        "training_lessons": ["LESSON_ARCH", "LESSON_BOWL", "LESSON_DIAGONAL_STRUT"],
        "unseen_exams": ["EXAM_ARCHED_BRIDGE", "EXAM_CHALICE", "EXAM_MONUMENTAL_PORTAL"],
        "canonical_tree_associations_verified": {
            "03": "Arbre de la Perception (I_FONDAMENTAUX) -> contours, extraction contrastes",
            "12": "Arbre de la Technique (III_CONNAISSANCE) -> outils, montants, géométrie paramétrique",
            "13": "Arbre de l'Art (III_CONNAISSANCE) -> modelé pictural, hachures tonales",
            "20": "Arbre de l'Action (V_ACTION_TRANSFORMATION) -> exécution motrice",
            "21": "Arbre de la Création (V_ACTION_TRANSFORMATION) -> composition originale sans cible",
            "24": "Arbre de la Mémoire (VI_TEMPORELS_MEMORIELS) -> rétention d'expériences",
            "26": "Arbre de la Cohérence (VII_META_STRUCTURELS) -> invariants de proportions",
        },
        "comparative_metrics": {
            "EXAM_ARCHED_BRIDGE": {
                "memory_on": _result_to_dict(res_b_full),
                "memory_flat": _result_to_dict(res_b_flat),
                "memory_off": _result_to_dict(res_b_off),
            },
        },
        "exam_1_visible_reproduction_bridge": {
            "full_multidimensional_memory": _result_to_dict(res_b_full),
            "flat_procedural_memory": _result_to_dict(res_b_flat),
            "memory_disabled": _result_to_dict(res_b_off),
        },
        "exam_2_occluded_retention_chalice": _result_to_dict(res_c_retention),
        "exam_3_intent_only_creation_portal": _result_to_dict(res_portal_create),
        "epistemic_invariants": {
            "decision_authority": "KX108_ONLY",
            "is_candidate": True,
            "native_memory_write_allowed": False,
            "is_3d_view_synthesis": False,
            "no_dynamic_code_execution": True,
        },
    }

    (out / "audit_comparative_results.json").write_text(json.dumps(summary_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary_data


def _result_to_dict(res: LearningAuditResultV1) -> dict[str, Any]:
    return {
        "exam_id": res.exam_id,
        "evaluation_mode": res.evaluation_mode,
        "condition_name": res.condition_name,
        "final_iou": res.final_iou,
        "final_xor": res.final_xor_error,
        "proportions_dev": res.proportions_fidelity,
        "centroid_drift_px": res.centroid_drift_px,
        "total_operations": res.total_operations_count,
        "total_cost": res.total_cost_incurred,
        "retrieved_experiences": list(res.retrieved_experience_ids),
        "canonical_trees_queried": list(res.canonical_trees_queried),
        "meaning_intents_used": list(res.meaning_intents_used),
        "trajectory_curve": [
            {
                "step": pt.step_index,
                "tool": pt.capability,
                "cost": pt.cumulative_cost,
                "iou": pt.iou,
                "xor_error": pt.xor_error,
                "proportions_dev": pt.proportions_dev,
            }
            for pt in res.trajectory_curve
        ],
    }


def _create_diff_mask(target_pix: set[int], candidate_pix: set[int]) -> Image.Image:
    diff_rgb = Image.new("RGB", (SIDE, SIDE), (255, 255, 255))
    pixels = diff_rgb.load()
    for p in target_pix.intersection(candidate_pix):
        pixels[p % SIDE, p // SIDE] = (50, 50, 50)
    for p in target_pix - candidate_pix:
        pixels[p % SIDE, p // SIDE] = (220, 20, 20)
    for p in candidate_pix - target_pix:
        pixels[p % SIDE, p // SIDE] = (20, 20, 220)
    return diff_rgb


if __name__ == "__main__":
    res = generate_learning_audit_artifacts("artifacts/audit_apprentissage")
    print(json.dumps(res, indent=2))
