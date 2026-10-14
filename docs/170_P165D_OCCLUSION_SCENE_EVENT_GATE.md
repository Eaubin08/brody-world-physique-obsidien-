# P165-D — Gate des événements masqués : première tranche, non intégration finale

## Livré
`scene_event_epistemic_p165d.py` avec 6 familles déjà synthétisées P165-A, 25 épisodes par famille par défaut, segmentation de composantes par P164, graphe relationnel UNKNOWN P165-C et verdict HOLD/MULTI. Quatre tests. L'oracle et les événements véritables ne sont inscrits que dans les preuves d'examen.

## Limite critique (ne pas travestir)
**Cette première tranche utilise le nom du scénario fourni par la fixture pour choisir HOLD/MULTI et la raison.** Ce n'est **pas** un moteur qui déduit l'incertitude ou l'événement depuis les images : elle prouve seulement les garde-fous **dans les scénarios préétiquetés**. `gates_rule_based_on_fixture_case=true` doit rester visible. Le graphe relationnel est UNKNOWN injecté, pas extrait des pixels. Les signatures P165-B ne sont pas encore fusionnées dans les tracks, aucune réapparition n'est vérifiée par signatures réellement mesurées.

Il serait incorrect de déclarer : « P165-D connecte maintenant toutes les couches ». L'étape qui manque est un détecteur d'observabilité **agnostique du nom de la fixture**, avec cas cachés, suivi multi-objet, graphe fond/avant/arrière dérivé du raster, et comparaison physique/multicapteur indépendante.

## Matrice exécutée
`occluded_jump`, `substitution`, `crossing_indistinguishable`, `color_swap`, `camera_without_landmarks`, `multiple_depth_planes`. Le même protocole n'entraîne pas le modèle sur les 77 anciennes conditions et ne les rejoue pas.

## Commande PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/scene_event_epistemic_p165d.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe échouée" }
py -m unittest discover -s tests -p "test_scene_event_epistemic_p165d.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués — STOP" }
py -m brody_world_physique.scene_event_epistemic_p165d --each 25 --out "build\brody-p165d-event-gate-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne échouée" }
Get-Content "build\brody-p165d-event-gate-001\MASTER_REPORT.json"
```

Gouvernance : `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

**Verdict avant validation PC :** `P165D_FIXTURE_GATE_PUBLISHED / TRUE_PERCEPTUAL_EVENT_REASONING_PENDING / SENSOR_FUSION_NOT_INTEGRATED / REAL_SCENE_GRAPH_NOT_INTEGRATED`.
