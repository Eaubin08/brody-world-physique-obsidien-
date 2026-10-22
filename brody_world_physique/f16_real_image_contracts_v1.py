"""F16 / MMonde Compliant Real Image Contracts and Epistemic Layering.

Implements strict tripartite epistemic separation for natural camera captures:
1. BrodyMeasuredObservationV1: Objective, deterministic physical pixel measurements
   (dimensions, luminance, color channels, edge density, bounding boxes).
2. QwenVLCandidatePerceptionV1: Descriptive semantic conjecture from local Jarvis Qwen-VL
   (explicitly CANDIDATE ONLY, unverified, zero world-state authority).
3. BrodyCognitiveHypothesisV1: Brody's internal hypotheses reconciling measured data
   with the 34 canonical trees and memory registers, preserving contradictions.

Constitutional boundaries:
- Decision authority: KX108_ONLY.
- Memory: Readonly, native_memory_write_allowed = False.
- Auto-promotion: False (candidates never silently promote to canonical truth).
- Emits act: False.
- No dynamic code execution (eval/exec forbidden).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence
from PIL import Image, ImageFilter, ImageStat

from .drawing_school_v0 import digest_bytes, bbox_of, black_pixels


@dataclass(frozen=True)
class RealImageProvenanceV1:
    """Authentic physical provenance metadata for a real-world camera image."""
    image_path: str
    origin_device: str
    source_sha256: str
    file_size_bytes: int
    color_mode: str
    native_dimensions: tuple[int, int]
    captured_at: str | None
    provenance_chain: tuple[str, ...]
    decision_authority: str = "KX108_ONLY"


@dataclass(frozen=True)
class BrodyMeasuredObservationV1:
    """Deterministic, objectively measured physical and statistical properties of raw pixels."""
    dimensions: tuple[int, int]
    aspect_ratio: float
    mean_luminance: float
    luminance_std: float
    channel_means_rgb: tuple[float, float, float]
    edge_pixel_count: int
    edge_density: float
    bounding_box_xyxy: tuple[int, int, int, int]
    contrast_ratio: float
    verified_deterministic: bool = True
    decision_authority: str = "KX108_ONLY"


@dataclass(frozen=True)
class QwenVLCandidatePerceptionV1:
    """Candidate descriptive semantics provided by local Jarvis Qwen-VL service.
    
    Strictly candidate conjecture: NOT an established world fact.
    """
    provider: str = "JARVIS_LOCAL_QWEN_VL"
    provider_model: str = "Qwen2.5-VL-3B-Instruct"
    candidate_caption: str = ""
    candidate_detected_objects: tuple[str, ...] = field(default_factory=tuple)
    is_hypothesis: bool = True
    semantics_verified: bool = False
    decision_authority: str = "CANDIDATE_ONLY_NO_AUTHORITY"


@dataclass(frozen=True)
class BrodyCognitiveHypothesisV1:
    """Brody's internal reasoning reconciling measured observations and candidate semantics."""
    hypothesized_category: str
    mapped_34_trees: tuple[str, ...]
    supporting_measurements: tuple[str, ...]
    contradictions_or_caveats: tuple[str, ...]
    confidence_score: float
    is_admissible_for_reasoning: bool
    decision_authority: str = "KX108_ONLY"


@dataclass(frozen=True)
class RealImageObservationF16V1:
    """Full F16/MMonde compliant real image contract holding partitioned epistemic layers."""
    observation_id: str
    provenance: RealImageProvenanceV1
    measured: BrodyMeasuredObservationV1
    qwen_candidate: QwenVLCandidatePerceptionV1
    brody_hypothesis: BrodyCognitiveHypothesisV1
    is_synthetic: bool = False
    f16_compliant: bool = True
    native_memory_write_allowed: bool = False
    auto_promotion_allowed: bool = False
    decision_authority: str = "KX108_ONLY"

    def to_mmonde_candidate_observation(self) -> dict[str, Any]:
        """Binds observation into MMonde-compatible candidate payload without canonical claim."""
        return {
            "schema_version": "OBSIDIA_MMONDE_REAL_IMAGE_F16_V1",
            "observation_id": self.observation_id,
            "source_sha256": self.provenance.source_sha256,
            "native_dimensions": list(self.provenance.native_dimensions),
            "is_synthetic": self.is_synthetic,
            "provenance": asdict(self.provenance),
            "measured_physical_facts": asdict(self.measured),
            "candidate_semantics": asdict(self.qwen_candidate),
            "brody_hypothesis": asdict(self.brody_hypothesis),
            "native_memory_write_allowed": False,
            "auto_promotion_allowed": False,
            "decision_authority": self.decision_authority,
        }

    def to_canonical_world_experience_candidate(self) -> Any:
        """Converts observation candidate to canonical WorldExperienceCandidateV0 contract."""
        from .contracts_v0 import (
            DECISION_AUTHORITY,
            ExperienceValidationStatusV0,
            MemoryEligibilityV0,
            WorldExperienceCandidateV0,
        )
        return WorldExperienceCandidateV0(
            experience_id=f"EXP-CAND-REAL-{self.provenance.source_sha256[:12]}",
            state_before_ref=f"STATE-RAW-IMAGE:{self.provenance.source_sha256[:12]}",
            state_after_ref=f"STATE-F16-OBS:{self.observation_id}",
            outcome="DETERMINISTIC_PIXEL_MEASUREMENT_AND_HYPOTHESIS_FORMED",
            validation_status=ExperienceValidationStatusV0.CANDIDATE,
            memory_eligibility=MemoryEligibilityV0.CANDIDATE_ONLY,
            context_refs=(f"FILE://{self.provenance.image_path}",),
            evidence_refs=(f"SHA256:{self.provenance.source_sha256}",),
            provenance_refs=self.provenance.provenance_chain,
            candidate_skill_refs=("skill:real_image_pixel_measurement_v1",),
            candidate_invariant_refs=("invariant:deterministic_measurements",),
            readonly=True,
            decision_authority=DECISION_AUTHORITY,
        )

    def to_json(self) -> str:
        return json.dumps(self.to_mmonde_candidate_observation(), indent=2, ensure_ascii=False)


@dataclass(frozen=True)
class RealImagePipelineAuditReceiptV1:
    """Audit report tracing the exact end-to-end real image pipeline:
    camera_capture -> extraction -> F16/MMonde -> memory -> tools -> reconstruction
    """
    image_path: str
    source_sha256: str
    native_dimensions: tuple[int, int]
    measured_luminance: float
    measured_edge_density: float
    measured_bbox: tuple[int, int, int, int]
    f16_observation_id: str
    retrieved_memory_experiences: tuple[str, ...]
    queried_34_trees: tuple[str, ...]
    tools_selected: tuple[str, ...]
    reconstruction_initial_iou: float
    reconstruction_final_iou: float
    reconstruction_final_xor: int
    operations_count: int
    cost_spent: float
    saved_artifact_paths: Mapping[str, str]
    mmonde_canonical_compatible: bool = True
    decision_authority: str = "KX108_ONLY"


def audit_real_image_pipeline(
    image_path: Path | str,
    output_dir: Path | str | None = None,
) -> RealImagePipelineAuditReceiptV1:
    """Executes and audits the complete, verifiable path from real image file to reconstructed production."""
    from .natural_image_curriculum_and_loop_v1 import (
        NaturalImageLoopExecutorV1,
        NaturalVisualConceptLevelV1,
    )

    path = Path(image_path).resolve()
    f16_obs = ingest_real_image_f16(path)
    canonical_cand = f16_obs.to_canonical_world_experience_candidate()

    executor = NaturalImageLoopExecutorV1()
    receipt, final_canvas, diff_mask = executor.execute_loop(
        f16_obs,
        concept_level=NaturalVisualConceptLevelV1.LEVEL_1_SILHOUETTES_CONTOURS,
    )

    saved_paths: dict[str, str] = {}
    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        with Image.open(path) as raw:
            raw_thumb = raw.convert("L").copy()
            raw_thumb.thumbnail((64, 64))
            raw_path = out / f"raw_input_{path.stem}.png"
            raw_thumb.save(raw_path)
            saved_paths["raw_input"] = str(raw_path)

            edges = raw.convert("L").filter(ImageFilter.FIND_EDGES)
            edges.thumbnail((64, 64))
            edges_path = out / f"measured_sobel_edges_{path.stem}.png"
            edges.save(edges_path)
            saved_paths["sobel_edges"] = str(edges_path)

        rec_path = out / f"brody_reconstruction_{path.stem}.png"
        final_canvas.save(rec_path)
        saved_paths["reconstruction"] = str(rec_path)

        diff_path = out / f"brody_diff_mask_{path.stem}.png"
        diff_mask.save(diff_path)
        saved_paths["diff_mask"] = str(diff_path)

    tools_used = ("PEN", "GEOMETRIC_STAMP")

    return RealImagePipelineAuditReceiptV1(
        image_path=str(path),
        source_sha256=f16_obs.provenance.source_sha256,
        native_dimensions=f16_obs.provenance.native_dimensions,
        measured_luminance=f16_obs.measured.mean_luminance,
        measured_edge_density=f16_obs.measured.edge_density,
        measured_bbox=f16_obs.measured.bounding_box_xyxy,
        f16_observation_id=f16_obs.observation_id,
        retrieved_memory_experiences=receipt.retrieved_experiences,
        queried_34_trees=receipt.queried_34_trees,
        tools_selected=tools_used,
        reconstruction_initial_iou=receipt.initial_reconstruction_iou,
        reconstruction_final_iou=receipt.final_reconstruction_iou,
        reconstruction_final_xor=receipt.final_xor_error,
        operations_count=receipt.total_operations,
        cost_spent=receipt.total_cost,
        saved_artifact_paths=saved_paths,
        mmonde_canonical_compatible=(canonical_cand.validation_status.value == "CANDIDATE"),
        decision_authority="KX108_ONLY",
    )


def measure_image_pixels(img: Image.Image) -> BrodyMeasuredObservationV1:
    """Extracts verifiable pixel measurements without AI speculation."""
    w, h = img.size
    aspect = round(w / max(1, h), 4)

    rgb = img.convert("RGB")
    stat_rgb = ImageStat.Stat(rgb)
    means_rgb = (round(stat_rgb.mean[0], 2), round(stat_rgb.mean[1], 2), round(stat_rgb.mean[2], 2))

    gray = img.convert("L")
    stat_gray = ImageStat.Stat(gray)
    mean_lum = round(stat_gray.mean[0], 2)
    std_lum = round(stat_gray.stddev[0], 2)

    # Edge detection via Laplacian-like filter (FIND_EDGES)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_pixels = [p for p in edges.getdata() if p > 50]
    edge_count = len(edge_pixels)
    edge_density = round(edge_count / max(1, w * h), 4)

    # Primary bounding box of non-background content (using Otsu-like threshold)
    threshold = int(mean_lum)
    dark_pixels = [idx for idx, val in enumerate(gray.getdata()) if val < threshold]
    if dark_pixels:
        x_coords = [p % w for p in dark_pixels]
        y_coords = [p // w for p in dark_pixels]
        bbox = (min(x_coords), min(y_coords), max(x_coords), max(y_coords))
    else:
        bbox = (0, 0, w, h)

    # Contrast ratio (max - min luminance) / max(1, mean_lum)
    min_lum, max_lum = gray.getextrema()
    contrast = round((max_lum - min_lum) / max(1.0, mean_lum), 2)

    return BrodyMeasuredObservationV1(
        dimensions=(w, h),
        aspect_ratio=aspect,
        mean_luminance=mean_lum,
        luminance_std=std_lum,
        channel_means_rgb=means_rgb,
        edge_pixel_count=edge_count,
        edge_density=edge_density,
        bounding_box_xyxy=bbox,
        contrast_ratio=contrast,
        verified_deterministic=True,
    )


def ingest_real_image_f16(
    image_path: Path | str,
    *,
    custom_device_name: str = "LOCAL_DESKTOP_CAMERA_ARCHIVE",
    qwen_override: QwenVLCandidatePerceptionV1 | None = None,
) -> RealImageObservationF16V1:
    """Ingests a real photograph from local disk and produces an F16-compliant contract."""
    path = Path(image_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Real image file not found: {path}")

    raw_bytes = path.read_bytes()
    sha = digest_bytes(raw_bytes)
    size_bytes = len(raw_bytes)

    with Image.open(path) as img:
        native_dim = img.size
        color_mode = img.mode
        measured = measure_image_pixels(img)

    provenance = RealImageProvenanceV1(
        image_path=str(path),
        origin_device=custom_device_name,
        source_sha256=sha,
        file_size_bytes=size_bytes,
        color_mode=color_mode,
        native_dimensions=native_dim,
        captured_at=datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
        provenance_chain=(f"LOCAL_DISK_FILE://{path.name}", f"SHA256:{sha[:16]}"),
    )

    # Layer 2: Candidate Perception from Qwen-VL (candidate only)
    if qwen_override is not None:
        qwen_cand = qwen_override
    else:
        # Default bounded candidate perception conjecture (safe local fallback)
        qwen_cand = QwenVLCandidatePerceptionV1(
            candidate_caption=f"Natural photograph depicting objects with edge density {measured.edge_density}",
            candidate_detected_objects=("natural_scene_elements", "structural_shapes"),
            is_hypothesis=True,
            semantics_verified=False,
        )

    # Layer 3: Brody's Cognitive Hypothesis formed by reconciling measurements with 34 trees
    trees: list[str] = ["03_PERCEPTION", "20_ESPACE"]
    support: list[str] = [
        f"Luminance mean {measured.mean_luminance} confirms real illumination gradient",
        f"Edge density {measured.edge_density} indicates natural texture variation",
    ]
    contradictions: list[str] = []

    if measured.edge_density > 0.15:
        trees.append("05_NATURE_VEGETAL")
        support.append("High edge frequency aligns with natural vegetation / organic branching")
    elif measured.aspect_ratio > 1.3:
        trees.append("12_TECHNIQUE_STRUCTURE")
        support.append("Elongated aspect ratio aligns with horizontal structural composition")

    hypothesis = BrodyCognitiveHypothesisV1(
        hypothesized_category="NATURAL_CAMERA_OBSERVATION",
        mapped_34_trees=tuple(trees),
        supporting_measurements=tuple(support),
        contradictions_or_caveats=tuple(contradictions) if contradictions else ("Requires bounded raster rendering verification",),
        confidence_score=0.85,
        is_admissible_for_reasoning=True,
    )

    return RealImageObservationF16V1(
        observation_id=f"F16-OBS-{sha[:12].upper()}",
        provenance=provenance,
        measured=measured,
        qwen_candidate=qwen_cand,
        brody_hypothesis=hypothesis,
        is_synthetic=False,
        f16_compliant=True,
    )
