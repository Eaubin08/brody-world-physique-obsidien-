import tempfile,unittest
from pathlib import Path
from brody_world_physique.u3_u4_visual_context_shared_v1 import run

class PixelContextSharedMemoryTests(unittest.TestCase):
    def test_pixel_context_drives_shared_prediction_and_image(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"run";r=run(out)
            rows={v["name"]:v for v in r["exams"]}
            self.assertEqual(rows["slope_new"]["inferred_context"],"intervention")
            self.assertLess(rows["slope_new"]["candidate_error"],rows["slope_new"]["baseline_error"])
            self.assertEqual(rows["clean_new"]["inferred_context"],"clean")
            self.assertEqual(rows["clean_new"]["candidate_error"],0.)
            self.assertIsNone(rows["unknown_new"]["inferred_context"])
            self.assertFalse(rows["unknown_new"]["candidate_image_generated"])
            self.assertFalse(r["global_correction_accepted"])
            self.assertTrue(r["same_candidate_for_forecast_and_raster"])
            self.assertFalse(r["native_memory_write"])
            self.assertTrue((out/"slope_new_predicted.png").exists())
            self.assertTrue((out/"MEMORY_CANDIDATE.json").exists())
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"existing";out.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(out)
if __name__=="__main__":unittest.main()
