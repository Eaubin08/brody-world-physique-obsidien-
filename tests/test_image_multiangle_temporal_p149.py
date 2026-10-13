import tempfile,unittest,json
from pathlib import Path
from brody_world_physique.image_multiangle_temporal_p149 import run,paired_counterfactual,KINDS,estimator
class P149Tests(unittest.TestCase):
 def test_pixel_identical_snapshot_with_different_past(self):
  p=paired_counterfactual()
  self.assertTrue(p["same_final_pixels"])
  self.assertTrue(p["different_histories"])
  self.assertTrue(p["different_hidden_identity_futures"])
 def test_history_requires_observations(self):
  self.assertIsNone(estimator([{"26":None}]*5)[0])
 def test_multiangle_report_and_preservation(self):
  with tempfile.TemporaryDirectory() as d:
   dest=Path(d)/"run"
   r=run(dest,minutes=2,episodes_per_kind=20)
   self.assertEqual(r["episodes"],240)
   self.assertEqual(r["scenarios_completed"],len(KINDS))
   self.assertFalse(r["identity_resolution_proven"])
   self.assertEqual(len((dest/"EPISODES.jsonl").read_text().splitlines()),240)
   with self.assertRaises(ValueError):run(dest,minutes=2,episodes_per_kind=20)
if __name__=="__main__":unittest.main()
