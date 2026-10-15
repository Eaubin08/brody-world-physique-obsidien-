import tempfile,unittest,json
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_background_adaptation_p146 import robust_features,run
class BackgroundAdaptationTests(unittest.TestCase):
 def test_foreground_descriptor_dark_and_light(self):
  light=Image.new("RGB",(96,96),"white")
  dark=Image.new("RGB",(96,96),(55,59,69))
  for image in (light,dark):
   ImageDraw.Draw(image).rectangle((22,31,67,48),fill=(230,40,45))
  a=robust_features(light,"orientation")
  b=robust_features(dark,"orientation")
  self.assertAlmostEqual(a[0],b[0],places=4)
 def test_sealed_exams_with_baselines_and_retention(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/"p146";report=run(out,minutes=2,train_each=30,adapt_each=10,exam_each=20)
   self.assertEqual(report["exam_cases"],500)
   self.assertEqual(report["cells_completed"],25)
   self.assertEqual(report["adaptation_examples"],200)
   self.assertIn("reference",report["world_stats"])
   self.assertIn("new_engine_dark",report["world_stats"])
   self.assertFalse(report["independent_real_sources"])
   seal=json.loads((out/"SEALED_ADAPTATION.json").read_text())
   self.assertFalse(seal["exam_feedback_used_in_memory"])
   with self.assertRaises(ValueError):run(out,minutes=2,train_each=30,adapt_each=10,exam_each=20)
if __name__=="__main__":unittest.main()
