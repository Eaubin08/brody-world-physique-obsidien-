# 06 — Forge Plan F0 -> F10

## F0 — Contract and source audit

**No model installation.**

Audit current:

- SENS / Cognition;
- MMonde;
- Native Memory;
- OS Trad / IR / Reverse;
- Brody;
- GPS evidence pipeline.

Deliver:

- mapping from proposed contracts to existing structures;
- duplicate/conflict report;
- names to keep;
- names to reject;
- minimum contract freeze.

Exit criteria:

- no parallel event ontology;
- observed/predicted/simulated are distinguishable;
- provenance survives;
- KX108 boundary unchanged.

## F1 — First visual perception

Candidate stack:

- MiniCPM-V;
- MobileSAM;
- Depth Anything 3.

Input:

- one static image.

Output:

- MediaObservation;
- VisualIR candidate;
- provenance;
- unknowns.

No generation.

Exit criteria:

- deterministic schema validation;
- source attribution;
- object/region/depth candidates represented separately;
- failure is explicit.

## F2 — Object identity through time

Add:

- Grounding DINO;
- EfficientTAM.

Input:

- short videos;
- multiple views.

Goal:

- ObjectCandidate;
- ObjectTrack;
- temporal identity;
- VisualFingerprint;
- first VisualInvariant.

Exit criteria:

- same object can persist across multiple frames;
- uncertainty on identity is representable;
- disappearance/occlusion is not automatically treated as deletion.

## F3 — Transition learning

Laboratory:

- EB-JEPA;
- TD-MPC2;
- simple deterministic synthetic environments.

Goal:

```text
State(t) + Action -> PredictedState(t+1)
```

Start with tiny controlled tasks:

- object translates;
- object falls;
- camera moves;
- object is occluded;
- object changes allowed property;
- impossible transformation.

Exit criteria:

- predicted and observed states remain separate;
- delta is measurable;
- transition model source is recorded;
- small-model baseline exists.

## F4 — Native Memory experience loop

Connect validated contract to Native Memory boundary.

Goal:

```text
episode -> ExperienceCandidate -> validation -> reusable context
```

Exit criteria:

- no automatic canonical promotion;
- replay can reconstruct source episode;
- failure pattern can be retrieved without becoming a global rule.

## F5 — Replay / dreaming

Reference ideas:

- DreamerV3;
- Dream-RSI.

Implement Obsidia-native distinction:

- recorded replay;
- simulation;
- counterfactual candidate.

Exit criteria:

- imagined state cannot masquerade as observed state;
- strategy candidates can be compared;
- all simulations are receipted.

## F6 — First functional local image generation

Start with:

- stable-diffusion.cpp;
- Z-Image candidate.

Optional after hardware measurement:

- SANA;
- FLUX Klein.

Implement:

- GenerationIntent;
- GeneratorAdapter;
- GeneratedArtifact;
- model/workflow/seed receipts.

Exit criteria:

- reproducible generation;
- no generator-specific fields leak into canonical contracts;
- adapter can be replaced.

## F7 — Analysis <-> synthesis loop

Generated output returns through F1/F2 perception.

Goal:

```text
intent -> generation -> re-perception -> comparison -> correction
```

Implement:

- LOCK;
- FLEX;
- IGNORE invariants.

Exit criteria:

- identity-critical and style-flexible properties can be separated;
- violations are machine-readable;
- Brody can propose a revised generation plan.

## F8 — Reverse360 / viewpoint persistence

Candidate:

- WorldFM;
- later InSpatio.

Tests:

- front -> side;
- side -> rear;
- controlled camera rotations;
- room/scene viewpoint changes.

Exit criteria:

- geometry/identity consistency metrics;
- occlusion awareness;
- impossible view contradictions exposed.

## F9 — Video / Invariant Dynamic

Add efficient tracking and a video generator only when required.

Goal:

- preserve world identity over time;
- compare legitimate motion with generative drift.

Exit criteria:

- object track continuity;
- temporal invariants;
- frame-time provenance;
- action/transition links.

## F10 — Cross-domain integration

Only after common contracts are stable.

Adapters:

### GPS / Defense
GNSS/RF/camera/inertial observations -> WorldState candidates.

### Jarvis
screen/camera/activity -> state/action/consequence loop.

### Monde / Pokémon
visualize the live contracts and experiment state.

### Brody
consume the common world/experience layer.

Exit criteria:

- same transition grammar works across at least two materially different domains;
- no domain-specific shortcut enters the kernel;
- KX108_ONLY preserved.
