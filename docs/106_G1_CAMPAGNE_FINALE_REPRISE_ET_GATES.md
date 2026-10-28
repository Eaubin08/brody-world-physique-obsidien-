# 106 - G1 consolidation, restart replay and external-evidence gates

## Executed predecessor evidence (from PC)
At Git revision 0295870a79146f9e97225968eeaab4892958f6a9 the user ran a full 718/718 PASS regression, targeted consolidation 2/2 PASS, U5B-U8 3/3 PASS, and synthetic candidate-memory replay tests with position and visual MAE 0 for learned and retained cases; unknown dynamics was HOLD. This is a **historical verified PC baseline**, not a guarantee that new G1 code passes.

## G1 added: actual session restart without canonical writes
The new `session_restart_replay_v1` loads the JSON candidate memory produced by `consolidated_education_replay_v1`, validates its seal and KX108_ONLY constraints, and runs completely new synthetic held-out episodes with distinct seeds. Its output is a different evidence directory and the predecessor memory's bytes must remain unchanged. Three tests cover replay, tampering, and evidence preservation. This establishes reload/replay across processes, NOT multi-day retention, world knowledge, or human-like lifelong learning.

## Unified one-command experiment for Windows PowerShell 5.1
From repository root:
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/RUN_BRODY_G1_FINAL_CAMPAIGN.ps1 -Out "build/BRODY_G1_FINAL_01"
```
This executes the new session tests, the complete historical regression runner, all its consolidation and multiview scenarios, then launches a **new Python process** to reload the previous candidate state and run unseen cases. It writes `MASTER_FREEZE_VERDICT.json` plus nested logs, refusing existing output paths. The script checks Python exit codes; normal unittest stderr is not a failure.

## Independent real video gate - user operation
The existing `video_observation_v0` has a real four-frame human annotation UI and precommits the prediction before fourth-frame annotation:
```powershell
py -m brody_world_physique.video_observation_v0 --video "C:\\path\\independent_video.mp4" --out "build/BRODY_REAL_VIDEO_EXAM_01" --source-kind OBSERVED_CLAIM
```
This needs an existing video and OpenCV in the Python environment. This is not included in headless batch automation because selecting the same object in four frames requires user interaction. It does not prove sensor authenticity, exact object identity, causation, or physics understanding. Never replace missing user video with simulator imagery while claiming real transfer.

## Independent multiview / Reverse 360 gate
Two distinct calibrated/independently captured viewpoints and external object correspondence are a starting condition. Source hashes and camera parameters must be recorded; training and test viewpoints must be separated; an unexpected viewpoint must be generated and compared with an independent observed target. The existing `image_multiview_identity_school_v0` applies mirror and 90/180-degree rotations of the same pixels and cannot fulfill this. The U7B tracker's `identity_proven=0` remains binding. Do not claim reverse 360 or persistent semantic identity.

## SENS/MMonde gate
The verified external GitHub tree of `Eaubin08/obsidia-x108-proofs` at `48f0c2fbcfe097c213b2783bc7b4d0fba78e6621` has a conceptual MMonde guide; the specific Mmonde_FORMAL_SPEC.md checked was a placeholder. See `docs/104_U6_UPSTREAM_SOURCE_AUDIT.md`. Do not invent upstream runtime class definitions. The contract must be sourced from the actual owner branch with commit SHAs, then adapted read-only, fail-closed and tested. No imported code is silently promoted to kernel authority.

## Research requirements held open
Visual/perceptual reciprocity; learning by interacting and comparing predictions with observations; collective symbolic, geometric and chronological knowledge; multi-hypothesis world models; active probing and curriculum; symmetry/multiscale connections and Reverse 360. These directions are not reduced to a color grid, and should not be described as already solved by the synthetic scalar experiments.

## Freeze states
- LOCAL_SYNTHETIC_GREEN can be declared after user PC confirms G1 full regression and restart replay.
- INDEPENDENT_VIDEO_GREEN only after real four-frame annotations from independently sourced video, source attribution and sealed evaluation.
- MULTICAMERA_IDENTITY_GREEN only after actual independent views, independent identity evidence and novel-view grade.
- UPSTREAM_INTERFACE_GREEN only after source-anchored real SENS/MMonde contract tests.
- GENERAL_WORLD_MODEL_PROVEN is NOT established by any of the above tests alone.

No automatic Native Memory write; no canonical promotion; KX108_ONLY.
