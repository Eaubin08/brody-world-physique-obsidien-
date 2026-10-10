import unittest,tempfile,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
from brody_world_physique.image_structural_observation_v1 import describe
from brody_world_physique.image_visual_reflex_teacher_loop_v1 import run
class StructuralObservationTests(unittest.TestCase):
 def test_two_components_with_relations(self):
  a=Image.new("L",(64,64),255);d=ImageDraw.Draw(a)
  d.rectangle((5,6,12,13),fill=0);d.rectangle((42,40,50,49),fill=0)
  r=describe(a)
  self.assertEqual(len(r["parts"]),2)
  self.assertEqual(len(r["relations"]),1)
  self.assertFalse(r["object_identity_known"])
 def test_context_reflects_distinct_geometries(self):
  a=Image.new("L",(64,64),255)
  ImageDraw.Draw(a).rectangle((3,25,56,29),fill=0)
  b=ImageOps.mirror(a.rotate(90))
  self.assertNotEqual(describe(a)["context"],describe(b)["context"])
 def test_school_receipts_include_structures(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);source=root/"inputs";source.mkdir()
   im=Image.new("L",(64,64),255)
   ImageDraw.Draw(im).rectangle((5,6,11,12),fill=0)
   im.save(source/"one.png")
   result=run(source,root/"out")
   self.assertEqual(result["lessons"],1)
   receipt=json.loads((root/"out"/"receipts.jsonl").read_text().splitlines()[0])
   self.assertIn("observed_parts",receipt)
   self.assertIn("observed_relations",receipt)
if __name__=="__main__":unittest.main()
