import tempfile,unittest
from pathlib import Path
from brody_world_physique.hard_scene_angles_p165d2 import (
 ANGLES,MOTIONS,OCCLUSIONS,APPEARANCES,BACKGROUNDS,
 spec_from_index,draw,image_only_evaluate,run
)
class HardSceneTests(unittest.TestCase):
 def test_full_factorial_unique(self):
  specs=[spec_from_index(i) for i in range(675)]
  self.assertEqual(len(set(tuple(s.items()) for s in specs)),675)
  self.assertEqual(len(ANGLES)*len(MOTIONS)*len(OCCLUSIONS)*len(APPEARANCES)*len(BACKGROUNDS),675)
 def test_pixel_only_evaluator_has_no_oracle_interface(self):
  spec=spec_from_index(0);frames,truth=draw(spec,21)
  try:
   d=image_only_evaluate(frames)
   self.assertEqual(len(d["positions"]),7)
   self.assertFalse(d["unique_identity_proven"])
   self.assertFalse(d["camera_cause_proven"])
  finally:
   for f in frames:f.close()
 def test_forced_ambiguity_must_not_select(self):
  spec=dict(angle=50,motion="jump",occlusion="full",appearance="change",background="parallax")
  ims,_=draw(spec,99)
  try:self.assertNotEqual(image_only_evaluate(ims)["status"],"SELECT")
  finally:
   for im in ims:im.close()
 def test_small_matrix_then_no_overwrite(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"hard"
   report=run(p,seeds=2,limit=5)
   self.assertEqual(report["exams"],10)
   self.assertFalse(report["run_complete"])
   self.assertFalse(report["inference_receives_fixture_label"])
   self.assertTrue((p/"EXAMS.jsonl").is_file())
   with self.assertRaises(ValueError):run(p,seeds=2,limit=5)
if __name__=="__main__":unittest.main()
