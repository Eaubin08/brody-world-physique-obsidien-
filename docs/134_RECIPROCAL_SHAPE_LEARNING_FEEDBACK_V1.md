# P134 — Réciprocité perception ↔ génération ↔ correction, mémoire de formes

Cette passe met en place une boucle de correction visuelle : **image de cours → décomposition en composantes RGB → génération initiale grossière (rectangles) → comparaison à l'image du professeur → correction par masque observé → conservation d'exemples géométriques → génération sur images d'examen inconnues**. Les examens ne mettent jamais la mémoire à jour.

## Capacités différentes testées

1. Perception de composantes RGB sous seuil de luminosité ; position, couleur moyenne, masque, aire et proportions.
2. Génération d'une reconstruction grossière par rectangles, avant correction.
3. Comparaison du rendu à l'original : écart absolu RGB par pixel et ratio de pixels identiques.
4. Correction locale : remplacer le rectangle par le masque de la composante observée (enseignée). C'est une **copie structurée de l'image de cours**, pas une découverte autonome.
5. Consolidation de formes candidates avec origine de chaque groupe.
6. Nouvelle scène : proposition à partir de formes mémorisées de **deux groupes distincts**, à géométrie équivalente ; sinon HOLD.
7. Mise à l'épreuve de formes nouvelles et de contre-exemples : le HOLD doit être compté.
8. Intégrité des partitions : images d'examens exactement identiques aux cours refusées, et groupes disjoints.

**Important :** la position, l'enveloppe, la couleur et la segmentation de l'objet de l'examen sont actuellement observées directement pendant la prévision. La génération transfère essentiellement les **masques mémorisés**. Ce protocole **ne démontre donc pas une génération depuis une simple description, une identité d'objet autonome ni un vrai apprentissage sémantique**. L'entraînement est explicitement supervisé et les sources sont déclarées, pas authentifiées. Les objets qui se touchent sont fusionnés par segmentation ; les couleurs claires restent difficiles.

## Manifeste utilisateur

Créer un tableau JSON comportant plusieurs fichiers PNG/JPEG avec `group` (prise de vue distincte), `split` (`train` ou `exam`) et `file` (chemin du fichier). Exemple :

```json
[
 {"group":"prise-01","split":"train","file":"build/enseignements/cercle-a.png"},
 {"group":"prise-02","split":"train","file":"build/enseignements/cercle-b.png"},
 {"group":"prise-03","split":"exam","file":"build/examens/cercle-c.png"}
]
```

## Commande PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull échoué" }
py -m unittest discover -s tests -p "test_image_reciprocal_shape_learning_p134.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P134 échoués" }
```

Le test crée ses propres scènes de cours et d'examen et mesure les erreurs. Pour un vrai corpus disponible sur PC :

```powershell
py -m brody_world_physique.image_reciprocal_shape_learning_p134 --manifest "build\\manifest-p134.json" --out "build\\brody-p134-real-001"
```

Artefacts : `MASTER_REPORT.json`, `candidate_shape_memory.json`, `train_*_initial.png`, `train_*_corrected.png` et `heldout_*.png` pour candidats seulement.

## Interprétation

Un faible écart sur cours corrigé n'est pas une mesure de transfert. Seules les images d'examen séparées et réellement indépendantes permettront de juger le transfert de forme ; les résultats doivent aussi indiquer les HOLD et les fausses ressemblances. Comparer ultérieurement contre un transfert à mémoire vide et contre des modèles de formes génériques, sans fuite géométrique involontaire.

**Gouvernance :** expérimental uniquement, `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`. Aucun changement au noyau souverain.
