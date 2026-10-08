"""V4 tests: a candidate world index is NOT canonical memory or SENS truth."""
from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from brody_world_physique.drawing_school_v1 import run_school as v1_school
from brody_world_physique.instrument_school_v2 import run_school as v2_school
from brody_world_physique.drawing_memory_school_v3 import run_school as v3_school
from brody_world_physique.world_experience_bridge_v4 import (
    build_candidate_world, verify_world_bundle,
    _spatial_relation_from_instructed_boxes,
)


class V4WorldExperienceTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = TemporaryDirectory()
        cls.root = Path(cls.tmp.name)
        cls.v1 = cls.root / "v1"
        cls.v2 = cls.root / "v2"
        cls.v3 = cls.root / "v3"
        v1_school(cls.v1)
        v2_school(cls.v2, prior_school=cls.v1, training_lessons=9)
        v3_school(cls.v3, prior_v2=cls.v2)
        cls.output = cls.root / "world-view-v4.json"
        cls.view = build_candidate_world(cls.v3)
        cls.output.write_text(json.dumps(cls.view, indent=2) + "\n", encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_actual_upstream_contract_ownership_and_local_experience_type(self):
        result = verify_world_bundle(self.v3, self.output)
        self.assertEqual(result["status"], "PASS_WORLD_VIEW_DERIVED_FROM_VERIFIED_EXPERIENCES")
        self.assertEqual(result["world_observations"], 6)
        self.assertEqual(result["candidate_experiences"], 3)
        self.assertGreaterEqual(result["relation_candidates"], 8)
        self.assertTrue(result["v3_replayed"])
        self.assertFalse(result["world_understanding_proven"])
        self.assertFalse(result["sens_runtime_executed"])
        self.assertFalse(self.view["canonical_world_state_constructed"])
        self.assertFalse(self.view["semantic_boundary"]["world_state_is_memory"])
        self.assertFalse(self.view["semantic_boundary"]["timestamp_as_freshness_authority"])

    def test_observation_truth_provenance_and_source_identity(self):
        world = self.view["views"]
        self.assertEqual(len(world["candidate_entities"]), 3)
        self.assertEqual(
            world["candidate_entities"][0]["reference_identity_group"],
            world["candidate_entities"][1]["reference_identity_group"])
        self.assertNotEqual(
            world["candidate_entities"][1]["reference_identity_group"],
            world["candidate_entities"][2]["reference_identity_group"])
        self.assertFalse(world["candidate_entities"][0]["same_physical_object_proven"])
        self.assertEqual(
            [x["source_kind"] for x in world["world_observations"]],
            ["SIMULATED", "GENERATED"] * 3)
        self.assertTrue(all(x["causal_status"] == "UNKNOWN"
                            and x["allowed_to_decide"] is False
                            and x["allowed_to_act"] is False
                            and x["memory_object"] is False
                            for x in world["world_observations"]))
        self.assertTrue(all(x["state"]["semantic_label_predicted"] is None
                            and x["state"]["physical_units"] is None
                            for x in world["world_observations"]))

    def test_spatial_relation_is_attached_to_teacher_instruction_not_image_learning(self):
        relation = next(x for x in self.view["views"]["typed_candidate_relations"]
                        if x.get("relation_id") == "rel:instructed:roof-over-base")
        self.assertEqual(relation["relation_kind"], "ABOVE_WITH_HORIZONTAL_OVERLAP")
        self.assertEqual(relation["relation_status"], "DERIVED_FROM_TEACHER_PLACEMENT")
        self.assertFalse(relation["causal_proven"])
        self.assertIn("NOT_AUTONOMOUS_PERCEPTION", relation["inference_source"])
        with self.assertRaisesRegex(ValueError, "does not justify"):
            _spatial_relation_from_instructed_boxes([
                {"skill_ref": "cours_carre", "box": [1,2,3,4]}
            ])

    def test_existing_world_experience_type_is_candidate_only(self):
        for exp in self.view["experience_candidates"]:
            self.assertEqual(exp["schema_version"], "WORLD_EXPERIENCE_CANDIDATE_V0")
            self.assertEqual(exp["validation_status"], "CANDIDATE")
            self.assertEqual(exp["memory_eligibility"], "CANDIDATE_ONLY")
            self.assertFalse(exp["canonical_memory"])
            self.assertFalse(exp["memory_write_allowed"])
            self.assertFalse(exp["auto_promotion_allowed"])
            self.assertEqual(exp["decision_authority"], "KX108_ONLY")
        self.assertTrue(all(x["causal_proof"] is False
                            for x in self.view["views"]["world_state_deltas"]))
        self.assertTrue(all(x["epistemic_class"] == "SIMULATED"
                            for x in self.view["views"]["transformations"]))

    def test_world_view_tamper_and_false_semantics_rejected(self):
        original = self.output.read_bytes()
        try:
            data = json.loads(original)
            data["experience_candidates"][0]["validation_status"] = "VALIDATED"
            self.output.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "inconsistent"):
                verify_world_bundle(self.v3, self.output)
            data = json.loads(original)
            data["semantic_boundary"]["sens_pipeline_executed"] = True
            self.output.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "inconsistent"):
                verify_world_bundle(self.v3, self.output)
        finally:
            self.output.write_bytes(original)

    def test_v3_source_change_is_not_ignored(self):
        target = self.v3 / "teacher_revealed" / "transfer_house_reference.png"
        original = target.read_bytes()
        try:
            target.write_bytes(original + b"changed")
            with self.assertRaises(ValueError):
                build_candidate_world(self.v3)
        finally:
            target.write_bytes(original)
        self.assertEqual(verify_world_bundle(self.v3, self.output)["candidate_experiences"], 3)

    def test_different_episode_representation_not_promoted_to_new_world_discovery(self):
        rel = next(x for x in self.view["views"]["typed_candidate_relations"]
                   if x.get("relation_kind") == "CANDIDATE_SAME_REFERENCE_ACROSS_TRIALS")
        self.assertEqual(rel["continuity_basis"], "EQUAL_SOURCE_SHA256_NOT_OBJECT_TRACKING")
        self.assertFalse(rel["visual_identity_learned"])
        self.assertFalse(rel["physical_identity_proven"])
        self.assertFalse(self.view["semantic_boundary"]["knowledge_promoted"])
