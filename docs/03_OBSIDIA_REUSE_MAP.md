# 03 — Obsidia Reuse Map

This project starts by reusing Obsidia. It must not rebuild existing organs under new names.

## obsidia-x108-proofs

Reuse / audit:

- OS Trad -> IR -> Reverse OS path;
- Brody readonly/advisory boundaries;
- MMonde source pack and current runtime boundary;
- receipts and replay patterns;
- provenance conventions;
- context packets;
- event structures;
- kernel authority separation.

Do not reintroduce obsolete runtime assumptions.

Current doctrine to preserve:

```text
KX108_ONLY
memory_write = False where current runtime requires it
emits_act = False for cognitive/perception organs
kernel_mutation = False
Graphiti / Neo4j runtime = 0
Native Memory = active memory path
```

## SENS / Cognition

Primary audit target.

Map:

```text
OccurrenceClaim
OccurrenceDerivation
EventCandidate
EventRef
occurrence_status
```

against:

```text
WorldState
Action
Transition
ObservedState
ExperienceCandidate
```

Objective: no duplicate semantics.

## MMonde

MMonde is the common grammar for situated reality.

Expected concepts:

- identity;
- object;
- agent;
- state;
- event;
- relation;
- time;
- duration;
- reference frame;
- scale;
- transformation;
- constraint;
- provenance;
- uncertainty;
- competing hypotheses;
- consequence;
- stoppability.

This project should strengthen the executable/data-contract side of those concepts without turning MMonde into an authority.

## Native Memory

Use for:

- chronological context;
- validated experience;
- previous failures;
- previous successful routes;
- compact reusable skill metadata.

Do not use memory as:

- hidden decision authority;
- automatic truth store;
- raw dump of every model output.

## Brody

Brody's future role here:

```text
contextualize
compose
compare
select bounded tools
form hypotheses
build generation plans
build learning candidates
explain conflicts
```

Brody should progressively internalize visual/world competence without collapsing OS, MMonde, Memory and X108 boundaries.

## Reverse OS

Reverse OS projects stabilized internal state outward.

Do not confuse:

```text
INWARD:
world -> OS translation -> internal representation

OUTWARD:
internal representation -> Reverse projection -> text/UI/image/action affordance
```

## GPS / Defense

Reuse the current pattern:

```text
physical evidence
 -> observation envelope
 -> Physical Reality Gate
 -> DomainState
 -> governance request
 -> receipt
```

Visual, depth or trajectory evidence must enter as another bounded source, not as authority.

## Jarvis / Jarjar

Later consumers/producers of observations:

- camera;
- screen;
- microphone/audio;
- computer state;
- human interaction.

Jarvis must consume common contracts rather than invent an independent vision ontology.

## Monde / Pokémon

Presentation and operational visibility layer.

Potential future display:

- active sensors;
- observations;
- hypotheses;
- state changes;
- learned skills;
- uncertainty;
- tool routing;
- experiments;
- replay state.

It does not become cognition or decision authority.
