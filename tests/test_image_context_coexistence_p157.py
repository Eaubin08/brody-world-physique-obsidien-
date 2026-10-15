import tempfile,unittest,random
from pathlib import Path
from brody_world_physique.image_context_coexistence_p157 import make,induce,predict,run,CONDITIONS,REQUESTS
class P157Tests(unittest.TestCase):
 def setUp(self):
  self.learn={}
  for regime in ("flat","slope"):
   imgs,_=make(random.Random(17),regime,"clear_"+regime)
   self.learn[regime]=[imgs]
  self.bank=induce(self.learn)
 def tearDown(self):
  for group in self.learn.values():
   for frames in group:
    for im in frames:im.close()
 def test_learn_two_non_overwriting_rules(self):
  self.assertLess(abs(self.bank["flat"]["acceleration"]),.25)
  self.assertLess(self.bank["slope"]["acceleration"],-.7)
 def test_unknown_context_single_holds_and_multiple_kept(self):
  imgs,_=make(random.Random(23),"slope","cue_missing")
  self.assertEqual(predict(imgs,self.bank,"single")["status"],"HOLD")
  alt=predict(imgs,self.bank,"possibilities")
  self.assertEqual(alt["status"],"MULTI")
  self.assertEqual(set(alt["predictions"]),{"flat","slope"})
  for im in imgs:im.close()
 def test_clear_context_selects(self):
  for regime in ("flat","slope"):
   imgs,_=make(random.Random(31),regime,"clear_"+regime)
   answer=predict(imgs,self.bank,"single")
   self.assertEqual(answer["status"],"SELECT")
   self.assertEqual(answer["selected"],regime)
   for im in imgs:im.close()
 def test_full_run_keeps_evidence(self):
  with tempfile.TemporaryDirectory() as td:
   folder=Path(td)/"p157";report=run(folder,minutes=2,lessons_each=10,exam_each=20)
   self.assertEqual(report["conditions_completed"],len(CONDITIONS)*len(REQUESTS))
   self.assertEqual(report["exams"],20*len(CONDITIONS)*len(REQUESTS))
   self.assertFalse(report["physical_law_discovery_proven"])
   self.assertTrue((folder/"FROZEN_CONTEXT_RULES.json").exists())
   with self.assertRaises(ValueError):run(folder,minutes=2,lessons_each=10,exam_each=20)
if __name__=="__main__":unittest.main()
