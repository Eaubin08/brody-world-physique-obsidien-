"""F3b curriculum contracts: multi-exercise run, score visibility and integrity."""
import tempfile,unittest,json
from pathlib import Path
from brody_world_physique.fusion_f3b_multilesson_school_v0 import school,LESSONS
from brody_world_physique.drawing_school_v0 import SIDE
class MultiLessonTests(unittest.TestCase):
 def test_all_layout_boxes_satisfy_motor_contract(self):
  for name,shape,boxes,stage in LESSONS:
   for x1,y1,x2,y2 in boxes:
    self.assertTrue(0<=x1<x2<SIDE and 0<=y1<y2<SIDE,name)

 def test_five_lessons_real_outputs_and_scores(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/"school"
   result=school(path)
   self.assertEqual(result["lessons"],5)
   self.assertEqual(len(result["rows"]),len(LESSONS))
   self.assertTrue((path/"scores.csv").is_file())
   self.assertEqual(result["total_blank_error"]-result["total_candidate_error"],
                    sum(r["gain"] for r in result["rows"]))
   for r in result["rows"]:
    self.assertTrue(r["candidate_sealed_before_teacher"])
    self.assertTrue((path/r["lesson"]/"comparison.png").is_file())
    self.assertTrue((path/r["lesson"]/"candidate.png").is_file())
    self.assertGreaterEqual(r["baseline_error"],0)
    self.assertGreaterEqual(r["candidate_error"],0)
 def test_refuse_overwrite_and_separate_training(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/"school"
   result=school(path)
   self.assertTrue(result["learning_is_independent_per_lesson"])
   with self.assertRaises(ValueError):school(path)
if __name__=="__main__":unittest.main()
