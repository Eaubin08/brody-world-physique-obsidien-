import json,tempfile,unittest
from pathlib import Path
from brody_world_physique.drawing_school_v0 import SIDE
from PIL import Image,ImageDraw
from brody_world_physique.p211b_frozen_gesture_transfer_v0 import learn,read
from brody_world_physique.p211c_gesture_recomposition_v0 import _remap
from brody_world_physique.p212a_bounded_gesture_revision_v0 import run as train_case,shifted
from brody_world_physique.p212b_frozen_shift_transfer_v0 import train,replay
from brody_world_physique.drawing_school_v1 import render

class ShiftTransferTests(unittest.TestCase):
    def prepare(self,td):
        root=Path(td);source=root/"source.png"
        im=Image.new("L",(SIDE,SIDE),255)
        ImageDraw.Draw(im).line((8,8,28,30),fill=0,width=3);im.save(source)
        memory=root/"mem.json";learn(source,memory)
        _,gestures=read(memory)
        receipts=[]
        for i,b in enumerate(([8,8,30,30],[13,12,38,37])):
            layout=root/f"train-layout{i}.json"
            layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[b]}))
            target=root/f"train-target{i}.png"
            render(shifted(_remap(gestures,b),2,0)).save(target)
            out=root/f"train-run{i}"
            train_case(memory,layout,target,out)
            receipts.append(out/"report.json")
        policy=root/"policy.json"
        train(memory,receipts,policy)
        layout=root/"test-layout.json"
        b=[22,25,48,49]
        layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0","boxes":[b]}))
        target=root/"test-target.png"
        render(shifted(_remap(gestures,b),2,0)).save(target)
        return memory,policy,layout,target

    def test_train_only_shift_improves_unseen_layout(self):
        with tempfile.TemporaryDirectory() as td:
            memory,policy,layout,target=self.prepare(td)
            frozen=json.loads(policy.read_text())
            self.assertEqual(frozen["shift"],[2,0])
            output=Path(td)/"blind"
            r=replay(memory,policy,layout,output,target)
            self.assertTrue(r["target_unseen_for_policy_selection"])
            self.assertEqual(r["verdict"],"IMPROVED")
            self.assertEqual(r["policy_error"],0)
            self.assertTrue((output/"baseline.png").exists())
            self.assertTrue((output/"frozen-policy.png").exists())

    def test_test_target_does_not_change_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            memory,policy,layout,target=self.prepare(td)
            a=replay(memory,policy,layout,Path(td)/"blind")
            b=replay(memory,policy,layout,Path(td)/"scored",target)
            self.assertEqual(a["candidate_sha256"],b["candidate_sha256"])

    def test_policy_tamper_and_train_layout_reuse_fail(self):
        with tempfile.TemporaryDirectory() as td:
            memory,policy,layout,target=self.prepare(td)
            d=json.loads(policy.read_text())
            d["shift"]=[0,0]
            policy.write_text(json.dumps(d))
            with self.assertRaises(ValueError):replay(memory,policy,layout,Path(td)/"tampered")

    def test_duplicate_train_teacher_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            memory,policy,layout,target=self.prepare(td)
            # Using a train teacher reference as TEST must be rejected.
            training_target=Path(td)/"train-target0.png"
            with self.assertRaises(ValueError):
                replay(memory,policy,layout,Path(td)/"duplicate",training_target)

if __name__=="__main__":unittest.main()
