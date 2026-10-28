import tempfile,unittest
from pathlib import Path
from brody_world_physique.reappearance_gate_p165d6 import evaluate_tracks,infer,run
from brody_world_physique.hard_scene_angles_p165d2 import draw
class D6Tests(unittest.TestCase):
 def test_four_correct_not_enough_for_reappearance(self):
  truth=[10,11,12,13,14,15,16]
  tracks=[{"xs":[10,11,12,13,None,90,90]}]
  score=evaluate_tracks(tracks,truth)
  self.assertTrue(score["topk_four_frame_recall"])
  self.assertFalse(score["same_path_pre_post_recall"])
 def test_same_path_reappearance_metric(self):
  t=[10,11,12,13,14,15,16]
  self.assertTrue(evaluate_tracks([{"xs":[10,11,None,None,None,15,16]}],t)["same_path_pre_post_recall"])
 def test_all_hypotheses_propagated_without_oracle(self):
  spec=dict(angle=0,motion="linear",occlusion="full",appearance="blue",background="plain")
  ims,_=draw(spec,18)
  try:
   result=infer(ims,beam=4)
   self.assertEqual(len(result["raw"]["tracks"]),len(result["persistent_hypotheses"]))
   self.assertFalse(result["unique_identity_proven"])
  finally:
   for im in ims:im.close()
 def test_report_persistence(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/"evidence"
   result=run(p,seeds=2,limit=5,beam=4)
   self.assertEqual(result["episodes"],10)
   self.assertFalse(result["full_matrix_complete"])
   with self.assertRaises(ValueError):run(p,seeds=2,limit=5,beam=4)
if __name__=="__main__":unittest.main()
