import tempfile
import unittest
from pathlib import Path
from brody_world_physique.skill_applicability_review_v1 import run, check

class F1DApplicabilityReviewTests(unittest.TestCase):
    def test_contradiction_triggers_hold_without_erasing_skill(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/"f1d"
            report=run(root)
            self.assertEqual(report["prior_positive_transfers"],2)
            self.assertEqual(report["prior_negative_transfers"],1)
            self.assertEqual(report["retest_holds"],3)
            self.assertEqual(report["retest_coverage"],0.0)
            self.assertTrue(report["original_skill_digest_unchanged"])
            self.assertFalse(report["adaptive_selective_risk_proven"])
            self.assertFalse(report["native_memory_write"])
            self.assertEqual(report["decision_authority"],"KX108_ONLY")
            self.assertTrue(all(x["committed_before_truth"] for x in report["retest"]))
    def test_review_refuses_existing_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/"f1d";root.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):
                run(root)

if __name__=="__main__":unittest.main()
