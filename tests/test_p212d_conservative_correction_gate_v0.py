import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.drawing_school_v1 import render
from brody_world_physique.p211b_frozen_gesture_transfer_v0 import learn,read
from brody_world_physique.p211c_gesture_recomposition_v0 import _remap
from brody_world_physique.p212a_bounded_gesture_revision_v0 import shifted,run as train_case
from brody_world_physique.p212b_frozen_shift_transfer_v0 import train
from brody_world_physique.p212d_conservative_correction_gate_v0 import fit,evaluate
class GateTests(unittest.TestCase):
    def setup_data(self,td,mixed=False):
        root=Path(td);src=root/"source.png";img=Image.new("L",(SIDE,SIDE),255)
        ImageDraw.Draw(img).line((8,8,28,30),fill=0,width=3);img.save(src)
        mem=root/"memory.json";learn(src,mem);_,gestures=read(mem)
        receipts=[]
        for i in range(2):
            box=[8+i*5,9+i*4,31+i*5,32+i*4]
            l=root/f"train-layout{i}.json";l.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[box]}))
            target=root/f"train-target{i}.png"
            shift=(-2,0) if mixed and i else (2,0)
            render(shifted(_remap(gestures,box),*shift)).save(target)
            folder=root/f"train{i}";train_case(mem,l,target,folder)
            receipts.append(folder/"report.json")
        policy=root/"policy.json";train(mem,receipts,policy)
        gate=root/"gate.json";fit(policy,receipts,gate)
        cases=[]
        for i,shift in enumerate(((2,0),(0,0),(-2,0))):
            box=[18+i*3,19+i*2,41+i*3,44+i*2]
            layout=root/f"test-layout{i}.json"
            layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[box]}))
            target=root/f"test-target{i}.png"
            render(shifted(_remap(gestures,box),*shift)).save(target)
            cases.append({"label":str(i),"layout":str(layout),"reference":str(target)})
        manifest=root/"test-manifest.json"
        manifest.write_text(json.dumps({"schema":"BRODY_P212C_CASES_V0","cases":cases}))
        return mem,policy,gate,manifest,receipts
    def test_act_and_visible_contradictory_results(self):
        with tempfile.TemporaryDirectory() as td:
            mem,p,g,m,_=self.setup_data(td)
            self.assertEqual(json.loads(g.read_text())["decision"],"ACT")
            r=evaluate(mem,p,g,m,Path(td)/"test")
            self.assertEqual(r["cases"],3)
            self.assertEqual((r["improved"],r["worsened"],r["ties"]),(1,2,0))
            self.assertTrue((Path(td)/"test"/"comparison.png").exists())
            self.assertTrue(all(v["target_hidden_during_decision"] for v in r["samples"]))
    def test_mixed_train_yields_hold(self):
        with tempfile.TemporaryDirectory() as td:
            mem,p,g,m,_=self.setup_data(td,mixed=True)
            self.assertEqual(json.loads(g.read_text())["decision"],"HOLD")
            r=evaluate(mem,p,g,m,Path(td)/"test")
            self.assertEqual((r["improved"],r["worsened"],r["ties"]),(0,0,3))
    def test_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            mem,p,g,m,_=self.setup_data(td)
            doc=json.loads(g.read_text());doc["decision"]="HOLD";g.write_text(json.dumps(doc))
            with self.assertRaises(ValueError):evaluate(mem,p,g,m,Path(td)/"bad")
if __name__=="__main__":unittest.main()
