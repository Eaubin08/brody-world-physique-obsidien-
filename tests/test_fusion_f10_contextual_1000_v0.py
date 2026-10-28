import tempfile,unittest,json
from pathlib import Path
from brody_world_physique.fusion_f10_contextual_1000_v0 import run,decide
from brody_world_physique.fusion_f9_intensive_education_v0 import verify_chain
class ContextualIntensiveTests(unittest.TestCase):
 def test_contextual_retention_and_unknown_hold(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"exp"
   r=run(root,episodes=240,checkpoint=60)
   self.assertEqual(r["episodes"],240)
   self.assertEqual(len(r["checkpoints"]),4)
   self.assertEqual(verify_chain(root/"receipts.jsonl")[0],240)
   self.assertTrue(r["ambiguous_contexts_held"])
   self.assertEqual(r["trained_contexts"],24)
   final=json.loads((root/"snapshot-000240.json").read_text())["policy"]
   self.assertEqual(decide(final,"LIGHT","line","OLD")["tool"],"PENCIL")
   self.assertEqual(decide(final,"LIGHT","line","NEW")["tool"],"PEN")
   self.assertIsNone(decide(final,"LIGHT","line","MIXED")["tool"])
   self.assertIsNone(decide(final,"LIGHT","line","UNKNOWN")["tool"])
   self.assertFalse(r["native_memory_write"])
 def test_reproducible_and_tamper_detected(self):
  with tempfile.TemporaryDirectory() as d:
   a=run(Path(d)/"a",episodes=48,checkpoint=24,seed=88)
   b=run(Path(d)/"b",episodes=48,checkpoint=24,seed=88)
   self.assertEqual(a["receipt_tip"],b["receipt_tip"])
   with self.assertRaises(ValueError):run(Path(d)/"a",episodes=48)
   receipt=Path(d)/"a"/"receipts.jsonl"
   lines=receipt.read_text().splitlines()
   obj=json.loads(lines[4]);obj["context"]="FORGED";lines[4]=json.dumps(obj)
   receipt.write_text("\n".join(lines)+"\n")
   with self.assertRaises(ValueError):verify_chain(receipt)
if __name__=="__main__":unittest.main()
