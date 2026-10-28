# P141 — Examen de transfert visuel : 30 conditions réellement différenciées

## Pourquoi

P140 a montré sur 30 000 examens synthétiques que l'accuracy augmente avec une mémoire de références, mais deux tâches restent fragiles : **forme** (52,63 %) et **orientation** (43,50 %). Le comparateur sans apprentissage de P140 était une classe constante, trop facile à battre. P141 éprouve le modèle sur des images perturbées jamais vues, en comparant trois prédicteurs (kNN de P140, centroïde des classes, classe majoritaire observée), et surtout en séparant le résultat **par famille ET par perturbation**.

## Matrice d'examen

5 questions (forme, couleur, nombre, disposition, orientation) × 6 conditions = 30 cellules :
- image native (contrôle) ;
- miroir horizontal (modification des pixels, étiquette inchangée pour les cinq questions) ;
- niveaux de gris (supprime l'information de couleur, un échec couleur est attendu et constitue une limite réelle) ;
- quantification des canaux RGB (posterize) ;
- flou supplémentaire ;
- changement de contraste.

Chaque cellule reçoit son propre lot d'examens et son score. L'étiquette générée n'entre ni dans l'extraction de caractéristiques ni dans les prédictions. **Les examens ne réentraîneront aucun des modèles**. Le cours et les examens ont des flux aléatoires séparés mais appartiennent toujours au même générateur de scènes : les sources ne sont donc pas réellement indépendantes.

## Exécution sur PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_transfer_stress_p141.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P141 échoués" }
py -m brody_world_physique.image_transfer_stress_p141 --minutes 15 --train-per-family 300 --exam-per-cell 1000 --out "build\brody-p141-transfer-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P141 interrompue" }
Get-Content "build\brody-p141-transfer-001\MASTER_REPORT.json"
```

Le programme s'arrête quand **le budget temporel ou le nombre de cases prévues est atteint** ; il ne ralentit jamais artificiellement. `CELL_REPORT.json` est indispensable : ne pas conclure à partir de la seule accuracy globale. `EXAMS.jsonl` permet de contrôler une entrée par décision et de comparer les trois prédicteurs.

**Prochaines extensions** : générateurs de formes indépendants, contexte occlus et provenance d'images réelles, groupes temporels, vraie mémoire qui modifie sa représentation après correction, intervention physique. Le moteur actuel n'établit ni une compréhension 3D, ni une capacité de physique générale, ni un transfert au monde réel. Les 30 cellules sont 30 **conditions d'évaluation**, non 30 compétences apprises.

**Gouvernance** : branche expérimentale, `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
