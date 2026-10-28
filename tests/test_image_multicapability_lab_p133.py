import json,tempfile,unittest
from pathlib import Path
from PIL import Image
from brody_world_physique.image_multicapability_lab_p133 import run,compose,occlusion_hypotheses,mirror_invariant,match
class MulticapabilityTests(unittest.TestCase):
 def test_eight_different_capabilities(self):
  with tempfile.TemporaryDirectory() as d:
   r=run(Path(d)/"lab")
   self.assertEqual(r["cases"],8);self.assertEqual(r["fail"],0)
   self.assertGreaterEqual(r["families"],6)
   self.assertFalse(r["novel_real_world_learning_proven"])
 def test_fail_closed_and_occlusion_uncertainty(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d)
   with self.assertRaises(ValueError):compose([{"shape":"triangle","bbox":[0,0,64,5]}],r/"bad.png")
   self.assertFalse((r/"bad.png").exists())
   compose([{"shape":"rectangle","bbox":[3,3,10,10]},{"shape":"rectangle","bbox":[30,3,39,11]}],r/"two.png")
   compose([{"shape":"rectangle","bbox":[3,3,10,10]}],r/"one.png")
   with Image.open(r/"two.png") as a,Image.open(r/"one.png") as b:
    self.assertEqual(occlusion_hypotheses(a,b)["status"],"DOUBT")
if __name__=="__main__":unittest.main()
