import tempfile
import unittest
from pathlib import Path
from brody_world_physique.f1b_physical_memory_bridge_v1 import run

class F1BTests(unittest.TestCase):
    def test_training_and_blind_pair(self):
        with tempfile.TemporaryDirectory() as d:
            report=run(Path(d)/"experiment")
            self.assertEqual(len(report["train"]),2)
            self.assertEqual(report["train"][-1]["experiences"],2)
            self.assertTrue(report["sealed_forecasts_unchanged"])
            self.assertFalse(report["unified_education_e2e"])
            self.assertFalse(report["p156_memory_connected"])
            self.assertFalse(report["native_memory_write"])
            self.assertEqual(report["decision_authority"],"KX108_ONLY")
            self.assertTrue(report["paired_errors_with_memory_px"])
    def test_preserve_existing_run(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"run";out.mkdir()
            marker=out/"proof.json";marker.write_text("untouched")
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):
                run(out)
            self.assertEqual(marker.read_text(),"untouched")

if __name__=="__main__":unittest.main()
