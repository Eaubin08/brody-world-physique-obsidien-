import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.fusion_f9_intensive_education_v0 import run,verify_chain
class IntensiveEducationTests(unittest.TestCase):
 def test_checkpoint_memory_and_sealed_heldout(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/"campaign"
   result=run(root,episodes=48,seed=441,checkpoint=12)
   self.assertEqual(result["completed_episodes"],48)
   self.assertEqual(result["receipt_count"],48)
   self.assertEqual(len(result["checkpoints"]),4)
   self.assertEqual(result["training_contexts"],12)
   self.assertEqual(verify_chain(root/"receipts.jsonl")[0],48)
   self.assertEqual(len(result["final_policy"]),12)
   exams=json.loads((root/"heldout_checkpoints.json").read_text())
   self.assertTrue(all(x["feedback_used_for_training"] is False for x in exams))
   self.assertTrue(all(x["test_target_access_before_candidate_seal"] is False for x in exams))
   self.assertTrue(all(x["exam_seed"]==exams[0]["exam_seed"] for x in exams))
   self.assertFalse(result["native_memory_write"])
 def test_repeatability_and_no_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   a=run(Path(t)/"a",episodes=36,seed=77,checkpoint=12)
   b=run(Path(t)/"b",episodes=36,seed=77,checkpoint=12)
   self.assertEqual(a["receipt_tip"],b["receipt_tip"])
   self.assertEqual(a["checkpoints"],b["checkpoints"])
   with self.assertRaises(ValueError):run(Path(t)/"a",episodes=36)
 def test_receipt_tamper_and_invalid_parameter_fail_closed(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/"course";run(root,episodes=24,checkpoint=12)
   ledger=root/"receipts.jsonl"
   lines=ledger.read_text().splitlines()
   forged=json.loads(lines[10]);forged["corrected"]=not forged["corrected"]
   lines[10]=json.dumps(forged)
   ledger.write_text("\n".join(lines)+"\n")
   with self.assertRaises(ValueError):verify_chain(ledger)
   with self.assertRaises(ValueError):run(Path(t)/"invalid",episodes=0)
if __name__=="__main__":unittest.main()
