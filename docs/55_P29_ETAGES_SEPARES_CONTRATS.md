# P2.9 — Chacun sa place, chacun son étage

Statut : **contrats typés expérimentaux publiés, tests PC non exécutés, apprentissage transférable non démontré**.

## Doctrine de l'auteur
Une observation pixel ne décide pas ce qu'elle signifie physiquement. Une représentation spatiale organise les relations, référentiels, échelles et incertitudes, mais n'établit pas de vérité. L'expérience conserve les succès, les contradictions et la provenance ; la connaissance de travail est révisable. Les buts humains choisissent le chemin d'utilisation du savoir, sans pouvoir changer les observations ou les preuves. La gouvernance B7/B8/B10 et KX108 reste une couche séparée, à autorité non répliquée.

## Contrats
| Étage | Entrée | Sortie | Interdictions |
|---|---|---|---|
| P — perception | image/paire d'images | `PixelObservation` (mesures, qualité, provenance) | interdit : oracle caméra, vérité monde, objectif utilisateur |
| R — représentations | observation + référentiel explicite | `SpatialRelations` | interdit : deviner une cause physique, fusionner des référentiels inconnus |
| E — interprétation / expérience | relations + éléments d'historique admissibles | `WorkingBelief` (provisoire, réfutable, HOLD) | interdit : promouvoir B8, écrire mémoire |
| I — intention | objectif humain + savoir disponible | `GoalRouting` (proposition d'exploration/génération/explication) | interdit : réécrire la fiabilité et les preuves |
| G — gouvernance externe | requêtes explicitement autorisées | B7/B8/B10/KX108 selon leurs contrats | interdit : autorité créée par Brody |

## Ce qui est réellement implémenté
`brody_world_physique/p29_layer_contracts_v0.py` fournit quatre objets typés et des fonctions séparées de représentation, inférence provisoire et orientation d'intention. Ce module **n'apprend pas la perception** et **ne modifie pas** le calcul de fiabilité P2.8c. Les interfaces sont le premier palier, pas la fermeture P2.9.

## Expérience à préparer pour le second palier P2.9
1. Entrées réellement hors générateur P2.8b, conservées sous forme de paires d'images et de métadonnées de capture indépendantes.
2. Mesurer séparément l'échec de perception (lumière, occultation, marqueurs manquants), l'échec de représentation (correspondance, référentiel), celui de la fiabilité historique (changement de régime), et celui de l'intention (mauvais choix de tâche, jamais changement de vérité).
3. Évaluer transferts avec séquences sans oracle et retours indépendants différés, dont le protocole doit rester explicite.
4. Interdire tout contournement `HOLD` ; tester que le but `generate` ne fabrique aucune position physique vérifiée.
5. Comparer à couverture égale et sur images inédites. Les scores P2.8b/c restent des diagnostics sur scènes synthétiques prédéfinies.
6. Conserver la distinction expérimentation locale / B8 `SUPPORTED`, `VERIFIED`, `PROMOTED`; persistance B10 encore HOLD.

## Lancer les tests (PC fixe, branche d'expérimentation)
```powershell
$repo = "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
Set-Location $repo
git branch --show-current
git pull --ff-only
py -m unittest discover -s tests -p "test_p29*.py" -v
if ($LASTEXITCODE -ne 0) { throw "P2.9 FAIL" }
```
Ne lancer `git pull --ff-only` que si la branche courante est `exp/p2-multirepresentation-ablation-20261009` et sans modifications locales à protéger.
