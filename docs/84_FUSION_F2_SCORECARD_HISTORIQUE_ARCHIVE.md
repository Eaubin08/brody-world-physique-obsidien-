# 84 — FUSION-F2 : comparaison historique V0 → V4.2 (preuves réelles)

Statut : lecture d'archive mise en code, tests PC à confirmer. Ne toucher ni main ni aux données d'époque.

## Entrées vérifiées dans build.rar
- `build/ecole-dessin-20261008-225534/evaluation.json` : V0.
- `build/ecole-dessin-v1-20261008-231554/evaluation.json` : V1.
- `build/dessin-memoire-v3-20261009-000320/evaluation.json` : V3.
- `build/relations-v4-1-20261009-003945/evaluation.json` : V4.1.
- `build/orientation-v4-2-20261009-012020/evaluation.json` : V4.2.

Le niveau V2 reste à réconcilier séparément : les anciens outils/instruments existent mais leur évaluation n'est pas arbitrairement substituée à une école complète.

## Comparabilité
V0 et V1 : erreurs de pixels, mais **exercices et conditions de feedback différents**.
V3 : IoU, erreurs XOR, rappel d'une représentation masquée.
V4.1 : 6 examens de relations simulées (lecture du nombre de réussites obligatoire).
V4.2 : 11 examens d'orientation, tous réussis dans l'archive simulée.
P2.12c : 1 cas amélioré/3, 2 dégradés sur des corrections de gestes, objectif différent.
**Ne pas faire une courbe unique de pourcentage de progression de ces résultats incompatibles.**

## Code
Utiliser **`fusion_f2_historical_scorecard_v1.py`**, pas la première proposition `_v0.py` qui employait des noms de champs V0 incompatibles avec l'archive. La V1 utilise `candidate_replay_error_pixels` et `after_feedback_error_pixels` de la véritable évaluation historique.

## Commandes PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_fusion_f2_historical_scorecard_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests historique échoués" }
py -m brody_world_physique.fusion_f2_historical_scorecard_v1 --build "build" --out "build\fusion-f2-scorecard-001.json"
```

Sortie : fichier JSON durable avec scores et SHA256 des évaluations disponibles. Les noms des cinq dossiers doivent se retrouver directement sous `build`; si un dossier n'y est pas, le rapport le marque `MISSING`. Ne pas recopier les sources ni les traiter comme un nouveau set d'entraînement.

Pour revoir *tous* les bancs code historiques + récents après validation :
```powershell
py -m brody_world_physique.fusion_f2_school_regression_v0 --repo . --out "build\fusion-f2-regression-001"
```
Les résultats doivent rester séparés par suite. Une réussite d'un test unitaire ne prouve pas une reconnaissance d'objet réel.

Prochain palier : associer les véritables références du professeur aux productions V0 archivées, générer la planche **SOURCE / AVANT / MÉMOIRE / APRÈS FEEDBACK**, et fusionner les épreuves d'apprentissage de l'objet sans réapprendre simplement des translations de pixels.
