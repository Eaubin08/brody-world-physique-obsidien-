# 93 — F1G : intervention factorielle et contre-factuels distincts

## Pourquoi
F1F a obtenu deux transferts positifs et deux négatifs : un marqueur bleu pouvait prédire correctement une inversion synthétique, mais une fausse alerte aggravait l'erreur de 14 px. La cause du changement n'était pas le marqueur lui-même.

## Ce banc fait réellement
Sur **une même histoire visuelle passée**, deux facteurs synthétiques sont manipulés indépendamment :
- Marqueur visuel décoratif présent / absent.
- Changement de régime dans le simulateur présent / absent, nommé *contact* pour décrire le facteur du générateur de scène, mais **non visible à l'instant où l'algorithme prédit**.

Les quatre combinaisons sont appariées, sur deux conditions d'entraînement et deux nouvelles conditions TEST. Les prévisions du moteur existant sont scellées avant de lire la cinquième image. L'effet de chaque facteur est estimé à l'aide de différences moyennes entre groupes équilibrés. Le marqueur n'agit pas sur la dynamique du simulateur, alors que le paramètre de changement de régime agit sur elle.

**Objectif :** détecter qu'une corrélation de F1F ne suffit pas à établir une causalité. L'influence du paramètre du simulateur se constate dans des paires expérimentales, mais le système ne peut pas prévoir sa valeur dans une scène nouvelle s'il reste inobservable.

## Limites et interprétation
La méthode utilise les conditions d'intervention fournies par le banc d'expérience pour établir les comparaisons : ce n'est PAS une découverte autonome des causes à partir des seuls pixels. Le facteur "contact" n'est pas un vrai moteur physique de collision; c'est une variation de continuation synthétique. Une relation trouvée dans ce banc ne devient pas une loi générale. L'intervention et les étiquettes servent à évaluer la représentation, pas à introduire illicitement une réponse dans l'examen.

P149/P150/P152 ne sont **pas** annoncés comme branchés. Leur réutilisation exige les API et les SHAs confirmés, et le raccord doit ensuite vérifier le mouvement de caméra, l'identité, les conditions d'observabilité, le Reverse 360 et la génération visuelle réelle.

## Exécution PC PowerShell
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_factorial_counterfactual_school_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.factorial_counterfactual_school_v1 --out "build/f1g-factorial-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/f1g-factorial-v1/MASTER_REPORT.json"
```

Le dossier de sortie doit être inexistant. Aucun écrasement, aucune mutation de mémoire canonique; `KX108_ONLY`.

## Plan après F1G
1. Valider F1G sur PC, documenter erreurs et tests inattendus.
2. Localiser les implémentations historiques exactes P149/P150/P152 et récupérer leurs contrats réels sans les reconstruire.
3. Expérimenter des indices de mécanismes physiquement observables (contact, changement de référentiel, occultation), sans fuiter la réponse future.
4. Relier perception, hypothèses multiples et génération puis confrontation d'invariants; ajouter les tests de compétences cumulatives et transfert négatif.
5. Étendre aux séquences vidéo réelles une fois les parcours synthétiques et les frontières SENS/MMonde vérifiés.
