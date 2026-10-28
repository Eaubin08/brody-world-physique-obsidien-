import tempfile
import unittest
from pathlib import Path
from brody_world_physique.integrated_education_v0 import run

class IntegratedEducationV0Tests(unittest.TestCase):
    def test_connected_experience_and_candidate_only(self):
        with tempfile.TemporaryDirectory() as d:
            result=run(Path(d)/"school")
            self.assertEqual(len(result["curriculum"]),3)
            self.assertEqual(len(result["exams"]),2)
            self.assertTrue(result["checkpoint_restore_verified"])
            self.assertTrue(result["same_experience_perception_prediction_render_comparison"])
            self.assertFalse(result["education_integrated_full"])
            self.assertFalse(result["learned_physical_law_proven"])
            self.assertFalse(result["native_memory_write"])
            self.assertEqual(result["decision_authority"],"KX108_ONLY")
            for row in result["exams"]:
                self.assertFalse(row["exam_feedback_reused_for_training"])
                self.assertTrue(row["baseline_visual_roundtrip"])
                self.assertTrue(row["learned_visual_roundtrip"])

    def test_does_not_overwrite_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/"school"
            out.mkdir()
            p=out/"proof";p.write_text("keep",encoding="utf8")
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):
                run(out)
            self.assertEqual(p.read_text(encoding="utf8"),"keep")
if __name__=="__main__":unittest.main()
