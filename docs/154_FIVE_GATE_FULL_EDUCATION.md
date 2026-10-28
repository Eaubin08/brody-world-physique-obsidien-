# P154 — Éducation intégrale en une passe : cinq critères

**Objet** : tester dans un même processus : 1) inférence d'une régularité depuis des images ; 2) gel/conservation d'une mémoire de règle ; 3) application à des mondes d'examen différents ; 4) production d'une image de prédiction et comparaison pixel à pixel ; 5) correction supervisée à partir d'un troisième jeu d'exemples, puis nouvel examen sans rétroaction.

**Limite centrale** : il s'agit d'un laboratoire synthétique et de modèles numériques simples, PAS de découverte autonome de lois physiques réelles. Le programme sait de quelle *famille de cours* provient une série, mais ne reçoit pas les valeurs de vitesse et d'accélération du simulateur. Le modèle apprend une estimation d'accélération moyenne par famille : cette procédure n'est pas une induction scientifique générale ; lorsque les accélérations positives et négatives s'annulent dans les leçons, la règle moyenne peut devenir inadaptée. L'examen le révélera.

## Contrats des étapes

1. **Cours** : quatre familles `stationary`, `constant_speed`, `constant_acceleration`, `reverse`. Mesurer les centres des objets dans cinq images avec extraction de pixels ; déduire variations de positions et accélération moyenne ; enregistrer `FROZEN_BEFORE_EXAM.json`.
2. **Examens de transfert** : six environnements `clean`, `dark`, `camera`, `noise`, `large`, `occluded`. Les images proviennent du simulateur (pas de vidéos extérieures). Les graines et scènes d'examen sont distinctes des cours.
3. **Prédiction visuelle** : prédire le prochain centre, rendre un disque sur une image canonique, mesurer intersection-sur-union des pixels colorés face à l'image canonique de la vérité future. Ce n'est pas une génération photoréaliste.
4. **Corrections** : prendre des **leçons additionnelles séparées** du corpus d'examen pour apprendre un décalage résiduel par couple famille/monde. Enregistrer le correctif séparément ; conserver intact le modèle de base.
5. **Réexamen** : nouveau jeu scellé ; comparer baseline gelée et version corrigée sur **exactement les mêmes séquences**. Inclure le monde `clean` pour mesurer l'oubli/régression. Tous les résultats, bons ou mauvais, doivent être conservés.

**Quantités par défaut** : 4 familles × 6 environnements = 24 cellules ; 32 exemples de cours par famille (128 leçons), 120 examens par cellule (2 880), 24 leçons de correction par cellule (576), 120 réexamens par cellule (2 880). La durée maximale autorisée est 20 minutes ; elle n'est pas forcée. Si le temps expire, le rapport indique les cellules incomplètes : aucune revendication de campagne intégralement réussie.

**Mesures** : erreur absolue en pixels, couverture, pourcentage à ±3 pixels, qualité des images par IoU, MAE avant/après correction, rétention sur monde de référence. Refuser de confondre `execution_green` et `education_criteria_proven`.

## Commande Windows — lancement complet et unique

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_full_education_p154.py" -v
if ($LASTEXITCODE -ne 0) { throw "P154 : tests échoués" }
py -m brody_world_physique.image_full_education_p154 --minutes 20 --lessons-each 32 --exam-each 120 --feedback-each 24 --retest-each 120 --out "build\brody-p154-education-001"
if ($LASTEXITCODE -ne 0) { throw "P154 : campagne échouée" }
Get-Content "build\brody-p154-education-001\MASTER_REPORT.json"
```

Fichiers de preuve : `FROZEN_BEFORE_EXAM.json`, `LEARNED_CORRECTIONS.json`, `EXAM.jsonl`, `RETEST.jsonl`, `MASTER_REPORT.json`, `samples/`. Un dossier existant entraîne un refus d'écrasement.

**Gouvernance** : `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`. Aucune promotion canonique après simple PASS ; validation scientifique et transférabilité restent distinctes.
