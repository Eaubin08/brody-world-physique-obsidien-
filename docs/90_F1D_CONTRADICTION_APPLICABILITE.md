# 90 — Contradiction, applicabilité et préservation des compétences (F1D)

**Mode : candidat expérimental, branche `exp/p2-multirepresentation-ablation-20261009`.** Le code de l'expérience antérieure reste inchangé et tous ses résultats sont conservés.

## Origine mesurée
Le protocole expérientiel V1 a mesuré deux gains (+1 px) et une dégradation (-1 px) sur trois examens synthétiques. Le mauvais transfert provenait du même contexte apparent de quatre images de mouvement accéléré, suivi d'une inversion non observable au moment de prédire.

## Ce qui est implémenté
- L'expérience antérieure est exécutée dans un sous-dossier et ses preuves sont préservées.
- La contradiction est lue **après** la prévision et le premier examen.
- Une révision candidate séparée et scellée est écrite, avec provenance, préconditions et dépendances.
- La compétence acquise n'est ni effacée ni promue; elle continue de produire une prédiction *shadow*.
- Le système classe en **HOLD** les prédictions pour lesquelles une inversion imprévue reste possible sans information supplémentaire; il ne fait pas semblant de savoir détecter une inversion future.
- Trois nouveaux examens (deux mouvements réguliers accélérés et une inversion cachée) mesurent l'erreur shadow et la couverture effective; les engagements sont écrits avant révélation du feedback.

## Limite scientifique importante
Une règle d'abstention généralisée, même si elle empêche une décision risquée, **ne démontre pas une meilleure calibration** : la couverture peut tomber à zéro. On n'a donc pas encore un moteur capable de distinguer un cas prévisible d'une contradiction future cachée. Il faut plus tard ajouter une variable réellement observable ou un modèle d'incertitude évalué avec des scénarios hors distribution. Ne pas interpréter le HOLD comme compréhension causale.

## Exécution Windows
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_skill_applicability_review_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.skill_applicability_review_v1 --out "build/skill-review-f1d-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/skill-review-f1d-v1/MASTER_REPORT.json"
```

Tout résultat doit rester candidat. `NATIVE_MEMORY_WRITE=FALSE`, `CANONICAL_PROMOTION=FALSE`, `DECISION_AUTHORITY=KX108_ONLY`. Les tests publiés ne constituent pas une exécution validée sur le PC.
