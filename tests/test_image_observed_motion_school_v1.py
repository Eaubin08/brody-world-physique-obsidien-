import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_observed_motion_school_v1 import run
class MotionSchoolTests(unittest.TestCase):
 def scene(self,path,y):
  im=Image.new("RGB",(64,64),"white")
  ImageDraw.Draw(im).ellipse((25,y-4,33,y+4),fill="black")
  im.save(path)
 def test_observed_acceleration_and_reconstruction(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);sequence=[]
   for i,y in enumerate((10,14,20)):
    file=root/f"frame{i}.png";self.scene(file,y)
    sequence.append({"t":i,"file":str(file)})
   manifest=root/"lesson.json";manifest.write_text(json.dumps({"observations":sequence,"predict_t":3}))
   result=run(manifest,root/"result")
   self.assertEqual(result["frames"],3)
   self.assertAlmostEqual(result["predicted_y"],28,delta=1.2)
   self.assertTrue((root/"result"/"predicted_next.png").exists())
   self.assertFalse(result["correction_applied"])
 def test_explicit_feedback_refit(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);sequence=[]
   for i,y in enumerate((10,14,20)):
    file=root/f"frame{i}.png";self.scene(file,y)
    sequence.append({"t":i,"file":str(file)})
   next_frame=root/"feedback.png";self.scene(next_frame,32)
   manifest=root/"lesson.json";manifest.write_text(json.dumps({"observations":sequence,"predict_t":3}))
   result=run(manifest,root/"result",next_frame)
   self.assertTrue(result["correction_applied"])
   self.assertGreater(result["feedback"]["error_px"],0)
   self.assertTrue(result["feedback"]["corrected_fitted_model"])
 def test_fail_closed_duplicate_feedback(self):
  with tempfile.TemporaryDirectory() as folder:
   root=Path(folder);sequence=[]
   for i,y in enumerate((10,14,20)):
    file=root/f"frame{i}.png";self.scene(file,y)
    sequence.append({"t":i,"file":str(file)})
   manifest=root/"lesson.json";manifest.write_text(json.dumps({"observations":sequence,"predict_t":3}))
   with self.assertRaises(ValueError):run(manifest,root/"result",root/"frame0.png")
   self.assertFalse((root/"result").exists())
if __name__=="__main__":unittest.main()
