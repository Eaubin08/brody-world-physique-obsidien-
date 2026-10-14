import tempfile,unittest,random
from pathlib import Path
from brody_world_physique.image_active_context_probe_p158 import trajectory,learn,decide,run,CONDITIONS
class P158Tests(unittest.TestCase):
 def test_early_histories_are_indistinguishable(self):
  a=trajectory("flat","discriminating",random.Random(8))
  b=trajectory("slope","discriminating",random.Random(8))
  for k in range(4):
   self.assertEqual(a[k].tobytes(),b[k].tobytes())
  for img in a+b:img.close()
 def test_probe_distinguishes_rules(self):
  bank=learn(random.Random(13),10)
  self.assertAlmostEqual(bank["flat"],0,delta=.05)
  self.assertAlmostEqual(bank["slope"],-1,delta=.05)
  for name in ("flat","slope"):
   seq=trajectory(name,"discriminating",random.Random(14))
   self.assertEqual(decide(seq[:4],bank,"single")["decision"],"PROBE")
   out=decide(seq[:4],bank,"single",after=seq)
   self.assertEqual(out["decision"],"SELECT")
   self.assertEqual(out["selected"],name)
   for im in seq:im.close()
 def test_hold_or_multi_when_not_identifiable(self):
  bank={"flat":0.,"slope":-1.}
  seq=trajectory("flat","uninformative",random.Random(4))
  self.assertEqual(decide(seq[:4],bank,"single",False)["decision"],"HOLD")
  self.assertEqual(decide(seq[:4],bank,"possibilities")["decision"],"MULTI")
  self.assertEqual(decide(seq[:4],bank,"single",after=seq)["decision"],"SELECT")
  for im in seq:im.close()
 def test_full_campaign_sealed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"p158";r=run(p,minutes=2,lessons_each=10,exam_each=20)
   self.assertEqual(r["episodes"],len(CONDITIONS)*20)
   self.assertEqual(r["conditions_completed"],len(CONDITIONS))
   self.assertFalse(r["probe_design_learned_autonomously"])
   with self.assertRaises(ValueError):run(p,minutes=2,lessons_each=10,exam_each=20)
if __name__=="__main__":unittest.main()
