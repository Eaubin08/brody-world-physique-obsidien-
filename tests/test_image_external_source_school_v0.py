import tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_external_source_school_v0 import run,transform
class ExternalSourceSchoolTests(unittest.TestCase):
 def test_external_png_and_all_transforms(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);inp=root/"input";inp.mkdir()
   im=Image.new("L",(80,80),255)
   ImageDraw.Draw(im).line((10,10,70,70),fill=0,width=3)
   im.save(inp/"hand_created.png")
   r=run(inp,root/"out")
   self.assertEqual(r["evaluations"],5)
   self.assertFalse(r["source_authenticity_verified"])
   self.assertFalse(r["image_semantics_proven"])
 def test_empty_folder_fails(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):run(d,Path(d)/"out")
 def test_refuse_existing_output(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);Image.new("L",(64,64),255).save(root/"a.png")
   out=root/"out";out.mkdir()
   with self.assertRaises(ValueError):run(root,out)
if __name__=="__main__":unittest.main()
