import random,tempfile,unittest
from pathlib import Path
from brody_world_physique.image_identity_occlusion_p164 import (
 candidates,track,decision,run,STYLES,TEST_LAWS
)
from brody_world_physique.image_hard_visual_ood_p161 import positions,draw_frames
class P164Tests(unittest.TestCase):
 def test_components_from_pixels(self):
  rng=random.Random(2)
  frames,_,_=draw_frames(positions("linear",rng),"canonical",rng)
  c=candidates(frames[0])
  self.assertTrue(c)
  self.assertLess(abs(c[0][1]-48),2)
  for im in frames:im.close()
 def test_track_on_clean_images(self):
  rng=random.Random(3)
  frames,_,_=draw_frames(positions("linear",rng),"canonical",rng)
  paths=track(frames,[0.]*7)
  self.assertEqual(sum(x is not None for x in paths[0]["xs"]),7)
  self.assertEqual(decision(paths).get("selected"),"linear")
  for im in frames:im.close()
 def test_missing_event_never_forced_into_single_truth(self):
  rng=random.Random(4)
  frames,_,_=draw_frames(positions("jump",rng),"occluded",rng)
  ans=decision(track(frames,[0.]*7))
  self.assertIn(ans["status"],("HOLD","MULTI"))
  for im in frames:im.close()
 def test_full_paired_report_and_immutable_evidence(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"p164"
   data=run(p,minutes=3,exam_each=10)
   self.assertEqual(data["episodes"],len(STYLES)*len(TEST_LAWS)*10)
   self.assertEqual(data["cells_completed"],len(STYLES)*len(TEST_LAWS))
   self.assertTrue((p/"EXAMS.jsonl").is_file())
   self.assertFalse(data["real_f12_f16_runtime_connected"])
   with self.assertRaises(ValueError):run(p,minutes=3,exam_each=10)
if __name__=="__main__":unittest.main()
