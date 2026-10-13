import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_motion_campaign_split_v1 import audit
from brody_world_physique.image_motion_independent_campaign_v1 import campaign
class CampaignTests(unittest.TestCase):
 def make(self,root,group,split,ys):
  directory=root/group;directory.mkdir()
  obs=[]
  for i,y in enumerate(ys):
   p=directory/f"{i}.png"
   im=Image.new("RGB",(64,64),"white")
   ImageDraw.Draw(im).ellipse((23,y-3,29,y+3),fill="black")
   im.save(p)
   if i<4:obs.append({"t":i,"file":str(p)})
  return {"source_group":group,"origin":"synthetic","split":split,
          "observations":obs,"predict_t":4,"actual":str(directory/"4.png")}
 def setup_cases(self,root):
  # Each group has distinct observations/sha and is wholly in one partition.
  rows=[self.make(root,"train1","train",(7,11,17,25,35)),
        self.make(root,"train2","train",(8,13,20,29,40)),
        self.make(root,"exam1","exam",(10,14,20,28,38))]
  p=root/"episodes.json";p.write_text(json.dumps(rows));return p,rows
 def test_grouped_full_campaign(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);manifest,_=self.setup_cases(root)
   report=campaign(manifest,root/"campaign")
   self.assertEqual(report["train_episodes"],2)
   self.assertEqual(report["exam_episodes"],1)
   self.assertTrue(report["memory_frozen_for_heldout"])
   self.assertFalse(report["real_world_generalization_proven"])
   self.assertTrue((root/"campaign"/"heldout_ablation"/"EVIDENCE.json").is_file())
 def test_reject_group_leak(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);manifest,rows=self.setup_cases(root)
   rows[-1]["source_group"]="train1"
   manifest.write_text(json.dumps(rows))
   with self.assertRaises(ValueError):audit(manifest,root/"bad")
   self.assertFalse((root/"bad").exists())
if __name__=="__main__":unittest.main()
