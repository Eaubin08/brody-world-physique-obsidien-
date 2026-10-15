import tempfile,unittest,random,json
from pathlib import Path
from brody_world_physique.image_full_education_p154 import simulate,observations,infer_rule,forecast,grade_visual,run,WORLD,LAWS
class P154Tests(unittest.TestCase):
 def test_observation_not_simulator_truth(self):
  ims,truth=simulate(random.Random(11),"constant_speed","clean")
  xs=observations(ims[:6],"clean")
  self.assertEqual(len(xs),6)
  self.assertTrue(all(x is not None for x in xs))
  self.assertAlmostEqual(xs[1]-xs[0],truth[1]-truth[0],delta=1.5)
  for im in ims:im.close()
 def test_induction_uses_examples(self):
  r=infer_rule([[1,3,5,7],[4,6,8,10]])
  self.assertAlmostEqual(r["mean_accel"],0)
  self.assertAlmostEqual(forecast([1,3,5],r),7)
  self.assertIsNone(forecast([None,None],r))
 def test_visual_comparison(self):
  self.assertEqual(grade_visual(30,30),1)
  self.assertLess(grade_visual(30,50),.1)
 def test_integrated_sealed_pass(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"test"
   r=run(p,minutes=3,lessons_each=8,exam_each=20,feedback_each=8,retest_each=20)
   self.assertEqual(r["exam_cases"],len(WORLD)*len(LAWS)*20)
   self.assertEqual(r["retest_cases"],len(WORLD)*len(LAWS)*20)
   self.assertEqual(r["exam_cells_complete"],24)
   self.assertEqual(r["retest_cells_complete"],24)
   self.assertTrue((p/"FROZEN_BEFORE_EXAM.json").exists())
   self.assertTrue((p/"LEARNED_CORRECTIONS.json").exists())
   self.assertTrue((p/"EXAM.jsonl").exists())
   self.assertTrue((p/"RETEST.jsonl").exists())
   self.assertFalse(r["real_world_observation"])
   with self.assertRaises(ValueError):
    run(p,minutes=3,lessons_each=8,exam_each=20,feedback_each=8,retest_each=20)
if __name__=="__main__":unittest.main()
