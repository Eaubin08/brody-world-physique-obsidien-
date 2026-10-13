import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.image_long_curriculum_p140 import run,FAMILIES
class LongCurriculumTests(unittest.TestCase):
 def test_multiple_learning_families_holdout_and_comparison(self):
  with tempfile.TemporaryDirectory() as folder:
   output=Path(folder)/"run"
   report=run(output,minutes=2,max_episodes=100,seed=10)
   self.assertEqual(report["episodes"],100)
   self.assertEqual(set(report["family_stats"]),set(FAMILIES))
   for metrics in report["family_stats"].values():
    self.assertGreater(metrics["train"],0)
    self.assertGreater(metrics["exam"],0)
    self.assertGreaterEqual(metrics["accuracy"],0)
    self.assertLessEqual(metrics["accuracy"],1)
   data=(output/"EPISODES.jsonl").read_text().splitlines()
   self.assertTrue(any('"phase": "forecast"' in row for row in data))
   self.assertTrue(any('"phase": "grade"' in row for row in data))
   self.assertTrue(report["no_exam_feedback_to_memory"])
   self.assertFalse(report["generalization_to_real_world_proven"])
 def test_no_overwrite_invalid_budget(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/"out";run(p,minutes=2,max_episodes=100)
   with self.assertRaises(ValueError):run(p,minutes=2,max_episodes=100)
   with self.assertRaises(ValueError):run(Path(folder)/"bad",minutes=1,max_episodes=100)
if __name__=="__main__":unittest.main()
