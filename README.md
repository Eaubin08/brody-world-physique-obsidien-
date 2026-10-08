# Brody World Physique Obsidia

**Status:** FOUNDATION / DOC-FIRST / NO RUNTIME YET  
**Authority:** Obsidia / X108 remains external and unchanged.  
**Purpose:** build the physical-world, visual, temporal and action-consequence learning layer used by Brody without turning Brody into a monolithic model.

## Core idea

The project is not trying to make a model memorize the world.

It builds a system that can:

1. observe a state;
2. situate it in space and time;
3. represent objects, relations, provenance and uncertainty;
4. observe or propose an action/transformation;
5. predict the next state;
6. compare prediction with reality;
7. store the validated experience;
8. improve routing, skills and expectations;
9. modify model weights only when accumulated evidence justifies it.

```text
WorldStateV0(t)
    + WorldTransformationV0
        |
        v
prediction / transition model
        |
        v
WorldStateProjectionV0(t+1)
        |
        +---- compare ---- WorldStateV0(t+1 observed/candidate)
                           |
                           v
                    WorldStateDeltaV0
                           |
                           v
              WorldExperienceCandidateV0
                           |
              +------------+------------+
              |            |            |
           Memory         Skill      Invariant
              \            |           /
               +-----------Brody------+
```

## Doctrine

- **Skill before encyclopedic knowledge.**
- **State -> action -> consequence before verbal definition.**
- Space, time, identity, relation, transformation, provenance and uncertainty are first-class.
- Perception is evidence, not truth.
- External AI models are replaceable organs, not canonical cognition.
- Native Memory provides context and validated experience; it does not become decision authority.
- Learning may first modify routing, skills, replay strategy and expectations.
- Parametric learning (LoRA/fine-tuning/distillation) is a later, evidence-driven step.
- Brody proposes/composes; **KX108_ONLY** remains the decision authority.
- No external model may bypass Obsidia contracts or mutate the kernel.
- No Graphiti/Neo4j runtime is reintroduced here.
- Trading is out of scope.

## Relation to existing Obsidia layers

This repository does **not** replace:

- OS Trad / IR
- SENS / Cognition
- MMonde
- Native Memory
- Brody
- Reverse OS
- X108 / GuardX108 / KX108
- receipts / replay

It prepares a reusable physical/visual/world layer that can later feed:

- Brody visual cognition and generation;
- GPS / Defense / Aviation;
- Jarvis / Jarjar perception;
- Monde / Pokémon visualization;
- future robotics or embodied agents.

## Documentation

- [Vision and doctrine](docs/00_VISION_DOCTRINE.md)
- [Target architecture](docs/01_ARCHITECTURE.md)
- [Canonical contracts](docs/02_CONTRACTS.md)
- [Obsidia components to reuse](docs/03_OBSIDIA_REUSE_MAP.md)
- [External open-source component map](docs/04_EXTERNAL_COMPONENTS.md)
- [Learning and memory loop](docs/05_LEARNING_MEMORY.md)
- [Forge plan F0-F10](docs/06_FORGE_PLAN.md)
- [Validation and tests](docs/07_TEST_STRATEGY.md)
- [Licences, provenance and boundaries](docs/08_LICENSE_PROVENANCE.md)
- [PC bring-up checklist](docs/09_PC_BRINGUP.md)
- [Frozen architecture decisions](docs/10_DECISIONS.md)
- [Sources and upstream references](docs/11_SOURCES.md)
- [Obsidia / user primary sources](docs/12_OBSIDIA_USER_SOURCES.md)
- [F0 cross-audit — SENS / MMonde / Memory / GPS](docs/13_F0_CROSS_AUDIT.md)
- [F0 learning-loop contract implementation](docs/14_F0_LEARNING_LOOP_IMPLEMENTATION.md)
- [Obsidia concept atlas / definitions](docs/15_CONCEPT_ATLAS.md)
- [Concept-definition audit method](docs/16_CONCEPT_AUDIT_METHOD.md)
- [F0 reconciliation of user primary sources and conflicting definitions](docs/17_F0_SOURCE_RECONCILIATION.md)
- [103-concept source traceability matrix](docs/18_CONCEPT_SOURCE_MATRIX.md)

## Current milestone

**F0 — Cross-audit + learning-loop contracts implemented; source reconciliation in progress (NOT DOCUMENTARY FREEZE).**

The four missing learning-loop contracts are implemented with an additive `TransitionTransformationBindingV0`, explicit schema versions and sovereignty tests. No upstream `TransitionV0` mutation was made.

**Current documentary gate:** reconcile the user's original concept definitions, source excerpts, attribution, genealogy and historical-vs-runtime differences (see docs/17 and docs/18). The atlas covers 103 named concepts but its individual source audit is not closed. The related two previous F0 PRs remain unmerged; new reconciliation work is stacked separately and does **not** affect `main`.

Model downloads remain deferred. **Do not start F1 / PC installation before the documentary/contract freeze is explicitly decided.**
