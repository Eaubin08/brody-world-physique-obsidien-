"""Bounded, falsifiable drawing-school memory and correction contracts."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from PIL import Image

from brody_world_physique.drawing_school_v0 import (
    CandidateExperienceLedgerV0, DrawingSkillCandidateV0, _stroke_catalog,
    black_pixels, bbox_of, choose_memory_seed, draw_strokes,
    practice_drawing, signature_for, verify_candidate_ledger,
)


class DrawingSchoolContractsTests(TestCase):
    def test_no_prior_experience_has_no_seed(self):
        teacher=black_pixels(draw_strokes([(8,16,48,16)]))
        self.assertEqual(choose_memory_seed((),teacher),())

    def test_student_draws_after_teacher_pixel_feedback(self):
        model=draw_strokes([(8,16,48,16)])
        single=[((8,16,48,16),black_pixels(model))]
        attempt=practice_drawing(model,catalog=single,max_strokes=1)
        self.assertGreater(attempt["blank_error_pixels"],0)
        self.assertEqual(attempt["final_error_pixels"],0)
        self.assertEqual(len(attempt["correction_steps"]),1)
        self.assertFalse("shape_name" in attempt)

    def test_candidate_memory_seed_replays_on_translated_reference(self):
        source=draw_strokes([(8,16,48,16)])
        observed=black_pixels(source)
        exemplar=DrawingSkillCandidateV0(
            source_sha256="a"*64,lesson_ref="training",
            source_bbox=bbox_of(observed),signature=signature_for(observed,bbox_of(observed)),
            strokes=((8,16,48,16),), final_pixel_error=0,
        )
        new_source=draw_strokes([(8,40,48,40)])
        target=black_pixels(new_source)
        seed=choose_memory_seed((exemplar,),target)
        self.assertNotEqual(seed,())
        before=practice_drawing(new_source,max_strokes=0,catalog=[])
        after=practice_drawing(new_source,memory=(exemplar,),max_strokes=0,catalog=[])
        self.assertLess(after["final_error_pixels"],before["final_error_pixels"])
        self.assertGreater(after["seed_stroke_count"],0)

    def test_harmful_memory_is_rejected_and_failure_remains_visible(self):
        seen=draw_strokes([(8,16,48,16)])
        pts=black_pixels(seen)
        skill=DrawingSkillCandidateV0(
            source_sha256="a"*64,lesson_ref="old_line",
            source_bbox=bbox_of(pts),signature=signature_for(pts,bbox_of(pts)),
            strokes=((8,16,48,16),),final_pixel_error=0,
        )
        different=draw_strokes([(8,16,48,16),(12,12,52,52),(12,52,52,12)])
        observed=practice_drawing(different,memory=(skill,),max_strokes=0,catalog=[])
        self.assertLessEqual(observed["final_error_pixels"],observed["blank_error_pixels"])
        self.assertIn(observed["memory_recall_status"],(
            "ACCEPTED_CANDIDATE","REJECTED_HARMFUL_RECALL"))

    def test_unrelated_mistaken_skill_does_not_force_bad_drawing(self):
        # Construct a deliberately long stroke, yet reference contains few pixels.
        points=black_pixels(draw_strokes([(24,24,32,24)]))
        skill=DrawingSkillCandidateV0(
            source_sha256="b"*64,lesson_ref="unrelated",
            source_bbox=(0,0,63,63),
            signature=signature_for(points,bbox_of(points)),
            strokes=((0,0,63,63),), final_pixel_error=999,
        )
        response=practice_drawing(draw_strokes([(24,24,32,24)]),
                                  memory=(skill,),max_strokes=0,catalog=[])
        self.assertTrue(response["memory_recall_rejected_as_harmful"])
        self.assertEqual(response["memory_recall_status"],"REJECTED_HARMFUL_RECALL")
        self.assertGreater(response["raw_memory_recall_error_pixels"],
                           response["blank_error_pixels"])
        self.assertEqual(response["final_error_pixels"],
                         response["blank_error_pixels"])

    def test_overprinting_must_not_worsen_target(self):
        picture=draw_strokes([(8,20,40,20)])
        noisy=practice_drawing(picture,max_strokes=2,catalog=[
            ((10,40,50,40),black_pixels(draw_strokes([(10,40,50,40)]))),
        ])
        self.assertEqual(noisy["final_error_pixels"],noisy["blank_error_pixels"])

    def test_candidate_ledger_detects_modified_past_and_refuses_authority(self):
        with TemporaryDirectory() as root:
            folder=Path(root);path=folder/"events.jsonl"
            ledger=CandidateExperienceLedgerV0(path)
            ledger.append({"event":"LESSON_OBSERVATION","source_sha256":"a"*64,
                           "memory_write_allowed":False})
            ledger.append({"event":"DRAWING_ATTEMPT_CORRECTED",
                           "error_pixels":12,"memory_write_allowed":False})
            self.assertEqual(verify_candidate_ledger(path)["verified_records"],2)
            with self.assertRaisesRegex(ValueError,"forbidden"):
                ledger.append({"event":"PROMOTE","memory_write_allowed":True})
            with self.assertRaisesRegex(ValueError,"never overwrite"):
                CandidateExperienceLedgerV0(path)
            before=path.read_text()
            path.write_text(before.replace('"error_pixels": 12','"error_pixels": 13'))
            with self.assertRaisesRegex(ValueError,"integrity"):
                verify_candidate_ledger(path)

    def test_fails_closed_on_wrong_size(self):
        with self.assertRaisesRegex(ValueError,"64x64"):
            black_pixels(Image.new("L",(32,32)))

    def test_real_catalog_is_generic_pen_strokes_not_named_shapes(self):
        options=_stroke_catalog()
        self.assertTrue(300<len(options)<12000)
        self.assertTrue(all(len(stroke)==4 for stroke,mask in options))
        self.assertTrue(all(len(mask)>0 for stroke,mask in options))
