"""Non-generative F1A guards: source split and evidence preservation."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from brody_world_physique.f1a_three_school_wiring_v1 import (
    _seal_sources, run_f1a,
)

class F1ASafetyTests(unittest.TestCase):
    def test_same_bytes_in_train_and_exam_refused_before_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);train=root/"train";test=root/"test"
            train.mkdir();test.mkdir()
            (train/"a.png").write_bytes(b"same bytes")
            (test/"b.png").write_bytes(b"same bytes")
            labels=root/"labels.json"
            labels.write_text(json.dumps({"a.png":"ball"}),encoding="utf8")
            with self.assertRaisesRegex(ValueError,"TRAIN_EXAM_SOURCE_LEAK"):
                run_f1a(train,labels,test,root/"output")
            self.assertFalse((root/"output").exists())

    def test_prior_output_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);out=root/"output";out.mkdir()
            sentinel=out/"sentinel";sentinel.write_text("untouched")
            with self.assertRaisesRegex(ValueError,"PRESERVE_PRIOR_EVIDENCE"):
                run_f1a("missing","missing","missing",out)
            self.assertEqual(sentinel.read_text(),"untouched")

    def test_seal_uses_training_hashes_not_identity_name(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);train=root/"train";test=root/"test"
            train.mkdir();test.mkdir()
            (train/"a.png").write_bytes(b"train")
            (test/"b.png").write_bytes(b"distinct")
            labels=root/"labels.json"
            labels.write_text(json.dumps({"a.png":"ball"}),encoding="utf8")
            tasks,exams=_seal_sources(train,labels,test)
            self.assertEqual(len(tasks),1)
            self.assertEqual(len(exams),1)
            self.assertNotEqual(tasks[0]["source_sha256"],exams[0]["sha256"])

if __name__=="__main__":
    unittest.main()
