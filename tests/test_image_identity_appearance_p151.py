import tempfile,unittest,random
from pathlib import Path
from brody_world_physique.image_identity_appearance_p151 import CASES,episode,predict,run
class P151Tests(unittest.TestCase):
 def test_scenarios_do_not_collapse_colour_into_motion(self):
  a,b=episode(random.Random(12),"colour_only")
  c,d=episode(random.Random(12),"motion_reverse_only")
  self.assertLess(d[-1]["A"][0],d[5]["A"][0])
  self.assertGreater(b[-1]["A"][0],b[5]["A"][0])
  for im in a+c:im.close()
 def test_image_only_inference(self):
  frames,truth=episode(random.Random(7),"cross_color")
  value,reason,seen=predict(frames[:9])
  self.assertIn(reason,("TRACK","HOLD_IDENTITY_AMBIGUOUS","HOLD_TARGET_INVISIBLE","HOLD_NO_INITIALIZATION"))
  for im in frames:im.close()
 def test_run_and_preserve_evidence(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"trial";r=run(p,minutes=2,episodes_each=10)
   self.assertEqual(r["exam_cases"],len(CASES)*10)
   self.assertIn("colour_only",r["per_condition"])
   self.assertIn("motion_reverse_only",r["per_condition"])
   self.assertFalse(r["tracking_identity_proven"])
   self.assertEqual(len((p/"EXAMS.jsonl").read_text().splitlines()),len(CASES)*10)
   with self.assertRaises(ValueError):run(p,minutes=2,episodes_each=10)
if __name__=="__main__":unittest.main()
