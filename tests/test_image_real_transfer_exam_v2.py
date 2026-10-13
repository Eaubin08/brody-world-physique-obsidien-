import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_real_transfer_exam_v2 import train,examine,grade
class RealTransferV2Tests(unittest.TestCase):
 def picture(self,p,colour,shift=0):
  im=Image.new("RGB",(64,64),"white")
  ImageDraw.Draw(im).rectangle((7+shift,12,28+shift,40),fill=colour)
  im.save(p)
 def test_training_blind_exam_separate_grading(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);red=root/"red.png";blue=root/"blue.png"
   self.picture(red,"red");self.picture(blue,"blue")
   lessons=root/"lessons.json"
   lessons.write_text(json.dumps([{"identity":"R","examples":[str(red)]},{"identity":"B","examples":[str(blue)]}]))
   self.assertEqual(train(lessons,root/"memory.json")["taught_identities"],2)
   exams=root/"exam";exams.mkdir()
   self.picture(exams/"red2.png","red",2)
   report=examine(root/"memory.json",exams,root/"blind")
   self.assertEqual(report["exam_cases"],1)
   self.assertFalse(report["teacher_labels_available_during_exam"])
   label=root/"labels.json";label.write_text(json.dumps({"red2.png":"R"}))
   counts=grade(root/"blind",label,root/"grade.json")
   self.assertEqual(sum(counts.values()),1)
   self.assertTrue((root/"blind"/"sealed_predictions.jsonl").exists())
 def test_exact_leak_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);im=root/"first.png";self.picture(im,"red")
   lesson=root/"l.json";lesson.write_text(json.dumps([{"identity":"R","examples":[str(im)]}]))
   train(lesson,root/"mem.json")
   cases=root/"cases";cases.mkdir();(cases/"duplicate.png").write_bytes(im.read_bytes())
   with self.assertRaises(ValueError):examine(root/"mem.json",cases,root/"out")
   self.assertFalse((root/"out").exists())
 def test_ambiguous_one_identity_yields_doubt(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);im=root/"a.png";self.picture(im,"blue")
   l=root/"l.json";l.write_text(json.dumps({"identity":"B","examples":[str(im)]}))
   train(l,root/"mem.json")
   q=root/"new";q.mkdir();self.picture(q/"test.png","blue",4)
   result=examine(root/"mem.json",q,root/"out")
   self.assertEqual(result["doubts"],1)
if __name__=="__main__":unittest.main()
