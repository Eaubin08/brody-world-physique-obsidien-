import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.fusion_f9_intensive_education_v0 import digest
from brody_world_physique.image_persistent_transfer_exam_v0 import run,one,context

class PersistentTransferTests(unittest.TestCase):
 def test_missing_or_corrupt_snapshot_fails_closed(self):
  with tempfile.TemporaryDirectory() as d:
   file=Path(d)/"s.json"
   file.write_text(json.dumps({"candidate_stats":{},"hash":"WRONG"}))
   with self.assertRaises(ValueError):run(Path(d)/"o",file,100,100)
 def test_train_updates_but_exam_does_not(self):
  policy={};cache={}
  one(1,42,policy,cache,True)
  after=digest(cache)
  one(1,123,policy,cache,False)
  self.assertEqual(digest(cache),after)
 def test_100_train_100_blind_split_and_no_memory(self):
  with tempfile.TemporaryDirectory() as d:
   file=Path(d)/"s.json"
   file.write_text(json.dumps({"candidate_stats":{},"hash":digest({})}))
   result=run(Path(d)/"o",file,100,100)
   self.assertEqual(result["blind_exam_episodes"],100)
   self.assertEqual(sum(x["cases"] for x in result["families"].values()),100)
   self.assertFalse(result["native_memory_write"])
   self.assertFalse(result["blind_exam_feedback_used_for_training"])
   self.assertTrue(result["family_label_available_to_learner"])
if __name__=="__main__":unittest.main()
