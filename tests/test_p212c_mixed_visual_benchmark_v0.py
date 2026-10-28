import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.drawing_school_v1 import render
from brody_world_physique.p211b_frozen_gesture_transfer_v0 import learn,read
from brody_world_physique.p211c_gesture_recomposition_v0 import _remap
from brody_world_physique.p212a_bounded_gesture_revision_v0 import shifted,run as train_case
from brody_world_physique.p212b_frozen_shift_transfer_v0 import train
from brody_world_physique.p212c_mixed_visual_benchmark_v0 import benchmark

class MixedVisualBenchmarkTests(unittest.TestCase):
    def setup_cases(self,folder):
        p=Path(folder);src=p/"train.png"
        im=Image.new("L",(SIDE,SIDE),255);ImageDraw.Draw(im).line((8,8,28,30),fill=0,width=3);im.save(src)
        memory=p/"memory.json";learn(src,memory);_,gestures=read(memory)
        training=[]
        for i in range(2):
            box=[8+i*4,8+i*3,30+i*4,32+i*3]
            layout=p/f"train-layout{i}.json"
            layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[box]}))
            target=p/f"train-target{i}.png";render(shifted(_remap(gestures,box),2,0)).save(target)
            output=p/f"train-output{i}";train_case(memory,layout,target,output)
            training.append(output/"report.json")
        policy=p/"policy.json";train(memory,training,policy)
        cases=[]
        for i,shift in enumerate(((2,0),(0,0),(-2,0))):
            box=[20+i*3,24+i*2,43+i*3,47+i*2]
            layout=p/f"test-layout{i}.json"
            layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[box]}))
            target=p/f"test-target{i}.png";render(shifted(_remap(gestures,box),*shift)).save(target)
            cases.append({"layout":str(layout),"reference":str(target),"label":f"case-{i}"})
        manifest=p/"manifest.json"
        manifest.write_text(json.dumps({"schema":"BRODY_P212C_CASES_V0","cases":cases}))
        return memory,policy,manifest

    def test_mixed_results_and_visual_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            memory,policy,manifest=self.setup_cases(td)
            report=benchmark(memory,policy,manifest,Path(td)/"report")
            self.assertEqual(report["cases"],3)
            self.assertEqual(report["improved"],1)
            self.assertEqual(report["worsened"],2)
            self.assertEqual(report["ties"],0)
            self.assertTrue((Path(td)/"report"/"comparison.png").exists())
            self.assertTrue((Path(td)/"report"/"scores.csv").exists())
            self.assertTrue(all(r["candidate_committed_before_target"] for r in report["samples"]))

    def test_deduplicated_cases_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            memory,policy,manifest=self.setup_cases(td)
            cfg=json.loads(manifest.read_text())
            cfg["cases"][1]["reference"]=cfg["cases"][0]["reference"]
            manifest.write_text(json.dumps(cfg))
            with self.assertRaises(ValueError):benchmark(memory,policy,manifest,Path(td)/"report")
            self.assertFalse((Path(td)/"report").exists())
if __name__=="__main__":unittest.main()
