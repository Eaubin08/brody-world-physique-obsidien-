"""V03/V04: Multi-Perspective Vantage Transformations & Object Permanence.

Extends visual perception across observer vantage points:
- 2D camera translations (dx, dy).
- Discrete planar frame rotations (0°, 90°, 180°, 270°).
- Scale changes (zoom in / zoom out).
- Object permanence tracking across perspective shifts.
- Partial visibility & occlusion detection (boundary clipping).

Epistemic boundary:
- is_3d_view_synthesis = False: strictly forbids falsely claiming 3D world understanding
  from 2D planar vantage transformations.
- Decision authority: KX108_ONLY.
- Readonly representation: native_memory_write_allowed = False.
- Emits act: False.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any, Mapping
from PIL import Image

from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes

SIDE = 64


@dataclass(frozen=True)
class VantageTransform2DV03:
    """Planar observer vantage specification."""
    rotation_degrees: int  # 0, 90, 180, 270
    translation_dx: int = 0
    translation_dy: int = 0
    scale: float = 1.0
    center_xy: tuple[int, int] = (SIDE // 2, SIDE // 2)
    is_3d_view_synthesis: bool = False  # Strictly False: 2D affine only

    def __post_init__(self) -> None:
        if self.rotation_degrees not in (0, 90, 180, 270):
            raise ValueError(f"rotation_degrees must be in (0, 90, 180, 270), got {self.rotation_degrees}")
        if self.scale <= 0.0:
            raise ValueError("scale must be strictly positive")
        if self.is_3d_view_synthesis:
            raise ValueError("3D view synthesis cannot be claimed from 2D planar vantage transform")


@dataclass(frozen=True)
class ObjectPermanenceRecordV04:
    """Certifies object identity and structural permanence under vantage change."""
    source_sha256: str
    transformed_sha256: str
    original_bbox: tuple[int, int, int, int]
    transformed_bbox: tuple[int, int, int, int]
    original_pixel_count: int
    visible_pixel_count: int
    in_bounds_ratio: float
    is_partially_occluded: bool
    shape_invariance_preserved: bool
    rotation_degrees: int
    decision_authority: str = "KX108_ONLY"


class MultiPerspectiveTransformerV03V04:
    """Performs geometric vantage transformations while recording object permanence."""

    def transform_vantage(
        self,
        image: Image.Image,
        transform: VantageTransform2DV03,
    ) -> tuple[Image.Image, ObjectPermanenceRecordV04]:
        gray = image.convert("L")
        w, h = gray.size
        orig_ink = black_pixels(gray)
        if not orig_ink:
            raise ValueError("Cannot transform blank canvas")

        orig_sha = digest_bytes(gray.tobytes())
        orig_bbox = bbox_of(orig_ink)
        cx, cy = transform.center_xy
        rad = math.radians(transform.rotation_degrees)
        cos_theta = round(math.cos(rad))
        sin_theta = round(math.sin(rad))

        out_img = Image.new("L", (w, h), 255)
        out_pixels = out_img.load()

        visible_transformed: list[tuple[int, int]] = []
        total_projected = 0

        # Transform each black pixel index (y * SIDE + x)
        for p in orig_ink:
            total_projected += 1
            x = p % w
            y = p // w

            # 1. Translate to center
            rx = (x - cx) * transform.scale
            ry = (y - cy) * transform.scale

            # 2. Planar rotation (image coordinates: positive y is down)
            nx = rx * cos_theta - ry * sin_theta
            ny = rx * sin_theta + ry * cos_theta

            # 3. Translate back with camera shift (dx, dy)
            final_x = int(round(nx + cx + transform.translation_dx))
            final_y = int(round(ny + cy + transform.translation_dy))

            # 4. Canvas boundary clip
            if 0 <= final_x < w and 0 <= final_y < h:
                out_pixels[final_x, final_y] = 0
                visible_transformed.append((final_x, final_y))

        trans_sha = digest_bytes(out_img.tobytes())
        vis_count = len(visible_transformed)
        in_bounds_ratio = vis_count / max(1, total_projected)
        is_occluded = in_bounds_ratio < 0.98

        if visible_transformed:
            flat_indices = {vy * w + vx for (vx, vy) in visible_transformed}
            trans_bbox = bbox_of(flat_indices)
        else:
            trans_bbox = (0, 0, 0, 0)

        # Invariance is preserved if shapes are intact without significant clipping
        invariance_ok = not is_occluded and vis_count > 0

        record = ObjectPermanenceRecordV04(
            source_sha256=orig_sha,
            transformed_sha256=trans_sha,
            original_bbox=orig_bbox,
            transformed_bbox=trans_bbox,
            original_pixel_count=len(orig_ink),
            visible_pixel_count=vis_count,
            in_bounds_ratio=round(in_bounds_ratio, 4),
            is_partially_occluded=is_occluded,
            shape_invariance_preserved=invariance_ok,
            rotation_degrees=transform.rotation_degrees,
        )

        return out_img, record
