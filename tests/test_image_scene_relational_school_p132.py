import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_scene_relational_school_p132 import experiment,observe,blank,learn,recall,load
class RelationalSchoolTests(unittest.TestCase):
 def scene(self,root,name,layout):
  p=root/(name+".png");im=Image.new("RGB",(64,64),"white");d=ImageDraw.Draw(im)
  if layout=="horizontal":
   d.rectangle((5,10,12,17),fill="black");d.rectangle((42,10,49,17),fill="black")
  elif layout=="vertical":
   d.rectangle((10,5,17,12),fill="black");d.rectangle((10,42,17,49),fill="black")
  else:
   d.rectangle((5,5,12,12),fill="black");d.rectangle((42,42,49,49),fill="black")
  im.putpixel((0,0),(235+len(name)%12,)*3);im.save(p);return p
 def rows(self,r):
  return [
   {"file":str(self.scene(r,"lesson-a","horizontal")),"split":"train","source_group":"rec-A","teacher":"PAIR-H"},
   {"file":str(self.scene(r,"lesson-bbb","horizontal")),"split":"train","source_group":"rec-B","teacher":"PAIR-H"},
   {"file":str(self.scene(r,"exam-c","horizontal")),"split":"exam","source_group":"rec-C","teacher":"PAIR-H"},
   {"file":str(self.scene(r,"exam-d","vertical")),"split":"exam","source_group":"rec-D","teacher":"PAIR-V"}]
 def test_multi_context_transfer_and_doubt(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);m=r/"input.json";m.write_text(json.dumps(self.rows(r)))
   report=experiment(m,r/"out")
   self.assertEqual(report["train"],2);self.assertEqual(report["exam"],2)
   self.assertEqual(report["candidate_predictions"],1)
   self.assertEqual(report["correct_candidates"],1)
   self.assertEqual(report["holds"],1)
   self.assertTrue((r/"out"/"reconstruction.png").exists())
 def test_provenance_and_teacher_contradiction(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);p=self.scene(r,"lesson","horizontal");s=blank()
   self.assertEqual(learn(s,"A","one",p)["status"],"LEARNED_CANDIDATE")
   with self.assertRaises(ValueError):learn(s,"B","two",p)
   rows=self.rows(r);rows[-1]["source_group"]="rec-A"
   m=r/"bad.json";m.write_text(json.dumps(rows))
   with self.assertRaises(ValueError):experiment(m,r/"refuse")
if __name__=="__main__":unittest.main()
