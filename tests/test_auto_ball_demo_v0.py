"""Bounded ball detection, simulated provenance, and heldout sequencing."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from PIL import Image, ImageDraw

from brody_world_physique.auto_ball_demo_v0 import (
    KNOWN_TEST_VIDEO_SHA256,
    detect_orange_ball,
    evaluate_known_demo_frames,
)


def make_frame(center_x: int, center_y: int, *, orange: bool = True) -> Image.Image:
    canvas = Image.new("RGB", (160, 120), (35, 44, 40))
    draw = ImageDraw.Draw(canvas)
    if orange:
        draw.ellipse(
            (center_x-15, center_y-15, center_x+15, center_y+15),
            fill=(255, 153, 91),
        )
    return canvas


class BallDemonstrationTests(TestCase):
    def test_color_object_detected_as_pixel_location_only(self):
        found = detect_orange_ball(make_frame(40, 50))
        self.assertAlmostEqual(found.center_x, 40.5)
        self.assertAlmostEqual(found.center_y, 50.5)
        self.assertEqual(found.method, "DEMO_ORANGE_HSV_THRESHOLD_NOT_GENERAL_SEGMENTATION")
        self.assertFalse(found.confidence_calibrated)
        self.assertGreater(found.orange_pixels, 100)

    def test_target_absent_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "target absent"):
            detect_orange_ball(make_frame(50, 50, orange=False))

    def test_unbounded_or_too_elongated_colored_area_rejected(self):
        image = Image.new("RGB", (180, 100), (20, 28, 25))
        ImageDraw.Draw(image).rectangle((10, 10, 140, 20), fill=(255, 153, 91))
        with self.assertRaisesRegex(ValueError, "ball-shaped"):
            detect_orange_ball(image)

    def test_precommit_before_reading_fourth_frame(self):
        positions={0:(30,35),3:(40,39),6:(50,47),9:(60,59)}
        calls=[]
        with TemporaryDirectory() as temp:
            folder=Path(temp)/"run"

            def fetch(index):
                calls.append(index)
                if index == 9:
                    receipt = folder/"prediction_before_frame_4.json"
                    self.assertTrue(receipt.is_file(), "Fourth frame must not be read before forecast")
                    data=json.loads(receipt.read_text())
                    self.assertEqual(len(data["history_source_refs"]),3)
                    self.assertEqual(data["source_kind"],"SIMULATED")
                    self.assertFalse(data["physical_law_proven"])
                return make_frame(*positions[index])

            result=evaluate_known_demo_frames(
                fetch,
                source_sha256=KNOWN_TEST_VIDEO_SHA256,
                fps=30.0,
                frame_indices=(0,3,6,9),
                out_dir=folder,
            )
            self.assertEqual(calls,[0,3,6,9])
            self.assertEqual(result["comparison"],"BETTER_THAN_LINEAR_BASELINE")
            self.assertLess(result["error"]["proposed"],2.0)
            self.assertFalse(result["physics_understood"])
            manifest=json.loads((folder/"evaluation.json").read_text())
            self.assertEqual(manifest["source_kind"],"SIMULATED")
            self.assertTrue(manifest["forecast_precommitted_before_heldout_detection"])
            self.assertFalse(manifest["world_knowledge_validated"])
            self.assertFalse(manifest["memory_write_allowed"])
            self.assertEqual(len(manifest["observations"]),4)
            self.assertTrue(all(x["source_kind"]=="SIMULATED" for x in manifest["observations"]))

    def test_reject_unapproved_sources_and_frame_selection(self):
        def no_read(_):
            self.fail("No frame can be accessed on rejected source")
        with TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
                evaluate_known_demo_frames(
                    no_read, source_sha256="0"*64,
                    fps=30,frame_indices=(0,3,6,9),out_dir=temp
                )
            with self.assertRaisesRegex(ValueError,"sampling"):
                evaluate_known_demo_frames(
                    no_read, source_sha256=KNOWN_TEST_VIDEO_SHA256,
                    fps=24,frame_indices=(0,3,6,9),out_dir=temp
                )

    def test_existing_results_cannot_be_silently_overwritten(self):
        with TemporaryDirectory() as temp:
            folder=Path(temp)/"out";folder.mkdir()
            (folder/"evaluation.json").write_text("keep evidence")
            with self.assertRaisesRegex(ValueError,"fresh output"):
                evaluate_known_demo_frames(
                    lambda i: self.fail("Do not read unneeded future frame"),
                    source_sha256=KNOWN_TEST_VIDEO_SHA256,
                    fps=30,frame_indices=(0,3,6,9),out_dir=folder,
                )
