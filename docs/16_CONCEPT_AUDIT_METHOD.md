# 16 — Méthode obligatoire d'audit des concepts Obsidia

**Status:** AUDIT METHOD V0  
**Purpose:** ensure user-origin concepts are explained, not merely detected.

---

## 1. Principle

An Obsidia source audit must answer two different questions:

1. **What does the source say?**
2. **What does the concept mean inside Obsidia today?**

A keyword hit is not a definition.

A current implementation is not automatically the original idea.

An old idea is not automatically obsolete because its name disappeared.

---

## 2. Required record for every concept

Use this structure:

~~~text
CONCEPT NAME

1. ORIGINAL DEFINITION
   What the user/source meant at that date.

2. PROBLEM IT WAS TRYING TO SOLVE
   Why the concept appeared.

3. MECHANISM
   How it was supposed to work.

4. INPUTS / OUTPUTS
   When meaningful.

5. WHAT IT IS NOT
   Neighboring concepts it must not be confused with.

6. RELATIONS
   What it connects to in the architecture.

7. AUTHORITY BOUNDARY
   Can it observe, infer, propose, write memory, decide, act?

8. GENEALOGY
   Older names / later names / changed meanings.

9. CURRENT DESCENDANT
   Current code, contract, organ or doctrine that carries the idea.

10. STATUS
    Historical / source pack / research / doc-only / code / tested / frozen / future.

11. SOURCE LINKS
    Original Drive document(s), current GitHub file(s), tests.

12. DRIFT / CONFLICT
    What changed or contradicts another source.

13. OPEN QUESTION
    What remains undefined or needs a decision.
~~~

---

## 3. Status vocabulary

Use explicit statuses.

### Historical

Idea belongs to an older stage and is not current runtime canon.

### Historical but survived

Original component disappeared, but its principle lives in a current mechanism.

### Source pack

Preserved material useful for recovery, not direct runtime authority.

### Research source

Experimental branch or concept suitable for selective porting.

### DOC_ONLY

Specified but not implemented.

### PARTIAL

Some mechanism exists, but not the complete claimed concept.

### CODE_PRESENT

Code exists; runtime connection is not yet proven.

### RUNTIME_CONNECTED

Actually called on a live/runtime path.

### TESTED

Behavior has direct test evidence.

### VERIFIED / FROZEN

Accepted current architecture with evidence/freeze.

### FUTURE / VISION

Explicit target, not current reality.

### NAME_COLLISION

The same name refers to materially different concepts in different eras.

### UNDEFINED / SOURCE_RECOVERY_REQUIRED

Not enough source evidence to define safely.

---

## 4. Claim ladder

Never collapse these states:

~~~text
mentioned
!= defined
!= specified
!= implemented
!= connected
!= causally useful
!= tested
!= proven
!= frozen
!= production
~~~

The audit must say exactly where the concept is on this ladder.

---

## 5. Genealogy rule

When names change, preserve the line.

Example:

~~~text
historical Multimodalité Harmonique
    ↓ surviving intent
ModalityObservationV0
    +
MMonde bounded multimodal bridge
~~~

Do not say the old concept is "implemented" simply because a descendant exists.

Correct wording:

> The original idea survives partially through X and Y; the historical formulation itself is not the current runtime contract.

---

## 6. Collision rule

When one name has several meanings, do not choose one silently.

Example:

~~~text
C10
├── historical Trace / Immutability block
└── current roadmap C10 Education / Oxygen
~~~

Classify as NAME_COLLISION until context disambiguates it.

Same rule applies to acronyms such as AVDR.

---

## 7. Historical acronym rule

Never reconstruct an acronym from memory when sources show multiple expansions.

For AVDR, audit:

~~~text
source/date
exact expansion or phase names
purpose
subsystem
current descendant
~~~

Do not rewrite historical AVDR documents to match the current Gencoin AVDR canon.

---

## 8. User concept vs generic AI term

If the user has a specific Obsidia meaning, that definition wins for the project audit.

Examples:

### Memory

Generic AI meaning: stored context/data.

Obsidia meaning: typed contextual/experience material without decision authority, with controlled promotion.

### World model

Generic AI meaning: often a predictive/generative neural model.

Obsidia meaning: may refer to a larger system of situated world state, transitions, transformations, evidence, prediction, delta, memory and specialized models.

### Education

Generic ML meaning: may be used loosely for training.

Obsidia meaning: long-term identity/context/genealogy development reserved for Oxygen in current doctrine.

---

## 9. Current-runtime priority rule

When historical source and current tested implementation conflict:

~~~text
current code + tests
>
current frozen/runtime docs
>
recent master support
>
older architecture docs
>
historical source packs
>
conversation reconstruction
~~~

But the historical source remains part of genealogy.

Runtime priority does not authorize rewriting history.

---

## 10. Required source links

Each concept entry should link, when available, to:

### User primary source

Google Drive original or master document.

### Current code

GitHub exact file path.

### Current test

GitHub test/report.

### External donor

Only when an external project materially contributed to the current concept.

---

## 11. Example — Veto Harmonique

### Original idea

A severe weak/blocking component should not disappear inside a favorable average.

### Historical mechanism

Harmonic aggregation + veto thresholds.

### Current descendant

sigma/contracts.py::calculate_immutable_vote() and readiness harmonic mean.

### Drift

Current function is readonly advisory and cannot override KX108. It is not identical to every historical threshold formula.

### Status

~~~text
HISTORICAL IDEA
+
CURRENT READONLY DESCENDANT
+
KX108_ONLY
~~~

---

## 12. Example — Continuum

### Original idea

Maintain structured chronological continuity through compact Input + State + Result summaries and a latent buffer.

### Current descendants

Parts are covered by:

- session/temporal context;
- receipts;
- memory candidates;
- replay;
- world experience candidates.

### Status

~~~text
HISTORICAL CONCEPT
PARTLY ABSORBED
NO SINGLE CURRENT CONTINUUM RUNTIME OBJECT REQUIRED
~~~

---

## 13. Example — World quadrillage

### Original idea

Make the world tractable by placing experience against stable coordinates/concepts:

- where;
- when;
- what;
- relation;
- transformation;
- consequence;
- source;
- uncertainty.

### Current descendants

- MMonde;
- world dynamics;
- measurement/evidence;
- Brody World Physique learning-loop contracts.

### Status

~~~text
FOUNDATIONAL USER IDEA
PARTLY MATERIALIZED
ACTIVE DESIGN PRINCIPLE
~~~

---

## 14. Output of a completed document audit

A completed audit should contain:

1. document identity/date;
2. concepts extracted;
3. definition cards;
4. genealogy map;
5. current-runtime mapping;
6. obsolete/dead concepts;
7. concepts that survived under another name;
8. conflicts/name collisions;
9. implementation gaps;
10. source links;
11. recommended actions;
12. atlas updates.

The audit is not complete until any new user-origin concept is added to:

docs/15_CONCEPT_ATLAS.md

or explicitly classified:

UNDEFINED / SOURCE_RECOVERY_REQUIRED.

---

## 15. Goal

The purpose is not only to know **what Obsidia contains**.

It is to preserve:

~~~text
why the idea appeared
what it meant
how it evolved
what survived
what became code
what remains only vision
~~~

This keeps the architecture connected to the user's actual reasoning trajectory rather than reducing it to a list of current files.
