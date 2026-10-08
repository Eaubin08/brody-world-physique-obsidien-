# 11 — Sources and Upstream References

**Purpose:** keep the project auditable and make every external idea traceable to a primary source.

## Source policy

Priority order:

1. official repository;
2. official project page;
3. paper / arXiv / publisher;
4. official vendor documentation;
5. secondary discovery source (for example Vision IA).

A secondary source may surface a project, but no component becomes `TAKE` or `ADAPT` until its primary sources and licence have been checked.

---

## A. Transition / World Dynamics

### EB-JEPA — Meta FAIR

**Role:** lightweight reference and laboratory for prediction/planning in representation space.

- Official repo: https://github.com/facebookresearch/eb_jepa
- Action-conditioned example: https://github.com/facebookresearch/eb_jepa/tree/main/examples/ac_video_jepa

Key reason for Obsidia:

```text
observation + action -> future representation
```

Status: **TAKE / LAB**

### TD-MPC2

**Role:** compact learned dynamics and planning/control.

- Official repo: https://github.com/nicklashansen/tdmpc2
- Project/paper links are maintained from the official repository README.

Key reason for Obsidia: published small configurations make it a strong benchmark for bounded transition learning.

Status: **TAKE / DISSECT**

### DreamerV3

**Role:** reference for learning from experience and training behavior on imagined trajectories.

- Official repo: https://github.com/danijar/dreamerv3

Status: **REFERENCE**

### Dream-RSI

**Role:** reference for recursive improvement using history/replay without immediately modifying base-model weights.

- Official repo: https://github.com/zhengkid/Dream-RSI
- Official project page: https://dream-rsi.com/

Status: **REFERENCE / WATCH**

Current upstream note: paper/project are public; full code/reproduction release must be rechecked before implementation.

---

## B. Visual Perception

### MiniCPM-V

**Role:** lightweight local image/video understanding candidate.

- Official repo: https://github.com/OpenBMB/MiniCPM-V

Status: **TAKE CANDIDATE**

### MobileSAM

**Role:** lightweight segmentation.

- Official repo: https://github.com/ChaoningZhang/MobileSAM

Status: **TAKE CANDIDATE**

### EfficientTAM

**Role:** efficient image/video segmentation and temporal tracking.

- Official repo: https://github.com/yformer/EfficientTAM

Status: **TAKE CANDIDATE**

### Depth Anything 3

**Role:** depth, spatial geometry and multiview candidate extraction.

- Official repo: https://github.com/ByteDance-Seed/Depth-Anything-3

Status: **TAKE CANDIDATE**

### Grounding DINO

**Role:** open-set/open-vocabulary grounding and detection.

- Official repo: https://github.com/IDEA-Research/GroundingDINO
- Paper is linked from the official repository.

Status: **TAKE CANDIDATE**

---

## C. Local Image Generation

### stable-diffusion.cpp

**Role:** low-overhead inference runtime for local/quantized generation.

- Official repo: https://github.com/leejet/stable-diffusion.cpp

Status: **TAKE CANDIDATE**

Important: upstream changes rapidly; record exact commit at installation.

### Z-Image

**Role:** efficient image generation/editing candidate.

- Official repo: https://github.com/Tongyi-MAI/Z-Image

Status: **TAKE CANDIDATE**

### SANA — NVIDIA Research / NVLabs

**Role:** efficient generative architecture and local generator candidate.

- Official repo: https://github.com/NVlabs/Sana
- Project material is linked from the repo.

Status: **TAKE / REFERENCE**

### MiniT2I

**Role:** small generation architecture useful as a learning laboratory.

Primary implementation/reference links must be frozen only after the exact implementation selected for the PC build is audited.

Status: **LAB / REFERENCE**

---

## D. Workflow / Generator Bus

### ComfyUI

**Role:** modular image/video/audio/3D workflow runtime and API.

- Official repo: https://github.com/Comfy-Org/ComfyUI
- Official docs: https://docs.comfy.org/
- Official organization: https://github.com/Comfy-Org

Status: **TAKE AS TOOL BUS**

Obsidia rule: canonical contracts must stay outside Comfy workflows.

---

## E. Spatial / Reverse360 / Persistent World

### WorldFM

**Role:** controlled viewpoint generation from reference image + target camera pose.

- Official repo: https://github.com/inspatio/worldfm

Status: **ADAPT / REVERSE360 LAB**

Important: audit submodules and their licences separately.

### InSpatio World

**Role:** persistent spatial/world generation research.

- Official repo: https://github.com/inspatio/inspatio-world

Status: **REFERENCE / LATER LAB**

Its published pipeline currently relies on several external models; provenance must therefore be evaluated per dependency.

---

## F. Embodied Skill / Robotics Benchmark

### SmolVLA / LeRobot

**Role:** compact vision-language-action benchmark for embodied know-how.

- Official LeRobot repo: https://github.com/huggingface/lerobot
- SmolVLA documentation: https://github.com/huggingface/lerobot/blob/main/docs/source/smolvla.mdx

Status: **BENCH / REFERENCE**

---

## G. Large Teacher / State-of-the-Art References

### V-JEPA 2 / 2.1 / AC

**Role:** high-end reference for video representation, prediction and planning.

- Official repo: https://github.com/facebookresearch/vjepa2

Status: **REFERENCE**

Use EB-JEPA for first local experiments; use V-JEPA to compare architectural direction.

### NVIDIA Cosmos

**Role:** large Physical AI / world-model reference and possible external teacher/benchmark.

- Official repo: https://github.com/NVIDIA/cosmos
- NVIDIA developer/model documentation should be rechecked for the exact Cosmos model selected.

Status: **REFERENCE / EXTERNAL TEACHER**

Do not assume all Cosmos components share identical licences or hardware requirements.

---

## H. Obsidia Sources

The project must map against current Obsidia sources before implementing duplicate contracts.

### Main Obsidia / X108

- https://github.com/Eaubin08/obsidia-x108-proofs

Relevant areas to audit:

- OS Trad / IR / Reverse;
- Brody;
- MMonde;
- Native Memory;
- SENS / cognition structures;
- receipts / replay;
- KX108 authority boundaries.

### GPS / Physical Evidence

- https://github.com/Eaubin08/obsidia-gps-defense-

Relevant existing path:

```text
recorded/physical evidence
-> observation envelope
-> Physical Reality Gate
-> DomainState
-> governance evidence
-> receipt
```

### Jarvis

- https://github.com/Eaubin08/Jarvis-iron-obsidia-

Use later as a producer/consumer of common world observations.

### Monde / Pokémon

- https://github.com/Eaubin08/monde-obsidia

Use later as presentation/operational visibility layer.

### Historical AGI visual repo

- https://github.com/Eaubin08/agi-vison

Status: **HISTORICAL / SOURCE OF IDEAS ONLY** until audited.  
Do not use it as the new technical base.

---

## I. Secondary Discovery / Watch Sources

### Vision IA

Useful for quickly discovering newly released AI, robotics and world-model projects.

- YouTube channel: https://www.youtube.com/@VisionIA-FR

Status: **DISCOVERY SOURCE ONLY**

Workflow:

```text
Vision IA mentions a project
        |
        v
find official repo / paper
        |
        v
audit architecture
        |
        v
audit licence
        |
        v
audit hardware
        |
        v
TAKE / ADAPT / REFERENCE / R&D_ONLY / REJECT
```

The channel itself is never the technical authority for a dependency.

---

## J. Mandatory source record before installation

For each selected component, create an entry in the future external manifest:

```yaml
name:
role:
status:
official_repo:
official_project:
paper:
selected_commit:
selected_model:
weights_source:
weights_hash:
code_license:
model_license:
dataset_terms:
commercial_allowed:
defense_allowed:
output_training_allowed:
derivative_training_allowed:
hardware_target:
adapter_version:
audit_date:
notes:
```

This file is the discovery/source index. The manifest created during PC bring-up will freeze the exact versions actually installed.
