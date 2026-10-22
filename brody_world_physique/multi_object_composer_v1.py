"""G03: Multi-Object Composition Preserving Proportions and Shape Identity.

Composes multi-object visual scenes from previously observed shapes, connected
components, and procedural gestures without distorting individual component
proportions or violating topological relations.

Constitutional boundaries:
- Candidate only: is_candidate = True.
- Decision authority: KX108_ONLY.
- Readonly memory: native_memory_write_allowed = False.
- Auto-promotion: False.
- Emits act: False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import io
import json
from math import hypot
from types import MappingProxyType
from typing import Any, Mapping, Sequence
from PIL import Image, ImageDraw

from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes
from .drawing_school_v1 import GestureV1, render
from .visual_intent_contracts_v1 import ConstraintKindV1, RegionConstraintV1


@dataclass(frozen=True)
class ObjectComponentV1:
    """An observed or recalled visual object component."""
    component_id: str
    source_experience_ref: str
    points: tuple[tuple[int, int], ...]
    aspect_ratio: float  # width / height
    original_bbox: tuple[int, int, int, int]
    kind: str = "COMPONENT_SHAPE"

    def __post_init__(self) -> None:
        if not self.component_id.strip():
            raise ValueError("component_id is required")
        if not self.points:
            raise ValueError("points cannot be empty")
        if self.aspect_ratio <= 0.0:
            raise ValueError("aspect_ratio must be positive")

    @classmethod
    def from_image(
        cls,
        component_id: str,
        image: Image.Image,
        source_ref: str = "OBSERVED_RASTER",
    ) -> ObjectComponentV1:
        pixels = black_pixels(image.convert("L"))
        if not pixels:
            raise ValueError("Cannot create component from blank image")
        x0, y0, x1, y1 = bbox_of(pixels)
        w = max(1, x1 - x0)
        h = max(1, y1 - y0)
        aspect = w / h
        img_w, _ = image.size
        pt_coords = tuple(((p % img_w), (p // img_w)) for p in sorted(pixels))
        return cls(
            component_id=component_id,
            source_experience_ref=source_ref,
            points=pt_coords,
            aspect_ratio=aspect,
            original_bbox=(x0, y0, x1, y1),
        )


@dataclass(frozen=True)
class SpatialRelationConstraintV1:
    """Relative topological or spatial relation between two components."""
    source_id: str
    target_id: str
    relation_kind: str  # "NEAR", "FAR", "TOP", "BOTTOM", "LEFT", "RIGHT"
    tolerance_px: float = 8.0

    def __post_init__(self) -> None:
        if self.relation_kind not in ("NEAR", "FAR", "TOP", "BOTTOM", "LEFT", "RIGHT"):
            raise ValueError(f"Unknown spatial relation kind: {self.relation_kind}")


@dataclass(frozen=True)
class SceneCompositionSpecV1:
    """Specification for composing multiple objects into a coherent scene."""
    spec_id: str
    canvas_dimensions: tuple[int, int]
    components: tuple[ObjectComponentV1, ...]
    target_placements: Mapping[str, tuple[int, int, int, int]]  # component_id -> target bbox [x0, y0, x1, y1]
    spatial_relations: tuple[SpatialRelationConstraintV1, ...] = ()
    preserve_aspect_ratio: bool = True
    max_aspect_ratio_deviation: float = 0.15
    decision_authority: str = "KX108_ONLY"

    def __post_init__(self) -> None:
        if self.decision_authority != "KX108_ONLY":
            raise ValueError("Decision authority must be KX108_ONLY")
        for comp in self.components:
            if comp.component_id not in self.target_placements:
                raise ValueError(f"Missing placement for component: {comp.component_id}")


@dataclass(frozen=True)
class ComposedSceneArtifactV1:
    """Result of multi-object composition with certified proportion integrity."""
    artifact_id: str
    spec_id: str
    image_bytes: bytes
    image_sha256: str
    placed_bboxes: Mapping[str, tuple[int, int, int, int]]
    aspect_ratio_deviations: Mapping[str, float]
    proportions_preserved: bool
    relations_satisfied: tuple[str, ...]
    relations_violated: tuple[str, ...]
    is_candidate: bool = True
    native_memory_write_allowed: bool = False
    decision_authority: str = "KX108_ONLY"

    def as_pil_image(self) -> Image.Image:
        return Image.open(io.BytesIO(self.image_bytes))


class MultiObjectComposerV1:
    """Deterministic multi-object composer preserving component geometry and proportions."""

    def compose_scene(self, spec: SceneCompositionSpecV1) -> ComposedSceneArtifactV1:
        cw, ch = spec.canvas_dimensions
        canvas = Image.new("L", (cw, ch), 255)
        canvas_pixels = canvas.load()

        placed_bboxes: dict[str, tuple[int, int, int, int]] = {}
        deviations: dict[str, float] = {}

        # 1. Place each component into target bbox while preserving proportion
        for comp in spec.components:
            tx0, ty0, tx1, ty1 = spec.target_placements[comp.component_id]
            tw = max(1, tx1 - tx0)
            th = max(1, ty1 - ty0)

            ox0, oy0, ox1, oy1 = comp.original_bbox
            ow = max(1, ox1 - ox0)
            oh = max(1, oy1 - oy0)

            # Proportion preservation calculation
            if spec.preserve_aspect_ratio:
                orig_aspect = comp.aspect_ratio
                target_aspect = tw / th
                aspect_dev = abs(orig_aspect - target_aspect) / orig_aspect
                deviations[comp.component_id] = round(aspect_dev, 4)

                # Fit inside target bbox preserving aspect ratio
                if target_aspect > orig_aspect:
                    # Target is wider than original: scale by height
                    scale = th / oh
                    actual_w = round(ow * scale)
                    actual_h = th
                    start_x = tx0 + (tw - actual_w) // 2
                    start_y = ty0
                else:
                    # Target is taller than original: scale by width
                    scale = tw / ow
                    actual_w = tw
                    actual_h = round(oh * scale)
                    start_x = tx0
                    start_y = ty0 + (th - actual_h) // 2
            else:
                scale_x = tw / ow
                scale_y = th / oh
                actual_w, actual_h = tw, th
                start_x, start_y = tx0, ty0
                deviations[comp.component_id] = 0.0

            # Render scaled pixels
            actual_points: list[tuple[int, int]] = []
            for px, py in comp.points:
                rel_x = (px - ox0) / ow
                rel_y = (py - oy0) / oh
                nx = int(start_x + rel_x * actual_w)
                ny = int(start_y + rel_y * actual_h)
                if 0 <= nx < cw and 0 <= ny < ch:
                    canvas_pixels[nx, ny] = 0
                    actual_points.append((nx, ny))

            if actual_points:
                actual_indices = {ny * cw + nx for (nx, ny) in actual_points}
                placed_bboxes[comp.component_id] = bbox_of(actual_indices)
            else:
                placed_bboxes[comp.component_id] = (start_x, start_y, start_x + actual_w, start_y + actual_h)

        # 2. Check spatial relation constraints
        satisfied: list[str] = []
        violated: list[str] = []

        for rel in spec.spatial_relations:
            if rel.source_id not in placed_bboxes or rel.target_id not in placed_bboxes:
                violated.append(f"MISSING_COMPONENTS:{rel.source_id}->{rel.target_id}")
                continue

            sb = placed_bboxes[rel.source_id]
            tb = placed_bboxes[rel.target_id]
            scx = (sb[0] + sb[2]) / 2.0
            scy = (sb[1] + sb[3]) / 2.0
            tcx = (tb[0] + tb[2]) / 2.0
            tcy = (tb[1] + tb[3]) / 2.0
            dist = hypot(scx - tcx, scy - tcy)

            rel_ok = False
            if rel.relation_kind == "NEAR":
                rel_ok = dist <= 32.0
            elif rel.relation_kind == "FAR":
                rel_ok = dist > 32.0
            elif rel.relation_kind == "TOP":
                rel_ok = scy < tcy
            elif rel.relation_kind == "BOTTOM":
                rel_ok = scy > tcy
            elif rel.relation_kind == "LEFT":
                rel_ok = scx < tcx
            elif rel.relation_kind == "RIGHT":
                rel_ok = scx > tcx

            label = f"{rel.source_id}_{rel.relation_kind}_{rel.target_id}"
            if rel_ok:
                satisfied.append(label)
            else:
                violated.append(label)

        buf = io.BytesIO()
        canvas.save(buf, format="PNG")
        png_bytes = buf.getvalue()
        sha = digest_bytes(canvas.tobytes())

        proportions_ok = all(
            d <= spec.max_aspect_ratio_deviation for d in deviations.values()
        )

        return ComposedSceneArtifactV1(
            artifact_id=f"COMP-{spec.spec_id}",
            spec_id=spec.spec_id,
            image_bytes=png_bytes,
            image_sha256=sha,
            placed_bboxes=MappingProxyType(placed_bboxes),
            aspect_ratio_deviations=MappingProxyType(deviations),
            proportions_preserved=proportions_ok,
            relations_satisfied=tuple(satisfied),
            relations_violated=tuple(violated),
        )
