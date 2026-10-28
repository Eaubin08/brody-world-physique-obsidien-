import tempfile,unittest,json,random
from pathlib import Path
from brody_world_physique.image_cross_renderer_world_p145 import run,alternative_scene,WORLD_TYPES
class CrossRendererTests(unittest.TestCase):
 def test_new_worlds_produce_different_pixels(self):
  a=random.Random(17);b=random.Random(17)
  x,_=alternative_scene(a,"shape","new_engine_light")
  y,_=alternative_scene(b,"shape","new_engine_dark")
  self.assertNotEqual(x.getpixel((0,0)),y.getpixel((0,0)))
  x.close();y.close()
 def test_sealed_cross_world_matrix(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/"trial"
   report=run(path,minutes=2,train_each=30,validation_each=20,exam_each=20)
   self.assertEqual(report["cases"],500)
   self.assertEqual(report["cells_completed"],25)
   self.assertEqual(len(report["world_scores"]),len(WORLD_TYPES))
   seal=json.loads((path/"FROZEN_BEFORE_EXAM.json").read_text())
   self.assertTrue(seal["no_exam_labels_in_training"])
   self.assertFalse(report["independent_real_world_sources"])
   with self.assertRaises(ValueError):run(path,minutes=2,train_each=30,validation_each=20,exam_each=20)
if __name__=="__main__":unittest.main()
