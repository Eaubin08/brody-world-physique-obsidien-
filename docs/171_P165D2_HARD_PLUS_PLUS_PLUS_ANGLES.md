# P165-D2 — HARD+++ : 675 combinaisons angle, mouvement, occultation, apparence, fond

## Résultat attendu (non encore exécuté sur le PC)
5 angles de caméra apparents (-50, -25, 0, 25, 50), 5 lois (immobile, linéaire, inversion, saut, accélération), 3 occultations (aucune, partielle, totale), 3 apparences (rouge, bleu, changement en cours) et 3 contextes (simple, deux plans, parallaxe synthétique). **675 configurations × 2 répétitions = 1350 examens**. Chaque épisode comprend sept images PIL.

Le générateur connaît le scénario pour fabriquer et noter les images, mais **`image_only_evaluate(frames)` ne reçoit ni étiquette, ni trajectoire vraie, ni paramètre de caméra, ni identité réelle**. Les observations sont extraites via les composantes connexes P164. Les conclusions disponibles sont HOLD ou NOVELTY_CANDIDATE — jamais une interprétation causale, une identité ou une profondeur prétendue certaine.

Les indices de formes et de couleur sont encore très limités. Cette passe est une batterie adversariale et non une réparation P164 ni le raccordement total F12/F16/MMonde. Aucun radar/thermique/LiDAR matériel, aucune fusion P165-B réellement connectée aux pixels, et pas de graphe complet extrait automatiquement. L'angle ici est un déplacement projeté synthétique et **non une véritable rotation de caméra 3D**. La parallaxe est également simplifiée à deux déplacements de décor. Les métriques de distance sur les positions uniques peuvent être biaisées par les distracteurs.

## Pourquoi la nouvelle campagne est utile
P165-D avait `gates_rule_based_on_fixture_case=true` : un résultat prudent par nom de scénario ne prouvait pas une compréhension. P165-D2 retire **ce paramètre de l'interface de décision**, tout en vérifiant la provenance de chaque vérité de notation. Une absence de faux SELECT est ici triviale puisque le moteur ne sélectionne jamais : ne pas annoncer de gain de précision physique. Le but est de révéler exactement les limites de visibilité et localisation lorsque l'on combine facteurs plutôt que de tester des scènes faciles séparément.

## Gates
1. 675 combinaisons distinctes, aucune cellule silencieusement ignorée.
2. Image-only inference, sans fuite de vérité.
3. Preuve brute par épisode, dossier jamais écrasé.
4. Couverture, HOLD, nouveauté candidate et erreurs de centres observés **par groupe**.
5. Les 77 conditions précédentes, les 150 tests P165-A et les 9 contrats multimodaux ne sont pas exécutés par cette seule commande : une régression transversale doit être organisée séparément.
6. Toute prétention de réussite du world model reste BLOCK sans récupération indépendante de l'identité, scène depuis pixels et prédiction visuelle.

## Windows PowerShell (branch gate + fail closed)
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/hard_scene_angles_p165d2.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe échouée" }
py -m unittest discover -s tests -p "test_hard_scene_angles_p165d2.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués — STOP" }
py -m brody_world_physique.hard_scene_angles_p165d2 --seeds 2 --out "build\brody-p165d2-hard-angles-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne échouée" }
Get-Content "build\brody-p165d2-hard-angles-001\MASTER_REPORT.json"
```

Gouvernance `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

**Verdict :** `P165D2_675_MATRIX_PUBLISHED / IMAGE_ONLY_LABEL_BLIND / PC_TEST_PENDING / TRUE_3D_AND_MULTISENSOR_PENDING`.
