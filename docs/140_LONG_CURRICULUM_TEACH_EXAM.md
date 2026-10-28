# Brody — P140 : curriculum long, enseignement et examen distincts

La P138 avait réalisé 20 000 micro-scénarios en seulement 52 secondes, tous PASS, car les questions n'étaient pas discriminantes. P140 change le protocole : **l'école confronte une mémoire d'exemples à des examens sur d'autres scènes** ; chaque résultat peut être moins bon que le modèle de référence.

## Cinq problèmes visuels différents

1. **Forme :** ellipse / triangle / rectangle
2. **Couleur :** rouge / bleu / vert / violet
3. **Nombre :** un / deux / trois éléments
4. **Disposition :** horizontale / verticale / diagonale
5. **Orientation :** allongée horizontalement / verticalement / équilibrée

Les tâches sont entrelacées ; les paramètres parasites varient : position, dimensions, couleur, forme, quantité, arrangement, flou léger et bruit, sur des images 96×96. C'est une diversité utile à l'intérieur d'un corpus **synthétique procédural 2D**, et pas une simulation du monde entier.

## Apprentissage/examen

- **Cours :** avant de connaître la bonne réponse, la mémoire réalise une première prédiction ; le professeur révèle l'étiquette puis l'exemple et l'étiquette sont inscrits dans une mémoire candidate **locale**.
- **Examen :** un autre générateur pseudo-aléatoire produit une scène différente ; une prédiction est inscrite dans `EPISODES.jsonl` avant de révéler la bonne réponse. Aucune correction d'examen n'est ajoutée à la mémoire.
- **Baseline :** classe fixe par famille, sans expérience ; comparaison de l'accuracy pour chaque famille.
- **Rétention limitée :** 400 exemples au maximum par famille pour rester exécutable sur 16 Go de RAM. Il s'agit d'une mémoire de voisinage sur descripteurs RGB, pas d'un modèle neuronal indépendant.
- **Critère honnête :** un résultat en dessous de la baseline est conservé. L'examen ne prouve pas la généralisation hors du générateur.

## Commande de lancement

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull échoué" }
py -m unittest discover -s tests -p "test_image_long_curriculum_p140.py" -v
if ($LASTEXITCODE -ne 0) { throw "P140 tests échoués" }
py -m brody_world_physique.image_long_curriculum_p140 --minutes 15 --max-episodes 60000 --out "build\brody-p140-15min-001"
if ($LASTEXITCODE -ne 0) { throw "P140 exécution échouée" }
Get-Content "build\brody-p140-15min-001\MASTER_REPORT.json"
```

La durée donnée est un **budget maximum** ; l'exécution s'arrête si 60 000 épisodes sont atteints avant 15 minutes. Aucun ralentissement artificiel n'est introduit. Si la machine termine encore rapidement, la prochaine étape doit apporter des tâches et observations plus exigeantes, pas des attentes vides.

## Preuves et limites

`EPISODES.jsonl` garde les phases de cours, prévision et révélation d'examen ; `CHECKPOINT.json` résume les dix dernières époques ; `MASTER_REPORT.json` fournit accuracy avec mémoire et baseline sur cinq tâches et durées réelles.

**Ce programme est une expérience d'apprentissage limitée** : les traits visuels sont extraits par un descripteur RGB fixe et un classifieur des plus proches voisins ; les étiquettes sont créées par un générateur supervisé. Il ne sait pas identifier des objets naturels, faire du vrai 360°, découvrir seul la gravité, représenter le contexte physique, ou générer des images réalistes. Les données d'examen restent issues de la même famille de générateur, donc pas de validation du transfert réel.

**Gouvernance :** seulement branche `exp/p2-multirepresentation-ablation-20261009` ; ne pas modifier `main` ; `native_memory_write=false`, `canonical_promotion=false`, `KX108_ONLY`.
