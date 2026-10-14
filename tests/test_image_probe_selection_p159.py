import tempfile,unittest,random
from pathlib import Path
from brody_world_physique.image_probe_selection_p159 import (
    learn,choose_probe,classify,trajectory,image_at,measure,response,run,CONDITIONS
)
class P159Tests(unittest.TestCase):
 def test_empirical_response_induced_from_pixels(self):
  bank=learn(random.Random(15),10)
  self.assertAlmostEqual(bank["flat"]["tap"],0,delta=.05)
  self.assertAlmostEqual(bank["slope"]["tap"],-1,delta=.05)
  self.assertAlmostEqual(bank["spring"]["tap"],1,delta=.05)
 def test_ex_ante_selection_and_no_useful_probe(self):
  bank=learn(random.Random(13),10)
  self.assertEqual(choose_probe(bank,["observe"])["decision"],"HOLD")
  ans=choose_probe(bank,["observe","tap"])
  self.assertEqual(ans["decision"],"PROBE")
  self.assertEqual(ans["action"],"tap")
 def test_observed_response_known_vs_novel(self):
  bank=learn(random.Random(19),10)
  for regime in ("flat","slope","spring","novel"):
   frames=[image_at(x) for x in trajectory(random.Random(18),regime,"tap")]
   v=response(measure(frames))
   ans=classify(bank,"tap",v)
   if regime=="novel":
    self.assertEqual(ans["decision"],"HOLD")
   else:
    self.assertEqual(ans["decision"],"SELECT")
    self.assertEqual(ans["selected"],regime)
   for frame in frames:frame.close()
 def test_whole_campaign_preserves_proofs(self):
  with tempfile.TemporaryDirectory() as d:
   folder=Path(d)/"p159"
   report=run(folder,minutes=2,lessons_each=10,exam_each=20)
   self.assertEqual(report["conditions_completed"],len(CONDITIONS))
   self.assertEqual(report["episodes"],len(CONDITIONS)*20)
   self.assertFalse(report["probe_selection_uses_exam_truth"])
   self.assertTrue((folder/"FROZEN_PROBE_RESPONSES.json").exists())
   self.assertTrue((folder/"EXAMS.jsonl").exists())
   with self.assertRaises(ValueError):run(folder,minutes=2,lessons_each=10,exam_each=20)
if __name__=="__main__":unittest.main()
