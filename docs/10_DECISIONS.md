# 10 — Frozen Architecture Decisions V0

These decisions summarize the current foundation and should be changed only by an explicit architecture revision.

## D-001 — The project is Obsidia-native

External projects donate capabilities. Obsidia defines the contracts.

## D-002 — Skill is the primary objective

The system is optimized for doing, predicting, correcting and reusing methods, not for maximizing stored encyclopedic text.

## D-003 — World understanding begins with state and transition

Primary abstraction:

```text
State(t) + Action/Transformation -> State(t+1)
```

## D-004 — Formal knowledge remains available but is not required for every skill

A system may learn a reliable physical regularity before possessing its formal scientific definition.

## D-005 — Prediction is not observation

Predicted, simulated, generated and observed states are distinct evidence classes.

## D-006 — Perception is not truth

Every model output is a candidate with source, provenance and uncertainty.

## D-007 — Experience is not automatically memory truth

New learning enters as ExperienceCandidate and requires promotion criteria.

## D-008 — Weight updates are late-stage learning

First improve:

- routes;
- skills;
- tools;
- deterministic transforms;
- retrieval;
- replay;
- adapters.

Only then consider LoRA/fine-tuning/distillation.

## D-009 — Visual generation is a closed learning loop

```text
understand
 -> represent
 -> generate
 -> re-perceive
 -> compare
 -> correct
```

## D-010 — Reverse360 is a consistency test

Its purpose is to test identity, geometry and world persistence across viewpoint changes, not merely create panoramic media.

## D-011 — Small specialized models are preferred when sufficient

Model size is not a status symbol. A small transition model can be preferred over a frontier model if it performs the bounded skill better and is auditable.

## D-012 — Multiple organs may disagree

Contradiction is preserved until resolved.

## D-013 — External generators are replaceable

Canonical contracts must not depend on Z-Image, SANA, FLUX, ComfyUI or any single vendor.

## D-014 — KX108_ONLY remains intact

This repository cannot authorize action by itself.

## D-015 — Native Memory remains the active memory direction

Do not reintroduce Graphiti/Neo4j runtime as part of this project.

## D-016 — GPS/Defense has stricter dependency rules

Licensing, provenance and source integrity must prevent research-only components from entering the defense path.

## D-017 — Trading is excluded

This project must not modify or absorb the Trading domain.

## D-018 — Build starts doc-first

No dependency avalanche before:

- contract audit;
- hardware inventory;
- minimal benchmark definition.

## D-019 — Each layer speaks its own language

Sensors, visual models, SENS, MMonde, Brody, Memory and X108 retain distinct responsibilities and representations.

## D-020 — The long-term target is progressive internalization

Brody begins by orchestrating external perception/generation organs.

Over time it may internalize:

- visual representations;
- transition expectations;
- generator planning;
- compact decoders/adapters;
- learned skills.

Progressive internalization must not collapse governance boundaries.
