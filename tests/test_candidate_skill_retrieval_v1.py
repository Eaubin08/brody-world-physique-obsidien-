"""Retrieval must never execute remembered code or modify Native Memory."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from PIL import Image

from brody_world_physique.candidate_skill_retrieval_v1 import propose_stored_procedure
from brody_world_physique.drawing_school_v1 import run_school


class ProcedureRetrievalTests(TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/"course"
        run_school(self.root)

    def test_visual_question_retrieves_whitelisted_code_and_skill_ref_only(self):
        img=self.root/"teacher_images"/"examen_cercle.png"
        ledger=self.root/"candidate_experience_ledger.jsonl"
        previous=ledger.read_bytes()
        outcome=propose_stored_procedure(self.root,img,max_signature_distance=64)
        self.assertEqual(outcome["status"],"PROCEDURE_CANDIDATE_RECALL_ONLY")
        self.assertTrue(outcome["memory_replay_verified"])
        self.assertEqual(outcome["interpretation"],
                         "8x8_NORMALIZED_INK_SIGNATURE_NOT_SEMANTIC")
        self.assertFalse(outcome["procedure_candidate"]["executing_from_memory_allowed"])
        self.assertFalse(outcome["image_created"])
        self.assertFalse(outcome["native_memory_write_allowed"])
        self.assertFalse(outcome["candidate_confidence_calibrated"])
        self.assertIn("drawing_school_v1.py",
                      outcome["procedure_candidate"]["code_ref"][1]["module_path"])
        self.assertEqual(ledger.read_bytes(),previous,"query must remain readonly")

    def test_blank_reference_returns_hold_with_no_auto_fabricated_skill(self):
        blank=self.root/"empty.png"
        Image.new("L",(64,64),255).save(blank)
        outcome=propose_stored_procedure(self.root,blank)
        self.assertEqual(outcome["status"],"HOLD_EMPTY_OBSERVATION")
        self.assertIsNone(outcome["procedure_candidate"])

    def test_tampered_candidate_memory_refuses_procedure_activation(self):
        path=self.root/"candidate_skill_memory.json"
        data=json.loads(path.read_text())
        data["skills"][0]["status"]="PROMOTED"
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError,"skill memory or event ledger was changed"):
            propose_stored_procedure(self.root,self.root/"teacher_images"/"examen_cercle.png")

    def test_reject_broad_parameters_and_wrong_image_dimensions(self):
        img=self.root/"teacher_images"/"examen_trait.png"
        with self.assertRaisesRegex(ValueError,"bounded retrieval"):
            propose_stored_procedure(self.root,img,max_signature_distance=65)
        other=self.root/"wrong.png"
        Image.new("L",(16,16),0).save(other)
        with self.assertRaisesRegex(ValueError,"64x64"):
            propose_stored_procedure(self.root,other)
