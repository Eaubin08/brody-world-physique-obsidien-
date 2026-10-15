# 91 — F1E calibration empirique, abstention et futurs indistinguables

Contexte : F1D a montré 3/3 HOLD (couverture nulle), tandis que la correction apprise +1 px améliorait deux trajectoires et détériorait une inversion cachée. Le prochain test doit distinguer **risque empirique** et **information impossible à obtenir avant la prédiction**.

## Implémentation réelle
Le module `brody_world_physique/selective_risk_calibration_v1.py` réutilise l'école de correction supervisée V1, puis sépare quatre cas de **calibration** et quatre cas de **TEST aveugle**. Les deux séries comportent des prolongements réguliers et des inversions qui présentent les mêmes quatre premières observations. Les prédictions de l'organe existant sont scellées; la décision de couverture est scellée avant le retour des images TEST.

Une règle de laboratoire déclarée : couvrir un contexte seulement si **l'erreur maximale observée en calibration** ne dépasse pas 2 px. Il ne s'agit ni d'une borne statistique générale, ni d'une compétence permettant de détecter l'inversion future. Si l'évidence est insuffisante, la règle conserve HOLD; les prédictions candidates demeurent disponibles pour comparaison après coup.

## Métriques
- Erreur maximale en calibration.
- Couverture de la politique testée, comparée à HOLD-all = 0 % et ACT-all = 100 %.
- Erreur moyenne parmi les réponses acceptées, null si aucune réponse acceptée.
- Erreur moyenne de toutes les prévisions candidates, même en cas de HOLD.
- Conservation du skill et rapports précédents (pas d'écriture canonique).

## Règles d'interprétation
Un HOLD universel n'est pas un succès pédagogique. Un ACT universel n'est pas une bonne calibration. L'inversion cachée ne peut pas être anticipée sans signal supplémentaire ou hypothèse de risque; le succès de ce protocole n'implique donc pas la résolution de l'applicabilité sélective. Il fournit un étalon documenté pour ajouter plus tard des indices réellement informatifs (mouvement caméra, collisions observables, occlusion et bruit) avec le monde MMonde, sans modifier aujourd'hui ses frontières.

L'expérience demeure synthétique, 2D, localement programmée. Les concepts Reverse 360, OS/IR, MMonde, P156 et programme E0–E7 restent incomplets et **non démontrés par cet audit**. KX108 conserve toute l'autorité.

## Commandes (racine du repo sur PowerShell)
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_selective_risk_calibration_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.selective_risk_calibration_v1 --out "build/f1e-risk-calibration-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/f1e-risk-calibration-v1/MASTER_REPORT.json"
```

Le chemin de sortie doit être inexistant, aucun écrasement des preuves F1D. Le code n'a pas encore été exécuté sur le PC utilisateur. `NATIVE_MEMORY_WRITE=FALSE`, `CANONICAL_PROMOTION=FALSE`, `DECISION_AUTHORITY=KX108_ONLY`.
