"""Reproducible SYNTHETIC fixture for Brody Image I1/R1 (not a real observation).

Run from the repository root:
    python -m examples.demo_image_v0 --out build/brody-image-demo
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

from brody_world_physique.image_v0 import run_image_edit


def demo(output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    source = output / "fixture_source.png"
    background = output / "fixture_background.png"

    # Synthetic toy portrait: unique known green background allows an honest
    # COLOR-KEY experiment. This is not evidence of general image segmentation.
    key = (19, 107, 46)
    subject = Image.new("RGB", (160, 130), key)
    draw = ImageDraw.Draw(subject)
    draw.rectangle((50, 55, 110, 115), fill=(198, 52, 43), outline=(53, 35, 31), width=3)
    draw.ellipse((42, 8, 118, 74), fill=(231, 188, 130), outline=(58, 42, 37), width=3)
    draw.ellipse((59, 32, 70, 43), fill=(40, 40, 43))
    draw.ellipse((91, 32, 102, 43), fill=(40, 40, 43))
    draw.arc((65, 43, 95, 63), 5, 175, fill=(100, 41, 37), width=3)
    draw.line((80, 9, 80, 0), fill=(50, 35, 29), width=4)
    draw.ellipse((75, 0, 85, 10), fill=(244, 225, 89))
    draw.rectangle((52, 116, 65, 127), fill=(75, 73, 78))
    draw.rectangle((94, 116, 107, 127), fill=(75, 73, 78))
    subject.save(source)

    target = Image.new("RGB", (380, 240), (183, 217, 246))
    pen = ImageDraw.Draw(target)
    pen.rectangle((0, 170, 380, 240), fill=(187, 177, 157))
    for gx in range(0, 380, 40):
        pen.line((gx, 170, gx + 45, 240), fill=(169, 157, 137), width=1)
    pen.ellipse((290, 22, 340, 72), fill=(255, 235, 154))
    pen.rectangle((15, 66, 91, 173), fill=(98, 144, 169), outline=(50, 95, 125), width=3)
    target.save(background)

    result = run_image_edit(
        source, background, output / "result",
        key_rgb=key, x=115, y=40, scale=1.0,
        user_intent="Keep every fully opaque source pixel; place the synthetic toy in a new scene.",
    )
    if result["visible_rgb_fidelity"]["status"] != "PASS":
        raise AssertionError("The deterministic demo failed its exact-pixel control")

    comparison = Image.new("RGB", (3 * 380, 270), "white")
    for i, image_path in enumerate((source, background, output / "result/composite.png")):
        with Image.open(image_path) as current:
            image = current.convert("RGB")
            comparison.paste(image, (i * 380 + 10, 20))
    comparison.save(output / "comparison.png", format="PNG")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=Path("build/brody-image-demo"))
    args = parser.parse_args()
    report = demo(args.out)
    print("fixture=SYNTHETIC, comparison_png=" + str(args.out / "comparison.png"))
    print("pixel_fidelity=" + report["visible_rgb_fidelity"]["status"])
    print("pixel_count=" + str(report["visible_rgb_fidelity"]["fully_opaque_pixels_compared"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
