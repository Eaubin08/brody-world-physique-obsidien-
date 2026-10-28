import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image, ImageDraw
from brody_world_physique.drawing_school_v0 import SIDE
from brody_world_physique.fusion_f4_education_journal_v0 import (
    append_event, verify_journal, teach_recorded, test_recorded, readonly_context
)

class EducationJournalTests(unittest.TestCase):
    def source(self,root):
        root.mkdir(parents=True,exist_ok=True)
        p=root/"train.png"
        image=Image.new("L",(SIDE,SIDE),255)
        ImageDraw.Draw(image).rectangle([12,10,33,31],outline=0,width=2)
        image.save(p)
        return p

    def test_retains_training_and_test_as_separate_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/"course"
            source=self.source(root)
            teach_recorded(root,0,"rectangle",source)
            layout=root/"layout.json"
            layout.write_text(json.dumps({"schema":"BRODY_P211C_LAYOUT_V0",
                "boxes":[[5,5,27,27],[35,34,57,56]]}))
            gold=Image.new("L",(SIDE,SIDE),255)
            ImageDraw.Draw(gold).rectangle([5,5,27,27],outline=0,width=2)
            ImageDraw.Draw(gold).rectangle([35,34,57,56],outline=0,width=2)
            teacher=root/"teacher.png";gold.save(teacher)
            result=test_recorded(root,1,"rectangle",layout,teacher,root/"exam")
            self.assertTrue(result["sealed_before_teacher"])
            history=verify_journal(root)
            self.assertEqual([r["kind"] for r in history],["TRAIN_CANDIDATE","HELD_OUT_TEST"])
            view=readonly_context(root,1)
            self.assertEqual(view["skill_ids"],["rectangle"])
            self.assertEqual(view["experience_count"],2)
            self.assertTrue(view["read_only"])
            self.assertTrue((root/"exam"/"comparison.png").exists())

    def test_tamper_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            append_event(root,"OBSERVATION",{"value":1})
            path=root/"education"/"event-0001.json"
            data=json.loads(path.read_text())
            data["payload"]["value"]=999
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                verify_journal(root)
            with self.assertRaises(ValueError):
                append_event(root,"OBSERVATION",{"value":2})

    def test_no_unrecorded_skill_examination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaises(ValueError):
                test_recorded(root,1,"unknown","layout","teacher",root/"exam")

if __name__=="__main__":
    unittest.main()
