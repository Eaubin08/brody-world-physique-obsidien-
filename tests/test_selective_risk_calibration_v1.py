import tempfile
import unittest
from pathlib import Path
from brody_world_physique.selective_risk_calibration_v1 import run, CALIBRATE, TEST

class SelectiveRiskTests(unittest.TestCase):
    def test_calibration_separate_from_blind_exam(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"audit"
            report=run(root)
            self.assertEqual(len(report["calibration"]),len(CALIBRATE))
            self.assertEqual(len(report["exam"]),len(TEST))
            self.assertTrue(all(e["committed_before_feedback"] for e in report["exam"]))
            self.assertGreater(report["policy"]["calibration_max_error_px"],2.0)
            self.assertFalse(report["policy"]["selection_allowed"])
            self.assertEqual(report["coverage"],0.0)
            self.assertIsNone(report["selective_mean_error_px"])
            self.assertFalse(report["calibration_guarantee"])
            self.assertFalse(report["native_memory_write"])
            self.assertEqual(report["decision_authority"],"KX108_ONLY")
    def test_prior_outputs_remain_intact(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"audit";root.mkdir()
            mark=root/"proof.txt";mark.write_text("preserved")
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):
                run(root)
            self.assertEqual(mark.read_text(),"preserved")

if __name__=="__main__":unittest.main()
