import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.p211b_frozen_gesture_transfer_v0 import learn,read,generate
class FrozenGestureTests(unittest.TestCase):
    def source(self,folder,name,shift=0):
        p=Path(folder)/(name+".png");im=Image.new("L",(SIDE,SIDE),255)
        ImageDraw.Draw(im).line((10+shift,12,60+shift,55),fill=0,width=3)
        im.save(p);return p
    def test_train_then_render_without_test_pixels(self):
        with tempfile.TemporaryDirectory() as td:
            train=self.source(td,"train")
            memory=Path(td)/"memory.json"
            x=learn(train,memory)
            self.assertGreater(len(x["gestures"]),0)
            out=Path(td)/"new.png"
            r=generate(memory,out)
            self.assertTrue(out.exists())
            self.assertTrue(r["sealed_before_test_reference"])
            self.assertEqual(len(x["gestures"]),r["gestures_replayed"])
            self.assertTrue(r["learned_content_reused"])
    def test_reference_only_scores_and_does_not_change_render(self):
        with tempfile.TemporaryDirectory() as td:
            learn(self.source(td,"train"),Path(td)/"memory.json")
            target=self.source(td,"new",shift=10)
            a=generate(Path(td)/"memory.json",Path(td)/"a.png")
            b=generate(Path(td)/"memory.json",Path(td)/"b.png",reference=target)
            self.assertEqual(a["candidate_sha256"],b["candidate_sha256"])
            self.assertIn("candidate_pixel_error",b)
    def test_tamper_and_duplicate_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            memory=Path(td)/"memory.json";src=self.source(td,"train")
            learn(src,memory)
            with self.assertRaises(ValueError):learn(src,memory)
            obj=json.loads(memory.read_text())
            obj["gestures"][0]["points"][0][0]+=1
            memory.write_text(json.dumps(obj))
            with self.assertRaises(ValueError):read(memory)
    def test_fingerprint_drift_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            memory=Path(td)/"memory.json"
            learn(self.source(td,"train"),memory)
            obj=json.loads(memory.read_text())
            obj["motor_code"]["code_sha256"]="0"*64
            memory.write_text(json.dumps(obj))
            with self.assertRaises(ValueError):read(memory)
if __name__=="__main__":unittest.main()
