import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_reciprocal_shape_learning_p134 import run,scene,compare
class ReciprocalSchoolTests(unittest.TestCase):
 def picture(self,root,group,shape):
  file=root/f"{group}.png";im=Image.new("RGB",(64,64),"white");d=ImageDraw.Draw(im)
  if shape=="circle":d.ellipse((10,10,26,26),fill="red")
  elif shape=="square":d.rectangle((10,10,26,26),fill="blue")
  else:d.polygon([(10,26),(18,10),(26,26)],fill="green")
  im.putpixel((0,0),(230+len(group)%20,)*3);im.save(file)
  return str(file)
 def test_train_correct_holdout_different_shapes(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   rows=[{"group":f"train{i}","split":"train","file":self.picture(root,f"train{i}","circle")} for i in range(3)]
   rows+= [{"group":"heldout-circle","split":"exam","file":self.picture(root,"heldout-circle","circle")},
           {"group":"heldout-triangle","split":"exam","file":self.picture(root,"heldout-triangle","triangle")}]
   m=root/"dataset.json";m.write_text(json.dumps(rows))
   r=run(m,root/"output")
   self.assertEqual(r["train_count"],3)
   self.assertEqual(r["exam_count"],2)
   self.assertGreaterEqual(r["exam_candidates"],1)
   self.assertGreaterEqual(r["exam_holds"],1)
   self.assertTrue(all(v["corrected_mae"]<=v["initial_mae"] for v in r["training"]))
   self.assertFalse(r["independent_real_world_proven"])
 def test_fails_closed_for_leaked_image(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);f=self.picture(root,"single","circle")
   rows=[{"group":"A","split":"train","file":f},{"group":"B","split":"exam","file":f}]
   m=root/"bad.json";m.write_text(json.dumps(rows))
   with self.assertRaises(ValueError):run(m,root/"out")
if __name__=="__main__":unittest.main()
