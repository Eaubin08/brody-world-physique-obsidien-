# 73 — P2.11b : réemploi réel de gestes mémorisés

STATUS: CODE_PUBLISHED / PC_TEST_PENDING / FROZEN_MOTOR_TRANSFER / IMAGE_GENERATION_ONLY

## Fonctionnement
Le module `brody_world_physique/p211b_frozen_gesture_transfer_v0.py` utilise `suggest_gestures_from_reference` de l'école de dessin V1 sur une image TRAIN, contrôle chaque geste avec `checked_gesture`, enregistre ses coordonnées et la version empreinte du code (`image-thinning`, `drawing-motor-render`) dans une mémoire locale candidate. À la génération, il relit et vérifie le registre, reconstitue les véritables `GestureV1` enregistrés et produit un PNG avec `render` **sans ouvrir la cible TEST**. Une cible facultative n'est ouverte qu'après sauvegarde du PNG pour calculer son erreur.

La génération dépend donc bien du contenu des gestes mémorisés. Il ne s'agit pas simplement de choisir un moteur sur la base d'un `ACCEPTED`.

## Limites
Ceci est un **rejeu de gestes extraits d'une référence TRAIN**. Ce n'est pas une sélection contextuelle optimisée de gestes pour une scène nouvelle, et ce n'est pas encore un apprentissage génératif général. En particulier, le système ne compose pas encore une intention inconnue depuis plusieurs gestes, n'applique pas Reverso, et ne démontre pas d'amélioration hors distribution. Le journal P2.10d n'est pas directement utilisé pour sélectionner un geste; il reste un témoin de tentatives supervisées et une étape de raccordement futur.

## Validation PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p211b*.py" -v
if ($LASTEXITCODE -ne 0) { throw "P2.11b tests échoués" }
```

## Exemple de deux commandes distinctes
```powershell
py -m brody_world_physique.p211b_frozen_gesture_transfer_v0 --train "SOURCE_TRAIN.png" --memory "build\p211b-gestures.json"
py -m brody_world_physique.p211b_frozen_gesture_transfer_v0 --memory "build\p211b-gestures.json" --out "build\p211b-rejeu.png"
```
Les PNG TRAIN doivent être compatibles avec la dimension `SIDE` du moteur de dessin historique. Ne pas confondre ce rejeu avec une nouvelle image conditionnée par une intention. Le fichier mémoire et les PNG ne sont jamais promus dans Native Memory.

## Prochain verrou
Comparer en aveugle ce rejeu, une page blanche, le moteur de dessin sans mémoire et une combinaison de gestes adaptée à la nouvelle image; séparer TRAIN et TEST et enregistrer aussi les régressions. L'objectif ultérieur est une **procédure choisie et modifiée à partir des expériences**, sans copie des pixels de la cible test.
