# 02 — Canonical Contracts — F0 Freeze Candidate

**Status:** F0 AUDITED / FREEZE CANDIDATE  
**Date:** 2026-10-08  
**Authority:** KX108_ONLY remains external and unchanged.

This file was rewritten after the cross-audit of current Obsidia SENS/Cognition, MMonde, Native Memory and GPS/physical-world sources.

The main F0 result is: **do not rebuild contracts that already exist in Obsidia.**

---

## 1. Canonical contracts already existing upstream

The following names are adopted as-is from the current Obsidia world stack.

### MMonde

Source branch used for the audit:

`obsidia-x108-proofs / feat/r6-sens-cognition-canonical-audit-v0`

Existing contracts:

```text
WorldObservationV0
WorldStateV0
```

Rules already present:

- observation != truth;
- world state != memory;
- world state != cognition;
- world state is candidate reality;
- provenance, uncertainty and contradictions are preserved;
- MMonde is readonly / representation-only;
- no decision and no ACT;
- decision authority remains KX108_ONLY.

**Decision:** this project MUST NOT create a parallel `WorldState` root type.

### Situated world dynamics

Existing contracts:

```text
TimeEnvelopeV0
SpatialFrameRefV0
TypedRelationV0
TransitionV0
TrajectoryV0
RelationStatusV0
ContinuityStatusV0
```

Existing relation distinction:

```text
TEMPORAL
CORRELATED
DERIVED
CAUSAL_ASSERTED
CAUSAL_PROVEN
UNKNOWN
```

`CAUSAL_PROVEN` requires explicit evidence refs.

**Decision:** this project adopts `TransitionV0` and `TrajectoryV0`. It does not create a second generic transition ontology.

### Multimodal transport

Existing contract:

```text
ModalityObservationV0
```

Existing bridge:

```text
ModalityObservationV0
  -> WorldObservationV0
  -> WorldStateV0
```

Important existing fields:

- modality;
- observed_at;
- source_ref;
- source_hash;
- evidence_refs;
- uncertainty;
- contradictions;
- latency;
- frame;
- `generated`;
- causal status.

**Decision:** future visual/audio/sensor organs enter through this bounded transport unless a more specialized upstream contract already exists.

### Measurement and physical evidence

Existing contracts:

```text
InstrumentRefV0
MeasurementContextV0
SituatedMeasurementV0

PhysicalSignalEventV0
SignalContradictionV0
PhysicalRiskHintV0
PhysicalSignalReportV0
WorldStateCandidateV0

EvidenceCompatibilityV0
ReplayablePhysicalEvidenceCandidateV0
```

Existing compatibility axes:

- temporal;
- spatial;
- metric;
- causal;
- source independence.

**Decision:** Brody World Physique does not create a new generic physical-evidence plane.

### Real image

Existing F16 contracts:

```text
ImageAssetRefV0
CaptureContextV0
VisualPrimitiveV0
CandidateInterpretationV0
ImageIntegrityReportV0
RealImageObservationV0
```

`VisualPrimitiveV0` already exposes refs for:

- geometry;
- mask;
- depth;
- motion;
- text;
- features;
- evidence.

`RealImageObservationV0` already preserves:

- immutable asset ref/hash;
- capture context;
- time;
- reference frame;
- latency;
- physical-signal refs;
- prior-state refs;
- candidate interpretations;
- integrity;
- uncertainty;
- contradictions.

It explicitly rejects generated imagery.

**Decision:** do NOT create a second root `VisualIR` that duplicates F16.

The term **VisualIR** may remain as a project-level name for a serialized/derived view over these existing contracts if implementation proves it useful, but it is not a new canonical ontology in F0.

---

## 2. What F0 still needs to add

The audit found four genuinely missing/common contracts for the learning loop.

### 2.1 WorldTransformationV0 — NEW

Do not call this generic object `ActionV0`.

Obsidia already uses **WorldAction** for governed execution/readiness. The learning/world-model layer needs a separate descriptive concept covering an observed, proposed or simulated transformation without granting execution authority.

Proposed contract:

```text
WorldTransformationV0
  transformation_id
  transformation_kind
  actor_ref?
  target_refs[]
  parameters
  time: TimeEnvelopeV0
  spatial_frame: SpatialFrameRefV0?
  provenance_refs[]
  evidence_refs[]
  epistemic_class =
      OBSERVED
    | PROPOSED
    | SIMULATED
    | INFERRED
    | UNKNOWN
  uncertainty[]
  readonly = true
  decision_authority = KX108_ONLY
  allowed_to_decide = false
  allowed_to_act = false
```

Examples:

- an object was physically pushed;
- the camera moved;
- Brody proposes rotating a virtual camera;
- a simulator applies a force;
- an unknown transformation occurred.

**Boundary:** `WorldTransformationV0 != WorldAction execution authority`.

### 2.2 WorldStateProjectionV0 — NEW

A prediction/simulation must never masquerade as an observation.

Rather than inventing a second state schema, the projected state wraps the existing `WorldStateV0`.

```text
WorldStateProjectionV0
  projection_id
  base_state_ref
  transformation_ref?
  projected_state: WorldStateV0
  projection_kind =
      PREDICTED
    | SIMULATED
    | COUNTERFACTUAL
  model_or_rule_ref
  generated_at
  prediction_horizon?
  assumptions[]
  uncertainty[]
  provenance_refs[]
  evidence_refs[]
  readonly = true
  decision_authority = KX108_ONLY
```

Rules:

- projected state != observed state;
- simulated state != evidence of occurrence;
- counterfactual state != history;
- model confidence != physical truth.

### 2.3 WorldStateDeltaV0 — NEW

Comparison between a projection and a later observed/candidate state.

```text
WorldStateDeltaV0
  delta_id
  projected_state_ref?
  baseline_state_ref?
  observed_world_state_ref
  matched_invariant_refs[]
  violated_invariant_refs[]
  expected_changes[]
  unexpected_changes[]
  missing_expected_changes[]
  metric_deltas[]
  continuity_status
  explanation_candidates[]
  uncertainty[]
  contradictions[]
  provenance_refs[]
  readonly = true
```

A delta records discrepancy. It does not prove its cause.

### 2.4 WorldExperienceCandidateV0 — NEW, NON-MEMORY

This is the compact learning episode.

```text
WorldExperienceCandidateV0
  experience_id
  context_refs[]
  state_before_ref
  transformation_ref?
  projection_ref?
  state_after_ref
  delta_ref?
  outcome
  replay_refs[]
  evidence_refs[]
  provenance_refs[]
  repeat_count
  validation_status
  candidate_skill_refs[]
  candidate_invariant_refs[]
  memory_eligibility
  readonly = true
  auto_promotion_allowed = false
```

Important:

`WorldExperienceCandidateV0` is **not itself canonical memory**.

It is a domain/cognitive candidate which may later be adapted into the existing Native Memory `MemoryCandidate` lifecycle.

---

## 3. Native Memory mapping

Current Native Memory already exposes:

```text
MemoryCandidate
MemoryCandidateStatus
MemoryCandidateLedger
PromotionDecision
```

Existing invariants include:

```text
memory_write_allowed = false
auto_promotion_allowed = false
PROMOTED_MANUAL_ONLY requires human review
```

**Decision:** do not invent a second memory-promotion system.

Expected future bridge:

```text
WorldExperienceCandidateV0
        |
        v
experience_to_memory_candidate(...)
        |
        v
MemoryCandidate
        |
        v
existing manual promotion policy
```

F0 gap:

The current `MemorySourceType` enum has no explicit `WORLD_EXPERIENCE` source class.

Do not silently overload another source type. A later upstream change should either:

1. add a dedicated source type such as `WORLD_EXPERIENCE`; or
2. document an explicit, reviewed mapping into an existing type.

Until then, no automatic bridge is allowed.

---

## 4. SENS / Cognition mapping

The experimental semantic-lattice branch contains useful primitives:

```text
EventRef
EventCandidate
OccurrenceClaim
OccurrenceDerivation
OccurrenceStatus (legacy compatibility)
```

But the current R6 audit classifies that lattice as:

```text
RESEARCH_SOURCE / DO_NOT_MERGE_AS_IS
```

and it has no common Git ancestor with the current public-freeze lineage.

### Meaning of the SENS concepts

`OccurrenceClaim` describes what the speaker/semantic level claims about realization.

It explicitly does **not** mean:

- world truth;
- physical verification;
- evidence proof;
- authority;
- memory truth.

`EventRef` is currently **frame-local** semantic identity.

Therefore:

```text
SENS EventRef
!=
PhysicalSignalEventV0
!=
TransitionV0
!=
persistent world-object identity
```

**Decision:** never reuse one ID across those layers merely because all are called “events”.

Later integration should use typed references/relations between them.

Example:

```text
semantic EventRef
   --refers_to / claims / describes-->
physical event or TransitionV0
```

without identity collapse.

### M8-D2 concepts retained as source

The following ideas remain valuable and should be ported selectively when SENS is migrated onto the current lineage:

- occurrence claim + derivation;
- explicit NO_ASSERTION vs UNRESOLVED;
- event candidate identity;
- anaphora/event reference;
- speaker-level occurrence distinct from truth.

They are **source concepts**, not yet runtime dependencies of this repository.

---

## 5. Observed state — NO NEW CONTRACT

The original draft proposed `ObservedState`.

F0 removes it.

Observed physical/world state is represented through the existing chain:

```text
source
 -> ModalityObservationV0 / SituatedMeasurementV0 / RealImageObservationV0
 -> WorldObservationV0
 -> WorldStateV0 / WorldStateCandidateV0
```

The provenance/time/frame/evidence contracts determine why it is an observation.

Do not add:

```text
ObservedStateV0
```

unless a future concrete gap proves it necessary.

---

## 6. Transition binding

Existing `TransitionV0` contains:

- entity;
- from state;
- to state;
- time;
- spatial frame;
- relations;
- continuity;
- uncertainty;
- contradictions;
- provenance/evidence.

It does not currently contain a transformation/action reference.

F0 does **not** fork `TransitionV0`.

Two acceptable implementation paths exist:

### Preferred

Add an optional `transformation_ref` upstream to `TransitionV0` after dedicated regression/audit.

### Compatibility path

Create a small additive binding:

```text
TransitionTransformationBindingV0
  transition_ref
  transformation_ref
  provenance_refs[]
```

until upstream migration is accepted.

No hidden action semantics may be stuffed into `relation_refs`.

---

## 7. Visual learning contracts still owned by this project

These are not duplicated by current F16 and remain valid project additions.

### VisualInvariantV0

```text
invariant_id
target_ref
category = LOCK | FLEX | IGNORE
property
expected_value_or_relation
tolerance
source_refs[]
confidence?
provenance_refs[]
```

### VisualFingerprintV0

Compact discriminative signature for continuity/recognition without pixel equality.

Possible ingredients:

- feature refs;
- shape descriptors;
- proportions;
- segmentation topology;
- temporal tracks;
- geometry relations;
- MMonde invariant refs.

Every ingredient keeps provenance.

### GenerationIntentV0

```text
generation_intent_id
semantic_goal
world_state_refs[]
required_invariant_refs[]
allowed_variations[]
forbidden_changes[]
target_modality
quality_target?
compute_budget?
latency_budget?
```

No execution authority.

### GeneratedArtifactV0

```text
artifact_id
generation_intent_ref
generator_adapter
generator_version
weights_hash
workflow_hash?
seed?
parameters
created_at
file_hash
source_refs[]
```

Generated imagery MUST NOT be represented as `RealImageObservationV0`.

It re-enters perception through a generated modality path, e.g.:

```text
ModalityObservationV0(generated=True)
```

or a later specialized generated-media contract that preserves that flag.

### ReverseEvaluationV0

```text
reverse_evaluation_id
artifact_ref
requested_invariant_refs[]
observed_invariant_refs[]
matches[]
violations[]
unknowns[]
severity
candidate_causes[]
provenance_refs[]
```

A reverse evaluation is evidence about generator consistency, not proof about physical reality.

---

## 8. GPS / Defense mapping

The existing GPS stack remains authoritative for its domain.

Current physical path already follows:

```text
recorded / physical evidence
 -> observation envelope
 -> Physical Reality Gate
 -> GPS DomainState
 -> MMonde / evidence bridge
 -> GPS domain gate
 -> KX108 boundary
 -> receipt / claim boundary
```

Current public C4.1 reconciliation also preserves:

```text
recorded evidence != live attestation
legacy RECORDED_RF_ATTACK label != proven causal spoofing
returned ACT in evidence transport != physical execution permission
```

**Decision:** new world-prediction contracts may consume GPS/MMonde state refs, but they cannot upgrade GPS claim scope or bypass the existing reality/authenticity gate.

---

## 9. Canonical F0 learning loop

The F0-frozen conceptual loop is now:

```text
SOURCE
  |
  v
existing observation contracts
  |
  v
WorldObservationV0
  |
  v
WorldStateV0 / WorldStateCandidateV0
  |
  +---- WorldTransformationV0
  |              |
  |              v
  |        prediction engine
  |              |
  |              v
  |     WorldStateProjectionV0
  |              |
  +---- later observed world state
                 |
                 v
          WorldStateDeltaV0
                 |
                 v
      WorldExperienceCandidateV0
                 |
          validate / replay
                 |
                 v
       Native MemoryCandidate
       only through reviewed bridge
```

---

## 10. F0 contract status table

| Contract / concept | F0 status |
|---|---|
| WorldObservationV0 | EXISTING / ADOPT |
| WorldStateV0 | EXISTING / ADOPT |
| TimeEnvelopeV0 | EXISTING / ADOPT |
| SpatialFrameRefV0 | EXISTING / ADOPT |
| TypedRelationV0 | EXISTING / ADOPT |
| TransitionV0 | EXISTING / ADOPT |
| TrajectoryV0 | EXISTING / ADOPT |
| ModalityObservationV0 | EXISTING / ADOPT |
| SituatedMeasurementV0 | EXISTING / ADOPT |
| PhysicalSignalEventV0 | EXISTING / ADOPT |
| WorldStateCandidateV0 | EXISTING / ADOPT |
| ReplayablePhysicalEvidenceCandidateV0 | EXISTING / ADOPT |
| RealImageObservationV0 | EXISTING / ADOPT |
| VisualPrimitiveV0 | EXISTING / ADOPT |
| ObservedStateV0 | REJECT — DUPLICATE |
| generic VisualIR root | HOLD — NOT NEEDED YET |
| WorldTransformationV0 | NEW / BUILD |
| WorldStateProjectionV0 | NEW / BUILD |
| WorldStateDeltaV0 | NEW / BUILD |
| WorldExperienceCandidateV0 | NEW / BUILD |
| TransitionTransformationBindingV0 | NEW ONLY IF upstream field not added |
| SENS EventRef/EventCandidate | RESEARCH SOURCE / SELECTIVE PORT |
| OccurrenceClaim/Derivation | RESEARCH SOURCE / SELECTIVE PORT |
| MemoryCandidate lifecycle | EXISTING / REUSE |
| VisualInvariantV0 | NEW / BUILD LATER |
| VisualFingerprintV0 | NEW / BUILD LATER |
| GenerationIntentV0 | NEW / BUILD LATER |
| GeneratedArtifactV0 | NEW / BUILD LATER |
| ReverseEvaluationV0 | NEW / BUILD LATER |

---

## 11. Constitutional invariants

Every new contract in this repository must preserve:

```text
decision_authority = KX108_ONLY
allowed_to_decide = false
allowed_to_act = false
kernel_mutation = false
memory auto-promotion = false
observation != truth
prediction != observation
simulation != history
generated media != physical evidence
temporal relation != causal proof
semantic occurrence claim != physical occurrence proof
```

This is the F0 contract freeze candidate.
