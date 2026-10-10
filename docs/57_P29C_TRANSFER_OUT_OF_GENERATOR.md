# Brody P2.9c — transfert visuel hors générateur (diagnostic)

## Contrat
Une calibration supervisée à partir de 80 scènes TRAIN (déplacements de caméra connus) est figée avant le TEST. Les 180 scènes TEST sont rendues par un **autre générateur graphique** (géométrie, fond, nuisance) puis lues par le détecteur couleur déjà programmé en P2.6. L'ancre fiable change tous les 45 épisodes dans le scénario `shifted`. Aucun feedback de vérité TEST ne met à jour la calibration : mesurer l'échec de transfert plutôt que d'introduire une adaptation supervisée dissimulée.

Comparateurs : choix figé du dernier repère ; repère calibré sur TRAIN ; abstention permanente. Cette comparaison contrôle la fiabilité du transfert, **pas** une supériorité sur P2.8c (qui dispose, lui, de feedback TEST différé). Les scénarios restent synthétiques et le détecteur n'est pas appris.

## Exécution sur PC fixe
```powershell
$repo = "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
Set-Location $repo
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull impossible" }
py -m unittest discover -s tests -p "test_p29c*.py" -v
if ($LASTEXITCODE -ne 0) { throw "TESTS P2.9c FAIL" }
$out = "build/p29c-transfer-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.p29c_transfer_v0 --out $out --train 80 --test 180 --family shifted
if ($LASTEXITCODE -ne 0) { throw "RUN P2.9c FAIL" }
py -m brody_world_physique.p29c_transfer_v0 --out $out --verify
if ($LASTEXITCODE -ne 0) { throw "REPLAY P2.9c FAIL" }
Write-Host "RESULTATS=$out"
```

## Verdict attendu après mesures (non préjugé)
Examiner le taux de mesure valide, la couverture, l'erreur moyenne et les erreurs >10 px, particulièrement avant et après chaque changement de repère. Le savoir acquis sur TRAIN reste provisoire. Si les performances baissent sur les régimes non vus, indiquer `TRANSFER_FAILURE`, pas `LEARNED_PHYSICS`. Même si la précision reste bonne, ce protocole seul ne prouve ni autonomie, ni compréhension physique réelle, ni généralisation ouverte.

## Frontières
`PixelObservation` ne reçoit que les mesures visuelles. `SpatialRelations` conserve un référentiel explicite. `WorkingBelief` est non vérifié et `GoalRouting` ne change pas la prédiction. Aucun appel B8/B10, aucun write Native Memory, aucune action KX108. Reçus calculés avant scoring en mémoire RAM, écrits/scellés sur disque après toute la simulation : pas de preuve cryptographique d'une isolation en ligne. `source_ref` est encore un identifiant synthétique. Le nouveau générateur garde volontairement couleurs et tailles de fiduciaux : il teste le changement de contexte graphique davantage qu'une perception ouverte.

**Statut** : code/tests/doc publiés, résultats à exécuter sur PC.
