# 08 — Licence, Provenance and Boundary Policy

## 1. Why this is architectural

This project may later feed:

- commercial products;
- safety-sensitive systems;
- GPS / Defense / Aviation.

Therefore model and code licences are not administrative metadata. They are execution constraints.

## 2. External component statuses

Allowed statuses:

```text
TAKE
ADAPT
REFERENCE
R&D_ONLY
REJECT
UNKNOWN
```

A component cannot become TAKE while licence status is UNKNOWN.

## 3. Separate code licence from model licence

For every donor, track independently:

- source-code licence;
- pretrained-weight licence;
- dataset terms;
- model-output terms;
- commercial-use permissions;
- geographic restrictions;
- defense/military restrictions;
- derivative-training restrictions;
- redistribution restrictions.

## 4. Defense contamination rule

Any component whose licence forbids or ambiguously restricts defense/military use must never be placed on the GPS/Defense production or demonstration path.

A research-only experiment must retain enough provenance to prove that its output, weights or derived training data did not contaminate the restricted chain.

## 5. Required receipt for generated media

At minimum:

```text
artifact hash
model name
model version
weights hash
adapter version
workflow hash
seed
generation parameters
source inputs
licence snapshot/ref
timestamp
```

## 6. Required receipt for observations

```text
source
sensor/model
version
input hash
observed_at
received_at
processed_at
reference frame
uncertainty
transform chain
```

## 7. Re-verification

External repositories change.

Before installation or release:

1. re-open upstream licence;
2. record exact commit/model version;
3. hash installed weights;
4. snapshot licence metadata in the manifest;
5. classify intended use.

## 8. No hidden dependency

A permissively licensed top-level project can depend on non-permissive models or submodules.

Example class:

```text
WorldFM code licence
!=
licence of every WorldFM dependency/submodule
```

The whole dependency path must be audited.
