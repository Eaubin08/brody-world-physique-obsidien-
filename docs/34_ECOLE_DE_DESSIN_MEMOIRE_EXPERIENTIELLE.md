# 34 — École de dessin Brody : enseignement humain, réciproque et mémoire expérientielle

**Date :** 2026-10-08. **Périmètre :** perception et génération d'images, gestes, progression pédagogique et rétention des expériences. **Statut :** concepts réconciliés depuis Drive + protocole V0 de dessin guidé implémenté ; **pas de World Model visuel général, pas de promotion Native Memory, pas de nouveaux poids.**

## 1. D'où vient vraiment l'idée et ce qu'on n'attribue pas à tort

| Source réelle | Formulation soutenue par le document | Conséquence pour Brody Image |
|---|---|---|
| [FSO — Formule du Savoir Obsidia et apprentissage full auto](https://docs.google.com/document/d/14yk4MPqd5rd3RnB1AAyys8zHU4KD4Dq1eqNtLQFJTA0/edit) — messages **utilisateur** ~lignes 1, 179 | Enfant/école : donner un savoir, apprendre, enregistrer, évaluer sous plusieurs formes ; comprendre les procédés d'apprentissage | Curriculum progressif, démonstration, pratique, évaluation et transferts, plutôt que simple génération répétée |
| FSO, **utilisateur** ~350 | Ne pas réinventer les capacités informatiques de lecture et de création visuelles, employer la réciproque ; plusieurs versions d'entraînement déjà envisagées | Bibliothèques graphiques comme outillage ; méthode d'apprentissage à éprouver, pas construction d'un nouveau décodeur/OS |
| FSO, **utilisateur** ~450 | Isoler un élément, le recréer, le replacer à une autre échelle et ajouter des éléments | Copier/adapter la forme par transformation différenciée de la création de contenu inédit |
| FSO, **utilisateur** ~626 | Respect pixel par pixel *quand demandé*, progression en couches et dans le bon ordre, comme les peintres et l'affichage informatique | Cours silhouette → contour → valeurs → couleur → détail ; master conservé ; mesures par zone et par propriété |
| FSO, **utilisateur** ~767, 1009, 1176, 1275 | Proportions/Fibonacci comme piste ; ressemblance et fidélité à la source malgré style ; règle valable pour tout objet ; respect de l'IN | Symétrie, 360°, grilles, proportion comme **hypothèses/outils optionnels**, jamais critères universels de beauté ou vérité |
| [Éveil OS Cognitif et Apprentissage Organique](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit) | **Synthèse de l'assistant historique**, pas verbatim : invariants dynamiques, analyse/synthèse, modalités, Continuum / Zone Latente, friction symbolique | Lire comme source de vocabulaire et pistes, pas comme une implémentation prouvée |
| [Architecture du système de mémoire — L'Expérience](https://docs.google.com/document/d/1SdeEtK9zpZoAgnyTSQtjbwTYO0cDG3_iFqgBof5kRPA/edit) | Texte d'architecture : mémoire vive/Map FIFO, archive diachronique, chaîne scellée, apprentissage post-mortem/RFE et correction | Séparer les traces de tentative et mémoire stable, garder échecs, historique et références ; **ne pas confondre son Merkle conceptuel avec la réalité de Native Memory actuelle** |
| [Protocoles fondateurs / méthodes de création](https://docs.google.com/document/d/1R-BkkUUknUUs-C0rUA6LwBAISGIGwx3P8ycOojbjzOk/edit) | Plusieurs sens d'AVDR, tension active, cristallisation par répétition, zones de non-savoir, mémoire des chemins non pris | Tester variations et chemins échoués. **Aucune ancienne expansion de sigle ne remplace l'AVDR canonique actuel.** |
| [Civilisation Cognitive Complète](https://docs.google.com/document/d/14WUSNQPcZ4MsNP0lfpHT2PkfEJxiHhGvdcdNefqSbOE/edit) | Nombreuses familles spécialisées de développement cognitif et propositions de versions d'entraînement | Les « 81 / 100+ » versions sont à **auditer une à une** avant raccord ; ne pas fabriquer de catalogue imaginaire à partir de ce seul nombre |

**Règle U/A/P :** `U` = énoncé réellement retrouvé de l'utilisateur ; `A` = réponse ou synthèse IA historique ; `P` = protocole technique proposé/écrit ici. [Audit de traçabilité déjà existant](23_BRODY_IMAGE_LEARNING_TRACEABILITY.md). Les liens Drive sont des archives primaires ou secondaires, pas des preuves de capacités runtime.

## 2. Une vraie pédagogie du dessin, sans fausses promesses

Le rôle du professeur (externe au learner) est de proposer un **cours** et un **modèle visible**. Le rôle de Brody est d'essayer de tracer, d'observer ses écarts, de corriger, puis d'essayer **un autre exemple** qui ne figurait pas dans ses souvenirs.

| Niveau du cursus cible | Exercice et compétence à mesurer | Type d'épreuve |
|---|---|---|
| **D0 — Geste** | Crayon, direction, longueur, précision et maîtrise du trait | Reproduire un trait montré ; recommencer après feedback |
| **D1 — Formes** | Cercles, lignes, triangle, carré, courbe, proportions et fermetures | Copier une forme jamais dessinée à cette position |
| **D2 — Assemblage** | Croquis composé de primitives, parties, voisinages et occlusions | Reproduire une petite scène plutôt que chaque point isolé |
| **D3 — Couche peintre** | Global → masses → valeurs/ombres → contours/couleurs → détails | Comparer les couches et contrôler l'IN/source |
| **D4 — Reverso** | Image → décomposition → reproduction → rétro-observation | Mesure fidélité exacte vs structure/identité selon exigence |
| **D5 — Variations** | Symétrie, rotations 360°, taille, perspective, Fibonacci/grilles **au choix** | Même concept inconnu vu autrement ; invariants conservés |
| **D6 — Imagination contrôlée** | Image partielle, chemin alternatif, hypothèses multiples, absence de données | Génération candidate + incertitude et comparaison à une référence révélée après |
| **D7 — Temps / monde** | Image puis état futur dans un repère physique ; retour vidéo | Transfert d'une compétence de dessin et comparaison temporelle |

**Un professeur réel n'enseigne pas une seule façon de dessiner.** Il faudra tester observation-copie, dessin de mémoire, dessin par construction, geste guidé, essais libres, correction humaine, comparaison de styles et apprentissage par exercices inverses. Tous ces modes ne sont **pas** encore codés. Le bon critère est « se corrige-t-il et réutilise-t-il une compétence ailleurs ? », pas le nombre d'exemples stockés.

## 3. Ce que V0 réalise véritablement

[`brody_world_physique/drawing_school_v0.py`](../brody_world_physique/drawing_school_v0.py) propose un **premier cours visuel D0–D1**, avec **Pillow** pour la feuille blanche et le crayon. Les scènes sont synthétiques ; les étiquettes « trait, carré, triangle » appartiennent au professeur et **ne sont pas fournies au copieur**.

1. Le professeur **montre un dessin 64×64** et l'enregistre dans `teacher_images/`. Sa somme SHA-256 est la référence non modifiée.
2. Le débutant a une feuille blanche. Il peut produire **des segments de crayon** (le catalogue de gestes est un outil préprogrammé, pas une forme enseignée).
3. Il sélectionne le segment qui réduit le plus les erreurs noir/blanc par comparaison à l'image référence, trace, mesure, recommence avec un budget limité de corrections.
4. Il garde sa **séquence de gestes** comme *skill candidate* locale ; elle n'est pas une loi ni un apprentissage de poids neuronal.
5. Devant des **examens jamais utilisés pour fabriquer la mémoire**, il consulte les signatures visuelles grossières et réemploie les gestes d'un exercice proche, transposés à la nouvelle position. Il compare cette première copie au **témoin à mémoire vide**, puis peut corriger par feedback.
6. Il sauvegarde des PNG : source du professeur, première tentative, copie initiale de mémoire et reprise corrigée. Aucune vidéo n'est nécessaire pour apprendre ces gestes.
7. Il écrit des événements distincts dans une **chaîne locale JSONL chaînée SHA-256**, vérifiable contre les modifications accidentelles : observation, corrections et suggestion de compétence. Ce **n'est pas** le Merkle Seal historique ni une authentification sécurisée.

### Premiers résultats exécutés en CI — essai guidé sur images synthétiques

Sur quatre **nouvelles références visibles** (64 × 64 px), après trois leçons et en mode comparateur de pixels, l'erreur est le nombre de pixels noirs/blancs non conformes à l'exemple. Ce **n'est pas** une métrique perceptive ni un apprentissage de style :

| Examen | Page blanche | Souvenir brut | Souvenir accepté | Après correction |
|---|---:|---:|---:|---:|
| 01 — trait déplacé | 123 | 0 | 0 | 0 |
| 02 — contour déplacé | 380 | 0 | 0 | 0 |
| 03 — forme oblique | 316 | 168 | 168 | 168 |
| 04 — forme inconnue | 393 | **659 (mauvais rappel)** | **393 (rejet du rappel)** | 0 |

**Le contre-exemple 04 est conservé :** une compétence rappelée donne initialement **plus d'erreurs qu'une feuille blanche**. Le système écrit `FAILURE_PATTERN_CANDIDATE` avec l'erreur brute et refuse ce transfert préjudiciable avant de recommencer à dessiner depuis une feuille blanche. Il ne supprime pas le souvenir original ni la trace de cet échec. Le cas 03 montre aussi une limite : **aucune amélioration malgré la correction proposée**, car le crayon actuel n'a pas encore une véritable gomme / révision des gestes anciens. Ces résultats sont des tests de **copie guidée de primitives préparées par un humain**, et non de création visuelle libre.

La chaîne candidate locale enregistre **26 événements** dans cette exécution ; sa vérification d'intégrité a réussi. Les **113 tests** de l'ensemble du dépôt ont passé Python 3.11 et 3.12 lors de [l'exécution CI](https://github.com/Eaubin08/brody-world-physique-obsidien-/actions/runs/37842164590), et la démo Pillow a été exécutée sur GitHub. La reproduction locale Windows reste à vérifier séparément.

**Ce qui est encore programmé :** l'outil de trait, la fonction d'erreur, la recherche gloutonne des traits, la normalisation d'échelle/position, la signature visuelle et la sélection de souvenir proche. Le V0 n'apprend pas les lois de l'image, la profondeur 3D, un concept verbal ni la meilleure méthode d'étude. Il n'a pas de mémoire de poids entraînés. Le professeur corrige explicitement par la comparaison à la référence. Toute affirmation « il apprend tout seul à partir de rien » serait fausse.

## 4. Où va chaque type de mémoire — et surtout où il ne va PAS

Conserver **source + IN + essai + erreur + correction + test de réemploi + statut** :

| Classe | Contenu retenu | État V0 |
|---|---|---|
| Source / maître / IN | Image originale, SHA-256, consignes de fidélité | `teacher_images/` + SHA, sans écrasement |
| Mémoire de travail (candidats) | Geste courant, dessin actuel, résultat et prochaine correction | Tentatives locales, pas Map FIFO Obsidia native |
| Épisodique | Leçon vécue et ordonnée, erreurs avant/après, méthode, reçus | `candidate_experience_ledger.jsonl`, chaîne vérifiable, **non canonique** |
| Compétence / geste | Dessin de segments appris, signature source, conditions d'usage | `candidate_skill_memory.json`, **proposition de réemploi** |
| Échec / friction | Retard, erreur qui augmente, action refusée, piste non suivie | Erreurs conservées ; politique avancée de chemins non pris non implémentée |
| Invariant | Ce qui se maintient sur plusieurs sources, rotations, styles et angles | **Non promu :** essais répétés et validation indépendante manquants |
| Hypothèse / zone blanche | Règle suspectée, cas jamais rencontré, zone inconnue | Candidat à formaliser, pas vérité ni action |
| Mémoire diachronique / Native Memory | Conservation gouvernée selon contrats Obsidia | **AUCUNE ÉCRITURE** ; nécessité d'un audit du contrat réel avant raccord |

Une **compétence candidate** doit franchir des tests séparés : `premier dessin`, `correction`, `nouvelle référence`, `transfert stable sur plusieurs contextes`, `source vérifiée`, `revue de promotion`. Aujourd'hui seules les premières étapes sont implémentées. Comme le spécifie [05 — mémoire existante](05_LEARNING_MEMORY.md), une image copiée n'est pas un savoir général.

### Invariants de gouvernance

- `KX108_ONLY`, `memory_write=False`, `kernel_mutation=False`, `emits_act=False`. Aucune modification de Sigma, Binder, Graphiti (obsolète runtime) ou Native Memory.
- Les sorties sont **SIMULATED / CANDIDATE**, pas `validated_world_knowledge`.
- L'original et l'intention ne sont jamais réécrits par la correction de l'élève ; toute solution plus libre exige une intention différente.
- Une erreur n'est ni supprimée ni présentée comme succès ; le transfert sur nouvelles références, l'abstention et les contre-exemples font partie des preuves.
- Pas de fusion forcée avec la doctrine FSO/AVDR antérieure ; vérifier les définitions historiques face au canon du projet.

## 5. Commande pour reproduire sur le PC Windows

Dans `C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image` après `git pull --ff-only origin main` :

```powershell
$out = "build\ecole-dessin-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.drawing_school_v0 --out $out
Invoke-Item $out
```

Ouvrir `teacher_images/` (les modèles), `attempts/` (les copies et corrections), `candidate_experience_ledger.jsonl`, `candidate_skill_memory.json` et `evaluation.json`. La commande ne dépend que de Pillow (déjà déclaré dans `requirements-image.txt`), fonctionne hors ligne et ne télécharge aucun poids ni dataset. Il faut **vérifier la progression sur le PC** ; les exemples synthétiques ne démontrent pas un cours d'art généralisé.

## 6. Ensuite, et seulement après les résultats

- **D1 courbes / vrai cercle :** moteur de traits courbes avec gestes réutilisables et comparaison silhouette/contour.
- **D2 objets** : pomme, tasse, cube, composition par parties et préservation de l'objet sur des décors différents.
- **D3 couches** : masse globale puis lumière/couleur/détail, rétrocroisement Reverso selon profils LOCK/FLEX et IN.
- **D4/D5** : symétrie, 360°, rotations hors plan (multi-vues sourcées), proportion et Fibonacci comme option de composition à valider, pas contrainte universelle.
- **Mémoire réelle** : auditer le contrat Native Memory effectif sur les branches canoniques, puis créer un **adaptateur en lecture seule** pour rejouer les épisodes, et un chemin d'écriture **soumis à autorisation explicite** à part, s'il est justifié.
- **Méthodes d'entraînement multiples** : relire les archives « 81 versions et + » pour une cartographie fidèle avant d'en choisir certaines ; ne jamais affirmer que toute la famille existe en runtime.
