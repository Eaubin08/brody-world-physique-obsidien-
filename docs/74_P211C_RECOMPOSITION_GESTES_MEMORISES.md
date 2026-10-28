# 74 — P2.11c : recomposer les gestes d'une expérience en une nouvelle image

STATUS: CODE_PUBLISHED / PC_TEST_PENDING / LIMITED_IMAGE_COMPOSITION

Le module `brody_world_physique/p211c_gesture_recomposition_v0.py` lit une mémoire P2.11b validée, transforme les coordonnées de ses gestes vers **plusieurs boîtes données par l'utilisateur** et dessine une nouvelle image avec le moteur `drawing_school_v1.render`. Il produit en parallèle une image témoin blanche, et pré-engage les deux PNG avant de lire éventuellement une référence d'évaluation.

C'est une première recomposition spatiale d'éléments appris. Les gestes viennent de TRAIN; la composition (`boxes`) est une instruction externe, non découverte par Brody. Reverso sémantique, choix autonome de composition, perspectives 360° et généralisation à plusieurs types de scènes ne sont **pas démontrés**. Pas de mémoire native et pas de promotion de connaissances.

## Commande de validation
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p211c*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.11c échoués" }
```

## Exemple de contrat d'entrée
Créer un manifeste JSON `composition.json` :
```json
{"schema":"BRODY_P211C_LAYOUT_V0","boxes":[[8,8,34,30],[35,35,60,60]]}
```
Avec la mémoire P2.11b déjà produite :
```powershell
py -m brody_world_physique.p211c_gesture_recomposition_v0 --memory "build\p211b-gestures.json" --layout "composition.json" --out "build\p211c-composition.png"
```
Utiliser un nouveau nom de sortie chaque essai. Pour scorer après génération, ajouter `--reference "REFERENCE_TEST.png"`.

## Prochaine étape
Faire varier les boîtes, les proportions et les compositions sur un ensemble préenregistré de nouveaux cas; comparer source de gestes vs image recomposée, image blanche et procédures alternatives. Conserver les erreurs, ne pas conclure à la créativité autonome uniquement parce que le modèle a transformé des coordonnées.
