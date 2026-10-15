import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_multiview_identity_school_v0 import run
class MultiviewIdentityTests(unittest.TestCase):
 def test_teacher_group_and_unseen_view_exam(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/"shape.png"
   im=Image.new("L",(64,64),255)
   ImageDraw.Draw(im).rectangle((8,8,45,25),outline=0,width=3);im.save(p)
   m=root/"manifest.json"
   m.write_text(json.dumps([{"identity":"forme-A","examples":[str(p)]}]))
   r=run(m,root/"results")
   self.assertEqual(r["taught_identities"],1)
   self.assertEqual(r["heldout_views"],2)
   self.assertFalse(r["identity_learned_from_pixels"])
   self.assertFalse(r["native_memory_write"])
 def test_powershell_single_object_manifest(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);p=root/"shape.png"
   Image.new("L",(64,64),255).save(p)
   manifest=root/"single.json"
   manifest.write_text(json.dumps({"identity":"single","examples":[str(p)]}))
   r=run(manifest,root/"result")
   self.assertEqual(r["taught_identities"],1)
   self.assertEqual(r["heldout_views"],2)
 def test_refuse_previous_output(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/"results").mkdir()
   with self.assertRaises(ValueError):run(root/"missing.json",root/"results")
if __name__=="__main__":unittest.main()
