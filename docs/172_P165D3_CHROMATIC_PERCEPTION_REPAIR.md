# 172 — P165-D3 : réparation de perception chromatique, mesure appariée

**Statut : code et tests publiés, validation PC en attente.**

## Diagnostic à corriger
P165-D2 : 675 conditions et 1350 examens GREEN à l'exécution, mais détecteur P164 dépendant du rouge. Les erreurs de localisation explosent pour bleu et changement de couleur ; le nombre de HOLD élevé ne prouve pas la compréhension.

## Nouvel essai
`brody_world_physique/color_agnostic_perception_p165d3.py` :
- détection de composantes **chromatiques** (contraste entre canaux), au lieu d'un seuil qui exige le rouge ;
- séparation des instances connectées dans une bande verticale de test ;
- plusieurs candidats gardés sans déclarer une identité unique ;
- comparaison **appariée sur exactement les mêmes scènes synthétiques** avec le détecteur P164 historique ;
- métriques par apparence/occultation : proximité du centre vrai ±6 pixels, candidats hors tolérance, erreur minimale par frame et couverture.

## Points à ne pas confondre
Ce module **n'est pas indépendant de toutes les couleurs** : il exploite la saturation/chromaticité et un prior de hauteur (y=38..59), ce qui n'est pas un détecteur de forme général. Les images achromatiques, photos réalistes, ombres et objets texturés exigent une autre méthode. Les faux positifs peuvent augmenter en présence d'éléments colorés du décor. Le scénario D2 contient une seconde ellipse rouge distractrice sur certaines frames.

La **vérité de position**, transmise exclusivement à la notation, peut être cachée par un obstacle. Le champ `recall_frames` mesure la **proximité géométrique des propositions** au centre vrai (±6 pixels), pas un rappel de visibilité réelle sous occultation. `old_pixel_abs_sum` et `pixel_abs_sum` doivent être comparés avec leur `pixel_pairs` respectif ; pas d'accuracy d'identité implicite.

Ni `identity_tracking_integrated`, ni `true_3d_or_scene_graph_integrated`, ni `real_multisensor_input_connected` ne sont revendiqués. Ce n'est pas encore le moteur définitif de perception contextuelle : le prochain verrou est l'association d'instances sans oracle, via objets/fond/caméra et évènements contradictoires.

## Commande PC Windows PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/color_agnostic_perception_p165d3.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P165-D3 échouée" }
py -m unittest discover -s tests -p "test_color_agnostic_perception_p165d3.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P165-D3 échoués — STOP" }
py -m brody_world_physique.color_agnostic_perception_p165d3 --seeds 2 --out "build\brody-p165d3-color-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P165-D3 échouée" }
Get-Content "build\brody-p165d3-color-001\MASTER_REPORT.json"
```

## Gouvernance / verdict
`native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

`P165D3_CHROMATIC_DETECTOR_PUBLISHED / PAIRED_675_TEST_PLANNED / IDENTITY_AND_REAL_SCENE_UNPROVEN / PC_VALIDATION_PENDING`.
