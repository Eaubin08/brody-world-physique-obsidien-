# P164 — Suivi d'identité candidate et hypothèses sous occultation

**Portée** : expérience synthétique isolée. P163 reste la référence; F12/F16/MMonde réels, KX108 et mémoire native inchangés.

## Pourquoi
La campagne P163 corrigée a passé 6/6 tests et 2310/2310 épisodes. Caméra/still 30/30, mais les scènes `clutter` et `combined` restent faibles. Le HOLD sur toute occultation évite de forcer une certitude, mais ne conserve pas de solutions alternatives de suivi.

## Implémentation
1. `candidates` identifie plusieurs composantes rouges connectées **dans les pixels**, sans connaissance de la position vraie ; stocke centre, hauteur, aire.
2. `track` propage jusqu'à quatre chemins candidats via une continuité spatiale et une pénalité sur disparition. Les images occultées restent `None` ; pas d'interpolation clandestine ni récupération de vérité du simulateur. Les repères de caméra P163 restent programmés dans la fixture et analysés depuis pixels.
3. `decision` reçoit les chemins et peut SELECT, MULTI, HOLD ou `NOVELTY_CANDIDATE`. Une lacune pendant les instants 3 à 5 interdit de déclarer un événement caché reconstitué comme vérité.
4. `run` compare le nouveau tracker à la décision P163 sur **les mêmes épisodes et images**, 11 rendus × 7 dynamiques × 30 = 2310 examens. `EXAMS.jsonl` contient les candidats, les décisions et la vérité **d'examen uniquement**. Métriques d'identité candidate, taux de couverture des trajectoires, erreur de centres, SELECT faux, HOLD, MULTI et nouveautés.

## Limites et pièges scientifiques
- Le suivi reste un problème d'association heuristique d'objets rouges. Aucun modèle d'identité d'objets naturels, pas de segmentation sémantique, pas de 3D.
- Le `beam` est une heuristique de continuité. Il peut perdre la bonne trajectoire si elle paraît moins plausible que les distracteurs ; un MULTI peut ne pas contenir la vraie trajectoire. Ne pas déclarer « identité démontrée ».
- La réapparition est traitée comme une **hypothèse**, pas une vérification indépendante de l'identité.
- P164 n'effectue pas encore un vrai rendu de nouvelle image future et comparaison avec un futur issu d'une autre source ; cela reste une étape suivante.
- La `camera_evidence` estime des repères synthétiques programmés ; l'estimation caméra naturelle n'est pas démontrée.
- La couverture de piste mesurée contre la simulation est une **métrique** d'évaluation, pas une mesure connue de l'étudiant.

## Windows PowerShell — arrêt immédiat au moindre échec
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/image_identity_occlusion_p164.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P164 échouée" }
py -m unittest discover -s tests -p "test_image_identity_occlusion_p164.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P164 échoués : STOP" }
py -m brody_world_physique.image_identity_occlusion_p164 --minutes 20 --exam-each 30 --out "build\brody-p164-identity-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P164 échouée" }
Get-Content "build\brody-p164-identity-001\MASTER_REPORT.json"
```

**Verdict avant run PC** : `P164_CODE_PUBLISHED / TESTS_PC_PENDING / TRACKING_HYPOTHESES_EXPERIMENTAL / REAL_WORLD_IDENTITY_UNPROVEN`.

Gouvernance `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.
