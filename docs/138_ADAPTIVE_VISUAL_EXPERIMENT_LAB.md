# Brody — P138 : laboratoire de tâches nouvelles, durée bornée et échecs observables

**Pourquoi P137 était insuffisante :** le budget était 600 secondes mais les neuf suites préexistantes étaient finies en ~2,39 secondes. P138 ne relance plus ces suites. Elle produit des scènes procédurales inédites à chaque épisode et exerce huit questions différentes : identification des couleurs, nombre de composantes, position, rotation, silhouette, disparition d'élément, réflexion, relations spatiales. Chaque tâche produit une preuve et un résultat.

La difficulté augmente périodiquement (un à quatre objets). Au-delà des premières phases, le moteur alloue davantage d'essais aux familles accumulant des échecs, tout en réexaminant toutes les familles. Chaque scène est nouvelle, mais les familles et les règles génératrices restent **limitées et programmées**, pas un monde physique autonome.

**Distinction capitale :** c'est un banc de **mesure et de découverte de failles** ; aucune règle de Brody n'est entraînée ou modifiée pendant ces épisodes. Ne pas confondre une campagne de plusieurs minutes avec apprentissage actif. Le code mesure des comportements heuristiques, pas une compréhension du monde réel. Des faux PASS sont possibles car plusieurs questions n'ont pas encore d'oracle robuste. Tout taux de succès doit être interprété avec cette limite.

## Commande PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_adaptive_visual_lab_p138.py" -v
if ($LASTEXITCODE -ne 0) { throw "P138 échouée" }
py -m brody_world_physique.image_adaptive_visual_lab_p138 --minutes 10 --max-episodes 20000 --out "build\brody-p138-10min-001"
if ($LASTEXITCODE -ne 0) { throw "P138 interrompue" }
Get-Content "build\brody-p138-10min-001\MASTER_REPORT.json"
```

La campagne s'arrête **au premier atteint** : durée de 10 minutes ou 20 000 épisodes. Elle peut donc finir avant les 10 minutes. Pour une durée plus longue, augmenter le plafond d'épisodes dans la limite 50 000 : `--minutes 30 --max-episodes 50000`. Il serait contraire aux objectifs de maintenir une boucle oisive uniquement pour remplir la durée.

**Résultats :**
- `EXPERIMENTS.jsonl` : chaque expérience différente avec sa famille, sa difficulté, son verdict et ses observations ;
- `failure_*.png` : exemples visuels des premiers échecs (limite de fichiers) ;
- `MASTER_REPORT.json` : nombre d'épisodes et cycles, durée réellement consommée, types de compétences et leurs erreurs.

**Prochaine phase scientifique :** alimenter le laboratoire avec vidéos et images réelles de provenance vérifiable, véritables leçons successives, inférence avant feedback, comparaison mémoire activée/désactivée, rétention différée et nouveaux types de tâches au-delà de l'image 2D (perspective 3D, gravité, interactions, causalité, autonomie d'expérience). Ces fonctions ne sont pas apportées par P138.

**Gouvernance :** expérimental uniquement ; `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`. Aucun changement de `main`.
