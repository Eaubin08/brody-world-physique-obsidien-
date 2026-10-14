import tempfile,unittest
from pathlib import Path
from brody_world_physique.goal_multi_continuity_p165d7 import fixtures
from brody_world_physique.local_epistemic_diagnostic_p165d9 import local_view,run
class D9Tests(unittest.TestCase):
 def test_local_symbolic_and_global_conflict_distinct(self):
  claims=[c for c in fixtures() if c["continuity"]!="symbolic"]
  v=local_view("INTERPRET_SYMBOL",claims)
  self.assertEqual(v["local_status"],"HOLD_LOCAL_NO_RELEVANT_EVIDENCE")
  self.assertEqual(v["global_status"],"MULTI")
 def test_priority_is_not_truth(self):
  evidence=fixtures()
  a=local_view("LOCATE",evidence)
  b=local_view("REIDENTIFY",evidence)
  self.assertNotEqual(a["focused_ids"],b["focused_ids"])
  self.assertFalse(a["priority_promotes_truth"])
  self.assertEqual(set(a["retained_all_ids"]),set(b["retained_all_ids"]))
 def test_conflict_local_and_global_separation(self):
  s=local_view("REIDENTIFY",fixtures())
  self.assertEqual(s["local_status"],"MULTI_LOCAL")
  self.assertIn("alternative",s["local_conflicts"])
 def test_report_bounded_and_immutable(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"d9"
   r=run(p,seeds=1,limit=3,beam=4)
   self.assertEqual(r["episodes"],3)
   self.assertFalse(r["tracker_algorithm_changed"])
   with self.assertRaises(ValueError):run(p,seeds=1,limit=3,beam=4)
if __name__=="__main__":unittest.main()
