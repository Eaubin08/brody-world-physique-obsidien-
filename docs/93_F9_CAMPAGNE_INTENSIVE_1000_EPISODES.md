# F9 — Campagne intensive de 1 000 épisodes (candidate only)

**Publication de code, pas de résultat.** Branche `exp/p2-multirepresentation-ablation-20261009`. Main inchangée.

## Contrat expérimental
- 1 000 expériences TRAIN reproductibles par seed, quatre familles de géométries (ligne, angle, zigzag, rectangle), trois intentions de style (LIGHT, UNIFORM, EXPRESSIVE) et trois outils simulés hérités de V2 (PENCIL, PEN, NIB).
- Politique candidate de sélection instrumentale fondée sur les erreurs TRAIN des trois outils. L'état reste versionné à chaque checkpoint, sans état canonique. Mise à jour exponentiellement pondérée (facteur de mémoire 0,75), qui permet une réorientation sur de nouvelles observations.
- Dans la deuxième moitié du TRAIN, le professeur change sa préférence pour le contexte LIGHT|line. La campagne comptabilise les expériences contradictoires et les changements effectifs de politique (`policy_changes_on_train`). Un changement n'est **pas** garanti par l'intitulé du test.
- Examen tenu à l'écart à chaque 100 épisodes : même jeu de 48 contextes géométriques déterministes à chaque étape. La politique et l'image candidate sont fixées avant création de la cible. Aucune erreur TEST ne met à jour TRAIN.
- Contrôle anti-oubli : différence d'erreur par contexte et par checkpoint contre la première évaluation disponible ; **une dégradation n'est pas bloquée automatiquement** mais apparaît dans `max_forgetting_delta`. Le benchmark reflète l'ancien régime de style et peut donc entrer en conflit avec la nouvelle préférence TRAIN : ce conflit est une mesure voulue, non un signe de généralisation.
- Reçus TRAIN chaînés SHA256 (un par épisode), détecteur de modification, snapshots immuables écrits dans un dossier neuf ; journal des évaluations et synthèse finale.
- `native_memory_write=false`, `canonical_promotion=false`, `KX108_ONLY`.

## Limites importantes
L'apprentissage F9 porte sur **la politique instrumentale empirique**, pas sur la correction des gestes ou la reconnaissance d'objets depuis des images naturelles. La famille de styles et le moteur de rendu de la cible sont synthétiques et communs au professeur et à l'élève. Les variations de formes changent les gestes fournis au moteur mais ne sont pas perçues ou reconstruites de manière autonome. Ce prototype a sa propre table candidate de routage, **pas l'intégration aboutie du registre F3c/F5 ni de Native Memory**. Une courbe favorable ne prouvera pas une compréhension du monde.

## Lancement Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f9_intensive_education_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F9 invalide" }
py -m unittest discover -s tests -p "test_fusion_f9*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F9 échoués" }
py -m brody_world_physique.fusion_f9_intensive_education_v0 --episodes 1000 --checkpoint 100 --out "build\fusion-f9-1000-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne échouée" }
Get-Content "build\fusion-f9-1000-001\summary.json"
```
Si la campagne échoue, ne pas écraser ses données : relancer dans un dossier `-002` après correction.

## Validation avant ambition supplémentaire
Le prochain travail consistera à rapprocher ces reçus de `experience_memory_v1` et à utiliser des géométries TEST réellement indépendantes des moteurs éducateurs, puis à entraîner les gestes eux-mêmes et pas seulement la préférence d'outil. Les résultats F8 13/13 restent une référence distincte ; F9 n'a pas été exécuté dans ces résultats.
