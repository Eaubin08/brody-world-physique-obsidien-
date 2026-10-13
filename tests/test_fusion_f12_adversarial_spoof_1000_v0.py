import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.fusion_f12_adversarial_spoof_1000_v0 import case,run,KINDS,policy
from brody_world_physique.fusion_f9_intensive_education_v0 import verify_chain

class SpoofFuzzingTests(unittest.TestCase):
 def test_baseline_and_cue_inversion(self):
  baseline=case(42,1,"baseline",policy())
  self.assertEqual(baseline["decision"],baseline["true_context"])
  spoof=case(42,1,"opposite",policy())
  self.assertNotEqual(spoof["decision"],spoof["true_context"])
  self.assertTrue(spoof["spoof_success"])
  both=case(42,1,"both",policy())
  self.assertIsNone(both["decision"])
 def test_campaign_receipts_and_evidence(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/"campaign"
   report=run(root,100,seed=72)
   self.assertEqual(report["cases"],100)
   self.assertEqual(report["attack_families"],len(KINDS))
   self.assertEqual(verify_chain(root/"attack_receipts.jsonl")[0],100)
   self.assertGreater(report["wrong_context_total"],0)
   self.assertGreater(report["spoof_success_total"],0)
   self.assertFalse(report["native_memory_write"])
   with self.assertRaises(ValueError):run(root,100)
 def test_tamper_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/"campaign";run(root,20,seed=72)
   p=root/"attack_receipts.jsonl";lines=p.read_text().splitlines()
   v=json.loads(lines[0]);v["payload"]["decision"]="FORGED";lines[0]=json.dumps(v)
   p.write_text("\n".join(lines)+"\n")
   with self.assertRaises(ValueError):verify_chain(p)
if __name__=="__main__":unittest.main()
