# Brody World Physique Obsidia

**Status:** BRODY IMAGE: REAL PC QWEN-VL DESCRIPTION VERIFIED BY USER; CPU IMAGE EDITOR + LOSSLESS REVERSO EXPERIMENT + RETENTION CANDIDATE GATES IMPLEMENTED; WORLD MODEL / GENERATOR / LEARNING RUNTIME NOT CONNECTED  
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
- **[Reverso + World Model + selective learning: source-grounded method and executable first slice](docs/27_REVERSO_WORLD_MODEL_APPRENTISSAGE_SELECTIF.md)**\n- **[Pre-verbal learning: situated world prediction, physics/sensor evidence, scoped knowledge vs truth](docs/28_APPRENTISSAGE_PREVERBAL_MONDE_PHYSIQUE.md)**
- **[Executable first pre-verbal prediction experiment — held-out future measurement, source/frame constraints and baseline checks](docs/29_PREVERBAL_PREDICTION_EXPERIENCE_V0.md)**
- **[First real-video intake — human annotated 4 positions, forecast sealed before showing frame 4](docs/30_PREMIERE_VIDEO_PHYSIQUE_ANNOTATION_MANUELLE.md)**
- **[Controlled automatic orange-ball detection on the exact simulated test video (SHA-256 pinned), then held-out evaluation](docs/31_BALLE_AUTO_SOURCE_PINNEE.md)**
- **[Experiential learning without preloaded physics laws: 8 simulated videos, empty/one/four experiences, holdout and honest benchmarks](docs/32_EXPERIENCES_ZERO_SAVOIR_SANS_LOI.md)**
- **[Twelve-video transfer probes — new object colors/shapes, mobile viewpoint, surprise, contradictory experience, occlusion, Reverso frame preview](docs/33_EPISODES_TRANSFER_MONDE_INCONNU_V1.md)**
- **[Image-first drawing school and candidate memory — source-guided strokes, pixel feedback, negative-transfer HOLD, episode ledger and unseen drawing exams](docs/34_ECOLE_DE_DESSIN_MEMOIRE_EXPERIENTIELLE.md)**
- **[Drawing class V1 — erase/replace gestures, raster-traced curves/circles, memory-sourced mistakes and six new exams](docs/35_ECOLE_DESSIN_V1_COURBES_GOMME_MEMOIRE.md)**
- **[BRODY_EXPERIENCE_MEMORY_V1 — observation, raster interpretation, actual chosen procedure/code fingerprints, executed gestures, mistakes, evaluation and deterministic memory replay](docs/36_BRODY_EXPERIENCE_MEMORY_V1_PROCEDURES_REPLAY.md)**
- **[Drawing instruments V2 — learn which pencil/pen/nib tool to route by observed lesson feedback, with 0/1/9 episodes, unknown HOLD and sealed future-target trials](docs/37_ECOLE_INSTRUMENTS_SELECTION_EXPERIENTIELLE_V2.md)**

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
Brody chat, Binder, native memory, or a generation model yet. CI tests mock the local HTTP server; **the user's later Windows PC run additionally validated the real Qwen-VL connection**.
See [26 — I1 Jarvis adapter and honest bring-up steps](docs/26_BRODY_IMAGE_I1_JARVIS_QWEN_VL_ADAPTER.md).

## Reverso pixel roundtrip (new bounded method experiment)

This is a **literal decoded RGBA pixel identity** baseline, not semantic
segmentation, AI generative reconstruction or learned world physics. The source
is decomposed into lossless spatial layers and reconstructed *from saved
layers*, then validated pixel by pixel / using an exact decoded pixel digest.

```powershell
py -m brody_world_physique.reverso_learning_v0 --image "C:\\photos\\reference.jpg" --out "build\\reverso-photo"
```

Result: `manifest.json`, independent `lossless_layers/*.png`, and
`reconstructed.png`. The module also defines **candidate** world relations and
a proposed `triage_learning` classification of source, raw outputs, skills,
invariants, errors and hypotheses, with NO native-memory writes. See
[27 — Reverso, world model and selective learning](docs/27_REVERSO_WORLD_MODEL_APPRENTISSAGE_SELECTIF.md).

**Physical confirmation:** the user ran the Jarvis Qwen-VL endpoint on their
fixed Windows PC with a personally selected photo; model description and
`build/vision-candidate.json` were produced. This proves the local
file-to-Qwen-description route on that PC only. The photo and output are not
committed to GitHub. Connecting F16/MMonde/World Model to this receipt, Brody
reasoning, Binder and genuine generation remain future work.

## First pre-verbal world experiment — independent held-out observation

The module [`preverbal_prediction_v0.py`](brody_world_physique/preverbal_prediction_v0.py)
tests a **kinematic mathematical candidate**, not learned physical laws: 3 prior
source-tagged positions -> predict a 4th -> compare against independent held-out
measurement and static/linear benchmarks. Different frames, units or observed vs
synthetic source types are rejected; no canonical knowledge or memory write.

```powershell
py -m examples.demo_preverbal_world_v0 --out build/preverbal-world-demo
py -m brody_world_physique.preverbal_prediction_v0 --input build/preverbal-world-demo/source_measurements.json --out build/preverbal-world-demo/result.json
```

This demonstration is SYNTHETIC. Real physical-world understanding,
reliable measurement extraction from video, transfer and learning are **not
proven**. See [29 — pre-verbal prediction protocol](docs/29_PREVERBAL_PREDICTION_EXPERIENCE_V0.md).

## First source-tagged video experiment (manual object points)

[Video annotation module](brody_world_physique/video_observation_v0.py):
reuse the optional OpenCV library already used in Jarvis. Choose a local
video and click a target in three frames; **a forecast is written to disk
before the fourth frame is opened for annotation**. Then compare against
the fourth frame, storing source video SHA-256 and explicit camera/time/
object-identity uncertainty. This is not automatic tracking, a new model
installation, physical-law proof or an adaptive learned world model.
Real video observations have NOT been run by CI (mocked GUI/decode tests only). **Video origin must be declared** with `--source-kind SIMULATED`, `GENERATED` or `OBSERVED_CLAIM`. The manual GUI now shows a click marker and requires **Enter/Space confirmation** (R retry, Esc cancel).

```powershell
py -c "import cv2;print(cv2.__version__)"
py -m brody_world_physique.video_observation_v0 --video "C:\\videos\\balle.mp4" --out "build\\first-real-video" --interval-seconds 0.1 --source-kind SIMULATED
```

See [30 — first real-video annotation protocol](docs/30_PREMIERE_VIDEO_PHYSIQUE_ANNOTATION_MANUELLE.md).

## Controlled automatic detection of the demo ball (no manual clicks)

For the **single known simulated video** with SHA-256
`a089fdff99f20df5a54e227f46f3b869feb6764b793e2c8e5e024c065b17153f`,
[`auto_ball_demo_v0.py`](brody_world_physique/auto_ball_demo_v0.py)
extracts ball centers by color/shape directly from native image pixels.
OpenCV decodes the local MP4; Pillow analyzes HSV. The forecast is written
*before the fourth video frame is read*; the source remains `SIMULATED`.
No generative model, universal object detector, learned physics or memory write.

```powershell
py -m brody_world_physique.auto_ball_demo_v0 --video "$env:USERPROFILE\\Downloads\\brody_balle_chute_simulee.mp4" --out "build\\auto-ball-$(Get-Date -Format yyyyMMdd-HHmmss)"
```

See [31 — pinned automatic ball measurement](docs/31_BALLE_AUTO_SOURCE_PINNEE.md).

## Learn motion patterns from experience (not a hardcoded physics law)

[`experiential_video_v0.py`](brody_world_physique/experiential_video_v0.py)
begins with **empty candidate memory** and `HOLD_NO_EXPERIENCE`. Four TRAIN
videos yield source-tagged motion histories. The learner matches patterns
with nearest previously observed transitions, with no built-in gravity,
bounce, or wind formula. It freezes memory BEFORE four distinct TEST
videos, emits candidate predictions before future frame decoding, and
reports both errors and honest HOLD rates. A programmed orange-marker
detector + numerical association algorithm are still necessary; this is
**self-supervised on SIMULATED data**, not a learned physical world model.
No pretrained vision model or new weights are installed.

Download the 8-clip suite archive linked separately in this conversation,
extract to a local folder, then run `--suite <folder>/suite.json` and
`--train-videos 0`, `1` and `4` with separate output folders.
[Complete Windows PowerShell commands and limits](docs/32_EXPERIENCES_ZERO_SAVOIR_SANS_LOI.md).

## Visual-transfer stress battery V1 (no domain-physics formulas in learner)

[12 videos: 6 source experiences + 6 withheld transfer cases](docs/33_EPISODES_TRANSFER_MONDE_INCONNU_V1.md).
The new [probe](brody_world_physique/world_transfer_probe_v1.py) uses source-tagged
OpenCV observations with synthetic scene anchors, **not** a universal
multimodal detector or a learned 3D world model. It checks invariance to
changed target color/shape, compensates a synthetic moving camera using a
visible static fiducial, marks surprising outcome changes, abstains on
conflicting histories and does not hallucinate missing video observations.
[Reverso-style preview](examples/reverso_future_preview_v1.py) translates a
predicted location into a synthetic next-frame candidate by reusing OpenCV
masks/inpainting, then compares it with the held-out frame. The image content
beyond target position is **not** generated or learned from a world model.

```powershell
py -m examples.generate_transfer_probes_v1 --out "build\\transfer-suite"
py -m brody_world_physique.world_transfer_probe_v1 --suite "build\\transfer-suite\\suite.json" --out "build\\transfer-anchored" --camera-mode anchored
py -m examples.reverso_future_preview_v1 --suite "build\\transfer-suite\\suite.json" --forecasts "build\\transfer-anchored\\forecasts_precommitted.jsonl" --out "build\\transfer-preview"
```

No model installation, KX108-only fields, no kernel changes or native memory
writes. The train/test source split remains immutable; all videos are
**SIMULATED**, and neither physics truth nor human-like understanding is
established.

## First drawing-school V0 — images before videos

[Drawing school](brody_world_physique/drawing_school_v0.py) implements bounded
**teacher image -> pupil pen strokes -> measured correction -> candidate
episodic/skill memory -> new unseen drawing tests**. It reuses Pillow and
existing Reverso/learning source policy, not an image foundation model.
The learner is not given shape labels or domain-physics formulas; its
pen gestures, pixel-feedback search, reference feature matching and
translation/scaling are **programmed**. It can learn/replay a series of
strokes for small synthetic line drawings; an unseen shape can cause
**negative transfer**, which is recorded and rejected before repetition.

```powershell
py -m brody_world_physique.drawing_school_v0 --out "build\\drawing-first-school"
```

The output contains PNG models, attempts and corrections; a replay-verified
local SHA-256-chained `candidate_experience_ledger.jsonl` and
`candidate_skill_memory.json`. This is **NOT Obsidia Native Memory**, not
its canonical Merkle sealing, and it does not promote any skill as truth.
[Full provenance from original Google Drive documents and roadmap](docs/34_ECOLE_DE_DESSIN_MEMOIRE_EXPERIENTIELLE.md).

## Drawing school V1 — correct old strokes, trace curved outlines

After the user reviewed V0 drawings, V1 adds [motor-gesture
correction](brody_world_physique/drawing_school_v1.py): `ADD`, `ERASE`
and `REPLACE` old strokes against a visible teacher reference, and
reuses experience-derived candidates for new triangles, circles,
crosses and curves. It includes generic raster thinning/path tracing
and evaluates 6 distinct unseen image references (visible at exam).
This is **guided copying**: the drawing correction algorithm is
engineered, and neither object semantics nor original image generation
has been learned.

```powershell
py -m brody_world_physique.drawing_school_v1 --out "build\\school-v1-demo"
```

`teacher_images/` are never overwritten, `attempts/` show raw recollection
versus accepted memory and corrected output, and the local SHA-256
episode ledger records harmful memory transfers as candidates.
No Native Memory writes. See [35 — measured six-image
experiment](docs/35_ECOLE_DESSIN_V1_COURBES_GOMME_MEMOIRE.md).

## Procedure-linked experience memory V1 (non-canonical)

Every drawing-school V1 lesson and exam now emits a
[`BRODY_EXPERIENCE_MEMORY_V1` episode](brody_world_physique/experience_memory_v1.py)
containing the source image SHA-256, *measured* raster interpretation (no
semantic claim), chosen method, whitelisted real Python
`module_path / function_name / file_sha256`, initial gestures, actual
`ADD / ERASE / REPLACE` steps, measured results, failed recalled procedures
and a **candidate** skill. The code fingerprint references actual functions;
the memory never stores executable code. A fixed-code **independent replay**
checks every operation, result image, source and module SHA. An
[isolated readonly procedure recall](brody_world_physique/candidate_skill_retrieval_v1.py)
shows which previous skill and current code *might* apply to a new visible
image, with HOLD if absent or unfamiliar. This does not write Obsidia's
Native Memory, ACT, promote results or train a vision model.

```powershell
py -m brody_world_physique.drawing_school_v1 --out "build\\new-school-memory"
py -m brody_world_physique.experience_memory_v1 --verify "build\\new-school-memory"
py -m brody_world_physique.candidate_skill_retrieval_v1 --memory "build\\new-school-memory" --image "build\\new-school-memory\\teacher_images\\examen_triangle.png"
```

See [36 — provenance, explicit choice and memory/code boundary](docs/36_BRODY_EXPERIENCE_MEMORY_V1_PROCEDURES_REPLAY.md).

## Instrument choice V2 — choosing among existing digital drawing tools

[`instrument_school_v2.py`](brody_world_physique/instrument_school_v2.py)
uses the **verified prior drawing-school V1 memory** to obtain source gestures,
then tests three existing synthetic computer tools: a soft pencil, a uniform
pen, and a direction-varying nib. The teacher gives an intent but does not
tell the student the corresponding tool. Every TRAIN lesson exercises all
three options and saves the observed pixel errors. On a new TEST sketch,
Brody proposes an instrument by **mean prior loss for the same intent**,
not by inspecting the hidden target or a fixed intent→tool map in the
student selector. New intents lead to **HOLD**.

```powershell
py -m brody_world_physique.instrument_school_v2 --out "build\\instrument-school-v2"
py -m brody_world_physique.instrument_school_v2 --verify "build\\instrument-school-v2"
```

Outputs include candidate scores, a SHA-chained lesson ledger,
`choices_before_heldout.jsonl`, actual image comparisons, and a code identity
registry. **These are small computer-drawn 2D fixtures with teacher targets
generated by the same tool renderer**: matching a teacher target does not
prove artistic creativity, general perception, true pen physics, or training
a new visual model. No Native Memory writes or authority promotion.
[Full experiment and Windows commands](docs/37_ECOLE_INSTRUMENTS_SELECTION_EXPERIENTIELLE_V2.md).

## Current milestone

**Brody Image I1/R1 CPU:** deterministic isolation and compositing implemented on `main`, with source/output hashing, fidelity controls, synthetic test fixtures and source-preserving boundaries. Details in [25 — executable baseline](docs/25_BRODY_IMAGE_I1_R1_PROTOTYPE_CPU.md).

**Still unproven:** Brody/Binder/F16 image flow, arbitrary background segmentation, image-generating model/weights, reverse visual evaluation, 3D, video/world physics and learned retention. A real photo and mask can be fed through the local CLI; the synthetic demo alone does not establish these capabilities.

**Historical F0:** the 108-concept archive and source attribution exist for traceability; their complete documentary audit remains open but **does not block the bounded image editor**. Old F0 PR work is consolidated on `main`; obsolete historical PRs have been closed. Keep `KX108_ONLY`, no memory auto-promotion or upstream kernel mutation.
