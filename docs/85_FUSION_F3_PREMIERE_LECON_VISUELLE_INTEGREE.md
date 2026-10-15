# 85 — FUSION-F3 : première leçon intégrée observable

**État : code + trois tests publiés ; validation PC nécessaire.** `main` intouchée.

## Ce qui est réellement raccordé
La leçon utilise `drawing_memory_school_v3.observe_only` pour encoder la référence **TRAIN** ; `p211b_frozen_gesture_transfer_v0.learn/read` pour figer et vérifier la mémoire gestuelle ; `p211c_gesture_recomposition_v0.compose` pour produire une **nouvelle composition** demandée par une disposition `IN`. Aucun pixel de la référence TEST n'est lu avant la sauvegarde du candidat et de son SHA256.

En mode démo : source d'entraînement = un rectangle ; consigne = deux nouvelles positions et dimensions ; professeur = deux rectangles synthétiques construits séparément. Image de comparaison persistante `TEACHER / BLANK / STUDENT`. Les erreurs sont des **pixels différents** et ne doivent pas être confondues avec compréhension des objets ni une généralisation à de vraies photographies. L'encodage V3 exploite un extracteur déterministe conçu par l'ingénierie.

## Lancer sur PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_fusion_f3*.py" -v
if ($LASTEXITCODE -ne 0) { throw "F3 échoué" }
py -m brody_world_physique.fusion_f3_integrated_visual_lesson_v0 --demo --out "build\fusion-f3-lesson-001"
if ($LASTEXITCODE -ne 0) { throw "Démo échouée" }
Get-Content "build\fusion-f3-lesson-001\episode.json"
Invoke-Item "build\fusion-f3-lesson-001\comparison.png"
```
**Important :** le chemin de sortie doit être absent ; chaque reprise utilise un autre nom.

## Interprétation et apprentissage
Les trois tests examinent la production d'images persistantes, l'absence de référence pour les scores inconnus et le refus d'écrasement ; ils ne représentent **pas** 3 nouvelles preuves de savoir visuel. Aucun candidat n'est promu en Native Memory, autorité `KX108_ONLY`.

## Suite à implémenter
Ce jalon reconnecte deux écoles sous un épisode observé, **pas encore le curriculum complet E0–E7**. F3b devra inclure de véritables compositions multiparties, propriétés d'identité/relations et transformations réciproques avec V4.1/V4.2 ; tracer ce qui est disponible en entrée de chaque méthode ; comparer le replay historique seul au pipeline fusionné et aux ablations, sur observations inédites, avec mêmes budgets. Une suite ultérieure devra étendre vers objets simples, scène avec occlusion, puis vidéos et situations physiques.
