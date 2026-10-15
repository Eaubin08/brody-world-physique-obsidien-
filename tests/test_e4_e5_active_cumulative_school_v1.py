import tempfile
import unittest
from pathlib import Path
from brody_world_physique.e4_e5_active_cumulative_school_v1 import run

class ActiveCumulativeSchoolTests(unittest.TestCase):
    def test_probe_selection_and_cumulative_replay(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"e4e5";r=run(out)
            rows={v["case"]:v for v in r["E4"]["exams"]}
            self.assertEqual(len(rows),5)
            self.assertEqual(rows["no_discriminator"]["chosen"],"HOLD")
            self.assertEqual(rows["hidden_novel"]["chosen"],"PROBE")
            self.assertEqual(rows["hidden_novel"]["outcome"]["decision"],"HOLD")
            self.assertTrue(r["E4"]["choice_committed_before_probe_result"])
            self.assertTrue(r["E5"]["full_curriculum_completed"])
            self.assertGreater(r["E5"]["exam_cases"],0)
            self.assertFalse(r["E5"]["real_image_skill_memory_shared_with_E1"])
            self.assertFalse(r["E2E3_FUTURE_GENERATOR_POLICY_CONNECTED"])
            self.assertFalse(r["native_memory_write"])
            self.assertEqual(r["decision_authority"],"KX108_ONLY")
    def test_preserves_existing_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/"already";target.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(target)
if __name__=="__main__":unittest.main()
