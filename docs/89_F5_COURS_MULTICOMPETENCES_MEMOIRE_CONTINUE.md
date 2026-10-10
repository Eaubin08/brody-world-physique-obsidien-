# 89 — F5 : plusieurs compétences dans une seule histoire éducative

**Statut : CODE PUBLIÉ ; validation PC en attente.** Branche `exp/p2-multirepresentation-ablation-20261009`, main inchangée.

## Intégration réelle
Un programme `fusion_f5_multiskill_course_v0.py` utilise les interfaces F3c/F4 existantes, pas une nouvelle infrastructure mémoire :
- entraîne successivement un rectangle, un triangle et une ellipse ;
- crée trois versions immuables du registre candidat ;
- enregistre trois reçus TRAIN chaînés ;
- relit le snapshot READONLY de version 3 pour proposer la compétence **explicitement demandée** par l'IN ;
- réalise trois examens aux cibles cachées, conserve les candidats et comparaisons, puis journalise trois reçus TEST indépendants ;
- rejette par HOLD un objectif inconnu, sans ouvrir d'image TEST, et teste l'isolation des snapshots antérieurs.

Les gains par examen sont mesurés, non prédits. **ATTENTION :** la sélection par identifiant fourni n'est pas une compréhension de l'image ; ni MEMZUM ni un moteur sémantique n'est ici raccordé. F5 ne corrige pas encore une compétence après erreur, ne prouve pas l'oubli ni le modèle du monde ; les trois compétences restent des gestes supervisés. Aucune écriture Native Memory ni promotion canonique. `KX108_ONLY` inchangé.

## Commandes Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_fusion_f5*.py" -v
if ($LASTEXITCODE -ne 0) { throw "F5 tests échoués" }
py -m unittest discover -s tests -p "test_fusion_f4*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Régression F4" }
py -m brody_world_physique.fusion_f5_multiskill_course_v0 --out "build\fusion-f5-course-001"
if ($LASTEXITCODE -ne 0) { throw "Cours F5 échoué" }
Get-Content "build\fusion-f5-course-001\summary.json"
Invoke-Item "build\fusion-f5-course-001\exam-02-triangle\comparison.png"
```
En cas d'échec, conserver le dossier `-001` pour examen et choisir `-002` après correctif, ne pas effacer les traces.

## Étape suivante
Boucle corrective **TRAIN seulement** avec avant/après sur une tâche nouvelle et test différé non consulté ; conserver les versions, les échecs et la preuve causale que l'apprentissage change effectivement le résultat. Ensuite admission exacte `experience_memory_v1`, politiques MEMZUM de recherche readonly, relations V4.1/V4.2 et Reverso multi-objet. Ne pas refaire une mémoire concurrente d'Obsidia.
