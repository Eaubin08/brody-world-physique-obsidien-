import tempfile
import unittest
from pathlib import Path
from brody_world_physique.experiential_skill_learning_v1 import run, inspect_skill

class ExperientialSkillTests(unittest.TestCase):
    def test_learning_changes_prediction_and_preserves_interference(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"run"
            report=run(root)
            self.assertEqual(len(report["lessons"]),3)
            self.assertTrue(report["interference_kept_skill"])
            self.assertEqual(report["skills_learned_by_error_correction"],2)
            self.assertEqual(len(inspect_skill(root/"candidate_skill.json")["residuals"]),2)
            self.assertTrue(report["train_test_hash_separated"])
            self.assertGreaterEqual(report["positive_transfer_cases"],1)
            self.assertFalse(report["native_memory_write"])
            self.assertFalse(report["canonical_promotion"])
            self.assertEqual(report["decision_authority"],"KX108_ONLY")
            self.assertFalse(report["reverse_360_integrated"])
    def test_immutable_existing_output(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"run";root.mkdir()
            marker=root/"old.txt";marker.write_text("preserved")
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):
                run(root)
            self.assertEqual(marker.read_text(),"preserved")

if __name__=="__main__":unittest.main()
