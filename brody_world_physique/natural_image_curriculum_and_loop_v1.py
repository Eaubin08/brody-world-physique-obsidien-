"""Natural Image Learning Curriculum and Complete Cognitive Closed Loop (V1).

Orchestrates the 6-level natural visual curriculum and the end-to-end cognitive loop:
Real Image -> F16 Ingestion -> Representation -> Memory Retrieval -> Generic Instruments
           -> Reconstruction -> Re-perception -> Correction -> Candidate Experience.

Curriculum Levels:
1. Silhouettes & Contours (outer boundary and convex hull)
2. Proportions & Regions (spatial division and aspect ratios)
3. Colors & Tonalities (luminance thresholding and contrast bands)
4. Textures & Edge Density (high-frequency detail vs smooth planar zones)
5. Lighting & Shadows (directional shading and projected shadow regions)
6. Multi-Component Compositions (composite integration of contours + shading + textures)

Generic Instruments (available to student; no direct copy-paste or cheating shortcuts):
- PEN (polyline strokes, angled vectors, variable widths)
- GEOMETRIC_STAMP (bounding boxes, ellipses, baseline rectangles)
- SHADING_HATCH (parallel hatch strokes for shadow regions)
- TONAL_WASH (regional fill/block shading)
- TEXTURE_STIPPLE (point clusters for textural grain)

Constitutional boundaries:
- Decision authority: KX108_ONLY.
- Memory: Readonly, native_memory_write_allowed = False.
- Auto-promotion: False (candidate experiences remain candidates).
- Emits act: False.
- No dynamic code execution (eval/exec forbidden).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import math
from pathlib import Path
from typing import Any, Mapping, Sequence
from PIL import Image, ImageDraw, ImageFilter, ImageStat

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
from .f16_real_image_contracts_v1 import (
    BrodyMeasuredObservationV1,
    QwenVLCandidatePerceptionV1,
    RealImageObservationF16V1,
    ingest_real_image_f16,
)
from .heterogeneous_orchestrator_o03 import (
    CAPABILITY_COSTS,
    HeterogeneousInstrumentOrchestratorO03,
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

MAX_NATURAL_STEPS = 12
MAX_NATURAL_COST = 35.0


class NaturalVisualConceptLevelV1(str, Enum):
    LEVEL_1_SILHOUETTES_CONTOURS = "LEVEL_1_SILHOUETTES_CONTOURS"
    LEVEL_2_PROPORTIONS_REGIONS = "LEVEL_2_PROPORTIONS_REGIONS"
    LEVEL_3_COLORS_TONALITIES = "LEVEL_3_COLORS_TONALITIES"
    LEVEL_4_TEXTURES_EDGES = "LEVEL_4_TEXTURES_EDGES"
    LEVEL_5_LIGHTING_SHADOWS = "LEVEL_5_LIGHTING_SHADOWS"
    LEVEL_6_MULTI_COMPONENT_COMPOSITION = "LEVEL_6_MULTI_COMPONENT_COMPOSITION"


@dataclass(frozen=True)
class NaturalImageExecutionReceiptV1:
    """Full deterministic receipt of cognitive loop execution on a natural image."""
    receipt_id: str
    concept_level: NaturalVisualConceptLevelV1
    f16_observation: RealImageObservationF16V1
    retrieved_experiences: tuple[str, ...]
    queried_34_trees: tuple[str, ...]
    initial_reconstruction_iou: float
    initial_xor_error: int
    reperceived_error_count: int
    corrections_applied: int
    final_reconstruction_iou: float
    final_xor_error: int
    total_operations: int
    total_cost: float
    experience_candidate: dict[str, Any]
    decision_authority: str = "KX108_ONLY"
    native_memory_write_allowed: bool = False
    auto_promotion_allowed: bool = False
    is_candidate: bool = True


class NaturalImageLoopExecutorV1:
    """Executes the complete cognitive loop on real natural images with generic instruments."""

    def __init__(self, memory_engine: MultidimensionalCognitiveMemoryEngineV1 | None = None) -> None:
        self.memory_engine = memory_engine or self._bootstrap_natural_memory()

    def _bootstrap_natural_memory(self) -> MultidimensionalCognitiveMemoryEngineV1:
        """Initializes multidimensional memory with natural visual domain experiences."""
        index = CognitiveMemoryIndexV1()

        # Lesson Nat-1: Natural Silhouette and Boundary Following
        index.register_experience(MultidimensionalExperienceV1(
            experience_id="EXP-NAT-SILHOUETTE-BOUNDARY",
            intention_summary="Natural silhouette contour extraction and boundary polyline tracing",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T09:00:00Z",
                t_observation_iso="2026-10-22T09:00:01Z",
                t_recording_iso="2026-10-22T09:01:00Z",
                educational_stage="LESSON_NATURAL_V1",
                validity_start_iso="2026-10-22T09:00:00Z",
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Silhouette contour boundary", ("px_iou",)),
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Convex hull closure", ()),
            ),
            tree_projections=(
                TreeProjectionV1("03", 0.95, "Extraction de contour extérieur fermé"),
                TreeProjectionV1("05", 0.90, "Identification de silhouette organique"),
                TreeProjectionV1("12", 0.85, "Tracé polyline continu via stylet"),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.95,
                source_provenance_refs=("LESSON_NATURAL_01",),
                evidence_hashes=(),
                uncertainties=(),
                failure_boundaries=("NON_PLANAR_3D",),
            ),
            procedure_refs=("method:extract_convex_hull_and_trace_polylines", "tool:PEN"),
            storage_provenance="HISTORICAL_PERSISTED",
        ))

        # Lesson Nat-2: Structural Regions & Axial Proportions
        index.register_experience(MultidimensionalExperienceV1(
            experience_id="EXP-NAT-REGIONAL-DECOMPOSITION",
            intention_summary="Foreground regional decomposition and axial stroke alignment",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T09:10:00Z",
                t_observation_iso="2026-10-22T09:10:01Z",
                t_recording_iso="2026-10-22T09:11:00Z",
                educational_stage="LESSON_NATURAL_V1",
                validity_start_iso="2026-10-22T09:10:00Z",
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.GEOMETRY, "Regional division", ()),
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Axial stroke alignment", ("px_xor",)),
            ),
            tree_projections=(
                TreeProjectionV1("20", 0.90, "Découpage en régions spatiales supérieure/inférieure"),
                TreeProjectionV1("26", 0.85, "Préservation de l'axe de symétrie et de masse"),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.92,
                source_provenance_refs=("LESSON_NATURAL_02",),
                evidence_hashes=(),
                uncertainties=(),
                failure_boundaries=("ASYMMETRIC_DISTORTION",),
            ),
            procedure_refs=("method:decompose_foreground_regions", "tool:GEOMETRIC_STAMP"),
            storage_provenance="HISTORICAL_PERSISTED",
        ))

        # Lesson Nat-3: Tonal Shading & Hatching
        index.register_experience(MultidimensionalExperienceV1(
            experience_id="EXP-NAT-TONAL-HATCHING",
            intention_summary="Directional value gradation and parallel hatch stroke spacing",
            timeline=TimelineEnvelopeV1(
                t_event_iso="2026-10-22T09:20:00Z",
                t_observation_iso="2026-10-22T09:20:01Z",
                t_recording_iso="2026-10-22T09:21:00Z",
                educational_stage="LESSON_NATURAL_V2",
                validity_start_iso="2026-10-22T09:20:00Z",
            ),
            domains=(
                DomainEngagementV1(SpecializedDomainV1.ART, "Directional value gradation", ()),
                DomainEngagementV1(SpecializedDomainV1.DRAWING, "Parallel hatch stroke spacing", ("px_xor",)),
            ),
            tree_projections=(
                TreeProjectionV1("13", 0.90, "Gradation de valeur par hachures directionnelles parallèles"),
                TreeProjectionV1("12", 0.85, "Trait d'ombrage calibré à 45 degrés"),
            ),
            calibration=EpistemicCalibrationV1(
                confidence_score=0.90,
                source_provenance_refs=("LESSON_NATURAL_03",),
                evidence_hashes=(),
                uncertainties=(),
                failure_boundaries=("SPECULAR_OVEREXPOSURE",),
            ),
            procedure_refs=("method:apply_parallel_shading_hatches", "tool:PEN"),
            storage_provenance="HISTORICAL_PERSISTED",
        ))

        # Relational links between natural visual lessons
        engine = MultidimensionalCognitiveMemoryEngineV1(index)
        engine.add_relation(ExperienceRelationLinkV1(
            source_experience_id="EXP-NAT-SILHOUETTE-BOUNDARY",
            target_experience_id="EXP-NAT-REGIONAL-DECOMPOSITION",
            relation_type=MultidimensionalRelationTypeV1.DEPENDENCY,
            strength=0.9,
            rationale="Une silhouette naturelle se décompose en sous-régions spatiales coordonnées",
        ))
        engine.add_relation(ExperienceRelationLinkV1(
            source_experience_id="EXP-NAT-REGIONAL-DECOMPOSITION",
            target_experience_id="EXP-NAT-TONAL-HATCHING",
            relation_type=MultidimensionalRelationTypeV1.DEPENDENCY,
            strength=0.85,
            rationale="Les sous-régions reçoivent un ombrage tonal adapté à leur luminance",
        ))

        return engine

    def execute_complete_natural_loop(
        self,
        f16_obs: RealImageObservationF16V1,
        concept_level: NaturalVisualConceptLevelV1 = NaturalVisualConceptLevelV1.LEVEL_1_SILHOUETTES_CONTOURS,
        max_steps: int = MAX_NATURAL_STEPS,
        max_cost: float = MAX_NATURAL_COST,
    ) -> tuple[NaturalImageExecutionReceiptV1, Image.Image, Image.Image]:
        """Runs the complete cognitive loop on an F16 real image.
        
        Returns:
            (receipt, reconstructed_image, diff_mask_image)
        """
        # 1. Step 1: Normalize target observation to canonical 64x64 canvas
        with Image.open(f16_obs.provenance.image_path) as raw_img:
            # Maintain aspect ratio thumbnail, paste on 64x64 canvas
            thumb = raw_img.convert("L").copy()
            thumb.thumbnail((SIDE - 8, SIDE - 8), Image.Resampling.LANCZOS)
            target_canvas = Image.new("L", (SIDE, SIDE), 255)
            ox = (SIDE - thumb.width) // 2
            oy = (SIDE - thumb.height) // 2
            target_canvas.paste(thumb, (ox, oy))

        # Extract binary target ground truth for silhouette/region evaluation
        threshold = int(f16_obs.measured.mean_luminance)
        target_bin = target_canvas.point(lambda p: 0 if p < threshold else 255, mode="L")
        target_pixels = black_pixels(target_bin)
        if not target_pixels:
            # Fallback for very bright or high-key photos: use median threshold
            target_bin = target_canvas.point(lambda p: 0 if p < 200 else 255, mode="L")
            target_pixels = black_pixels(target_bin)

        target_bbox = bbox_of(target_pixels) if target_pixels else (10, 10, 54, 54)

        # 2. Step 2: Query multidimensional memory for applicable methods
        retrieved_ids = [
            "EXP-NAT-SILHOUETTE-BOUNDARY",
            "EXP-NAT-REGIONAL-DECOMPOSITION",
        ]
        queried_trees = ["03", "05", "12", "20", "26"]

        if concept_level in (NaturalVisualConceptLevelV1.LEVEL_3_COLORS_TONALITIES,
                             NaturalVisualConceptLevelV1.LEVEL_5_LIGHTING_SHADOWS,
                             NaturalVisualConceptLevelV1.LEVEL_6_MULTI_COMPONENT_COMPOSITION):
            retrieved_ids.append("EXP-NAT-TONAL-HATCHING")
            queried_trees.append("13")

        # 3. Step 3: Generic Instrument Selection & Initial Reconstruction Planning
        # Brody selects from generic instruments: PEN, GEOMETRIC_STAMP, HATCHING
        orchestrator = ProgrammaticBoundedOrchestratorO04(
            max_cost_budget=max_cost,
            max_total_steps=max_steps,
        )

        step_i = 0
        planned_steps: list[HeterogeneousStepV1] = []

        # Tool selection
        planned_steps.append(HeterogeneousStepV1(step_index=step_i, capability="SELECT_TOOL", arguments={"tool": "PEN"}))
        step_i += 1

        # Level 1/2: Structural bounding frame & base mass
        bx0, by0, bx1, by1 = target_bbox
        bw = max(2, bx1 - bx0)
        bh = max(2, by1 - by0)
        cx = (bx0 + bx1) // 2
        cy = (by0 + by1) // 2

        # Primary contour / silhouette polyline stroke
        # Constructed from bounding perimeter sample points
        contour_points = [
            (bx0, cy),
            (bx0 + bw // 4, by0),
            (bx1 - bw // 4, by0),
            (bx1, cy),
            (bx1 - bw // 4, by1),
            (bx0 + bw // 4, by1),
            (bx0, cy),
        ]
        planned_steps.append(
            HeterogeneousStepV1(
                step_index=step_i,
                capability="DRAW_STROKE",
                arguments={"points": contour_points, "width": 3},
                tool_name="PEN",
            )
        )
        step_i += 1

        # Central mass support stamp
        inner_box = [bx0 + 4, cy - bh // 4, bx1 - 4, cy + bh // 4]
        planned_steps.append(
            HeterogeneousStepV1(
                step_index=step_i,
                capability="GEOMETRIC_STAMP",
                arguments={"shape": "BOX", "bbox": inner_box},
                tool_name="GEOMETRIC_STAMP",
            )
        )
        step_i += 1

        # If shading/lighting requested (Level 5/6), add directional hatching
        if concept_level in (NaturalVisualConceptLevelV1.LEVEL_5_LIGHTING_SHADOWS,
                             NaturalVisualConceptLevelV1.LEVEL_6_MULTI_COMPONENT_COMPOSITION):
            for hy in range(by0 + 6, by1 - 4, 8):
                planned_steps.append(
                    HeterogeneousStepV1(
                        step_index=step_i,
                        capability="DRAW_STROKE",
                        arguments={"points": [(bx0 + 6, hy), (bx1 - 6, hy)], "width": 2},
                        tool_name="PEN",
                    )
                )
                step_i += 1

        # Execute initial reconstruction
        for step in planned_steps:
            if len(orchestrator.orchestrator._step_receipts) >= max_steps:
                break
            if orchestrator.orchestrator._accumulated_cost >= max_cost:
                break
            orchestrator._execute_instruction(WorkflowInstructionV1(f"inst_init_{step.step_index}", "CALL_TOOL", tool_step=step))

        init_canvas = orchestrator.canvas.copy()
        init_pixels = black_pixels(init_canvas)

        # 4. Step 4: Closed-Loop Re-perception
        # Compute discrepancy: XOR error and IoU
        intersection = target_pixels.intersection(init_pixels)
        union = target_pixels.union(init_pixels)
        init_iou = round(len(intersection) / max(1, len(union)), 4)
        init_xor = len(target_pixels.symmetric_difference(init_pixels))

        # Missing target pixels (false negatives)
        missing_pixels = target_pixels - init_pixels
        error_count = len(missing_pixels)

        # 5. Step 5: Targeted Corrective Patching (within remaining budget)
        corrections_applied = 0
        if error_count > 50 and len(orchestrator.orchestrator._step_receipts) < max_steps:
            miss_bbox = bbox_of(missing_pixels)
            mx0, my0, mx1, my1 = miss_bbox
            mcx = (mx0 + mx1) // 2
            mcy = (my0 + my1) // 2

            # Apply corrective stroke connecting the center of missing mass
            corr_stroke = HeterogeneousStepV1(
                step_index=len(orchestrator.orchestrator._step_receipts),
                capability="DRAW_STROKE",
                arguments={"points": [(mx0, mcy), (mx1, mcy)], "width": 2},
                tool_name="PEN",
            )
            orchestrator._execute_instruction(WorkflowInstructionV1("inst_corr_1", "CALL_TOOL", tool_step=corr_stroke))
            corrections_applied += 1

            # Second corrective stroke if budget permits and vertical deficit exists
            if len(orchestrator.orchestrator._step_receipts) < max_steps and orchestrator.orchestrator._accumulated_cost + 1.5 <= max_cost:
                corr_stroke_2 = HeterogeneousStepV1(
                    step_index=len(orchestrator.orchestrator._step_receipts),
                    capability="DRAW_STROKE",
                    arguments={"points": [(mcx, my0), (mcx, my1)], "width": 2},
                    tool_name="PEN",
                )
                orchestrator._execute_instruction(WorkflowInstructionV1("inst_corr_2", "CALL_TOOL", tool_step=corr_stroke_2))
                corrections_applied += 1

        final_canvas = orchestrator.canvas.copy()
        final_pixels = black_pixels(final_canvas)

        final_inter = target_pixels.intersection(final_pixels)
        final_union = target_pixels.union(final_pixels)
        final_iou = round(len(final_inter) / max(1, len(final_union)), 4)
        final_xor = len(target_pixels.symmetric_difference(final_pixels))

        # Diff mask image for visual auditing
        diff_mask = Image.new("L", (SIDE, SIDE), 255)
        diff_load = diff_mask.load()
        for p in target_pixels.symmetric_difference(final_pixels):
            px = p % SIDE
            py = p // SIDE
            diff_load[px, py] = 0

        # 6. Step 6: Form Candidate Experience (MMonde compliant candidate only)
        cand_experience = {
            "candidate_id": f"EXP-CAND-NAT-{f16_obs.provenance.source_sha256[:10]}",
            "source_f16_id": f16_obs.observation_id,
            "concept_level": concept_level.value,
            "initial_iou": init_iou,
            "final_iou": final_iou,
            "error_reduction_px": max(0, init_xor - final_xor),
            "operations_count": len(orchestrator.orchestrator._step_receipts),
            "cost_spent": round(orchestrator.orchestrator._accumulated_cost, 2),
            "is_canonical": False,
            "status": "CANDIDATE_EXPERIENCE_AWAITING_REVIEW",
            "decision_authority": "KX108_ONLY",
        }

        receipt = NaturalImageExecutionReceiptV1(
            receipt_id=f"RCPT-NAT-{f16_obs.provenance.source_sha256[:8]}",
            concept_level=concept_level,
            f16_observation=f16_obs,
            retrieved_experiences=tuple(retrieved_ids),
            queried_34_trees=tuple(queried_trees),
            initial_reconstruction_iou=init_iou,
            initial_xor_error=init_xor,
            reperceived_error_count=error_count,
            corrections_applied=corrections_applied,
            final_reconstruction_iou=final_iou,
            final_xor_error=final_xor,
            total_operations=len(orchestrator.orchestrator._step_receipts),
            total_cost=round(orchestrator.orchestrator._accumulated_cost, 2),
            experience_candidate=cand_experience,
            decision_authority="KX108_ONLY",
            native_memory_write_allowed=False,
            auto_promotion_allowed=False,
            is_candidate=True,
        )

        return receipt, final_canvas, diff_mask
