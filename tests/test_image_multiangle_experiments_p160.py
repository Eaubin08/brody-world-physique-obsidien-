import tempfile,unittest
from pathlib import Path
from brody_world_physique.image_multiangle_experiments_p160 import (
 train,choose,posterior,decision,trial,run,SCENARIOS
)
import random
class P160Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.model=train(160,10)
 def test_pixels_train_separates_dynamics(self):
  self.assertLess(self.model["slope"]["tap"]["mean"],-.7)
  self.assertGreater(self.model["spring"]["tap"]["mean"],.7)
 def test_no_budget_means_hold(self):
  self.assertIsNone(choose([.25]*4,["tap"],.2,[],self.model,.12))
 def test_posterior_normalized(self):
  p=posterior([.25]*4,"tilt",-2.,self.model,.12)
  self.assertAlmostEqual(sum(p),1.)
  self.assertGreater(p[1],p[0])
 def test_ambiguous_request_retains_options(self):
  result=decision([.25]*4,"possibilities")
  self.assertEqual(result["status"],"MULTI")
  self.assertEqual(len(result["hypotheses"]),4)
  self.assertEqual(decision([.25]*4,"single")["status"],"HOLD")
 def test_compound_campaign_and_preservation(self):
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/"p160"
   report=run(path,minutes=3,lessons_each=10,exam_each=20)
   self.assertEqual(report["conditions_completed"],len(SCENARIOS))
   self.assertEqual(report["exams"],len(SCENARIOS)*20)
   self.assertTrue(report["test_truth_hidden_from_policy"])
   self.assertTrue((path/"FROZEN_RESPONSE_MODELS.json").exists())
   with self.assertRaises(ValueError):run(path,minutes=3,lessons_each=10,exam_each=20)
if __name__=="__main__":unittest.main()
