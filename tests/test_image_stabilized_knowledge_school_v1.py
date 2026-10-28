import tempfile,unittest
from pathlib import Path
from brody_world_physique.image_stabilized_knowledge_school_v1 import fresh,observe,apply,save,load
class KnowledgeReflexTests(unittest.TestCase):
 def teach(self,state,method="raw",prefix="lesson"):
  for i in range(3):
   observe(state,"stroke/side",method,"prof-1",f"{prefix}-{i}")
 def test_stable_reflex_and_restart(self):
  with tempfile.TemporaryDirectory() as d:
   state=fresh();self.teach(state)
   self.assertEqual(apply(state,"stroke/side")["mode"],"REFLEX")
   save(state,Path(d)/"candidate.json")
   self.assertEqual(apply(load(Path(d)/"candidate.json"),"stroke/side")["procedure"],"raw")
 def test_contradiction_reopens_only_local_context(self):
  state=fresh();self.teach(state)
  self.teach_other(state)
  observe(state,"stroke/side","invert","prof-2","counterexample")
  self.assertEqual(apply(state,"stroke/side")["mode"],"DOUBT")
  self.assertEqual(apply(state,"stroke/side",["other"])["hypotheses"],["raw"])
  self.assertEqual(apply(state,"other")["mode"],"REFLEX")
 def teach_other(self,state):
  for i in range(3):observe(state,"other","raw","prof",f"other-{i}")
 def test_at_most_three_hypotheses(self):
  state=fresh()
  for j,p in enumerate(("raw","invert","threshold","sharpen")):
   for i in range(3):observe(state,f"c{j}",p,"prof",f"c{j}-{i}")
  self.assertEqual(len(apply(state,"novel",[f"c{j}" for j in range(4)])["hypotheses"]),3)
 def test_duplicate_does_not_stabilize(self):
  state=fresh();observe(state,"a","raw","prof","one")
  with self.assertRaises(ValueError):observe(state,"a","raw","prof","one")
  self.assertEqual(apply(state,"a")["mode"],"DOUBT")
if __name__=="__main__":unittest.main()
