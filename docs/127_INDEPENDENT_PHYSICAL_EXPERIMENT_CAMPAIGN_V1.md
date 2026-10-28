# Brody — Passe 127 : campagne complète d'expériences indépendantes

## Objectif

**Arrêter d'interpréter des tests unitaires réussis comme une preuve d'apprentissage physique réel.** La présente passe livre une campagne réellement exécutable à partir de séquences d'images, organisée en deux partitions imperméables par source : cours et examen. Un seul appel orchestre les corrections des cours, la mémoire résultante et la comparaison à mémoire figée sur les examens. Le script ne fournit PAS d'images réelles : elles doivent venir de vidéos/caméras effectivement différentes, avec leur provenance.

### Contrat de provenance

Fichier JSON `build\\brody-campaign-127.json` : liste d'épisodes. Chacun contient :
- `source_group` : identifiant unique du tournage ou de la scène ; toutes les séquences issues de ce tournage doivent rester dans **une seule** partition ;
- `origin` : `camera`, `video`, `synthetic` ou `unknown` ; information déclarative, non authentifiée ;
- `split` : `train` ou `exam` ;
- `observations` : au moins quatre images avec temps croissants ;
- `predict_t` : temps de l'image suivante ;
- `actual` : image observée à ce temps.

Exemple :

```json
[
 {"source_group":"tournage-A","origin":"camera","split":"train",
  "observations":[{"t":0,"file":"build/A/0.png"},{"t":1,"file":"build/A/1.png"},{"t":2,"file":"build/A/2.png"},{"t":3,"file":"build/A/3.png"}],
  "predict_t":4,"actual":"build/A/4.png"},
 {"source_group":"tournage-B","origin":"camera","split":"train",
  "observations":[{"t":0,"file":"build/B/0.png"},{"t":1,"file":"build/B/1.png"},{"t":2,"file":"build/B/2.png"},{"t":3,"file":"build/B/3.png"}],
  "predict_t":4,"actual":"build/B/4.png"},
 {"source_group":"tournage-C","origin":"camera","split":"exam",
  "observations":[{"t":0,"file":"build/C/0.png"},{"t":1,"file":"build/C/1.png"},{"t":2,"file":"build/C/2.png"},{"t":3,"file":"build/C/3.png"}],
  "predict_t":4,"actual":"build/C/4.png"}
]
```

**Ne pas transformer un seul tournage par miroir/rotation en plusieurs tournages indépendants.** Les fichiers identiques d'une partition à l'autre et les groupes répartis entre partitions sont refusés. La vérification de provenance est structurelle : les métadonnées sont déclaratives, une image légèrement modifiée d'un même enregistrement peut échapper à la vérification SHA.

## Exécution

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_motion_independent_campaign_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

Après constitution du corpus, une seule commande effectue **la campagne entière** :

```powershell
py -m brody_world_physique.image_motion_independent_campaign_v1 --manifest "build\brody-campaign-127.json" --out "build\brody-campaign-127-results"
Get-Content "build\brody-campaign-127-results\MASTER_REPORT.json"
Get-Content "build\brody-campaign-127-results\heldout_ablation\MASTER_REPORT.json"
```

## Résultats à lire

`split/MASTER_REPORT.json` : provenance déclarée et séparation des groupes ;
`train_forecast_*/`, `train_feedback_*/` : cours, réponses scellées, corrections et mémoire candidate ;
`heldout_ablation/MASTER_REPORT.json` : erreurs A/B de la mémoire activée/désactivée sur les cas d'examen, HOLD et écart moyen sur cas appariés ;
`heldout_ablation/EVIDENCE.json` : détail de chaque expérience de test.

**Un delta positif ne constitue pas automatiquement une preuve universelle.** La méthode ne sait suivre qu'un objet sombre sur fond clair en 2D, le groupement de tournages n'est pas validé indépendamment, et les trois familles physiques sont programmées. Il faut plusieurs tournages différents et des contre-exemples, sinon les résultats restent exploratoires.

**Gouvernance** : branche expérimentale seulement ; Native Memory et promotion canonique interdits, autorité `KX108_ONLY`. Aucun changement au noyau souverain.
