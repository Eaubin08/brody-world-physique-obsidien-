# P163 — Estimation visuelle du repère caméra et gestion prudente de l'occultation

## Objectif
P162 a réussi ses 2310 examens, mais il confond un objet immobile et une caméra mobile : `camera/still` 30/30 fausses sélections. Sur `occluded/reverse` et `occluded/jump`, 60/60 sélections forcées sur des lois connues. P163 vérifie si **un indice de mouvement de caméra présent dans les images** suffit à normaliser le référentiel, et si une occultation critique déclenche correctement HOLD au lieu de masquer une rupture possible.

## Modifications expérimentales
- Réutilise **sans modifier** les générateurs P161 et le classificateur P162.
- Le protocole de rendu ajoute trois repères verts statiques dans le monde et entraînés avec le déplacement de caméra : ils sont visibles uniquement dans les pixels ; les valeurs `sim_camera` du générateur sont réservées au rapport d'examen, **non** transmises à l'estimateur.
- `camera_evidence` estime le déplacement apparent du fond en observant ces repères à y=13, puis `normalize` transforme la coordonnée image en position relative à la scène.
- Si les repères sont absents : `HOLD/UNOBSERVABLE_CAMERA_FRAME`. Une séquence dont les instants 3–5 sont occultés : `HOLD/EVENT_MAY_BE_HIDDEN`, sans interpolation ou lecture du futur.
- Le classificateur de P162 reçoit les coordonnées corrigées quand elles sont identifiables ; sa prédiction de position future est comparée au futur physique simulé tenu en réserve jusqu'après la prédiction.
- **Comparateur apparié** P162 : mêmes images annotées, mais sans estimation de caméra ni garde d'occultation. La perte de précision visuelle par distracteurs n'est pas automatiquement résolue.

## Campagne
77 cellules issues de 11 apparences × 7 régimes, 30 épisodes par cellule par défaut (2310 examens). Chaque ligne dans `EXAMS.jsonl` conserve mesure brute, estimation de caméra depuis pixels, positions réalignées, décision P163, témoin P162, futur candidate et vérité future **pour notation uniquement**.

Mesures : `correct_known`, `false_known`, `unknown_select`, `unknown_novelty`, `unknown_hold`, `frame_observed`, `occlusion_hold`, `paired_p162_correct`, `paired_p162_false`, erreurs de perception en px et erreur sur futur prédit. **Attention : la mesure de perception compare aux coordonnées apparentes de l'image, pas à celles du monde.**

## Limites impératives
- **Ce ne sont pas des repères automatiquement découverts dans des scènes naturelles** ; le test possède des fiduciels verts artificiels dédiés. Il ne prouve ni SLAM 3D ni compensation générale des caméras.
- La politique conservatrice HOLD sur occultation peut faire baisser le taux de couverture même lorsque les mouvements sont en réalité prévisibles ; comparer aussi le taux de fausse certitude.
- Le détecteur saturé reste fragile sous distracteurs. Les appels à F12/F16/MMonde réels ne sont **pas** branchés ; aucun noyau ni mémoire Obsidia n'est modifié.
- La « génération depuis un monde » n'est pas encore un moteur de création réel : ici la prédiction est une coordonnée numérique candidate et sa précision est évaluée par le simulateur. Le **rendu image autonome contre frame future** reste un gate P164. Il ne faut pas appeler cette passe « raccordement canonique complet ».

## Commande Windows PowerShell

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/image_camera_occlusion_gate_p163.py
if ($LASTEXITCODE -ne 0) { throw "P163 syntaxe échouée" }
py -m unittest discover -s tests -p "test_image_camera_occlusion_gate_p163.py" -v
if ($LASTEXITCODE -ne 0) { throw "P163 tests échoués" }
py -m brody_world_physique.image_camera_occlusion_gate_p163 --minutes 20 --exam-each 30 --out "build\brody-p163-camera-occlusion-001"
if ($LASTEXITCODE -ne 0) { throw "P163 campagne échouée" }
Get-Content "build\brody-p163-camera-occlusion-001\MASTER_REPORT.json"
```

**Verdict provisoire :** `P163_CODE_PUBLISHED / REAL_PC_RESULTS_PENDING / CAMERA_FRAME_PIXEL_CANDIDATE / OCCLUSION_FAIL_CLOSED / F12_F16_NOT_CONNECTED / GENERATION_NOT_CONNECTED`.

Gouvernance : `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.
