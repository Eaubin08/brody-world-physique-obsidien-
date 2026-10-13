import tempfile,json,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_motion_one_shot_campaign_v1 import run
class EndToEndPhysicsTests(unittest.TestCase):
 def test_complete_demo_is_explicitly_synthetic(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);r=run("demo",root/"demo")
   self.assertTrue(r["synthetic_demonstration_only"])
   self.assertEqual(r["train_episodes"],3)
   self.assertEqual(r["exam_episodes"],3)
   self.assertFalse(r["real_world_generalization_proven"])
   self.assertTrue((root/"demo"/"campaign"/"heldout_ablation"/"EVIDENCE.json").is_file())
 def test_real_source_provenance_required(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);sources=root/"sources";sources.mkdir()
   scene=sources/"recording-A";scene.mkdir()
   for i,y in enumerate((10,14,20,28,38)):
    im=Image.new("RGB",(64,64),"white")
    ImageDraw.Draw(im).ellipse((20,y-3,26,y+3),fill="black")
    im.save(scene/(str(i)+".png"))
   with self.assertRaises(ValueError):run("real",root/"invalid",sources)
if __name__=="__main__":unittest.main()
