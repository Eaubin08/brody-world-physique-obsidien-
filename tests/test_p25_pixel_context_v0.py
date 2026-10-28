"""P2.5 image-derived measurements: same apparent ball, differing context."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from brody_world_physique import p25_pixel_context_v0 as p


class P25PixelContextTest(unittest.TestCase):
    def test_pixel_scenarios(self):
        with tempfile.TemporaryDirectory() as root:
            report=p.run(Path(root)/"case")
            rows={item["case"]:item for item in report["per_case"]}
            self.assertTrue(report["raw_pixels_tested"])
            self.assertFalse(report["learned_vision"])
            self.assertEqual(len(rows),5)
            self.assertTrue(all(row["object_only"]==10.0 for row in rows.values()))
            self.assertEqual(rows["object_only"]["contextual"],10.0)
            self.assertEqual(rows["camera_only"]["contextual"],0.0)
            self.assertEqual(rows["both"]["contextual"],6.0)
            self.assertEqual(rows["one_corrupt_landmark"]["contextual"],6.0)
            self.assertIsNone(rows["three_corrupt_landmarks"]["contextual"])
            self.assertEqual(p.verify(Path(root)/"case")["verified"],True)

    def test_reject_tampered_report(self):
        with tempfile.TemporaryDirectory() as root:
            out=Path(root)/"run"
            p.run(out)
            (out/"evaluation.json").write_text('{"fake":true}',encoding="utf-8")
            with self.assertRaises(ValueError):
                p.verify(out)


if __name__=="__main__":
    unittest.main()
