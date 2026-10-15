# 86 — FUSION-F3b : école de cinq leçons, images et notes réelles

**Statut : code et 2 tests publiés, exécution PC attendue.** Sur branche `exp/p2-multirepresentation-ablation-20261009`; ne pas toucher `main`.

## Les cinq leçons
| Leçon | Stade | Apprentissage guidé TRAIN | TEST / nouvelle composition |
|---|---|---|---|
| 01 | E0 | trait | trait dans une autre position |
| 02 | E0 | rectangle | 2 rectangles de tailles / positions différentes |
| 03 | E1 | triangle | 2 triangles dans de nouveaux cadres |
| 04 | E1 | cercle | 2 cercles, variation de position / taille |
| 05 | E2 précurseur | rectangle | trois éléments géométriques composés |

Chaque leçon utilise **l'observation V3** `observe_only`, l'encodage de gestes TRAIN de P2.11b et la recomposition P2.11c. La cible professeur est construite de façon indépendante, cachée jusqu'au scellement du PNG de Brody, puis ouverte pour le score. Aucun score TEST ne sert à choisir le geste suivant. Les cinq leçons sont **indépendantes** : ce n'est pas encore un entraînement continu avec accumulation du savoir d'une leçon à l'autre.

### Sorties persistantes
Un dossier par leçon contenant `candidate.png`, `comparison.png`, `episode.json` et la mémoire locale. La racine de l'école contient `scores.csv` et `summary.json`. Pour comprendre le progrès : `baseline_error` (dessin blanc), `candidate_error` (Brody), `gain` (pixels évités), `verdict` et `gestures`. Les 5 comparaisons sont de vrais fichiers de sortie.

## PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_fusion_f3b*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F3b échoués" }
py -m brody_world_physique.fusion_f3b_multilesson_school_v0 --out "build\fusion-f3b-school-001"
if ($LASTEXITCODE -ne 0) { throw "École F3b échouée" }
Get-Content "build\fusion-f3b-school-001\scores.csv"
Get-Content "build\fusion-f3b-school-001\summary.json"
Invoke-Item "build\fusion-f3b-school-001\03-triangle\comparison.png"
```

**Ne pas relancer sur un répertoire de sortie existant** : utiliser `-002` pour un deuxième essai.

## Ce que cette école NE démontre pas
- Le moteur à gestes reste largement déterministe et supervisé.
- Les « objets » E2 ne sont ici que des primitives répétées : ni identification d'objet réel, ni sémantique, ni causalité.
- Les compétences historiques de V4.1/V4.2 existent et passent en régression, **mais ne sont pas encore branchées au choix visuel de cette école**.
- Pas encore de savoir cumulatif entre leçons, de Reverso complet ni de contexte physique.
- `KX108_ONLY`, aucune écriture Native Memory/B8.

**Suite recherchée :** curriculum cumulatif à souvenirs conservés d'une leçon à l'autre, parties d'objets, positions réciproques, transformation et évaluation en aveugle sans fuite.
