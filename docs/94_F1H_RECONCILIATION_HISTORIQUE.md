# 94 — F1H : réutilisation réelle des modules historiques P149, P150 et P152

## Module exact retrouvé
- `brody_world_physique/image_multiangle_temporal_p149.py` : `paired_counterfactual()`, `experiment(rng,kind)`. Observe les images, conserve des historiques incompatibles avec un même instant final. Limite : voies détectées fixées dans `observed`.
- `brody_world_physique/image_tracking_beam_p150.py` : `build(rng,scenario)`, `infer(frames)`. Recalage caméra par repères visibles et suivi d'objets; pas d'identités oracle exposées au moteur.
- `brody_world_physique/image_identity_beam_p152.py` : `beam_predict(frames)`. Maintien de plusieurs hypothèses d'identité au cours des frames, possibilité de HOLD.

Ces noms et signatures sont relevés dans les fichiers du dépôt, sur `exp/p2-multirepresentation-ablation-20261009`, pas déduits des mails.

## Ce qui est codé
`f1h_historical_reconciliation_v1.py` importe les **vraies fonctions** des trois modules, appelle 12 épisodes synthétiques dans une seule campagne, confronte les prédictions à la vérité du simulateur seulement après inférence et conserve les résultats dans un rapport. Le test vérifie également le contre-factuel P149 « même image finale, histoires différentes ». Aucune réécriture de leurs algorithmes.

## Ce qui reste HOLD
C'est une **réconciliation par exécution**, pas encore une représentation pédagogique partagée. La mémoire expérimentale F1C/F1F n'a pas été reliée à l'identité suivie par P152; le modèle du monde SENS/MMonde n'a pas été raccordé. On ne revendique ni compréhension 3D, ni apprentissage causal autonome, ni génération réciproque.

## Commandes PowerShell
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_f1h_historical_reconciliation_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.f1h_historical_reconciliation_v1 --out "build/f1h-historical-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/f1h-historical-v1/MASTER_REPORT.json"
```
Le dossier de sortie doit être inexistant. Tests PC non encore exécutés. `KX108_ONLY`; `NATIVE_MEMORY_WRITE=FALSE`; `CANONICAL_PROMOTION=FALSE`.

## Étapes restantes
1. Tests F1H et analyse des HOLD / erreurs par origine.
2. Définir un contrat d'échange d'observation (temps, caméra, identités candidates, provenance, incertitude) en réutilisant F12/MMonde.
3. École F1I : indice de contact effectivement observable, générateur avec/sans collision et paires négatives.
4. École F1J : boucle perception ⇄ génération et vérification des invariants.
5. École F1K : compétences cumulatives, transfert et rétention.
6. F1L : séquences réelles et audits interbranches.
