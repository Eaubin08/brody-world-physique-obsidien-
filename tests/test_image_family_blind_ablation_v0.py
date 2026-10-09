import json,tempfile,unittest
from pathlib import Path
from collections import Counter
from brody_world_physique.fusion_f9_intensive_education_v0 import digest
from brody_world_physique.image_family_blind_ablation_v0 import schedule,evaluate_case,run
class BlindAblationTests(unittest.TestCase):
 def test_balanced_randomized_independent_context(self):
  fixtures=schedule(1000,45)
  self.assertEqual(set(Counter(x[0] for x in fixtures).values()),{100})
  self.assertGreater(len(set(x[1:] for x in fixtures[:100])),40)
 def test_hidden_family_not_in_learner_key(self):
  base={};learned={}
  x=evaluate_case(("wrong_intent","LIGHT","line",8),base,learned,True)
  self.assertEqual(x["key_visible_to_learner"],"LIGHT|line")
  self.assertTrue(all("wrong_intent" not in key for key in learned))
 def test_blind_exam_and_receipt_integrity(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);snapshot=root/"snapshot.json"
   snapshot.write_text(json.dumps({"candidate_stats":{},"hash":digest({})}))
   report=run(root/"out",snapshot,100,100)
   self.assertEqual(report["exam"],100)
   self.assertFalse(report["family_label_exposed_to_learner"])
   self.assertFalse(report["exam_feedback_used_for_training"])
   self.assertFalse(report["native_memory_write"])
 def test_tamper_refused(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/"snap.json"
   path.write_text(json.dumps({"candidate_stats":{},"hash":"BAD"}))
   with self.assertRaises(ValueError):run(Path(tmp)/"out",path,100,100)
if __name__=="__main__":unittest.main()
