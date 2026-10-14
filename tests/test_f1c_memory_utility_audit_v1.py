import tempfile
import unittest
from pathlib import Path
from brody_world_physique.f1c_memory_utility_audit_v1 import run, TEST

class F1CMemoryUtilityTests(unittest.TestCase):
    def test_paired_scoring_without_forced_improvement(self):
        with tempfile.TemporaryDirectory() as temp:
            report=run(Path(temp)/"audit")
            self.assertEqual(report["paired_cases"],len(TEST))
            self.assertEqual(report["comparable_cases"],len(TEST))
            self.assertEqual(report["improved_cases"]+report["degraded_cases"]+
                             report["unchanged_cases"],len(TEST))
            self.assertTrue(report["all_forecasts_sealed"])
            self.assertTrue(report["source_hash_separation_checked"])
            self.assertFalse(report["physics_discovery_proven"])
            self.assertFalse(report["native_memory_write"])
            self.assertEqual(report["decision_authority"],"KX108_ONLY")
    def test_no_overwrite_after_success(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"audit"
            run(out)
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):
                run(out)
if __name__=="__main__":
    unittest.main()
