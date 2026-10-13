import tempfile,unittest,random,json
from pathlib import Path
from brody_world_physique.image_temporal_occlusion_p148 import generate,locate,forecast,run,KINDS
class TemporalOcclusionTests(unittest.TestCase):
 def test_hidden_observation_causes_hold(self):
  self.assertEqual(forecast([None,None,None,None])[0],None)
 def test_history_and_snapshot_are_different(self):
  self.assertEqual(forecast([10,14,18,22])[0],26)
  self.assertEqual(forecast([10,14,18,22])[0]-22,4)
 def test_corpus_ten_families_and_evidence(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/"trial"
   r=run(path,minutes=2,episodes_per_kind=20)
   self.assertEqual(r["episodes"],200)
   self.assertEqual(set(r["scenarios"]),set(KINDS))
   self.assertTrue(any(s["history_holds"]>0 for s in r["scenarios"].values()))
   self.assertFalse(r["physics_learning_proven"])
   self.assertEqual(len((path/"EPISODES.jsonl").read_text().splitlines()),200)
   with self.assertRaises(ValueError):run(path,minutes=2,episodes_per_kind=20)
if __name__=="__main__":unittest.main()
