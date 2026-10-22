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
    object_id: str = ""
    depth_z: float = 1.0
    permanence_certified: bool = True
    is_3d_view_synthesis: bool = False


@dataclass(frozen=True)
class DepthLayeredObjectV04:
    """An object positioned in 2.5D space with explicit depth layer z."""
    object_id: str
    image: Image.Image
    depth_z: float
    anchor_xy: tuple[int, int] = (0, 0)
    label: str = ""

    def __post_init__(self) -> None:
        if self.depth_z <= 0.0:
            raise ValueError(f"depth_z must be strictly positive, got {self.depth_z}")


@dataclass(frozen=True)
class ObserverVantageShiftV04:
    """Observer vantage shift specifying 2D motion and planar parallax parameters."""
    observer_dx: int
    observer_dy: int = 0
    rotation_degrees: int = 0
    parallax_factor: float = 1.0
    is_3d_view_synthesis: bool = False
    decision_authority: str = "KX108_ONLY"

    def __post_init__(self) -> None:
        if self.rotation_degrees not in (0, 90, 180, 270):
            raise ValueError(f"rotation_degrees must be in (0, 90, 180, 270), got {self.rotation_degrees}")
        if self.is_3d_view_synthesis:
            raise ValueError("3D view synthesis cannot be claimed from 2.5D planar parallax")


@dataclass(frozen=True)
class MultiObjectParallaxSceneResultV04:
    """Result of 2.5D multi-object rendering under observer vantage shift."""
    composite_image: Image.Image
    composite_sha256: str
    object_records: list[ObjectPermanenceRecordV04]
    occlusion_fractions: dict[str, float]
    permanence_certified: bool
    is_3d_view_synthesis: bool = False
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

    def render_multi_object_parallax(
        self,
        objects: list[DepthLayeredObjectV04],
        shift: ObserverVantageShiftV04,
        canvas_size: tuple[int, int] = (SIDE, SIDE),
    ) -> MultiObjectParallaxSceneResultV04:
        """Renders 2.5D multi-object scene with depth parallax and partial occlusions.

        Strict epistemic boundary: 2.5D depth ordering and translation parallax ONLY.
        is_3d_view_synthesis is strictly False.
        """
        if shift.is_3d_view_synthesis:
            raise ValueError("3D view synthesis cannot be claimed from 2.5D planar parallax")

        cw, ch = canvas_size
        # Sort objects by depth descending: farthest objects rendered first, closest last
        sorted_objs = sorted(objects, key=lambda o: o.depth_z, reverse=True)

        pixel_owner_map: dict[tuple[int, int], str] = {}
        transformed_pixels_by_obj: dict[str, set[tuple[int, int]]] = {}
        orig_pixels_by_obj: dict[str, set[int]] = {}

        rad = math.radians(shift.rotation_degrees)
        cos_t = round(math.cos(rad))
        sin_t = round(math.sin(rad))

        records: list[ObjectPermanenceRecordV04] = []
        occlusion_fractions: dict[str, float] = {}

        # 1. Transform each object with depth-dependent parallax
        for obj in sorted_objs:
            gray = obj.image.convert("L")
            ow, oh = gray.size
            ink = black_pixels(gray)
            orig_pixels_by_obj[obj.object_id] = ink

            # Motion parallax: apparent displacement is inversely proportional to depth z
            disp_x = int(round((shift.observer_dx * shift.parallax_factor) / obj.depth_z))
            disp_y = int(round((shift.observer_dy * shift.parallax_factor) / obj.depth_z))

            obj_pixels_transformed: set[tuple[int, int]] = set()
            cx, cy = ow // 2, oh // 2

            for p in ink:
                x = p % ow
                y = p // ow
                rx = x - cx
                ry = y - cy
                nx = rx * cos_t - ry * sin_t
                ny = rx * sin_t + ry * cos_t
                final_x = int(round(nx + cx + obj.anchor_xy[0] + disp_x))
                final_y = int(round(ny + cy + obj.anchor_xy[1] + disp_y))
                if 0 <= final_x < cw and 0 <= final_y < ch:
                    obj_pixels_transformed.add((final_x, final_y))

            transformed_pixels_by_obj[obj.object_id] = obj_pixels_transformed

            # Painter's layering: closer object overwrites pixels of farther object
            for pt in obj_pixels_transformed:
                pixel_owner_map[pt] = obj.object_id

        # 2. Render composite image
        composite = Image.new("L", (cw, ch), 255)
        comp_pixels = composite.load()
        for (x, y) in pixel_owner_map:
            comp_pixels[x, y] = 0

        comp_sha = digest_bytes(composite.tobytes())

        # 3. Analyze visibility and verify object permanence for each object
        for obj in objects:
            orig_count = len(orig_pixels_by_obj[obj.object_id])
            transformed_pts = transformed_pixels_by_obj[obj.object_id]
            visible_pts = [pt for pt in transformed_pts if pixel_owner_map.get(pt) == obj.object_id]
            vis_count = len(visible_pts)

            in_bounds_ratio = vis_count / max(1, orig_count)
            is_occluded = vis_count < orig_count
            occlusion_frac = round((orig_count - vis_count) / max(1, orig_count), 4)
            occlusion_fractions[obj.object_id] = occlusion_frac

            orig_bbox = bbox_of(orig_pixels_by_obj[obj.object_id]) if orig_count > 0 else (0, 0, 0, 0)
            if visible_pts:
                flat_vis = {vy * cw + vx for (vx, vy) in visible_pts}
                trans_bbox = bbox_of(flat_vis)
            else:
                trans_bbox = (0, 0, 0, 0)

            record = ObjectPermanenceRecordV04(
                source_sha256=digest_bytes(obj.image.convert("L").tobytes()),
                transformed_sha256=comp_sha,
                original_bbox=orig_bbox,
                transformed_bbox=trans_bbox,
                original_pixel_count=orig_count,
                visible_pixel_count=vis_count,
                in_bounds_ratio=round(in_bounds_ratio, 4),
                is_partially_occluded=is_occluded,
                shape_invariance_preserved=(vis_count > 0 and not is_occluded),
                rotation_degrees=shift.rotation_degrees,
                decision_authority="KX108_ONLY",
                object_id=obj.object_id,
                depth_z=obj.depth_z,
                permanence_certified=True,
                is_3d_view_synthesis=False,
            )
            records.append(record)

        return MultiObjectParallaxSceneResultV04(
            composite_image=composite,
            composite_sha256=comp_sha,
            object_records=records,
            occlusion_fractions=occlusion_fractions,
            permanence_certified=True,
            is_3d_view_synthesis=False,
            decision_authority="KX108_ONLY",
        )
