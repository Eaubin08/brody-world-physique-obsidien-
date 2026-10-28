"""Verify F2 scorecard does not conflate education, memory or pixels."""
import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.fusion_f2_historical_scorecard_v1 import scorecard,SCHOOLS
class ScorecardTests(unittest.TestCase):
 def test_archives_and_missing_are_explicit(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);folder=p/SCHOOLS["V0"];folder.mkdir()
   (folder/"evaluation.json").write_text(json.dumps({"exams":[{"exercise_ref":"exam01","candidate_replay_error_pixels":12,"after_feedback_error_pixels":0}]}))
   r=scorecard(p,p/"scores.json")
   self.assertEqual(r["schools"][0]["scores"][0]["initial"],12)
   self.assertEqual(r["schools"][0]["scores"][0]["final"],0)
   self.assertEqual(r["schools"][1]["status"],"MISSING")
   self.assertFalse(r["metric_cross_school_comparison_valid"])
 def test_existing_output_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/"scores.json").write_text("{}")
   with self.assertRaises(ValueError):scorecard(p,p/"scores.json")
if __name__=="__main__":unittest.main()
