# Brody — P143 : router de représentations, sélection gelée AVANT l'examen

## Motivation

P142 prouve que géométrie et mémoire RGB ont des forces complémentaires, avec des régressions nettes selon les domaines. Il serait trompeur de choisir après l'examen la meilleure représentation dans chaque cellule : cela exploiterait les réponses. P143 crée **trois flux distincts** de données synthétiques :

1. Cours : entraîne uniquement les mémoires RGB et géométriques ;
2. Validation : compare les trois méthodes dans 30 conditions, choisit un modèle **par domaine × transformation** ; la récompense est le nombre de réponses correctes sur toutes les questions, et non seulement parmi celles où la méthode répond ;
3. Examen inédit : utilise le router figé et calcule ses erreurs, sa couverture et la performance des trois comparateurs ; les réponses d'examen ne servent jamais à choisir la méthode.

Le router et les statistiques de validation sont sauvegardés dans `FROZEN_ROUTER.json` **avant toute génération d'examen**. La règle d'abstention en couleur/niveaux de gris est explicite et fixée par contrat, pas découverte automatiquement. Le router connaît ici le nom de la transformation : ce n'est PAS une inférence autonome de la dégradation.

## Exécution PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_validation_router_p143.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P143 échoués" }
py -m brody_world_physique.image_validation_router_p143 --minutes 15 --train-per-family 300 --validation-per-cell 120 --exam-per-cell 1000 --out "build\brody-p143-router-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P143 échouée" }
Get-Content "build\brody-p143-router-001\MASTER_REPORT.json"
```

## Résultats attendus

`FROZEN_ROUTER.json` contient le choix gelé par condition et la preuve de séparation logique. `EXAM_DECISIONS.jsonl` conserve chaque réponse et toutes les alternatives. `CELL_REPORT.json` donne les scores par condition, refus et régressions ; `MASTER_REPORT.json` donne scores globaux et couverture.

Aucun score PASS préjugé. Les trois flux sont issus de la **même famille de générateur artificiel** malgré des graines différentes. Les labels des transformations sont fournis au router. Une sélection de modèles figée peut encore surapprendre les validations et doit être testée sur plusieurs nouvelles graines. Les failles de forme, d'occlusion et de physique réelle restent ouvertes.

**Gouvernance inchangée :** branche expérimentale, `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
