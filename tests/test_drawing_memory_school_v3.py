"""School V3: visible briefly, hidden during response, delayed/interference and novel composition.

We test boundaries, not claim human-style recall or general visual cognition.
"""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from PIL import Image, ImageDraw

from brody_world_physique.drawing_school_v1 import run_school as run_v1
from brody_world_physique.instrument_school_v2 import run_school as run_v2
from brody_world_physique.drawing_memory_school_v3 import (
    observe_only, _verify_representation, draw_from_snapshot,
    teacher_hidden_model, teacher_new_composition,
    assemble_from_prior_skills, verify_school, run_school,
)


class HiddenMemoryContractTests(TestCase):
    def test_teacher_representation_has_no_png_bytes_and_is_hash_bound(self):
        source=teacher_hidden_model()
        import hashlib
        src=hashlib.sha256(source.tobytes()).hexdigest()
        rep=observe_only(source,"teacher:unseen",src)
        self.assertFalse(rep["source_pixels_in_memory"])
        self.assertTrue(rep["representation_contains_detailed_contour"])
        self.assertFalse(rep["interpretation_semantic"])
        self.assertNotIn("source_bitmap",rep)
        self.assertGreater(len(_verify_representation(rep,src)),0)
        rep["bbox"]=[0,0,0,0]
        with self.assertRaisesRegex(ValueError,"receipt modified"):
            _verify_representation(rep,src)

    def test_render_after_observation_uses_snapshot_not_the_hidden_source(self):
        source=teacher_hidden_model()
        import hashlib
        h=hashlib.sha256(source.tobytes()).hexdigest()
        rep=observe_only(source,"teacher:unique",h)
        choice={"chosen_tool":"PEN"}
        original=draw_from_snapshot(rep,choice,h).tobytes()
        # Overwrite the original reference *after* encoding: drawing takes
        # no image or image path and must be invariant to changed source.
        ImageDraw.Draw(source).rectangle((0,0,63,63),fill=0)
        self.assertEqual(draw_from_snapshot(rep,choice,h).tobytes(),original)

    def test_untrusted_gesture_and_unknown_tool_are_rejected(self):
        source=teacher_hidden_model()
        import hashlib
        h=hashlib.sha256(source.tobytes()).hexdigest()
        rep=observe_only(source,"teacher:unique",h)
        with self.assertRaisesRegex(ValueError,"authorised"):
            draw_from_snapshot(rep,{"chosen_tool":None},h)
        with self.assertRaisesRegex(ValueError,"unexpected/altered"):
            draw_from_snapshot(rep,{"chosen_tool":"PEN"},"0"*64)


class EndToEndHiddenMemoryTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=TemporaryDirectory()
        cls.root=Path(cls.temp.name)
        cls.prior_v1=cls.root/"v1"
        run_v1(cls.prior_v1)
        cls.prior_v2=cls.root/"v2"
        run_v2(cls.prior_v2,prior_school=cls.prior_v1,training_lessons=9)
        cls.school=cls.root/"v3"
        cls.result=run_school(cls.school,prior_v2=cls.prior_v2)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_immediate_delayed_and_unobserved_transfer_all_verified(self):
        out=self.result
        self.assertEqual(out["episodes"],3)
        self.assertTrue(out["reference_hidden_during_drawing"])
        self.assertFalse(out["native_memory_write_allowed"])
        score=json.loads((self.school/"evaluation.json").read_text())
        self.assertEqual(score["episodes"],3)
        self.assertEqual(verify_school(self.school)["episodes_verified"],3)
        receipts=[json.loads(x) for x in
                  (self.school/"committed_before_teacher_reveal.jsonl").read_text().splitlines()]
        self.assertEqual([r["level"] for r in receipts],
                         ["immediate","delayed","transfer"])
        for r in receipts:
            self.assertFalse(r["teacher_reference_read_during_student_step"])
            self.assertFalse(r["teacher_reference_available_to_student_during_drawing"])
            self.assertIn(r["instrument_selection"]["chosen_tool"],("PEN","PENCIL","NIB"))
            self.assertNotIn("teacher_target",r)
            self.assertTrue(r["gestures"])
        self.assertEqual(receipts[1]["distractor_count"],3)
        self.assertEqual(receipts[2]["representation_ref"],None)
        self.assertEqual(receipts[2]["level"],"transfer")

    def test_delayed_reuses_same_persisted_representation_with_interference(self):
        reps=self.school/"representations"
        a=json.loads((reps/"immediate_pentagon.json").read_text())
        b=json.loads((reps/"delayed_pentagon.json").read_text())
        self.assertEqual(a["representation_sha256"],b["representation_sha256"])
        self.assertEqual(a["gestures"],b["gestures"])
        score=json.loads((self.school/"evaluation.json").read_text())
        self.assertEqual(score["results"][0]["score"],score["results"][1]["score"])
        self.assertEqual(len(list((self.school/"interference").glob("task_*.json"))),3)
        self.assertIsNone(score["physical_delay_seconds"])

    def test_no_holdout_composition_reference_observation_prior(self):
        records=[json.loads(x) for x in
                 (self.school/"committed_before_teacher_reveal.jsonl").read_text().splitlines()]
        assert records[2]["level"]=="transfer"
        self.assertEqual([x["skill_ref"] for x in records[2]["composition_task"]],
                         ["cours_carre","cours_triangle"])
        self.assertIsNone(records[2]["representation_sha256"])
        self.assertTrue((self.school/"teacher_revealed"/"transfer_house_reference.png").is_file())
        image=teacher_new_composition()
        self.assertEqual(image.size,(64,64))

    def test_changes_to_student_image_refuse_replay(self):
        path=self.school/"student_images"/"transfer_house_drawing.png"
        good=path.read_bytes()
        try:
            path.write_bytes(good+b"tamper")
            with self.assertRaisesRegex(ValueError,"SHA changed"):
                verify_school(self.school)
        finally:
            path.write_bytes(good)

    def test_changes_to_recollection_or_interference_refuse_replay(self):
        path=self.school/"representations"/"delayed_pentagon.json"
        good=path.read_bytes()
        try:
            content=json.loads(good)
            content["bbox"]=[0,0,0,0]
            path.write_text(json.dumps(content))
            with self.assertRaisesRegex(ValueError,"receipt modified"):
                verify_school(self.school)
        finally:
            path.write_bytes(good)
        path=self.school/"interference"/"task_02.json"
        good=path.read_bytes()
        try:
            data=json.loads(good)
            data["representation_sha256"]="0"*64
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                verify_school(self.school)
        finally:
            path.write_bytes(good)

    def test_output_never_overwrites_existing_results(self):
        with self.assertRaisesRegex(ValueError,"must be fresh"):
            run_school(self.school,prior_v2=self.prior_v2)

    def test_gesture_composition_requires_known_primitive_and_bounded_geometry(self):
        with self.assertRaisesRegex(ValueError,"unknown primitive"):
            assemble_from_prior_skills(self.prior_v1,
                   [{"skill_ref":"import os","box":[0,0,30,30]}])
        with self.assertRaisesRegex(ValueError,"bounds"):
            assemble_from_prior_skills(self.prior_v1,
                   [{"skill_ref":"cours_carre","box":[1,1,70,70]}])
