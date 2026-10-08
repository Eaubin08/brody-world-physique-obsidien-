from dataclasses import dataclass
from unittest import TestCase

from brody_world_physique import (
    ExperienceValidationStatusV0,
    MemoryEligibilityV0,
    ProjectionKindV0,
    TransformationEpistemicClassV0,
    TransitionTransformationBindingV0,
    WorldExperienceCandidateV0,
    WorldStateDeltaV0,
    WorldStateProjectionV0,
    WorldTransformationV0,
)


@dataclass(frozen=True)
class TimeEnvelopeStub:
    observed_at: str


@dataclass(frozen=True)
class SpatialFrameStub:
    frame_ref: str


@dataclass(frozen=True)
class WorldStateStub:
    world_state_id: str


class WorldTransformationTests(TestCase):
    def test_observed_transformation_is_descriptive_only(self):
        item = WorldTransformationV0(
            transformation_id="tx-1",
            transformation_kind="OBJECT_TRANSLATION",
            time=TimeEnvelopeStub("2026-10-08T03:00:00Z"),
            actor_ref="human:1",
            target_refs=("object:a",),
            parameters={"dx_m": 1.0},
            spatial_frame=SpatialFrameStub("room:frame"),
            provenance_refs=("camera:1",),
            epistemic_class=TransformationEpistemicClassV0.OBSERVED,
        )
        self.assertEqual(item.epistemic_class, TransformationEpistemicClassV0.OBSERVED)
        self.assertEqual(item.schema_version, "WORLD_TRANSFORMATION_V0")
        self.assertFalse(item.allowed_to_act)
        self.assertFalse(item.execution_authority)
        self.assertEqual(item.decision_authority, "KX108_ONLY")

    def test_proposed_transformation_does_not_become_world_action(self):
        item = WorldTransformationV0(
            transformation_id="tx-proposed",
            transformation_kind="ROTATE_CAMERA",
            time=TimeEnvelopeStub("2026-10-08T03:00:00Z"),
            epistemic_class=TransformationEpistemicClassV0.PROPOSED,
        )
        self.assertEqual(item.epistemic_class.value, "PROPOSED")
        self.assertFalse(item.execution_authority)
        self.assertFalse(item.allowed_to_act)

    def test_execution_authority_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "execution authority"):
            WorldTransformationV0(
                transformation_id="tx-bad",
                transformation_kind="MOVE",
                time=TimeEnvelopeStub("2026-10-08T03:00:00Z"),
                execution_authority=True,
            )

    def test_requires_upstream_time_shape(self):
        with self.assertRaisesRegex(ValueError, "observed_at"):
            WorldTransformationV0(
                transformation_id="tx-bad-time",
                transformation_kind="MOVE",
                time=object(),
            )


class WorldStateProjectionTests(TestCase):
    def test_prediction_wraps_upstream_world_state(self):
        item = WorldStateProjectionV0(
            projection_id="proj-1",
            base_state_ref="world:t0",
            transformation_ref="tx-1",
            projected_state=WorldStateStub("world:t1:predicted"),
            projection_kind=ProjectionKindV0.PREDICTED,
            model_or_rule_ref="rule:constant-velocity-v0",
            generated_at="2026-10-08T03:00:01Z",
            assumptions=("NO_EXTERNAL_FORCE",),
        )
        self.assertEqual(item.projected_state.world_state_id, "world:t1:predicted")
        self.assertEqual(item.projection_kind, ProjectionKindV0.PREDICTED)
        self.assertEqual(item.schema_version, "WORLD_STATE_PROJECTION_V0")
        self.assertFalse(item.allowed_to_act)

    def test_observed_is_not_a_projection_kind(self):
        with self.assertRaises(ValueError):
            WorldStateProjectionV0(
                projection_id="proj-observed",
                base_state_ref="world:t0",
                projected_state=WorldStateStub("world:t1"),
                projection_kind="OBSERVED",
                model_or_rule_ref="bad",
                generated_at="2026-10-08T03:00:01Z",
            )

    def test_requires_upstream_world_state_shape(self):
        with self.assertRaisesRegex(ValueError, "world_state_id"):
            WorldStateProjectionV0(
                projection_id="proj-bad",
                base_state_ref="world:t0",
                projected_state=object(),
                projection_kind=ProjectionKindV0.SIMULATED,
                model_or_rule_ref="sim:v0",
                generated_at="2026-10-08T03:00:01Z",
            )


class WorldStateDeltaTests(TestCase):
    def test_delta_records_discrepancy_without_causal_proof(self):
        item = WorldStateDeltaV0(
            delta_id="delta-1",
            projected_state_ref="proj-1",
            observed_world_state_ref="world:t1:observed",
            expected_changes=("x:+1m",),
            unexpected_changes=("yaw:+2deg",),
            metric_deltas={"position_error_m": 0.12},
            explanation_candidates=("CAMERA_DRIFT",),
        )
        self.assertEqual(item.metric_deltas["position_error_m"], 0.12)
        self.assertEqual(item.schema_version, "WORLD_STATE_DELTA_V0")
        self.assertFalse(item.causal_proof)

    def test_delta_requires_comparison_anchor(self):
        with self.assertRaisesRegex(ValueError, "projected_state_ref or baseline_state_ref"):
            WorldStateDeltaV0(
                delta_id="delta-no-anchor",
                observed_world_state_ref="world:t1",
            )

    def test_delta_cannot_claim_causal_proof(self):
        with self.assertRaisesRegex(ValueError, "causal proof"):
            WorldStateDeltaV0(
                delta_id="delta-causal",
                projected_state_ref="proj-1",
                observed_world_state_ref="world:t1",
                causal_proof=True,
            )


class WorldExperienceCandidateTests(TestCase):
    def test_validated_experience_is_still_not_canonical_memory(self):
        item = WorldExperienceCandidateV0(
            experience_id="exp-1",
            state_before_ref="world:t0",
            transformation_ref="tx-1",
            projection_ref="proj-1",
            state_after_ref="world:t1:observed",
            delta_ref="delta-1",
            outcome="OBJECT_MOVED_AS_EXPECTED",
            replay_refs=("replay:1",),
            validation_status=ExperienceValidationStatusV0.VALIDATED,
            memory_eligibility=MemoryEligibilityV0.REVIEW_REQUIRED,
            candidate_skill_refs=("skill:predict-translation",),
        )
        self.assertEqual(item.validation_status, ExperienceValidationStatusV0.VALIDATED)
        self.assertEqual(item.schema_version, "WORLD_EXPERIENCE_CANDIDATE_V0")
        self.assertFalse(item.canonical_memory)
        self.assertFalse(item.memory_write_allowed)
        self.assertFalse(item.auto_promotion_allowed)

    def test_repeat_count_must_be_positive(self):
        with self.assertRaisesRegex(ValueError, "repeat_count"):
            WorldExperienceCandidateV0(
                experience_id="exp-bad",
                state_before_ref="world:t0",
                state_after_ref="world:t1",
                outcome="UNKNOWN",
                repeat_count=0,
            )

    def test_memory_write_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "canonical memory"):
            WorldExperienceCandidateV0(
                experience_id="exp-write",
                state_before_ref="world:t0",
                state_after_ref="world:t1",
                outcome="UNKNOWN",
                memory_write_allowed=True,
            )

    def test_auto_promotion_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "auto-promote"):
            WorldExperienceCandidateV0(
                experience_id="exp-promote",
                state_before_ref="world:t0",
                state_after_ref="world:t1",
                outcome="UNKNOWN",
                auto_promotion_allowed=True,
            )


class SovereigntyNegativeTests(TestCase):
    def _base_transformation(self, **kwargs):
        payload = dict(
            transformation_id="tx-boundary",
            transformation_kind="MOVE",
            time=TimeEnvelopeStub("2026-10-08T03:00:00Z"),
        )
        payload.update(kwargs)
        return payload

    def test_wrong_decision_authority_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "KX108_ONLY"):
            WorldTransformationV0(
                **self._base_transformation(decision_authority="BRODY")
            )

    def test_allowed_to_decide_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot decide"):
            WorldTransformationV0(
                **self._base_transformation(allowed_to_decide=True)
            )

    def test_allowed_to_act_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cannot act"):
            WorldTransformationV0(
                **self._base_transformation(allowed_to_act=True)
            )

    def test_kernel_mutation_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "kernel"):
            WorldTransformationV0(
                **self._base_transformation(kernel_mutation=True)
            )

    def test_mutable_contract_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "readonly"):
            WorldTransformationV0(
                **self._base_transformation(readonly=False)
            )


class TransitionTransformationBindingTests(TestCase):
    def test_binding_links_existing_transition_without_mutating_upstream(self):
        item = TransitionTransformationBindingV0(
            binding_id="bind-1",
            transition_ref="transition:upstream-1",
            transformation_ref="tx-1",
            provenance_refs=("audit:f0",),
        )
        self.assertEqual(item.transition_ref, "transition:upstream-1")
        self.assertEqual(item.transformation_ref, "tx-1")
        self.assertEqual(
            item.schema_version, "TRANSITION_TRANSFORMATION_BINDING_V0"
        )
        self.assertFalse(item.allowed_to_act)
        self.assertEqual(item.decision_authority, "KX108_ONLY")

    def test_binding_cannot_gain_action_authority(self):
        with self.assertRaisesRegex(ValueError, "cannot act"):
            TransitionTransformationBindingV0(
                binding_id="bind-bad",
                transition_ref="transition:1",
                transformation_ref="tx-1",
                allowed_to_act=True,
            )
