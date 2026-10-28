import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_blind_symbolic_regeneration_p135 import run
class BlindSymbolicTests(unittest.TestCase):
 def picture(self,r,name,shape):
  p=r/(name+".png");im=Image.new("RGB",(64,64),"white");d=ImageDraw.Draw(im)
  if shape=="ellipse":d.ellipse((12,14,30,32),fill="red")
  else:d.polygon([(12,32),(21,14),(30,32)],fill="blue")
  im.putpixel((0,0),(220+len(name)%20,)*3);im.save(p);return str(p)
 def make(self,r):
  rows=[{"split":"train","group":f"lesson-{i}","label":"circle","file":self.picture(r,f"lesson-{i}","ellipse")} for i in range(3)]
  rows.extend([
   {"split":"exam","group":"unseen-circle","file":self.picture(r,"unseen-circle","ellipse"),"prompt":[{"label":"circle","bbox":[12,14,30,32],"rgb":[255,0,0]}]},
   {"split":"exam","group":"unknown-shape","file":self.picture(r,"unknown-shape","triangle"),"prompt":[{"label":"triangle","bbox":[12,14,30,32],"rgb":[0,0,255]}]},
   {"split":"exam","group":"composition","file":self.picture(r,"composition","ellipse"),"prompt":[{"label":"circle","bbox":[12,14,30,32],"rgb":[255,0,0]},{"label":"triangle","bbox":[36,12,50,27]}]}])
  p=r/"dataset.json";p.write_text(json.dumps(rows));return p
 def test_blind_regeneration_known_unknown_and_composition(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);report=run(self.make(r),r/"output")
   self.assertEqual(report["exam"],3)
   self.assertEqual(report["candidates"],1)
   self.assertEqual(report["holds"],2)
   self.assertTrue(report["exam_target_not_used_in_generation"])
   self.assertLess(report["avg_mae_candidates"],5)
   self.assertTrue((r/"output"/"SEALED_BEFORE_EXAM.json").is_file())
 def test_group_leak_rejected_before_output(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);manifest=self.make(r);rows=json.loads(manifest.read_text())
   rows[3]["group"]="lesson-0";manifest.write_text(json.dumps(rows))
   with self.assertRaises(ValueError):run(manifest,r/"forbidden")
   self.assertFalse((r/"forbidden").exists())
if __name__=="__main__":unittest.main()
