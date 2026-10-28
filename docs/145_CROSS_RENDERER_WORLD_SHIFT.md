# P145 — Transfert vers de nouveaux mondes de rendu

## Objet de l'examen

P144 a obtenu 85,15 % en routage ignorant le nom de la transformation, mais apprentissage et examen venaient toujours de la même famille de dessins P140. P145 met en place un **deuxième moteur de génération écrit indépendamment**, avec ses propres choix de placement, proportions, fonds, contours et occultations.

Les scènes d'apprentissage et de validation restent issues de P140. Le routeur construit sur validation est figé avant l'examen. Pendant l'examen, il reçoit les pixels et le domaine demandé, mais pas le nom du monde d'origine. Les résultats ne sont pas utilisés pour adapter le modèle.

## Cinq mondes d'examen × cinq compétences

- `reference` : scène habituelle P140, contrôle.
- `new_engine_light` : nouveau moteur, fond ivoire et flou.
- `new_engine_dark` : nouveau moteur, fond sombre.
- `new_engine_outlined` : nouveau moteur, contours ajoutés.
- `new_engine_occluded` : nouveau moteur, bandes occultantes sur objets.

Ces mondes sont croisés avec forme, couleur, nombre, disposition et orientation : **25 conditions différentes**. Le cas du fond sombre est particulièrement important car certains détecteurs de premier plan codés en dur risquent de se tromper ; conserver cet échec est l'objectif. Le test de nombre dans les mondes occultés peut devenir ambigu visuellement, ce qui doit être analysé en détail.

Ces mondes ont **des implémentations différentes**, pas des sources indépendantes du monde réel. Ils restent générés par notre code et connaissent les mêmes classes symboliques.

## Lancement PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_cross_renderer_world_p145.py" -v
if ($LASTEXITCODE -ne 0) { throw "P145 : tests échoués" }
py -m brody_world_physique.image_cross_renderer_world_p145 --minutes 15 --train-each 300 --validation-each 90 --exam-each 1000 --out "build\brody-p145-world-001"
if ($LASTEXITCODE -ne 0) { throw "P145 : campagne échouée" }
Get-Content "build\brody-p145-world-001\MASTER_REPORT.json"
```

Le programme s'arrête dès que **15 minutes ou 25 000 examens** sont atteints. Il ne simule pas artificiellement une durée. Le rapport `CELL_REPORT.json` permet de comparer chaque compétence entre les cinq mondes. `EXAM.jsonl` conserve les décisions individuelles. `FROZEN_BEFORE_EXAM.json` documente les frontières cours/validation/examen.

## Critère scientifique

Ne pas confondre réussite technique de la campagne et robustesse de Brody. Si la performance baisse fortement dans les nouveaux moteurs, **l'hypothèse de transfert robuste est réfutée** dans les conditions testées. Les labels restent issus du moteur de génération et ne garantissent pas qu'un objet soit observable après occlusion. Aucun résultat d'images naturelles, de 3D réelle ni de causalité physique n'est établi.

Gouvernance inchangée : branche expérimentale, `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
