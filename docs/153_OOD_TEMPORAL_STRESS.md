# P153 — Examen hors distribution des trajectoires

## Objet

P152 a obtenu de meilleurs résultats que le comparateur P151 sur les mêmes scènes ; il reste inconnu si l'amélioration résiste à un **autre moteur de scènes et d'autres dynamiques**. P153 teste P151 et P152 **sans réentraînement** et sur les mêmes nouvelles images.

## Dix perturbations distinctes

Vitesse irrégulière, inversion brusque, caméra mobile sans repères, caméra mobile avec repères, occultation partielle, occultation prolongée, couleurs identiques, changement de couleur, bruit et distracteurs, pas de temps irrégulier. Les deux moteurs n'ont accès qu'aux 9 images de perception et doivent prédire la position de la cible au temps suivant. Les identités latentes A/B sont réservées à l'évaluation.

Le générateur P153 est écrit séparément de P151 : fond légèrement variable, hauteurs indépendantes des mobiles, déplacement de caméra, occultation et distracteurs. Ce laboratoire **reste synthétique et programmé** ; l'absence de repères peut conduire à des erreurs de caméra importantes.

## Évaluation

Pour chaque perturbation : nombre d'examens, couverture, erreur moyenne parmi les réponses, proportion de tous les examens pour lesquels l'identité cible est correctement attribuée, taux de HOLD. Le comparateur P151 et la mémoire multi-hypothèses P152 sont évalués sur **les mêmes images**. Conservation des épisodes et échantillons PNG pour inspection. Budget de temps et nombre d'épisodes bornés.

Critère : un score élevé sur P152 uniquement n'autorise pas à conclure à une compétence généralisée. Il faut examiner les pertes sur plusieurs facteurs et la pertinence des refus. Les « pas de temps irréguliers » sont des sauts de mouvement simulés ; le système ne reçoit pas de véritable horodatage variable — ce scénario mesure donc surtout la robustesse à des sauts imprévus, pas la compréhension du temps.

## Commande PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_ood_temporal_p153.py" -v
if ($LASTEXITCODE -ne 0) { throw "P153 tests échoués" }
py -m brody_world_physique.image_ood_temporal_p153 --minutes 15 --episodes-each 200 --out "build\brody-p153-ood-001"
if ($LASTEXITCODE -ne 0) { throw "P153 run échoué" }
Get-Content "build\brody-p153-ood-001\MASTER_REPORT.json"
```

**Gouvernance :** branche expérimentale ; `decision_authority=KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`. Les résultats PC ne sont pas encore connus, et la comparaison n'établit pas un apprentissage de la physique.
