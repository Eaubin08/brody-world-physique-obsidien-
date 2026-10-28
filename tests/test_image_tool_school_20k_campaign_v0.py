import tempfile,unittest,json
from pathlib import Path
from PIL import Image
from brody_world_physique.image_tool_school_20k_campaign_v0 import (
 FAMILIES,perturb,blind_challenge,evaluate,
)
class School20KContractTests(unittest.TestCase):
 def test_ten_distinct_exam_families(self):
  self.assertEqual(len(FAMILIES),10)
  self.assertEqual(len(set(FAMILIES)),10)
 def test_all_perturbations_preserve_dimensions(self):
  for mode in FAMILIES:
   im=perturb(Image.new("L",(64,64),255),mode,__import__("random").Random(42))
   self.assertEqual(im.size,(64,64))
 def test_unknown_intent_holds(self):
  self.assertTrue(blind_challenge({},"unknown_intent",1,123)["held"])
 def test_exam_receipts_and_no_memory_writes(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/"exam.jsonl"
   result=evaluate({},100,123,path)
   self.assertEqual(result["cases"],100)
   self.assertEqual(sum(x["cases"] for x in result["families"].values()),100)
   self.assertTrue(all(x["holds"]==10 for x in result["families"].values()))
   first=json.loads(path.read_text(encoding="utf-8").splitlines()[0])
   self.assertFalse(first["native_memory_write"])
   self.assertFalse(first["canonical_promotion"])
if __name__=="__main__":unittest.main()
