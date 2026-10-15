# P162 — Première jointure expérimentale : représentation mathématique → prédiction → image → re-perception

## Statut
**Implémentation expérimentale P162**, sur branche d'ablation et en lecture seule du reste d'Obsidia. Il ne s'agit PAS encore de l'intégration runtime de F12/F16/MMonde, d'un générateur 3D ou d'un moteur de lois physiques.

Référence d'audit : [162_PREBUILD_AUDIT_PHYSICS_MATH_REPRESENTATION.md](162_PREBUILD_AUDIT_PHYSICS_MATH_REPRESENTATION.md).
Base de comparaison : `image_hard_visual_ood_p161.py`, sur **les mêmes épisodes** de chaque cellule P162 (comparaison appariée). La réexécution P161 historique n'a pas les mêmes graines et ne doit pas être présentée comme une comparaison appariée.

## Ce qui a été implémenté
- Extraction visuelle de positions (route expérimentale P161 réutilisée), sans oracle de position.
- `features` : échantillons horodatés dans le référentiel **image en pixels**, vitesses, accélérations, changements de direction, rupture et disponibilité de la mesure. On ne prétend pas convertir le pixel en mètre ni calculer des forces.
- `classify` : distinguer `still` de `linear` avec la vitesse ; détecter certains changements temporels comme `NOVELTY_CANDIDATE` ; `HOLD` si information insuffisante ; `SELECT` connu. Les règles de décision sont **codées**, non découvertes automatiquement.
- `predict_next` : candidat position future uniquement pour un régime sélectionné. Aucun accès à la future vérité.
- `render_projection` : reconstruire une **image synthétique canonique** de la position prédite, puis `reverse_check` repasse le détecteur sur cette image et compare l'alignement interne.
- Campagne : 11 styles visuels × 7 familles temporelles, avec baseline P161 recalculée **sur les mêmes images** et stats séparées par cellule.
- Rejet de l'écrasement des artefacts existants, mémoire native et contrats extérieurs intacts.

## Ce que cette passe ne fait PAS
- `SpatialFrameRefV0`/`TrajectoryV0`/`WorldStateV0`/F16/F12 ne sont pas importés ou exécutés dans ce module. Il n'existe pas encore de raccordement inter-dépôt runtime démontré : ceci est un *adaptateur expérimental*, pas l'achèvement du plan d'intégration.
- Le mouvement de caméra n'est pas compensé : les résultats mélangent encore référentiel caméra et monde.
- Les distracteurs peuvent polluer l'extraction des positions.
- Reverso ici est un rendu déterministe 2D du **candidat**, pas une génération sémantique ou une reconstitution du monde réel.
- L'examen des nouveaux mouvements ne prouve pas qu'ils sont reconnus ; le statut `NOVELTY_CANDIDATE` indique une rupture de modèle, non une loi découverte.
- La comparaison `projection_abs_sum` mesure l'écart de position face à un futur caché dans le simulateur ; elle n'est pas une preuve physique indépendante.
- La restitution image et re-perception démontrent la cohérence locale du rendu synthétique. Elles ne mesurent pas à elles seules le bon choix de trajectoire, et ne prouvent pas que la représentation est exacte au-delà des observations.

## Métriques, verdict scientifique
Dans `MASTER_REPORT.json`, lire séparément pour les 77 cellules : `new_correct_known`, `new_wrong_known`, `baseline_correct_known`, `baseline_wrong_known`, `new_novelty_unknown`, `new_select_unknown`, `baseline_select_unknown`, `new_hold`, `new_multi`, `perception_abs_sum/perception_pairs`, `projection_abs_sum/projection_scored`, `reverse_abs_sum/reverse_scored`. Le score de perception ne remplace jamais le score de décision.

Avant de prétendre que le modèle mathématique complet du projet a été validé, il faudra brancher les contrats réels F12/F16/MMonde, les repères géométriques et caméra, l'identité multi-objet, une génération depuis état physique et un contrôle hors-rendu.

## Commande PC (Windows PowerShell)
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/image_math_physical_bridge_p162.py
if ($LASTEXITCODE -ne 0) { throw "P162 syntaxe échouée" }
py -m unittest discover -s tests -p "test_image_math_physical_bridge_p162.py" -v
if ($LASTEXITCODE -ne 0) { throw "P162 tests échoués" }
py -m brody_world_physique.image_math_physical_bridge_p162 --minutes 20 --exam-each 30 --out "build\brody-p162-math-physical-001"
if ($LASTEXITCODE -ne 0) { throw "P162 run échoué" }
Get-Content "build\brody-p162-math-physical-001\MASTER_REPORT.json"
```

**Aucune promotion canonique, aucun effet mémoire native :** `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.
