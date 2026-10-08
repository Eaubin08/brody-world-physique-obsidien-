# 05 — Learning and Memory Loop

## 1. Principle

The system should improve primarily through structured experience before modifying model weights.

```text
DO
 -> OBSERVE
 -> COMPARE
 -> EXPLAIN
 -> STORE CANDIDATE
 -> REPLAY
 -> GENERALIZE
 -> TEST
 -> VALIDATE
```

## 2. Experience lifecycle

### Step A — Context

Record the state before an action.

### Step B — Prediction

If the system has enough prior structure, generate an expected next state.

Prediction may come from:

- deterministic rule;
- learned transition model;
- previous experience;
- domain model;
- Brody hypothesis.

The source must be explicit.

### Step C — Action / Transformation

Action may be:

- external observed action;
- human action;
- Brody proposal;
- simulated action;
- physical transformation not caused by an agent.

### Step D — Observation

Capture the resulting state with source/time/provenance.

### Step E — Delta

Compare expected vs observed.

Classify:

- expected match;
- expected but quantitatively wrong;
- unexpected event;
- source contradiction;
- unknown;
- model failure;
- representation failure;
- timing/reference-frame failure.

### Step F — ExperienceCandidate

Create a candidate, not a permanent truth.

### Step G — Validation

Evidence for promotion can include:

- repeated occurrence;
- cross-source consistency;
- deterministic check;
- formal/domain rule;
- human validation;
- successful replay;
- controlled experiment.

## 3. Memory classes

The exact Native Memory schema is external to this repo and must be audited, but this project needs at least conceptual separation between:

### Episodic history

What happened in a specific episode.

### Stable invariant

What survived multiple valid transformations.

### Skill

A reusable procedure for obtaining a result.

### Failure pattern

A known route, condition or tool configuration that tends to fail.

### Source reliability evidence

How a source performed under known conditions.

### Open hypothesis

Useful but not yet proven.

## 4. Replay

Replay is critical because the system should not need to re-enter the physical world for every alternative.

```text
validated episode
 -> reconstruct state
 -> replay candidate strategy
 -> estimate outcome
 -> compare alternatives
 -> select candidate for real test
```

Replay must distinguish:

- exact replay from recorded evidence;
- simulation;
- counterfactual prediction.

Those are not equivalent evidence classes.

## 5. Dreaming / internal simulation

Dreamer-like and Dream-RSI-like mechanisms are references for this layer.

Obsidia version must preserve:

- provenance;
- uncertainty;
- distinction between imagined and observed;
- bounded authority;
- receipts.

## 6. Skill before weight update

Preferred hierarchy:

```text
1. Better route
2. Better tool selection
3. Better prompt/plan
4. Better deterministic transform
5. Better memory retrieval
6. Better reusable skill
7. Small adapter / LoRA
8. Distillation / fine-tuning
9. Base model mutation only with strong justification
```

This avoids treating every mistake as a training problem.

## 7. Learning from image generation

Example:

```text
Intent:
 preserve identity, change lighting

Generator:
 Z-Image adapter

Result:
 identity partially drifted

Reverse perception:
 face geometry mismatch

Experience:
 this model/configuration is weak for this identity-lock task

Later:
 route identity-critical tasks elsewhere
 or strengthen constraints
 or collect a validated adapter dataset
```

The useful memory is not merely the generated image. It is the **validated relationship between context, method and outcome**.
