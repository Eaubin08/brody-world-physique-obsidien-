"""Brody Image I1/R1: deterministic image isolation, reconstruction and compositing.

This is a bounded IMAGE-EDITING tool, not an autonomous image generator,
physics model, proof of understanding, or native-memory writer.
Masks may be supplied or extracted from a uniform known background color.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_rgb(value: str) -> tuple[int, int, int]:
    """Accept comma-separated RGB, e.g. 20,110,35."""
    values = value.split(",")
    if len(values) != 3:
        raise ValueError("key must contain three comma-separated RGB integers")
    try:
        rgb = tuple(int(v.strip()) for v in values)
    except ValueError as exc:
        raise ValueError("key requires integer RGB channels") from exc
    if any(not 0 <= v <= 255 for v in rgb):
        raise ValueError("RGB channels must be in 0..255")
    return rgb  # type: ignore[return-value]


def chroma_key_mask(
    source: Image.Image, key: tuple[int, int, int], tolerance: int = 0
) -> Image.Image:
    """A COLOR-KEY baseline, not neural segmentation.

    Pixels within the max-channel tolerance of the supplied key become clear.
    Similar-colored portions of the subject can be removed. Do not use this
    for complex natural scenes without a reviewed explicit mask.
    """
    if not 0 <= tolerance <= 255:
        raise ValueError("tolerance must be in 0..255")
    rgb = source.convert("RGB")
    mask = Image.new("L", rgb.size)
    pixels = rgb.load()
    mask.putdata([
        0 if max(abs(pixels[xx, yy][c] - key[c]) for c in range(3)) <= tolerance else 255
        for yy in range(rgb.height) for xx in range(rgb.width)
    ])
    return mask


def _mask_metrics(mask: Image.Image) -> dict[str, Any]:
    hist = mask.histogram()
    total = mask.width * mask.height
    return {
        "pixels_total": total,
        "pixels_transparent": hist[0],
        "pixels_fully_opaque": hist[255],
        "pixels_partially_transparent": total - hist[0] - hist[255],
        "subject_coverage_fraction": round((total - hist[0]) / total, 6),
    }


def _exact_pixel_check(
    original: Image.Image, composited: Image.Image, mask: Image.Image, x: int, y: int
) -> dict[str, Any]:
    """Compare fully opaque unscaled source pixels to their composed positions."""
    original_rgb = original.convert("RGB")
    composed_rgb = composited.convert("RGB")
    sampled = 0
    mismatched = 0
    for iy in range(mask.height):
        for ix in range(mask.width):
            if mask.getpixel((ix, iy)) == 255:
                sampled += 1
                if original_rgb.getpixel((ix, iy)) != composed_rgb.getpixel((ix + x, iy + y)):
                    mismatched += 1
    return {
        "status": "PASS" if sampled and mismatched == 0 else ("FAIL" if mismatched else "INCONCLUSIVE"),
        "fully_opaque_pixels_compared": sampled,
        "rgb_mismatched_pixels": mismatched,
        "comparison_scope": "UNSCALED_FULLY_OPAQUE_SOURCE_PIXELS_ONLY",
        "does_not_test": ["semantic identity", "occlusion realism", "depth", "causality"],
    }


def run_image_edit(
    source_path: str | Path,
    background_path: str | Path,
    output_dir: str | Path,
    *,
    mask_path: str | Path | None = None,
    key_rgb: tuple[int, int, int] | None = None,
    key_tolerance: int = 0,
    x: int = 0,
    y: int = 0,
    scale: float = 1.0,
    user_intent: str = "Place reference subject into another background; preserve source pixels where possible.",
) -> dict[str, Any]:
    """Build cutout/composite PNGs and an honest image-fidelity JSON receipt.

    Requires exactly one mask source: explicit PNG mask or chroma key.
    No generation model and no inferred/hidden perspective are involved.
    """
    if (mask_path is None) == (key_rgb is None):
        raise ValueError("provide exactly one of mask_path or key_rgb")
    if not 0 < scale <= 16 or scale != scale:
        raise ValueError("scale must be finite and in (0, 16]")
    if x < 0 or y < 0:
        raise ValueError("placement x/y must be nonnegative")
    if not user_intent.strip():
        raise ValueError("user_intent must be nonempty")
    source_path = Path(source_path).resolve()
    background_path = Path(background_path).resolve()
    mask_path = Path(mask_path).resolve() if mask_path is not None else None
    output_dir = Path(output_dir).resolve()
    output_files = [output_dir / n for n in ("cutout.png", "composite.png", "report.json")]
    inputs = {source_path, background_path}
    if mask_path is not None:
        inputs.add(mask_path)
    if inputs.intersection(output_files):
        raise ValueError("output paths must not overwrite source, background, or mask")

    with Image.open(source_path) as opened:
        src = opened.convert("RGBA")
    with Image.open(background_path) as opened:
        bg = opened.convert("RGBA")
    if mask_path is not None:
        with Image.open(mask_path) as opened:
            # An RGBA mask can express opacity through its alpha channel.
            mask = opened.getchannel("A") if "A" in opened.getbands() else opened.convert("L")
        mask_method = "EXPLICIT_MASK"
    else:
        mask = chroma_key_mask(src, key_rgb, key_tolerance)
        mask_method = "KNOWN_BACKGROUND_CHROMA_KEY"
    if mask.size != src.size:
        raise ValueError("mask dimensions must match source image dimensions")
    if mask.getbbox() is None:
        raise ValueError("mask contains no visible subject")

    master = src.copy()
    master.putalpha(ImageChops.multiply(src.getchannel("A"), mask))
    new_size = (max(1, round(src.width * scale)), max(1, round(src.height * scale)))
    if x + new_size[0] > bg.width or y + new_size[1] > bg.height:
        raise ValueError("scaled subject must be entirely inside the destination canvas")
    placed = master if scale == 1.0 else master.resize(new_size, Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    overlay.paste(placed, (x, y))
    composite = Image.alpha_composite(bg, overlay)

    # Pass/fail only on genuinely comparable pixels. Scaling/interpolation and
    # semi-transparent pixels require a different metric, not a false PASS.
    exact = (
        _exact_pixel_check(src, composite, mask, x, y)
        if scale == 1.0 and src.getchannel("A").getextrema() == (255, 255)
        else {
            "status": "NOT_COMPARABLE",
            "reason": "scale changed or original has partial transparency",
            "comparison_scope": "UNSCALED_FULLY_OPAQUE_SOURCE_PIXELS_ONLY",
        }
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    master.save(output_files[0], format="PNG")
    composite.save(output_files[1], format="PNG")
    report: dict[str, Any] = {
        "schema_version": "BRODY_IMAGE_EDIT_REPORT_V0",
        "processing_route": "DETERMINISTIC_2D_COMPOSITE",
        "output_kind": "EDITED_COMPOSITE",
        "source_kind": "USER_SUPPLIED_OR_SYNTHETIC_INPUT_UNKNOWN",
        "produced_media_is_real_observation": False,
        "real_world_proof": False,
        "generator_model": None,
        "learned_visual_model": None,
        "human_intent": user_intent,
        "mask_method": mask_method,
        "key_rgb": list(key_rgb) if key_rgb is not None else None,
        "key_tolerance": key_tolerance if key_rgb is not None else None,
        "input_assets": {
            "source_sha256": file_sha256(source_path),
            "background_sha256": file_sha256(background_path),
            "mask_sha256": file_sha256(mask_path) if mask_path is not None else None,
        },
        "output_assets": {
            "cutout_png": str(output_files[0]),
            "cutout_sha256": file_sha256(output_files[0]),
            "composite_png": str(output_files[1]),
            "composite_sha256": file_sha256(output_files[1]),
        },
        "geometry": {
            "source_size": list(src.size),
            "background_size": list(bg.size),
            "placed_size": list(placed.size),
            "placed_x": x,
            "placed_y": y,
            "scale": scale,
        },
        "mask_statistics": _mask_metrics(mask),
        "visible_rgb_fidelity": exact,
        "verification_limits": [
            "No segmentation model; explicit masks or known-color backgrounds only",
            "No novel viewpoint, 3D reconstruction, illumination matching or image synthesis",
            "Source pixels preserved only where no resampling or alpha mixing occurs",
            "No physical-world understanding or learning from this receipt alone",
        ],
        "experience_validation": "NOT_RUN",
        "memory_write_allowed": False,
        "auto_promotion_allowed": False,
        "readonly": True,
        "decision_authority": "KX108_ONLY",
        "allowed_to_act": False,
        "kernel_mutation": False,
    }
    output_files[2].write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Brody Image I1/R1: deterministic image cutout and transplant")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--background", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    mask = parser.add_mutually_exclusive_group(required=True)
    mask.add_argument("--mask", type=Path, help="grayscale/alpha source-sized mask")
    mask.add_argument("--key-rgb", help="known uniform background RGB, e.g. 20,110,35")
    parser.add_argument("--tolerance", type=int, default=0)
    parser.add_argument("--x", type=int, default=0)
    parser.add_argument("--y", type=int, default=0)
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("--intent", default="Preserve reference subject while changing its background")
    args = parser.parse_args(argv)
    result = run_image_edit(
        args.source, args.background, args.out, mask_path=args.mask,
        key_rgb=parse_rgb(args.key_rgb) if args.key_rgb else None,
        key_tolerance=args.tolerance, x=args.x, y=args.y,
        scale=args.scale, user_intent=args.intent
    )
    print(json.dumps({
        "output": result["output_assets"]["composite_png"],
        "receipt": str(Path(args.out).resolve() / "report.json"),
        "visible_rgb_fidelity": result["visible_rgb_fidelity"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
