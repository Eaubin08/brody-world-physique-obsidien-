import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.image_validation_router_p143 import run
class RouterTests(unittest.TestCase):
 def test_three_way_split_frozen_routing_and_hold(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"run"
   r=run(p,minutes=2,train_per_family=30,validation_per_cell=20,exam_per_cell=20)
   self.assertEqual(r["cells_completed"],30)
   self.assertEqual(r["exam"],600)
   self.assertEqual(r["validation"],600)
   self.assertGreater(r["router_coverage"],0)
   self.assertLess(r["router_coverage"],1)
   router=json.loads((p/"FROZEN_ROUTER.json").read_text())
   self.assertTrue(router["frozen_before_exam"])
   self.assertEqual(router["choices"]["colour/greyscale"],"HOLD")
   cells=json.loads((p/"CELL_REPORT.json").read_text())
   self.assertEqual(cells["colour/greyscale"]["holds"],20)
   self.assertTrue((p/"EXAM_DECISIONS.jsonl").exists())
 def test_preserves_evidence(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"run"
   run(p,minutes=2,train_per_family=30,validation_per_cell=20,exam_per_cell=20)
   with self.assertRaises(ValueError):
    run(p,minutes=2,train_per_family=30,validation_per_cell=20,exam_per_cell=20)
if __name__=="__main__":unittest.main()
