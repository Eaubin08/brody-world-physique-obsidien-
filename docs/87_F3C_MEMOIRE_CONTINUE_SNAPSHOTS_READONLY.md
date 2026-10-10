# 87 — F3c : réparer la rupture de mémoire continue

## Pourquoi reprendre F3b
Le moteur F3b créait une nouvelle `memory.json` indépendante à chaque leçon. Il vérifiait cinq transferts, pas un apprentissage cumulatif. C'était contraire à la trajectoire éducative recherchée et aux couches historiques déjà existantes : `experience_memory_v1`, `drawing_memory_school_v3`, `p211b_frozen_gesture_transfer_v0`.

## Contrats confirmés
`experience_memory_v1` implémente des épisodes, le rejeu d'exécutions, des empreintes, `finalize_index` et `verify_memory_bundle` ; ce schéma est un **export expérimental read-only**, non un droit général d'écriture en mémoire native. V3 contient le rappel masqué. P2.11b contient la lecture vérifiée d'une mémoire candidate et P2.11c la recomposition sans voir le professeur. Une mémoire **continue** doit accumuler des expériences sous contrôle, puis publier des snapshots vérifiés que les consommateurs lisent seulement.

## F3c — premier pont effectif
`fusion_f3c_cumulative_skill_archive_v0.py` enregistre une compétence candidate TRAIN une seule fois dans `skills/rectangle.json`, avec `versions/v001.json`. Le registre est versionné, contient les SHA256, contrôle chaque mémoire via `p211b.read`, refuse les altérations et accepte un append-only strict si l'on ajoute de nouvelles compétences. Le candidat mémorisé sert **à trois examens ultérieurs** de tailles, nombres et dispositions différents, sans nouvel entraînement. Images réelles `candidate.png`, `comparison.png`, reçu `exam.json` et bilan `summary.json`. Aucune lecture de fichier TEST avant scellement du candidat. Le TEST est uniquement utilisé pour noter.

**Limite fondamentale :** cette démonstration réutilise effectivement un acquis antérieur ; elle n'apprend pas encore après un échec, ne choisit pas de façon autonome parmi plusieurs savoir-faire, n'accumule qu'une compétence pendant la démo, et n'est pas encore branchée comme writer autorisé à la Native Memory d'Obsidia. Il serait faux de prétendre que toutes les couches de mémoire existantes sont d'ores et déjà fusionnées. Les versions historiques demeurent utilisables mais non mutées.

## Commandes Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_fusion_f3c*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Échec F3c" }
py -m brody_world_physique.fusion_f3c_cumulative_skill_archive_v0 --demo --out "build\fusion-f3c-cumulative-001"
if ($LASTEXITCODE -ne 0) { throw "Démo F3c échouée" }
Get-Content "build\fusion-f3c-cumulative-001\summary.json"
Invoke-Item "build\fusion-f3c-cumulative-001\03-transfer\comparison.png"
```

## Fermeture architecturale restante
Adapter ce registre expérimental au format et au validateur exacts de `experience_memory_v1` en conservant sa traçabilité. Faire consommer à l'élève plusieurs skills de générations antérieures, avec sélection justifiée **sur TRAIN uniquement**, HOLD sur inconnu, gestion de l'oubli, versions comparées et examen caché. Examiner ensuite l'assemblage de composants hétérogènes avec relations V4.1/V4.2 et génération dans une scène. Ne pas autoriser B8, Native Memory write ou Kernel mutation à travers une démo.
