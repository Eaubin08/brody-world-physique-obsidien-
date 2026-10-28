# P165-D8 — D6→D7 contextual bridge and deterministic evidence views

## Scope
The module `brody_world_physique/goal_track_bridge_p165d8.py` connects *image-derived* D6 multiple tracks to D7 epistemic claims. The same measured evidence supports distinct goal-focused views without rewriting physical observations. No truth-label, movement label, fixture type or hidden target location is passed to inference. Evaluation alone scores continuity using the existing D6 oracle.

This is an **integration test** for evidence ownership, not a gain in visual perception or proof of true identity. D6 candidate positions remain in image pixels and synthetic 1D world-state adapters; physical camera corrections, 3D models, multimodal radio sensing and semantic understanding of natural-language goals are absent.

### Claim mapping
- P165-D3 detected candidate counts → OBSERVED spatial claim (observed by a synthetic image detector, not guaranteed correct).
- P165-D6 first association path → INFERRED temporal candidate.
- P165-D4 synthetic state adapter → provisional physical model estimate, explicitly NOT measured world coordinates.
- P165-D6 competing paths → UNKNOWN identity alternative, conflicting with the chosen track hypothesis.
- Cause of occultation or identity change → UNKNOWN causal status.
- Symbolism → **no statement invented**; symbolic focus remains empty unless a user supplies an interpretation.

### Tests and scoring
The same scene is evaluated with LOCATE, REIDENTIFY, RENDER, EXPLAIN_CAUSE, PREDICT and INTERPRET_SYMBOL. The serialized evidence digest must not change across views. Repeated identical frames must yield identical digest and D7 views. A common MULTI status may remain even for an empty symbolic focus, because D7 retains contradictions across all domains; distinguish `focused=[]` from `status=MULTI`. No successful physical resolution is claimed.

The D6 `same_path_pre_post_recall` is recomputed only **after** inference, as an evaluation measure. It does not identify objects physically. P165-D8 reuses the same full matrix of 675 parameter combinations × 2 seeds = 1,350 episodes; it does NOT yet repair the 324 continuity failures. The existing 77-configuration historical regression and previous suites must be run separately.

## PowerShell run
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/goal_track_bridge_p165d8.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe échouée" }
py -m unittest discover -s tests -p "test_goal_track_bridge_p165d8.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués — STOP" }
py -m brody_world_physique.goal_track_bridge_p165d8 --seeds 2 --beam 8 --out "build\brody-p165d8-goal-bridge-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne échouée" }
Get-Content "build\brody-p165d8-goal-bridge-001\MASTER_REPORT.json"
```

Gouvernance: `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`. Code published, execution and results on PC pending.
