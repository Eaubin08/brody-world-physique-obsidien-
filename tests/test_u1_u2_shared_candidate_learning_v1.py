import tempfile,unittest
from pathlib import Path
from brody_world_physique.u1_u2_shared_candidate_learning_v1 import run

class SharedCandidateLearningTests(unittest.TestCase):
    def test_real_probe_changes_candidate_future_and_retains_clean(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"u12";r=run(root)
            self.assertEqual(r["probe_decision"],"PROBE")
            self.assertTrue(r["state_changed"])
            self.assertFalse(r["global_correction_accepted"])
            scores={s["case"]:s for s in r["cases"]}
            self.assertLess(scores["known_probe"]["corrected_error"],scores["known_probe"]["baseline_error"])
            self.assertLessEqual(scores["retention_clean"]["corrected_error"],scores["retention_clean"]["baseline_error"])
            self.assertTrue((root/"STATE_BEFORE.json").exists())
            self.assertTrue((root/"STATE_AFTER.json").exists())
            self.assertTrue((root/"U2_PROBE_PRECOMMIT.json").exists())
            self.assertFalse(r["native_memory_write"])
            self.assertEqual(r["decision_authority"],"KX108_ONLY")
    def test_prior_results_immutable(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"prior";root.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(root)
if __name__=="__main__":unittest.main()
