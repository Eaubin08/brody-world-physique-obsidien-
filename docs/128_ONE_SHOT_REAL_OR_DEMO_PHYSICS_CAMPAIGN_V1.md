# Brody — Passe 128 : acquisition, campagne et preuve A/B en une seule commande

La passe crée un **parcours complet** sans imposer à l'utilisateur un JSON long à rédiger à la main. Elle regroupe préparation des images, constitution du manifeste, contrôle provenance/splits de la passe 127, formation de la mémoire uniquement sur les cours et comparaison A/B sur les examens. Aucun téléchargement non sollicité ou fabrication de données présentées comme réelles.

## Mode démo — fonctionne sans fichiers externes

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_motion_one_shot_campaign_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
py -m brody_world_physique.image_motion_one_shot_campaign_v1 --mode demo --out "build\brody-campaign-128-demo-001"
if ($LASTEXITCODE -ne 0) { throw "Démonstration échouée" }
Get-Content "build\brody-campaign-128-demo-001\MASTER_REPORT.json"
Get-Content "build\brody-campaign-128-demo-001\campaign\heldout_ablation\MASTER_REPORT.json"
```

La démonstration fabrique **6 séquences synthétiques** distinctes : 3 de cours (deux trajectoires accélérées et un objet immobile), 3 d'examen (accélération, inversion, arrêt). L'indicateur `synthetic_demonstration_only=true` est explicite. Ce test peut montrer un gain ou une dégradation, sans prétendre mesurer une généralisation sur images physiques réelles. Ne pas confondre indépendance des fichiers et indépendance scientifique des scénarios.

## Mode réel — répertoire de tournages

Créer un dossier `build\\brody-real-recordings` contenant au moins **un tournage de cours et un autre d'examen**, chacun dans son propre sous-dossier. Chaque sous-dossier comporte exactement **cinq photos successives** (ou captures vidéo) triées par nom, avec un objet sombre et un fond clair dans un cadrage fixe. Format PNG/JPEG/WEBP/BMP accepté. Le module suppose des intervalles temporels égaux ; ce n'est pas une mesure physique calibrée.

Chaque sous-dossier contient également `provenance.json` :

```json
{"recording_id":"filmage-unique-A","origin":"camera","split":"train"}
```

Changer `recording_id` et `split` (`train` ou `exam`) pour chaque tournage, en gardant tous les extraits d'un tournage dans la même partition. Ne pas répartir un même tournage en deux groupes ni réutiliser une même capture. Valeurs `origin` autorisées : `camera`, `video`.

```powershell
py -m brody_world_physique.image_motion_one_shot_campaign_v1 --mode real --sources "build\brody-real-recordings" --out "build\brody-campaign-128-real-001"
Get-Content "build\brody-campaign-128-real-001\MASTER_REPORT.json"
Get-Content "build\brody-campaign-128-real-001\campaign\heldout_ablation\MASTER_REPORT.json"
```

Attention : 5 images complètement identiques pendant l'immobilité seront refusées comme doublons ; utiliser de vraies captures distinctes. Le contrôleur valide les empreintes et identifiants déclarés, **pas l'origine caméra cryptographiquement**. Un recadrage/redimensionnement peut créer des duplications ou masquer des liens de provenance. La segmentation échoue si fond sombre ou objets multiples.

## Où lire les preuves

- `campaign_manifest.json` : manifeste obtenu automatiquement ;
- `campaign/split/SPLIT_EVIDENCE.json` : empreintes des images et contrôles de partition ;
- `campaign/train_forecast_*` et `train_feedback_*` : cours et mémoire physique candidate ;
- `campaign/heldout_ablation/EVIDENCE.json` : chaque prédiction sans et avec mémoire et leurs erreurs ;
- `campaign/heldout_ablation/MASTER_REPORT.json` : nombre de HOLD, erreurs et avantage apparié de la mémoire.

**Interprétation :** avantage positif = diminution moyenne des erreurs sur les cas communs sélectionnés du corpus examiné ; négatif = dégradation ; nul = absence d'avantage mesuré. Toujours examiner le nombre de HOLD. Une campagne sur six trajectoires synthétiques ne prouve pas que Brody comprend la gravité ou généralisera aux vrais tournages. Les modèles restent STILL / VELOCITY / ACCELERATION, 2D et programmés ; la mémoire est locale et non canonique.

**Gouvernance :** branche expérimentale, aucun accès `main`, ni mutation Native Memory, ni promotion canonique ; `KX108_ONLY`. Résultats publiés sur GitHub mais exécution PC à confirmer.
