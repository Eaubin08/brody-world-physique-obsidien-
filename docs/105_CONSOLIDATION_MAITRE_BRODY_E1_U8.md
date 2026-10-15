# 105 — BRODY : CONSOLIDATION MAITRE E1-E8 / U1-U8

Date: 2026-10-15. Status: CODE PUBLISHED, FULL PC REGRESSION PENDING.

## Central vision: perceptual and generative reciprocity

Brody aims to learn visual and physical regularities through accumulating experiences: perceive an object; extract structure; predict change; generate a representation; compare later observation; locate error; propose experiment; update candidate memory; replay learned competencies. This is education through friction and discrepancy rather than treating a very large image dataset as sufficient proof of understanding.

The author's conceptual directions retained in scope: perception ↔ generation, human-like experiential curriculum, reverse and 360 views, structural symmetry, multiscale micro/macro, chronological cumulative memory, symbolic inferences, multiple simultaneous hypotheses, active probing, World Foundry as school and laboratory. The ideas are *requirements and research concepts*, not claims of proven implementations. This file does not replace the historical concept atlas and original author material.

## Historical results ALREADY reported from user's machine

P0-P5: 695 historical unit tests + 3 integrated tests PASS. E1 shape retention and transfer pass; unknown triangle DOUBT. E2-E3 2 regular synthetic future images exact, surprise reversal worse than static. E4 five simulated probe cases, known SELECT, novel HOLD. E5 24/24 curriculum cycles, 9 corrections accepted/15 rejected, 480 exams; initial mean error 0.85925, ungated 1.60331, gated 0.57291. E6 no independent images, HOLD. E7 only local contracts. E8 evidence link not shared model. U1/U2 experiment changes candidate acceleration, new estimate improves error 1→0 while clean stays 0. U3/U4 pixel-derived context drives forecast and raster (2 exact, novel HOLD). U5/U7 six scenario families with multiple hypotheses where identity is ambiguous; identity proven=0. U5B-U8 batch 5/5 tests passed and synthetic shared shape/motion state generated 2 exact future images, unknown HOLD.

**Do not confuse above historical runs with current full repository regression**. The NEW campaign will save its own result after actually running the tests.

## New consolidation files

- `brody_world_physique/consolidated_education_replay_v1.py`: new candidate-only offline memory with shape and clean/intervention dynamics, P155 retention gate, independently seeded heldout predicted images, precommit receipts; rejects novel regime. The memory is a *joint state* not a pretrained unified model or multi-day memory.
- `tests/test_consolidated_education_replay_v1.py`: positive learning, retained clean and unknown HOLD, no-overwrite guard.
- `scripts/RUN_BRODY_FULL_CONSOLIDATION.ps1`: full test discovery, targeted tests, multiview campaign, report with Git HEAD and immutable output. Tests failing create an explicit CAMPAIGN_FAILURE.json.

### Windows — one command for whole consolidation

Run in the repo:
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "GIT_PULL_FAILED" }
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/RUN_BRODY_FULL_CONSOLIDATION.ps1
```
Output: `build/BRODY_CONSOLIDATION_20261015/MASTER_REGRESSION_REPORT.json`, `REPLAY/MASTER_REPORT.json`, `MULTIVIEW/MASTER_REPORT.json`, `TEST_ALL.log`.

Never reuse an existing output path: pass `-Out "build/BRODY_CONSOLIDATION_02"` for another run.

### Optional external video (separate exam)

Actual video is still missing in this project. To create a legitimate human-annotated held-out prediction, use the existing procedure separately:
```powershell
py -m brody_world_physique.video_observation_v0 --video "C:\path\external.mp4" --out "build/video_independent_01" --source-kind OBSERVED_CLAIM
```
This opens an OpenCV UI (requires cv2 installed): human clicks 3 positions, prediction is saved **before** fourth frame is annotated, then scored. `OBSERVED_CLAIM` does not authenticate a sensor, object identity or the claim that it is genuine real-world footage. Never present the source as real/authenticated just because it is a file.

## Camera, identity, reverse 360 — evidence thresholds

1. `2D_TRANSFORM`: mirror/quarter-turn/half-turn of one image. Tests known context only.
2. `MULTI_FRAME_TRACK`: infer paths from temporal pixels; multiple hypotheses at occlusion/crossing.
3. `INDEPENDENT_VIEW`: source 2+ independently captured perspectives with camera metadata, external identity check and heldout target.
4. `REVERSE_360`: many-angle novel-view generation, consistency against independent views, geometry/camera separation, no 2D rotation shortcut.

Only levels 1 and bounded level 2 have actual lab support. Neither semantic identity nor 3D real Reverse360 is proven.

## SENS/MMonde independent GitHub audit

`Eaubin08/obsidia-x108-proofs` Git tree `48f0c2fbcfe097c213b2783bc7b4d0fba78e6621`, original MMonde guide `docs/couches/03_COSMOS_MMONDE_WORLD.md` indexed as conceptual; examined `Mmonde_FORMAL_SPEC.md` contained only placeholder. These sources alone do NOT establish runtime type ownership or entrypoints. Do not import guessed upstream types, silently duplicate them or grant Brody action authority. See `docs/104_U6_UPSTREAM_SOURCE_AUDIT.md`.

## Constitution and invariants

`KX108_ONLY`: Brody observes, learns and proposes. No authority to decide/act. No canonical promotion. `native_memory_write=false`. Histories are candidate receipts. Unknown or contradictory evidence leads to explicit HOLD/MULTI. An evaluation result never becomes sensor authentication or scientific proof by label.

## Remaining blockers after this consolidation

- independent external photo/video, annotation and provenance assessment
- real multi-camera calibrated views and independently attested persistent identity
- long duration staged curriculum, cross-session replay, forgetting and adversarial transfer
- exact upstream active SENS/MMonde contracts in current branches and safely gated readonly adapter
- end-to-end physical ↔ image ↔ symbolic skill curriculum with stable candidate memory and non-circular examination
- global regression GREEN with true local PC logs; any red must be fixed and rerun before freeze.

## Freeze rule

Technical GREEN only after complete regression passes on PC. Research status remains BOUNDED/SYNTHETIC. Do not claim autonomous general intelligence, learned real physics, source-authenticated imagery, Reverse360 or canonical decision authority until independent corresponding proofs exist.
