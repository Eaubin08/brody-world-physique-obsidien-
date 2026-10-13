import tempfile,json,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_reciprocal_generation_school_v1 import encode_training,reconstruct,assess,validate
class ReciprocalTests(unittest.TestCase):
 def make(self,path,colour,x=8):
  im=Image.new("RGB",(64,64),"white");ImageDraw.Draw(im).rectangle((x,12,x+20,45),fill=colour);im.save(path)
 def test_train_generate_holdout_without_image_copy(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);a=root/"r.png";b=root/"b.png";self.make(a,"red");self.make(b,"blue")
   manifest=root/"courses.json"
   manifest.write_text(json.dumps([{"identity":"red","examples":[str(a)]},{"identity":"blue","examples":[str(b)]}]))
   result=encode_training(manifest,root/"memory.json")
   self.assertEqual(result["identities"],2)
   rendered=reconstruct(root/"memory.json",root/"renders")
   self.assertEqual(rendered["reconstructions"],2)
   self.assertNotEqual((root/"renders"/"prototype_001.png").read_bytes(),a.read_bytes())
   exam=root/"exams";exam.mkdir();self.make(exam/"unseen.png","red",11)
   report=assess(root/"memory.json",exam,root/"exam-output")
   self.assertEqual(report["cases"],1)
   self.assertTrue(report["generations_from_stored_prototypes"])
   self.assertFalse(report["semantic_generation_proven"])
 def test_exam_leak_and_corrupt_memory_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);a=root/"a.png";self.make(a,"green")
   course=root/"courses.json";course.write_text(json.dumps({"identity":"green","examples":[str(a)]}))
   encode_training(course,root/"m.json")
   exams=root/"exams";exams.mkdir();(exams/"same.png").write_bytes(a.read_bytes())
   with self.assertRaises(ValueError):assess(root/"m.json",exams,root/"out")
   p=json.loads((root/"m.json").read_text());p["identities"]["green"]["status"]="VERIFIED"
   (root/"tampered.json").write_text(json.dumps(p))
   with self.assertRaises(ValueError):validate(root/"tampered.json")
if __name__=="__main__":unittest.main()
