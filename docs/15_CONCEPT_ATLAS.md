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


---

# 70. AVDR

## Definition

AVDR is a user-origin cognitive/process concept whose acronym and operational interpretation **changed across the history of Obsidia**.

That drift must be preserved rather than flattened.

### Historical research usage

Older AVDR research documents describe AVDR as an auto-evolving / auto-verifiable developmental reasoning protocol concerned with:

- self-generated tasks;
- multi-agent solving;
- cognitive evaluation;
- reasoning traces;
- calibration;
- structured feedback;
- controlled cognitive evolution.

Historical expansions include formulations around **Auto-Verifiable Developmental Reasoner** and older phase interpretations such as adaptation/validation/disruption/regulation.

### Current repository canon for the Gencoin sandbox

The current file:

`docs/gencoin/sandbox_pre_freeze/AVDR_CANON.md`

defines:

```text
A = Accueil
V = Vibration
D = Déploiement
R = Résolution
```

with:

- **Accueil** = perception / écoute / réception;
- **Vibration** = friction / reaction / sorting / tension;
- **Déploiement** = expression / engagement / action phase;
- **Résolution** = integration / learning / return toward stability.

It describes AVDR as a protocol for reading and transforming a living cognitive state.

### Obsidure implementation usage

The current `AgentObsidure` code uses another operational mapping:

```text
A = Audit
V = Validation
D = Disruption
R = Réintégration
```

for its bounded software-building cycle.

## Purpose

AVDR is best treated as a **family of transformation-cycle patterns**, not as one acronym whose historical wording must be forced onto every subsystem.

## It is not

- KX108;
- one universal decision algorithm;
- a proof that every historical AVDR variant is active today.

## Audit rule

Whenever AVDR appears, the audit must record:

```text
which AVDR variant?
which date/source?
which subsystem?
runtime or doctrine?
```

## Status

**MULTI-GENERATION USER CONCEPT / CURRENT LOCAL VARIANTS EXIST**

---

# 71. ADeLe / A2DR

## Definition

A historical/user concept paired with AVDR in current sandbox documentation.

The current AVDR canon says:

```text
ADeLe gives the measure.
AVDR gives the dynamic.
Obsidia gives the organs and structural meaning.
```

## Purpose

Separate **measurement/evaluation** from **dynamic transformation**.

## It is not

A current global kernel authority unless independently verified in runtime.

## Status

**HISTORICAL / SANDBOX-LEVEL CONCEPT — NEEDS DEDICATED SOURCE AUDIT**

---

# 72. Balance exponentielle / Balance Proportionnelle Exponentielle

## Definition

A user-origin weighting concept intended to make evaluation **non-linear** rather than treating every signal as having equal importance.

Historical visual/cognitive documents also describe it as a possible common "pivot" between modalities.

## Purpose

Represent that:

- a small critical contradiction may matter more than many weak positive signals;
- transformations/relations can be weighted non-linearly;
- cognitive or system balance may depend on proportions rather than simple averages.

## Current repository reality

Current formalisation status explicitly says:

```text
Balance exponentielle -> domaines formels
Pondération non-linéaire
Documentée, non reliée
```

A Gencoin sandbox balance operator exists, but that does **not** prove that the historical universal Balance is currently bound across Obsidia.

## It is not

- current universal physics;
- automatically the kernel vote formula;
- proof of cross-modal equivalence.

## Status

**DOCUMENTED / PARTIAL SANDBOX IMPLEMENTATIONS / NOT GLOBALLY BOUND**

---

# 73. Veto Harmonique

## Definition

Historical governance concept in which a sufficiently severe low score/contradiction can block a consensus rather than being averaged away.

Older source material ties the name to a harmonic-mean style vote plus absolute veto thresholds.

## Purpose

Prevent a majority of moderate positive signals from erasing one critical blocking condition.

## Current repository reality

The F22 source traceability audit states:

- harmonic immutable-vote calculation: **MISSING**;
- vote structure: present but **CODE_DORMANT** in that historical form;
- historical harmonic thresholds: **doc-only**.

Current X108/Guard/Sigma governance therefore must not be described as if the old harmonic-veto formula is the active canonical decision mechanism.

## It is not

The same thing as current KX108 decision authority.

## Status

**HISTORICAL GOVERNANCE IDEA / OLD FORMULA NOT CURRENT RUNTIME CANON**

---

# 74. Obsidure

## Definition

Obsidure is Obsidia's bounded **builder / researcher / formalizer organ**.

Current code describes it as:

```text
CO_PILOTE_CODE
+
CI_REPO_SURGEON
```

and gives it responsibilities such as:

- audit a requested objective;
- build or repair peripheral code;
- prepare Lean sandbox material;
- organize bounded memory/session artefacts;
- test and stabilize proposals;
- emit patch proposals.

## Current bounded cycle

Current AgentObsidure uses:

```text
Audit
-> Validation
-> Disruption
-> Réintégration
```

## Hard boundary

Current code explicitly sets:

```text
decision_authority = KX108_ONLY
allowed_to_decide = false
emits_act = false
kernel_mutation = false
x108_merge = false
sandbox_mode = HUMAN_APPROVED_WRITE
```

## Purpose

Let an AI organ build, formalize and repair without acquiring sovereignty.

## It is not

- Brody;
- KX108;
- automatic main-branch writer;
- kernel modifier.

## Status

**CURRENT IMPLEMENTED ORGAN**

---

# 75. OS3ProofTicket

## Definition

A structured proof/receipt object linking an action candidate, X108 result and evidence surface through hashes.

Current fields include:

- ticket ID;
- action ID;
- domain;
- X108 gate;
- reason/severity;
- scores;
- unknowns;
- risk flags;
- contradictions;
- evidence refs;
- input hash;
- output hash;
- trace hash;
- Merkle root;
- replay status.

## Purpose

Create a replay/audit anchor for the decision path.

## Current implementation detail

Current builder computes SHA-256 hashes for:

```text
input
output
trace
Merkle-style aggregate root
```

and currently initializes:

`replay_status = NOT_RUN`

until replay is actually performed.

## It is not

A proof that replay ran merely because a ticket exists.

It is not itself decision authority.

## Status

**CURRENT RUNTIME/RECEIPT BRICK — REPLAY STATUS MUST REMAIN HONEST**

---

# 76. OS3

## Definition

A proof/replay layer/family in Obsidia associated with:

- proof tickets;
- hashes;
- receipts;
- replay status;
- audit linkage.

## Purpose

Bind the path through the system to evidence that can later be inspected/replayed.

## It is not

The cognitive layer or kernel decision itself.

## Status

**CURRENT PROOF/REPLAY FAMILY — EXACT SUBCOMPONENT STATUS VARIES**

---

# 77. Runtime Binder

## Definition

The Runtime Binder is the layer that turns an already-governed mandate into **bounded capabilities and runtime context**.

Conceptually it answers:

```text
what may this organ access?
what may it call?
what may it write?
for how long?
under which limits?
```

## Purpose

Separate:

```text
capability detected
!= authority granted
!= consequence verified
```

## It is not

The authority that decides ACT/HOLD/BLOCK.

## Current reality

Binder-related current/recent branches include capability routing, Brody/Obsidure repair, context packets and runtime-boundary work.

## Status

**CURRENT EXECUTION-BOUNDARY ARCHITECTURE**

---

# 78. Provider Cognitive Binder

## Definition

A more specific binder family for external/internal cognitive providers.

It keeps provider identity, runtime result and receipts bound without merging providers into a new sovereign intelligence.

## Purpose

Allow multiple cognitive providers/tools to be used while preserving:

- provider identity;
- comparison boundaries;
- receipts;
- non-sovereignty.

## It is not

A consensus authority.

## Status

**CURRENT / TESTED IN CG9 SURFACES**

---

# 79. ERA — Espace de Raisonnement Assisté

## Definition

Historical cognitive/interface metric or visualization concept used to summarize the relative contribution/tension of memory, reasoning, autonomy/friction or other cognitive factors.

Older Reverse OS material refers to ERA as something that may be **displayed** to the user.

## Purpose

Make internal cognitive balance understandable/visible.

## It is not

A kernel score unless a current runtime contract explicitly says so.

## Current status

No current canonical world-runtime binding was established during this audit.

## Status

**HISTORICAL / UI-COGNITIVE CONCEPT — CURRENT BINDING UNCONFIRMED**

---

# 80. World Foundry

## Definition

User concept for an educational/simulation environment where an intelligence can learn through controlled worlds, exercises, consequences and progressively richer experience.

It is the "school + workshop" idea applied to world learning.

## Purpose

Provide an environment where:

```text
state
-> action
-> consequence
-> correction
-> transfer
```

can be learned without requiring every experiment to happen in the real world.

## It is not

A claim that the full world can be simulated perfectly.

## Relation

Closely related to:

- replay;
- dreaming;
- sandbox;
- Transition learning;
- MMonde;
- Oxygen education;
- Brody/agent skill acquisition.

## Status

**USER VISION / FUTURE EDUCATIONAL-SIMULATION LAYER**

---

# 81. Formule du Savoir Obsidia (FSO)

## Definition

Historical user framework for turning a domain's existing knowledge into a structured learning path rather than making an AI rediscover everything from zero.

The archived document describes a sequence broadly resembling:

```text
ingest knowledge
-> normalize vocabulary
-> extract entities / relations / constraints
-> derive invariants
-> represent
-> analyse <-> synthesize
-> evaluate
-> transfer
```

## Purpose

Use existing human knowledge as a starting curriculum, then move toward independent application and skill.

## It is not

The current canonical memory schema or one universal proven mathematical formula.

## Current relation

Its strongest surviving ideas are now distributed across:

- corpus;
- OS/IR;
- MMonde;
- invariants;
- learning loops;
- tests;
- memory candidates;
- experience.

## Status

**HISTORICAL LEARNING FRAMEWORK / PARTLY ABSORBED**

---

# 82. "Build the body before searching for a total brain"

## Definition

Core user design strategy: build the organism around intelligence before attempting to create one monolithic model that does everything.

The "body" includes:

- memory;
- domains;
- representation;
- tools;
- proofs;
- world-state structures;
- authority;
- execution boundaries;
- replay;
- learning paths.

## Purpose

Allow intelligence to improve by replacing or adding organs rather than rebuilding the entire system around a larger model.

## It is not

A rejection of neural models.

## Status

**FOUNDATIONAL USER METHOD**

---

# 83. "Structure can replace part of inference"

## Definition

When a route is already known, bounded and validated, Obsidia should reuse the structure rather than asking a large model to rediscover the route probabilistically.

## Purpose

Reduce:

- latency;
- token use;
- cost;
- variability;
- unnecessary model dependence.

## It is not

A claim that structure replaces all cognition.

## Related mechanisms

- routers;
- Fast Path;
- Path Compute;
- deterministic domains;
- proof surfaces;
- cached/validated routes.

## Status

**CURRENT ARCHITECTURAL PRINCIPLE / PARTLY BENCHMARKED**

---

# 84. Fast Path

## Definition

A route for situations whose structure is sufficiently known and bounded that the system can avoid a broad cognitive/model path.

## Purpose

Use the smallest sufficient path.

## It is not

Automatic permission to act.

Fast Path still remains inside governance boundaries.

## Status

**CURRENT ARCHITECTURAL/RUNTIME FAMILY**

---

# 85. Path Compute

## Definition

User/Obsidia idea that compute should follow the **minimal adequate path**, rather than always invoking the most general/expensive intelligence.

## Purpose

Turn compute allocation into a routing decision.

Conceptually:

```text
known admissible route
> unnecessary general inference
```

## It is not

Simply "faster hardware".

The gain is often from avoiding computation rather than accelerating identical computation.

## Status

**CURRENT ARCHITECTURAL PRINCIPLE**

---

# 86. MEMZUM

## Definition

Current Brody memory-activation layer answering a narrow question:

> Does this request currently require memory?

Current docs explicitly distinguish MEMZUM from retrieval itself.

## Purpose

Avoid querying memory unnecessarily.

## It is not

The memory store.

It does not decide what is true.

## Current relation

```text
cognitive signals
-> MEMZUM yes/no
-> Native Memory retrieval if needed
```

## Status

**CURRENT / BRANCH-SPECIFIC RUNTIME COMPONENT**

---

# 87. Point cloud / cognitive point cloud

## Definition

A structured multi-axis representation used in parts of Brody's cognitive path to summarize the state/tensions relevant to routing/context.

## Purpose

Compress several cognitive signals into a machine-readable structure that downstream components can use.

## It is not

A literal 3D point cloud and not automatically a world-state representation.

## Status

**CURRENT COGNITIVE MECHANISM / EXACT AXES VERSION-SPECIFIC**

---

# 88. True Voice

## Definition

The final expression layer used to turn structured Brody/cognitive state into a readable human-facing response.

## Purpose

Keep phrasing/output separate from the underlying authority and evidence status.

## It is not

The source of truth or decision.

## Status

**CURRENT OUTPUT COMPONENT / BRANCH-SPECIFIC**

---

# 89. SRL — Session Registry Layer

## Definition

A session-organization concept used by Obsidure to classify candidate session material into bounded tiers such as:

- ACTIVE;
- SEMI_ACTIVE;
- COLD;
- GHOST_SIDE_TABLE.

Current Obsidure creates candidate session cards but does not directly write canonical memory.

## Purpose

Organize working/session material without confusing it with durable memory.

## It is not

Native Memory canonical storage.

## Status

**CURRENT OBSIDURE SUPPORT CONCEPT**

---

# 90. "Present != connected != causally useful != tested != proven != frozen != production"

## Definition

A maturity/claim ladder repeatedly used in recent Obsidia master documents.

It prevents a concept or file from being overclaimed merely because it exists.

## Purpose

Force every audit to distinguish:

```text
idea
artifact
component
connected runtime
causal contribution
test
proof
freeze
production
```

## It is not

A rhetorical disclaimer. It is a project-status discipline.

## Status

**CURRENT AUDIT DOCTRINE**

---

# 91. Concept lineage

## Definition

For a user-origin idea, the atlas must preserve its evolution through time.

Example:

```text
historical intuition
-> named concept
-> architecture document
-> prototype
-> current descendant
-> runtime/test status
```

## Purpose

Prevent two opposite errors:

1. reviving obsolete ideas as current canon;
2. losing the user's original idea merely because its implementation was renamed.

## Status

**MANDATORY AUDIT METHOD**

---

# 92. Canon vs source pack vs research source

## Definition

Three different epistemic statuses for project material.

### Canon/current source

Material currently accepted as architecture/runtime truth.

### Source pack

Preserved material used to recover ideas, history or unmerged specifications.

### Research source

Experimental branch/doc useful for selective migration but not directly mergeable/canonical.

## Purpose

Keep a huge historical project intelligible without flattening everything into "current".

## Status

**CURRENT AUDIT CLASSIFICATION**

---

# 93. C10

## Definition

A future concept associated in project materials with long-term cognition/education/Oxygen.

During this audit, no sufficiently precise current runtime definition was recovered to safely assign a stronger meaning.

## Purpose

Unknown until dedicated source recovery.

## Status

**UNDEFINED / SOURCE RECOVERY REQUIRED**

This status is intentional: the atlas must prefer an explicit unknown over reconstructing a definition from neighboring concepts.
