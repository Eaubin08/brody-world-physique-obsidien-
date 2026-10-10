import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_continuous_learning_cycle_v0 import run,load_state,decision
class ContinuousImageCycleTests(unittest.TestCase):
 def test_persistent_learning_across_two_cycles_and_fail_closed(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);imgs=p/"images";imgs.mkdir()
   im=Image.new("L",(64,64),255)
   ImageDraw.Draw(im).line((5,5,53,43),fill=0,width=3);im.save(imgs/"sample.png")
   a=run(imgs,p/"cycle-1",episodes=14)
   previous=p/"cycle-1"/"candidate_skills.json"
   b=run(imgs,p/"cycle-2",previous=previous,episodes=14)
   self.assertEqual(b["cycles_completed"],2)
   self.assertTrue(b["cross_restart_state_supported"])
   self.assertFalse(b["native_memory_write"])
   with self.assertRaises(ValueError):run(imgs,p/"cycle-2",previous=previous,episodes=14)
 def test_corrupt_state_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);f=p/"bad.json"
   f.write_text(json.dumps({"schema":"BRODY_LOCAL_CONTINUOUS_VISION_SKILLS_V0","digest":"FAKE"}))
   with self.assertRaises(ValueError):load_state(f,{})
 def test_no_previous_context_uses_raw(self):
  self.assertEqual(decision({},"sample.png"),"raw")
if __name__=="__main__":unittest.main()
