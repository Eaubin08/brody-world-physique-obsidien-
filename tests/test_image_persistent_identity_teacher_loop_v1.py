import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_persistent_identity_teacher_loop_v1 import run,load
class PersistentIdentityTests(unittest.TestCase):
 def write_image(self,path,offset=0):
  im=Image.new("L",(64,64),255)
  ImageDraw.Draw(im).rectangle((8+offset,12,20+offset,40),fill=0)
  im.save(path)
 def test_multi_session_recall_and_contradiction_quarantine(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);a=root/"a.png";b=root/"b.png";self.write_image(a);self.write_image(b,4)
   lesson=root/"lesson.json";lesson.write_text(json.dumps({"file":str(a),"teacher_identity":"shape-A","teacher_ref":"prof"}))
   one=run(lesson,root/"cycle1")
   self.assertEqual(one["known_identities"],1)
   follow=root/"follow.json";follow.write_text(json.dumps({"file":str(b),"teacher_identity":"shape-A","teacher_ref":"prof"}))
   two=run(follow,root/"cycle2",root/"cycle1"/"identity_memory_candidate.json")
   self.assertEqual(two["distinct_taught_examples"],2)
   clash=root/"clash.json";clash.write_text(json.dumps({"file":str(a),"teacher_identity":"shape-B","teacher_ref":"prof"}))
   three=run(clash,root/"cycle3",root/"cycle2"/"identity_memory_candidate.json")
   self.assertEqual(three["contradictions"],1)
   self.assertEqual(three["known_identities"],1)
 def test_refuse_tampered_state(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"bad.json";p.write_text('{"schema":"BRODY_PERSISTENT_IDENTITY_CANDIDATES_V1","digest":"invalid"}')
   with self.assertRaises(ValueError):load(p)
if __name__=="__main__":unittest.main()
