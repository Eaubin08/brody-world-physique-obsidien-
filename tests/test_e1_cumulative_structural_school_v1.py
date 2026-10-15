import tempfile
import unittest
from pathlib import Path
from brody_world_physique.e1_cumulative_structural_school_v1 import run

class CumulativeStructuralSchoolTests(unittest.TestCase):
    def test_acquisition_retention_transfer_and_novel_hold(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"e1";r=run(out)
            self.assertEqual(r["before"]["mode"],"CANDIDATE")
            self.assertTrue(r["retained_after_interference"])
            self.assertEqual(r["circle_transfer"]["mode"],"CANDIDATE")
            self.assertEqual(r["novel"]["mode"],"DOUBT")
            self.assertEqual(r["before"]["mae_rgb"],r["after"]["mae_rgb"])
            self.assertEqual(len(r["lessons"]),4)
            self.assertTrue(r["exam_observation_supplies_geometry_and_shape_signature"])
            self.assertFalse(r["pure_blind_generation_proven"])
            self.assertFalse(r["native_memory_write"])
            self.assertEqual(r["decision_authority"],"KX108_ONLY")
            for name in ("square_before","square_after","circle_new","novel_triangle"):
                self.assertTrue((out/(name+"_pre_feedback.json")).exists())
    def test_preserve_prior_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"e1";out.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(out)

if __name__=="__main__":unittest.main()
