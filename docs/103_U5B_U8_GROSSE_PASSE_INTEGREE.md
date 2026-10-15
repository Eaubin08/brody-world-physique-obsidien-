# 103 - Large integrated delivery U5B/U6/U7B/U8

## Scope and actual working contracts
This delivery bundles earlier historical school modules into ONE executable campaign without inventing remote integrations.

U8 stores both learned structural shape (P134 image mask) and pixel-estimated intervention acceleration (P158/P157) in ONE noncanonical candidate memory. A held-out motion sequence selects its context from observed pixel positions, predicts frame seven using the stored acceleration, renders that frame from the stored mask, commits the prediction, and ONLY THEN exposes the held-out target for visual MAE scoring. Tests exercise learned intervention, retained clean regime, and unknown regime HOLD. This is a genuine shared local candidate **state** across visual generation and numerical dynamics, not shared LLM parameters or generic long-term skill transfer.

U7B runs the historical P165D12 six-family tracker on 18 synthetic camera/occlusion/crossing episodes (default 3 seeds). Separately, a teacher-assigned asymmetric image is transformed through the historical 2D multiview identity school: original and mirror lessons, quarter-turn and half-turn exams. Same-source transformed views are NOT truly independent physical camera angles. Identity is teacher-assigned, not established by a semantic learner. Therefore Reverse360 and 3D remain unproven.

U5B preserves optional video file name, size and SHA256. The existing manual annotation module video_observation_v0 can score future pixels on actual frames, but the batch **does not decode or score independent video without manual annotation**. This is an explicit HOLD, not a substitute for real data.

U6 confirms local candidate contract symbols only. Without fetching and examining the actual upstream SENS/MMonde repository code and version SHAs, it emits LOCAL_CONTRACTS_ONLY_NO_UPSTREAM_SOURCE_AUDIT. No cross-repo runtime connection is claimed.

## One PowerShell run
From the Brody repo:
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/RUN_BRODY_U5B_U8_BIG_BATCH.ps1
```
Runs 2 U8 tests, 3 integrated batch tests, and the full U5B-U8 synthetic campaign. Requires a fresh output directory; results stored at build/u5b-u8-big-batch-v1/MASTER_REPORT.json. Optional video, in a NEW output folder:
`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/RUN_BRODY_U5B_U8_BIG_BATCH.ps1 -Out build/u5b-u8-video-01 -Video "C:\\path\\video.mp4"`.

## Evidence to request before further progress
1. Independent video for user-led four-frame annotation, with immutable heldout future.
2. Multiple actual independent camera views of the same object with external identity attestation.
3. Upstream SENS and MMonde repository/path/commit references for authority-safe read-only adapter.
4. Cross-skill shared persistent training with replay across physical, visual and reasoning tasks; current shared state only joins a stored shape and scalar acceleration.
5. Broader multi-seed and adversarial evaluation; no claimed general physical understanding.

## Boundary verdict
KX108_ONLY; native_memory_write false; canonical_promotion false; no automatic external action.
