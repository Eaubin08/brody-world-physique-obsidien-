# 178 — P165-D9 : statut local de demande et diagnostic stratifié des échecs D6

## Problème initial
P165-D8 valide 1350/1350 vues immuables et la variation des priorités selon la demande. Il ne corrige pas les 324 échecs de continuité D6 (1026/1350 réussites). Le compteur `symbolic_hold=0` est ambigu parce que des contradictions dans d'autres couches imposent le statut global MULTI, même lorsqu'aucune preuve symbolique n'existe.

## Première tranche P165-D9
Module `brody_world_physique/local_epistemic_diagnostic_p165d9.py` :
- `local_view(goal,claims)` fournit `local_status` **distinct** de `global_status`.
- `HOLD_LOCAL_NO_RELEVANT_EVIDENCE` signifie aucune assertion pertinente, quelle que soit la contradiction ailleurs ; `HOLD_LOCAL_UNKNOWN` signifie focalisation composée uniquement de UNKNOWN sans contradiction ; `MULTI_LOCAL` signifie contradiction impliquant une assertion focalisée ; `SUPPORTED_VIEW_NOT_PROOF` n'est jamais une promotion de vérité.
- Contradictions globales préservées via D7 sans modifier les observations.
- Diagnostic des mêmes 675 conditions ×2 graines=1350 épisodes D6, classé par `motion/occlusion`, avec `pre_fail`, `post_fail`, `continuity_fail` et `old_four_pass_new_fail`.
- Préservation des preuves dans EXAMS.jsonl et MASTER_REPORT.json. Les résultats d'évaluation utilisent l'oracle **uniquement après l'inférence**.
- Ne modifie pas le suivi, n'améliore donc pas intrinsèquement les 324 échecs. Le diagnostic mesure des associations, pas des causes physiques démontrées.

### Nouvelles limites et étape suivante
Une « résolution effective » d'hypothèses par observation nouvelle n'est **pas encore livrée**. Ce premier volet construit les indicateurs, le second devra vérifier une élimination motivée par des observations indépendantes, sans utiliser la vérité cachée du générateur ni supprimer des hypothèses alternatives injustement. La vérité de position dans les essais est simulée ; ni RF/CSI/Wi-Fi, ni radar, ni caméra 3D calibrée, ni données terrain réelles sont connectées.

Les buts sont passés comme codes explicites, pas inférés depuis le langage naturel. Les assertions physiques, conceptuelles et symboliques n'ont pas le même statut de preuve.

## Exécution PC Windows PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/local_epistemic_diagnostic_p165d9.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P165-D9 échouée" }
py -m unittest discover -s tests -p "test_local_epistemic_diagnostic_p165d9.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P165-D9 échoués — STOP" }
py -m brody_world_physique.local_epistemic_diagnostic_p165d9 --seeds 2 --beam 8 --out "build\brody-p165d9-local-audit-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P165-D9 échouée" }
Get-Content "build\brody-p165d9-local-audit-001\MASTER_REPORT.json"
```

Gouvernance `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`. Pas d'écriture canonique ni dans main.

**Verdict pré-validation :** `P165D9_LOCAL_STATUS_AND_DIAGNOSTICS_PUBLISHED / 675_MATRIX_PENDING / TRUE_CONTINUITY_REPAIR_PENDING`.
