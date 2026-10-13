import tempfile,unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.image_visible_reference_abstention_v0 import choose_from_pixels,case,run
class VisibleReferenceTests(unittest.TestCase):
 def test_hidden_reference_holds(self):
  self.assertEqual(choose_from_pixels(None,{})["status"],"HOLD_UNOBSERVABLE")
 def test_out_of_catalog_holds(self):
  ref=Image.new("L",(64,64),0)
  choices={"PENCIL":Image.new("L",(64,64),255),"PEN":Image.new("L",(64,64),255),"NIB":Image.new("L",(64,64),255)}
  self.assertEqual(choose_from_pixels(ref,choices)["status"],"HOLD_UNMATCHED_REFERENCE")
 def test_visible_and_hidden_are_distinct(self):
  self.assertTrue(case(2,12)["reference_visible_to_learner"])
  self.assertFalse(case(1,12)["reference_visible_to_learner"])
 def test_100_cases_integrity_and_no_memory(self):
  with tempfile.TemporaryDirectory() as d:
   report=run(Path(d)/"out",100,93)
   self.assertEqual(report["cases"],100)
   self.assertFalse(report["native_memory_write"])
   self.assertFalse(report["semantic_visual_understanding_proven"])
if __name__=="__main__":unittest.main()
