import random,tempfile,unittest
from pathlib import Path
from brody_world_physique.image_camera_occlusion_gate_p163 import (
 camera_evidence,annotate_fiducials,normalize,decide,track_gate,run,STYLES,TEST_LAWS
)
from brody_world_physique.image_hard_visual_ood_p161 import positions,draw_frames
class P163Tests(unittest.TestCase):
 def test_camera_from_pixels_not_simulator_truth(self):
  rng=random.Random(2)
  original,_,cam=draw_frames(positions("still",rng),"camera",rng)
  stamped=annotate_fiducials(original,"camera",cam)
  shifts=camera_evidence(stamped)
  self.assertIsNotNone(shifts)
  self.assertAlmostEqual(shifts[6],6*cam)
  for im in original+stamped:im.close()
 def test_negative_and_positive_camera_clipping_regression(self):
  # The left marker becomes clipped at -12px, but the central marker must
  # give an unbiased shift. Neither test supplies true motion to estimator.
  from PIL import Image
  for speed in (-2.,2.):
   blanks=[Image.new("RGB",(168,96),(235,233,225)) for _ in range(7)]
   marked=annotate_fiducials(blanks,"camera",speed)
   inferred=camera_evidence(marked)
   self.assertEqual(inferred,[speed*t for t in range(7)])
   for im in blanks+marked:im.close()
 def test_camera_unobservable_must_hold(self):
  self.assertEqual(decide([30.,32.,34.,36.,38.,40.,42.],"UNOBSERVABLE_FRAME")["status"],"HOLD")
 def test_event_hidden_must_hold(self):
  seq=[30.,33.,36.,39.,None,None,50.]
  self.assertEqual(decide(seq,"FRAME_ESTIMATED")["status"],"HOLD")
  self.assertEqual(track_gate(seq)["reason"],"EVENT_MAY_BE_HIDDEN")
 def test_known_stationary_with_cam_corrected(self):
  seq=[42.+2*i for i in range(7)]
  world=normalize(seq,[2.*i for i in range(7)])
  ans=decide(world["xs"],world["status"])
  self.assertEqual(ans.get("selected"),"still")
 def test_complete_matrix_and_no_overwrite(self):
  with tempfile.TemporaryDirectory() as td:
   folder=Path(td)/"p163"
   report=run(folder,minutes=3,exam_each=10)
   self.assertEqual(report["cells_completed"],len(STYLES)*len(TEST_LAWS))
   self.assertEqual(report["episodes"],len(STYLES)*len(TEST_LAWS)*10)
   self.assertFalse(report["real_f12_f16_runtime_connected"])
   self.assertTrue((folder/"EXAMS.jsonl").is_file())
   with self.assertRaises(ValueError):run(folder,minutes=3,exam_each=10)
if __name__=="__main__":unittest.main()
