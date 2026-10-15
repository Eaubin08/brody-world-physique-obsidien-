"""P2.8b regression: actual render/detect, delayed truth, and reproducibility."""
import tempfile
import unittest
from pathlib import Path

from brody_world_physique import p28b_pixel_reversal_v0 as p


class P28bPixelReversal(unittest.TestCase):
    def test_detected_pixels_not_simulator_shift_api(self):
        spec = p.fixture(2)
        obs, status = p.observe(spec)
        self.assertEqual(status, "MEASURED_PIXELS")
        self.assertEqual(len(obs["shifts"]), 5)
        self.assertNotIn("world", obs)
        self.assertNotIn("camera", obs)
        self.assertNotIn("anchor", obs)
        self.assertAlmostEqual(obs["shifts"][spec["anchor"]], spec["camera"], delta=2)

    def test_reliable_anchor_moves(self):
        self.assertEqual((p.fixture(0)["anchor"], p.fixture(40)["anchor"],
                          p.fixture(90)["anchor"]), (4, 0, 2))

    def test_no_verdict_or_memory_mutation(self):
        report = p.execute(100, 2)
        self.assertFalse(report["native_memory_write"])
        self.assertFalse(report["b8_promotion"])
        self.assertEqual(report["decision_authority"], "KX108_ONLY")
        self.assertTrue(all(not r["prediction"]["memory_write"]
                            for r in report["prediction_receipts"]))

    def test_hold_on_missing_object(self):
        spec = p.fixture(17)
        self.assertTrue(spec["occluded"])
        obs, status = p.observe(spec)
        self.assertIsNone(obs)
        self.assertEqual(status, "HOLD_OBJECT")

    def test_replay_and_tamper(self):
        with tempfile.TemporaryDirectory() as root:
            out = Path(root) / "b"
            p.run(out, 100, 2)
            self.assertTrue(p.verify(out)["verified"])
            with (out / "predictions_pre_feedback.json").open("ab") as f:
                f.write(b"corrupt")
            with self.assertRaises(ValueError):
                p.verify(out)


if __name__ == "__main__":
    unittest.main()
