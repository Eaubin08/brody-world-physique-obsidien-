import tempfile,json,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_blind_identity_transfer_v1 import run,build_memory,classify
class BlindIdentityTests(unittest.TestCase):
 def make(self,path,vertical=False):
  im=Image.new("L",(64,64),255)
  if vertical:ImageDraw.Draw(im).rectangle((27,6,35,55),fill=0)
  else:ImageDraw.Draw(im).rectangle((5,28,54,36),fill=0)
  im.save(path)
 def test_label_blind_exam_and_doubt(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);a=r/"a.png";b=r/"b.png";q=r/"q.png"
   self.make(a);self.make(b,True)
   im=Image.new("L",(64,64),255);ImageDraw.Draw(im).rectangle((8,28,54,36),fill=0);im.save(q)
   l=r/"lessons.json";l.write_text(json.dumps([{"identity":"H","examples":[str(a)]},{"identity":"V","examples":[str(b)]}]))
   e=r/"exams.json";e.write_text(json.dumps([{"file":str(q),"teacher_identity":"H"}]))
   result=run(l,e,r/"out")
   self.assertEqual(result["exam_images"],1)
   self.assertTrue(result["identity_labels_hidden_during_prediction"])
   self.assertLessEqual(len(json.loads((r/"out"/"receipts.jsonl").read_text().splitlines()[0])["pre_feedback"]["hypotheses"]),3)
 def test_identical_training_and_exam_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);a=r/"a.png";self.make(a)
   l=r/"l.json";l.write_text(json.dumps({"identity":"H","examples":[str(a)]}))
   e=r/"e.json";e.write_text(json.dumps({"file":str(a)}))
   with self.assertRaises(ValueError):run(l,e,r/"out")
if __name__=="__main__":unittest.main()
