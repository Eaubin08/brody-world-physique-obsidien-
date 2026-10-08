"""V4.1 checks visual inference, invariant probes, honest failures and world boundary."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
import json

from PIL import Image

from brody_world_physique.drawing_school_v1 import run_school as school_v1
from brody_world_physique.instrument_school_v2 import run_school as school_v2
from brody_world_physique.drawing_memory_school_v3 import run_school as school_v3
from brody_world_physique.world_experience_bridge_v4 import build_candidate_world
from brody_world_physique.world_relations_school_v4_1 import (
    classify, compose_from_experience, inspect_pixels, learn_relation,
    professor_scene, run_school, verify_school,
)


class VisualPerceptionTests(TestCase):
    def test_detect_parts_directly_from_pixels_no_box_input(self):
        original=professor_scene("NEAR")
        observation=inspect_pixels(original)
        self.assertEqual(observation["component_count"],2)
        self.assertEqual(observation["segmentation"],
                         "BINARY_8_CONNECTED_PIXELS_NO_TEACHER_BOXES")
        self.assertGreater(observation["features"]["normalized_distance"],0)
        self.assertTrue(all(x["pixel_points"] for x in observation["components"]))

    def test_rotation_translation_and_scale_preserve_normalized_distance_approximately(self):
        base=inspect_pixels(professor_scene("NEAR"))["features"]
        for scene in (
            professor_scene("NEAR",dx=6,dy=4),
            professor_scene("NEAR",turn=90),
            professor_scene("NEAR",scale=1.18),
        ):
            new=inspect_pixels(scene)["features"]
            self.assertLess(abs(new["normalized_distance"]-base["normalized_distance"]),.16)
            self.assertLess(abs(new["area_ratio"]-base["area_ratio"]),.15)

    def test_learned_rule_depends_on_feedback_not_teacher_dictionary(self):
        close=inspect_pixels(professor_scene("NEAR"))["features"]
        distant=inspect_pixels(professor_scene("FAR"))["features"]
        lessons=[{"id":"a","features":close,"teacher_feedback":"NEAR"},
                 {"id":"b","features":distant,"teacher_feedback":"FAR"}]
        policy=learn_relation(lessons)
        self.assertEqual(policy["status"],"CANDIDATE_LEARNED_THRESHOLD")
        self.assertEqual(classify(inspect_pixels(professor_scene("NEAR")),policy)["candidate"],"NEAR")
        self.assertEqual(classify(inspect_pixels(professor_scene("FAR")),policy)["candidate"],"FAR")
        swapped=[{**item,"teacher_feedback":("FAR" if item["teacher_feedback"]=="NEAR" else "NEAR")}
                 for item in lessons]
        self.assertEqual(learn_relation(swapped)["status"],"HOLD_NOT_SEPARABLE")

    def test_topology_unknown_holds(self):
        empty=inspect_pixels(Image.new("L",(64,64),255))
        policy={"status":"CANDIDATE_LEARNED_THRESHOLD","threshold":.9}
        self.assertEqual(classify(empty,policy)["status"],"HOLD_UNSUPPORTED_COMPONENT_TOPOLOGY")

    def test_limitations_are_not_semantic_understanding(self):
        observation=inspect_pixels(professor_scene("NEAR",turn=90))
        self.assertEqual(observation["component_count"],2)
        self.assertNotIn("semantic_type",observation)
        self.assertNotIn("object_identity_verified",observation)


class FullWorldRelationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=TemporaryDirectory()
        cls.base=Path(cls.temp.name)
        cls.prior1=cls.base/"v1"
        cls.prior2=cls.base/"v2"
        cls.prior3=cls.base/"v3"
        cls.prior4=cls.base/"v4.json"
        school_v1(cls.prior1)
        school_v2(cls.prior2,prior_school=cls.prior1,training_lessons=9)
        school_v3(cls.prior3,prior_v2=cls.prior2)
        cls.prior4.write_text(json.dumps(build_candidate_world(cls.prior3),indent=2)+"\n")
        cls.school=cls.base/"v4_1"
        cls.report=run_school(cls.school,prior_v3=cls.prior3,prior_v4=cls.prior4)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_drawing_course_replays_and_no_canonical_memory_promotion(self):
        self.assertEqual(self.report["tests"],6)
        self.assertEqual(self.report["verified"],"PASS_WORLD_RELATION_V4_1_BOUNDED_REPLAY")
        self.assertGreaterEqual(self.report["correct"],4)
        r=verify_school(self.school,prior_v3=self.prior3,prior_v4=self.prior4)
        self.assertEqual(r["training_verified"],6)
        self.assertEqual(r["exams_verified"],6)
        self.assertFalse(r["native_memory_write_allowed"])
        self.assertFalse(r["sens_executed"])
        output=json.loads((self.school/"evaluation.json").read_text())
        self.assertEqual(output["relation_attribution"],
                         "PIXEL_COMPONENT_DISTANCE_LEARNED_FROM_LABELED_TEACHER_EXAMPLES")
        self.assertFalse(output["world_identity_verified"])
        self.assertFalse(output["spatial_direction_understood"])
        self.assertFalse(output["auto_promotion_allowed"])
        self.assertFalse(output["no_b8_promotion"] is False)

    def test_v4_1_experiences_reuse_existing_world_types_not_another_memory_authority(self):
        evaluation=json.loads((self.school/"evaluation.json").read_text())
        records=evaluation["world_experience_candidates"]
        self.assertEqual(len(records),6)
        for bundle in records:
            experience=bundle["experience"]
            self.assertEqual(experience["schema_version"],"WORLD_EXPERIENCE_CANDIDATE_V0")
            self.assertEqual(experience["validation_status"],"CANDIDATE")
            self.assertEqual(experience["memory_eligibility"],"CANDIDATE_ONLY")
            self.assertFalse(experience["canonical_memory"])
            self.assertFalse(experience["memory_write_allowed"])
            self.assertFalse(experience["auto_promotion_allowed"])
            self.assertFalse(bundle["transformation"]["execution_authority"])
            self.assertFalse(bundle["delta"]["causal_proof"])
            self.assertTrue(bundle["no_sens_semantic_claim"])
            self.assertEqual(bundle["transformation"]["epistemic_class"],"SIMULATED")
        failed=next(r for r in records if
                    r["experience"]["experience_id"]=="world-exp:v4-1:reversed_hard_negative")
        self.assertEqual(failed["experience"]["outcome"],"CONTRADICTED_BY_TEACHER_FEEDBACK")

    def test_test_decisions_are_committed_without_ground_truth(self):
        receipts=[json.loads(line) for line in
                  (self.school/"choices_before_teacher_feedback.jsonl").read_text().splitlines()]
        self.assertEqual(len(receipts),6)
        for receipt in receipts:
            self.assertNotIn("truth",receipt)
            self.assertFalse(receipt["teacher_label_accessed_before_decision"])
            self.assertTrue(receipt["no_teacher_boxes_provided"])
            self.assertIsNone(receipt["choice"].get("semantic_label_predicted"))
        evaluation=json.loads((self.school/"evaluation.json").read_text())
        self.assertEqual(evaluation["tests"][-1]["truth"],"HOLD")
        self.assertEqual(evaluation["tests"][-1]["decision"]["candidate"],None)

    def test_composer_reuses_observed_pixels_without_teacher_boxes(self):
        data=json.loads((self.school/"world_relation_memory_candidate.json").read_text())
        art=compose_from_experience(data["training"],data["policy"])
        self.assertEqual(art.size,(64,64))
        self.assertEqual(art.tobytes(),Image.open(
            self.school/"images"/"composition_candidate.png").convert("L").tobytes())
        commit=json.loads((self.school/"composition_before_reveal.json").read_text())
        self.assertIsNone(commit["instructed_component_boxes"])
        self.assertIsNone(commit["semantic_object_name_given_to_student"])
        self.assertFalse(commit["target_revealed"])

    def test_altered_training_source_blocks_replay(self):
        path=self.school/"images"/"train_lesson01.png"
        before=path.read_bytes()
        try:
            path.write_bytes(before+b"modification")
            with self.assertRaises(ValueError):
                verify_school(self.school,prior_v3=self.prior3,prior_v4=self.prior4)
        finally:
            path.write_bytes(before)

    def test_false_promotion_and_cooked_evaluation_detected(self):
        path=self.school/"evaluation.json"
        original=path.read_bytes()
        try:
            data=json.loads(original)
            data["native_memory_write_allowed"]=True
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,"untrusted"):
                verify_school(self.school,prior_v3=self.prior3,prior_v4=self.prior4)
        finally:
            path.write_bytes(original)

    def test_upstream_world_not_writable_and_output_no_overwrite(self):
        before=self.prior4.read_bytes()
        with self.assertRaisesRegex(ValueError,"fresh"):
            run_school(self.school,prior_v3=self.prior3,prior_v4=self.prior4)
        self.assertEqual(self.prior4.read_bytes(),before)
