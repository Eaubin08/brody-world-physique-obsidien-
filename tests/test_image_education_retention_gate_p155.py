import tempfile,unittest
from pathlib import Path
from brody_world_physique.image_education_retention_gate_p155 import choose,run,LAWS,WORLD
class P155Tests(unittest.TestCase):
 def test_accept_when_gain_and_retention(self):
  self.assertTrue(choose(1,[(1,2),(2,3)],[(1,2),(2,3)],.1)[0])
 def test_hold_when_retention_degrades(self):
  ok,why=choose(1,[(1,2),(2,3)],[(2,2),(3,3)],.03)
  self.assertFalse(ok);self.assertEqual(why,"HOLD_RETENTION_REGRESSION")
 def test_hold_without_gain(self):
  self.assertFalse(choose(0,[(1,2)],[(1,2)])[0])
 def test_campaign_and_preservation(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"p155"
   a=run(p,minutes=3,lessons_each=8,feedback_each=8,validation_each=8,exam_each=20)
   self.assertEqual(a["exam_cells_completed"],len(LAWS)*len(WORLD))
   self.assertEqual(a["aggregate"]["total_exam"],20*len(LAWS)*len(WORLD))
   self.assertFalse(a["exam_used_for_selection"])
   with self.assertRaises(ValueError):run(p,minutes=3,lessons_each=8,feedback_each=8,validation_each=8,exam_each=20)
if __name__=="__main__":unittest.main()
