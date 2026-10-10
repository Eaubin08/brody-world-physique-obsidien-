# F10 — Campagne intensive contextualisée de 1 000 épisodes

**Branche :** `exp/p2-multirepresentation-ablation-20261009`. **Statut : publiée, pas encore exécutée sur le PC.**

## Objectif
Prolonger F9 (1000 épisodes, 1 changement de politique, dégradation après contradiction) en testant si des expériences contradictoires peuvent être **conservées simultanément dans deux contextes**, plutôt que de réécrire la même politique.

## Trois situations
- `OLD` : `LIGHT|line` doit utiliser le crayon.
- `NEW` : `LIGHT|line` doit utiliser le stylo.
- `MIXED` : sans indication du contexte réel, `LIGHT|line` doit répondre `HOLD_AMBIGUOUS_CONFLICT`. Les autres contextes peuvent utiliser une proposition si OLD et NEW ont appris et donnent le même choix. Une valeur hors contrat retourne HOLD.

Les 1000 expériences TRAIN alternent OLD / NEW ; formes `line/angle/zigzag/box`, intentions `LIGHT/UNIFORM/EXPRESSIVE`, outils hérités V2 `PENCIL/PEN/NIB`. Chaque épisode contribue à une politique contextuelle candidate, avec mise à jour EWMA existante de F9. Le moteur de rendu du professeur reste synthétique. Les formes sont fournies au dessin et non reconnues depuis une image inconnue.

## Preuves et contrôles
- 1000 reçus TRAIN en JSONL chaînés SHA256, vérifiés en fin de boucle ;
- mémoire de politique contextualisée, snapshot à chaque 100 épisodes, sans écraser les précédents ;
- examen TEST de 144 cas par checkpoint (3 régimes × 3 styles × 4 formes × 4 répétitions), dont les cas MIXED ambigus qui doivent aboutir à HOLD ; candidat calculé et hashé avant génération de la référence TEST ;
- mesures séparées par OLD, NEW, MIXED : erreur moyenne, propositions évaluées et HOLD ;
- mêmes cibles aveugles à chaque checkpoint pour suivre dégradation et préservation ;
- aucune correction provenant des évaluations TEST, aucune promotion automatique, aucun writer Native Memory ; `KX108_ONLY` maintenu.

**Limites :** l'étiquette de contexte est explicitement donnée. Aucune inférence autonome du bon contexte à partir de pixels, aucune correction des gestes, et aucune garantie de mémorisation permanente ou de compréhension physique. Le routage est une table candidate locale : ce banc ne prouve pas la connexion Native Memory/MEMZUM ni l'intégration achevée à `experience_memory_v1`.

## Lancement Windows (une seule campagne)
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f10_contextual_1000_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F10 échouée" }
py -m unittest discover -s tests -p "test_fusion_f10*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F10 échoués" }
py -m brody_world_physique.fusion_f10_contextual_1000_v0 --episodes 1000 --checkpoint 100 --out "build\fusion-f10-contextual-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne F10 échouée" }
Get-Content "build\fusion-f10-contextual-001\report.json"
```
En cas d'échec, utiliser `-002` après correctif sans effacer le rapport précédent. Les résultats ne seront considérés comme validés qu'après exécution locale et lecture du rapport.
