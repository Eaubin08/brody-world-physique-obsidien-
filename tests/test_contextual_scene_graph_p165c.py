import tempfile,unittest
from pathlib import Path
from brody_world_physique.contextual_scene_graph_p165c import *
class SceneTests(unittest.TestCase):
 def test_order_contradiction(self):
  a,b,e=fixture("contradictory_order")
  self.assertEqual(fuse_scene(a,b,e)["status"],"MULTI")
 def test_unknown_depth_is_not_metric_depth(self):
  a,b,e=fixture("depth_unknown")
  v=fuse_scene(a,b,e)
  self.assertEqual(v["status"],"HOLD")
  self.assertFalse(v["physical_depth_proven"])
 def test_matching_signatures_do_not_prove_identity(self):
  a,b,e=fixture("identity_indistinguishable")
  v=fuse_scene(a,b,e)
  self.assertFalse(v["unique_identity_proven"])
 def test_source_frame_mismatch_holds(self):
  a,b,e=fixture("frame_mismatch")
  self.assertEqual(fuse_scene(a,b,e)["status"],"HOLD")
 def test_contradictory_modalities_yield_multi(self):
  a,b,e=fixture("modal_conflict")
  self.assertEqual(fuse_scene(a,b,e)["status"],"MULTI")
 def test_no_fixed_layer_count(self):
  a,b,e=fixture("occlusion_order")
  self.assertEqual(fuse_scene(a,b,e)["status"],"SCENE_CANDIDATE")
 def test_report_and_preservation(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"report";r=run(p)
   self.assertEqual(r["cases_completed"],len(CASES))
   self.assertFalse(r["real_f12_f16_mmonde_runtime_connected"])
   with self.assertRaises(ValueError):run(p)
if __name__=="__main__":unittest.main()
