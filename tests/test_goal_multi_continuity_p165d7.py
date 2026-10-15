import tempfile,unittest
from pathlib import Path
from brody_world_physique.goal_multi_continuity_p165d7 import claim,arbitrate,fixtures,GOALS,run
class P165D7Tests(unittest.TestCase):
 def test_goal_changes_relevance_not_evidence(self):
  evidence=fixtures()
  before=repr(evidence)
  a=arbitrate("LOCATE",evidence);z=arbitrate("INTERPRET_SYMBOL",evidence)
  self.assertNotEqual(a["focused"],z["focused"])
  self.assertEqual(repr(evidence),before)
  self.assertEqual(set(a["relevance_order"]),set(z["relevance_order"]))
 def test_symbol_not_promoted_to_physical_observation(self):
  x=arbitrate("INTERPRET_SYMBOL",fixtures())
  self.assertFalse(x["priority_is_evidence"])
  self.assertIn("symbol",x["focused"])
  self.assertNotIn("symbol",arbitrate("LOCATE",fixtures())["focused"])
 def test_contradictions_do_not_disappear(self):
  for goal in GOALS:
   o=arbitrate(goal,fixtures())
   self.assertIn("alternative",o["contradiction_ids"])
   self.assertEqual(o["status"],"MULTI")
   self.assertFalse(o["epistemically_resolved"])
 def test_invalid_and_duplicate_evidence_rejected(self):
  with self.assertRaises(ValueError):claim("x","imaginary","OBSERVED","x","sensor")
  x=fixtures()[0]
  with self.assertRaises(ValueError):arbitrate("LOCATE",[x,x])
 def test_report_preserve(self):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/"d7"
   r=run(path)
   self.assertEqual(r["goal_count"],len(GOALS))
   self.assertFalse(r["d6_tracker_connected"])
   with self.assertRaises(ValueError):run(path)
if __name__=="__main__":unittest.main()
