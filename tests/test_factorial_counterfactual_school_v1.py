import tempfile
import unittest
from pathlib import Path
from brody_world_physique.factorial_counterfactual_school_v1 import run, effects

class FactorialCounterfactualTests(unittest.TestCase):
    def test_independent_interventions_and_heldout_effects(self):
        with tempfile.TemporaryDirectory() as d:
            result=run(Path(d)/"f1g")
            self.assertEqual(result["training_cases"],8)
            self.assertEqual(result["heldout_cases"],8)
            self.assertEqual(result["training_effects"]["marker_effect_px"],0)
            self.assertEqual(result["test_effects"]["marker_effect_px"],0)
            self.assertEqual(result["training_effects"]["contact_effect_px"],-15)
            self.assertEqual(result["test_effects"]["contact_effect_px"],-15)
            self.assertTrue(result["marker_discarded_as_causal_factor"])
            self.assertTrue(result["contact_unobservable_at_prediction_time"])
            self.assertFalse(result["p149_p150_p152_integrated"])
            self.assertFalse(result["native_memory_write"])
            self.assertEqual(result["decision_authority"],"KX108_ONLY")
    def test_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)/"f1g";folder.mkdir()
            marker=folder/"keep";marker.write_text("original")
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):
                run(folder)
            self.assertEqual(marker.read_text(),"original")
if __name__=="__main__":unittest.main()
