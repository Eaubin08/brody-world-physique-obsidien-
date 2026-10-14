# P156 — Éducation séquentielle, mémoire cumulative et contrôle d'oubli

## Objectif
P155 a validé un mécanisme qui accepte ou refuse une correction sur un examen de validation indépendant : 6 ACCEPT, 18 HOLD, 15 régressions d'examen évitées sur 24 conditions et 1 920 examens. P156 teste maintenant si ce principe fonctionne lors de **24 leçons consécutives**, où une modification de la connaissance courante peut détériorer les sujets déjà étudiés.

## Expérience
Quatre familles de mouvement et six rendus visuels, dans un ordre de curriculum fixe. Pour chaque famille une règle initiale est estimée depuis les pixels puis figée. À chaque leçon, une nouvelle proposition de décalage cumulatif est estimée sur un jeu de feedback ; elle est évaluée sur un lot de validation propre à la tâche et sur les validations antérieures de la même famille conservées dans le replay bank. ACCEPT exige un gain significatif sur la tâche et aucune perte dépassant 0,035 pixel d'erreur absolue moyenne sur une ancienne tâche. HOLD laisse la mémoire gouvernée inchangée. Un témoin ungated accumule toutes les propositions.

**Important :** le rejeu est un jeu de validation, pas une mémoire sémantique universelle. Les corrections sont de simples scalaires par famille, pas des lois physiques auto-découvertes. Le protocole ne mesure pas les interactions entre familles et ne prétend pas garantir un non-oubli complet. L'ordre est fixe et le candidat est calculé depuis le modèle gouverné courant, non le témoin ; cela définit le témoin ungated, sans prétendre être une trajectoire indépendante optimale.

Un examen final entièrement séparé note les 24 conditions sur les mêmes séquences avec trois variantes : règle initiale figée, corrections systématiques cumulées, corrections gouvernées cumulées. Le critère d'acceptation n'utilise pas les examens.

## Commande unique PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_cumulative_education_p156.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P156 échoués" }
py -m brody_world_physique.image_cumulative_education_p156 --minutes 20 --lessons-each 24 --feedback-each 24 --validation-each 24 --exam-each 50 --out "build\brody-p156-cumulative-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P156 échouée" }
Get-Content "build\brody-p156-cumulative-001\MASTER_REPORT.json"
```

Preuves : `FROZEN_BASE.json`, `CYCLES.jsonl`, `FINAL_EXAM.jsonl`, `MASTER_REPORT.json`. Le répertoire existant est préservé, aucun écrasement.

Lecture scientifique : `cycles_completed==24` et `exam_cases==1200` sont des contrôles d'exécution, non de performance ; juger les trois moyennes d'erreur, les ACCEPT/HOLD et les variations par tâche. Un gain moyen ne prouve pas que chaque connaissance a été conservée.

Gouvernance : branche expérimentale exclusivement ; `decision_authority=KX108_ONLY`; `native_memory_write=false`; `canonical_promotion=false`.
