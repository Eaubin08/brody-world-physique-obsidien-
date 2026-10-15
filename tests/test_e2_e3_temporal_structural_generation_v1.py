import tempfile
import unittest
from pathlib import Path
from brody_world_physique.e2_e3_temporal_structural_generation_v1 import run

class TemporalGenerationTests(unittest.TestCase):
    def test_future_image_is_generated_before_heldout_grading(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"e2e3";r=run(root)
            cases={v["case"]:v for v in r["exam"]}
            self.assertEqual(len(cases),3)
            self.assertEqual(cases["regular_A"]["status"],"CANDIDATE")
            self.assertLess(cases["regular_A"]["candidate_mae"],cases["regular_A"]["static_mae"])
            self.assertEqual(cases["regular_A"]["reconstructed_parts"],1)
            self.assertTrue(cases["hidden_reversal"]["candidate_mae"]>0)
            self.assertTrue(r["counterfactual"]["same_final_pixels"])
            self.assertTrue(r["counterfactual"]["different_histories"])
            self.assertFalse(r["target_geometry_passed_to_generator"])
            self.assertFalse(r["target_pixels_passed_to_generator"])
            self.assertFalse(r["physical_understanding_proven"])
            for name in cases:
                self.assertTrue((root/name/"PRECOMMIT.json").exists())
                self.assertTrue((root/name/"generated_future.png").exists())
    def test_never_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"e2e3";root.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(root)

if __name__=="__main__":unittest.main()
