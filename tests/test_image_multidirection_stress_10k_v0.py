import tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_multidirection_stress_10k_v0 import AXES,probe,run
class MultiAxisStressTests(unittest.TestCase):
 def test_adversarial_axes_not_all_same(self):
  im=Image.new("L",(64,64),255)
  ImageDraw.Draw(im).line((4,8,54,49),fill=0,width=3)
  a=probe(im,"invert",12)
  b=probe(im,"mirror",12)
  self.assertNotEqual(a["proposal_sha256"],b["proposal_sha256"])
 def test_140_cases_receipts_and_governance(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);folder=r/"imgs";folder.mkdir()
   im=Image.new("L",(64,64),255)
   ImageDraw.Draw(im).line((8,8,55,55),fill=0,width=2)
   im.save(folder/"a.png")
   report=run(folder,r/"result",140)
   self.assertEqual(report["cases"],140)
   self.assertEqual(len(report["axes"]),len(AXES))
   self.assertFalse(report["native_memory_write"])
 def test_refuse_bad_count(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):run(Path(d),Path(d)/"out",10000)
if __name__=="__main__":unittest.main()
