import tempfile,unittest,json
from pathlib import Path
from PIL import Image
from brody_world_physique.image_blind_router_p144 import run,context_features,pick_router
class BlindRouterTests(unittest.TestCase):
 def test_image_context_not_transform_name(self):
  a=Image.new("RGB",(20,20),(240,10,20))
  b=Image.new("RGB",(20,20),(100,100,100))
  self.assertNotEqual(context_features(a),context_features(b))
 def test_validation_exam_separation(self):
  with tempfile.TemporaryDirectory() as d:
   target=Path(d)/"run"
   r=run(target,minutes=2,train_per_family=30,validation_per_condition=20,exam_per_condition=20)
   self.assertEqual(r["exam_cases"],600)
   self.assertEqual(r["cells_completed"],30)
   self.assertTrue(r["transform_name_hidden_at_runtime"])
   self.assertLess(r["blind_coverage"],1)
   frozen=json.loads((target/"FROZEN_ROUTER.json").read_text())
   self.assertFalse(frozen["exam_labels_used"])
   self.assertFalse(frozen["runtime_requires_transform_name"])
   with self.assertRaises(ValueError):run(target,minutes=2,train_per_family=30,validation_per_condition=20,exam_per_condition=20)
if __name__=="__main__":unittest.main()
