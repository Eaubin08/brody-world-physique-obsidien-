import tempfile
import unittest
from pathlib import Path
from brody_world_physique.f1h_historical_reconciliation_v1 import run

class HistoricalReuseTests(unittest.TestCase):
    def test_real_p149_p150_p152_integrations(self):
        with tempfile.TemporaryDirectory() as d:
            result=run(Path(d)/"f1h")
            self.assertEqual(result["cases"],12)
            self.assertTrue(result["counterfactual"]["same_final_pixels"])
            self.assertTrue(result["counterfactual"]["different_histories"])
            self.assertEqual({r["module"] for r in result["exams"]},{"P149","P150","P152"})
            self.assertFalse(result["single_shared_skill_state"])
            self.assertFalse(result["native_memory_write"])
            self.assertEqual(result["decision_authority"],"KX108_ONLY")
    def test_preserve_existing(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"f1h";root.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(root)

if __name__=="__main__":unittest.main()
