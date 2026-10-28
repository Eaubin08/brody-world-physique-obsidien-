# Brody — P142, nouvelles représentations géométriques et transfert

## Origine expérimentale

P141, 30 000 examens, révèle une forte asymétrie : `orientation/native=0.424`, `shape/native=0.520`, et `arrangement/mirror=0.674` avec le kNN RGB. Le problème majeur n'est pas le nombre d'essais mais leur interprétation et la faiblesse du descripteur.

## Modification apportée

Un **nouveau descripteur observable** calcule les composantes connexes du premier plan, leur surface relative, leur taux de remplissage, le rapport largeur/hauteur logarithmique, leurs centres, la dispersion des centres et la couleur moyenne. Les variables sont extraites des **pixels** et non de la description d'origine donnée au générateur.

Chaque domaine sélectionne les attributs pertinents : orientation emploie le rapport largeur/hauteur ; forme emploie remplissage et géométrie ; nombre s'appuie sur les composants visibles ; disposition sur la dispersion spatiale ; couleur sur le RGB des objets visibles. Il s'agit d'un inductive bias codé, non d'une découverte autonome de représentation.

L'expérience compare trois modèles : l'ancien `rgb_knn` de P140, le `geometric` fondé sur centroïdes d'exemples, et la baseline `majority`. Même matrice que P141 : **5 domaines × 6 transformations = 30 conditions** (native, miroir, niveaux de gris, posterize, flou, contraste). De nouvelles graines de cours/examen sont utilisées ; aucun examen de P141 n'est réutilisé directement.

Une exception non négociable : **la couleur sur une image en niveaux de gris** déclenche `HOLD/DESTROYED_CHROMATIC_INFORMATION` pour le nouveau prédicteur. Le rapport indique **à la fois précision conditionnelle et couverture**. Un modèle qui abstient partout n'est donc jamais présenté comme un modèle meilleur.

## Validation et exécution PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_geometric_transfer_p142.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P142 échoués" }
py -m brody_world_physique.image_geometric_transfer_p142 --minutes 15 --train-per-family 300 --exam-per-cell 1000 --out "build\brody-p142-geometric-001"
if ($LASTEXITCODE -ne 0) { throw "P142 échouée" }
Get-Content "build\brody-p142-geometric-001\MASTER_REPORT.json"
```

Pour lire les 30 comparaisons détaillées :

```powershell
$r = Get-Content "build\brody-p142-geometric-001\CELL_REPORT.json" -Raw | ConvertFrom-Json
$r.PSObject.Properties | ForEach-Object {
 [PSCustomObject]@{Condition=$_.Name;Examens=$_.Value.n;RGB=$_.Value.rgb_knn.accuracy_attempted;Geometrie=$_.Value.geometric.accuracy_attempted;Couverture=$_.Value.geometric.coverage;Majorite=$_.Value.majority.accuracy_attempted}
} | Format-Table -AutoSize
```

## Réserves

Les examens restent des mondes artificiels 2D dérivés de la même famille de générateur ; l'augmentation de score éventuelle ne prouvera pas la reconnaissance générale d'images. Le filtrage du premier plan par seuil peut rompre les composantes après perturbation ; les familles d'images très encombrées ou d'arrière-plan réel ne sont pas traitées. Le descripteur géométrique est conçu par un développeur et le calcul de centroïdes n'est pas une acquisition autonome d'invariants.

Aucun score n'est proclamé avant les mesures sur PC. Gouvernance : branche expérimentale uniquement, `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
