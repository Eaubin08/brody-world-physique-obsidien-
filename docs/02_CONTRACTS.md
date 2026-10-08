# 02 — Canonical Contract Draft

**Status:** DRAFT FOR F0 AUDIT.  
These contracts must be mapped against existing SENS, MMonde, Native Memory and GPS structures before implementation.

## WorldState

Represents a bounded state of a world at a given temporal reference.

Suggested fields:

```text
world_state_id
observed_at
valid_from / valid_to
reference_frame
entities[]
relations[]
state_variables[]
source_refs[]
uncertainty
competing_hypotheses[]
provenance
```

## Action

An action or transformation candidate.

```text
action_id
actor_ref
target_refs[]
action_type
parameters
started_at
ended_at
source
observed | proposed | simulated
authority_status
```

## Transition

Links a prior state, an action/transformation and a later state.

```text
transition_id
state_before_ref
action_ref
predicted_state_ref?
observed_state_after_ref?
delta_ref?
time_delta
confidence
provenance
```

## PredictedState

A prediction is never an observation.

Required distinction:

```text
kind = PREDICTED
model_or_rule_source
generated_at
prediction_horizon
assumptions[]
uncertainty
```

## ObservedState

An observed state must identify:

```text
kind = OBSERVED
sensor/source
received_at
observed_at
reference_frame
measurement_uncertainty
provenance
```

## StateDelta

Comparison between expected and observed state.

```text
delta_id
predicted_state_ref
observed_state_ref
matched_invariants[]
violated_invariants[]
unexpected_changes[]
missing_expected_changes[]
uncertainty
explanation_candidates[]
```

## ExperienceCandidate

Nothing learned from one event becomes automatically canonical.

```text
experience_id
context_refs[]
state_before_ref
action_ref
prediction_ref?
state_after_ref
delta_ref?
outcome
repeat_count
validation_status
provenance
candidate_skills[]
candidate_invariants[]
memory_eligibility
```

## VisualIR

VisualIR is not a caption.

It should be a structured candidate representation.

```text
visual_ir_id
media_ref
frame_time
camera_or_view_ref?
objects[]
tracks[]
masks[]
relations[]
depth_candidates[]
motion_candidates[]
light_candidates[]
occlusion_candidates[]
reference_frame
provenance
uncertainty
```

## VisualInvariant

```text
invariant_id
target_ref
category = LOCK | FLEX | IGNORE
property
expected_value_or_relation
tolerance
source
confidence
```

Examples:

- LOCK: identity, critical geometry, required object count.
- FLEX: lighting, background, texture, style.
- IGNORE: compression noise, irrelevant microdetail.

## VisualFingerprint

A VisualFingerprint is a compact discriminative signature used to recognize continuity without requiring exact pixel equality.

Possible ingredients:

- embedding candidates;
- shape descriptors;
- proportions;
- segmentation structure;
- track continuity;
- geometric relations;
- MMonde invariants.

It must preserve provenance for every contributing signal.

## GenerationIntent

```text
generation_intent_id
semantic_goal
world_state_refs[]
required_invariants[]
allowed_variations[]
forbidden_changes[]
target_modality
quality_target
compute_budget
latency_budget
```

## GeneratedArtifact

```text
artifact_id
generation_intent_ref
generator_adapter
generator_version
weights_hash
workflow_hash
seed
parameters
created_at
file_hash
```

## ReverseEvaluation

```text
reverse_evaluation_id
artifact_ref
requested_invariants[]
observed_invariants[]
matches[]
violations[]
unknowns[]
severity
candidate_cause[]
```

## Compatibility with existing SENS

F0 must verify whether current:

- OccurrenceClaim
- OccurrenceDerivation
- EventCandidate
- EventRef
- occurrence_status

already cover part of:

- observed transformation;
- temporal event;
- derived occurrence;
- action-consequence relation.

The project must extend existing semantics rather than invent a parallel event language.
