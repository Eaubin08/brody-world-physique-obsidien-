# F11 — Campagne de 1 000 observations de contexte visuel

**Code et tests publiés, résultats d'exécution non encore connus.** Branche expérimentale `exp/p2-multirepresentation-ablation-20261009` ; ne pas toucher `main`.

## Ce qui est réellement appris

Après F10 (OLD/NEW explicitement étiquetés), F11 présente des **images synthétiques 64×64** avec des marqueurs noirs dans les coins, que le système mesure dans les pixels. Le contexte n'est pas transmis directement au sélecteur pendant TEST : celui-ci lit les pixels, retrouve les observations TRAIN accumulées, propose OLD/NEW ou HOLD. Des marques contradictoires `BOTH` et absentes `NONE` sont évaluées ; le retour TEST n'est pas injecté dans TRAIN.

Par défaut : **1000 épisodes TRAIN**, dix checkpoints de **80 examens** chacun. Reçus numérotés, chaînés SHA256, sauvegardes des mémoires candidates, refus lorsque les indices sont ambigus ou sans expériences suffisantes. Aucune écriture Native Memory, aucune promotion automatique, décision `KX108_ONLY`.

## Limites scientifiques

Ce n'est **pas une compréhension générale d'une scène** : les coins et seuils de pixels sont des caractéristiques préprogrammées, les deux classes OLD/NEW sont enseignées pendant TRAIN. Le protocole vérifie une association apprise entre de très simples caractéristiques de perception et les contextes. Il n'entraîne pas les gestes dessinés, ne gère pas encore superpositions/mouvements, n'utilise pas directement l'index `experience_memory_v1`, MEMZUM, ni la correction de gestes. Les imports du rendu V2 et de F10 ne suffisent pas à prouver que le choix d'un instrument a été évalué visuellement dans cette campagne : les scores portent ici sur la **reconnaissance du contexte et HOLD**.

## Lancement sur PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f11_visual_context_1000_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F11 invalide" }
py -m unittest discover -s tests -p "test_fusion_f11*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F11 échoués" }
py -m brody_world_physique.fusion_f11_visual_context_1000_v0 --episodes 1000 --checkpoint 100 --out "build\fusion-f11-visual-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne F11 échouée" }
Get-Content "build\fusion-f11-visual-001\report.json"
```

En cas de correction, conserver les sorties antérieures et utiliser un nouveau dossier `-002`.

## Suite, après les résultats
Éliminer davantage d'indices préprogrammés en utilisant les représentations visuelles d'Obsidia, des transformations et de vrais défauts de dessins ; mesure de transfert non trivial, échec/anti-oubli et correction TRAIN sur le moteur gestuel. Ne pas confondre un banc de routage des marqueurs avec l'apprentissage physique visuel de Brody.
