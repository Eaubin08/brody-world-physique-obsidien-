# 176 — P165-D7 : continuités multiples et arbitrage épistémique orienté par la demande

## Vision utilisateur — à préserver
La priorité des représentations dépend de la demande. Les continuités possibles comprennent physique, temps, espace, identité, causalité, vécu/expérience, concept, symbolique, métaphysique et d'autres aspects selon le besoin. Il ne s'agit pas de choisir mécaniquement une unique « bonne vérité » ou de filtrer le monde à partir d'une seule image. L'observation, l'inférence, la prédiction et l'interprétation doivent conserver leurs statuts distincts. Une question symbolique n'établit pas de fait physique ; des questions physiques peuvent rester indécidables. Les questions métaphysiques relèvent d'un cadre d'interprétation, pas d'une vérité mesurée par ces tests.

## Première tranche livrée
Module `brody_world_physique/goal_multi_continuity_p165d7.py` :
- huit catégories de continuité : `physical, temporal, spatial, identity, causal, experiential, symbolic, conceptual` ;
- sept buts explicites : `LOCATE, REIDENTIFY, EXPLAIN_CAUSE, PREDICT, RENDER, INTERPRET_SYMBOL, EXPLORE` ;
- assertions avec provenance, statut épistémique `OBSERVED/INFERRED/PREDICTED/INTERPRETED/UNKNOWN`, confiance optionnelle et contradictions ;
- une priorisation différente selon la demande, **sans mutation des assertions**, sans oubli des hypothèses non prioritaires et sans promotion de vérité ;
- contradictions reportées même si elles affectent un autre aspect que le focus en cours ;
- résultat `MULTI`, `HOLD` ou `CONTEXTUAL_VIEW` ; `epistemically_resolved=false` sans preuve ;
- sept examens sur une collection de six assertions **explicitement simulées**, rapports `EXAMS.jsonl` et `MASTER_REPORT.json`, dossier préservé.

## Frontières / suites nécessaires
Cette tranche n'infère pas automatiquement le but depuis le langage naturel, n'interprète pas de vrais signaux Wi-Fi/CSI/radar/thermique, ne récupère pas le graphe P165-C et **n'est pas encore reliée au tracker P165-D6** ni aux 324 épisodes de continuité défaillante. Elle organise les hypothèses : elle ne démontre ni la bonne identité, ni la vérité d'un énoncé métaphysique, ni une physique comprise.

Les poids de priorité sont des ordres de pertinence, pas des probabilités ni des privilèges de vérité. Les conflits entre preuves de sources différentes devront être résolus plus tard par calibration, expérience, confrontation et jugement de provenance, pas par le seul but utilisateur. Les 324 échecs D6 restent une épreuve distincte à réexécuter.

## Commande PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/goal_multi_continuity_p165d7.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P165-D7 échouée" }
py -m unittest discover -s tests -p "test_goal_multi_continuity_p165d7.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P165-D7 échoués — STOP" }
py -m brody_world_physique.goal_multi_continuity_p165d7 --out "build\brody-p165d7-goal-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P165-D7 échouée" }
Get-Content "build\brody-p165d7-goal-001\MASTER_REPORT.json"
```

Gouvernance `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

**Verdict avant validation :** `P165D7_GOAL_ARBITRATION_PUBLISHED / TRACKER_INTEGRATION_PENDING / PRIORITY_NOT_TRUTH / PC_VALIDATION_PENDING`.
