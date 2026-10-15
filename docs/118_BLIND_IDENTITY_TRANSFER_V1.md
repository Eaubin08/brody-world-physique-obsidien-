# Brody — identité candidate : enseignement puis examen sans étiquette V1

Ce module distingue les fichiers de **cours** (chaque professeur attribue une identité candidate à plusieurs exemples) et les fichiers **d'examen** (l'identité n'est consultée qu'après le scellement de la proposition). Il regroupe sous une même identité une mémoire locale de descriptions structurelles et de signatures spatiales 4×4 de pixels sombres, et compare une observation nouvelle avec les signatures enregistrées. Le doute contient **au maximum trois identités candidates** ; en l'absence de différence probante, il ne fabrique pas une reconnaissance certaine. Les rapports, reçus chaînés, empreintes et mémoire candidate sont sauvegardés dans un nouveau dossier. Les images d'examen strictement identiques à une image de cours sont refusées (SHA256).

**Limites :** la validation d'identité est une correspondance heuristique de pixels et non une compréhension sémantique ; les fichiers sont indépendants en octets, pas nécessairement indépendants dans la réalité. Les labels de professeur sont déclaratifs et leur origine n'est pas vérifiée. Aucune découverte autonome de données, aucune consolidation automatique entre sessions, aucun entraînement neuronal ou compréhension de la physique. La stabilisation transversale avec le graphe de connaissances de l'étape 117 reste à réaliser. Pas de mutation Native Memory / KX108.

## Test sur PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_blind_identity_transfer_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

Pour une véritable campagne, créer deux JSON séparés, avec chemins absolus vers des photographies indépendantes et labels fournis par un professeur : `lessons.json` = `[{"identity":"objet-1","examples":["C:\\photos\\a.png","C:\\photos\\b.png"]}]` ; `exam.json` = `[{"file":"C:\\photos\\c.png","teacher_identity":"objet-1"}]`. Puis :

```powershell
py -m brody_world_physique.image_blind_identity_transfer_v1 --lessons "build\lessons.json" --exam "build\exam.json" --out "build\brody-identity-transfer-001"
```

Les images de cours/examen doivent être réellement différentes. Ne pas assigner artificiellement une même identité à des objets différents juste pour produire un résultat positif.
