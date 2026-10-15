import tempfile,json,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_unified_continuous_school_v1 import learn,exam
class UnifiedContinuousTests(unittest.TestCase):
 def fixtures(self,root):
  source=root/"lessons";source.mkdir()
  for i in range(4):
   im=Image.new("L",(64,64),255)
   ImageDraw.Draw(im).rectangle((5+i*3,7,15+i*3,45),fill=0)
   im.save(source/(str(i)+".png"))
  labels=root/"labels.json"
  labels.write_text(json.dumps({str(i)+".png":"shape-A" for i in range(4)}))
  return source,labels
 def test_checkpoint_resume_and_cross_cycle(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);src,labels=self.fixtures(root)
   a=learn(src,labels,root/"run1",max_new=2)
   self.assertEqual(a["status"],"PAUSED_CHECKPOINTED")
   b=learn(src,labels,root/"run1")
   self.assertEqual(b["lessons"],4)
   self.assertEqual(b["identities"],1)
   self.assertFalse(b["native_memory_write"])
   run2=root/"run2"
   c=learn(src,labels,run2,root/"run1"/"identity_memory_candidate.json")
   self.assertEqual(c["observations"],4)
 def test_blind_exam_and_leakage(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);src,labels=self.fixtures(root)
   learn(src,labels,root/"run")
   examdir=root/"exam";examdir.mkdir()
   im=Image.new("L",(64,64),255)
   ImageDraw.Draw(im).rectangle((22,5,35,50),fill=0)
   im.save(examdir/"new.png")
   outcome=exam(root/"run"/"identity_memory_candidate.json",examdir,root/"examout")
   self.assertEqual(outcome["cases"],1)
   with self.assertRaises(ValueError):
    exam(root/"run"/"identity_memory_candidate.json",src,root/"leaked")
 def test_manifest_without_labels_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);src,labels=self.fixtures(r)
   labels.write_text("{}")
   with self.assertRaises(ValueError):learn(src,labels,r/"out")
if __name__=="__main__":unittest.main()
