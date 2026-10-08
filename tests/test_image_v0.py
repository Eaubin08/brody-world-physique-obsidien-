"""CPU tests for the image-editing I1/R1 baseline. Fixtures are synthetic."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from PIL import Image

from brody_world_physique.image_v0 import (
    chroma_key_mask,
    parse_rgb,
    run_image_edit,
)


class ImageR1Tests(TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source.png"
        self.background = self.root / "background.png"
        self.mask = self.root / "mask.png"
        src = Image.new("RGB", (6, 5), (0, 255, 0))
        for x in range(2, 5):
            for y in range(1, 4):
                src.putpixel((x, y), (210, x * 11, y * 17))
        src.save(self.source)
        Image.new("RGB", (18, 14), (70, 85, 120)).save(self.background)
        mask = Image.new("L", src.size, 0)
        for x in range(2, 5):
            for y in range(1, 4):
                mask.putpixel((x, y), 255)
        mask.save(self.mask)

    def test_strict_source_preserved_with_known_background_color(self):
        out = self.root / "out"
        result = run_image_edit(
            self.source, self.background, out, key_rgb=(0, 255, 0), x=4, y=3
        )
        self.assertEqual(result["visible_rgb_fidelity"]["status"], "PASS")
        self.assertEqual(result["visible_rgb_fidelity"]["rgb_mismatched_pixels"], 0)
        self.assertEqual(result["visible_rgb_fidelity"]["fully_opaque_pixels_compared"], 9)
        self.assertEqual(result["mask_statistics"]["pixels_fully_opaque"], 9)
        self.assertEqual(result["mask_method"], "KNOWN_BACKGROUND_CHROMA_KEY")
        self.assertTrue((out / "cutout.png").is_file())
        self.assertTrue((out / "composite.png").is_file())
        self.assertTrue((out / "report.json").is_file())
        with Image.open(out / "cutout.png") as cutout:
            self.assertEqual(cutout.getpixel((0, 0))[3], 0)
            self.assertEqual(cutout.getpixel((3, 2)), (210, 33, 34, 255))
        with Image.open(out / "composite.png") as composed:
            self.assertEqual(composed.getpixel((0, 0))[:3], (70, 85, 120))
            self.assertEqual(composed.getpixel((7, 5))[:3], (210, 33, 34))
        saved = json.loads((out / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["output_kind"], "EDITED_COMPOSITE")
        self.assertEqual(saved["generator_model"], None)
        self.assertFalse(saved["produced_media_is_real_observation"])
        self.assertFalse(saved["memory_write_allowed"])
        self.assertFalse(saved["auto_promotion_allowed"])
        self.assertEqual(saved["decision_authority"], "KX108_ONLY")

    def test_explicit_grayscale_mask(self):
        result = run_image_edit(
            self.source, self.background, self.root / "maskout", mask_path=self.mask, x=2, y=1
        )
        self.assertEqual(result["mask_method"], "EXPLICIT_MASK")
        self.assertEqual(result["visible_rgb_fidelity"]["status"], "PASS")

    def test_scale_disables_noncomparable_pixel_identity_claim(self):
        result = run_image_edit(
            self.source, self.background, self.root / "scale", mask_path=self.mask,
            scale=2, x=1, y=1
        )
        self.assertEqual(result["visible_rgb_fidelity"]["status"], "NOT_COMPARABLE")
        self.assertEqual(result["geometry"]["placed_size"], [12, 10])

    def test_soft_alpha_mask_is_preserved_without_false_pixel_claim(self):
        with Image.open(self.mask) as opened:
            mask = opened.copy()
        mask.putpixel((3, 2), 127)
        mask.save(self.mask)
        result = run_image_edit(
            self.source, self.background, self.root / "alpha", mask_path=self.mask
        )
        self.assertEqual(result["mask_statistics"]["pixels_partially_transparent"], 1)
        self.assertEqual(result["visible_rgb_fidelity"]["status"], "PASS")
        self.assertEqual(result["visible_rgb_fidelity"]["fully_opaque_pixels_compared"], 8)
        with Image.open(self.root / "alpha" / "cutout.png") as image:
            self.assertEqual(image.getpixel((3, 2))[3], 127)

    def test_mismatched_mask_size_fails_closed(self):
        Image.new("L", (5, 5), 255).save(self.mask)
        with self.assertRaisesRegex(ValueError, "mask dimensions"):
            run_image_edit(self.source, self.background, self.root / "bad", mask_path=self.mask)

    def test_no_mask_or_both_mask_routes_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            run_image_edit(self.source, self.background, self.root / "no")
        with self.assertRaisesRegex(ValueError, "exactly one"):
            run_image_edit(
                self.source, self.background, self.root / "both",
                mask_path=self.mask, key_rgb=(0, 255, 0),
            )

    def test_overflowing_placement_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "entirely inside"):
            run_image_edit(
                self.source, self.background, self.root / "bad",
                mask_path=self.mask, x=16, y=3,
            )

    def test_empty_subject_rejected(self):
        Image.new("L", (6, 5), 0).save(self.mask)
        with self.assertRaisesRegex(ValueError, "no visible subject"):
            run_image_edit(self.source, self.background, self.root / "bad", mask_path=self.mask)

    def test_output_cannot_overwrite_source(self):
        self.source.rename(self.root / "cutout.png")
        with self.assertRaisesRegex(ValueError, "must not overwrite"):
            run_image_edit(
                self.root / "cutout.png", self.background, self.root,
                mask_path=self.mask
            )

    def test_input_hashes_stay_stable_and_deterministic_output(self):
        a = run_image_edit(self.source, self.background, self.root / "one", mask_path=self.mask)
        b = run_image_edit(self.source, self.background, self.root / "two", mask_path=self.mask)
        self.assertEqual(a["input_assets"]["source_sha256"], b["input_assets"]["source_sha256"])
        self.assertEqual(a["output_assets"]["composite_sha256"], b["output_assets"]["composite_sha256"])
        self.assertEqual(a["output_assets"]["cutout_sha256"], b["output_assets"]["cutout_sha256"])

    def test_parse_rgb_and_key_mask(self):
        self.assertEqual(parse_rgb(" 20, 110,35 "), (20, 110, 35))
        for invalid in ("a,b,c", "1,2", "300,0,0"):
            with self.assertRaises(ValueError):
                parse_rgb(invalid)
        with self.assertRaises(ValueError):
            chroma_key_mask(Image.new("RGB", (1, 1)), (0, 0, 0), 256)
