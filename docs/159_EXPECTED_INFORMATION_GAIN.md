# P159 — Choix d'expérience par gain d'information attendu

## Motivation
P158 a réussi 700 examens et évalué un **probe discriminant déjà désigné**. Il ne choisissait pas réellement entre plusieurs expériences. P159 fournit au système un ensemble d'actions possibles, leur coût, et des effets statistiques **appris depuis les images des leçons**, afin de choisir avant toute observation de résultat.

## Protocole
Trois contextes appris `flat`, `slope`, `spring`; un contexte `novel` absent de la banque, évalué séparément. Quatre expériences disponibles au laboratoire : `observe` (non informative), `weak_tap`, `tap`, `tilt`. Les réponses temporelles à ces interventions sont apprises par lecture de trajectoires visuelles. Un choix maximise `information_gain - cost_weight * probe_cost` (entropie Shannon, hypothèses initialement équiprobables). Si aucune expérience ne vaut son coût : HOLD.

Après intervention, le résultat observé est comparé aux prédictions des modèles : SELECT pour une hypothèse identifiable, MULTI pour des modèles encore indiscernables, HOLD pour une dynamique hors de la banque. Les régimes latents servent **uniquement à la notation**. Les paramètres de génération ne sont pas transmis au modèle.

Sept conditions indépendantes : `tap_available`, `tilt_only`, `weak_only`, `no_informative`, `cost_sensitive`, `novel_only`, `known_vs_novel`. Par défaut, 140 épisodes par condition = 980 examens. Les deux dernières conditions fournissent la distinction détaillée entre situations connues et inédites qui manquait à P158.

Mesurer : décision PROBE/HOLD en amont ; coût et action choisie ; exactitude des sélections sur les régimes connus ; maintien de MULTI si non discriminant ; HOLD sur le hors-banque ; faux SELECT sur les régimes inconnus ; preuve de non-utilisation du résultat d'examen pour choisir l'expérience.

## Limites et frontières
Les expériences candidates sont **fournies par programmation** et non inventées par Brody. Le calcul d'entropie et les prix sont une règle algorithmique fixée ; ce n'est pas une expérimentation physique réelle. Les données sont synthétiques ; la pertinence des choix peut être différente avec des observations bruitées, des actions dont les effets sont incertains, des priors déséquilibrés et des lois nouvelles plus proches des anciennes. La `novel` simulée est volontairement distante, ce qui facilite HOLD. Ces points sont à auditer avant toute affirmation forte.

Aucune mutation du noyau ni de mémoire native. `decision_authority=KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.

## Commande PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/image_probe_selection_p159.py
if ($LASTEXITCODE -ne 0) { throw "P159 SYNTAXE échouée" }
py -m unittest discover -s tests -p "test_image_probe_selection_p159.py" -v
if ($LASTEXITCODE -ne 0) { throw "P159 TESTS échoués" }
py -m brody_world_physique.image_probe_selection_p159 --minutes 12 --lessons-each 25 --exam-each 140 --out "build\brody-p159-information-gain-001"
if ($LASTEXITCODE -ne 0) { throw "P159 RUN échoué" }
Get-Content "build\brody-p159-information-gain-001\MASTER_REPORT.json"
```

Fichiers `FROZEN_PROBE_RESPONSES.json`, `EXAMS.jsonl`, `MASTER_REPORT.json`. Le dossier de résultats ne peut pas être écrasé. Lire les métriques par condition avant d'en tirer une conclusion : réussite technique ≠ découverte autonome de causalité ou de physique.
