# 01 — Target Architecture

## 1. General pipeline

```text
RAW SOURCE
 image / video / GNSS / RF / inertial / screen / simulator
        |
        v
SourceObservation
 provenance + time + frame + source + uncertainty
        |
        v
OS / modality translator
        |
        v
Structured Observation Candidate
        |
        +---------------------+
        |                     |
        v                     v
Perception adapters      Domain adapters
        |                     |
        +----------+----------+
                   v
                 MMonde
                   |
                   v
              WorldState(t)
                   |
            Action / Transform
                   |
                   v
           Transition Layer
                   |
                   v
         PredictedState(t+1)
                   |
                   +--------- ObservedState(t+1)
                                 |
                                 v
                              StateDelta
                                 |
                                 v
                      ExperienceCandidate
                                 |
             +-------------------+-------------------+
             |                   |                   |
          Replay               Memory              Skill
             |                   |                   |
             +-------------------+-------------------+
                                 |
                                 v
                               Brody
```

## 2. Visual specialization

```text
image / video / camera / multiview
          |
          v
MediaObservation
          |
          v
Visual Translator
          |
          v
VisualIR
  - objects
  - tracks
  - masks
  - spatial relations
  - depth candidates
  - camera/reference frame
  - motion
  - lighting candidate
  - provenance
  - uncertainty
          |
          v
MMonde
          |
          v
VisualInvariant
 LOCK / FLEX / IGNORE
          |
          v
Brody
          |
          v
GenerationIntent
          |
          v
GeneratorAdapter
          |
          v
GeneratedArtifact
          |
          v
RE-PERCEPTION
          |
          v
VisualIR'
          |
          v
Invariant / State comparison
          |
          v
ReverseEvaluation
          |
          v
ExperienceCandidate
```

## 3. Reverse360

Reverse360 is not defined as “generate a 360 image”.

Its working role is to test whether a representation survives viewpoint and transformation changes.

```text
view A
  -> VisualIR A
  -> infer stable structure
  -> request view B / C / D
  -> regenerate or obtain new views
  -> re-perceive
  -> compare identities / proportions / relations
  -> detect contradictions
```

Questions include:

- Is the same object still the same object?
- Do dimensions and proportions remain compatible?
- Are occlusions plausible?
- Do relations survive viewpoint changes?
- Did the generator invent or delete structure?
- Is the difference explained by viewpoint, time, action, uncertainty or model error?

## 4. Dynamic world model

Video is not treated as independent frames.

```text
State(t0)
 -> transformation
State(t1)
 -> transformation
State(t2)
...
```

The system tracks a stable identity and changing state.

The target is an **Invariant Dynamic**: the stable structure that persists through legitimate change.

## 5. Multiple hypotheses

MMonde must be able to retain competing candidates.

Example:

```text
Observation:
  object moved 30 cm

Hypothesis A:
  object was pushed

Hypothesis B:
  camera moved

Hypothesis C:
  depth estimate drifted

Hypothesis D:
  source timestamp mismatch
```

Until evidence discriminates between them, uncertainty must remain explicit.

## 6. No authority collapse

This project must never collapse:

```text
perception == truth
prediction == decision
generation == reality
memory == authority
Brody == KX108
```

Those equivalences are forbidden architectural shortcuts.
