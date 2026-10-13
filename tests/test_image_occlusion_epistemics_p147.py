import tempfile,unittest,json,random
from pathlib import Path
from brody_world_physique.image_occlusion_epistemics_p147 import render,run
class OcclusionTests(unittest.TestCase):
 def test_same_course_and_exam_are_separate(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/"school"
   result=run(out,minutes=2,lessons=30,exam_per_condition=20)
   self.assertEqual(result["exam_count"],60)
   self.assertEqual(result["condition_scores"]["full"]["holds"],20)
   self.assertEqual(result["condition_scores"]["full"]["answered"],0)
   self.assertEqual(result["condition_scores"]["none"]["answered"],20)
   sealed=json.loads((out/"SEALED_COURSE.json").read_text())
   self.assertTrue(sealed["memory_frozen_before_exam"])
   with self.assertRaises(ValueError):run(out,minutes=2,lessons=30,exam_per_condition=20)
 def test_full_occlusion_is_visible_ambiguity(self):
  a=random.Random(55)
  im,_,_=render(a,"full")
  self.assertEqual(im.getpixel((25,25)),(95,95,95))
  im.close()
if __name__=="__main__":unittest.main()
