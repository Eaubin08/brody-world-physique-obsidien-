import tempfile,unittest
from pathlib import Path
from brody_world_physique.image_scene_adversarial_p165a import CASES,make_case,observe_and_test,run
class P165ATests(unittest.TestCase):
 def test_six_different_cases(self):
  self.assertEqual(len(CASES),6)
  for case in CASES:
   images,oracle=make_case(case,165)
   self.assertEqual(len(images),7)
   self.assertEqual(oracle["case"],case)
   for im in images:im.close()
 def test_ambiguity_ground_truth_not_injected(self):
  out=observe_and_test("crossing_indistinguishable",165)
  self.assertFalse(out["oracle_identity_identifiable"])
  self.assertEqual(len(out["paths"][0]["xs"]),7)
 def test_color_change_is_adversarial(self):
  imgs,_=make_case("color_swap",3)
  self.assertNotEqual(imgs[1].getpixel((36,48)),imgs[5].getpixel((52,48)))
  for im in imgs:im.close()
 def test_output_evidence_preserved(self):
  with tempfile.TemporaryDirectory() as td:
   folder=Path(td)/"p165a"
   report=run(folder,n_each=5,minutes=3)
   self.assertTrue(report["run_complete"])
   self.assertEqual(report["episodes"],30)
   self.assertFalse(report["full_hard_plus_plus_16_family_suite_implemented"])
   with self.assertRaises(ValueError):run(folder,n_each=5,minutes=3)
if __name__=="__main__":unittest.main()
