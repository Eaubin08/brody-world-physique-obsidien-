import tempfile,unittest,json
from pathlib import Path
from brody_world_physique.fusion_f13_provenance_guard_audit_v0 import gate,run
from brody_world_physique.fusion_f9_intensive_education_v0 import verify_chain
class ProvenanceGateTests(unittest.TestCase):
 def test_single_source_cannot_authorize(self):
  self.assertIsNone(gate("LEFT")["accepted"])
  self.assertEqual(gate("LEFT")["status"],"HOLD_UNVERIFIED_ORIGIN")
  self.assertEqual(gate("LEFT","NEW",True)["status"],"HOLD_SOURCE_CONTRADICTION")
  self.assertEqual(gate("LEFT","OLD",True)["accepted"],"OLD")
  self.assertIsNone(gate("BOTH","OLD",True)["accepted"])
 def test_campaign_replays_and_chained_receipts(self):
  with tempfile.TemporaryDirectory() as t:
   folder=Path(t)/"audit";result=run(folder,100)
   self.assertEqual(result["cases"],100)
   self.assertEqual(verify_chain(folder/"receipts.jsonl")[0],100)
   self.assertGreater(result["old_wrong_total"],0)
   self.assertEqual(result["accepted_wrong_total"],0)
   self.assertGreater(result["hold_total"],0)
   self.assertFalse(result["sensor_authentication_proven"])
   with self.assertRaises(ValueError):run(folder,100)
 def test_tamper_detection(self):
  with tempfile.TemporaryDirectory() as t:
   folder=Path(t)/"audit";run(folder,20)
   loc=folder/"receipts.jsonl"
   lines=loc.read_text().splitlines()
   x=json.loads(lines[0]);x["evidence"]["verified"]=False;lines[0]=json.dumps(x)
   loc.write_text("\n".join(lines)+"\n")
   with self.assertRaises(ValueError):verify_chain(loc)
if __name__=="__main__":unittest.main()
