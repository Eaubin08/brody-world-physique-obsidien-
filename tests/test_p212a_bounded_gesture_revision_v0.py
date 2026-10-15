import tempfile,json,unittest
from pathlib import Path
from PIL import Image,ImageDraw
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.p211b_frozen_gesture_transfer_v0 import learn
from brody_world_physique.p212a_bounded_gesture_revision_v0 import run
class RevisionTests(unittest.TestCase):
    def data(self,root,blank=False):
        r=Path(root);training=r/"train.png";m=r/"memory.json";layout=r/"layout.json";target=r/"target.png"
        im=Image.new("L",(SIDE,SIDE),255);ImageDraw.Draw(im).line((12,12,36,30),fill=0,width=3);im.save(training)
        learn(training,m)
        layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[[12,12,38,32]]}))
        ref=Image.new("L",(SIDE,SIDE),255)
        if not blank:ImageDraw.Draw(ref).line((14,12,40,32),fill=0,width=3)
        ref.save(target)
        return m,layout,target
    def test_seal_all_proposals_then_score_and_keep_history(self):
        with tempfile.TemporaryDirectory() as td:
            memory,layout,target=self.data(td)
            out=Path(td)/"output";result=run(memory,layout,target,out)
            self.assertEqual(len(result["attempts"]),5)
            self.assertTrue(all(Path(x["path"]).exists() for x in result["attempts"]))
            self.assertTrue(result["proposals_committed_before_reference_scoring"])
            self.assertFalse(result["test_feedback_used_for_learning"])
            self.assertLessEqual(result["best_error_px"],result["baseline_error_px"])
            self.assertTrue(result["all_failed_attempts_preserved"])
    def test_blank_reference_does_not_improve_revision(self):
        with tempfile.TemporaryDirectory() as td:
            m,l,t=self.data(td,blank=True)
            r=run(m,l,t,Path(td)/"out")
            self.assertEqual(r["selected_index"],0)
    def test_invalid_layout_or_existing_output_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            m,l,t=self.data(td)
            l.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[[1,1,SIDE,SIDE]]}))
            with self.assertRaises(ValueError):run(m,l,t,Path(td)/"out")
            self.assertFalse((Path(td)/"out").exists())
            l.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[[2,2,40,40]]}))
            (Path(td)/"out").mkdir()
            with self.assertRaises(ValueError):run(m,l,t,Path(td)/"out")
if __name__=="__main__":unittest.main()
