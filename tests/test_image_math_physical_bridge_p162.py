import tempfile,unittest
from pathlib import Path
from brody_world_physique.image_math_physical_bridge_p162 import (
 features,classify,predict_next,reverse_check,run,STYLES,TEST_LAWS
)
class P162Tests(unittest.TestCase):
 def test_still_vs_linear_separated_by_velocity(self):
  still=[35.]*7
  linear=[35.+3*i for i in range(7)]
  self.assertEqual(classify(features(still))["selected"],"still")
  self.assertEqual(classify(features(linear))["selected"],"linear")
 def test_temporal_change_preserved_as_novel_candidate(self):
  reverse=[30.,34.,38.,42.,46.,42.,38.]
  result=classify(features(reverse))
  self.assertEqual(result["status"],"NOVELTY_CANDIDATE")
 def test_projection_reverse_is_tested(self):
  xs=[30.+3*i for i in range(7)]
  state=features(xs);result=classify(state)
  p=predict_next(xs,state,result)
  self.assertAlmostEqual(p,51.)
  evidence=reverse_check(p)
  self.assertIsNotNone(evidence["reread_x"])
  self.assertLess(evidence["reread_abs_error"],.51)
 def test_missing_visibility_holds(self):
  self.assertEqual(classify(features([None,None,30.,None,33.,None,34.]))["status"],"HOLD")
 def test_full_paired_exam_and_evidence(self):
  with tempfile.TemporaryDirectory() as td:
   folder=Path(td)/"p162"
   data=run(folder,minutes=3,exam_each=10)
   self.assertEqual(data["cells_completed"],len(STYLES)*len(TEST_LAWS))
   self.assertEqual(data["episodes"],len(STYLES)*len(TEST_LAWS)*10)
   self.assertFalse(data["real_f12_f16_runtime_connected"])
   self.assertTrue((folder/"EXAMS.jsonl").is_file())
   with self.assertRaises(ValueError):run(folder,minutes=3,exam_each=10)
if __name__=="__main__":unittest.main()
