import tempfile,unittest
from pathlib import Path
from brody_world_physique.scene_event_epistemic_p165d import run,infer,CASES
from brody_world_physique.image_scene_adversarial_p165a import make_case
class P165DTests(unittest.TestCase):
 def test_all_fixture_gates_fail_closed(self):
  for case in CASES:
   frames,_=make_case(case,35)
   try:result=infer(case,frames)
   finally:
    for im in frames:im.close()
   self.assertIn(result["status"],("MULTI","HOLD"))
   self.assertFalse(result["unique_identity_proven"])
   self.assertFalse(result["hidden_event_recovered"])
 def test_camera_ambiguity_hold(self):
  frames,_=make_case("camera_without_landmarks",165)
  try:self.assertEqual(infer("camera_without_landmarks",frames)["status"],"HOLD")
  finally:
   for im in frames:im.close()
 def test_raster_components_measured(self):
  frames,_=make_case("occluded_jump",165)
  try:
   row=infer("occluded_jump",frames)
   self.assertEqual(len(row["candidate_counts"]),7)
  finally:
   for im in frames:im.close()
 def test_preserves_evidence(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"proof";a=run(p,each=5)
   self.assertEqual(a["exams"],len(CASES)*5)
   self.assertTrue(a["gates_rule_based_on_fixture_case"])
   with self.assertRaises(ValueError):run(p,each=5)
if __name__=="__main__":unittest.main()
