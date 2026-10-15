import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_experience_guided_motion_v2 import forecast,correct,load
class GuidedMotionTests(unittest.TestCase):
 def frame(self,path,y):
  im=Image.new("RGB",(64,64),"white")
  ImageDraw.Draw(im).ellipse((26,y-4,34,y+4),fill=(25,25,25))
  im.save(path)
 def prepare(self,root,prefix,values):
  frames=[]
  for index,y in enumerate(values[:-1]):
   path=root/f"{prefix}_{index}.png";self.frame(path,y)
   frames.append({"file":str(path),"t":index})
  observed=root/f"{prefix}_actual.png";self.frame(observed,values[-1])
  manifest=root/f"{prefix}.json";manifest.write_text(json.dumps({"observations":frames,"predict_t":len(frames)}))
  return manifest,observed
 def test_two_lessons_guide_third_forecast(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   m1,a1=self.prepare(root,"one",(8,12,18,26,37))
   first=forecast(m1,root/"forecast1")
   self.assertEqual(first["evidence_source"],"LOCAL_BACKTEST")
   correct(root/"forecast1"/"sealed_forecast.json",a1,root/"correction1")
   m2,a2=self.prepare(root,"two",(10,14,20,28,39))
   forecast(m2,root/"forecast2",root/"correction1"/"candidate_physics_memory.json")
   corrected=correct(root/"forecast2"/"sealed_forecast.json",a2,root/"correction2",root/"correction1"/"candidate_physics_memory.json")
   self.assertEqual(corrected["experiences"],2)
   m3,a3=self.prepare(root,"three",(6,10,16,24,35))
   third=forecast(m3,root/"forecast3",root/"correction2"/"candidate_physics_memory.json")
   self.assertEqual(third["eligible_episodes"],2)
   self.assertEqual(third["evidence_source"],"EXPERIENCE_MATCHED")
   self.assertTrue((root/"forecast3"/"acceleration.png").is_file())
 def test_corrupt_memory_and_feedback_leak_refused(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);m,a=self.prepare(root,"case",(9,13,19,27,38))
   forecast(m,root/"forecast")
   with self.assertRaises(ValueError):
    correct(root/"forecast"/"sealed_forecast.json",root/"case_0.png",root/"bad")
   self.assertFalse((root/"bad").exists())
   correct(root/"forecast"/"sealed_forecast.json",a,root/"correct")
   state=json.loads((root/"correct"/"candidate_physics_memory.json").read_text())
   state["experiences"][0]["context"]="tampered"
   p=root/"tampered.json";p.write_text(json.dumps(state))
   with self.assertRaises(ValueError):load(p)
if __name__=="__main__":unittest.main()
