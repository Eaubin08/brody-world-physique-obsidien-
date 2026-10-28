import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.image_adaptive_visual_lab_p138 import run,SKILLS
class AdaptiveLabTests(unittest.TestCase):
 def test_new_scenes_and_all_skill_families(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"experiment"
   result=run(p,minutes=1,maximum=80)
   self.assertEqual(result["episodes"],80)
   self.assertEqual(len(SKILLS),8)
   self.assertTrue(all(s["attempts"]>0 for s in result["family_stats"].values()))
   self.assertEqual(result["stopped_by"],"EPISODE_CAP")
   self.assertEqual(len((p/"EXPERIMENTS.jsonl").read_text().splitlines()),80)
   self.assertFalse(result["training_or_generalization_proven"])
 def test_preserves_evidence_and_bounds(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"experiment";run(p,minutes=1,maximum=80)
   with self.assertRaises(ValueError):run(p,minutes=1,maximum=80)
   with self.assertRaises(ValueError):run(Path(d)/"invalid",minutes=0,maximum=80)
if __name__=="__main__":unittest.main()
