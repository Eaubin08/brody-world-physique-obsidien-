# P158 — Découverte active du contexte par expérience discriminante

## Hypothèse
Deux trajectoires peuvent produire **exactement les mêmes quatre premières images**, tout en obéissant à deux régularités distinctes. Les deux modèles appris sont conservés. Avant intervention : `MULTI` si plusieurs explications sont demandées, `HOLD` si aucun test n'est possible, et `PROBE` si une expérimentation discriminante est disponible. Après intervention : `SELECT` seulement si le résultat observé distingue suffisamment les modèles ; `HOLD` si la physique observée ne correspond à aucun modèle ; `MULTI` si elle demeure ambiguë.

## Protocole
Deux régimes de dynamique cachée (`flat` et `slope`) et un régime nouveau `novel`. Le simulateur rend sept images ; le système ne voit d'abord que les quatre premières, identiques par construction entre régimes pour un même état initial. Il peut demander l'expérience `observe_after_discriminating_intervention`, programmée dans le simulateur. L'observation post-intervention est alors confrontée à une banque de deux accélérations inférées depuis les **pixels** de leçons séparées.

Cinq familles : expérience discriminante, absence d'expérience, expérience non discriminante, observation bruitée, dynamique hors banque. **Une expérience non discriminante ne permet aucune identification**, même si la trajectoire observée ressemble à l'un des modèles hors intervention ; le statut de l'action est connu de l'élève. Le protocole signale les erreurs de confiance en comptant les sélections erronées.

140 examens × 5 conditions = **700** examens par défaut. Les modèles ne reçoivent jamais le régime caché. Les vérités cachées servent uniquement à la notation. Les résultats sont écrits dans `FROZEN_HYPOTHESES.json`, `EXAMS.jsonl`, `MASTER_REPORT.json`.

## Limitations explicites
Ce n'est pas un agent qui invente une expérience : **le choix du probe est codé**. Les scènes demeurent synthétiques et la famille de problèmes est définie. La décision est une règle statistique simple, non une compréhension causale générale. Le retour SELECT/MULTI/HOLD est une **proposition épistémique locale** sans autorité d'action. Le modèle ne modifie pas la mémoire native, ni le kernel.

## Une seule commande Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_active_context_probe_p158.py" -v
if ($LASTEXITCODE -ne 0) { throw "P158 TESTS échoués" }
py -m brody_world_physique.image_active_context_probe_p158 --minutes 12 --lessons-each 30 --exam-each 140 --out "build\brody-p158-active-probe-001"
if ($LASTEXITCODE -ne 0) { throw "P158 RUN échoué" }
Get-Content "build\brody-p158-active-probe-001\MASTER_REPORT.json"
```

Critères d'analyse : discrimination exacte des premières images, conformité des décisions avant/après intervention, sélections correctes, sélections erronées, maintien de l'ambiguïté en l'absence de test et détection du hors banque. Le verdict scientifique reste dépendant des scores PC.

Gouvernance : `decision_authority=KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
