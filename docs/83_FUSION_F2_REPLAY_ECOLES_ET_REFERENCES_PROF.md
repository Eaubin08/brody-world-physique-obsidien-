# 83 — FUSION-F2 : réexamen des écoles historiques et des bancs P2

**Statut : CODE PUBLIÉ / TESTS PC EN ATTENTE.** Branche expérimentale `exp/p2-multirepresentation-ablation-20261009`, sans modification de `main`.

## Objectif
Exécuter les tests historiques de l'école V0–V4.2 et les tests P2 d'images sans confondre leurs conditions de supervision. Le module `brody_world_physique/fusion_f2_school_regression_v0.py` lance 15 suites indépendantes en sous-processus. Chaque suite conserve son log, son code de sortie, sa durée et le SHA256 du test dans `report.json`. PASS signifie assertions satisfaites ; ce n'est pas une note de qualité de génération.

## Correction importante de provenance des images locales
L'utilisateur a confirmé explicitement le 9 octobre 2026 que **les sept nouvelles images partagées pendant F2 sont celles du PROFESSEUR**, et non des réalisations de Brody.

Les onze images partagées auparavant sont des PRODUCTIONS DE BRODY : trois `lesson_01..03_first_drawing(1).png`, quatre `exam_01..04_from_memory(1).png` et quatre `exam_01..04_after_feedback(1).png`.

Nous disposons donc de **11 productions élève et 7 références professeur**. L'association exacte référence→leçon/examen n'est pas démontrée simplement par les images : identifier les noms de fichiers originaux et les reçus dans `build` avant de créer un manifest d'appariement. Ne pas considérer `after_feedback` comme une référence professeur.

L'adaptateur F1 `fusion_historical_evidence_v0.py` lit les vrais chemins et peut scorer `teacher` contre les productions de même taille. Les scores restent UNKNOWN pour les épisodes dont la référence n'est pas appariée de façon vérifiable.

## Validation Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_fusion_f2*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F2 échoués" }
```

## Audit complet des anciennes et nouvelles suites
```powershell
py -m brody_world_physique.fusion_f2_school_regression_v0 --repo . --out "build\fusion-f2-audit-001"
if ($LASTEXITCODE -ne 0) { Write-Warning "Consulter build\fusion-f2-audit-001\report.json pour les échecs" }
```
Le répertoire de sortie doit être absent. Les exercices exécutés peuvent produire leurs propres fichiers temporaires. Les preuves historiques brutes sont inchangées par le contrôleur.

## Suite
**FUSION-F3 :** retrouver le véritable appariement des sept références du professeur et des onze productions de Brody ; obtenir une planche comparative fiable et les notes par examen. Puis reprendre le curriculum formes, objets, relations, transformations, scènes et monde avec rappel différé, épreuves inédites, Reverso et corrections P2. Préserver séparation TRAIN/TEST, `KX108_ONLY`, absence d'écriture Native Memory.
