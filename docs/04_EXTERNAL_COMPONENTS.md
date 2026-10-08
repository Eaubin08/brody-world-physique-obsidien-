# 04 — External Open-Source Component Map

> **Image-first placement and branch-level status (2026-10-08):** [22_IMAGE_BRANCH_AND_DONOR_MAP.md](22_IMAGE_BRANCH_AND_DONOR_MAP.md). This is the original donor candidate inventory, **not** evidence of installations. First goal is to make I1 perception and G1 generation work separately, then IG2 closed-loop comparison; do **not** wait for full Dreaming. The current Jarvis Qwen-VL seam is an optional first visual describer, so MiniCPM-V is not a mandatory second vision LLM.

**Rule:** external components provide capabilities. They never define Obsidia's canonical ontology.

Licences and model terms must be re-verified at install time and recorded in the external manifest.

## Tier A — first practical candidates

### MiniCPM-V

Role: lightweight local visual/video understanding.

Use as:

```text
FAST_EYE
media -> observation candidates
```

Do not use its natural-language answer as canonical truth.

Expected integration: adapter -> VisualIR candidate.

Official project: https://github.com/OpenBMB/MiniCPM-V

### MobileSAM

Role: lightweight image segmentation.

Use for:

- object masks;
- regions;
- geometry support;
- reverse validation.

Official project: https://github.com/ChaoningZhang/MobileSAM

### EfficientTAM

Role: efficient segmentation/tracking for image/video.

Use for:

- object continuity;
- track IDs;
- temporal identity;
- Invariant Dynamic experiments.

Official project: https://github.com/yformer/EfficientTAM

### Depth Anything 3

Role: depth and geometric candidate extraction.

Use for:

- relative depth;
- multiview geometry;
- spatial constraints;
- Reverse360 support.

Official project: https://github.com/ByteDance-Seed/Depth-Anything-3

### Grounding DINO

Role: open-vocabulary object grounding/detection.

Use for:

```text
concept -> candidate bounding region -> segmentation
```

Official project: https://github.com/IDEA-Research/GroundingDINO

## Tier A — transition and world dynamics

### EB-JEPA

Role: lightweight laboratory for representation prediction and action-conditioned world modeling.

Its AC Video JEPA example learns future representations from current observation + action and includes planning.

Use as:

- conceptual reference;
- testbed for Transition contracts;
- first action-conditioned latent prediction experiment.

Official project: https://github.com/facebookresearch/eb_jepa

### TD-MPC2

Role: compact learned dynamics + planning/control.

Important for this project because published model sizes include 1M and 5M parameter configurations.

Use as:

- evidence that useful transition models can stay small;
- donor architecture for state/action/future experiments;
- benchmark against our explicit MMonde representation.

Official project: https://github.com/nicklashansen/tdmpc2

### DreamerV3

Role: reference architecture for learning a world model from experience and improving behavior through imagined trajectories.

Use as REFERENCE first, not as a drop-in Obsidia architecture.

### Dream-RSI

Role: reference for improvement through replay/strategy evolution without immediate modification of base model weights.

Use as conceptual donor for:

```text
history -> replay -> strategy candidates -> evaluate -> retain best
```

Full implementation status must be rechecked before adoption.

## Tier A — generation on modest hardware

### stable-diffusion.cpp

Role: minimal local inference runtime.

Current upstream supports multiple model families including FLUX, Z-Image, Qwen Image, MiniT2I and video families.

Use as:

```text
GeneratorAdapter -> local runtime
```

Official project: https://github.com/leejet/stable-diffusion.cpp

### Z-Image

Role: efficient image generation candidate.

Use as the first practical local generator if hardware tests confirm acceptable latency and memory.

Official project: https://github.com/Tongyi-MAI/Z-Image

### SANA

Role: efficient NVIDIA-origin image generation architecture.

Use as:

- local generator candidate;
- efficiency benchmark.

Official project: https://github.com/NVlabs/Sana

### MiniT2I

Role: small, understandable image-generation laboratory.

Use for:

- studying how a generator learns;
- controlled fine-tuning experiments;
- later Brody-native generation research.

It is not necessarily the best quality generator; its value is architectural simplicity.

stable-diffusion.cpp currently includes MiniT2I support.

## Tier B — workflow and multi-engine laboratory

### ComfyUI

Role: visual/workflow execution bus.

Use for:

- model comparison;
- reproducible workflows;
- exact workflow/seed/parameter receipts;
- image and video experiments.

Brody should call a bounded adapter, not manipulate arbitrary nodes without contract validation.

Official project: https://github.com/Comfy-Org/ComfyUI

## Tier B — spatial / Reverse360

### WorldFM

Role: generate views from a reference image and target camera poses.

Use for:

- viewpoint consistency;
- identity persistence;
- Reverse360 experiments;
- testing whether representation survives camera movement.

Official project: https://github.com/inspatio/worldfm

Important: code may be Apache-2.0 while dependencies/submodules have separate licences. Verify every dependency before production/defense use.

### InSpatio World

Role: persistent spatial/world generation research.

Use later for:

- 3D/4D continuity;
- state-anchored world experiments;
- spatial persistence.

Not required for V0.

## Tier B — embodied skill benchmark

### SmolVLA / LeRobot

Role: small vision-language-action benchmark.

SmolVLA receives multiple camera views, sensorimotor state and instruction, then predicts action chunks.

Use to study:

- compact embodied know-how;
- action representation;
- asynchronous perception/action separation.

Official project: https://github.com/huggingface/lerobot

## Tier C — references, teachers, or research-only

Examples:

- V-JEPA / V-JEPA-AC;
- NVIDIA Cosmos;
- Qwen multimodal plugins;
- large Qwen image models;
- Ming Image layer decomposition;
- HiDream unified pixel architectures;
- large video generators;
- large 3D world models.

These may teach architecture or provide external benchmarks without becoming local dependencies.

## Exclusion / caution bucket

Any component with:

- military/defense restrictions;
- non-commercial restrictions incompatible with the target;
- EU geographic restrictions;
- output-use restrictions incompatible with learning;
- unclear redistribution terms;

must be isolated under research-only status.

Never allow a research-only component to contaminate the GPS/Defense deliverable chain.

## External manifest

Every installed donor/model must eventually have:

```yaml
name:
upstream_repo:
upstream_commit:
model_id:
weights_hash:
code_license:
model_license:
commercial_allowed:
defense_allowed:
derivative_training_allowed:
output_training_allowed:
local_or_cloud:
hardware_requirement:
adapter_version:
installed_at:
notes:
```
