# 13 — F0 Cross-Audit — SENS / Cognition / MMonde / Native Memory / GPS

**Date:** 2026-10-08  
**Mode:** READ-ONLY audit of source repositories; documentation changes only in Brody World Physique Obsidia.  
**Verdict:** F0_CONTRACT_CROSS_AUDIT_COMPLETE / FREEZE_CANDIDATE

## 1. Repositories and branches inspected

### Obsidia X108

Primary current audit line:

```text
Eaubin08/obsidia-x108-proofs
feat/r6-sens-cognition-canonical-audit-v0
```

This branch is the useful cross-domain source because it already contains the accumulated MMonde/world/vision/physical/GPS contracts plus R6 SENS work.

Observed ancestry:

- `feat/premiere-mise-au-monde-mmonde-v0` is an ancestor of R6; R6 is 128 commits ahead / 0 behind.
- `feat/premiere-mise-au-monde-situated-world-dynamics-v0` is an ancestor of R6; R6 is 92 commits ahead / 0 behind.
- `feat/premiere-mise-au-monde-gps-physical-world-closure-v0` is an ancestor of R6; R6 is 54 commits ahead / 0 behind.

Therefore those world branches are treated as **absorbed into the current R6 line**, not separate competing canonical sources.

### Semantic lattice research branch

```text
exp/semantic-grammar-cognitive-lattice-v0
```

Git reports no common ancestor with current `main`.

The R6 audit itself classifies it:

```text
RESEARCH_SOURCE / DO_NOT_MERGE_AS_IS
USEFUL_NON_SOVEREIGN_EXPERIMENT_NOT_CANONICAL_RUNTIME
```

It is used only as a forensic/source corpus.

### Native Memory repair line

```text
repair/brody-native-memory-cleanup-20261008
```

Relative to `main`:

- 8 commits ahead;
- 0 behind.

Its runtime validation document reports:

```text
Native Memory active
Graphiti/Neo4j legacy
memory_write = false
decision_authority = KX108_ONLY
54 targeted tests passed / 0 failed
```

It diverges from the R6 feature line, so this F0 audit uses its memory contracts/boundaries but does not imply code merge.

### GPS public repository

```text
Eaubin08/obsidia-gps-defense-
feat/c41-gps-kernel-response-and-claim-boundary-v0
```

Relative to its `main`:

- 1 commit ahead;
- 0 behind.

It adds public X108 response normalization and explicit quarantine of an over-strong historical RF attack label.

The isolated `native-builder-trusted-navigation-v1` branch has no common ancestor with current GPS main and is not used as the canonical F0 base.

---

## 2. Existing world contracts found

### MMonde

Source:

`periphery/mmonde/contracts_v0.py`

Found:

- `WorldObservationV0`
- `WorldStateV0`

Important existing semantics:

```text
OBSERVATION != TRUTH
WORLD_STATE != MEMORY
WORLD_STATE != COGNITION
candidate_reality = true
readonly representation
KX108_ONLY
```

**F0 consequence:** our draft `WorldState` was redundant.

### Situated World Dynamics

Source:

`periphery/world_dynamics/contracts_v0.py`

Found:

- `TimeEnvelopeV0`
- `SpatialFrameRefV0`
- `TypedRelationV0`
- `TransitionV0`
- `TrajectoryV0`
- `RelationStatusV0`
- `ContinuityStatusV0`

The upstream F12 document reports:

```text
VERIFIED / NO F12 REGRESSION
12490 passed / 11 historical baseline failures / 46 skipped / 207 deselected
F12-visible failures = 0
```

No tests were rerun by this F0 audit; this is upstream recorded evidence.

**F0 consequence:** transition/time/space are already present and should be adopted.

### Measurement

Source:

`periphery/measurement/contracts_v0.py`

Found:

- `InstrumentRefV0`
- `MeasurementContextV0`
- `SituatedMeasurementV0`

Upstream F13 reports no F13 regression.

### Physical signal / evidence

Sources:

- `periphery/physical_signal/contracts_v0.py`
- `periphery/physical_evidence/contracts_v0.py`

Found:

- signal events;
- contradictions;
- reports;
- risk hints;
- `WorldStateCandidateV0`;
- replayable evidence candidates;
- temporal/spatial/metric/causal/independence compatibility.

Critical rule already implemented:

```text
co-occurrence != causality
measurement != physical truth
candidate world state != canonical reality
```

**F0 consequence:** do not recreate a generic evidence engine.

---

## 3. Multimodal and vision findings

### Multimodal

Source:

`periphery/multimodal/bridge_v0.py`

Found:

`ModalityObservationV0`

It already preserves:

- modality;
- clock;
- source and source hash;
- uncertainty;
- contradiction;
- latency;
- reference frame;
- generated/not-generated;
- causal status.

Its bridge creates `WorldObservationV0` and `WorldStateV0` without promoting fusion to truth.

### Real image

Source:

`periphery/vision/contracts_v0.py`

Found:

- `ImageAssetRefV0`
- `CaptureContextV0`
- `VisualPrimitiveV0`
- `CandidateInterpretationV0`
- `ImageIntegrityReportV0`
- `RealImageObservationV0`

The F16 doc reports:

```text
VERIFIED / NO F16 REGRESSION
12513 passed / 11 historical baseline failures / 46 skipped / 207 deselected
F16-visible failures = 0
```

Important:

`RealImageObservationV0` rejects generated imagery.

**F0 consequence:** our generic VisualIR draft duplicated most of F16. We retain “VisualIR” only as a possible derived/serialized view, not a new root ontology.

---

## 4. Cross-modal / GPS findings

### Cross-modal

F20 already assesses modality pairs on:

- temporal alignment;
- spatial/frame compatibility;
- metric compatibility;
- causal compatibility;
- source independence.

F20 explicitly keeps causality UNKNOWN and flags generated modalities as not physical truth.

Recorded upstream status:

```text
VERIFIED / NO F20 REGRESSION
12538 passed / 11 historical baseline failures / 46 skipped / 207 deselected
F20-visible failures = 0
```

### GPS physical closure

F21 already binds:

- recorded evidence;
- MMonde world-state ref;
- UDIP domain-state ref;
- optional cross-modal report;
- receiver status;
- blockers;
- bounded claim scope.

Existing explicit rule:

```text
recorded provenance != live sensor attestation
```

Recorded upstream status:

```text
VERIFIED / NO F21 REGRESSION
12545 passed / 11 historical baseline failures / 46 skipped / 207 deselected
F21-visible failures = 0
```

### GPS public C4.1

The dedicated public GPS branch adds a conservative claim guard.

It preserves the raw historical `RECORDED_RF_ATTACK` label as source data but quarantines it as:

```text
SOURCE_LEVEL_CONFLICT_REVIEW_REQUIRED
RECORDED_RF_ATTACK_LABEL_WITHOUT_CAUSAL_ATTRIBUTION
```

and explicitly sets:

- spoofing causal attribution proven = false;
- aviation validated = false;
- allowed_to_act = false;
- emits_verdict = false.

**F0 consequence:** the new learning/world-model layer must never silently upgrade physical claims.

---

## 5. SENS / Cognition findings

The experimental lattice contains:

- `PredicateUnit`;
- `LatticeRelation`;
- `EventRef`;
- `EventCandidate`;
- `OccurrenceClaim`;
- `OccurrenceDerivation`;
- event reference/anaphora logic.

### OccurrenceClaim

The source is explicit:

> occurrence claim is what the semantic/speaker level claims about realization; it is not world truth, verification, evidence, authority or memory truth.

This is highly compatible with the new project but must remain semantically scoped.

### EventRef

`EventRef` is explicitly:

```text
frame-local occurrence identity
```

It is not:

- memory identity;
- physical event identity;
- persistent world identity.

### M8-D2

The source branch shows the intended migration:

```text
OccurrenceClaim + OccurrenceDerivation
        -> EventCandidate
EventRef identity preserved
legacy occurrence_status retained for compatibility
```

This is valuable source material.

But current R6 explicitly forbids direct branch merge.

**F0 decision:**

- reuse concepts selectively;
- never use semantic EventRef as physical identity;
- later bridge semantic events to world transitions through typed refs/relations;
- preserve NO_ASSERTION vs UNRESOLVED;
- never treat linguistic causality as physical proof.

---

## 6. Native Memory findings

Current module already provides:

- `MemoryCandidate`;
- append-only candidate ledger;
- candidate statuses;
- manual promotion policy.

Existing rules:

```text
memory_write_allowed = false
auto_promotion_allowed = false
PROMOTED_MANUAL_ONLY requires human review
memory = context, not truth
```

**F0 consequence:** `WorldExperienceCandidateV0` must not create its own promotion mechanism.

Gap found:

`MemorySourceType` currently has no explicit world/physical experience source type.

This is a real later integration decision.

---

## 7. What our original draft got wrong

### Duplicate 1 — WorldState

Draft:

`WorldState`

Reality:

`WorldStateV0` already exists.

Verdict: **REMOVE DUPLICATE.**

### Duplicate 2 — ObservedState

Draft proposed a separate observed-state type.

Reality:

observations already become `WorldObservationV0 -> WorldStateV0`, with specialized measurement/image/signal contracts preserving evidence class.

Verdict: **DO NOT CREATE.**

### Duplicate 3 — VisualIR as root ontology

Most required fields already exist in:

- `RealImageObservationV0`;
- `VisualPrimitiveV0`;
- `ModalityObservationV0`;
- `WorldObservationV0`.

Verdict: **HOLD AS DERIVED VIEW ONLY.**

### Duplicate 4 — Generic Transition

`TransitionV0` already exists.

Verdict: **ADOPT.**

---

## 8. Genuine gaps found

### GAP-A — descriptive transformation/action

Existing world dynamics has a transition but no explicit non-sovereign object describing the transformation/action that links states.

Because `WorldAction` already means governed execution, the new contract should be called:

`WorldTransformationV0`

### GAP-B — projected/simulated world state

No audited common wrapper currently distinguishes:

```text
PREDICTED
SIMULATED
COUNTERFACTUAL
```

while reusing the existing WorldState schema.

Proposed:

`WorldStateProjectionV0`

### GAP-C — prediction/observation delta

No common contract found for explicit state-difference learning.

Proposed:

`WorldStateDeltaV0`

### GAP-D — experience episode

Native Memory has memory candidates, but no common physical/world episode linking:

```text
state_before
transformation
projection
state_after
delta
outcome
```

Proposed:

`WorldExperienceCandidateV0`

This stays outside canonical memory until adapted through the Native Memory candidate policy.

### GAP-E — transition <-> transformation link

Existing `TransitionV0` lacks an action/transformation ref.

Preferred later upstream patch:

`TransitionV0.transformation_ref?`

Fallback compatibility object:

`TransitionTransformationBindingV0`

---

## 9. F0 classification

### EXISTING / ADOPT

- WorldObservationV0
- WorldStateV0
- TimeEnvelopeV0
- SpatialFrameRefV0
- TypedRelationV0
- TransitionV0
- TrajectoryV0
- ModalityObservationV0
- SituatedMeasurementV0
- PhysicalSignalEventV0
- PhysicalSignalReportV0
- WorldStateCandidateV0
- ReplayablePhysicalEvidenceCandidateV0
- RealImageObservationV0
- VisualPrimitiveV0
- Native Memory MemoryCandidate lifecycle

### RESEARCH SOURCE / SELECTIVE PORT

- EventRef
- EventCandidate
- OccurrenceClaim
- OccurrenceDerivation
- experimental semantic lattice relations/projections

### NEW / BUILD

- WorldTransformationV0
- WorldStateProjectionV0
- WorldStateDeltaV0
- WorldExperienceCandidateV0
- optional TransitionTransformationBindingV0

### NEW LATER — VISUAL LEARNING / GENERATION

- VisualInvariantV0
- VisualFingerprintV0
- GenerationIntentV0
- GeneratedArtifactV0
- ReverseEvaluationV0

### REJECT AS DUPLICATE

- new root WorldState
- ObservedStateV0
- new generic Transition
- parallel physical-evidence ontology

---

## 10. F0 verdict

```text
MMONDE_CORE                  EXISTING
WORLD_DYNAMICS               EXISTING
TIME / SPATIAL FRAME         EXISTING
MEASUREMENT                  EXISTING
PHYSICAL_SIGNAL              EXISTING
PHYSICAL_EVIDENCE            EXISTING
MULTIMODAL_BRIDGE            EXISTING
REAL_IMAGE_CONTRACT          EXISTING
GPS_PHYSICAL_CLOSURE         EXISTING
NATIVE_MEMORY_CANDIDATE      EXISTING

SENS_EVENT/OCCURRENCE        RESEARCH_SOURCE_ONLY_ON_CURRENT_LINE
WORLD_TRANSFORMATION         MISSING
WORLD_STATE_PROJECTION       MISSING
WORLD_STATE_DELTA            MISSING
WORLD_EXPERIENCE_CANDIDATE   MISSING
TRANSITION_TRANSFORM_BINDING MISSING

F0_CONTRACT_AUDIT            COMPLETE
F0_CONTRACT_FREEZE           CANDIDATE
RUNTIME_IMPLEMENTATION       NOT_STARTED_IN_THIS_REPO
MODEL_DOWNLOADS              NONE
```

## 11. Next gate

The next step is no longer “invent the world schema”.

It is:

1. implement the four missing contracts locally in this new repository;
2. add schema/unit tests and negative sovereignty tests;
3. decide whether `TransitionV0` receives an upstream optional `transformation_ref` or uses an additive binding;
4. only then perform PC hardware inventory and F1 perception installation.

No external model is required for that next contract implementation gate.


## 12. Mandatory concept-definition rule for future audits

F0 showed that finding a name in a document is not enough.

Every future document/source audit must also explain each relevant user concept with:

```text
definition in Obsidia
purpose
what it is not
inputs / outputs when applicable
relations to neighboring concepts
authority boundary
current implementation status
historical source
current code/test source
drift from older definitions
```

The canonical explanatory companion is:

`docs/15_CONCEPT_ATLAS.md`

If an audit discovers a new user-origin concept, the audit must either:

1. add it to the atlas; or
2. mark it `UNDEFINED / SOURCE RECOVERY REQUIRED`.

No concept may be silently redefined from generic AI terminology when the user has a specific Obsidia meaning.
