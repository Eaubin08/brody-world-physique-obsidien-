"""E05: Progressive Visual Education Curriculum with Complex Silhouettes, Shading, and SVG.

Extends visual education beyond 2D geometric primitives to:
1. Complex composite silhouettes: curved vases, mugs with handles, articulated lamps, teapots.
2. Textures, tonal shading, and contact shadows: cross-hatching, directional shading, ground shadows.
3. Explicit epistemic boundaries: surfaces and hidden faces are strictly tagged 'UNKNOWN'.
4. Vectorial SVG generation: deterministic XML emission and rasterization bridge.
5. Multi-session curriculum: lessons (learning) vs heldout exams (generalization).

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
from types import MappingProxyType
from typing import Any, Mapping, Sequence
from PIL import Image, ImageDraw

from .drawing_school_v0 import black_pixels, bbox_of, digest_bytes

SIDE = 64


@dataclass(frozen=True)
class ShadedVisualObjectV1:
    """A rich visual object with silhouette, shading, and explicit unknown properties."""
    object_id: str
    object_type: str  # "MUG", "VASE", "LAMP", "TEAPOT", "COMPOSITE_SCENE"
    contour_points: tuple[tuple[int, int], ...]
    shading_style: str = "CROSS_HATCH"  # "NONE", "LINEAR_SHADE", "CROSS_HATCH", "STIPPLE"
    light_direction_degrees: float = 45.0  # Light from top-left (45°)
    contact_shadow_bbox: tuple[int, int, int, int] | None = None
    observed_properties: Mapping[str, Any] = field(default_factory=dict)
    unobserved_surfaces: tuple[str, ...] = ("BACK_FACING_SURFACE", "INTERIOR_BOTTOM", "OCCLUDED_INTERIOR_VOLUME")
    epistemic_surface_status: str = "UNKNOWN_FOR_OCCLUDED_FACES"

    def __post_init__(self) -> None:
        if not self.object_id.strip():
            raise ValueError("object_id is required")
        if not self.contour_points:
            raise ValueError("contour_points cannot be empty")
        if self.epistemic_surface_status != "UNKNOWN_FOR_OCCLUDED_FACES":
            raise ValueError("Epistemic boundary violation: unobserved surfaces must be marked UNKNOWN")


@dataclass(frozen=True)
class SVGElementV1:
    """An individual SVG drawing primitive."""
    tag: str  # "path", "rect", "ellipse", "line", "polyline"
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_xml_tag(self) -> str:
        attrs = " ".join(f'{k}="{v}"' for k, v in sorted(self.attributes.items()))
        return f"  <{self.tag} {attrs} />"


@dataclass(frozen=True)
class SVGVisualPlanV1:
    """Deterministic, bounded SVG vector plan."""
    plan_id: str
    width: int = SIDE
    height: int = SIDE
    elements: tuple[SVGElementV1, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_svg_xml(self) -> str:
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" height="{self.height}">',
            '  <!-- Brody World Physique Image Bounded SVG Export -->',
            '  <rect width="100%" height="100%" fill="white" />',
        ]
        for elem in self.elements:
            lines.append(elem.to_xml_tag())
        lines.append("</svg>")
        return "\n".join(lines)

    def render_to_pil(self) -> Image.Image:
        """Rasterizes the SVG plan deterministically into a PIL 64x64 grayscale image."""
        img = Image.new("L", (self.width, self.height), 255)
        draw = ImageDraw.Draw(img)

        for elem in self.elements:
            tag = elem.tag
            attrs = elem.attributes
            stroke_width = int(attrs.get("stroke-width", 2))
            fill_val = 0 if attrs.get("fill") == "black" else None
            outline_val = 0 if attrs.get("stroke") == "black" else None

            if tag == "rect":
                x = int(attrs.get("x", 0))
                y = int(attrs.get("y", 0))
                w = int(attrs.get("width", 0))
                h = int(attrs.get("height", 0))
                draw.rectangle([x, y, x + w, y + h], fill=fill_val, outline=outline_val, width=stroke_width)

            elif tag == "ellipse":
                cx = int(attrs.get("cx", 0))
                cy = int(attrs.get("cy", 0))
                rx = int(attrs.get("rx", 0))
                ry = int(attrs.get("ry", 0))
                draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill_val, outline=outline_val, width=stroke_width)

            elif tag == "line":
                x1 = int(attrs.get("x1", 0))
                y1 = int(attrs.get("y1", 0))
                x2 = int(attrs.get("x2", 0))
                y2 = int(attrs.get("y2", 0))
                draw.line([(x1, y1), (x2, y2)], fill=0, width=stroke_width)

            elif tag == "polyline":
                raw_pts = attrs.get("points", "")
                pts = []
                for pair in raw_pts.strip().split():
                    if "," in pair:
                        coords = pair.split(",")
                        pts.append((int(coords[0]), int(coords[1])))
                if len(pts) >= 2:
                    draw.line(pts, fill=0, width=stroke_width, joint="curve")

            elif tag == "path":
                # Handle simple path d="M x y L x y ..."
                d = attrs.get("d", "").strip()
                tokens = d.split()
                pts = []
                idx = 0
                while idx < len(tokens):
                    cmd = tokens[idx]
                    if cmd in ("M", "L") and idx + 2 < len(tokens):
                        pts.append((int(tokens[idx + 1]), int(tokens[idx + 2])))
                        idx += 3
                    elif cmd == "Z":
                        if pts:
                            pts.append(pts[0])
                        idx += 1
                    else:
                        idx += 1
                if len(pts) >= 2:
                    draw.line(pts, fill=0, width=stroke_width)

        return img


# -------------------------------------------------------------------------
# RENDERERS FOR PROGRESSIVE OBJECTS
# -------------------------------------------------------------------------

def create_mug_object(x: int = 16, y: int = 20, w: int = 24, h: int = 28) -> ShadedVisualObjectV1:
    """Creates a coffee mug with cylindrical body, elliptical rim, curved handle, and shadow."""
    body_pts = (
        (x, y + 4), (x, y + h), (x + w, y + h), (x + w, y + 4),
        (x + w, y + 4), (x + w // 2, y + 6), (x, y + 4), (x + w // 2, y + 2), (x + w, y + 4),
    )
    return ShadedVisualObjectV1(
        object_id="mug_01",
        object_type="MUG",
        contour_points=body_pts,
        shading_style="CROSS_HATCH",
        light_direction_degrees=45.0,
        contact_shadow_bbox=(x - 4, y + h - 1, x + w + 6, y + h + 4),
        observed_properties=MappingProxyType({
            "has_handle": True,
            "handle_side": "RIGHT",
            "body_aspect_ratio": round(w / h, 2),
            "rim_ellipse_semi_minor": 2,
        }),
    )


def create_vase_object(x: int = 18, y: int = 12, w: int = 28, h: int = 44) -> ShadedVisualObjectV1:
    """Creates a curved ceramic vase with narrow neck, bulbous body, flat base, and shading."""
    pts = (
        (x + 6, y), (x + w - 6, y),  # Rim
        (x + 8, y + 10), (x + w - 8, y + 10),  # Neck
        (x + 2, y + 24), (x + w - 2, y + 24),  # Upper belly
        (x, y + 34), (x + w, y + 34),  # Maximum width
        (x + 6, y + h), (x + w - 6, y + h),  # Base
    )
    return ShadedVisualObjectV1(
        object_id="vase_01",
        object_type="VASE",
        contour_points=pts,
        shading_style="LINEAR_SHADE",
        light_direction_degrees=45.0,
        contact_shadow_bbox=(x + 2, y + h - 1, x + w - 2, y + h + 3),
        observed_properties=MappingProxyType({
            "curvature_kind": "DOUBLE_CURVE_BELL",
            "neck_ratio": 0.40,
            "body_aspect_ratio": round(w / h, 2),
        }),
    )


def create_lamp_object(x: int = 20, y: int = 14, w: int = 26, h: int = 42) -> ShadedVisualObjectV1:
    """Creates an articulated desk lamp with weighted base, armature arm, and shaded conical shade."""
    pts = (
        (x + 4, y + h), (x + w - 4, y + h),  # Base
        (x + w // 2, y + h), (x + w // 2 - 4, y + h // 2),  # Lower armature
        (x + w // 2 - 4, y + h // 2), (x + 8, y + 12),  # Upper armature
        (x, y + 6), (x + 18, y + 18),  # Conical shade
    )
    return ShadedVisualObjectV1(
        object_id="lamp_01",
        object_type="LAMP",
        contour_points=pts,
        shading_style="STIPPLE",
        light_direction_degrees=45.0,
        contact_shadow_bbox=(x + 2, y + h, x + w - 2, y + h + 3),
        observed_properties=MappingProxyType({
            "armature_joints": 2,
            "shade_orientation": "DOWN_LEFT",
        }),
    )


def create_teapot_object(x: int = 12, y: int = 18, w: int = 40, h: int = 32) -> ShadedVisualObjectV1:
    """Creates a teapot with rounded body, curved spout on left, handle on right, lid with knob, and shadow."""
    pts = (
        # Lid knob
        (x + w // 2 - 2, y), (x + w // 2 + 2, y), (x + w // 2, y + 3),
        # Lid rim
        (x + 14, y + 6), (x + w - 14, y + 6),
        # Spherical belly
        (x + 8, y + 14), (x + w - 8, y + 14),
        (x + 6, y + 22), (x + w - 6, y + 22),
        # Spout on left
        (x, y + 10), (x + 6, y + 18),
        # Handle on right
        (x + w + 4, y + 12), (x + w + 4, y + 24),
        # Foot base
        (x + 12, y + h), (x + w - 12, y + h),
    )
    return ShadedVisualObjectV1(
        object_id="teapot_exam_heldout",
        object_type="TEAPOT",
        contour_points=pts,
        shading_style="CROSS_HATCH",
        light_direction_degrees=45.0,
        contact_shadow_bbox=(x + 8, y + h - 1, x + w - 8, y + h + 4),
        observed_properties=MappingProxyType({
            "spout_side": "LEFT",
            "handle_side": "RIGHT",
            "has_lid_knob": True,
        }),
    )


def render_shaded_object(
    obj: ShadedVisualObjectV1,
    canvas_size: tuple[int, int] = (SIDE, SIDE),
) -> Image.Image:
    """Renders a ShadedVisualObjectV1 to a 64x64 grayscale PIL image with tonal hatching and shadow."""
    img = Image.new("L", canvas_size, 255)
    draw = ImageDraw.Draw(img)

    # 1. Draw contact shadow if present
    if obj.contact_shadow_bbox:
        sx0, sy0, sx1, sy1 = obj.contact_shadow_bbox
        draw.ellipse([sx0, sy0, sx1, sy1], fill=120)  # Mid-gray ground shadow

    # 2. Draw object body according to type
    if obj.object_type == "MUG":
        # Rim ellipse
        x0, y0, x1, y1 = 16, 20, 40, 48
        draw.ellipse([x0, y0, x1, y0 + 6], outline=0, width=2)
        # Cylinder sides and base
        draw.line([(x0, y0 + 3), (x0, y1)], fill=0, width=2)
        draw.line([(x1, y0 + 3), (x1, y1)], fill=0, width=2)
        draw.line([(x0, y1), (x1, y1)], fill=0, width=2)
        # Curved handle on right
        draw.arc([x1 - 2, y0 + 8, x1 + 10, y1 - 6], start=270, end=90, fill=0, width=2)

        # Cross-hatch shading on shaded side (right side, opposite to 45° top-left light)
        if obj.shading_style in ("CROSS_HATCH", "LINEAR_SHADE"):
            for y_line in range(y0 + 8, y1 - 2, 4):
                draw.line([(x0 + 14, y_line), (x1 - 2, y_line)], fill=0, width=1)
            if obj.shading_style == "CROSS_HATCH":
                for diag in range(-4, 16, 4):
                    draw.line([(x0 + 16 + diag, y0 + 8), (x0 + 16 + diag + 8, y1 - 2)], fill=0, width=1)

    elif obj.object_type == "VASE":
        # Double curved contour
        x0, y0, x1, y1 = 18, 12, 46, 56
        cx = (x0 + x1) // 2
        # Rim
        draw.line([(cx - 8, y0), (cx + 8, y0)], fill=0, width=2)
        # Neck
        draw.line([(cx - 8, y0), (cx - 5, y0 + 12)], fill=0, width=2)
        draw.line([(cx + 8, y0), (cx + 5, y0 + 12)], fill=0, width=2)
        # Belly curve
        draw.line([(cx - 5, y0 + 12), (x0, y0 + 26)], fill=0, width=2)
        draw.line([(cx + 5, y0 + 12), (x1, y0 + 26)], fill=0, width=2)
        draw.line([(x0, y0 + 26), (cx - 7, y1)], fill=0, width=2)
        draw.line([(x1, y0 + 26), (cx + 7, y1)], fill=0, width=2)
        # Base
        draw.line([(cx - 7, y1), (cx + 7, y1)], fill=0, width=2)

        # Shading lines on bottom-right belly
        if obj.shading_style in ("LINEAR_SHADE", "CROSS_HATCH"):
            for sy in range(y0 + 20, y1 - 2, 3):
                draw.line([(cx + 2, sy), (cx + 11, sy)], fill=0, width=1)

    elif obj.object_type == "LAMP":
        # Base
        x0, y0, x1, y1 = 20, 14, 46, 56
        draw.ellipse([x0, y1 - 3, x1, y1 + 1], outline=0, width=2)
        # Armature lines
        draw.line([(33, y1 - 2), (28, 36)], fill=0, width=3)
        draw.line([(28, 36), (36, 22)], fill=0, width=3)
        # Shade cone
        draw.polygon([(24, 18), (38, 14), (32, 28)], outline=0)

    elif obj.object_type == "TEAPOT":
        # Main belly ellipse
        draw.ellipse([18, 24, 46, 46], outline=0, width=2)
        # Lid & knob
        draw.line([(26, 24), (38, 24)], fill=0, width=2)
        draw.ellipse([30, 20, 34, 24], fill=0)
        # Spout
        draw.line([(20, 32), (12, 26)], fill=0, width=2)
        draw.line([(12, 26), (14, 38)], fill=0, width=2)
        draw.line([(14, 38), (22, 38)], fill=0, width=2)
        # Handle
        draw.arc([42, 26, 52, 42], start=270, end=90, fill=0, width=2)
        # Shading
        for y_hatch in range(32, 44, 3):
            draw.line([(34, y_hatch), (44, y_hatch)], fill=0, width=1)

    return img


def convert_object_to_svg_plan(obj: ShadedVisualObjectV1) -> SVGVisualPlanV1:
    """Produces a clean SVG vector plan corresponding to the progressive visual object."""
    elements: list[SVGElementV1] = []

    # Shadow element
    if obj.contact_shadow_bbox:
        x0, y0, x1, y1 = obj.contact_shadow_bbox
        cx = (x0 + x1) // 2
        cy = (y0 + y1) // 2
        rx = (x1 - x0) // 2
        ry = max(1, (y1 - y0) // 2)
        elements.append(
            SVGElementV1(
                tag="ellipse",
                attributes={"cx": cx, "cy": cy, "rx": rx, "ry": ry, "fill": "#888888", "stroke": "none"},
            )
        )

    # Outline elements based on object type
    if obj.object_type == "MUG":
        elements.append(SVGElementV1(tag="ellipse", attributes={"cx": 28, "cy": 23, "rx": 12, "ry": 3, "stroke": "black", "stroke-width": 2, "fill": "none"}))
        elements.append(SVGElementV1(tag="line", attributes={"x1": 16, "y1": 23, "x2": 16, "y2": 48, "stroke": "black", "stroke-width": 2}))
        elements.append(SVGElementV1(tag="line", attributes={"x1": 40, "y1": 23, "x2": 40, "y2": 48, "stroke": "black", "stroke-width": 2}))
        elements.append(SVGElementV1(tag="line", attributes={"x1": 16, "y1": 48, "x2": 40, "y2": 48, "stroke": "black", "stroke-width": 2}))
        # Handle
        elements.append(SVGElementV1(tag="line", attributes={"x1": 40, "y1": 28, "x2": 48, "y2": 32, "stroke": "black", "stroke-width": 2}))
        elements.append(SVGElementV1(tag="line", attributes={"x1": 48, "y1": 32, "x2": 48, "y2": 42, "stroke": "black", "stroke-width": 2}))
        elements.append(SVGElementV1(tag="line", attributes={"x1": 48, "y1": 42, "x2": 40, "y2": 44, "stroke": "black", "stroke-width": 2}))

    elif obj.object_type == "VASE":
        pts_str = "24,12 40,12 37,24 46,38 39,56 25,56 18,38 27,24 24,12"
        elements.append(SVGElementV1(tag="polyline", attributes={"points": pts_str, "stroke": "black", "stroke-width": 2, "fill": "none"}))

    elif obj.object_type == "LAMP":
        elements.append(SVGElementV1(tag="ellipse", attributes={"cx": 33, "cy": 55, "rx": 13, "ry": 2, "stroke": "black", "stroke-width": 2, "fill": "none"}))
        elements.append(SVGElementV1(tag="line", attributes={"x1": 33, "y1": 53, "x2": 28, "y2": 36, "stroke": "black", "stroke-width": 3}))
        elements.append(SVGElementV1(tag="line", attributes={"x1": 28, "y1": 36, "x2": 36, "y2": 22, "stroke": "black", "stroke-width": 3}))
        elements.append(SVGElementV1(tag="polyline", attributes={"points": "24,18 38,14 32,28 24,18", "stroke": "black", "stroke-width": 2, "fill": "none"}))

    elif obj.object_type == "TEAPOT":
        elements.append(SVGElementV1(tag="ellipse", attributes={"cx": 32, "cy": 35, "rx": 14, "ry": 11, "stroke": "black", "stroke-width": 2, "fill": "none"}))
        elements.append(SVGElementV1(tag="ellipse", attributes={"cx": 32, "cy": 22, "rx": 2, "ry": 2, "fill": "black", "stroke": "black"}))
        elements.append(SVGElementV1(tag="polyline", attributes={"points": "20,32 12,26 14,38 22,38", "stroke": "black", "stroke-width": 2, "fill": "none"}))
        elements.append(SVGElementV1(tag="polyline", attributes={"points": "46,28 52,32 52,40 44,42", "stroke": "black", "stroke-width": 2, "fill": "none"}))

    return SVGVisualPlanV1(
        plan_id=f"svg_plan_{obj.object_id}",
        elements=tuple(elements),
        metadata=MappingProxyType({"object_type": obj.object_type, "shading": obj.shading_style}),
    )
