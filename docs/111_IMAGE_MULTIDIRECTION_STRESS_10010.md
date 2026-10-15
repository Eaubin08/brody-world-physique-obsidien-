# École Brody — campagne de stress multidirectionnelle (>10 000 cas)

Ce module attaque l'école visuelle à partir des 63 images archivées déjà présentes sur PC. Au lieu d'évaluer encore un trio d'outils dans un seul scénario, il varie les sources et combine 14 agressions visuelles : rotation libre, miroir, échelle, translation, flou, contraste, bruit, occultation, inversion, recadrage, transformations composées, perte partielle, fond modifié, entrée sans tracé stable. Les 14 familles sont équilibrées, mélangées, et leurs catégories ne sont pas communiquées au traceur.

**Protocole réel** : 10 010 cas (715 par famille) ; chaque cas conserve un reçu, l'empreinte de source et de sortie, les erreurs du tracé et de la toile blanche, les HOLD et la proportion des dessins supérieurs à la toile blanche. Les catégories/transformations sont des données de l'examinateur. Les cas peuvent échouer ; aucune correction oracle ne garantit le zéro. Le traceur reste le moteur générique Brody en 64×64 et l'outil PEN fixe.

**Lacunes assumées** : 14 attaques sur images n'équivalent pas à 14 capacités cognitives validées ; le référent est visible lors du tracé et aucune représentation 3D, causalité, génération libre ou apprentissage inter-épisodes n'est prouvé par ce module. L'exécution longue peut prendre du temps sur CPU : commencer avec 140 cas pour mesurer le débit, puis passer à 10 010. Les images archivées ne sont pas des preuves indépendantes de capture réelle. Pas de modification du noyau, de main ni de Native Memory.

## Exécuter d'abord un pilote 140 cas, puis la campagne complète

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_multidirection_stress_10k_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
py -m brody_world_physique.image_multidirection_stress_10k_v0 --images "build\brody-images-ready" --cases 140 --out "build\brody-multiaxis-pilot-140-001"
if ($LASTEXITCODE -ne 0) { throw "Pilote échoué" }
py -m brody_world_physique.image_multidirection_stress_10k_v0 --images "build\brody-images-ready" --cases 10010 --out "build\brody-multiaxis-stress-10010-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne échouée" }
Get-Content "build\brody-multiaxis-stress-10010-001\MASTER_REPORT.json"
```

La suite scientifique doit utiliser les résultats les plus faibles pour concevoir une école visuelle avec suivi d'objet, mémoire temporelle, inférence de transformation et sources de perception réellement indépendantes : ne pas assimiler un bon score de tracé au monde physique.
