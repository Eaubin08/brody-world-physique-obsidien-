import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.p211b_frozen_gesture_transfer_v0 import learn
from brody_world_physique.p211d_paired_composition_audit_v0 import run

class PairedCompositionTests(unittest.TestCase):
    def prepare(self,root):
        root=Path(root)
        training=root/"training.png"
        im=Image.new("L",(SIDE,SIDE),255)
        ImageDraw.Draw(im).line((10,11,48,39),fill=0,width=3)
        im.save(training)
        memory=root/"memory.json"
        learn(training,memory)
        cases=[]
        for i in range(2):
            layout=root/f"layout{i}.json"
            layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0",
                "boxes":[[3+i*4,3,20+i*4,20],[30,30+i*4,SIDE-4,SIDE-5]]}))
            reference=root/f"target{i}.png"
            target=Image.new("L",(SIDE,SIDE),255)
            if i==0:ImageDraw.Draw(target).line((3,3,20,20),fill=0,width=3)
            target.save(reference)
            cases.append({"layout":str(layout),"reference":str(reference)})
        cfg=root/"manifest.json"
        cfg.write_text(json.dumps({"schema":"BRODY_P211D_MANIFEST_V0",
             "memory":str(memory),"cases":cases}))
        return cfg,cases

    def test_paired_comparison_counts_improvement_and_regression(self):
        with tempfile.TemporaryDirectory() as td:
            config,_=self.prepare(td)
            r=run(config,Path(td)/"result")
            self.assertEqual(r["cases"],2)
            self.assertEqual(r["improved"]+r["worsened"]+r["ties"],2)
            self.assertEqual(r["worsened"],1)
            self.assertTrue(all(x["candidate_precommitted"] for x in r["rows"]))
            self.assertFalse(r["test_feedback_used_for_learning"])

    def test_layout_duplicate_refused(self):
        with tempfile.TemporaryDirectory() as td:
            config,cases=self.prepare(td)
            x=json.loads(config.read_text())
            x["cases"][1]["layout"]=cases[0]["layout"]
            config.write_text(json.dumps(x))
            with self.assertRaises(ValueError):run(config,Path(td)/"result")

    def test_train_test_source_leakage_refused(self):
        with tempfile.TemporaryDirectory() as td:
            config,cases=self.prepare(td)
            x=json.loads(config.read_text())
            x["cases"][0]["reference"]=str(Path(td)/"training.png")
            config.write_text(json.dumps(x))
            with self.assertRaises(ValueError):run(config,Path(td)/"result")

    def test_existing_output_refused(self):
        with tempfile.TemporaryDirectory() as td:
            config,_=self.prepare(td)
            out=Path(td)/"result";out.mkdir()
            with self.assertRaises(ValueError):run(config,out)

if __name__=="__main__":unittest.main()
