import tempfile,unittest
from pathlib import Path
from brody_world_physique.world_camera_identity_p165d12 import CASES,world,raster,episode,run
from brody_world_physique.reappearance_gate_p165d6 import infer
class WorldCameraIdentityTests(unittest.TestCase):
 def test_world_and_camera_are_distinct(self):
  a=world("OBJECT_MOVES",19);b=world("CAMERA_MOVES",19)
  self.assertNotEqual(a[-1]["main_x"],b[-1]["main_x"])
  self.assertNotEqual(a[-1]["camera_x"],b[-1]["camera_x"])
 def test_compensated_projection_near_constant(self):
  a=world("COMPENSATED_MOTION",10)
  self.assertEqual(len(set(x["main_x"]-x["camera_x"] for x in a)),1)
 def test_camera_only_changes_image_projection(self):
  a=world("CAMERA_MOVES",10)
  self.assertEqual(len(set(x["main_x"] for x in a)),1)
  self.assertEqual(len(set(x["main_x"]-x["camera_x"] for x in a)),7)
 def test_swap_changes_rendered_identity(self):
  a=world("IDENTITY_SWAP",20)
  self.assertEqual(a[2]["rendered_main_identity"],"A")
  self.assertEqual(a[4]["rendered_main_identity"],"B")
 def test_occultation_preserves_latent_world(self):
  a=world("OCCLUSION",20)
  self.assertFalse(a[3]["main_visible"])
  self.assertIsNotNone(a[3]["main_x"])
 def test_oracle_never_passed_to_infer(self):
  ims,oracle=episode("CROSSING",20)
  try:
   r=infer(ims,beam=4)
   self.assertFalse(r["unique_identity_proven"])
   self.assertFalse(r["fixture_label_used"])
  finally:
   for im in ims:im.close()
 def test_renderer_seven_frames_and_replay(self):
  a,ao=episode("CAMERA_MOVES",71)
  b,bo=episode("CAMERA_MOVES",71)
  try:
   self.assertEqual(len(a),7)
   self.assertEqual(ao,bo)
   self.assertEqual([im.tobytes() for im in a],[im.tobytes() for im in b])
  finally:
   for im in a+b:im.close()
 def test_six_families_and_immutable_report(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"d12";r=run(p,seeds=2,beam=4)
   self.assertEqual(r["episodes"],12)
   self.assertEqual(len(r["families"]),len(CASES))
   self.assertEqual(r["families"]["IDENTITY_SWAP"]["identity_proven"],0)
   with self.assertRaises(ValueError):run(p,seeds=2,beam=4)
if __name__=="__main__":unittest.main()
