# P161 — Hard Mode : transferts de représentations visuelles et lois absentes

## Point de départ : le RED de P160
P160 a fini 1920/1920 examens et cinq tests unitaires, mais `unknown_far` a produit 160/160 fausses sélections. C'est un **échec d'identification hors-banque**, même si le pipeline tourne. Les réussites sur les contextes connus reflètent un générateur d'images trop régulier ; elles ne justifient aucune conclusion sur la physique inconnue ni la robustesse multimodale.

## Objectif expérimental
Ne pas seulement transformer un régime connu en le déclarant « inédit ». Tester **des lois de mouvement complètement absentes de la phase d'éducation**, croisées avec **des rendus différents de ceux de l'apprentissage**.

Éducation visuelle : seuls les mouvements `still`, `linear`, `brake` et `boost` sur images `canonical` sont disponibles. L'élève extrait les positions d'images puis ajuste une banque figée d'accélérations. Les règles `reverse`, `oscillate`, `jump` ne figurent ni dans les exemples d'entraînement ni dans cette banque de modèles ; elles n'apparaissent que lors de la génération des examens, et leurs étiquettes ne sont utilisées que pour noter.

## Axe image — onze représentations
`canonical`, `dark`, `palette_shift` (couleur objet changée), `square`, `triangle`, `camera` (mouvement de caméra), `clutter` (distracteurs), `occluded`, `blur`, `scale` (changement de taille), `combined` (clutter + caméra + occultation).

Le système ne reçoit pas le label de style pendant l'inférence. L'extraction RGB utilise volontairement une segmentation simple pour fournir un diagnostic falsifiable de la robustesse de perception. **Il n'y a pas de correction du mouvement de caméra ; un échec sur cet axe est attendu et informatif.** Les styles ne sont pas encore des photographies réelles, des points de vue 3D, ni une multimodalité audio/vidéo réelle.

## Axe physique — sept dynamiques
Quatre lois vues à l'entraînement ; trois lois absentes : inversion de vitesse, oscillation alternée et saut brusque. Le contrôleur peut SELECT une loi connue, MULTI si plusieurs lois sont compatibles, ou HOLD. Noter : `still` et `linear` ont ici toutes deux une accélération nulle ; **leur indiscernabilité à partir de ce seul attribut est un diagnostic**, pas une réussite artificielle. De même, un inconnu peut imiter une accélération connue à court terme : HOLD n'est pas garanti.

## Matrice et verdict
11 rendus × 7 lois × 40 épisodes = **77 cellules et 3080 examens**. Rapporter par cellule : couverture de perception, erreur de localisation visuelle, SELECT correct/erroné pour les lois connues, HOLD/MULTI/SELECT sur les lois réellement inconnues. **Ne pas agréger en un pourcentage unique** : une représentation inconnue mais bien perçue n'est pas équivalente à une dynamique inconnue masquée par l'occlusion.

P161 est un **stress test indépendant**, pas une preuve de découverte d'une loi physique. L'inducteur ne connaît que l'accélération et le jeu d'images reste synthétique. Le cas `combined` peut révéler une faillite conjointe perception + cinématique.

## Commande PC (Windows PowerShell)

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/image_hard_visual_ood_p161.py
if ($LASTEXITCODE -ne 0) { throw "P161 syntaxe échouée" }
py -m unittest discover -s tests -p "test_image_hard_visual_ood_p161.py" -v
if ($LASTEXITCODE -ne 0) { throw "P161 tests échoués" }
py -m brody_world_physique.image_hard_visual_ood_p161 --minutes 20 --lessons-each 35 --exam-each 40 --out "build\brody-p161-hard-visual-001"
if ($LASTEXITCODE -ne 0) { throw "P161 run échoué" }
Get-Content "build\brody-p161-hard-visual-001\MASTER_REPORT.json"
```

Fichiers `FROZEN_PIXELS_BANK.json`, `EXAMS.jsonl`, `MASTER_REPORT.json`. Répertoire de preuves non écrasable. `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.
