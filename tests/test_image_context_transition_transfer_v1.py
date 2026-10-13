import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.image_context_transition_transfer_v1 import forecast,correct,context
class ContextTransitionTests(unittest.TestCase):
 def episode(self,root,group,ys,x=30):
  obs=[]
  for i,y in enumerate(ys[:-1]):
   p=root/f"{group}_{i}.png";im=Image.new("RGB",(64,64),"white")
   ImageDraw.Draw(im).ellipse((x-3,y-3,x+3,y+3),fill="black");im.save(p)
   obs.append({"t":i,"file":str(p)})
  actual=root/f"{group}_actual.png";im=Image.new("RGB",(64,64),"white")
  ImageDraw.Draw(im).ellipse((x-3,ys[-1]-3,x+3,ys[-1]+3),fill="black");im.save(actual)
  m=root/f"{group}.json";m.write_text(json.dumps({"source_group":group,"observations":obs,"predict_t":4}))
  return m,actual
 def test_cross_group_context_transition_transfer(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);previous=None
   for i,ys in enumerate(((10,18,26,22,18),(12,20,28,24,20)),1):
    m,actual=self.episode(r,f"teach{i}",ys,x=20+i*4)
    f=r/f"forecast{i}";c=r/f"correction{i}"
    forecast(m,f,previous);correct(f/"sealed_forecast.json",actual,c,previous)
    previous=c/"candidate_transition_memory.json"
   m,actual=self.episode(r,"new_group",(11,19,27,23,19),x=40)
   result=forecast(m,r/"transfer",previous)
   self.assertEqual(result["event"],"REVERSAL")
   self.assertEqual(result["source"],"TRANSFERRED_TRANSITION")
   self.assertEqual(result["matched_groups"],2)
   self.assertTrue((r/"transfer"/"predicted.png").exists())
 def test_insufficient_independent_groups_holds(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);m,a=self.episode(r,"one",(8,16,24,20,16))
   report=forecast(m,r/"output")
   self.assertEqual(report["mode"],"DOUBT")
 def test_corrupted_memory_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);m,a=self.episode(r,"one",(8,16,24,20,16))
   forecast(m,r/"forecast")
   correct(r/"forecast"/"sealed_forecast.json",a,r/"corrected")
   p=json.loads((r/"corrected"/"candidate_transition_memory.json").read_text())
   p["episodes"][0]["source_group"]="tampered";bad=r/"bad.json";bad.write_text(json.dumps(p))
   with self.assertRaises(ValueError):forecast(m,r/"refused",bad)
if __name__=="__main__":unittest.main()
