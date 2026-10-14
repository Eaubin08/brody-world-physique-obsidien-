# 181 — P165-D10 Global regression gate and historical manifest correction

## Evidence from PC (previous stage)
147 files `tests/test*.py`, 649 AST-declared `test_*` functions/methods and zero syntax errors. Historical P161–P165-D: 41/41 PASS. D2–D9: 34/34 PASS; D10 invariant: 45/45 PASS; inventory tests: 3/3 PASS. These are selected replay results, **not** 649 executed tests.

## Corrected inventory semantics
`scripts/p165d10_repo_test_inventory.py` now classifies the eight legacy files through **exact filename matches**, so `p165d` must list **only** `tests/test_scene_event_epistemic_p165d.py` (4 declarations) instead of swallowing versions D4…D10. Existing reports stay immutable; issue a new output folder.

## Global discovery run
`scripts/p165d10_global_regression_runner.py` launches standard library `unittest discover -s tests -p test*.py -v`, saving stdout, stderr, exit code and timeout in a new `build/` folder. Any nonzero exit or timeout is RED/INCOMPLETE. A successful exit is GREEN **for unittest discovery only**: pytest-specific tests, unconventional naming, missing imports and uncollected functions are NOT silently claimed as executed. Compare unittest's `Ran N tests` against AST 649 but do not expect exact equivalence.

Runner deliberately doesn't edit tests, source modules or canonical memory. Warning: discovered test code **itself can write artifacts**; this runner is not a guarantee of read-only test execution. Review scripts and working tree before broad reruns; use an isolated checkout if write side-effects are unacceptable.

## Windows PowerShell commands — gate before C
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
git status --short
py -m unittest discover -s tests -p "test_p165d10_global_runner.py" -v
if ($LASTEXITCODE -ne 0) { throw "Runner unit tests RED — STOP" }
py scripts/p165d10_repo_test_inventory.py --root . --out "build\brody-p165d10-inventory-002"
if ($LASTEXITCODE -ne 0) { throw "Inventory RED — STOP" }
Get-Content "build\brody-p165d10-inventory-002\SUMMARY.json"
py scripts/p165d10_global_regression_runner.py --root . --timeout 1800 --out "build\brody-p165d10-global-001"
if ($LASTEXITCODE -ne 0) {
  Get-Content "build\brody-p165d10-global-001\MASTER_REPORT.json"
  Get-Content "build\brody-p165d10-global-001\STDERR.txt" -Tail 120
  throw "GLOBAL REGRESSION RED — GATE C HOLD"
}
Get-Content "build\brody-p165d10-global-001\MASTER_REPORT.json"
Get-Content "build\brody-p165d10-global-001\STDERR.txt" -Tail 30
git status --short
```

## Gate C, intentionally still HOLD
After global regression, construct **independent** adversarial movement fixtures and counterfactual pairs to diagnose 270 jump, 36 accelerate/full, and 18 linear/full failures. At least two evaluations: scenario labels held out from inference, and evidence after reappearance scored separately from before. Do not just add 1,350 duplicates or accept always MULTI. Do not tune to hidden oracle. The tracker remains untouched until failure categories have unit-level counterexamples and explicitly scored controls.

Governance: `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

**Status:** `GLOBAL_RUNNER_PUBLISHED / EXACT_LEGACY_CLASSIFICATION_FIXED / PC_GLOBAL_RUN_PENDING / GATE_C_HOLD`.
