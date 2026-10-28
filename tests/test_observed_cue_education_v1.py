import tempfile
import unittest
from pathlib import Path
from brody_world_physique.observed_cue_education_v1 import run

class ObservedCueEducationTests(unittest.TestCase):
    def test_cue_is_visible_and_negative_controls_are_reported(self):
        with tempfile.TemporaryDirectory() as d:
            r=run(Path(d)/"f1f")
            self.assertEqual(len(r["lessons"]),4)
            self.assertEqual(len(r["exam"]),4)
            self.assertTrue(r["marker_observed_before_future"])
            self.assertFalse(r["p149_p150_p152_verified_reuse"])
            self.assertFalse(r["real_world_learning_proven"])
            by_case={x["case"]:x for x in r["exam"]}
            self.assertGreater(by_case["new_cue"]["utility_px"],0)
            self.assertGreater(by_case["new_free"]["utility_px"],0)
            self.assertLess(by_case["cue_false_alarm"]["utility_px"],0)
            self.assertLess(by_case["invisible_reversal"]["utility_px"],0)
            self.assertTrue(all(x["candidate_committed_before_truth"] for x in r["exam"]))
            self.assertEqual(r["decision_authority"],"KX108_ONLY")
    def test_preserves_existing_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"f1f";out.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(out)
if __name__=="__main__":unittest.main()
