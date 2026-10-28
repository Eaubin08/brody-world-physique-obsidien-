# P165-D10 — test hardening and coverage audit (first pass)

## Scope / verified branch files
Audited these eight test files on `exp/p2-multirepresentation-ablation-20261009`:
- `test_hard_scene_angles_p165d2.py` — 4 tests
- `test_color_agnostic_perception_p165d3.py` — 4
- `test_persistent_world_state_p165d4.py` — 6
- `test_image_persistent_tracks_p165d5.py` — 3
- `test_reappearance_gate_p165d6.py` — 4
- `test_goal_multi_continuity_p165d7.py` — 5
- `test_goal_track_bridge_p165d8.py` — 4
- `test_local_epistemic_diagnostic_p165d9.py` — 4

**Subtotal = 34 declared test methods in these eight files. NOT an exhaustive repository-wide count.** Earlier P161/P162/P163/P164/P165 test suites, other project tests and external tests have not been inventoried. The directory listing was unavailable via the GitHub file API; do not claim the whole repository contains 34 tests.

## New first-pass suite
`tests/test_p165d10_invariant_hardening.py` provides **45 additional distinct methods**, divided into raster generation (6), chromatic perception (6), persistent state (12), hypothesis/reappearance (8), epistemic and D6-D7 bridge (13).

Targeted checks include: factorial completeness and generator determinism; red/blue components, multiple targets and empty background; source provenance, invalid frame/quality/time, prediction uncertainty and immutable prior state; beam bound, pre/post gap discontinuity and several tracks not silently becoming a single proof; local HOLD despite global MULTI, stable evidence digests and no symbolic fabrication.

These are **code-level invariant tests**, not independent proof of real-world physics, identity reconstruction, multi-sensor grounding or learned world models. There are known gaps: monochrome real scenes; varying vertical image position; unknown affine camera motion; hidden identity; event detection after a jump; black-box unseen datasets; genuine sensors. D2's hard-coded scene palette/vertical band and D6's association limitations remain.

## P165-D9 baseline (PC-reported)
1,350 episodes, 324 failures of same-path before/after continuity:
- JUMP: 270 failures (90 none, 90 partial, 90 full).
- ACCELERATE/full: 36.
- LINEAR/full: 18.
- Other motion/occlusion bins: zero in that generator.
This attribution is **by generated motion class**, not a causal proof about underlying physical mechanisms.

## Test gates
A — focused unit regressions including the new suite. GREEN required, no mutation of production modules by this pass.
B — existing integration and historical tests. The known eight suites can be replayed, but do not call this a repository-wide regression. Full historical 77 conditions require separate commands/scripts and a confirmed manifest.
C — 675×2 adversarial episodes re-run only after A and B. Re-running existing generator alone cannot establish external validity.

First run can expose RED tests: preserve failing trace, then audit source versus assertion. Do not weaken a test to force GREEN.

## Windows PowerShell commands
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }

py -m unittest discover -s tests -p "test_p165d10_invariant_hardening.py" -v
if ($LASTEXITCODE -ne 0) { throw "Gate A D10 RED — STOP" }

$prior = @(
 "test_hard_scene_angles_p165d2.py",
 "test_color_agnostic_perception_p165d3.py",
 "test_persistent_world_state_p165d4.py",
 "test_image_persistent_tracks_p165d5.py",
 "test_reappearance_gate_p165d6.py",
 "test_goal_multi_continuity_p165d7.py",
 "test_goal_track_bridge_p165d8.py",
 "test_local_epistemic_diagnostic_p165d9.py"
)
foreach ($pattern in $prior) {
 py -m unittest discover -s tests -p $pattern -q
 if ($LASTEXITCODE -ne 0) { throw "Gate B RED: $pattern" }
}
Write-Output "GATE_A_B_GREEN_IF_ALL_PASS"
```

This first pass does not change D6 tracking and cannot claim 324 failures repaired. Governance: `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

**Verdict:** `P165D10_FIRST_45_TESTS_PUBLISHED / GATE_A_B_PC_PENDING / REPO_WIDE_TEST_INVENTORY_INCOMPLETE / TRACKER_UNMODIFIED`.
