import tempfile,unittest
from pathlib import Path
from brody_world_physique.image_cumulative_education_p156 import check,run,LAWS,WORLD
class P156Tests(unittest.TestCase):
 def test_allow_gain_without_forgetting(self):
  self.assertTrue(check(1,[(1,2),(2,3)],[("old",[(1,2)],0.)],retention_tolerance=.05)[0])
 def test_hold_if_prior_skill_regresses(self):
  ok,reason=check(1,[(1,2),(2,3)],[("old",[(2,2),(3,3)],0.)])
  self.assertFalse(ok);self.assertEqual(reason,"HOLD_FORGETTING")
 def test_hold_without_gain(self):
  self.assertFalse(check(0.,[(1,2)],[])[0])
 def test_cumulative_run_and_preservation(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"p156"
   r=run(p,minutes=3,lessons_each=8,feedback_each=8,validation_each=8,exam_each=20)
   self.assertEqual(r["cycles_completed"],len(LAWS)*len(WORLD))
   self.assertEqual(r["exam_cases"],20*len(LAWS)*len(WORLD))
   self.assertEqual(len(r["history"]),24)
   self.assertTrue(any(row["replayed_prior_skills"] for row in r["history"]))
   self.assertFalse(r["exam_selection_leakage"])
   with self.assertRaises(ValueError):
    run(p,minutes=3,lessons_each=8,feedback_each=8,validation_each=8,exam_each=20)
if __name__=="__main__":unittest.main()
