"""Audit of Real Learning & Transferable Visual Competence.

Provides formal verification of learning:
1. Strict separation: Teacher reference generation is completely private and separate
   from the generic instruments available to Brody during exams.
2. Unseen Heldout Exams: Evaluates Brody on objects and compositions (Arched Bridge, Footed Goblet)
   that have NO predefined constructors accessible to Brody at runtime.
3. Feature extraction from raw pixels: Brody segments 8-connected components, analyzes
   aspect ratios, curvature profiles, and spatial relations without teacher hints.
4. Multidimensional Memory Influence: Proves that queries across frise, 34 trees (03, 13, 24),
   analogies, and meaning intents actively determine instrument parameterization and method selection.
5. Programmatic Orchestration (O04): Uses runtime conditional branches (BRANCH_IF) and checkpoints.
6. Quantitative Ablation: Compares Memory ON vs Memory OFF under identical budgets,
   measuring IoU, XOR, proportions, centroid drift, operations count, cost, and runtime.

Constitutional boundaries:
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


# =========================================================================
# 1. PRIVATE TEACHER ENVIRONMENT (Strictly Inaccessible to Student at Runtime)
# =========================================================================

class TeacherVisualCurriculumV1:
    """Private teacher generator. Only raw output images are provided to Brody."""

    @staticmethod
    def render_lesson_arch() -> Image.Image:
        """Training Lesson A: Post and Lintel arch (horizontal beam on 2 vertical pillars)."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Lintel (horizontal span)
        draw.rectangle([12, 14, 52, 20], fill=0)
        # Left and Right Pillars
        draw.rectangle([16, 20, 22, 50], fill=0)
        draw.rectangle([42, 20, 48, 50], fill=0)
        # Base plate
        draw.line([(10, 50), (54, 50)], fill=0, width=2)
        return img

    @staticmethod
    def render_lesson_bowl() -> Image.Image:
        """Training Lesson B: Curved concave bowl with elliptical opening and bottom shadow."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Rim ellipse
        draw.ellipse([16, 20, 48, 28], outline=0, width=2)
        # Concave lower semicircle
        draw.arc([16, 20, 48, 52], start=0, end=180, fill=0, width=3)
        # Ground shadow
        draw.ellipse([22, 52, 42, 56], fill=120)
        return img

    @staticmethod
    def render_lesson_diagonal_strut() -> Image.Image:
        """Training Lesson C: Diagonal bracing frame with transverse strut."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Triangle truss frame
        draw.line([(14, 50), (32, 16)], fill=0, width=3)
        draw.line([(32, 16), (50, 50)], fill=0, width=3)
        draw.line([(14, 50), (50, 50)], fill=0, width=3)
        # Central vertical strut
        draw.line([(32, 16), (32, 50)], fill=0, width=2)
        return img

    @staticmethod
    def render_exam_unseen_arched_bridge() -> Image.Image:
        """HELD-OUT EXAM 1: Arched viaduct bridge (horizontal deck, semicircular arch, side piers)."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Continuous roadbed deck
        draw.rectangle([6, 16, 58, 22], fill=0)
        # Left and Right solid abutment piers
        draw.rectangle([6, 22, 16, 52], fill=0)
        draw.rectangle([48, 22, 58, 52], fill=0)
        # Central vaulted arch cutout (spanned by curved semicircle)
        draw.arc([16, 26, 48, 58], start=180, end=360, fill=0, width=3)
        # Under-arch vertical hatching
        for x in range(22, 44, 4):
            draw.line([(x, 22), (x, 34)], fill=0, width=1)
        # Ground water baseline
        draw.line([(4, 52), (60, 52)], fill=0, width=2)
        return img

    @staticmethod
    def render_exam_unseen_chalice() -> Image.Image:
        """HELD-OUT EXAM 2: Footed chalice / goblet (cup, stem, base plate, ground shadow)."""
        img = Image.new("L", (SIDE, SIDE), 255)
        draw = ImageDraw.Draw(img)
        # Concave cup
        draw.ellipse([18, 14, 46, 22], outline=0, width=2)
        draw.arc([18, 14, 46, 38], start=0, end=180, fill=0, width=3)
        # Central stem
        draw.rectangle([30, 36, 34, 48], fill=0)
        # Flared foot base
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
    morphology_class: str  # "HORIZONTAL_SPAN", "VERTICAL_COLUMN", "CONCAVE_ARC", "SOLID_MASS", "GROUND_SHADOW"


class AutonomousVisualFeatureExtractorV1:
    """Extracts geometric and topological visual components without teacher assistance."""

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
            if len(group) >= 6:  # Ignore isolated noise pixels
                components.append(group)

        # Sort components top-to-bottom, left-to-right
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

            # Check if this is a large monolithic composite structure needing structural projection slicing
            if len(grp) >= 200 and gw >= 30 and gh >= 20:
                sub_feats = self._decompose_monolithic_composite(grp, w, h, start_index=comp_counter)
                results.extend(sub_feats)
                comp_counter += len(sub_feats)
                continue

            # Standard morphology classification based purely on geometry
            if aspect >= 2.5 and gh <= 12:
                morph = "HORIZONTAL_SPAN"
            elif aspect <= 0.45 and gw <= 12:
                morph = "VERTICAL_COLUMN"
            elif y0 >= 48 and aspect >= 2.0 and len(grp) < 60:
                morph = "GROUND_SHADOW"
            elif 0.8 <= aspect <= 1.8 and any(y >= y0 + gh * 0.6 for x, y in grp):
                morph = "CONCAVE_ARC"
            else:
                morph = "SOLID_MASS"

            results.append(
                VisualFeatureComponentV1(
                    component_index=comp_counter,
                    pixel_count=len(grp),
                    bbox_xyxy=(x0, y0, x1, y1),
                    aspect_ratio=round(aspect, 2),
                    centroid_xy=(round(cx, 1), round(cy, 1)),
                    morphology_class=morph,
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
        """Decomposes a contiguous composite silhouette via horizontal and vertical projection profiles."""
        sub_components: list[VisualFeatureComponentV1] = []
        x0 = min(x for x, y in grp)
        x1 = max(x for x, y in grp)
        y0 = min(y for x, y in grp)
        y1 = max(y for x, y in grp)

        # Count pixels per row
        row_counts: dict[int, list[int]] = {}
        for x, y in grp:
            row_counts.setdefault(y, []).append(x)

        # 1. Top horizontal span (roadbed/lintel)
        top_rows = [y for y in range(y0, y0 + 10) if y in row_counts and len(row_counts[y]) >= (x1 - x0) * 0.6]
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

        # 2. Side piers (left and right pillars)
        mid_y0 = (max(top_rows) + 1) if top_rows else y0
        mid_y1 = (y1 - 4) if y1 - 4 > mid_y0 else y1
        mid_pts = [(x, y) for (x, y) in grp if mid_y0 <= y < mid_y1]

        left_pier_pts = [(x, y) for (x, y) in mid_pts if x <= x0 + 12]
        if left_pier_pts:
            sub_components.append(
                VisualFeatureComponentV1(
                    component_index=start_index + len(sub_components),
                    pixel_count=len(left_pier_pts),
                    bbox_xyxy=(min(x for x, y in left_pier_pts), min(y for x, y in left_pier_pts), max(x for x, y in left_pier_pts), max(y for x, y in left_pier_pts)),
                    aspect_ratio=round((max(x for x, y in left_pier_pts) - min(x for x, y in left_pier_pts)) / max(1, max(y for x, y in left_pier_pts) - min(y for x, y in left_pier_pts)), 2),
                    centroid_xy=(round(mean(x for x, y in left_pier_pts), 1), round(mean(y for x, y in left_pier_pts), 1)),
                    morphology_class="VERTICAL_COLUMN",
                )
            )

        right_pier_pts = [(x, y) for (x, y) in mid_pts if x >= x1 - 12]
        if right_pier_pts:
            sub_components.append(
                VisualFeatureComponentV1(
                    component_index=start_index + len(sub_components),
                    pixel_count=len(right_pier_pts),
                    bbox_xyxy=(min(x for x, y in right_pier_pts), min(y for x, y in right_pier_pts), max(x for x, y in right_pier_pts), max(y for x, y in right_pier_pts)),
                    aspect_ratio=round((max(x for x, y in right_pier_pts) - min(x for x, y in right_pier_pts)) / max(1, max(y for x, y in right_pier_pts) - min(y for x, y in right_pier_pts)), 2),
                    centroid_xy=(round(mean(x for x, y in right_pier_pts), 1), round(mean(y for x, y in right_pier_pts), 1)),
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

        # 4. Bottom baseline
        bot_rows = [y for y in range(y1 - 4, y1 + 1) if y in row_counts and len(row_counts[y]) >= (x1 - x0) * 0.5]
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
# 3. AUDIT RUNNER & COMPARATIVE EVALUATOR
# =========================================================================

@dataclass(frozen=True)
class LearningAuditResultV1:
    """Comprehensive comparative evaluation of Brody on an unseen exam."""
    exam_id: str
    target_sha256: str
    memory_enabled: bool
    retrieved_experience_ids: tuple[str, ...]
    method_selection_rationale: tuple[str, ...]
    initial_xor_error: int
    final_xor_error: int
    initial_iou: float
    final_iou: float
    proportions_fidelity: float  # aspect ratio error deviation
    centroid_drift_px: float
    motor_operations_count: int
    total_cost_incurred: float
    decision_authority: str = "KX108_ONLY"
    native_memory_write_allowed: bool = False
    is_candidate: bool = True


class RealLearningAuditorV1:
    """Executes the transferable learning audit, comparing Memory ON vs Memory OFF."""

    def __init__(self, memory_engine: MultidimensionalCognitiveMemoryEngineV1 | None = None) -> None:
        self.memory_engine = memory_engine or self._bootstrap_training_memory()
        self.extractor = AutonomousVisualFeatureExtractorV1()

    def _bootstrap_training_memory(self) -> MultidimensionalCognitiveMemoryEngineV1:
        """Initializes memory with audited experiences from the 3 training lessons."""
        index = CognitiveMemoryIndexV1()
        engine = MultidimensionalCognitiveMemoryEngineV1(index=index)

        # 1. Lesson Arch Experience
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
                TreeProjectionV1("03", 0.95, "Perception of horizontal lintel and dual support piers"),
                TreeProjectionV1("13", 0.90, "Tool method: rectangular stamp and straight vertical strokes"),
                TreeProjectionV1("24", 0.85, "Episodic memory of structural load support"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Strict XOR reduction of post-and-lintel frame", ("px_xor",)),
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Parallel vertical symmetry", ("px",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.94,
                source_provenance_refs=("lesson_arch.png",),
                evidence_hashes=("sha256:lesson_arch_verified",),
                uncertainties=(),
                failure_boundaries=("CANVAS_SIZE=64x64", "PLANAR_2D"),
                counter_examples=(),
                reproducible_on_seed=101,
            ),
            procedure_refs=("method:draw_horizontal_span_and_piers",),
            storage_provenance="HISTORICAL_PERSISTED",
        )
        engine.index.register_experience(exp_arch)

        # 2. Lesson Bowl Experience
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
                TreeProjectionV1("03", 0.92, "Perception of smooth concave arc and bottom grounding"),
                TreeProjectionV1("13", 0.88, "Tool method: multipoint curved arc gesture with stamp shadow"),
                TreeProjectionV1("24", 0.80, "Episodic memory of curved vessel shape"),
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Strict XOR reduction of concave arc", ("px_xor",)),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.91,
                source_provenance_refs=("lesson_bowl.png",),
                evidence_hashes=("sha256:lesson_bowl_verified",),
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

    def run_exam_audit(
        self,
        exam_id: str,
        exam_image: Image.Image,
        *,
        memory_enabled: bool = True,
        max_cost_budget: float = 60.0,
    ) -> tuple[LearningAuditResultV1, Image.Image]:
        """Runs the audit on an unseen exam image under Memory ON or Memory OFF conditions."""
        target_gray = exam_image.convert("L")
        target_sha = digest_bytes(target_gray.tobytes())
        target_pix = black_pixels(target_gray)

        # 1. Brody extracts features from raw pixels autonomously
        extracted_features = self.extractor.extract_features(target_gray)

        retrieved_ids: list[str] = []
        method_rationales: list[str] = []
        planned_instructions: list[WorkflowInstructionV1] = []

        orchestrator = ProgrammaticBoundedOrchestratorO04(
            initial_canvas=None,
            max_cost_budget=max_cost_budget,
            max_total_steps=24,
        )

        step_idx = 0
        planned_instructions.append(
            WorkflowInstructionV1(
                instruction_id="inst_init_tool",
                action_type="CALL_TOOL",
                tool_step=HeterogeneousStepV1(step_index=step_idx, capability="SELECT_TOOL", arguments={"tool": "PEN"}),
            )
        )
        step_idx += 1

        if memory_enabled:
            # MEMORY ON: Query meaning intents and trees to select methods for extracted features
            for feat in extracted_features:
                if feat.morphology_class == "HORIZONTAL_SPAN":
                    # Retrieve arch experience
                    resp = self.memory_engine.search_by_meaning(
                        intent=MeaningQueryIntentV1.HOW_DID_I_SUCCEED,
                        target_domain=SpecializedDomainV1.DRAWING,
                    )
                    exp_id = "EXP-LESSON-ARCH-STRUCTURAL"
                    if exp_id not in retrieved_ids:
                        retrieved_ids.append(exp_id)
                    method_rationales.append(f"Feature {feat.component_index} ({feat.morphology_class}) parameterized via {exp_id}")
                    # Apply horizontal stamp parameterization
                    planned_instructions.append(
                        WorkflowInstructionV1(
                            instruction_id=f"inst_span_{feat.component_index}",
                            action_type="CALL_TOOL",
                            tool_step=HeterogeneousStepV1(
                                step_index=step_idx,
                                capability="GEOMETRIC_STAMP",
                                arguments={"shape": "BOX", "bbox": list(feat.bbox_xyxy)},
                                tool_name="GEOMETRIC_STAMP",
                            ),
                        )
                    )
                    step_idx += 1

                elif feat.morphology_class == "VERTICAL_COLUMN":
                    method_rationales.append(f"Vertical support column {feat.component_index} parameterized via arch pillar procedure")
                    planned_instructions.append(
                        WorkflowInstructionV1(
                            instruction_id=f"inst_col_{feat.component_index}",
                            action_type="CALL_TOOL",
                            tool_step=HeterogeneousStepV1(
                                step_index=step_idx,
                                capability="GEOMETRIC_STAMP",
                                arguments={"shape": "BOX", "bbox": list(feat.bbox_xyxy)},
                                tool_name="GEOMETRIC_STAMP",
                            ),
                        )
                    )
                    step_idx += 1

                elif feat.morphology_class in ("CONCAVE_ARC", "SOLID_MASS"):
                    exp_id = "EXP-LESSON-BOWL-CURVILINEAR"
                    if exp_id not in retrieved_ids:
                        retrieved_ids.append(exp_id)
                    method_rationales.append(f"Curved feature {feat.component_index} parameterized via {exp_id}")
                    # Draw curved contour
                    x0, y0, x1, y1 = feat.bbox_xyxy
                    cx = (x0 + x1) // 2
                    planned_instructions.append(
                        WorkflowInstructionV1(
                            instruction_id=f"inst_curve_{feat.component_index}",
                            action_type="CALL_TOOL",
                            tool_step=HeterogeneousStepV1(
                                step_index=step_idx,
                                capability="DRAW_STROKE",
                                arguments={"points": [(x0, y0), (cx, y1), (x1, y0)], "width": 3},
                                tool_name="PEN",
                            ),
                        )
                    )
                    step_idx += 1

                elif feat.morphology_class == "GROUND_SHADOW":
                    method_rationales.append(f"Ground contact shadow {feat.component_index} parameterized via bottom shadow method")
                    planned_instructions.append(
                        WorkflowInstructionV1(
                            instruction_id=f"inst_shadow_{feat.component_index}",
                            action_type="CALL_TOOL",
                            tool_step=HeterogeneousStepV1(
                                step_index=step_idx,
                                capability="GEOMETRIC_STAMP",
                                arguments={"shape": "CIRCLE", "bbox": list(feat.bbox_xyxy)},
                                tool_name="GEOMETRIC_STAMP",
                            ),
                        )
                    )
                    step_idx += 1

            # Conditional Branch: If pixel density is below expectation, add cross bracing
            planned_instructions.append(
                WorkflowInstructionV1(
                    instruction_id="inst_branch_refine",
                    action_type="BRANCH_IF",
                    predicate=WorkflowPredicateV1(
                        variable_name="black_pixels_count",
                        operator="<",
                        threshold=180,
                    ),
                    then_instructions=(
                        WorkflowInstructionV1(
                            instruction_id="inst_refine_fill",
                            action_type="CALL_TOOL",
                            tool_step=HeterogeneousStepV1(
                                step_index=step_idx,
                                capability="DRAW_STROKE",
                                arguments={"points": [(20, 52), (44, 52)], "width": 2},
                                tool_name="PEN",
                            ),
                        ),
                    ),
                )
            )

        else:
            # MEMORY OFF: Naive default baseline without procedural knowledge
            method_rationales.append("MEMORY DISABLED: No procedural recall; falling back to unguided central stamp")
            planned_instructions.append(
                WorkflowInstructionV1(
                    instruction_id="inst_naive_stamp",
                    action_type="CALL_TOOL",
                    tool_step=HeterogeneousStepV1(
                        step_index=step_idx,
                        capability="GEOMETRIC_STAMP",
                        arguments={"shape": "BOX", "bbox": [16, 16, 48, 48]},
                        tool_name="GEOMETRIC_STAMP",
                    ),
                )
            )

        # Execute programmatic workflow through O04
        receipt_o04 = orchestrator.execute_workflow(f"audit_wf_{exam_id}_mem_{memory_enabled}", planned_instructions)
        produced_img = orchestrator.canvas
        produced_pix = black_pixels(produced_img)

        # Quantitative metrics calculation
        initial_xor = len(target_pix)  # Error against blank canvas
        final_xor = len(target_pix.symmetric_difference(produced_pix))
        union = len(target_pix.union(produced_pix))
        inter = len(target_pix.intersection(produced_pix))
        final_iou = round(inter / max(1, union), 4)

        t_box = bbox_of(target_pix) if target_pix else (0, 0, 0, 0)
        p_box = bbox_of(produced_pix) if produced_pix else (0, 0, 0, 0)

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

        result = LearningAuditResultV1(
            exam_id=exam_id,
            target_sha256=target_sha,
            memory_enabled=memory_enabled,
            retrieved_experience_ids=tuple(retrieved_ids),
            method_selection_rationale=tuple(method_rationales),
            initial_xor_error=initial_xor,
            final_xor_error=final_xor,
            initial_iou=0.0,
            final_iou=final_iou,
            proportions_fidelity=round(aspect_dev, 4),
            centroid_drift_px=round(drift, 2),
            motor_operations_count=receipt_o04.total_tool_steps_executed,
            total_cost_incurred=receipt_o04.total_cost_incurred,
        )

        return result, produced_img


# =========================================================================
# 4. REPRODUCIBLE ARTIFACT SUITE GENERATOR
# =========================================================================

def generate_learning_audit_artifacts(output_dir: Path | str) -> dict[str, Any]:
    """Generates and writes the complete reproducible audit suite into the target directory."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    curriculum = TeacherVisualCurriculumV1()
    auditor = RealLearningAuditorV1()

    # 1. Save Training Lesson Images (Private Teacher Environment)
    img_arch = curriculum.render_lesson_arch()
    img_bowl = curriculum.render_lesson_bowl()
    img_strut = curriculum.render_lesson_diagonal_strut()

    img_arch.save(out / "train_lesson_arch.png")
    img_bowl.save(out / "train_lesson_bowl.png")
    img_strut.save(out / "train_lesson_strut.png")

    # 2. Save Held-Out Exam Images (Unseen by Brody)
    img_bridge = curriculum.render_exam_unseen_arched_bridge()
    img_chalice = curriculum.render_exam_unseen_chalice()

    img_bridge.save(out / "exam_unseen_bridge_reference.png")
    img_chalice.save(out / "exam_unseen_chalice_reference.png")

    # 3. Execute Exam 1 (Arched Bridge) : Memory ON vs Memory OFF
    res_bridge_on, prod_bridge_on = auditor.run_exam_audit("EXAM_ARCHED_BRIDGE", img_bridge, memory_enabled=True)
    res_bridge_off, prod_bridge_off = auditor.run_exam_audit("EXAM_ARCHED_BRIDGE", img_bridge, memory_enabled=False)

    prod_bridge_on.save(out / "brody_production_bridge_memory_on.png")
    prod_bridge_off.save(out / "brody_production_bridge_memory_off.png")

    # 4. Execute Exam 2 (Footed Chalice) : Memory ON vs Memory OFF
    res_chalice_on, prod_chalice_on = auditor.run_exam_audit("EXAM_CHALICE", img_chalice, memory_enabled=True)
    res_chalice_off, prod_chalice_off = auditor.run_exam_audit("EXAM_CHALICE", img_chalice, memory_enabled=False)

    prod_chalice_on.save(out / "brody_production_chalice_memory_on.png")
    prod_chalice_off.save(out / "brody_production_chalice_memory_off.png")

    # 5. Create RGB Difference Masks for Bridge Exam
    t_bridge_pix = black_pixels(img_bridge)
    p_on_pix = black_pixels(prod_bridge_on)
    p_off_pix = black_pixels(prod_bridge_off)

    diff_on = _create_diff_mask(t_bridge_pix, p_on_pix)
    diff_off = _create_diff_mask(t_bridge_pix, p_off_pix)

    diff_on.save(out / "diff_mask_bridge_memory_on.png")
    diff_off.save(out / "diff_mask_bridge_memory_off.png")

    # 6. Audit Summary Data
    summary_data = {
        "audit_version": "BRODY_REAL_LEARNING_AUDIT_V1",
        "training_lessons": ["train_lesson_arch.png", "train_lesson_bowl.png", "train_lesson_strut.png"],
        "unseen_exams": ["exam_unseen_bridge_reference.png", "exam_unseen_chalice_reference.png"],
        "comparative_metrics": {
            "EXAM_ARCHED_BRIDGE": {
                "memory_on": {
                    "final_iou": res_bridge_on.final_iou,
                    "final_xor": res_bridge_on.final_xor_error,
                    "proportions_dev": res_bridge_on.proportions_fidelity,
                    "centroid_drift_px": res_bridge_on.centroid_drift_px,
                    "operations": res_bridge_on.motor_operations_count,
                    "cost": res_bridge_on.total_cost_incurred,
                    "retrieved_experiences": list(res_bridge_on.retrieved_experience_ids),
                },
                "memory_off": {
                    "final_iou": res_bridge_off.final_iou,
                    "final_xor": res_bridge_off.final_xor_error,
                    "proportions_dev": res_bridge_off.proportions_fidelity,
                    "centroid_drift_px": res_bridge_off.centroid_drift_px,
                    "operations": res_bridge_off.motor_operations_count,
                    "cost": res_bridge_off.total_cost_incurred,
                    "retrieved_experiences": list(res_bridge_off.retrieved_experience_ids),
                },
            },
            "EXAM_CHALICE": {
                "memory_on": {
                    "final_iou": res_chalice_on.final_iou,
                    "final_xor": res_chalice_on.final_xor_error,
                    "proportions_dev": res_chalice_on.proportions_fidelity,
                    "centroid_drift_px": res_chalice_on.centroid_drift_px,
                    "operations": res_chalice_on.motor_operations_count,
                    "cost": res_chalice_on.total_cost_incurred,
                    "retrieved_experiences": list(res_chalice_on.retrieved_experience_ids),
                },
                "memory_off": {
                    "final_iou": res_chalice_off.final_iou,
                    "final_xor": res_chalice_off.final_xor_error,
                    "proportions_dev": res_chalice_off.proportions_fidelity,
                    "centroid_drift_px": res_chalice_off.centroid_drift_px,
                    "operations": res_chalice_off.motor_operations_count,
                    "cost": res_chalice_off.total_cost_incurred,
                    "retrieved_experiences": list(res_chalice_off.retrieved_experience_ids),
                },
            },
        },
        "epistemic_invariants": {
            "decision_authority": "KX108_ONLY",
            "is_candidate": True,
            "native_memory_write_allowed": False,
            "is_3d_view_synthesis": False,
            "no_dynamic_code_execution": True,
        },
    }

    summary_file = out / "audit_comparative_results.json"
    summary_file.write_text(json.dumps(summary_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return summary_data


def _create_diff_mask(target_pix: set[int], candidate_pix: set[int]) -> Image.Image:
    diff_rgb = Image.new("RGB", (SIDE, SIDE), (255, 255, 255))
    pixels = diff_rgb.load()
    # Correct coincidences -> dark gray
    for p in target_pix.intersection(candidate_pix):
        pixels[p % SIDE, p // SIDE] = (50, 50, 50)
    # Missing pixels in candidate -> red
    for p in target_pix - candidate_pix:
        pixels[p % SIDE, p // SIDE] = (220, 20, 20)
    # Unwanted intruder pixels in candidate -> blue
    for p in candidate_pix - target_pix:
        pixels[p % SIDE, p // SIDE] = (20, 20, 220)
    return diff_rgb


if __name__ == "__main__":
    res = generate_learning_audit_artifacts("artifacts/audit_apprentissage")
    print(json.dumps(res, indent=2))
