# P157 — Connaissances coexistantes, pertinence contextuelle et décision selon la demande

## Précision de doctrine
Une connaissance nouvelle n'écrase pas nécessairement l'ancienne : deux règles peuvent être correctes dans des contextes différents. L'éducation doit apprendre la **condition d'application** d'une connaissance, et non seulement ajuster le paramètre d'une règle globale. Lorsqu'une demande exige une conclusion unique sans information suffisante, la réponse est HOLD ; lorsque la demande réclame les possibilités, la réponse est MULTI et conserve deux hypothèses ; avec indices suffisants, SELECT privilégie la connaissance contextuelle pertinente.

## Protocole expérimental
Deux régimes synthétiques d'objet mobile sont observés depuis les pixels : `flat` (vitesse régulière) et `slope` (décélération discrète). Les exemples sont enregistrés comme **deux représentations distinctes** ; aucun écrasement. Le contexte est fourni à l'inférence par une marque visuelle bleue qui indique `flat` ou `slope`, ou qui est absente, inconnue, brouillée ou volontairement contradictoire. Le système infère une accélération moyenne depuis les différences secondes de trajectoires de cours. L'examen utilise de nouvelles trajectoires, jamais les règles cachées du générateur.

Trois demandes : `single` (une prédiction unique ou HOLD), `possibilities` (afficher deux propositions), `explain` (sélectionner ou exposer l'ambiguïté). Six conditions : `clear_flat`, `clear_slope`, `cue_missing`, `cue_conflict`, `noisy_cue`, `unknown_context`. Cela produit 18 cellules, 100 examens par cellule, soit 1 800 examens par défaut. Mesures : SELECT/MULTI/HOLD, exactitude de sélection et erreur de prédiction, préservation des deux modèles contextuels.

## Limites explicites
Le symbole bleu est artificiel et construit pour le test. Les familles physiques sont connues du programme et les demandes sont structurées ; ni compréhension du langage libre ni compréhension de causalité ou du monde réel ne sont démontrées. Le test `cue_conflict` ne prouve pas l'identification d'une cause : il confronte un indice à la différence de mouvement observée. La règle d'incertitude est programmée. Ceci constitue un prototype de **sélection contextuelle et de pluralité épistémique**, pas une démonstration d'intelligence générale. Les règles et les résultats ne modifient pas la mémoire native.

## Commande Windows (une campagne)

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_context_coexistence_p157.py" -v
if ($LASTEXITCODE -ne 0) { throw "P157 : tests échoués" }
py -m brody_world_physique.image_context_coexistence_p157 --minutes 15 --lessons-each 40 --exam-each 100 --out "build\brody-p157-context-001"
if ($LASTEXITCODE -ne 0) { throw "P157 : campagne échouée" }
Get-Content "build\brody-p157-context-001\MASTER_REPORT.json"
```

Vérifier : couverture 18/18, exactitude SELECT sur contextes clairs, HOLD sur demandes uniques ambiguës, MULTI comprenant les deux règles quand l'information manque. Ne pas appeler un 100 % de MULTI une prédiction résolue. Conserver `FROZEN_CONTEXT_RULES.json`, `EXAMS.jsonl` et `MASTER_REPORT.json`.

Gouvernance : `decision_authority=KX108_ONLY`; `native_memory_write=false`; `canonical_promotion=false`.
