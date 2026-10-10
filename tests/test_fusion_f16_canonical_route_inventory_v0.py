import tempfile,unittest
from pathlib import Path
from brody_world_physique.fusion_f16_canonical_route_inventory_v0 import inspect,REQUIRED
class CanonicalRouteInventoryTests(unittest.TestCase):
 def test_missing_repo_refused(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(RuntimeError):inspect(d)
 def test_contract_mismatch_exposed_not_patched(self):
  with tempfile.TemporaryDirectory() as d:
   base=Path(d)
   for rel in REQUIRED.values():
    dest=base/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text("pass\n")
   (base/REQUIRED["domains"]).write_text('from enum import Enum\nclass Domain(Enum):\n    META="meta"\n')
   result=inspect(base)
   self.assertEqual(result["status"],"CONTRACT_MISMATCH_REVIEW_REQUIRED")
   self.assertFalse(result["brody_image_registered"])
   self.assertFalse(result["runtime_execution"])
if __name__=="__main__":unittest.main()
