import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_motion_memory_ablation_v1 import run
from brody_world_physique.image_experience_guided_motion_v2 import fresh
from brody_world_physique.fusion_f9_intensive_education_v0 import digest
class PairedMotionAblationTests(unittest.TestCase):
 def frame(self,path,y):
  im=Image.new("RGB",(64,64),"white")
  ImageDraw.Draw(im).ellipse((26,y-4,34,y+4),fill="black");im.save(path)
 def setup(self,r):
  obs=[]
  for i,y in enumerate((8,12,18,26)):
   p=r/f"f{i}.png";self.frame(p,y);obs.append({"file":str(p),"t":i})
  actual=r/"actual.png";self.frame(actual,36)
  cases=r/"cases.json";cases.write_text(json.dumps([{"observations":obs,"predict_t":4,"actual":str(actual)}]))
  memory=fresh()
  memory["digest"]=digest(memory)
  m=r/"memory.json";m.write_text(json.dumps(memory))
  return cases,m,actual
 def test_frozen_memory_matches_baseline_without_experience(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);cases,m,_=self.setup(r)
   report=run(cases,m,r/"result")
   self.assertEqual(report["cases"],1)
   self.assertEqual(report["episodes_available"],0)
   self.assertEqual(report["mean_paired_advantage_px"],0)
   self.assertTrue(report["memory_frozen_during_exam"])
 def test_leakage_protected(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);cases,m,actual=self.setup(r)
   state=json.loads(m.read_text());state.pop("digest")
   state["experiences"].append({"forecast_digest":"example","context":"vertical|speeding_up",
      "feedback_sha256":__import__("hashlib").sha256(actual.read_bytes()).hexdigest(),
      "errors_px":{"STILL":1,"VELOCITY":2,"ACCELERATION":3}})
   state["digest"]=digest(state);m.write_text(json.dumps(state))
   with self.assertRaises(ValueError):run(cases,m,r/"invalid")
   self.assertFalse((r/"invalid").exists())
if __name__=="__main__":unittest.main()
