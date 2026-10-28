# P146 — Adaptation aux fonds nouveaux sans oubli du monde initial

## Diagnostic issu de P145

Le nouveau moteur de rendu a exposé des failles reproductibles : référence 89,34 %, clair 85,72 %, sombre 26,88 %, occlusion 58,52 %. Les tests de détail montrent que la reconnaissance des formes ne dépasse pas 59,5 % même dans le monde de référence, et que l'orientation occultée tombe à 31,5 %.

## Ce qui est effectivement implémenté

Deux mécanismes expérimentaux séparables :

1. **Descripteur relatif au fond** : estime la couleur du fond aux coins, isole les pixels qui s'en distinguent, puis mesure les composantes connexes, leurs proportions, positions, dispersions et couleurs moyennes. Il n'utilise pas une hypothèse de fond toujours blanc. Il peut échouer si les coins sont occupés, si les objets et le fond ont des couleurs proches, ou en présence d'ombres et de textures.
2. **Adaptation supervisée de quelques exemples** : la représentation `robust_before` est instruite seulement sur les scènes originales ; `adapted` reçoit quelques scènes étiquetées de chaque monde nouveau. L'examen utilise de nouvelles graines et ne réinjecte aucun résultat dans la mémoire. Le vieux monde `reference` est lui aussi réévalué après adaptation pour quantifier l'oubli éventuel.

Il existe également un comparateur `p144` : sa représentation géométrique, mais **pas son sélecteur complet** ; il est nommé ainsi seulement pour indiquer la filiation. Il ne faudrait pas assimiler sa précision à la précision complète de P144/P145.

Les 25 conditions de P145 sont conservées : 5 questions × 5 mondes. **Occlusion explicative, restauration de partie invisible et calibration du HOLD ne sont pas implémentées** dans cette passe : les scènes occultées servent à quantifier les limites, non à proclamer une capacité de reconstruction.

## Lancement PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_background_adaptation_p146.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P146 échoués" }
py -m brody_world_physique.image_background_adaptation_p146 --minutes 15 --train-each 300 --adapt-each 60 --exam-each 600 --out "build\brody-p146-adapt-001"
if ($LASTEXITCODE -ne 0) { throw "P146 échouée" }
Get-Content "build\brody-p146-adapt-001\MASTER_REPORT.json"
```

L'expérience vise 15 000 examens (25 × 600), et s'arrête au nombre maximal ou au budget temporel. Les métriques distinguent ancienne géométrie, nouveau détecteur sans adaptation et nouvelle mémoire adaptée. Le score de référence après adaptation doit être examiné : un gain dans le monde sombre ne justifie pas une forte perte ailleurs.

**Limites :** scènes 2D procédurales ; le fait qu'un enseignant donne les étiquettes des nouveaux mondes signifie qu'il s'agit d'adaptation supervisée, pas de découverte autonome. Pas de source naturelle indépendante, pas de physique réelle ni de compréhension d'occlusion prouvée. Les résultats sur PC restent à valider.

**Gouvernance :** branche expérimentale uniquement, `native_memory_write=false`, `canonical_promotion=false`, `KX108_ONLY`.
