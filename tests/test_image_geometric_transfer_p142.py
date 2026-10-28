import tempfile,unittest,json
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_geometric_transfer_p142 import descriptor,feat_for,run,confidence_predict
class GeometryTransferTests(unittest.TestCase):
 def test_geometry_distinguishes_wide_and_tall(self):
  wide=Image.new("RGB",(96,96),"white");tall=wide.copy()
  ImageDraw.Draw(wide).rectangle((10,30,62,42),fill="red")
  ImageDraw.Draw(tall).rectangle((30,10,42,62),fill="red")
  self.assertGreater(feat_for(wide,"orientation")[0],0)
  self.assertLess(feat_for(tall,"orientation")[0],0)
 def test_destroyed_colour_abstains(self):
  p,why=confidence_predict([([1,0,0],"red")],[0,0,0],["red","blue"],unknown=True)
  self.assertEqual(p,"HOLD")
  self.assertEqual(why,"DESTROYED_CHROMATIC_INFORMATION")
 def test_all_thirty_conditions_and_no_exam_teaching(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/"trial";report=run(p,minutes=2,train_per_family=30,exam_per_cell=20)
   self.assertEqual(report["completed_cells"],30)
   self.assertEqual(report["exam_cases"],600)
   self.assertFalse(report["trained_on_exam"])
   cell=json.loads((p/"CELL_REPORT.json").read_text())
   self.assertEqual(cell["colour/greyscale"]["geometric"]["holds"],20)
   with self.assertRaises(ValueError):run(p,minutes=2,train_per_family=30,exam_per_cell=20)
if __name__=="__main__":unittest.main()
