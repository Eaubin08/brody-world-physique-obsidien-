import tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.color_agnostic_perception_p165d3 import components,detect_sequence,ambiguity_and_motion,run
from brody_world_physique.hard_scene_angles_p165d2 import draw
class P165D3Tests(unittest.TestCase):
 def test_both_red_and_blue(self):
  for color in ((215,40,50),(28,120,220)):
   im=Image.new("RGB",(168,96),(233,228,216))
   ImageDraw.Draw(im).ellipse((45,43,55,53),fill=color)
   c=components(im);self.assertEqual(len(c),1);self.assertLess(abs(c[0]["x"]-50),1)
   im.close()
 def test_two_objects_not_unjustifiably_fused(self):
  im=Image.new("RGB",(168,96),(233,228,216));d=ImageDraw.Draw(im)
  d.ellipse((35,43,45,53),fill=(215,40,50))
  d.ellipse((85,43,95,53),fill=(28,120,220))
  self.assertEqual(len(components(im)),2);im.close()
 def test_evaluator_without_oracle_input(self):
  images,truth=draw(dict(angle=25,motion="linear",occlusion="none",appearance="blue",background="plain"),5)
  try:
   v=ambiguity_and_motion(detect_sequence(images))
   self.assertEqual(len(v["candidates"]),7)
   self.assertFalse(v["unique_identity_proven"])
  finally:
   for im in images:im.close()
 def test_limited_report_no_overwrite(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/"report"
   r=run(p,seeds=2,limit=5)
   self.assertEqual(r["exams"],10)
   self.assertFalse(r["run_complete"])
   self.assertTrue((p/"EXAMS.jsonl").exists())
   with self.assertRaises(ValueError):run(p,seeds=2,limit=5)
if __name__=="__main__":unittest.main()
