# 64 — P2.9i Comparaison appariée / sélectivité HOLD

**Statut :** analyseur et tests publiés. Aucun verdict de supériorité avant résultats sur PC.

Entrée : rapport P2.9h EXISTANT `build/p29h-ablation-20261009-061517.json`. Aucun nouvel entraînement, décodage vidéo, seuil modifié ni retour TEST dans une décision. L'analyse sépare :
1. épisodes où A1 (spatial) **et** A4 (mémoire) prédisent : erreurs appariées, différence moyenne mémoire moins spatial;
2. épisodes où mémoire HOLD mais spatial prédit : erreur de la méthode spatiale;
3. épisodes où les deux HOLD;
4. cas inverse mémoire seule.

Le rapprochement est fondé sur `(clip, frame_video)`, en convertissant le champ `scores.frame` de P2.9h (indice d'observation à pas 6) en `frame_video = frame * 6`. Le rapport doit contenir exactement un score par bras et épisode et un précommit correspondant. Les valeurs sont déjà des **erreurs post-révélation**, non une nouvelle prédiction. La sélection sur les acceptés peut être biaisée; la comparaison appariée le rend visible mais ne prouve pas à elle seule un avantage hors échantillon.

## Exécution
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p29i*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.9i échoués" }
$source = "build\p29h-ablation-20261009-061517.json"
$out = "build\p29i-paired-$(Get-Date -Format yyyyMMdd-HHmmss).json"
py -m brody_world_physique.p29i_paired_audit_v0 --source $source --out $out
if ($LASTEXITCODE -ne 0) { throw "Analyse appariée échouée" }
py -m brody_world_physique.p29i_paired_audit_v0 --source $source --out $out --verify
if ($LASTEXITCODE -ne 0) { throw "Rejeu P2.9i échoué" }
Write-Host "RESULTATS=$out"
```

**Frontières :** aucune évaluation raster ou modification de P1/Reverso/V4.2, aucune corrélation causalement démontrée, aucune promotion B8, Native Memory readonly et KX108_ONLY. Étape suivante après les chiffres : visualiser les prédictions appariées et créer une ablation réellement multimodale utilisant les mêmes frames, non simplement renommer A4.
