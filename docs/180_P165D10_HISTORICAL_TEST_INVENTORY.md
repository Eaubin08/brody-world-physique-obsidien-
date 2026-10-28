# 180 — P165-D10 Historical inventory and legacy replay

## Scope verified from branch
Eight existing historical test files were read and counted, **41 declared test methods**:
- P161 visual OOD: 4
- P162 math/physical bridge: 5
- P163 camera/occlusion: 6
- P164 identity/occlusion: 4
- P165-A scene adversarial: 4
- P165-B modal signatures: 7
- P165-C contextual scene: 7
- P165-D epistemic event: 4

Eight previously audited D2-D9 suites: 34 declared tests. P165-D10 invariant suite: 45 declared tests, PC reports 45 PASS. **120 declared tests in these 17 known test files**, not necessarily all tests in this repository; the new inventory tests add 3 more potential tests, not yet executed. A new read-only AST inventory provides the complete count for files named `tests/**/test*.py` on the current PC checkout. Method declarations are not identical to discovered/runnable test cases, particularly if test generators/decorators/parameterization are involved.

## Files published
- `scripts/p165d10_repo_test_inventory.py`: parses every `test*.py` under `tests/` using AST, records method declarations/imports/classes/path/SHA-256/syntax failures, identifies legacy filenames, writes immutable JSON reports; does not import or execute test modules.
- `tests/test_p165d10_repository_inventory.py`: 3 tests of count presence, safe AST no-side-effect behavior and report preservation.
- This document is diagnostic only; **no tracker, perception or governance code changed**.

## Gate C prerequisite — PC PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }

py -m unittest discover -s tests -p "test_p165d10_repository_inventory.py" -v
if ($LASTEXITCODE -ne 0) { throw "Inventory tests RED — STOP" }

py scripts/p165d10_repo_test_inventory.py --root . --out "build\brody-p165d10-inventory-001"
if ($LASTEXITCODE -ne 0) { throw "Inventory RED — STOP" }
Get-Content "build\brody-p165d10-inventory-001\SUMMARY.json"

$historical = @(
 "test_image_hard_visual_ood_p161.py",
 "test_image_math_physical_bridge_p162.py",
 "test_image_camera_occlusion_gate_p163.py",
 "test_image_identity_occlusion_p164.py",
 "test_image_scene_adversarial_p165a.py",
 "test_modal_signature_fusion_p165b.py",
 "test_contextual_scene_graph_p165c.py",
 "test_scene_event_epistemic_p165d.py"
)
foreach ($pattern in $historical) {
 py -m unittest discover -s tests -p $pattern -v
 if ($LASTEXITCODE -ne 0) { throw "Historical regression RED: $pattern" }
}
Write-Output "LEGACY_41_REPLAY_COMPLETE_IF_ALL_GREEN"
```

## Follow-through
If the historical replay is GREEN, the next stage should audit test depth (counterexample sensitivity, mutation tests, independence of fixtures) and only then Gate C. Running the full 675 matrix on the existing fixed renderer does **not** validate real 3D physical comprehension. P165-D9 showed 270/324 failing episodes in the `jump` category, 36 accelerate/full and 18 linear/full. These categories are generator labels; they do not prove causes.

Governance: `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`; experimental branch only. No code authority promotion.

**Status:** `HISTORICAL_41_FILES_VERIFIED / INVENTORY_AUTOMATION_PUBLISHED / INVENTORY_AND_REPLAY_PC_PENDING / GATE_C_HOLD`.
