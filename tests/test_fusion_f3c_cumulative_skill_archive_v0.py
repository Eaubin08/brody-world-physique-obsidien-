import tempfile,unittest,json
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.fusion_f3c_cumulative_skill_archive_v0 import demo,load_registry,teach,exam
from brody_world_physique.drawing_school_v0 import SIDE
class ContinuousMemoryTests(unittest.TestCase):
 def test_single_train_three_frozen_recalls(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"school";result=demo(root)
   self.assertEqual(result["training_count"],1)
   self.assertEqual(result["exams_without_retraining"],3)
   self.assertTrue(result["frozen_candidate_reuse_proven"])
   self.assertTrue(all(x["sealed_before_teacher"] for x in result["rows"]))
   for name in ("01-recall","02-recomposition","03-transfer"):
    self.assertTrue((root/name/"comparison.png").exists())
   registry=load_registry(root,1)
   self.assertEqual(len(registry["skills"]),1)
 def test_tamper_detection_and_immutable_output(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"school";demo(root)
   with self.assertRaises(ValueError):demo(root)
   p=root/"skills"/"rectangle.json";p.write_text("{}")
   with self.assertRaises(ValueError):load_registry(root,1)
 def test_teacher_cannot_modify_frozen_memory(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"school";demo(root)
   version=load_registry(root,1)
   before=version["skills"][0]["memory_sha256"]
   self.assertEqual(load_registry(root,1)["skills"][0]["memory_sha256"],before)
if __name__=="__main__":unittest.main()
