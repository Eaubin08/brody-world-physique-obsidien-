import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.p211b_frozen_gesture_transfer_v0 import learn
from brody_world_physique.p211d_paired_composition_audit_v0 import run
from brody_world_physique.p211e_regression_diagnostic_v0 import audit

class DiagnosticTests(unittest.TestCase):
    def setup_run(self,folder):
        root=Path(folder)
        train=root/"train.png"
        a=Image.new("L",(SIDE,SIDE),255)
        ImageDraw.Draw(a).line((8,10,40,35),fill=0,width=3)
        a.save(train)
        mem=root/"mem.json";learn(train,mem)
        cases=[]
        for i in range(2):
            lay=root/f"layout{i}.json"
            lay.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0",
                "boxes":[[4,4,24,24],[30,30,SIDE-4,SIDE-4]]}))
            target=root/f"target{i}.png"
            im=Image.new("L",(SIDE,SIDE),255)
            if i==0:ImageDraw.Draw(im).line((5,5,22,22),fill=0,width=3)
            im.save(target)
            cases.append({"layout":str(lay),"reference":str(target)})
        # P2.11d refuses duplicate layout paths; use distinct layout files.
        cfg=root/"manifest.json"
        cfg.write_text(json.dumps({"schema":"BRODY_P211D_MANIFEST_V0",
            "memory":str(mem),"cases":cases}))
        generated=root/"generation"
        run(cfg,generated)
        return cfg,generated,cases

    def test_partial_and_empty_targets_flagged_without_learning(self):
        with tempfile.TemporaryDirectory() as td:
            cfg,generated,_=self.setup_run(td)
            result=audit(cfg,generated,Path(td)/"diagnostic.json")
            self.assertEqual(result["cases"],2)
            self.assertEqual(result["goal_mismatches"],2)
            self.assertEqual(result["rows"][0]["goal_status"],"PARTIAL_REFERENCE")
            self.assertEqual(result["rows"][1]["goal_status"],"INVALID_GOAL_EMPTY_TARGET")
            self.assertTrue(all(x["posthoc_best"]=="UNDETERMINED_GOAL_MISMATCH" for x in result["rows"]))
            self.assertFalse(result["test_feedback_used_for_learning"])

    def test_candidate_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            cfg,generated,_=self.setup_run(td)
            Image.new("L",(SIDE,SIDE),0).save(generated/"case0.png")
            with self.assertRaises(ValueError):audit(cfg,generated,Path(td)/"diagnostic.json")

    def test_reference_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            cfg,generated,cases=self.setup_run(td)
            Image.new("L",(SIDE,SIDE),0).save(cases[0]["reference"])
            with self.assertRaises(ValueError):audit(cfg,generated,Path(td)/"diagnostic.json")

if __name__=="__main__":unittest.main()
