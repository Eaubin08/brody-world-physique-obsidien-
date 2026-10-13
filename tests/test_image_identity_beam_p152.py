import tempfile,unittest,random
from pathlib import Path
from brody_world_physique.image_identity_beam_p152 import run,beam_predict,step,initial_tracks
from brody_world_physique.image_identity_appearance_p151 import CASES,episode
class P152Tests(unittest.TestCase):
 def test_competing_paths_survive(self):
  beam=initial_tracks([(12,30,0),(90,30,0)])
  future=step(beam,[(16,30,0),(86,30,0)],12)
  self.assertGreater(len(future),1)
  self.assertGreaterEqual(future[0][2],0)
 def test_pixels_only_interface(self):
  frames,teacher=episode(random.Random(9),"colour_only")
  result,reason,info=beam_predict(frames[:9])
  self.assertIn(reason,("TRACK","HOLD_NO_TRACK","HOLD_LONG_OCCLUSION","HOLD_COMPETING_IDENTITIES"))
  for im in frames:im.close()
 def test_paired_test_and_no_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"trial";r=run(p,minutes=2,episodes_each=10,beam_width=4)
   self.assertEqual(r["cases"],10*len(CASES))
   self.assertEqual(r["conditions_completed"],len(CASES))
   self.assertTrue(r["no_exam_feedback"])
   self.assertFalse(r["oracle_identity_exposed_to_predictors"])
   self.assertIn("motion_reverse_only",r["per_condition"])
   self.assertEqual(len((p/"EXAMS.jsonl").read_text().splitlines()),r["cases"])
   with self.assertRaises(ValueError):run(p,minutes=2,episodes_each=10)
if __name__=="__main__":unittest.main()
