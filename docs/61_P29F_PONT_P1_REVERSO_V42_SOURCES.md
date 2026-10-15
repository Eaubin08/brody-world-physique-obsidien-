# 61 — P2.9f : pont de preuves originales P1/Reverso et V4.2

**État : code/tests publiés, tests PC et pont complet pas encore exécutés.**

## Ce que fait le code
`p29f_original_organs_bridge_v0.py` appelle directement `multirepresentation_ball_bridge_v5.verify` et `world_orientation_school_v4_2.verify` avec **leurs véritables sources ancestrales**, avant de lire leurs rapports. Il rejette tout rejeu en échec, les quatre vues P1 manquantes, les sources non synthétiques et les droits de mutation. Le reçu résultant relie les deux preuves par hash, sans prétendre qu'elles concernent le même objet ou une même observation. Les quatre vues P1 (RASTER, SPATIAL, TEMPORAL, MOTION) et les résultats Reverso sont relus; V4.2 apporte ses anciens scores et la déclaration de réciprocité 2D.

**Limite :** ce pont ne fait aucune prédiction nouvelle ni apprentissage; il démontre uniquement que le code des organes déjà existants peut être recontrôlé et rapproché sans écraser les frontières. `source_count_as_one_experiment=false` et `same_scene_cross_modal_inference=false` interdisent l'interprétation fausse. Les composants n'ont pas été forcés à partager des référentiels artificiels.

## Validation rapide PC fixe
```powershell
$repo = "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
Set-Location $repo
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p29f*.py" -v
if ($LASTEXITCODE -ne 0) { throw "P2.9f tests échoués" }
```

## Rejeu complet facultatif — uniquement si les dossiers originaux sont disponibles
- `--suite` : ancien `suite.json` P1
- `--forecasts` : `forecasts_precommitted.jsonl` correspondant
- `--preview` : dossier des images/reçu Reverso du même P1
- `--p1-out` : dossier du pont P1 avec evaluation.json et 4 images
- `--v42-out` : dossier original V4.2
- `--v3`, `--v4`, `--v41` : les trois ancêtres exacts de V4.2
- `--out` : fichier JSON de jointure **nouveau**, puis `--verify` pour rejouer

**Ne pas improviser les chemins** : un dossier ancien peut manquer, avoir changé ou provenir d'un autre PC. Le pont doit répondre FAIL si la traçabilité originale n'est plus vérifiable.

## Suite opérationnelle
Construire ensuite un **seul banc sur la même vidéo sourcée** : rendre les observations temporelles P1 compatibles avec des relations V4.2 pertinentes, avec comparaison séparée des transformations de point de vue et des hypothèses de mouvement. P2.9f est un préalable de provenance, pas la démonstration déjà obtenue de cette fusion. La génération visuelle reste du côté Reverso et la décision reste `KX108_ONLY`.
