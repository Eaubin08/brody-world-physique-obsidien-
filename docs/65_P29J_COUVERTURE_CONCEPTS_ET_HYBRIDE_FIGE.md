# 65 — Couverture des recherches et P2.9j hybride figé

## Réponse documentaire
**NON : toutes les recherches personnelles ne sont PAS encore réintégrées au runtime.** Les tests P2.9h/i ne portent que sur la position spatiale et le rappel expérientiel sur vidéos synthétiques.

### Concepts reconnus et statut honnête
| Concept/source | État dans Brody P2.9j | Blocage ou prochain test |
|---|---|---|
| Apprentissage préverbal type enfant, école/expérience | simulation partielle V1–V4, P1 | autonomie des stratégies non prouvée |
| Mémoire des procédures, erreurs, instruments, savoir-faire | V1–V4 existants; P2.9j n'en réutilise pas la totalité | rattacher capacité + code + version + contexte |
| Historiquement fiable / données nouvelles / vérité vérifiée | P2.8–2.9i tests partiels | preuve de portée, révision sans oracle TEST |
| Connaissance provisoire, stabilisation, intention humaine | contrats P2.8, séparation P2.9 | valider B7/B8/B10 puis préserver KX108_ONLY |
| Chaque étage son langage, sa hiérarchie, espace et temps | couches P2.9, ponts P2.9d–g | transformations typées avec provenance/horloge |
| Fluctuation dite « bruit » = données de précision contextualisées | P2.4–P2.6 partiels | scènes visuelles changées et faux repères corrélés |
| Invariants, symétrie, Fibonacci, proportion | relations V4.2 2D; autres idées documentées | tester utilité, pas forcer une loi universelle |
| 360°, perception réciproque, inverse | orientations cardinales V4.2 et inverse algébrique | monde 3D et perspectives non démontrés |
| Analyse↔synthèse, décomposition, couches du peintre | Reverso + école de dessin | raccordement de re-perception et édition |
| Fidélité pixels, source et IN, précision variable par zone | éditeur/Reverso disponibles | contrat multi-régions et conservation de la source |
| Shazam visuel, signatures, 34 arbres | pistes historiques | interfaces précises et tests absents du P2 actuel |
| World Foundry, multiples versions/formes d'entraînement | conceptuel/documentaire | catalogue exhaustif des configurations non gelé |
| Multidimensionnel, micro↔macro, matière, thermodynamique | contrats/propositions | dépend de mesures/variables distinctes selon échelles |
| F16, F12, MMonde, SENS, GPS comme organes | contrats et certaines représentations candidates | adaptation runtime explicite sans fusion des autorités |
| Représentations en circulation, mutualisation sans double compter | P1 et P2.9g quatre vues d'une source | vraie ablation multimodale sur mêmes frames |
| Génération visuelle apprise, contrôle par Reverso | images Reverso synthétiques | pas encore un générateur autonome de qualité |

**Ne pas présenter cette table comme l'inventaire exhaustif de toutes les archives**, notamment des 81+ variantes d'apprentissage évoquées dans d'autres travaux : attribution et définition d'origine doivent être réconciliées séparément. Les scripts P2.9d-g ne constituent pas l'activation générale de ces organes.

## P2.9j : ce qui est effectivement développé
`p29j_frozen_hybrid_audit_v0.py` évalue une **règle figée avant lecture des scores de cette analyse** : si A4 mémoire a proposé, choisir A4; sinon A1 spatial; sinon HOLD. Les prédictions A4/A1 viennent du fichier P2.9h déjà pré-engagé. L'analyse utilise les erreurs uniquement pour mesurer la politique, pas pour la choisir. Politique suggérée après inspection de P2.9i : **post-hoc sur le même banc, pas preuve prospective indépendante**. Aucune nouvelle perception, apprentissage ou génération; score attendu à mesurer, pas anticiper. Documenter les 50 cas, couverture/erreur, variantes de baselines, provenance et replay.

## PC fixe — sans changer de branche ni modifier main
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p29j*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
$source = "build\p29h-ablation-20261009-061517.json"
$out = "build\p29j-hybrid-$(Get-Date -Format yyyyMMdd-HHmmss).json"
py -m brody_world_physique.p29j_frozen_hybrid_audit_v0 --source $source --out $out
if ($LASTEXITCODE -ne 0) { throw "P2.9j échoué" }
py -m brody_world_physique.p29j_frozen_hybrid_audit_v0 --source $source --out $out --verify
if ($LASTEXITCODE -ne 0) { throw "Rejeu échoué" }
Write-Host "RESULTATS=$out"
```

## GATE suivant
Ne pas retoucher le choix hybride à la vue du score. Tester sur nouvelles familles d'images et changements d'environnement, en réintroduisant effectivement P1 raster, Reverso et les outils F12/F16/MMonde avant de déclarer un gain multimodal. Aucun B8/B10 write et KX108_ONLY.

## Correction de rejeu P2.9j — observation future absente
Le run réel P2.9h contient au moins une prédiction pré-engagée dont l'image future est manquante (score `null`). Cette situation **ne constitue pas un HOLD du prédicteur** et ne doit pas être une erreur artificielle à 0 px. Le rapport P2.9j conserve le choix pré-engagé, distingue `issued_predictions` et `unscorable_predictions`, calcule `coverage` sur les cas où une frame future a effectivement été observée, et fournit `issued_coverage` sur tous les épisodes. Le code refuse toujours un score absent pour la méthode choisie **si une autre méthode prouve que la frame future était observable**. Tests de non-régression ajoutés. Aucun changement P2.9h/P2.9i.

## Retour utilisateur : échecs utiles, boucles réversibles, non-irréversibilité
L'utilisateur précise que les erreurs sont une composante du développement des compétences, non une raison de bloquer systématiquement toute progression. Ce principe s'applique aux **erreurs de prédiction, reconstruction ou choix de méthode** et aux frictions observées, pas à la falsification des preuves ou à une autorisation d'action. Proposition de contrat d'apprentissage, **pas encore un moteur runtime** :

1. **Observer / situer** — garder source, scène, point de vue, intervalle et niveau de représentation.
2. **Proposer / pré-engager** — choisir méthode et chemin, enregistrer l'hypothèse sans voir le résultat futur.
3. **Tenter / reconstruire** — utiliser la capacité déjà disponible (Reverso, outil de dessin, prédicteur, etc.).
4. **Comparer / qualifier l'écart** — distinguer erreur de procédure, écart physique, observation manquante, contradiction et erreur technique du banc; ne pas écraser une observation utile sous l'étiquette « bruit ».
5. **Diagnostiquer le chemin** — conserver succès, échec, raison, contexte, version de la capacité et possibilité de reprendre une étape intermédiaire.
6. **Réessayer sélectivement** — changer une méthode, une vue ou une hypothèse à la fois; reprendre un acquis stabilisé sans tout refaire; garder aussi l'ancien essai.
7. **Tester sur un autre épisode indépendant** avant d'attribuer un gain; ni l'intention ni la simulation auto-générée ne fabriquent une vérité.

Arrêts nécessaires : budget d'essais, stagnation, information absente → demander autre observation/UNKNOWN/HOLD, dérive de source/référentiel → revenir au dernier point vérifié; aucun écrasement automatique du savoir, aucune promotion B8 et aucune écriture Native Memory. Réversibilité = pouvoir *revenir à un état de travail et réviser l'hypothèse*, pas effacer l'historique ni contourner KX108_ONLY.

### Retour expérimental P2.9j, 2026-10-09
50 épisodes, 50 prédictions émises, 49 scorables, hybride 3.368161194972157 px, 2 erreurs >10 px, 39 choix mémoire et 11 spatiaux; rapport rejoué avec succès. **Échec des tests 5/6 non expérimental** : `test_replay_and_mutation` fixait `coverage=1.0`, devenue la vraie couverture sur les 49 observables. Mutation changée en `0.12345` afin d'exercer effectivement la détection de rapport altéré. À revalider PC.
