import json,tempfile,unittest,random
from pathlib import Path
from brody_world_physique.image_tracking_beam_p150 import build,observe,camera_from_marks,infer,run,SCENARIOS
class TestP150(unittest.TestCase):
 def test_detector_no_lane_argument(self):
  images,truth,cam=build(random.Random(3),"cross")
  objects,marks=observe(images[0])
  self.assertGreaterEqual(len(objects),2)
  self.assertIsNotNone(camera_from_marks(marks))
  for im in images:im.close()
 def test_camera_motion_uses_observed_landmarks(self):
  imgs,truth,cam=build(random.Random(12),"camera_pan")
  result=infer(imgs[:8])
  self.assertTrue(result["camera_observed"])
  for im in imgs:im.close()
 def test_sealed_run_and_distinct_scoring(self):
  with tempfile.TemporaryDirectory() as d:
   dest=Path(d)/"run"
   report=run(dest,minutes=2,episodes_each=10)
   self.assertEqual(report["episodes"],10*len(SCENARIOS))
   self.assertEqual(report["scenarios_completed"],len(SCENARIOS))
   self.assertIn("occlude_both",report["scenarios"])
   self.assertFalse(report["real_identity_proven"])
   self.assertEqual(len((dest/"EXAMS.jsonl").read_text().splitlines()),10*len(SCENARIOS))
   with self.assertRaises(ValueError):run(dest,minutes=2,episodes_each=10)
if __name__=="__main__":unittest.main()
