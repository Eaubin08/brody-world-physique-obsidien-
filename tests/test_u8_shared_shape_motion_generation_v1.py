import tempfile,unittest
from pathlib import Path
from brody_world_physique.u8_shared_shape_motion_generation_v1 import run
class SharedShapeMotionTests(unittest.TestCase):
    def test_shared_memory_drives_both_position_and_pixels(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"u8";r=run(root)
            c={x["case"]:x for x in r["cases"]}
            self.assertEqual(c["learned"]["context"],"intervention")
            self.assertEqual(c["learned"]["visual_mae"],0.)
            self.assertEqual(c["retained"]["context"],"clean")
            self.assertEqual(c["retained"]["visual_mae"],0.)
            self.assertIsNone(c["unknown"]["context"])
            self.assertIsNone(c["unknown"]["visual_mae"])
            self.assertTrue((root/"SHARED_MEMORY.json").exists())
            self.assertTrue((root/"learned_future.png").exists())
            self.assertFalse(r["canonical_promotion"])
            self.assertFalse(r["same_object_identity_across_camera_views_proven"])
    def test_output_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"prior";p.mkdir()
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):run(p)
if __name__=="__main__":unittest.main()
