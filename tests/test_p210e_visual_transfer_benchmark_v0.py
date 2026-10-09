import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.p210e_visual_transfer_benchmark_v0 import run,learn_offset

class TransferTests(unittest.TestCase):
    def pair(self,root,label,x,y,dx,dy,kind="square"):
        root=Path(root)
        a=Image.new("L",(40,40),255);b=Image.new("L",(40,40),255)
        for im,xx,yy in ((a,x,y),(b,x+dx,y+dy)):
            d=ImageDraw.Draw(im)
            if kind=="square":d.rectangle((xx,yy,xx+4,yy+4),fill=0)
            else:d.ellipse((xx,yy,xx+6,yy+6),fill=0)
        p=root/(label+"-initial.png");q=root/(label+"-target.png")
        a.save(p);b.save(q)
        return {"initial":str(p),"reference":str(q)}

    def execute(self,root,train,test):
        manifest=Path(root)/"input.json";out=Path(root)/"output.json"
        manifest.write_text(json.dumps({"schema":"BRODY_P210E_INPUT_V0","train":train,"test":test}))
        return run(manifest,out)

    def test_train_offset_transfers_to_separate_test_image(self):
        with tempfile.TemporaryDirectory() as td:
            tr=[self.pair(td,"train",3,3,3,2)]
            te=[self.pair(td,"unseen",16,14,3,2,"circle")]
            result=self.execute(td,tr,te)
            self.assertEqual(result["frozen_offset"],{"dx":3,"dy":2})
            self.assertEqual(result["improved"],1)
            self.assertEqual(result["rows"][0]["memory_pixel_error"],0)
            self.assertFalse(result["test_feedback_used_for_learning"])
            self.assertTrue(result["rows"][0]["candidate_committed_before_scoring"])

    def test_transfer_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as td:
            tr=[self.pair(td,"train",3,3,3,2)]
            te=[self.pair(td,"unseen",16,14,-3,-2,"circle")]
            result=self.execute(td,tr,te)
            self.assertEqual(result["test_count"],1)
            self.assertEqual(result["worsened"],1)

    def test_no_train_test_leakage(self):
        with tempfile.TemporaryDirectory() as td:
            tr=[self.pair(td,"train",3,3,3,2)]
            with self.assertRaises(ValueError):self.execute(td,tr,tr)

    def test_ambiguous_train_hold(self):
        with tempfile.TemporaryDirectory() as td:
            tr=[self.pair(td,"one",3,3,3,2),
                self.pair(td,"two",13,13,-2,-1)]
            te=[self.pair(td,"unseen",20,20,3,2)]
            with self.assertRaises(ValueError):self.execute(td,tr,te)

if __name__=="__main__":unittest.main()
