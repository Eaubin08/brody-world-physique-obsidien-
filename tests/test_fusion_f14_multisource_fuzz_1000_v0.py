import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.fusion_f14_multisource_fuzz_1000_v0 import (
  adjudicate,observation,build_case,MODES,run)
from brody_world_physique.fusion_f9_intensive_education_v0 import verify_chain

class MultiSourceFuzzTests(unittest.TestCase):
 def test_independence_and_contradiction(self):
  a=observation("OLD","one","origin1",1000)
  b=observation("OLD","two","origin2",1000)
  self.assertEqual(adjudicate([a,b])["accepted"],"OLD")
  b["value"]="NEW"
  self.assertIsNone(adjudicate([a,b])["accepted"])
  b["value"]="OLD";b["origin_id"]="origin1"
  self.assertIsNone(adjudicate([a,b])["accepted"])
 def test_attack_matrix_exposes_correlated_spoofing(self):
  for mode in MODES:
   outcome=adjudicate(build_case(mode,"OLD",None))
   if mode in ("clean_two","clean_three"):
    self.assertEqual(outcome["accepted"],"OLD")
   elif mode=="all_spoof":
    self.assertEqual(outcome["accepted"],"NEW")
   else:
    self.assertIsNone(outcome["accepted"],mode)
 def test_report_and_receipt_tamper(self):
  with tempfile.TemporaryDirectory() as t:
   output=Path(t)/"audit"
   report=run(output,100)
   self.assertEqual(report["cases"],100)
   self.assertEqual(verify_chain(output/"receipts.jsonl")[0],100)
   self.assertGreater(report["accepted_wrong"],0)
   self.assertTrue(report["source_attestation_is_harness_fixture_only"])
   with self.assertRaises(ValueError):run(output,100)
   p=output/"receipts.jsonl"
   lines=p.read_text().splitlines()
   x=json.loads(lines[0]);x["decision"]["accepted"]="FORGED"
   lines[0]=json.dumps(x);p.write_text("\n".join(lines)+"\n")
   with self.assertRaises(ValueError):verify_chain(p)
if __name__=="__main__":unittest.main()
