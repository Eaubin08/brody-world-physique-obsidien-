# 101 — U3/U4 pixels to shared candidate prediction and raster

A P158 pixel-sequence intervention produces a measured acceleration. A single immutable candidate state holds this acceleration for both numerical forecast and generated future raster. The candidate is NOT canonical Native Memory.

Previously U1/U2 exam context was passed by fixture. U3 infers context from frame centroids and second differences; no exam regime labels reach routing. Clean trajectories retain zero acceleration; trained slope trajectories receive learned acceleration; novel spring dynamics trigger no image and HOLD.

P155 is used to test and reject the harmful global update. Each prediction and selected context is sealed before revealing target frame 7. Scores include position error and generated RGB image MAE.

## Run on Windows PowerShell
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_u3_u4_visual_context_shared_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.u3_u4_visual_context_shared_v1 --out "build/u3-u4-visual-context-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/u3-u4-visual-context-v1/MASTER_REPORT.json"
```

## What this does not show
Single scalar physical memory, synthetic pixels with a known rendering convention. Shape semantics, reverse 360, multi-object identity, real-world source verification, cross-repo SENS/MMonde runtime and cross-skill memory E1-E5 integration are not proven.

## Continued plan
U5: independent source videos and strict no-leak evaluation.
U6: upstream repository contracts audit, no canon replacement.
U7: 360 multi-view / occlusion identity invariants.
U8: actual single skill/motion/visual candidate memory and replay, with out-of-domain transfer.
