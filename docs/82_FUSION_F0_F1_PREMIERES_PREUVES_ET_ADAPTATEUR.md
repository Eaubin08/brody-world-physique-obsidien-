# 82 — FUSION-F0/F1 : reprise des examens historiques, sans faux score

**Statut : F0 inventaire initial effectué ; F1 adaptateur publié ; TESTS PC EN ATTENTE.** Branche `exp/p2-multirepresentation-ablation-20261009`, pas de modification de main.

## Résultats d'inventaire
Modules déjà présents : `drawing_school_v0.py`, `drawing_school_v1.py`, `instrument_school_v2.py`, `drawing_memory_school_v3.py`, `world_relations_school_v4_1.py`, `world_orientation_school_v4_2.py`, `reverso_learning_v0.py`, `experience_memory_v1.py`. Bancs récents P2.10, P2.11, P2.12 conservés tels quels.

Branche historique `evidence/brody-local` : sous `evidence/` se trouvent les archivages `relations-v4-1-20261009-003945`, `orientation-v4-2-20261009-012020`, `p2-evidence`, ainsi que les séries de contexte/fluctuations. Le rapport V4.2 porte onze examens corrects sur onze, **mais pas une preuve de compréhension sémantique des objets réels**.

Premières images **fournies par l'utilisateur** depuis `build` :
`lesson_01_first_drawing(1).png`, `lesson_02_first_drawing(1).png`, `lesson_03_first_drawing(1).png`, `exam_01..04_from_memory(1).png` et `exam_01..04_after_feedback(1).png`. Ces onze images sont des preuves visuelles de travail, pas toutes des références professeur. Le « tout premier dessin » doit être distingué entre fichier local attribué et ancienneté chronologique vérifiée.

## Adaptateur F1
`brody_world_physique/fusion_historical_evidence_v0.py` prend des chemins d'images réelles dans un manifest utilisateur. Il garde les SHA256 de chaque fichier, affiche une planche `teacher / first / from_memory / after_feedback / transfer`, et calcule l'erreur de pixels **uniquement** lorsqu'une image professeur explicite est présente avec les mêmes dimensions. Sinon il note `UNKNOWN_NO_COMPARABLE_TEACHER` et `N/A`. Aucune donnée source n'est éditée ; aucun ancien algorithme n'est modifié ; ni mémoire native ni promotion.

### Éviter la confusion
Le fichier `teacher` n'est **pas** interchangeable avec `after_feedback`. Une image produite après correction ne prouve pas qu'elle est la cible du professeur. Ne pas fabriquer de référence depuis les sorties de Brody.

## Manifest de départ
Sous le répertoire de travail PC, créer `build/fusion-historical-manifest.json` en adaptant les vrais chemins dans `build` :
```json
{
  "schema":"BRODY_FUSION_EVIDENCE_V0",
  "episodes":[
    {"id":"lesson-01","stage":"E0","mode":"GUIDED",
     "files":{"first":"CHEMIN_REEL_VERS_lesson_01_first_drawing(1).png"}},
    {"id":"exam-01","stage":"E1","mode":"HIDDEN_TARGET",
     "files":{"from_memory":"CHEMIN_REEL_VERS_exam_01_from_memory(1).png",
              "after_feedback":"CHEMIN_REEL_VERS_exam_01_after_feedback(1).png"}}
  ]
}
```
Ne remplir la clef `teacher` que lorsqu'on a réellement retrouvé le PNG professeur correspondant.

## Validation Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_fusion_historical*.py" -v
if ($LASTEXITCODE -ne 0) { throw "F1 tests échoués" }
```
Exécution sur les preuves locales une fois les chemins retrouvés :
```powershell
py -m brody_world_physique.fusion_historical_evidence_v0 --manifest "build\fusion-historical-manifest.json" --out "build\fusion-archive-001"
```
Livrables : `historical_comparison.png` et `metrics.json`.

## Suite de F0/F1
Retrouver les dossiers `build` originaux, leurs fichiers `evaluation.json` et références professeur; réconcilier exactement les onze images; comparer dans le même mode pédagogique les résultats historiques à P2.10–P2.12, puis tester une **véritable leçon intégrée E0→E1→E2** sur formes, parties et objets. Garder l'exécution `UNSEEN_TRANSFER` séparée des corrections supervisées. Aucune réussite de test de l'adaptateur ne vaut pour une réussite à dessiner un objet.
