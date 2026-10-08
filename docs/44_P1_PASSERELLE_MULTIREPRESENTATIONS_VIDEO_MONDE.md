# 44 — Brody P1 : un épisode, quatre représentations (image, espace, temps, mouvement)

**Date :** 2026-10-09. **État :** assemblage readonly P1 implémenté et testé en CI.  
**Demande utilisateur :** [42 — audit reprenant les quatre échanges](42_AUDIT_TRANSVERSAL_REPRESENTATIONS_MONDE_MULTIECHELLES.md), [43 — protocole d'expérience commune](43_EXPERIENCE_COMMUNE_BALLE_REPRESENTATIONS_V0.md). Cette étape implémente la **jointure P1** uniquement. Les **ablations P2**, les modèles **micro↔macro** et le raccordement **SENS** ne sont pas revendiqués.

## 1. Ce qui existe maintenant

**Source de classe synthétique :** 12 vidéos de [\`generate_transfer_probes_v1.py\`](../examples/generate_transfer_probes_v1.py). Le générateur sait comment les scènes sont calculées, **pas le prédicteur**.

**Routes préexistantes réutilisées telles quelles** :
1. \`world_transfer_probe_v1.run_probe_suite\` vérifie les SHA vidéos, récupère les positions via OpenCV et ancre les coordonnées sur le fiduciel de la scène (hypothèse de fixture), réutilise les expériences TRAIN, émet des prévisions TEST et les écrit dans \`forecasts_precommitted.jsonl\` **pendant le décodage séquentiel, avant la frame future** ;
2. \`examples.reverso_future_preview_v1.create_preview\` utilise l'une de ces prévisions scellées pour produire quatre PNG (dernière frame, image future déplacée/inpaintée, frame cachée révélée, différence), et une métrique absolue sur tous les pixels ;
3. **Nouvelle route de jointure** \`brody_world_physique.multirepresentation_ball_bridge_v5\` : **après** les étapes 1–2, vérifie les sources/splits, repère le même précommit \`test_01.mp4\`, relit les positions sourcées avec le détecteur EXISTANT, compare la future mesure visuelle à la prédiction, contrôle les fichiers PNG et le MAE, puis constitue **quatre vues d'un même épisode candidat**.

Aucun nouveau décodeur/estimateur de mouvement/générateur d'images/WorldStateV0 ni MemoryManager n'est créé. La liaison utilise les **classes F0 existantes** \`WorldTransformationV0\`, \`WorldStateProjectionV0\`, \`WorldStateDeltaV0\` et \`WorldExperienceCandidateV0\` ; l'objet projeté structuralement référencé n'est **pas** une nouvelle implémentation canonique de \`WorldStateV0\`.

\`\`\`text
Video TEST, source sha256, frame timestamps (SIMULATED)
  -> détecteur existant / XY ancré / frames 0,6,12
  -> candidat de prédiction (historique et mémoire TRAIN)
  -> PRECOMMIT original avant décodage frame 18
  -> Reverso déterministe : predicted PNG
  -> VÉRITÉ SIMULÉE RÉVÉLÉE : frame 18/position
  -> P1 quatre vues et trois erreurs (centre, base linéaire, MAE image)
  -> candidat WorldTransformation / Projection / Delta / Experience
  -> images + preuve JSON vérifiable
\`\`\`

## 2. Vues et indicateurs — jamais les confondre

| Vue | Données | Unité / provenance | Ce qu'elle ne prouve pas |
|---|---|---|---|
| RASTER | Images \`last_observed\`, \`predicted_reverso_candidate\`, \`heldout_frame\`, \`difference\`, chacune avec SHA | pixels BGR enregistrés en PNG, provenance source vidéo vérifiée | rendu généré ≠ observation réelle F16 |
| SPATIAL | trois \`(x,y)\` passés, XY futur proposé, XY futur observé **après** precommit | \`px\`, repère \`scene-fiducial:<sha>:anchored\` | pas de mètres, distance réelle, identité physique |
| TEMPORAL | instants des frames source, horizon et ordre | \`time_s\` artificiel / frame / FPS du fixture | pas un timing physique calibré par capteur |
| MOTION | vitesse apparente \`px/s\`, extrapolation linéaire témoin | dérivée programmée sur positions existantes | pas de gravité, friction, masse ou causalité prouvée |

**Mesures séparées :** erreur de centre en px de l'ancien learner, erreur de centre d'une baseline cinématique linéaire, erreur absolue moyenne sur le frame complet généré. Le protocole P1 **n'est pas** une compétition équitable multi-bras A0–A6 : pas de victoire « multi-représentations » déclarée.

### Première validation observée en CI

- Exécution source : [GitHub Actions P1](https://github.com/Eaubin08/brody-world-physique-obsidien-/actions/runs/37860641213).
- Première passe Linux Python 3.11 : **191 tests Python**, jointure P1 construite et rejouée, **4 vues**, **une source indépendante**, \`center_error_px ≈ 2.90944\` sur \`test_01.mp4\`. Ce chiffre n'est **ni** une moyenne générale ni une preuve de supériorité sur l'ablation.
- Windows Python 3.14 : la batterie contractuelle Python est également prévue ; le test vidéo complet requiert \`opencv-python-headless\`, exécuté ici dans le job Linux 3.11.

## 3. Gates de traçabilité

- SHA du manifeste source, SHA du fichier MP4, SHA des précommits vidéo, SHA du rapport Reverso, SHA du code P1, SHA des 4 PNGs.
- Choix du **même** precommit que Reverso, contrôle des références des 3 frames passées, vérification qu'aucun \`#frame:future#\` n'apparaît dans ces références.
- La réexécution pure P1 reproduit le JSON et recalcule les pixels PNG, les différences, l'alignement du repère et les écarts de centre ; les copies destinées à GitHub sont confrontées aux originaux SHA par SHA.
- **Restriction honnête :** un post-traitement n'est pas une preuve cryptographique indépendante que les deux programmes distincts ont été exécutés dans cet ordre réel ; l'absence de fuite de futur dépend du contrat et de l'implémentation du producteur des précommits, déjà testé séparément.
- **Une vidéo source = une source** même si quatre projections en sont dérivées ; pas de preuve de triangulation multimodale indépendante.
- \`physical_truth_proven=false\`, \`ablation_results_claimed=false\`, \`sens_runtime_executed=false\`, \`native_memory_write_allowed=false\`, \`auto_promotion_allowed=false\`, \`emits_act=false\`, \`kernel_mutation=false\`, \`decision_authority=KX108_ONLY\`.

## 4. Exécuter toute la chaîne sur Windows

Depuis \`C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image\` :

\`\`\`powershell
git pull --ff-only origin main

# Vérifier la présence d'OpenCV. Installer seulement si absent :
py -c "import cv2; print(cv2.__version__)"
# Si erreur ModuleNotFoundError :
# py -m pip install "opencv-python-headless>=4.8,<5"

$run = "build\ball-multirepresentations-p1-$(Get-Date -Format yyyyMMdd-HHmmss)"
$suite = "$run\suite"
$forecasts = "$run\anchored"
$preview = "$run\reverso"
$out = "$run\p1"

py -m examples.generate_transfer_probes_v1 --out $suite
if ($LASTEXITCODE -ne 0) { throw "Generation des videos en echec" }

py -m brody_world_physique.world_transfer_probe_v1 --suite "$suite\suite.json" --out $forecasts --camera-mode anchored
if ($LASTEXITCODE -ne 0) { throw "Previsions non produites" }

py -m examples.reverso_future_preview_v1 --suite "$suite\suite.json" --forecasts "$forecasts\forecasts_precommitted.jsonl" --out $preview --clip test_01.mp4
if ($LASTEXITCODE -ne 0) { throw "Reverso en echec" }

py -m brody_world_physique.multirepresentation_ball_bridge_v5 --suite "$suite\suite.json" --forecasts "$forecasts\forecasts_precommitted.jsonl" --preview $preview --out $out
if ($LASTEXITCODE -ne 0) { throw "Passerelle P1 en echec" }

py -m brody_world_physique.multirepresentation_ball_bridge_v5 --suite "$suite\suite.json" --forecasts "$forecasts\forecasts_precommitted.jsonl" --preview $preview --verify $out
if ($LASTEXITCODE -ne 0) { throw "Rejeu de P1 en echec" }

# Les quatre PNG copiés sous $out\images et le rapport sous $out\evaluation.json
.\scripts\publish_local_evidence.ps1 -RunPath $out
if ($LASTEXITCODE -ne 0) { throw "Publication des preuves en echec" }

Invoke-Item "$out\images"
notepad "$out\evaluation.json"
\`\`\`

**Important pour l'archive :** le script de publication reste limité à \`evidence/brody-local\`. Le dossier P1 se nomme toujours \`p1\` dans cet exemple : pour publier **plusieurs** expériences sans collision de chemin, utiliser un répertoire P1 au nom unique lors de l'exécution, ou adapter \`$out\` à \`"build\ball-p1-$(Get-Date -Format yyyyMMdd-HHmmss)"\` (les entrées restent dans le dossier \`$run\`). La commande [\`publish_local_evidence.ps1\`](../scripts/publish_local_evidence.ps1) refuse à juste titre un répertoire d'archive déjà publié.

## 5. Prochaine phase — P2, pas encore obtenue

- Ablations sur le **même split, la même source et les mêmes timestamps** avec voie raster/position/mouvement/ensemble, \`0 / 1 / N\` expériences et test caméra mobile.
- Scores indépendants : centre, comportement \`HOLD\`, couverture et image (pixel strict, recadrage explicitement autorisé mais pas appris sur target).
- Échecs instrumentaux documentés : occlusion, sans repère, sources incompatibles ou ambiguës.
- Exploration multiéchelle **ensuite** : pas d'informations micro/nano/moléculaires inventées depuis la trajectoire image.

**État actuel :** P1 est un **raccordement conservateur vérifiable**, pas un nouveau modèle du monde autonome ; MMonde/F12/F16, GPS, SENS/B8 et Native Memory n'ont pas été modifiés.
