# Brody P133 — Laboratoire transversal de scènes, formes, transformations, doute

La passe P133 installe le module expérimental `image_multicapability_lab_p133.py`. Elle se distingue des campagnes de trajectoires en mettant en œuvre plusieurs fonctions qualitativement différentes. C'est un banc de démonstration **déterministe** de capacités visuelles, non une IA découvrant la physique du monde.

## Fonctions exécutables

- **PERCEPTION** : objets disjoints dans une scène RGB, contours et géométrie à partir des composantes connexes sombres.
- **GÉNÉRATION** : programme 2D de rectangles, ellipses et triangles, couleurs validées, composition sous contraintes de taille et de cadre, rendu PNG.
- **INFÉRENCE AVEC DOUTE** : une disparition de composante est compatible avec une occultation, une fusion visuelle ou une disparition effective. Aucune cause n'est déclarée connue.
- **MULTIVUE 2D** : transformation en miroir, comparaison des silhouettes, correspondances descriptives sans identification sémantique certaine.
- **TRACKING DES COMPOSANTES** : appariement de deux ensembles visuels par proportions et aire ; aucune continuité temporelle ni identité physique prouvée.
- **ROBUSTESSE** : bornes des images et refus d'un programme d'image illégal.
- **RETENUE CAUSALE** : l'observation d'un changement n'autorise pas l'attribution d'une cause.

8 sondes fonctionnelles, au moins 6 familles. Elles ne sont PAS 8 entraînements : certaines vérifient des composants déterministes ou la prudence des conclusions.

## Commande PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_multicapability_lab_p133.py" -v
if ($LASTEXITCODE -ne 0) { throw "P133 tests échoués" }
py -m brody_world_physique.image_multicapability_lab_p133 --out "build\brody-multicapability-p133-001"
if ($LASTEXITCODE -ne 0) { throw "P133 campagne échouée" }
Get-Content "build\brody-multicapability-p133-001\MASTER_REPORT.json"
```

Le rapport contient PASS/FAIL de chaque sonde dans `EVIDENCE.json`; les images générées dans le dossier de sortie. Les résultats PC ne sont pas connus avant exécution.

## Limites et prochaines compétences réelles

La méthode actuelle décrit des composantes sombres. **RGB sert ici au rendu, non à l'identification robuste d'objets colorés** : jaune ou cyan peuvent être invisibles au détecteur de composantes. Un objet masqué n'est pas reconstruit, la causalité ne se déduit pas et l'appariement par taille ne donne pas d'identité. Les transformations ne créent pas de nouvelles vues 3D. Il manque le passage du programme génératif fourni à un programme **appris**, puis aux expériences avec vrais tournages, segmentation plus riche et transfert par relations à travers des objets différents.

Ne pas confondre « nouveau type de test », « nouvelle fonctionnalité déterministe » et « preuve d'apprentissage ». Documentation du backlog : `130_DIVERSITY_FIRST_80_DISTINCT_TESTS.md`.

Gouvernance intacte : expérimental, `native_memory_write=false`, `canonical_promotion=false`, `KX108_ONLY`, pas de modification de `main`.
