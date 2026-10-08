# 07 — Validation and Test Strategy

## Test philosophy

We do not test whether a model gives a convincing answer.

We test whether the whole system preserves:

- identity;
- state;
- time;
- provenance;
- uncertainty;
- separation of evidence classes;
- replayability;
- authority boundaries.

## Test levels

### T0 — Schema

Every contract:

- validates;
- rejects invalid states;
- distinguishes required/optional fields;
- has versioning.

### T1 — Deterministic fixtures

Synthetic scenes with known answers.

Examples:

- two objects at known coordinates;
- known camera move;
- known object translation;
- known occlusion;
- known depth order.

Purpose: detect representation errors before model-quality errors.

### T2 — Model adapter

Each external adapter receives the same fixture.

Measure:

- latency;
- memory use;
- output stability;
- unsupported cases;
- confidence/unknown behavior.

### T3 — Multi-model contradiction

Example:

```text
MiniCPM says object A is behind B
Depth model says A is in front
tracking model lost A
```

Expected system behavior:

- preserve contradiction;
- do not silently merge;
- do not fabricate consensus.

### T4 — Transition prediction

For each episode:

```text
state_before
action
predicted_state
observed_state
delta
```

Metrics depend on domain:

- position error;
- identity preservation;
- relation error;
- temporal error;
- categorical outcome;
- unknown rate.

### T5 — Memory / replay

Tests:

- exact episode retrieval;
- same receipt reproduces same deterministic transform;
- imagined state is marked imagined;
- rejected experience cannot silently become invariant.

### T6 — Generation

Record:

- model;
- model version;
- weights hash;
- seed;
- workflow;
- intent;
- invariants.

Then re-perceive the artifact.

### T7 — Reverse360

Measure:

- identity consistency;
- geometry consistency;
- relation consistency;
- object count;
- occlusion plausibility;
- hallucinated structure.

### T8 — Authority

Negative tests:

- perception model attempts ACT;
- generator emits an action request;
- memory candidate attempts canonical promotion;
- Brody attempts kernel mutation.

Expected result: blocked by architecture.

## Minimum benchmark scenarios

1. Static tabletop scene.
2. Same object from four viewpoints.
3. Object moved by a known translation.
4. Object dropped.
5. Camera moved while object stays still.
6. Temporary occlusion.
7. Image generation with identity LOCK.
8. Image generation with style FLEX.
9. Deliberately contradictory sensors.
10. Missing timestamp / stale observation.
11. Replay of a previously validated episode.
12. Counterfactual that must remain non-observed.

## Result classification

Every milestone result should be classified:

- PASS;
- PARTIAL;
- BLOCKED;
- UNKNOWN;
- UNSUPPORTED;
- INVALID_TEST.

No “looks good” acceptance criterion.
