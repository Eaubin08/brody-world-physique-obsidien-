# E4 + E5 — grouped empirical school

E4 reuses P159 to learn experimental response patterns from pixels, chooses interventions by information gain minus cost before observing their results, and grades familiar, novel, and no-probe scenarios. P158 supplies a separate prior identifiability gate. A proposed probe is a synthetic experiment, never a real-world act.

E5 executes P156 historical cumulative curriculum with independent lesson, feedback, validation/replay and final exam streams. Checkpoint results are stored separately. E5 is not yet the same experimental shape memory as E1, and the E4 policy does not yet drive the E2/E3 future-image renderer. Do not claim end-to-end cognitive integration.

## Windows
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_e4_e5_active_cumulative_school_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.e4_e5_active_cumulative_school_v1 --out "build/e4-e5-active-cumulative-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/e4-e5-active-cumulative-v1/MASTER_REPORT.json"
```

## Remaining
E6 independent images/videos with provenance; E7 source-backed SENS/MMonde/OS translation read-only contract audit. After E7: genuine *single* shared school E1-E5, then new-scene generalization and Reverse360 tests.

Decision authority KX108_ONLY. No Native Memory writes or canonical promotion.
