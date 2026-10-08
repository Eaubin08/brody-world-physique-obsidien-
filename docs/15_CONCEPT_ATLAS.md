# 15 — Atlas des concepts Obsidia — Monde Physique / Brody / Cognition

**Status:** CONCEPT ATLAS V0  
**Purpose:** define the user's concepts in their Obsidia meaning, not only list their names.

This atlas is a **semantic audit layer**. It does not replace code contracts. It explains what the concepts mean, why they exist, what they must not be confused with, how they relate to one another, and which sources support them.

---

# 0. Rule for every future document audit

Every concept or architectural idea found in a user document must be audited with at least:

```text
NAME
DEFINITION IN OBSIDIA
PURPOSE
WHAT IT IS NOT
INPUTS
OUTPUTS
RELATIONS TO OTHER CONCEPTS
AUTHORITY / BOUNDARY
CURRENT STATUS
PRIMARY USER SOURCE
CURRENT CODE / TEST SOURCE IF ANY
OPEN QUESTIONS / DRIFT
```

A document audit is incomplete if it only says:

> "Concept found."

It must explain what the concept means **inside the user's architecture**.

---

# 1. Obsidia

## Definition

Obsidia is not a single AI model.

It is an architecture and method for keeping **understanding, memory, proof, decision, authority and action separated** while allowing many cognitive and technical organs to cooperate.

The project shifts part of intelligence outside model weights into:

- structured representations;
- typed memory;
- domains;
- tools;
- agents;
- mathematical/deterministic checks;
- experience;
- replay;
- proofs;
- explicit authorities.

## Purpose

Allow intelligence to grow without silently giving one model every power in the chain.

## It is not

- a chatbot;
- one LLM;
- one autonomous agent;
- a traditional operating system;
- a simple rules engine;
- a memory database;
- a world model in isolation.

## Core relation

```text
understand
!=
remember
!=
prove
!=
decide
!=
authorize
!=
act
```

## Status

**FOUNDATIONAL / CURRENT ARCHITECTURE**

## Primary user source

- `OBSIDIA_SUPPORT_MAITRE_MISE_AU_MONDE_V4_MONDE_PHYSIQUE_GPS_2026-09-21`
- current X108 repositories and architecture docs.

---

# 2. "Each layer speaks its own language"

## Definition

A fundamental Obsidia design principle: each layer should manipulate the representation appropriate to its role instead of forcing all cognition, evidence, memory and execution into one universal format or one model.

Examples:

```text
sensor -> measurement language
SENS -> semantic/event language
MMonde -> situated-world language
Brody -> contextual/compositional language
KX108 -> decision-structure language
runtime -> capability/execution language
proof -> receipt/replay language
```

## Purpose

Prevent semantic collapse between layers.

## It is not

A ban on interoperability. Layers communicate through explicit contracts and adapters.

## Status

**FOUNDATIONAL DOCTRINE**

---

# 3. Skill before encyclopedic knowledge

## Definition

The target is primarily an intelligence that can **do, predict, correct and reuse procedures**, rather than one whose main value is storing verbal definitions.

Formal knowledge remains available, but operational competence may emerge first.

Example:

```text
object released
-> object moves downward
```

can be learned operationally before the system knows or needs a formal statement of gravitational acceleration.

## Purpose

Reduce dependence on massive parametric memory and focus learning on reusable competence.

## It is not

A rejection of knowledge, science or definitions.

Knowledge is used when it improves prediction, explanation, transfer or proof.

## Relation

This principle motivates:

- WorldState;
- Transition;
- WorldTransformation;
- ExperienceCandidate;
- replay;
- small specialized models;
- late-stage parameter updates.

## Status

**FOUNDATIONAL DOCTRINE**

---

# 4. State -> transformation/action -> consequence

## Definition

The basic operational grammar for learning the world:

```text
WorldState(t)
   +
Transformation / Action
   ->
WorldState(t+1)
```

The system then compares the predicted next state to the observed next state.

## Purpose

Turn experience into a reusable causal/dynamic learning structure.

## It is not

Automatic causal proof.

A transition may be temporal or correlated without proving cause.

## Current canonical implementation

Existing upstream:

- `WorldStateV0`
- `TransitionV0`

New project contracts:

- `WorldTransformationV0`
- `WorldStateProjectionV0`
- `WorldStateDeltaV0`
- `WorldExperienceCandidateV0`

## Status

**FOUNDATIONAL / PARTLY IMPLEMENTED**

---

# 5. WorldObservationV0

## Definition

A bounded observation about a world entity/state with time, source, provenance, uncertainty and evidence references.

## Purpose

Represent what a source reports without promoting it to truth.

## It is not

- reality itself;
- memory truth;
- a decision;
- a causal conclusion.

## Canonical rule

```text
observation != truth
```

## Status

**EXISTING / CURRENT**

---

# 6. WorldStateV0

## Definition

A candidate representation of the world at a given validity time, built from bounded observations, contradictions, unknowns and provenance.

## Purpose

Give heterogeneous observations a common situated world context.

## It is not

- an absolute world truth;
- Brody's belief;
- Native Memory;
- KX108 decision state.

## Canonical rule

```text
world state = candidate reality representation
```

## Status

**EXISTING / CURRENT**

---

# 7. MMonde

## Definition

MMonde is the common grammar used to situate heterogeneous observations in a world.

Its important reference concepts include:

- space;
- time;
- object;
- identity;
- relation;
- transformation;
- scale;
- constraint;
- provenance;
- uncertainty;
- consequence;
- competing hypotheses;
- stoppability.

## Purpose

Allow camera, GNSS, RF, inertial data, generated media and other modalities to be compared without pretending they measure the same thing.

## It is not

- a total generative copy of reality;
- one neural world model;
- a decision authority;
- a sensor fusion engine that erases contradictions.

## Key principle

Different modalities can carry different kinds of truth.

A camera can indicate form; radar can indicate distance; GNSS can indicate position; inertial sensing can indicate motion continuity.

MMonde preserves those differences.

## Status

**EXISTING / CURRENT WORLD REPRESENTATION**

---

# 8. WorldTransformationV0

## Definition

A descriptive representation of a transformation affecting the world.

Examples:

- an object moved;
- a camera rotated;
- an agent pushed an object;
- a simulator applied a force;
- Brody proposes a virtual transformation.

## Purpose

Bind state changes to a described transformation without confusing description with execution authority.

## It is not

`WorldAction`.

It cannot authorize or execute anything.

## Epistemic classes

- OBSERVED
- PROPOSED
- SIMULATED
- INFERRED
- UNKNOWN

## Status

**IMPLEMENTED IN THIS PROJECT**

---

# 9. WorldAction

## Definition

In current Obsidia vocabulary, WorldAction belongs to the governed execution/readiness side.

It concerns the possibility of a real or controlled world action after authority and capability checks.

## Purpose

Keep physical/software execution behind explicit governance.

## It is not

A neutral description of something that happened.

That is why this project uses `WorldTransformationV0` for learning.

## Status

**EXISTING / EXECUTION-SIDE CONCEPT**

---

# 10. WorldStateProjectionV0

## Definition

A wrapper around a world state that explicitly marks it as:

- predicted;
- simulated;
- counterfactual.

## Purpose

Allow internal forecasting and dreaming without letting imagined states masquerade as observed reality.

## It is not

An observation.

## Core rule

```text
prediction != observation
simulation != history
counterfactual != evidence of occurrence
```

## Status

**IMPLEMENTED IN THIS PROJECT**

---

# 11. WorldStateDeltaV0

## Definition

The structured difference between an expected/baseline state and a later observed/candidate state.

It can contain:

- expected changes;
- unexpected changes;
- missing expected changes;
- metric differences;
- invariant matches;
- invariant violations;
- explanation candidates.

## Purpose

Turn prediction error into learning material.

## It is not

A proof of why the difference occurred.

## Core rule

```text
delta != causal proof
```

## Status

**IMPLEMENTED IN THIS PROJECT**

---

# 12. WorldExperienceCandidateV0

## Definition

A compact learning episode linking:

```text
state before
transformation
prediction
state after
delta
outcome
replay refs
candidate skills/invariants
```

## Purpose

Convert lived or simulated episodes into structured learning candidates.

## It is not

Canonical memory.

## Core rule

```text
experience candidate
!=
memory truth
```

## Status

**IMPLEMENTED / MEMORY BRIDGE NOT YET BUILT**

---

# 13. TransitionV0

## Definition

Existing upstream world-dynamics contract representing a state transition with temporal, spatial, relational, continuity, uncertainty and evidence context.

## Purpose

Describe how a situated entity moves from one state to another.

## It is not

An execution command.

## Current project decision

Do not mutate it during F0.

Use:

`TransitionTransformationBindingV0`

to link transition to a WorldTransformation.

## Status

**EXISTING / ADOPTED**

---

# 14. TransitionTransformationBindingV0

## Definition

Small additive contract binding an existing `TransitionV0` reference to a `WorldTransformationV0` reference.

## Purpose

Make the transformation behind a transition explicit without changing the verified upstream contract.

## It is not

A new transition ontology.

## Status

**IMPLEMENTED / V0 COMPATIBILITY DECISION**

---

# 15. OS Trad / inward translation

## Definition

The inward semantic translation layer that takes an external expression or source and maps it into an internal representation usable by Obsidia.

Conceptually:

```text
external expression
-> translation
-> internal representation
```

## Purpose

Preserve structure, relationships, ambiguity and constraints before downstream cognition.

## It is not

- Brody;
- KX108;
- the execution layer;
- the outward Reverse OS.

## Historical source

The older `Obsidia OS : L'Architecture de la Souveraineté Sémantique` document describes an Alphabet IR with historical primitives such as VALUE, STATE, READ, WRITE, FLOW, COND, LOOP, CALL, RETURN, EVENT, TIME, ERROR.

Those exact primitives are **historical source material** unless confirmed by current runtime.

## Status

**CURRENT PRINCIPLE / HISTORICAL DETAILS TO AUDIT**

---

# 16. IR — Internal Representation

## Definition

The structured internal language used to transport meaning between external input and downstream Obsidia layers.

## Purpose

Reduce dependence on raw natural language and preserve structure explicitly.

## It is not

One frozen universal syntax forever.

The exact current IR must be derived from present code/contracts, not assumed from historical documents.

## Status

**CURRENT PRINCIPLE / IMPLEMENTATION EVOLVES**

---

# 17. Reverse OS / SSR

## Definition

The outward projection layer.

Its job is to transform a stabilized internal state into a useful external form:

- text;
- UI;
- audio;
- visual representation;
- interaction affordance.

## Purpose

Give Obsidia an intelligible output without giving the projection layer authority over the underlying decision.

## Core rule

```text
Reverse OS projects.
It does not decide.
```

## It is not

- KX108;
- a contradiction arbiter;
- memory;
- kernel mutation;
- an authorization mechanism.

## Status

**CURRENT ARCHITECTURAL PRINCIPLE**

---

# 18. Brody

## Definition

Brody is Obsidia's cognitive/compositional organ.

It gathers useful context, connects structures, compares options, builds hypotheses, prepares propositions, selects bounded tools and explains outcomes.

## Purpose

Make the architecture cognitively useful and transmissible without becoming sovereign.

## It is not

- the kernel;
- KX108;
- OS Trad;
- Native Memory;
- one specific LLM;
- an execution authority.

## "Pseudo-LLM"

The user's idea is that Brody's capability should not be defined solely by a giant pretrained model.

Its intelligence comes from the organization around it:

- structured corpus;
- memory;
- domains;
- trees;
- tools;
- specialized organs;
- routing;
- experience;
- correction loops.

A generative model can contribute to Brody without being Brody.

## Status

**CURRENT ORGAN / CONTINUING DEVELOPMENT**

---

# 19. SENS / Cognition

## Definition

The semantic/cognitive layer concerned with extracting and preserving meaningful structures such as predicates, events, relations, occurrence claims and references.

## Purpose

Prevent language from silently turning:

- mention into fact;
- future into past;
- belief into truth;
- report into direct observation;
- reference into identity.

## It is not

Physical truth or evidence.

## Current status

The strongest current semantic lattice material is still classified as research source / selective-port material on the current R6 line.

---

# 20. EventRef

## Definition

In the semantic lattice, an EventRef is a **frame-local semantic event identity** derived from a predicate.

## Purpose

Allow language to refer back to an event and build event relations/anaphora.

## It is not

- a persistent physical event ID;
- a memory ID;
- a world-object identity;
- a TransitionV0 ID.

## Status

**RESEARCH SOURCE / SELECTIVE PORT**

---

# 21. EventCandidate

## Definition

A semantic extraction record around an EventRef, carrying provenance and occurrence classification.

## Purpose

Represent a possible semantic event conservatively.

## It is not

Proof that the event physically happened.

## Status

**RESEARCH SOURCE / SELECTIVE PORT**

---

# 22. OccurrenceClaim

## Definition

The semantic claim about whether an event is presented as realized, not realized, possible, projected, unresolved, or not asserted.

## Purpose

Prevent language from collapsing different commitments into one "event happened" flag.

## Important distinction

```text
OccurrenceClaim
!= truth
!= physical evidence
!= verification
!= memory truth
```

## Status

**M8-D2 SOURCE CONCEPT / SELECTIVE PORT**

---

# 23. OccurrenceDerivation

## Definition

The structured explanation of how an OccurrenceClaim was derived from linguistic structure.

## Purpose

Make semantic classification replayable and auditable instead of opaque.

## It is not

A causal derivation of a physical-world event.

## Status

**M8-D2 SOURCE CONCEPT / SELECTIVE PORT**

---

# 24. Native Memory

## Definition

The active memory direction in current Obsidia.

Memory supplies context and preserves validated or candidate information with provenance/status.

## Purpose

Maintain continuity without turning memory into hidden authority.

## It is not

- the kernel;
- a decision engine;
- a truth oracle;
- an automatic learning sink.

## Current rule

```text
memory_write = false
auto_promotion = false
manual/reviewed promotion only
```

## Status

**ACTIVE CURRENT MEMORY PATH**

---

# 25. MemoryCandidate

## Definition

A candidate proposed for possible memory promotion.

It carries source, hash, summary, status and risk flags.

## Purpose

Create a controlled boundary between new experience/information and durable memory.

## It is not

Automatically accepted memory.

## Status

**EXISTING / CURRENT**

---

# 26. Zone Latente

## Definition

Historical concept for a temporary non-executable holding area for ideas, hypotheses, partial concepts and structured summaries that have not yet earned durable memory status.

## Purpose

Allow long reasoning and emerging concepts without polluting canonical memory.

## It is not

Canonical memory or execution authority.

## Current architectural analogue

Parts of this intent now overlap with:

- candidates;
- context packets;
- memory candidates;
- experiment/replay buffers;
- unknown/hypothesis states.

Exact runtime equivalence must be audited before reviving a separate "Zone Latente" component.

## Status

**HISTORICAL CONCEPT / PARTLY ABSORBED**

---

# 27. Continuum

## Definition

Historical mechanism where actions produce structured summaries such as:

```text
Input + State + Result
```

so long-running cognition can preserve continuity.

## Purpose

Maintain chronological/structural continuity without retaining all raw context.

## It is not

A decision engine.

## Current relation

Conceptually close to:

- receipts;
- replay;
- experience candidate;
- memory candidate;
- chronological world history.

## Status

**HISTORICAL CONCEPT / TO MAP**

---

# 28. Friction Symbolique

## Definition

Learning through explicit discrepancy, contradiction, correction, paradox or failed expectation.

The system does not merely accumulate examples; it pays special attention to **where its representation or prediction breaks**.

## Purpose

Turn error into structured learning material.

## Current modern expression

```text
prediction
-> observation
-> delta
-> explanation candidate
-> experience
```

## It is not

Random adversarial noise or unbounded self-modification.

## Status

**FOUNDATIONAL LEARNING IDEA / NOW MAPPED TO DELTA LOOP**

---

# 29. Shazam Cognitif

## Definition

Recognition through discriminative signatures rather than simple semantic labels.

Historical examples include:

- unusual writing style;
- rhythm;
- intonation;
- breath;
- recurrent patterns.

The principle can extend to visual signatures.

## Purpose

Recognize continuity or hidden pattern quickly from compact distinctive features.

## It is not

A claim that emotion/style detection is automatically true.

It produces a candidate signature with uncertainty.

## Current project descendant

`VisualFingerprintV0` is a likely visual descendant of this idea.

## Status

**HISTORICAL PRIMARY CONCEPT / ACTIVE DESIGN SOURCE**

---

# 30. 34 Arbres

## Definition

Historical cognitive organization where multiple conceptual "trees" represent different dimensions/perspectives and only a small dominant subset is activated for a given context.

## Purpose

Reduce cognitive overload by dynamically focusing on relevant dimensions.

## It is not

Current verified runtime unless a branch/code audit says so.

## Status

**HISTORICAL COGNITIVE SOURCE**

---

# 31. VisualFingerprint

## Definition

A compact discriminative signature for recognizing the continuity of a visual object/entity without requiring exact pixel equality.

Potential components:

- visual features;
- shape;
- proportions;
- segmentation topology;
- geometry;
- temporal track;
- invariant relations.

## Purpose

Answer:

> Is this still the same object/entity under a different view, lighting, style or frame?

## It is not

A biometric truth claim by default.

## Status

**PLANNED**

---

# 32. Invariant rho (ρ)

## Definition

Historical visual-learning notion for properties that should survive a transformation when the underlying identity remains the same.

Examples:

- essential geometry;
- proportions;
- identity-defining structure;
- stable relationships.

## Purpose

Allow the system to distinguish legitimate variation from structural drift.

## It is not

Every pixel.

## Current descendant

`VisualInvariantV0`.

## Status

**HISTORICAL IDEA / ACTIVE DESIGN SOURCE**

---

# 33. VisualInvariant — LOCK / FLEX / IGNORE

## Definition

A planned explicit rigor contract for generation/reconstruction.

### LOCK

Properties that must be preserved.

### FLEX

Properties that may change within limits.

### IGNORE

Properties irrelevant to the evaluation.

## Purpose

Make image generation testable instead of using a vague "looks similar" judgment.

## Example

```text
LOCK:
  identity
  proportions

FLEX:
  lighting
  clothes
  background

IGNORE:
  compression noise
```

## Status

**PLANNED**

---

# 34. FaceLock / ID-Lock

## Definition

Historical example of applying very high rigor to identity-critical facial structure while allowing more freedom elsewhere.

## Purpose

Demonstrate that generation constraints can have different strengths by property.

## It is not

A claim of current pixel-perfect identity preservation.

## Current descendant

VisualInvariant LOCK semantics.

## Status

**HISTORICAL CONCEPT / DESIGN SOURCE**

---

# 35. Contrôleur de Rigueur

## Definition

Historical idea of adjustable constraint strength depending on what must remain invariant.

## Purpose

Avoid treating every generated property with equal strictness.

## Current expression

LOCK / FLEX / IGNORE plus tolerances.

## Status

**HISTORICAL IDEA / MODERNIZED**

---

# 36. Analyse <-> Synthèse / Méthode Réciproque

## Definition

Learning/validation loop in which the system:

1. decomposes an object/image/world state;
2. extracts structure/invariants;
3. reconstructs or generates a new case;
4. re-perceives the result;
5. checks whether the important structure survived.

## Purpose

Test whether the system actually captured the structure rather than only producing a description.

## It is not

Generation for aesthetics alone.

## Current implementation direction

```text
perception
-> world representation
-> generation
-> re-perception
-> ReverseEvaluation
```

## Status

**FOUNDATIONAL VISUAL LEARNING METHOD / NOT FULLY IMPLEMENTED**

---

# 37. Invariant Dynamique

## Definition

A stable spatio-temporal identity/coherence kernel that persists while legitimate properties change over time.

Video is treated as a sequence of transformations around persistent identity, not as unrelated frames.

## Purpose

Maintain:

- object identity;
- trajectory;
- relation continuity;
- scene coherence;
- temporal structure.

## It is not

A static visual embedding.

## Current relation

- TransitionV0;
- TrajectoryV0;
- tracking;
- WorldStateDelta;
- future video invariants.

## Status

**PRIMARY HISTORICAL IDEA / PARTLY COVERED BY WORLD DYNAMICS**

---

# 38. Multimodalité Harmonique

## Definition

Historical idea that different modalities should connect through a shared internal structure rather than be relearned as isolated worlds.

## Purpose

Allow image, language, sound, sensor data and other modalities to contribute to one situated model without erasing modality-specific meaning.

## It is not

Simple concatenation of sensor outputs.

## Current operational descendant

```text
ModalityObservationV0
-> WorldObservationV0
-> MMonde
```

while preserving each modality's clock, provenance, frame and uncertainty.

## Status

**HISTORICAL IDEA / CURRENTLY MATERIALIZED IN A MORE BOUNDED FORM**

---

# 39. Reverse360

## Definition

Working project concept for testing whether a world/object representation survives viewpoint transformations.

It is not simply "make a 360° image".

## Process

```text
view A
-> represent
-> generate/obtain view B
-> re-perceive
-> compare invariants
```

Repeated across several views.

## Purpose

Test if the system learned an object/world rather than one particular image.

## It is not

A panoramic rendering feature.

## Status

**PROJECT CONCEPT / DEFINITION STILL SUBJECT TO HISTORICAL SOURCE RECOVERY**

---

# 40. RealImageObservationV0

## Definition

Existing specialized contract for a physically captured image with immutable asset identity, capture context, visual primitives, integrity, provenance and uncertainty.

## Purpose

Keep physical image evidence distinct from generated media.

## It is not

Generated imagery.

The contract explicitly rejects generated media.

## Status

**EXISTING / VERIFIED UPSTREAM**

---

# 41. GeneratedArtifactV0

## Definition

Planned receipt-bearing representation of media produced by a generator.

It should preserve:

- generator;
- model version;
- weights hash;
- workflow;
- seed;
- parameters;
- source refs;
- output hash.

## Purpose

Make generation reproducible and auditable.

## It is not

Physical evidence.

## Status

**PLANNED**

---

# 42. ReverseEvaluationV0

## Definition

Planned evaluation of a generated artifact after it has been re-perceived.

## Purpose

Compare requested invariants against observed output and produce machine-readable violations/unknowns.

## It is not

Physical-world truth.

It is evidence about generator consistency.

## Status

**PLANNED**

---

# 43. Physical Signal Periphery

## Definition

Non-sovereign layer representing physical signals, measurements, contradictions, risk hints and candidate world states.

## Purpose

Bring real sensor data into Obsidia while preserving physical provenance and uncertainty.

## It is not

A detector that automatically proves an attack or physical cause.

## Status

**EXISTING / CURRENT**

---

# 44. Physical Reality Gate

## Definition

Domain-side boundary that determines whether a physical observation has enough provenance/validity to be admitted at a given claim level.

## Purpose

Prevent recorded, synthetic, malformed or insufficiently attested data from silently becoming "real live physical truth".

## It is not

KX108.

It qualifies evidence before governance.

## Status

**EXISTING IN GPS DOMAIN**

---

# 45. Evidence Compatibility

## Definition

Existing physical-evidence assessment across several dimensions:

- temporal;
- spatial;
- metric;
- causal;
- source independence.

## Purpose

Ask whether several physical channels can coherently support the same candidate.

## It is not

Automatic proof of causality.

## Status

**EXISTING / CURRENT**

---

# 46. Provenance

## Definition

The trace of where an observation, claim, artifact, rule or state came from.

It can include:

- source ID;
- source hash;
- instrument;
- configuration;
- model/version;
- time;
- transformation history.

## Purpose

Make every important statement traceable and replayable.

## It is not

Trust.

A source can be perfectly traceable and still wrong.

## Canonical distinction

```text
provenance != truth
```

## Status

**FOUNDATIONAL / CURRENT**

---

# 47. UNKNOWN

## Definition

A legitimate state meaning the system lacks enough grounded information to classify something more strongly.

## Purpose

Prevent forced certainty.

## It is not

An error to hide.

## Status

**FOUNDATIONAL**

---

# 48. HOLD

## Definition

A governance decision that keeps a problem open because required information, proof, authority or consistency is missing.

## Purpose

Stop uncertainty from being converted into unauthorized action.

## It is not

A crash or indecision.

## Status

**CURRENT KERNEL AUTHORITY OUTPUT**

---

# 49. BLOCK

## Definition

A governance decision that prohibits the proposed action because a blocking condition is established.

## It is not

Merely low confidence.

## Status

**CURRENT KERNEL AUTHORITY OUTPUT**

---

# 50. ACT

## Definition

A governance decision that the candidate action is admissible at the kernel decision level.

## Important boundary

```text
ACT != physical execution
```

Execution can still require Binder/capability/runtime/human conditions.

## Status

**CURRENT KERNEL AUTHORITY OUTPUT**

---

# 51. GuardX108

## Definition

The kernel-side structural judge evaluating contradictions, unknowns, confidence, risk and admissibility before a decision.

## Purpose

Keep decision structure outside generative cognition.

## It is not

A world-understanding model.

Domains translate world meaning before it reaches this layer.

## Status

**CURRENT KERNEL CONCEPT**

---

# 52. KX108_ONLY

## Definition

Constitutional statement that final decision authority belongs to the X108/KX108 governance boundary, not to Brody, memory, perception, tools or generators.

## Purpose

Prevent authority creep as individual organs become more capable.

## Status

**CURRENT CONSTITUTIONAL INVARIANT**

---

# 53. Sigma

## Definition

Post-/meta-Guard supervision layer used to surface alert/freeze conditions and maintain contradiction/risk visibility.

## Purpose

Keep unresolved or dangerous tensions explicit.

## It is not

A replacement for KX108 authority.

## Status

**CURRENT ARCHITECTURAL CONCEPT / EXACT RUNTIME SHOULD BE READ FROM CURRENT SOURCE**

---

# 54. Binder / Runtime Binder

## Definition

The mechanism that materializes the specific capabilities granted after governance.

Examples:

- accessible files;
- permitted commands;
- read/write rights;
- budget;
- duration;
- stop conditions.

## Purpose

Translate a decision into a bounded executable mandate.

## It is not

The decision itself.

## Status

**CURRENT EXECUTION ARCHITECTURE**

---

# 55. Receipt

## Definition

A structured proof/audit record linking what entered the system, which transformations/decisions occurred, what capability was used and what result was observed.

## Purpose

Support audit, replay and responsibility.

## It is not

Only a post-hoc log.

In Obsidia, proof should begin before action and continue after action.

## Status

**CURRENT FOUNDATIONAL MECHANISM**

---

# 56. Replay

## Definition

The ability to reconstruct or rerun a previously recorded path from receipts, source material and deterministic steps.

## Purpose

Verify reproducibility, compare strategies and support learning without always re-entering the real world.

## Important distinction

```text
recorded replay
!= simulation
!= counterfactual
```

## Status

**CURRENT / EXTENDING INTO LEARNING**

---

# 57. Dreaming / internal simulation

## Definition

Future learning mechanism in which the system uses recorded experience and learned transitions to explore candidate futures without claiming they happened.

## Purpose

Test alternatives cheaply before real execution.

## It is not

History or evidence.

## External reference ideas

- DreamerV3;
- Dream-RSI.

## Status

**PLANNED**

---

# 58. Weight-last learning

## Definition

The system should first improve behavior through:

1. routing;
2. tool choice;
3. deterministic transforms;
4. memory retrieval;
5. reusable skills;
6. replay;
7. adapters;

before considering larger parametric updates.

## Purpose

Avoid treating every error as a retraining problem.

## It is not

A ban on fine-tuning or LoRA.

## Status

**FOUNDATIONAL LEARNING POLICY**

---

# 59. World quadrillage

## Definition

The user's idea of making the world tractable by giving the system stable coordinates/concepts for placing experience rather than forcing it to memorize every possible world state.

The quadrillage is based on recurring questions:

```text
where?
when?
what?
relative to what?
what changed?
what stayed invariant?
which source?
with what uncertainty?
what action/transformation?
what consequence?
```

## Purpose

Create a reusable scaffold where new experience can be situated and compared.

## It is not

A literal rectangular spatial grid only.

It is a conceptual/situational coordinate system.

## Relation

MMonde is the current architectural home for much of this idea.

## Status

**FOUNDATIONAL USER IDEA / PARTLY MATERIALIZED**

---

# 60. Physical world model in Obsidia

## Definition

Not one giant generative network that contains a compressed copy of reality.

It is the combination of:

- situated observations;
- world-state representation;
- time and reference frames;
- transitions;
- transformations;
- predictions;
- deltas;
- experience;
- memory;
- replay;
- specialized predictive models.

## Purpose

Learn how the world changes and what actions tend to produce.

## It is not

One model checkpoint.

## Status

**CURRENT PROJECT TARGET**

---

# 61. "The model is an organ"

## Definition

A replaceable AI model is a capability provider inside a larger organism.

Its competence does not imply:

- truth;
- authority;
- identity of the whole system.

## Purpose

Allow Qwen, MiniCPM, SANA, Z-Image, JEPA, TD-MPC or future models to be swapped without rewriting the constitution of Obsidia.

## Status

**FOUNDATIONAL PRINCIPLE**

---

# 62. Oxygen

## Definition

Future concept for a continuously educated entity whose identity/trajectory should persist while individual organs/models may change.

Historical/current support documents distinguish:

```text
agents know how to do
Oxygen learns to know / become
```

## Purpose

Address continuity, education, genealogy and long-lived identity.

## It is not

Brody.

Brody is a cognitive organ.

## Current reality

Oxygen is not currently built.

## Status

**FUTURE / CONCEPTUAL**

---

# 63. "One birth"

## Definition

Continuity principle attached to Oxygen: an entity should not be considered the same enduring entity merely because each session loads similar weights/configuration.

Identity requires continuity of history and development.

## Purpose

Separate durable identity from model replacement.

## It is not

A claim that present Obsidia is conscious.

## Status

**FUTURE IDENTITY PRINCIPLE**

---

# 64. Education vs training

## Definition

Training changes or calibrates capabilities.

Education, in the user's architecture, is broader: it concerns context, history, errors, humans, meaning, genealogy and identity across time.

## Purpose

Keep long-lived cognitive development distinct from model optimization.

## Status

**FOUNDATIONAL FUTURE-COGNITION DISTINCTION**

---

# 65. Status against eloquence

## Definition

A linguistic output may sound convincing without gaining any mechanical status.

Examples:

```text
hypothesis
candidate
reported claim
observed fact
validated evidence
proof
decision
```

must remain mechanically distinct regardless of how eloquently they are described.

## Purpose

Prevent language generation from laundering uncertainty into truth.

## Status

**FOUNDATIONAL COGNITIVE SAFETY PRINCIPLE**

---

# 66. Proof before and after action

## Definition

Obsidia treats post-action logs as insufficient.

The chain should preserve evidence before action (representation, proposal, decision, authority) and after action (actual consequence).

## Purpose

Link intention to consequence rather than only proving that a command happened.

## Status

**FOUNDATIONAL PROOF PRINCIPLE**

---

# 67. Current concept graph

```text
                 EXTERNAL WORLD
                       |
                  observations
                       |
        +--------------+---------------+
        |                              |
      SENS                         measurements
  semantics/events               image/GPS/RF/etc
        |                              |
        +--------------+---------------+
                       |
                     MMonde
                       |
                  WorldStateV0
                       |
              WorldTransformationV0
                       |
           +-----------+------------+
           |                        |
        observed                 predict
           |                        |
           |             WorldStateProjectionV0
           |                        |
           +-----------compare------+
                       |
                WorldStateDeltaV0
                       |
             WorldExperienceCandidateV0
                       |
                  replay/review
                       |
                 MemoryCandidate
                       |
                   Native Memory

Brody reads/composes/proposes across these layers.
KX108 remains the authority boundary.
Reverse OS projects stabilized outputs outward.
```

---

# 68. Audit drift policy

When an old user document and current runtime differ, the audit must explicitly record:

```text
ORIGINAL CONCEPT
CURRENT DESCENDANT
WHAT SURVIVED
WHAT CHANGED
WHAT WAS ABANDONED
WHAT IS STILL ONLY AN IDEA
```

Example:

```text
Zone Latente
-> current candidate/buffer/memory-boundary mechanisms

Invariant rho
-> VisualInvariantV0 direction

Multimodalité Harmonique
-> ModalityObservationV0 + MMonde bounded fusion

Analyse <-> Synthèse
-> perception -> generation -> re-perception -> ReverseEvaluation

Continuum
-> receipts / chronological experience / replay direction
```

This prevents historical documents from being either blindly revived or incorrectly discarded.

---

# 69. Source policy

Each concept definition should link back to one or more of:

- current code/test;
- current architecture document;
- master support document;
- original user research document;
- historical visual/AGI corpus.

The source index lives in:

- `docs/11_SOURCES.md`
- `docs/12_OBSIDIA_USER_SOURCES.md`

This atlas explains meaning; those files provide traceability.
