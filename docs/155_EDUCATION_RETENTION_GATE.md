# P155 — Porte de validation avant conservation des acquis

## Problème issu de P154
La boucle P154 est exécutée, mais certaines corrections détériorent l'examen indépendant, notamment l'accélération avec occultation (2,149 → 2,496 px). Une correction proposée ne doit donc plus être appliquée automatiquement.

## Contrat expérimental
Quatre ensembles **distincts et reproductibles** : apprentissage initial des paramètres depuis les pixels ; propositions d'ajustements résiduels depuis un cours correctif ; validation de la proposition (gain obligatoire sur la condition, non-régression sur un lot de référence `clean`) ; examen aveugle effectué après verrouillage ACCEPT/HOLD. Les 24 couples mouvement/environnement sont évalués. Le comparateur « correction toujours appliquée » est noté en parallèle du modèle gelé et du modèle gouverné. Aucune rétroaction d'examen n'intervient dans le choix.

**Décisions** : `ACCEPT_VALIDATED_CORRECTION`, `HOLD_NO_VALIDATED_GAIN`, `HOLD_RETENTION_REGRESSION`, `HOLD_INSUFFICIENT_VISIBILITY`.

**Limites scientifiques** : la rétention vérifie seulement le monde `clean` de la même famille ; elle ne garantit pas l'absence d'oubli sur toutes les anciennes compétences. Les simulateurs, les familles de lois, les paramètres de l'algorithme et les jeux de critères sont conçus par programmation. Ce n'est pas un apprentissage autonome global, ni une preuve de compréhension physique réelle. Les paramètres appris sont des artefacts d'une campagne locale, pas des écritures mémoire native Obsidia.

## Campagne unique Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_education_retention_gate_p155.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P155 échoués" }
py -m brody_world_physique.image_education_retention_gate_p155 --minutes 20 --lessons-each 32 --feedback-each 24 --validation-each 32 --exam-each 80 --out "build\brody-p155-retention-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P155 échouée" }
Get-Content "build\brody-p155-retention-001\MASTER_REPORT.json"
```

En cas de temps insuffisant, `stopped_by=TIME_BUDGET` et `exam_cells_completed` signalent la couverture. Les preuves ne sont jamais écrasées. Trois perspectives : correction systématique, aucune correction, et correction validée. Le verdict doit comparer les MAE **d'examen aveugle** et le nombre de régressions évitées.

Gouvernance : `decision_authority=KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
