import tempfile,unittest,json
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_external_visual_gallery_v0 import run
class ExternalGalleryTests(unittest.TestCase):
 def test_gallery_produced_and_no_authority(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);pics=root/"inputs";pics.mkdir()
   image=Image.new("L",(96,96),255)
   ImageDraw.Draw(image).line((10,20,80,70),fill=0,width=4)
   image.save(pics/"line.png")
   result=run(pics,root/"run")
   self.assertEqual(result["cases"],5)
   self.assertEqual(len(list((root/"run"/"gallery").glob("*.png"))),5)
   self.assertFalse(result["native_memory_write"])
   self.assertFalse(result["canonical_promotion"])
   for line in (root/"run"/"receipts.jsonl").read_text().splitlines():
    receipt=json.loads(line)
    self.assertIs(receipt["native_memory_write"],False)
    self.assertIs(receipt["canonical_promotion"],False)
   self.assertFalse(result["blind_generalization_proven"])
 def test_output_must_be_new(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);Image.new("L",(64,64),255).save(root/"input.png")
   existing=root/"already";existing.mkdir()
   with self.assertRaises(ValueError):run(root,existing)
if __name__=="__main__":unittest.main()
