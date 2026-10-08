# Brody World Physique Obsidia

**Status:** IMAGE R1 CPU EDITOR + I1 JARVIS-QWEN-VL LOCAL CLIENT IMPLEMENTED; PHYSICAL-PC CHECK AND GENERATOR NOT YET VALIDATED  
**Authority:** Obsidia / X108 remains external and unchanged.  
**Purpose:** visual perception, physical-world learning and **image generation with reverse evaluation**, while keeping Obsidia's existing organs separate.

> **FOCUS PRODUIT AU 2026-10-08 : BRODY IMAGE** — comprendre, apprendre et générer des images / vidéos à partir du monde physique. Les 108 concepts de l'Atlas servent de **référentiel historique secondaire**, pas de roadmap produit. **Lire d'abord** le [plan maître Brody Image](docs/21_BRODY_IMAGE_MASTER_PLAN.md) et la [carte des branches + moteurs externes](docs/22_IMAGE_BRANCH_AND_DONOR_MAP.md). Aucun modèle externe n'est déclaré installé ni intégré d'après cette passe.

## Core idea — Brody Image

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
- [108-concept source traceability matrix](docs/18_CONCEPT_SOURCE_MATRIX.md)
- [F0 source trace batch 2 — ADeLe, ERA, SENS/GPS, runtime contracts](docs/19_F0_SOURCE_TRACE_BATCH2.md)
- [F0 source-gap triage — C10, UNKNOWN, visual, Dreaming, quadrillage](docs/20_F0_FINAL_SOURCE_GAPS.md)
- **[BRODY IMAGE — visual learning and generation master plan](docs/21_BRODY_IMAGE_MASTER_PLAN.md)**
- **[Real upstream branches, code seams and open-source donors](docs/22_IMAGE_BRANCH_AND_DONOR_MAP.md)**
- **[Original learning methods → image experiments, provenance and test gates](docs/23_BRODY_IMAGE_LEARNING_TRACEABILITY.md)**
- **[Brody Image original vision fidelity: source/IN, layered reconstruction, region rigour and functional tests](docs/24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md)**
- **[Image I1/R1 CPU executable baseline — subject isolation, transplant and pixel fidelity report](docs/25_BRODY_IMAGE_I1_R1_PROTOTYPE_CPU.md)**
- **[Jarvis Qwen-VL local adapter — descriptive candidate, no new model download, fixed/portable setup](docs/26_BRODY_IMAGE_I1_JARVIS_QWEN_VL_ADAPTER.md)**

## First actual image editor (I1/R1 CPU)

This baseline preserves known source pixels and creates a real edited PNG; it **does not yet synthesize new images with an ML model**.

```sh
python -m pip install -r requirements-image.txt
python -m unittest discover -s tests -p "test_*.py" -v
python -m examples.demo_image_v0 --out build/brody-image-demo
```

With personal files and a prepared mask:

```sh
python -m brody_world_physique.image_v0 --source photo.png --mask masque.png --background scene.png --x 80 --y 35 --out build/essai
```

Outputs: `cutout.png`, `composite.png`, `report.json`. The demonstration fixture is **SYNTHETIC**, not a claim of natural-scene understanding or learned image generation.


## Existing Jarvis/Qwen-VL vision model: reuse, not reinstall

The separate Jarvis installation provides the OpenAI-compatible local Qwen-VL
endpoint (normally `127.0.0.1:8081`). Brody Image now has a small,
**loopback-only**, file-based client of that **existing** vision API:

```powershell
py -m brody_world_physique.jarvis_vision_v0 --image "C:\\photos\\test.jpg" --out "build\\vision-candidate.json"
```

The server must **already be running on the same PC**, or be available over an
explicit local SSH tunnel. The output is an **unverified text description
candidate**, not an F16 real-world observation. It does **not** pass through
Brody chat, Binder, native memory, or a generation model yet. Tests mock the
local HTTP server; **they are not a successful real Qwen-VL PC connection**.
See [26 — I1 Jarvis adapter and honest bring-up steps](docs/26_BRODY_IMAGE_I1_JARVIS_QWEN_VL_ADAPTER.md).

## Current milestone

**Brody Image I1/R1 CPU:** deterministic isolation and compositing implemented on `main`, with source/output hashing, fidelity controls, synthetic test fixtures and source-preserving boundaries. Details in [25 — executable baseline](docs/25_BRODY_IMAGE_I1_R1_PROTOTYPE_CPU.md).

**Still unproven:** live PC Qwen-VL bridge, Brody/Binder/F16 image flow, arbitrary background segmentation, image-generating model/weights, reverse visual evaluation, 3D, video/world physics and learned retention. A real photo and mask can be fed through the local CLI; the synthetic demo alone does not establish these capabilities.

**Historical F0:** the 108-concept archive and source attribution exist for traceability; their complete documentary audit remains open but **does not block the bounded image editor**. Old F0 PR work is consolidated on `main`; obsolete historical PRs have been closed. Keep `KX108_ONLY`, no memory auto-promotion or upstream kernel mutation.
