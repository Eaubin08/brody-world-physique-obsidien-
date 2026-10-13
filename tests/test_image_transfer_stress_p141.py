import json,tempfile,unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.image_transfer_stress_p141 import run,shift_image,SHIFTS,centroid_predict,majority
class TransferStressTests(unittest.TestCase):
 def test_cross_condition_matrix_and_baselines(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"trial"
   result=run(p,minutes=2,train_per_family=30,exam_per_cell=20)
   self.assertEqual(result["exam_cases"],600)
   self.assertEqual(result["cells_completed"],30)
   self.assertEqual(result["cells_expected"],30)
   self.assertEqual(set(result["global_accuracy"]),{"knn","centroid","majority"})
   self.assertTrue(result["exam_feedback_used_in_learning"] is False)
   detail=json.loads((p/"CELL_REPORT.json").read_text())
   self.assertEqual(detail["colour/greyscale"]["n"],20)
 def test_shift_is_not_identity_and_no_overwrite(self):
  im=Image.new("RGB",(12,12),(230,50,20))
  self.assertNotEqual(shift_image(im,"greyscale").getpixel((4,4)),im.getpixel((4,4)))
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"trial";run(p,minutes=2,train_per_family=30,exam_per_cell=20)
   with self.assertRaises(ValueError):run(p,minutes=2,train_per_family=30,exam_per_cell=20)
if __name__=="__main__":unittest.main()
