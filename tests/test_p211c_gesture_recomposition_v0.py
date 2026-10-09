import json,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.p211b_frozen_gesture_transfer_v0 import learn
from brody_world_physique.p211c_gesture_recomposition_v0 import compose

class CompositionTests(unittest.TestCase):
    def prep(self,td):
        t=Path(td);src=t/"train.png";memory=t/"mem.json";layout=t/"layout.json"
        image=Image.new("L",(SIDE,SIDE),255)
        ImageDraw.Draw(image).line((9,12,50,42),fill=0,width=3)
        image.save(src);learn(src,memory)
        layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0",
            "boxes":[[8,8,34,30],[SIDE//2,SIDE//2,SIDE-5,SIDE-5]]}),encoding="utf-8")
        return memory,layout

    def test_recomposition_generates_png_and_blank(self):
        with tempfile.TemporaryDirectory() as td:
            memory,layout=self.prep(td)
            out=Path(td)/"composed.png"
            report=compose(memory,layout,out)
            self.assertTrue(out.is_file())
            self.assertTrue((Path(td)/"composed-blank.png").is_file())
            self.assertEqual(report["boxes"],2)
            self.assertTrue(report["reference_unseen_during_generation"])
            self.assertGreater(report["gestures"],1)

    def test_test_target_only_scores_after_commit(self):
        with tempfile.TemporaryDirectory() as td:
            memory,layout=self.prep(td)
            first=compose(memory,layout,Path(td)/"a.png")
            Image.new("L",(SIDE,SIDE),255).save(Path(td)/"target.png")
            second=compose(memory,layout,Path(td)/"b.png",Path(td)/"target.png")
            self.assertEqual(first["candidate_sha256"],second["candidate_sha256"])
            self.assertEqual(second["verdict"],"WORSENED")

    def test_invalid_layout_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            memory,layout=self.prep(td)
            layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[[0,0,SIDE,SIDE]]}))
            with self.assertRaises(ValueError):
                compose(memory,layout,Path(td)/"bad.png")

    def test_memory_tampering_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            memory,layout=self.prep(td)
            record=json.loads(memory.read_text())
            record["gestures"][0]["points"][0][0]+=1
            memory.write_text(json.dumps(record))
            with self.assertRaises(ValueError):
                compose(memory,layout,Path(td)/"bad.png")
if __name__=="__main__":unittest.main()
