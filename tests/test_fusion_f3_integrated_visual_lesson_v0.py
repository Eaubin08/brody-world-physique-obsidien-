import json,tempfile,unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.fusion_f3_integrated_visual_lesson_v0 import demo,lesson
class IntegratedLessonTests(unittest.TestCase):
 def test_demo_seals_candidate_and_produces_visible_metrics(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/"lesson";r=demo(root)
   self.assertTrue(r["target_hidden_until_after_candidate_sealed"])
   self.assertEqual(r["boxes"],2)
   self.assertGreater(r["gesture_count"],0)
   self.assertTrue((root/"comparison.png").is_file())
   self.assertTrue((root/"memory.json").is_file())
   self.assertIsInstance(r["candidate_error_px"],int)
   self.assertIsInstance(r["gain_px"],int)
 def test_demo_refuses_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/"lesson";demo(root)
   with self.assertRaises(ValueError):demo(root)
 def test_without_teacher_preserves_unknown(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)
   demo(root/"setup")
   inp=root/"setup-inputs"
   result=lesson(inp/"train.png",inp/"layout.json",root/"unscored")
   self.assertNotIn("candidate_error_px",result)
   self.assertFalse((root/"unscored"/"comparison.png").exists())
if __name__=="__main__":unittest.main()
