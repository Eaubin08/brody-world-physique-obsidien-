# P160 — Examen multi-angle, expériences séquentielles et connaissances coexistantes

## Principe
Après P159 (980 examens ; choix d'une expérience unique sur trois régimes connus), P160 évalue **plusieurs expérimentations successives** et des conditions contradictoires : règles proches, bruit, budget, changements de régime, demandes d'alternatives et possibilité de HOLD.

**Modèles et données** : 4 régimes de mouvement synthétiques `flat`, `slope`, `spring`, `near_slope`. Les réponses à 4 interventions `observe`, `tap`, `tilt`, `pulse` sont inférées depuis des positions mesurées dans des images rendues. Le modèle empirique est ensuite gelé avant l'examen. Le régime `novel` n'a pas été appris. Les choix d'action utilisent uniquement ces modèles, une estimation de gain d'information (quadrature gaussienne), les coûts et la distribution de plausibilité courante. Aucune étiquette cachée n'est transmise au mécanisme de prédiction.

## Douze conditions croisées
`clear`, `near`, `ambiguous`, `noisy`, `budget_tight`, `budget_open`, `unknown_far`, `unknown_near`, `changed_context`, `request_multi`, `unidentifiable`, `mixed_noise`.

Attention :
- `unknown_far` est effectivement un régime `novel` hors de la banque. Le comportement attendu est HOLD lorsque l'écart aux modèles est grand.
- `unknown_near` simule une réponse perturbée de `near_slope`, qui **est présent dans la banque**. Ce n'est donc pas une authentique nouveauté absente de l'entraînement, mais un test de réponse proche/perturbée ; son compteur `unknown_holds` doit être interprété comme un indicateur de prudence, non un taux de reconnaissance de nouveauté.
- `changed_context` commute la loi après la première intervention. Il permet de repérer les sélections injustifiées après un changement, sans garantir qu'un contrôleur sait déjà détecter ce changement.
- `unidentifiable` ne rend disponible que l'observation sans intervention utile et demande les possibilités ; MULTI/HOLD est pertinent.
- Trois interventions au plus peuvent être choisies par épisode, sous contrainte budgétaire et sans réutilisation d'action. Le programme n'invente pas les interventions et ne réalise aucune action physique réelle.

## Mesures et réserves
Chaque condition fournit SELECT / MULTI / HOLD, sélection correcte ou fausse, couverture des hypothèses vraies dans MULTI, nombre d'expériences, coût, refus des dynamiques hors banque. Les 12 cellules contiennent 160 épisodes par défaut (**1 920 examens**), avec modèles figés, journal JSONL et rapport intégral. Une expérience peut se terminer par HOLD sans être un échec si les données ne permettent pas une conclusion sûre. Le protocole ne démontre pas une compréhension causale autonome, un apprentissage de nouveaux contextes hors entraînement, ni une robustesse réelle à toute nouveauté.

## Lancement PC — une campagne

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Git pull échoué" }
py -m py_compile brody_world_physique/image_multiangle_experiments_p160.py
if ($LASTEXITCODE -ne 0) { throw "P160 syntaxe échouée" }
py -m unittest discover -s tests -p "test_image_multiangle_experiments_p160.py" -v
if ($LASTEXITCODE -ne 0) { throw "P160 tests échoués" }
py -m brody_world_physique.image_multiangle_experiments_p160 --minutes 20 --lessons-each 30 --exam-each 160 --out "build\brody-p160-multiangle-001"
if ($LASTEXITCODE -ne 0) { throw "P160 campagne échouée" }
Get-Content "build\brody-p160-multiangle-001\MASTER_REPORT.json"
```

Fichiers : `FROZEN_RESPONSE_MODELS.json`, `EXAMS.jsonl`, `MASTER_REPORT.json`. Aucun ancien dossier de résultats n'est écrasé. Ne pas déclarer GREEN scientifique à partir du seul statut `EXAM_CAP`. Auditer séparément les fausses sélections, les coûts, l'hésitation pertinente, les modèles voisins et les changements de régime.

Gouvernance : `decision_authority=KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`. Branche expérimentale exclusivement.
