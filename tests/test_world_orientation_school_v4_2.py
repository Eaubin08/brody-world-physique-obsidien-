"""V4.2: four screen orientations, reciprocity and model-blind reconstruction.

Do NOT present this as semantic identity, an SENS pipeline or true 3-D 360.
"""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from PIL import Image

from brody_world_physique.drawing_school_v1 import run_school as run_v1
from brody_world_physique.instrument_school_v2 import run_school as run_v2
from brody_world_physique.drawing_memory_school_v3 import run_school as run_v3
from brody_world_physique.world_experience_bridge_v4 import build_candidate_world
from brody_world_physique.world_relations_school_v4_1 import (
    run_school as run_v41, inspect_pixels,
)
from brody_world_physique.world_orientation_school_v4_2 import (
    classify_oriented, directed_features, fill_ratio, learn_frame_policy,
    professor_scene, training_fixtures, test_fixtures,
    build, verify, turn_scene, student_reconstruct,
)


class DirectedVisualLearningTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lessons=[]
        for name,orientation,frame in training_fixtures():
            obs=inspect_pixels(frame)
            ratios=[fill_ratio(c) for c in obs["components"]]
            pointed=min(range(2),key=lambda i:ratios[i])
            cls.lessons.append({
                "id":name,"teacher_direction":orientation,
                "features":directed_features(obs,pointed),
            })
        # Feedback from already bounded V4.1 is a scalar measured on prior.
        # The real end-to-end test uses the V4.1 verified memory JSON.
        from brody_world_physique.world_relations_school_v4_1 import (
            learn_relation,
        )
        previous=learn_relation([
            {"id":"near","features":inspect_pixels(professor_scene("NEAR"))["features"],
             "teacher_feedback":"NEAR"},
            {"id":"far","features":inspect_pixels(professor_scene("FAR"))["features"],
             "teacher_feedback":"FAR"},
        ])
        cls.policy=learn_frame_policy(cls.lessons,previous)

    def test_four_observed_cardinals_without_teacher_box_input(self):
        expected={0:"TOP",90:"LEFT",180:"BOTTOM",270:"RIGHT"}
        for angle,orientation in expected.items():
            obs=inspect_pixels(turn_scene(angle,dx=2,dy=2))
            decision=classify_oriented(obs,self.policy)
            self.assertEqual(decision["direction"],orientation)
            self.assertEqual(decision["status"],"CANDIDATE_ONLY")
            self.assertTrue(decision["reciprocal_by_reverse_vector_not_hardcoded_dictionary"])
            self.assertFalse(decision["semantic_identity_proven"])

    def test_inverse_edges_are_derived_not_keyword_swaps(self):
        for angle,expected in [(0,"BOTTOM"),(90,"RIGHT"),
                               (180,"TOP"),(270,"LEFT")]:
            decision=classify_oriented(inspect_pixels(turn_scene(angle)),self.policy)
            self.assertEqual(decision["reciprocal_direction"],expected)
            self.assertNotEqual(decision["direction"],decision["reciprocal_direction"])

    def test_reversed_layout_is_no_longer_mistaken_for_top(self):
        opposite=classify_oriented(inspect_pixels(professor_scene("REVERSED")),self.policy)
        self.assertEqual(opposite["direction"],"BOTTOM")

    def test_unknown_frame_and_diagonal_do_not_get_arbitrary_direction(self):
        src=inspect_pixels(turn_scene(0))
        self.assertEqual(classify_oriented(src,self.policy,frame_ref="UNKNOWN")["status"],
                         "HOLD_UNKNOWN_SPATIAL_FRAME")
        cases={name:img for name,label,img in test_fixtures()}
        self.assertTrue(classify_oriented(inspect_pixels(cases["diagonal_hold"]),
                                          self.policy)["status"].startswith("HOLD"))

    def test_unsupported_single_ambiguous_occluded_are_held(self):
        for name in ["single_component_hold","identical_roles_hold",
                     "occlusion_hold","far_top_hold"]:
            cases={n:img for n,_,img in test_fixtures()}
            choice=classify_oriented(inspect_pixels(cases[name]),self.policy)
            self.assertIsNone(choice["candidate"],name)
            self.assertTrue(choice["status"].startswith("HOLD_"),name)

    def test_cannot_learn_without_four_cardinal_supervision(self):
        with self.assertRaisesRegex(ValueError,"four directions"):
            learn_frame_policy(self.lessons[:2],{"status":"CANDIDATE_LEARNED_THRESHOLD",
                                                 "threshold":1.5})


class EndToEndOrientationReplayTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=TemporaryDirectory()
        cls.base=Path(cls.tmp.name)
        cls.v1=cls.base/"v1"
        cls.v2=cls.base/"v2"
        cls.v3=cls.base/"v3"
        cls.v4=cls.base/"v4.json"
        cls.v41=cls.base/"v41"
        cls.v42=cls.base/"v42"
        run_v1(cls.v1)
        run_v2(cls.v2,prior_school=cls.v1,training_lessons=9)
        run_v3(cls.v3,prior_v2=cls.v2)
        cls.v4.write_text(json.dumps(build_candidate_world(cls.v3))+"\n")
        run_v41(cls.v41,prior_v3=cls.v3,prior_v4=cls.v4)
        cls.result=build(cls.v42,v3=cls.v3,v4=cls.v4,v41=cls.v41)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_competence_world_memory_and_evidence_all_replay(self):
        r=self.result
        self.assertEqual(r["lessons"],8)
        self.assertEqual(r["exams"],11)
        self.assertGreaterEqual(r["correct"],9)
        self.assertGreaterEqual(r["held_unknown"],4)
        self.assertGreaterEqual(r["reciprocal_predictions"],6)
        check=verify(self.v42,v3=self.v3,v4=self.v4,v41=self.v41)
        self.assertEqual(check["status"],
                         "PASS_V4_2_BOUNDED_ORIENTATION_AND_RECIPROCITY_REPLAY")
        self.assertEqual(check["candidate_world_experiences_verified"],11)
        self.assertFalse(check["native_memory_write_allowed"])
        self.assertFalse(check["world_semantics_proven"])

    def test_no_test_teacher_label_or_instructor_boxes_in_student_precommit(self):
        ledger=[json.loads(s) for s in
                (self.v42/"decisions_before_feedback.jsonl").read_text().splitlines()]
        self.assertEqual(len(ledger),11)
        for event in ledger:
            self.assertNotIn("expected",event)
            self.assertNotIn("teacher_label",event)
            self.assertTrue(event["teacher_feedback_unavailable_to_student"])
            self.assertTrue(event["teacher_part_boxes_unavailable_to_student"])
        receipt=json.loads((self.v42/"composition_before_teacher_reveal.json").read_text())
        self.assertFalse(receipt["teacher_target_read_before_student_commit"])
        self.assertFalse(receipt["teacher_box_coordinates_supplied"])

    def test_world_experiences_all_candidate_and_frame_synthetic(self):
        e=json.loads((self.v42/"evaluation.json").read_text())
        self.assertEqual(e["range_of_rotations_tested"],[0,90,180,270])
        self.assertEqual(e["rotation_frame"],"SYNTHETIC_2D_CANVAS_NOT_3D_360")
        self.assertFalse(e["world_state_is_memory"])
        self.assertFalse(e["sens_runtime_executed"])
        self.assertFalse(e["auto_promotion_allowed"])
        self.assertEqual(len(e["world_experience_candidates"]),11)
        for item in e["world_experience_candidates"]:
            self.assertEqual(item["experience"]["memory_eligibility"],"CANDIDATE_ONLY")
            self.assertFalse(item["experience"]["canonical_memory"])
            self.assertFalse(item["experience"]["memory_write_allowed"])
            self.assertFalse(item["delta"]["causal_proof"])
            self.assertFalse(item["transformation"]["execution_authority"])

    def test_composition_and_replay_images_match(self):
        memory=json.loads((self.v42/"world_orientation_memory_candidate.json").read_text())
        img=student_reconstruct(memory["training"],memory["policy"],"LEFT")
        stored=Image.open(self.v42/"images"/"composition_student.png").convert("L")
        self.assertEqual(img.tobytes(),stored.tobytes())
        evaluation=json.loads((self.v42/"evaluation.json").read_text())
        self.assertFalse(evaluation["composition"]["student_saw_target_before_render"])
        self.assertTrue(evaluation["composition"]["role_masks_transformed_by_programmed_motor"])

    def test_mutation_of_negative_reciprocal_receipt_rejected(self):
        filename=self.v42/"evaluation.json"
        backup=filename.read_bytes()
        try:
            payload=json.loads(backup)
            payload["exams"][0]["decision"]["reciprocal"]="BLOCK_TOP_OF_POINTED"
            filename.write_text(json.dumps(payload))
            with self.assertRaises(ValueError):
                verify(self.v42,v3=self.v3,v4=self.v4,v41=self.v41)
        finally:
            filename.write_bytes(backup)

    def test_mutation_of_generated_image_rejected(self):
        path=self.v42/"images"/"composition_student.png"
        good=path.read_bytes()
        try:
            path.write_bytes(good+b"tampered")
            with self.assertRaises(ValueError):
                verify(self.v42,v3=self.v3,v4=self.v4,v41=self.v41)
        finally:
            path.write_bytes(good)

    def test_previous_world_memory_never_modified(self):
        before=self.v4.read_bytes()
        with self.assertRaisesRegex(ValueError,"new V4.2"):
            build(self.v42,v3=self.v3,v4=self.v4,v41=self.v41)
        self.assertEqual(before,self.v4.read_bytes())
