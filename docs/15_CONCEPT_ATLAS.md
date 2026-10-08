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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Source historique OS Trad](https://docs.google.com/document/d/1ZTisSqVwl4SUyp3T_BjZr2OxCkKaMmoUtY9W8X8oyYE/edit).
- **Lecture / frontière :** Source indexée, lecture de définition exacte à finaliser ; OS Trad n'est pas le kernel.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Source historique OS Trad](https://docs.google.com/document/d/1ZTisSqVwl4SUyp3T_BjZr2OxCkKaMmoUtY9W8X8oyYE/edit).
- **Lecture / frontière :** Source indexée ; portée actuelle du format IR à auditer sur branche runtime.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Source historique Reverse OS](https://docs.google.com/document/d/1L_LG0UE4vyLn-iXF0pvjc94owZCI3McF2SWJo3TG8nY/edit).
- **Lecture / frontière :** Source indexée ; ne confondre ni représentation de sortie ni autorisation d'action.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Audit historique Brody](https://docs.google.com/document/d/1PmNNst_WVYflLQmCn8z6RrwGpYTHZBMe5F4DULiN7yc/edit).
- **Lecture / frontière :** Source d'audit historique, ne vaut pas preuve de branchement Brody actuel.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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


## Preuve de source F0 — 2026-10-08

- [SENS source research](https://github.com/Eaubin08/obsidia-x108-proofs/blob/85d55e3538f1b049f2f9eb7f12892928187d3de4/app/semantic/lattice/events.py) — source inspectée à un commit identifié.
- **Limite :** La branche source est expérimentale et distincte de R6; une lecture de code ne transforme pas M8-D2 en runtime canonique.
- **Audit de frontière :** [F0 passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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


## Preuve de source F0 — 2026-10-08

- [EventRef original](https://github.com/Eaubin08/obsidia-x108-proofs/blob/85d55e3538f1b049f2f9eb7f12892928187d3de4/app/semantic/lattice/events.py) — source inspectée à un commit identifié.
- **Limite :** Identifiant strictement local au frame/énoncé; ni identité physique, ni mémoire, ni preuve.
- **Audit de frontière :** [F0 passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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


## Preuve de source F0 — 2026-10-08

- [EventCandidate experimental](https://github.com/Eaubin08/obsidia-x108-proofs/blob/85d55e3538f1b049f2f9eb7f12892928187d3de4/tests/test_occurrence_migration.py) — source inspectée à un commit identifié.
- **Limite :** Le test source documente le candidat d'événement et la projection M8-D2; tests non relancés.
- **Audit de frontière :** [F0 passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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


## Preuve de source F0 — 2026-10-08

- [OccurrenceClaim original](https://github.com/Eaubin08/obsidia-x108-proofs/blob/85d55e3538f1b049f2f9eb7f12892928187d3de4/app/semantic/lattice/occurrence_derivation.py) — source inspectée à un commit identifié.
- **Limite :** Ce que la phrase affirme, pas la réalisation prouvée d'un événement dans le monde.
- **Audit de frontière :** [F0 passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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


## Preuve de source F0 — 2026-10-08

- [OccurrenceDerivation original](https://github.com/Eaubin08/obsidia-x108-proofs/blob/85d55e3538f1b049f2f9eb7f12892928187d3de4/app/semantic/lattice/occurrence_derivation.py) — source inspectée à un commit identifié.
- **Limite :** La dérivation du claim conserve NO_ASSERTION ≠ UNRESOLVED et la frontière linguistique.
- **Audit de frontière :** [F0 passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit) ; [Friction Symbolique](https://docs.google.com/document/d/1Zu6jX4P-RFB8owuCNTs6yWTkC8Yvo5Ef34lYTtcjBFo/edit).
- **Lecture / frontière :** Le sas latent historique n'est ni mémoire validée ni droit d'écriture. La source Friction montre un exemple, pas une intégration actuelle.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** Input + État + Résultat attesté comme principe historique ; le grand export Continuum est une archive dialoguée, pas un contrat runtime.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Friction Symbolique](https://docs.google.com/document/d/1Zu6jX4P-RFB8owuCNTs6yWTkC8Yvo5Ef34lYTtcjBFo/edit) ; [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** La source Friction donne la divergence |logique-diffusif| et un seuil illustratif 0,3 ; ne pas en faire un seuil X108 ni une écriture mémoire canonique.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Shazam Cognitif — 34 Arbres](https://docs.google.com/document/d/1KshgP97PKdTZAfRxe9-YfcVnIJceKbgGCyxC-HdRj18/edit) ; [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** Le document Shazam propose extraction de signatures + projection 34 arbres en pseudocode ; aucune preuve de reconnaissance émotionnelle fiable ou de middleware déployé.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Shazam Cognitif — 34 Arbres](https://docs.google.com/document/d/1KshgP97PKdTZAfRxe9-YfcVnIJceKbgGCyxC-HdRj18/edit).
- **Lecture / frontière :** 34 arbres = proposition d'espace d'activation historique ; ne pas déduire que la matrice tourne en production.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Shazam Cognitif — 34 Arbres](https://docs.google.com/document/d/1KshgP97PKdTZAfRxe9-YfcVnIJceKbgGCyxC-HdRj18/edit).
- **Lecture / frontière :** Filiation d'intention seulement : Shazam texte/tonalité ≠ algorithme VisualFingerprint. Implémentation visuelle non attestée.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** ρ désigne des propriétés identitaires à préserver selon cette archive ; ce n'est pas une constante physique établie.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** Critères de rigueur historiques (identité versus transformation permise), sans validation de pipeline image.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** FaceLock/ID-Lock présent dans l'archive ; l'exigence « pixel par pixel » est une intention historique, pas une fidélité garantie.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** Contrôle différentiel de rigueur décrit ; aucune connexion exécutable présumée.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** Décomposer → reconstruire → revérifier : méthode de validation proposée, non démonstration actuelle de conservation d'identité.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** Le noyau spatio-temporel vidéo est une idée de continuité ; la branche de dynamique du monde n'en fournit qu'une couverture partielle.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit).
- **Lecture / frontière :** La « note pivot » intermodale est un objectif historique ; absence de preuve d'une équivalence mathématique universelle.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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


## Preuve de source F0 — 2026-10-08

- [GPS public claim matrix](https://github.com/Eaubin08/obsidia-gps-defense-/blob/d1221fce6914274f7b0c445a829739367b0c6abb/docs/CLAIM_MATRIX.md) — source inspectée à un commit identifié.
- **Limite :** Le Physical Reality Gate classe une observation physique; l'adaptateur `gps_x108_gate.py` transporte une décision KX108 et ne doit pas être confondu avec le gate de recevabilité.
- **Audit de frontière :** [F0 passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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


## Preuve de source F0 — 2026-10-08

- [X108 safety doctrine](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/SECURITE.md) — source inspectée à un commit identifié.
- **Limite :** HOLD = suspension décisionnelle souveraine, non vote advisory Sigma. Domaine GPS: réponse mal formée → HOLD.
- **Audit de frontière :** [F0 passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

---
# 49. BLOCK

## Definition

A governance decision that prohibits the proposed action because a blocking condition is established.

## It is not

Merely low confidence.

## Status

**CURRENT KERNEL AUTHORITY OUTPUT**


## Preuve de source F0 — 2026-10-08

- [X108 safety doctrine](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/SECURITE.md) — source inspectée à un commit identifié.
- **Limite :** BLOCK = refus d'action par autorité du kernel, non valeur émotionnelle ou score de modèle.
- **Audit de frontière :** [F0 passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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


## Preuve de source F0 — 2026-10-08

- [X108 safety doctrine](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/SECURITE.md) — source inspectée à un commit identifié.
- **Limite :** ACT représente une décision d'autorité bornée, pas une action automatique émise par les agents, SENS ou Brody.
- **Audit de frontière :** [F0 passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Module 5 — Apprentissage et cinématique](https://docs.google.com/document/d/1iVwqEeo2TTa3Mv6wYFdJOq_8-mAfFpz7-AJ46iMxm7o/edit).
- **Lecture / frontière :** Le Module 5 expose une direction de simulation sans interférence, pas un moteur dreaming connecté.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

AVDR is a user-origin cognitive/process concept with a **documented lineage of meanings**. Its acronym and phase names changed over time and across subsystems.

The audit must preserve that lineage instead of retroactively forcing one expansion onto every document.

### Historical research protocol — 2025

The strongest dedicated research documents define AVDR as:

**Auto-Verifiable Developmental Reasoner**

and describe a modular cognitive protocol for:

- generating internal tasks/tensions;
- solving through multiple reasoning styles or agents;
- evaluating outputs;
- filtering/calibrating context;
- tracing reasoning;
- adapting/calibrating the next cycle.

A common six-step research form is:

```text
Task Forge
-> Solve Engine
-> Cognitive Evaluator
-> Context Filter
-> Reasoning Trace
-> Cognitive Calibrator
-> loop
```

The research intent was not a decision kernel. It was a **traceable self-regulating cognitive workshop**.

### Other historical expansions

Other Obsidia documents reuse the letters A-V-D-R with different pedagogical/formal meanings, including formulations around:

- Adaptation / Validation / Dérive or Disruption / Régulation;
- Apprentissage / Validation / Déduction / Résonance.

These are historical variants and must be cited with their source/date rather than merged silently.

### Current Gencoin sandbox canon

Current repository file:

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
- **Vibration** = internal reaction / friction / tri / tension;
- **Déploiement** = expression / engagement / action phase;
- **Résolution** = integration / learning / return toward stability.

The file defines AVDR as a **protocol for reading and transforming a living cognitive state**.

### Obsidure operational variant

Current Obsidure materials use a software-building cycle:

```text
Audit
-> Validation
-> Disruption
-> Réintégration
```

This is an **Obsidure-local AVDR interpretation**, not proof that every Obsidia subsystem uses those four words.

## Purpose

Across generations, the stable idea is:

> cognition progresses through explicit phases of reception/tension, examination, transformation and reintegration, with traceability and correction.

## It is not

- KX108;
- one immutable acronym expansion across all years;
- a universal decision algorithm;
- permission to act;
- proof that every historical AVDR module is runtime-connected.

## Audit rule

Every occurrence must record:

```text
AVDR variant
source/date
subsystem
phase meanings
runtime / sandbox / doctrine / research
current descendant if any
```

## Status

**MULTI-GENERATION USER CONCEPT / CURRENT LOCAL VARIANTS + HISTORICAL RESEARCH PROTOCOL**

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [AVDR Auto-Verifiable Developmental Reasoner](https://docs.google.com/document/d/1uDk3FC6a7aBGmGEul4mHzn9fMitc44xRSgPz2kxDzh4/edit) ; [Protocoles Fondateurs (variante AVDR)](https://docs.google.com/document/d/1R-BkkUUknUUs-C0rUA6LwBAISGIGwx3P8ycOojbjzOk/edit) ; [Friction Symbolique](https://docs.google.com/document/d/1Zu6jX4P-RFB8owuCNTs6yWTkC8Yvo5Ef34lYTtcjBFo/edit).
- **Lecture / frontière :** Variantes effectivement retrouvées : (i) Auto-Verifiable Developmental Reasoner ; (ii) Apprentissage par Vision-Dérive-Réflexion ; (iii) Observation–Validation–Disruption–Réintégration. Maintenir séparément canon Gencoin Accueil–Vibration–Déploiement–Résolution et AVDR opérationnel Obsidure Audit–Validation–Disruption–Réintégration. Aucune expansion universelle.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

---
# 71. ADeLe / A2DR — donateurs externes et rapprochement avec AVDR

## Définition exacte — ADeLe externe

**ADeLe n'est pas un concept créé par Obsidia.** C'est un cadre d'évaluation d'IA issu d'une collaboration de chercheurs (notamment Microsoft Research et institutions universitaires), fondé sur des niveaux d'exigence des tâches et profils de capacités de modèles.

Selon les sources primaires et générations, ADeLe est développé comme *Annotated-Demand-Levels* et présenté également comme *AI Evaluation with Demand Levels*. Il utilise 18 dimensions de capacité/demande avec des niveaux de difficulté pour expliquer/prédire la performance.

## Définition de la proposition Obsidia

La source dialoguée sur **ADeLe × AVDR × Obsidia** propose de juxtaposer :

- ADeLe : mesures des exigences de tâches et profils de capacités (**méthode externe**) ;
- AVDR : phases de régulation/évaluation/progression selon la version (**protocole historique Obsidia**) ;
- Obsidia : organes, mémoire, contrats, preuves, gouvernance (**architecture projet**).

Il s'agit d'une **proposition de composition**, pas de preuve que la fusion est actuellement implémentée, équivalente mathématiquement ou validée expérimentalement.

## A2DR — point non réconcilié

Le sigle A2DR apparaît dans des archives conversationnelles à proximité de ADeLe et d'une référence à un papier externe, mais son expansion, son équipe d'origine et son rapport exact avec ADeLe ne sont pas documentés ici par une source primaire vérifiée.

**Statut A2DR : SOURCE_RECOVERY_REQUIRED.** Aucune identification ou fusion automatique.

## Ce que ce n'est pas

- l'invention d'ADeLe par Obsidia ;
- le mécanisme de décision KX108 ;
- une mesure déjà branchée en runtime ;
- une démonstration que l'association est nouvelle, supérieure ou fonctionnelle.

## Origines

- [Microsoft Research — présentation initiale (2025)](https://www.microsoft.com/en-us/research/blog/predicting-and-explaining-ai-model-performance-a-new-approach-to-evaluation/)
- [Microsoft Research — bilan et article scientifique (2026)](https://www.microsoft.com/en-us/research/blog/adele-predicting-and-explaining-ai-performance-across-tasks/)
- [Projet de recherche ADeLe](https://kinds-of-intelligence-cfi.github.io/ADELE/)
- [Archive Obsidia — Fusion AVDR × ADeLe](https://docs.google.com/document/d/15pZLOlYVu2POMMbU6nztWlAOIaGlnhjIa5-X9q4dtE4/edit)
- [Archive où A2DR est cité, sans source primaire isolée](https://docs.google.com/document/d/1eHi6LmYA-1XG94u_jau1f8vqv7Zgy76dzI1vxz-cGss/edit)

## Frontière et statut

**EXTERNAL DONOR (ADeLe) + USER-PROJECT COMPOSITION IDEA (ADeLe×AVDR×Obsidia) / HISTORICAL PROPOSAL ONLY / A2DR UNRESOLVED / KX108_ONLY**.

Voir [audit F0, passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Éveil de l'OS Cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit) ; [Calcul de la Balance Mathématique](https://docs.google.com/document/d/1SKfhUnnGYKiOM9w8FDPavtEtwqDWb7HH/edit).
- **Lecture / frontière :** La Balance Proportionnelle Exponentielle (pondération/résonance) **n'est pas** le Calcul de la Balance Mathématique (retrait d'un facteur/réintégration inverse). Rapport formel : NON ÉTABLI.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

---
# 73. Veto Harmonique

## Definition

A user-origin governance idea built around one intuition:

> a critical weak/blocking signal must not disappear inside a comfortable average.

Historical documents expressed this with harmonic aggregation and hard veto thresholds.

## Historical form

Older material proposed:

- harmonic-mean style aggregation;
- absolute veto under a low critical score;
- refusal to let a majority of moderate positive signals erase one severe contradiction.

## Current repository descendant

The old F22 audit correctly reported that the historical implementation was then missing/dormant.

That state later changed.

Current `sigma/contracts.py` now contains:

`calculate_immutable_vote()`

with tests in:

`tests/sigma/test_f25b_immutable_vote_minimal.py`

The current function:

- counts/weights ALLOW, HOLD and BLOCK advisory votes;
- computes a bounded score in [-1, 1];
- emits an **advisory** ALLOW/HOLD/BLOCK label;
- preserves the real X108 gate;
- explicitly sets `decision_authority = KX108_ONLY`;
- sets `emits_act = false`;
- sets `emits_verdict = false`;
- cannot override a KX108 BLOCK.

Current confidence readiness also uses a true harmonic mean between integrity and governance confidence.

## Critical nuance

The current function is **not identical to every historical “Veto Harmonique” formula**.

The durable idea survived, but its implementation was re-bounded as a readonly advisory metric under X108 authority.

## Purpose

Preserve sensitivity to asymmetric/critical weakness while keeping the score non-sovereign.

## It is not

- KX108;
- a majority vote;
- permission to ACT;
- proof that historical thresholds remain canonical today.

## Status

**HISTORICAL IDEA WITH CURRENT READONLY DESCENDANT / KX108 AUTHORITY PRESERVED**

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Constitution X-108 historique](https://docs.google.com/document/d/115BlgqjdgU8B1UQiryBvoBxYaXoZu_60uo19CHxEqxs/edit).
- **Lecture / frontière :** Source constitutionnelle indexée ; tests et formule actuels du descendant readonly restent à vérifier sur branche actuelle avant tout freeze.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

# 79. ERA — Espace de Raisonnement Assisté (collision de définitions)

## ERA-A : atelier cognitif temporaire (carte B9)

La source **Carte B9 ERA** définit un espace mental de travail borné créé à la demande pour réunir contexte, mémoires et agents spécialisés autour d'une tâche complexe. C'est un **dispositif de collaboration / interface / contexte**, pas un score arithmétique. La carte parle d'« arbitrages » au sens d'usage humain/agentique historique ; elle ne confère aucune décision souveraine dans le runtime actuel.

## ERA-B : indicateur de balance de raisonnement (Reverse OS)

La source **Reverse OS — L'Éloquence Sémantique** utilise le même sigle pour un ratio de projection de l'état cognitif :

```text
ERA = (M + R + A) / F
```

M = mémoire ; R = raisonnement ; A = contribution dite « Auto » selon la variante ; F = friction. Un ratio écrit dans une archive ne fournit ni étalonnage, ni preuve de performance, ni preuve de mise en production. La définition des variables et les domaines de validité exigent l'analyse de la version source.

## Collision et évolution

Les deux usages partagent le nom, **mais ne désignent pas un objet identique**. Le dossier doit conserver deux variantes identifiées par document/version :

```text
ERA_A_WORKSPACE_B9 (atelier temporaire)
ERA_B_REVERSE_METRIC (projection / ratio)
```

Aucune équivalence prouvée. Si un composant porte le seul label ERA, déterminer d'abord son contexte.

## Runtime exact observé

Dans `apps/obsidia_api/brody_cognitive_modules_adapter.py` à la révision de code vérifiée en F0, le module ERA est :

```text
resolution = DESIGN_SPEC_NOT_IMPLEMENTED
active = false
needs_operator_spec = true
```

Le snapshot générique n'arbitre pas entre ERA-A et ERA-B ; ce n'est pas un moteur ERA fonctionnel.

## Ce que ce n'est pas

- une même implémentation deux fois décrite ;
- le kernel KX108 ;
- une mesure scientifique universelle du raisonnement ;
- une preuve qu'un groupe d'agents dispose d'un espace de réflexion actif.

## Sources

- [Carte B9 — ERA atelier cognitif](https://docs.google.com/document/d/1Que8iatRKSCtGwuFaIHAOFQHGU4_aMn4EKRydYktfQU/edit)
- [Reverse OS — ERA indicateur](https://docs.google.com/document/d/1L_LG0UE4vyLn-iXF0pvjc94owZCI3McF2SWJo3TG8nY/edit)
- [Statut courant du module Brody](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_cognitive_modules_adapter.py)

## Statut

**NAME_COLLISION / TWO HISTORICAL DEFINITIONS / DESIGN_SPEC_NOT_IMPLEMENTED (CURRENT GENERIC MODULE)**.

Voir [audit F0, passe 2](19_F0_SOURCE_TRACE_BATCH2.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Archive World Foundry](https://docs.google.com/document/d/1d5Gf5-r1d43wetqaANCzCff5CPyYckwTw9_AuWwicpg/edit).
- **Lecture / frontière :** WorldSpec (ontology/entities/laws/capabilities/events/initial_state/hidden_state/perturbations/objectives/invariants/renderers) présent dans l'archive ; conception, pas moteur World Foundry installé.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Formule du Savoir](https://docs.google.com/document/d/1bpOAmI8uIjbDYdDLBwkoxBDv5WYIMjv0/edit).
- **Lecture / frontière :** Source primaire indexée ; principes pédagogiques transmis partiellement, pas une formule mathématique universelle prouvée.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [Obsidia V5](https://docs.google.com/document/d/1emMNeq8Lgxckos1B2RoKSISXpTIZHlk4qOYfv7Q9yl8/edit).
- **Lecture / frontière :** Passage lu directement : « PROLOGUE — CONSTRUIRE LE CORPS AVANT DE CHERCHER LE CERVEAU ». C'est une doctrine de construction progressive, pas la preuve que chaque organe est en production.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

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


## Sources et généalogie — F0 (2026-10-08)

- [Obsidia V5, Édition livre (18 août 2026)](https://docs.google.com/document/d/1emMNeq8Lgxckos1B2RoKSISXpTIZHlk4qOYfv7Q9yl8/edit) — passage lu sur la conversion de compétences répétées en calcul, règle, route ou réflexe, pour réserver l'inférence générative à la nouveauté.
- **Frontière :** hypothèse méthodologique et économique, non garantie de performance universelle. Test/benchmark spécifique à produire pour chaque implémentation.

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

`C10` is a **name collision across generations of Obsidia**, not one safely universal concept.

### Historical structural use

Older structured-source packs contain:

```text
Bloc 11 — Trace et Immuabilité (C10)
```

associated with:

- cryptography;
- Merkle structures;
- auditability;
- immutability/trace concepts.

### Current education-roadmap use

Current `docs/EDUCATION.md` uses:

```text
C10 Éducation / Oxygen
```

for the future large education phase that follows stable memory/runtime/cognition foundations.

It explicitly says that this phase is **not yet launched as a massive phase**.

## Purpose

The term therefore cannot be interpreted without context.

## Audit rule

Every `C10` occurrence must identify:

```text
C10_TRACE_IMMUTABILITY_HISTORICAL
or
C10_EDUCATION_OXYGEN_ROADMAP
or
UNRESOLVED_OTHER_C10
```

until naming is formally reconciled.

## It is not

A single current runtime component merely because both source families use the same label.

## Status

**NAME COLLISION RECOVERED / CONTEXT REQUIRED**

---

# 94. Immutable Vote / SIGMA_IMMUTABLE_VOTE_V1

## Definition

Current readonly advisory scoring packet produced by `calculate_immutable_vote()`.

It aggregates peripheral votes into a bounded diagnostic score and advisory label while explicitly preserving X108/KX108 authority.

## Purpose

Give Sigma/audit surfaces a compact measure of vote direction without turning aggregation into sovereignty.

## Hard boundaries

```text
readonly = true
decision_authority = KX108_ONLY
emits_act = false
emits_verdict = false
memory_write = false
kernel_mutation = false
x108_mutation = false
advisory verdict != runtime decision
```

## It is not

The final decision.

## Status

**CURRENT CODE + TESTED**

---

# 95. Balance Obsidienne

## Definition

Current sandbox canon defines the Balance as a **structural weighting operator**.

It asks not merely how many signals exist, but how well an element/path/hypothesis holds relative to:

- invariants;
- coherence;
- utility;
- cost;
- risk;
- admissibility.

The current canon summarizes:

```text
Peser -> Simplifier -> Réintégrer -> Statuer
```

and:

> The Balance does not count. It weighs.

## Relation to AVDR

Current sandbox doctrine states:

```text
AVDR = dynamics of the process
Balance = structural weighting of the process
```

## Important distinction

This current sandbox Balance must not automatically be equated with every historical “Balance Proportionnelle Exponentielle” or with KX108 decision authority.

## Status

**CURRENT SANDBOX CANON / GLOBAL BINDING STILL LIMITED**

---

# 96. Task Forge

## Definition

Historical AVDR module that creates internal tasks, tensions or challenges for a cognitive system to work on.

## Purpose

Move learning from passive response toward active practice/self-challenge in a sandbox.

## It is not

A current autonomous task authority.

## Current relation

Conceptually relevant to:

- World Foundry;
- sandbox exercises;
- Dreaming/replay;
- future Oxygen education.

## Status

**HISTORICAL AVDR MODULE / FUTURE LEARNING REFERENCE**

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [AVDR Auto-Verifiable Developmental Reasoner](https://docs.google.com/document/d/1uDk3FC6a7aBGmGEul4mHzn9fMitc44xRSgPz2kxDzh4/edit).
- **Lecture / frontière :** Task Forge apparaît comme module du protocole de recherche AVDR, sans autonomie exécutoire.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

---
# 97. Solve Engine

## Definition

Historical AVDR module where several reasoning styles/agents attempt to solve a generated task.

## Purpose

Create diversity of candidate approaches before evaluation.

## It is not

A voting authority.

## Status

**HISTORICAL AVDR MODULE / SELECTIVE DESIGN SOURCE**

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [AVDR Auto-Verifiable Developmental Reasoner](https://docs.google.com/document/d/1uDk3FC6a7aBGmGEul4mHzn9fMitc44xRSgPz2kxDzh4/edit).
- **Lecture / frontière :** Solve Engine apparaît comme module de proposition de pistes, sans droit de décision.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

---
# 98. Cognitive Evaluator / Context Filter / Reasoning Trace / Cognitive Calibrator

## Definition

Historical AVDR submodules forming the evaluation/learning half of the loop.

### Cognitive Evaluator

Assesses candidate reasoning/results.

### Context Filter

Applies contextual/domain/symbolic calibration.

### Reasoning Trace

Preserves the path, tensions, choices and feedbacks.

### Cognitive Calibrator

Adjusts how the next cycle should operate based on evaluated outcomes.

## Purpose

Turn an attempt into structured feedback rather than a one-shot answer.

## It is not

Current KX108 governance.

## Current descendants

Parts of the intent are now distributed across:

- receipts/replay;
- memory candidates;
- Sigma/readiness;
- Brody routing;
- domain constraints;
- learning-loop deltas;
- explicit calibration.

## Status

**HISTORICAL AVDR MODULE FAMILY / PARTLY ABSORBED**

## Sources et généalogie — F0 (2026-10-08)

- **Documents :** [AVDR Auto-Verifiable Developmental Reasoner](https://docs.google.com/document/d/1uDk3FC6a7aBGmGEul4mHzn9fMitc44xRSgPz2kxDzh4/edit).
- **Lecture / frontière :** Évaluation/filtrage/trace/calibration explicitement dans l'architecture de recherche, pas connexion actuelle attestée.
- **Statut de preuve :** lien documentaire; pas une preuve de runtime, de priorité intellectuelle ni de validité scientifique. Voir [réconciliation F0](17_F0_SOURCE_RECONCILIATION.md) et [matrice 108 concepts](18_CONCEPT_SOURCE_MATRIX.md).

---
# 99. CG9 Global Provider Binder

## Definition

Current controlled integration boundary between governance and runtime providers.

It allows providers such as Brody Runtime or Obsidure Runtime to execute bounded workloads while remaining non-sovereign.

## Current architecture

```text
CG9 Governance
-> Provider Arbitration
-> Capability Arbitration
-> Invocation Envelope
-> Runtime Execution
-> Runtime Receipt
-> Conformance Proof
```

## Hard boundaries

Providers:

- cannot decide;
- cannot mutate kernel;
- cannot write memory;
- cannot emit actions.

## Purpose

Make providers replaceable executors of bounded work rather than hidden authorities.

## Status

**CURRENT / CLOSED CG9 BINDER SURFACE**

---

# 100. OS3 proof scope

## Definition

Current OS3ProofTicket is a **runtime integrity/audit proof artefact**.

It uses a SHA-256 chain over input, output and trace, then derives a Merkle-style root.

## Purpose

Prove integrity/linkage of the recorded runtime path.

## It does not prove

- a Lean theorem;
- a production RFC3161 timestamp;
- that replay actually ran when `replay_status = NOT_RUN`;
- that the underlying physical claim is true.

## Status

**CURRENT RUNTIME PROOF / CLAIM SCOPE BOUNDED**

---

# 101. Calibration

## Definition

In current Obsidia doctrine, calibration changes **how an organ operates** without creating a new identity.

Examples:

- route adjustment;
- vocabulary adjustment;
- threshold adjustment;
- output/projection adjustment;
- tool preference adjustment.

## Purpose

Improve competence while keeping education/identity separate.

## It is not

- Oxygen's birth;
- canonical memory promotion;
- automatic increase of authority.

## Status

**FOUNDATIONAL CURRENT DISTINCTION**

---

# 102. Maturation

## Definition

Progressive stabilization of routes, tests, refus and learned procedures.

## Purpose

Describe improvement of the existing organism without falsely calling each improvement a new birth or a new intelligence.

## It is not

Identity creation.

## Status

**FOUNDATIONAL EDUCATION DOCTRINE**

---

# 103. One continuity, many organs

## Definition

Core Oxygen/Obsidia doctrine:

```text
one educational/identity continuity
+
many replaceable functional organs
```

The system may replace models, tools, agents and specialized organs without automatically creating a new identity.

## Purpose

Separate identity from implementation.

## It is not

A claim that Oxygen currently exists.

## Status

**FUTURE IDENTITY DOCTRINE / CURRENT ARCHITECTURAL CONSTRAINT**

---

# 104. Calcul de la Balance Mathématique — retrait / réintégration

## Définition historique

Méthode documentée qui retire provisoirement un facteur ou une difficulté d'un calcul, traite la forme réduite, puis réintroduit exactement l'élément retiré par opération inverse ou réciproque.

## Pourquoi

Explorer des transformations réversibles qui rendent les calculs plus maniables sans oublier les facteurs écartés.

## Mécanisme d'exemple de la source

```text
X = (A × B × C) / (D × E × F)
X' = (A × B × C) / (D × F)
X = X' / E, sous hypothèse E != 0
```

L'exemple confirme une **réintégration algébrique élémentaire**, pas un théorème d'accélération universelle : les conditions de définition, le coût du calcul et le gain réel doivent être démontrés séparément.

## Ce que ce n'est pas

- La Balance Proportionnelle Exponentielle (#72) ;
- une opération déjà prouvée pour tous les domaines ;
- le vote Sigma ou le gate KX108.

## Relations et autorité

Méthode mathématique candidate pour traitements spécialisés; **aucune décision, aucun ACT ni mutation kernel**. Correspondance avec la Balance exponentielle : `NOT ESTABLISHED`.

## Origine vérifiée

[Obsidia_Dossier_Technique_Balance_Mathematique](https://docs.google.com/document/d/1SKfhUnnGYKiOM9w8FDPavtEtwqDWb7HH/edit) — section « Algorithme – Le Calcul de la Balance Mathématique ». Attribution personnelle exclusive / date originale exacte non établies.

## Statut

**HISTORICAL DOCUMENTED ALGORITHM SKETCH / MATHEMATICAL GENERALITY UNPROVEN / RUNTIME UNKNOWN**

---

# 105. Mode Shadow — apprentissage passif / non-interférence

## Définition historique

Observer des flux réels (télémétrie, capteurs, interactions), produire des actions *théoriques* en parallèle et comparer aux résultats sans émettre d'action dans l'environnement.

## Pourquoi

Permettre l'évaluation et l'entraînement candidat sur signaux réels tout en protégeant le système en exploitation de l'expérimentation.

## Chaîne décrite

```text
captation non intrusive
→ proposition / simulation interne
→ comparaison avec système observé
→ écart et correction candidate
```

## Ce que ce n'est pas

- un mode LIVE actif ;
- une licence pour capter des données privées sans cadre ;
- un mécanisme d'écriture automatique de poids/mémoire ;
- une preuve que LiteRT, JAX ou les capteurs concernés sont branchés.

## Relations et frontière d'autorité

MMonde, observations datées, WorldStateDelta, Shadow evaluation, expérience candidate. **KX108_ONLY**, `emits_act=false`, mémoire candidate non promue automatiquement. La source emploie des formules de « correction de poids » comme intention historique, non politique de runtime validée.

## Origine vérifiée

[Rapport Technique : Architecture de l'Apprentissage et Sécurité Cinématique (Module 5)](https://docs.google.com/document/d/1iVwqEeo2TTa3Mv6wYFdJOq_8-mAfFpz7-AJ46iMxm7o/edit) — section « Le Mode Shadow ».

## Statut

**HISTORICAL DESIGN / SHADOW MODE NOT VERIFIED AS CONNECTED**

---

# 106. Mémoire Fractale (FAM) / L'Expérience Cognitive Intégrée

## Définition historique

Proposition de mémoire articulant un buffer actif linéaire de type `Map FIFO`, un historique ou archive diachronique et des mécanismes de rangement/scellement. Le document nomme l'ensemble « L'Expérience » et présente la `FAM`.

## Pourquoi

Séparer contexte réactif et continuité durable, maîtriser la saturation et distinguer ce qui reste provisoire de ce qui mérite une conservation longue.

## Ce que ce n'est pas

- la `Native Memory` courante par équivalence de nom ;
- la preuve d'une mémoire autonome, consciente ou inaltérable ;
- une autorité sur la décision ou sur la vérité du monde ;
- l'autorisation d'écrire des souvenirs sans validation.

## Relations et frontière d'autorité

Filiation conceptuelle possible avec Zone Latente (#26), Continuum (#27), MemoryCandidate (#25) et Native Memory (#24), **sans fusion de schémas**. Scellés/Merkle mentionnés dans l'archive : effets actuels à vérifier dans les tests runtime, non supposés.

## Origine vérifiée

[Architecture du Système de Mémoire Obsidia : L'Expérience Cognitive Intégrée](https://docs.google.com/document/d/1SdeEtK9zpZoAgnyTSQtjbwTYO0cDG3_iFqgBof5kRPA/edit) — sections « Fondations », « Mémoire Vive », « Map FIFO ».

## Statut

**HISTORICAL ARCHITECTURE / PARTIAL INTENT ONLY / NOT NATIVE MEMORY CANON**

---

# 107. Curriculum Forge

## Définition historique

Composant éducatif proposé dans le dispositif World Foundry : choisir une prochaine situation d'apprentissage selon l'état de l'agent, ses compétences déjà prouvées, ses lacunes et dépendances, la nouveauté et le risque.

## Pourquoi

Construire une progression par exercices et conséquences plutôt que faire sélectionner arbitrairement les prochains sujets par un LLM.

## Entrées / sortie

```text
agent state + proven skills + gaps
+ dependencies + novelty + risk
→ next educational situation candidate
```

## Ce que ce n'est pas

- `Task Forge` de l'AVDR recherche (#96), qui crée des tensions/tâches internes ;
- un arbitre souverain de missions ;
- un simulateur complet World Foundry ;
- une preuve d'implémentation.

## Relations et autorité

World Foundry (#80), Oxygen et éducation, Skill Forge/Experience Ledger comme éléments du même *design source*. Les propositions restent non exécutables sans contrats et permissions ; décision `KX108_ONLY`.

## Origine vérifiée

[Archive « obsidia suite 29.07 deu »](https://docs.google.com/document/d/1d5Gf5-r1d43wetqaANCzCff5CPyYckwTw9_AuWwicpg/edit) — section « Architecture cible pour la Sandbox Obsidia », juste après `WorldSpec`. Source dialoguée ; attribution et date exacte de la proposition à réconcilier.

## Statut

**HISTORICAL / EDUCATIONAL DESIGN SOURCE / NOT IMPLEMENTED**

---

# 108. Deux thermodynamiques — physique mesurable vs signaux computationnels

## Définition

Obsidia distingue explicitement **la thermodynamique du monde physique**, portant sur des grandeurs mesurées avec unités, sources, modèles, contraintes et incertitudes, de **la thermodynamique computationnelle / cognitive**, où des scores de coût, d'entropie informative ou de dissipation servent à caractériser des processus de calcul.

Ce ne sont **pas** deux interprétations identiques d'une même mesure.

## Pourquoi cette frontière existe

Éviter qu'une valeur comme `entropy_score`, `coherence_temperature`, `dissipation_score`, `thermo_debt`, `compute_cost` ou `attention_cost` soit vendue comme température thermodynamique, chaleur, travail, énergie interne ou entropie physique mesurée.

## Mécanisme actuel (source code et documentation)

Le contrat F19 définit des références de système/mesure et une liaison à des lois/modèles scientifiques. Les évaluations restent **candidates**, conservant unités, erreurs, références et conditions.

```text
signal physique + mesure située + modèle scientifique
      -> contrainte / état thermodynamique candidat
      != vérité physique automatiquement démontrée

métriques internes de cognition / compute
      -> coût, route, alerte / pilotage non souverain
      != grandeur physique
```

## Relations et frontières

- F13 : mesures situées ;
- F18 : références scientifiques, équations, invariants et contraintes ;
- F19 : `PhysicalThermodynamicStateCandidateV0` et objets spécialisés ;
- MMonde et preuve physique sans promotion automatique ;
- Brody peut exploiter les états pour comprendre/proposer, pas décider ;
- **KX108_ONLY**, pas de fusion forcée avec la « Balance exponentielle » historique.

## Origine source vérifiée

- [F19 contrat de thermodynamique physique](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/architecture/PHYSICAL_THERMODYNAMICS_ADAPTER_V0.md)
- [F19 code `periphery/physical_thermodynamics/contracts_v0.py`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/physical_thermodynamics/contracts_v0.py)
- [Piste d'archive sur les régimes physiques (non prouvée)](https://docs.google.com/document/d/1cUJjRYhfn6Sg837G-8GvvTLntNvaLHd3LbwtKF2P6ew/edit)

## Ce que ce n'est pas

- une théorie du tout validée ;
- une identité formelle entre loi physique et score cognitif ;
- une preuve de fonctionnement d'un simulateur thermodynamique autonome.

## Statut

**CURRENT PHYSICAL ADAPTER CODE + DOC READ / NOT A PROOF OF PHYSICAL TRUTH OR SCIENTIFIC NOVELTY**.
