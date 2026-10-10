import tempfile,unittest
from pathlib import Path
from brody_world_physique.fusion_f5_multiskill_course_v0 import course,route
from brody_world_physique.fusion_f4_education_journal_v0 import verify_journal,readonly_context
class MultiSkillCourseTests(unittest.TestCase):
 def test_three_skills_and_readonly_exams(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)/"course"
   result=course(root)
   self.assertEqual(result["training_skill_count"],3)
   self.assertEqual(result["snapshot_version"],3)
   self.assertEqual(len(result["exams"]),3)
   self.assertEqual(result["history_count"],6)
   self.assertEqual(len(verify_journal(root)),6)
   self.assertEqual(len(readonly_context(root,3)["skill_ids"]),3)
   self.assertTrue(all(x["choice"]["test_pixels_seen"] is False for x in result["exams"]))
   for item in result["exams"]:
    self.assertTrue((Path(item["exam_dir"])/"comparison.png").exists())
    self.assertEqual(item["choice"]["selected"],item["goal"])
 def test_unknown_goals_hold_and_prior_snapshot_cannot_leak_future_skills(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)/"course";course(root)
   self.assertEqual(route(root,3,"UNKNOWN")["authority"],"HOLD")
   self.assertEqual(route(root,1,"triangle")["authority"],"HOLD")
   self.assertEqual(route(root,2,"triangle")["selected"],"triangle")
   with self.assertRaises(ValueError):course(root)
if __name__=="__main__":unittest.main()
