# 14 — F0 Learning-Loop Contracts Implementation V0

**Branch:** `f0/learning-loop-contracts-v0`  
**Base:** `f0/cross-audit-contract-freeze-v0`

## Scope

Implemented only the four missing contracts isolated by F0:

- `WorldTransformationV0`
- `WorldStateProjectionV0`
- `WorldStateDeltaV0`
- `WorldExperienceCandidateV0`

No external model, runtime, weight or PC dependency was added.

## Dependency policy

The package deliberately does not copy/import the upstream MMonde implementation.

Instead it accepts upstream objects structurally:

- transformation time must expose `observed_at`;
- spatial frame, when supplied, must expose `frame_ref`;
- projected world state must expose `world_state_id`.

This allows the repository to be tested alone while preserving ownership of canonical Obsidia contracts in `obsidia-x108-proofs`.

## Boundaries encoded

All four contracts reject attempts to:

- change decision authority away from `KX108_ONLY`;
- gain decision authority;
- gain action authority;
- mutate the kernel;
- become mutable.

Additional boundaries:

### WorldTransformationV0

- descriptive transformation only;
- never WorldAction execution authority;
- supports OBSERVED / PROPOSED / SIMULATED / INFERRED / UNKNOWN.

### WorldStateProjectionV0

Only:

- PREDICTED;
- SIMULATED;
- COUNTERFACTUAL.

There is deliberately no OBSERVED projection kind.

### WorldStateDeltaV0

- requires a projected or baseline comparison anchor;
- records discrepancy;
- cannot claim causal proof.

### WorldExperienceCandidateV0

- not canonical memory;
- `memory_write_allowed=false`;
- `auto_promotion_allowed=false`;
- repeat count >= 1;
- uses explicit memory eligibility instead of promotion.

## Tests

Stdlib-only `unittest` suite covers:

- normal construction;
- upstream shape compatibility;
- prediction != observation;
- proposed transformation != WorldAction;
- delta != causal proof;
- validated experience != canonical memory;
- KX108_ONLY invariants;
- no ACT;
- no decision;
- no kernel mutation;
- readonly requirement;
- no memory write;
- no auto-promotion.

GitHub Actions runs the suite on Python 3.11 and 3.12.

## Deliberately not implemented

- `TransitionTransformationBindingV0`: still an architecture decision.
- upstream modification of `TransitionV0`;
- experience -> Native Memory adapter;
- VisualInvariant / VisualFingerprint;
- perception models;
- image generation.

Those remain later gates.
