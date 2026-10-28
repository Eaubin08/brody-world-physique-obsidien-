# Brody — Grande passe : expériences physiques qui guident les prévisions V2

## Fonctionnalité

Cette étape fait évoluer la simple accumulation de corrections en **réutilisation effective** des expériences pour guider une prévision ultérieure.

Le module `image_experience_guided_motion_v2.py` reprend les trois hypothèses de mouvement prédéfinies (STILL, VELOCITY, ACCELERATION) et distingue plusieurs **contextes locaux** inférés des positions : axe dominant horizontal/vertical, mouvement stable, accélération apparente, ralentissement, inversion de direction, stationnarité. À partir de quatre images successives horodatées, il mesure les positions, rétro-prédit la dernière observation connue et produit trois images candidates futures. Il écrit la prévision dans `sealed_forecast.json`, avant tout accès au feedback.

Une invocation **séparée** de correction révèle la prochaine image observée, calcule les erreurs de chaque hypothèse, et ajoute cette expérience dans `candidate_physics_memory.json` (digest obligatoire). Lors d'un nouvel essai avec `--previous`, si au moins **deux épisodes de prévision distincts** possèdent le même contexte, les erreurs conservées guident la sélection. Sinon, le mécanisme revient à l'évaluation locale des trois hypothèses. En cas d'égalité, `DOUBT`, pas de sélection forcée. Les anciens résultats ne sont jamais écrasés.

Ce protocole met en évidence une séparation : apprentissage de l'expérience **oui**, découverte autonome d'une nouvelle loi physique **non**. Les modèles de mouvement et les familles de contextes sont écrits par le développeur. Le système ne sait pas encore mesurer la fiabilité des étiquettes de contexte, gérer deux objets, reconnaître une collision, interpréter un rebond comme interaction physique ou stabiliser un comportement universel. Aucune preuve de transfert hors synthétique sans campagne réelle distincte. Le système ne touche pas le noyau, n'écrit pas en Native Memory, et conserve `KX108_ONLY`.

## Validation sur PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_experience_guided_motion_v2.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

## Campagne en conditions nouvelles

Préparer un manifeste du même type que la passe 124 : `{"observations":[{"t":0,"file":"...0.png"},{"t":1,"file":"...1.png"},{"t":2,"file":"...2.png"},{"t":3,"file":"...3.png"}],"predict_t":4}`. Garder `...4.png` hors de l'entraînement et de la prévision.

```powershell
py -m brody_world_physique.image_experience_guided_motion_v2 --mode forecast --manifest "build\brody-motion-four.json" --out "build\brody-guided-forecast-001"
py -m brody_world_physique.image_experience_guided_motion_v2 --mode correct --forecast "build\brody-guided-forecast-001\sealed_forecast.json" --observed "build\frames\frame4.png" --out "build\brody-guided-correction-001"
```

Pour le nouvel épisode, employer `--previous "build\\brody-guided-correction-001\\candidate_physics_memory.json"` dans la nouvelle prévision **et** dans la nouvelle correction, en gardant des dossiers inédits.

## Piste après validation

Établir un vrai protocole de transfert avec scènes distinctes et négatifs difficiles, segmentation multi-objet et interactions, apprentissage d'une rupture de régime à partir de signaux observés, et calibrage explicite du doute plutôt que de confondre quelques exemples réussis avec une loi générale. Les modèles récents forment pour l'instant un laboratoire de trajectoires 2D.
