# 00 — Vision and Doctrine

## 1. What this project is solving

The project is not built around the question:

> How can an AI know every definition about the physical world?

The working question is:

> How can Brody observe a world, represent it, act or reason about an action, anticipate a consequence, compare prediction with reality, and become more competent from experience?

A child does not need a formal definition of gravity before learning that a released object tends to move downward. Operational competence can precede formal explanation.

For Obsidia, formal scientific knowledge remains useful when needed, but it is not the only substrate of physical competence.

## 2. Operational world understanding

The minimum reusable grammar is:

```text
WHERE?
WHEN?
WHAT?
RELATIVE TO WHAT?
WHAT CHANGED?
WHAT REMAINED INVARIANT?
WHAT ACTION OR TRANSFORMATION OCCURRED?
WHAT WAS EXPECTED?
WHAT WAS OBSERVED?
WHICH SOURCE SUPPORTS IT?
WITH WHAT UNCERTAINTY?
```

This grammar is modality-independent.

A camera, GNSS receiver, RF stream, inertial sensor, screen capture, generated image or simulator can all produce observations, but they do not carry the same kind of truth.

## 3. Learning target

The primary learned artefacts are:

- transition expectations;
- validated patterns;
- invariants;
- reusable skills;
- routing preferences;
- failure patterns;
- source reliability information;
- action-consequence experience.

The default learning order is:

```text
experience
  -> structured history
  -> replay
  -> compare strategies
  -> improve routing / skill / expectation
  -> validate in reality
  -> only later consider weight updates
```

## 4. Separation of powers

### External models

They may:

- detect;
- segment;
- estimate;
- generate;
- predict;
- propose.

They do not:

- establish canonical truth;
- authorize ACT;
- mutate X108;
- write canonical memory directly;
- silently merge incompatible evidence.

### Brody

Brody can:

- contextualize;
- compose;
- compare;
- propose;
- explain;
- choose an adapter according to bounded routing rules;
- create learning candidates.

Brody does not become the final decision authority.

### MMonde / SENS

They provide the structured language needed to situate observations, entities, events, relations, time, reference frames, transformations and uncertainty.

### Native Memory

Memory retains context and validated experience. It is not a hidden policy engine.

### X108 / KX108

Decision authority remains outside this project.

## 5. Why small models are valuable

The project explicitly allows a large capability to emerge from:

- small specialized models;
- explicit representations;
- structured memory;
- replay;
- tools;
- deterministic validation;
- routing;
- experience.

A 5M transition model can be more useful for a narrowly defined physical skill than a much larger encyclopedic model.

## 6. Visual cognition is the first laboratory, not the final scope

Image work is used because it gives a controlled first environment for testing:

- object identity;
- spatial relation;
- invariance;
- viewpoint change;
- temporal persistence;
- generation;
- reverse inspection;
- prediction vs observation.

The same contracts must later generalize to GPS, RF, Jarvis, robotics and other physical domains.
