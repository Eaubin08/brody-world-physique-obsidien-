import tempfile
import unittest
from pathlib import Path
from brody_world_physique import p26_adversarial_pixels_v0 as p


class P26StressTest(unittest.TestCase):
    def test_reproducible_pixel_stress_and_sealed_scoring(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"run"
            report=p.run(out,24)
            self.assertEqual(report["count"],24)
            self.assertEqual(report["test_count"],18)
            self.assertEqual(len(report["rows"]),24)
            self.assertTrue((out/"images"/"sample_pairs.png").exists())
            self.assertTrue((out/"predictions_pre_scoring.jsonl").exists())
            self.assertTrue(p.verify(out)["verified"])
            self.assertFalse(report["learned"])

    def test_modified_receipt_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"run"
            p.run(out,20)
            with (out/"predictions_pre_scoring.jsonl").open("a") as f:
                f.write("tampered")
            with self.assertRaises(ValueError):
                p.verify(out)

    def test_invalid_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                p.run(Path(tmp)/"bad",4)


if __name__=="__main__":
    unittest.main()
