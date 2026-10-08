# 45 — Brody P2 : protocole d'ablation multireprésentation (PRÉ-FORGE)

**Statut :** contrat expérimental, pas résultat. **Parent :** [44 — P1](44_P1_PASSERELLE_MULTIREPRESENTATIONS_VIDEO_MONDE.md). **Branche :** `exp/p2-multirepresentation-ablation-20261009`.

## Question falsifiable
L'utilisation conjointe des vues RASTER / SPATIAL / TEMPORAL / MOTION améliore-t-elle la prédiction hors échantillon ou la reconstruction Reverso par rapport au meilleur système autorisé utilisant une seule vue, à budget d'information et d'expérience comparable ?

## Définition et équité des bras
- **A0 Immobile** : dernière position observée, témoin naïf.
- **A1 Cinématique** : positions XY + timestamps du passé; extrapolation à vitesse constante (aucune image brute).
- **A2 Spatial** : géométrie et repère ancré passés, sans dérivées de mouvement ni prévisions issues des autres bras.
- **A3 Raster** : images passées uniquement, avec détection propre au bras; ne doit pas recevoir la série XY du bras spatial déjà nettoyée.
- **A4 Motion** : états de mouvement observables avant le cutoff, dérivés selon le contrat de ce bras; aucune future observation.
- **A5 Fusion partielle** : SPATIAL + MOTION; même budget historique, sans accès à la future frame.
- **A6 Fusion complète** : RASTER + SPATIAL + TEMPORAL + MOTION; même budget, même cutoff.
- **A7 A6 privé d'une vue** (quatre retraits un par un) : déterminer quelle vue est utile, inutile ou nuisible.

**Contrôle anticontamination :** si A3 utilise le même détecteur que A2, déclarer explicitement la dépendance commune; ne pas attribuer le gain à l'indépendance des modalités. Aucun bras ne peut avoir accès aux positions vérifiées après cutoff, aux étiquettes du professeur ou à la cible Reverso pendant sa prédiction. Si un bras manque d'implémentation réelle, statut `NOT_IMPLEMENTED` et aucun score fabriqué.

## Jeux d'essais
- Conserver le jeu P1 pour **régression uniquement**, pas comme test indépendant de découverte.
- Nouveaux épisodes synthétiques à graines retenues et génération traçable : déplacements et vitesses inconnus, accélérations différentes, formes/couleurs, changement d'échelle, caméra mobile, repère manquant, occlusion, mouvement imprévisible.
- Même liste d'ID d'épisode, mêmes horizons, timestamps, partitions TRAIN/VALIDATION/TEST et seeds pour tous les bras; tous les paramètres et règles de sélection sont gelés avant TEST.
- Les transformations d'une vidéo restent **une seule source dépendante**. Pour généraliser : regrouper l'analyse et les intervalles de confiance par vidéo/épisode source, non par frame.
- Prévoir ensuite une vidéo extérieure à ce générateur, retenue jusqu'au gel, pour une première vérification de transfert. Ne pas appeler cela « réel » avant réception et vérification de la source.

## Reçu pré-engagé et rejeu
Pour chaque `episode_id × horizon × arm_id` : `source_sha256`, `split`, `frame_ids`, `cutoff`, `view_inputs`, `procedure_ref`, `code_sha256`, `prediction`, `HOLD`, `reason`, `forecast_sha256`, `commit_index`. Écrire l'engagement avant de décoder/révéler la frame cible. Rejeu SHA exact de l'artefact et de l'évaluation. Un simple JSON fabriqué après le futur n'est pas une preuve indépendante du pré-engagement.

## Métriques séparées
1. **Prédiction** : erreur euclidienne du centre en px, médiane, moyenne, quantiles 90/95 et écart par épisode.
2. **Disponibilité** : couverture des prévisions, HOLD corrects/incorrects, abstentions opportunistes; comparer les erreurs à couverture égale ET rapporter les refus.
3. **Reconstruction** : différence dans une ROI objet décidée avant révélation, IoU des masques, fidélité du fond séparée; MAE frame entière seulement comme diagnostic secondaire. Ne pas aligner sur la cible future.
4. **Relations** : orientation, continuité et invariants corrects, séparément de l'erreur pixel.
5. **Coût** : calcul, latence, mémoire et dépendances réellement mesurés, sans supposer qu'une fusion plus complexe est gratuite.

## Règle de verdict
- `P2_PASS_GAIN` : A6 améliore le **meilleur bras isolé sur TEST indépendant**, à couverture comparable, avec amélioration vérifiée sur plusieurs sources/conditions et sans violation d'accès aux données futures. Fixer les seuils quantitatifs et un protocole d'incertitude **avant** la première exécution TEST.
- `P2_NO_GAIN` : aucune amélioration démontrable, ou gain limité à une métrique de fond/à un unique épisode.
- `P2_INCONCLUSIVE` : échantillon insuffisant, variabilité ou dépendance non résolue, comparaison de bras non équitable.
- `P2_BLOCKED` : fuite de futur, provenance non contrôlée, pré-engagement rompu, mismatch de repère/split.
- Si A5 > A6, documenter la **fusion nuisible** ; ne pas effacer ce résultat. Un avantage sur A0 seulement n'est pas un gain multireprésentation.

## Frontières
`WORLD_STATE != MEMORY`; `OBSERVATION != TRUTH`; `CANDIDATE != PROMOTED`. Reverso peut reconstruire une image sans compréhension physique prouvée. Pas de promotion de savoir, d'écriture Native Memory, d'exécution SENS/B8, de mutation GPS ou kernel, ni d'autorité autre que `KX108_ONLY`. Les 4 vues P1 restent 4 projections corrélées d'une unique source synthétique, pas 4 preuves indépendantes.

## Prochaines tâches d'implémentation
1. Inventorier les prédicteurs de `world_transfer_probe_v1` et les formes d'entrées : marquer chaque bras exécutable/non exécutable.
2. Introduire un runner déterministe d'ablations sans dupliquer les méthodes existantes, sorties JSONL/JSON et commandes `--verify`.
3. Ajouter tests de non-fuite, ordre précommit, parité des splits, traitement HOLD, répétabilité SHA et score sans target leak.
4. Exécuter d'abord les tests contractuels et de régression P1, puis seulement la batterie TEST P2 après gel des seuils.
5. Publier uniquement les reçus sur la branche `evidence/brody-local` après contrôle local; aucun push sur `main` via ce protocole.

**À ce stade : zéro résultat P2 revendiqué.**
