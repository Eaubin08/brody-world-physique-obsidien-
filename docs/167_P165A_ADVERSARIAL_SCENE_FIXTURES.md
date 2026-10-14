# 167 — P165-A : nouveaux examens adverses de scène, première tranche

**Statut : code et tests publiés, validation PC en attente.**

Source : [166 — Protocole Hard++ scène contextuelle](166_P165_HARD_PLUS_PLUS_CONTEXTUAL_SCENE_PROTOCOL.md). Ce chapitre est **un premier lot de six scénarios adverses**, et non les 16 familles complètes ni une réparation réussie du moteur de perception.

## Six familles de la première tranche
- `color_swap` : une cible change de couleur alors qu'une autre cible conserve sa couleur.
- `crossing_indistinguishable` : deux objets visuellement identiques croisent effectivement leurs positions dans la vidéo ; identité intrinsèquement ambiguë si aucun indice additionnel.
- `occluded_jump` : déplacement discontinu et obstacle sur deux frames.
- `camera_without_landmarks` : même déplacement apparent avec aucune référence caméra indépendante ; ne pas forcer un modèle causal.
- `multiple_depth_planes` : plusieurs surfaces apparentes et repères de caméra instrumentés ; ne prouve pas une reconstruction 3D.
- `substitution` : positions/identités ambiguës après masquage, dont les données cachées ne peuvent servir de preuve.

## Contrat de test
Le générateur `make_case` produit les frames synthétiques et un oracle d'examen isolé. Les décisions passent exclusivement par `camera_evidence`, `track` et `decision` P163/P164. L'oracle ne fournit **pas** ses identifiants ni les mouvements caméra au tracker. L'exception : le générateur lui-même connaît ses paramètres pour réaliser la fixture; ils ne sont utilisés que pour la notation.

L'examen note `unsafe_identity_claim` et `unsafe_camera_claim` quand une décision SELECT intervient dans un scénario où l'identité/la caméra sont marquées non identifiables. Ce n'est qu'un **premier indicateur** de surconfiance : aucune validation complète de scène, du plan de profondeur, ni des lois physiques n'est revendiquée.

## Limites méthodologiques
- **Pas de baseline 77 exécutée par cette commande** ; les 77 cellules P161–P164 demeurent inchangées et les résultats précédents restent distincts.
- Il s'agit de **six familles** sur 16 envisagées, pas de la campagne Hard++ complète.
- Les objets restent des ellipses synthétiques générées par PIL. Les tests n'utilisent ni photos réelles, ni annotations manuelles indépendantes, ni moteur de rendu tiers.
- Les labels d'indiscernabilité sont des propriétés définies par la fixture : la capacité à refuser doit être mesurée, pas présumée.
- `track` et `decision` ne sont **pas réparés dans P165-A** ; cette tranche expose leurs échecs. Le raccordement à F12/F16/MMonde, 3D/génération, et à la mémoire gouvernée reste ultérieur.
- Les métriques d'unsafe SELECT sont des gardes rudimentaires, pas une mesure probabiliste calibrée ou une preuve d'indiscernabilité de tous les cas.

## Windows PowerShell — STOP si test échoue
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/image_scene_adversarial_p165a.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P165-A échouée" }
py -m unittest discover -s tests -p "test_image_scene_adversarial_p165a.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P165-A échoués : STOP" }
py -m brody_world_physique.image_scene_adversarial_p165a --minutes 20 --n-each 25 --out "build\brody-p165a-hard-scene-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P165-A échouée" }
Get-Content "build\brody-p165a-hard-scene-001\MASTER_REPORT.json"
```

**Gouvernance :** `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

**Verdict :** `P165A_SIX_FIXTURES_PUBLISHED / HARD++_FULL_MATRIX_NOT_IMPLEMENTED / VALIDATION_PC_PENDING`.
