import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_multihypothesis_motion_memory_v1 import forecast,feedback
class MotionModelTests(unittest.TestCase):
 def picture(self,path,y):
  im=Image.new("RGB",(64,64),"white");ImageDraw.Draw(im).ellipse((26,y-4,34,y+4),fill="black");im.save(path)
 def test_competing_hypotheses_and_persistent_correction(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);frames=[]
   for i,y in enumerate((9,12,17,24)):
    p=r/("frame"+str(i)+".png");self.picture(p,y);frames.append({"file":str(p),"t":i})
   manifest=r/"manifest.json"
   manifest.write_text(json.dumps({"observations":frames,"predict_t":4}))
   result=forecast(manifest,r/"forecast")
   self.assertEqual(len(result["model_hypotheses"]),3)
   for name in ("still","velocity","acceleration"):
    self.assertTrue((r/"forecast"/(name+".png")).exists())
   real=r/"actual.png";self.picture(real,33)
   graded=feedback(r/"forecast"/"sealed_forecast.json",real,r/"feedback")
   self.assertEqual(graded["saved_episodes"],1)
   next_run=feedback(r/"forecast"/"sealed_forecast.json",real,r/"feedback2",r/"feedback"/"candidate_experience_memory.json")
   self.assertEqual(next_run["saved_episodes"],1)
 def test_feedback_leakage_refused(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);frames=[]
   for i,y in enumerate((10,14,20,28)):
    p=r/(str(i)+".png");self.picture(p,y);frames.append({"file":str(p),"t":i})
   m=r/"m.json";m.write_text(json.dumps({"observations":frames,"predict_t":4}))
   forecast(m,r/"out")
   with self.assertRaises(ValueError):
    feedback(r/"out"/"sealed_forecast.json",r/"0.png",r/"refused")
   self.assertFalse((r/"refused").exists())
if __name__=="__main__":unittest.main()
