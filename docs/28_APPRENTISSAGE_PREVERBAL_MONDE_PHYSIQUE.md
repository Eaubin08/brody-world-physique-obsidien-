# 28 — Brody : expérience préverbale, représentation du monde et émergence du savoir

**Date :** 2026-10-08 · **Statut :** clarification conceptuelle issue de l'utilisateur + protocole expérimental **proposé**, PAS implémentation d'un world model apprenant.  
**Périmètre :** Brody Image / monde physique. Ne pas détourner vers un assistant textuel général ni inventer 81 entraînements.

## 1. Correction formulée par l'utilisateur (U, conversation 2026-10-08)

L'idée directrice est qu'un enfant peut **anticiper une conséquence** avant de connaître les mots, les équations ou les explications qui permettent de la nommer. Il voit un objet tomber, essaie, observe ce qui suit, et développe une compréhension pratique. Ses capacités initiales et son histoire d'expériences se combinent. Il ne faut donc pas concevoir le savoir de Brody comme une encyclopédie de descriptions ni exiger un passage par le langage pour chaque apprentissage.

L'utilisateur demande de prendre réellement en compte : **vent, physique, biologie, microscopie, chutes d'objets, environnement, localisation GPS physique**, la position relative dans le monde et les échelles. Il veut reconnecter cela aux outils déjà construits dans Obsidia, avec analyse/réciproque, plutôt que réinventer l'affichage des pixels ou les routes de calcul du système d'exploitation. Il rapproche l'organisation associative des connaissances de la **branche des 34 arbres**, mais pour la représentation physique des objets et de leurs relations : **analogie d'architecture, pas identité des schémas ni import direct des règles cognitives**.

Il insiste sur la distinction entre **comprendre, savoir, vérité et degré de certitude**. Le raisonnement peut avancer en conditions d'incertitude : prédire utilement n'est ni nommer une loi, ni établir la cause avec certitude.

**Sources précédentes :** [23 — apprentissage](23_BRODY_IMAGE_LEARNING_TRACEABILITY.md), [24 — fidélité/reconstruction](24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md), [27 — Reverso + tri](27_REVERSO_WORLD_MODEL_APPRENTISSAGE_SELECTIF.md), [05 — expérience/mémoire](05_LEARNING_MEMORY.md) ; [FSO — archive primaire](https://docs.google.com/document/d/14yk4MPqd5rd3RnB1AAyys8zHU4KD4Dq1eqNtLQFJTA0/edit) (U ~179 enseignement/humain-école, U ~350 réemploi des capacités visuelles, U ~450/626 réciproque et isolation, U ~1275 respect de l'original). Le présent complément *préverbal et physique* provient de la précision exprimée par l'utilisateur aujourd'hui ; les algorithmes plus bas sont des **propositions P**.

## 2. Capacité avant le mot : trois niveaux non interchangeables

**A. Compétence préverbale candidate :** une représentation capteur/temps/espace/objet et un modèle de transition permettent d'anticiper « si cet objet est lâché, sa position peut évoluer vers le sol » sans émettre de phrase ni connaître le mot *gravité*. L'absence de texte ne dispense pas de vérifier la prédiction contre l'observation.

**B. Concept explicitable :** après un nombre approprié d'expériences, des catégories et mots (tomber, rebond, vent, lourd) peuvent étiqueter une régularité. Un label du modèle linguistique ne prouve pas l'existence du mécanisme.

**C. Savoir transférable :** reconnaître l'invariant ou la relation dans une scène différente, avec preuve de source, conditions d'application et incertitude ; échouer proprement quand la situation excède les observations. La loi physique formalisée peut intervenir **plus tard**.

Un enfant réel ne naît pas avec une liste complète des lois ; ses dispositions perceptives et motrices, puis les expériences, interagissent. **P (ingénierie)** : pour Brody, les prédispositions sont des biais/compétences initiales bornées (continuité temporelle, séparation candidat objet/fond, suivi, comparaison, attention au changement, hypothèses concurrentes), jamais des faits physiques gravés comme vérité.

## 3. Réutiliser l'informatique et les organes existants

- **Pixel / binaire / écran :** Windows, codecs et bibliothèques graphiques assurent déjà le décodage/rendu. Reverso V0 (64 tuiles sur le test utilisateur ; `PASS_EXACT_DECODED_RGBA`) prouve une reconstruction **de pixels décodés**, pas l'apprentissage de la physique. Ne pas rebâtir un OS graphique. Son intérêt est la **référence exacte/round trip** servant de contrôle.
- **Vision candidate :** Qwen-VL, déjà utilisé avec Jarvis et appelé avec succès depuis le PC fixe, permet des descriptions candidates mais pas des masques/object-tracks, vérités ni lois à lui seul.
- **MMonde / F16 / F12 :** réutiliser les **contrats amont** pour sources visuelles, objets/relations situées, temps, transformations et trajectoires ; pas de nouvel `WorldState` racine dans le dépôt image.
- **GPS / GNSS :** une position mesurée (avec repère, timestamp, précision, confiance, qualité et limites du signal) peut donner un **ancrage spatial** à l'expérience ; ne garantit pas la vérité ni n'explique la gravité. Réutiliser les sources GNSS existantes lorsque disponibles et pertinentes, sans transférer l'autorité du domaine GPS vers une nouvelle ontologie.
- **Biologie / microscopie / autres échelles :** sources d'observations et de modèles spécialisés, liées par les relations et preuves, **pas de capteurs imaginés ni de données fabriquées**.
- **Native Memory :** histoire/savoirs/compétences candidats avec source; **aucune écriture ou promotion automatique**. **KX108_ONLY**, Binder et kernel inchangés.

### Analogie des 34 arbres, sans assimilation abusive

L'idée de rapprocher des signatures, objets, invariants et relations de multiples « branches » ou domaines doit être évaluée sur **retrieval**, association transversale et mise à jour d'expérience. Le document historique [Shazam / 34 arbres](https://docs.google.com/document/d/1KshgP97PKdTZAfRxe9-YfcVnIJceKbgGCyxC-HdRj18/edit) porte initialement sur la détection de profils d'intention à partir de caractéristiques de texte/voix ; il ne constitue **pas** déjà une base physique ni un algorithme vérifié pour le monde.

## 4. Schéma cible : expérience → prédiction → erreur → transfert

```text
PHOTO / VIDÉO / GPS / SOURCES PHYSIQUES / MICROSCOPIE (selon disponibilité)
        |
        v
OBSERVATIONS SOURCÉES + TEMPS + REPÈRE + INCERTITUDES
        |
        v
OBJETS / ÉTATS / RELATIONS / CONTINUITÉ (MMonde, F16, F12)
        |
        +----> ANTICIPATION PRÉVERBALE : état suivant plausible
        |                      |
        |                      v
        |              EXPÉRIENCE / OBSERVATION NOUVELLE
        |                      |
        |                      v
        |              ÉCART / CONTRE-EXEMPLE / INCONNU
        |                      |
        +------------- RÉVISION DU MODÈLE CANDIDAT
                               |
                   NOUVEAU CONTEXTE / TRANSFERT
                               |
                       REVUE / SAVOIR CANDIDAT
                               |
                   MÉMOIRE NATIVE SI AUTORISÉE
```

Reverso reste une **route de reconstruction et de contrôle**, associée au même objet/source/IN; il n'est ni la condition suffisante de compréhension ni l'organe unique d'apprentissage.

## 5. Épistémologie à conserver dans le runtime futur

| Niveau | Exemple | Ce qu'il n'autorise PAS |
|---|---|---|
| `OBSERVED` | Dans deux frames sourcées, la position de la balle change | Affirmer pourquoi elle a bougé |
| `INTERPRETATION_CANDIDATE` | Qwen propose « balle », « sol », « chute » | Déclarer l'objet/événement prouvé |
| `PREDICTION_CANDIDATE` | La prochaine position prévue est plus basse | Transformer un scénario plausible en vérité |
| `MODEL_EXPLANATION_CANDIDATE` | Hypothèse : effet de la gravité | Ignorer le mouvement caméra ou d'autres causes |
| `SUPPORTED_SKILL_OR_KNOWLEDGE_CANDIDATE` | Prédiction généralisée après épisodes indépendants | Étendre au-delà des conditions vérifiées |
| `VERIFIED_FACT_WITH_SCOPE` | Mesure répétée, source/test adéquats et domaine précisé | Déclarer une certitude absolue/universelle |

**Vérité** = correspondance avec le monde (indépendante de l'affirmation du système). **Savoir** = croyance/compétence suffisamment étayée et bornée par ses justifications; **compréhension** = capacité de représenter/expliquer/anticiper/manipuler des situations; **confiance** = quantité subjective ou calibrée qui peut être élevée alors même que la proposition est fausse. Ce sont ici des **distinctions de conception**, pas la prétention de trancher toute l'épistémologie.

## 6. Premier protocole expérimental P (avant toute déclaration d'apprentissage)

1. Donner une **séquence temporelle réelle ou filmée avec source**, pas une photo seule, montrant une balle tenue puis relâchée ; relever timestamps, position et contexte. Distinguer observation réelle, vidéo de laboratoire et rendu synthétique.
2. Faire proposer l'**état suivant sans réponse verbale obligatoire** : sortie d'une position/trajectoire et de son incertitude; comparer avec une frame ultérieure **non fournie au prédicteur**.
3. Déplacer le point de vue ou modifier un paramètre (balle de taille différente, support/vent, caméra en mouvement). Vérifier si la régularité apprise **se transfère** ou s'il faut réviser.
4. Conserver séparément la source, la prédiction, l'erreur, les conditions et les candidats « règle/compétence ». Rejouer des épisodes et comparer une nouvelle tentative à la version précédente; ne pas présenter la réduction d'une erreur unique comme une acquisition validée.
5. Tester l'**apport réel** des signaux supplémentaires (position GPS, direction du vent ou autres mesures uniquement quand disponibles) avec/sans les signaux, pour savoir s'ils améliorent les prédictions, plutôt que les exiger pour chaque image.
6. Expérimenter « mémoire sélective vs historique brut » : mesurer coût, déduplication, réussite sur situations nouvelles, échecs connus évités, et capacité d'explication. **Ne pas présumer que la méthode proposée de tri 27 est la règle finale.**

**Critères de preuve** : score prédictif vs baseline, généralisation hors exemples vus, provenance, séparation mouvement objet/caméra, erreurs calibrées et replay indépendant. `NOT_RUN` tant que les vrais tests n'ont pas eu lieu.

## 7. Gates et frontière d'implémentation

| Capacité | État au 2026-10-08 |
|---|---|
| Image → Qwen local PC réel → description | **TESTÉ PAR L'UTILISATEUR** ; répétitions/hallucinations possibles |
| Reverso lossless → reconstruire RGBA décodé | **TESTÉ SUR PHOTO UTILISATEUR**, 64 tuiles, empreinte source/reconstruction identique |
| État spatio-temporel / contrats F16, F12, MMonde | **EXISTENT DANS D'AUTRES DÉPÔTS**, raccord image à prouver |
| Prédiction préverbale à partir de frames réelles | **NON IMPLÉMENTÉE / NOT_RUN** |
| Référentiel GPS + physique + échelles biologiques | **ARCHITECTURE À MAPPER**, aucun modèle unifié opérationnel prouvé |
| Reverso sémantique / nouveaux points de vue / génération conditionnée | **NON IMPLÉMENTÉ / NOT_RUN** |
| Révision de modèle basée sur expériences et mémoire sélective | **POLITIQUE CANDIDATE SEULEMENT**, pas d'entraînement ni d'écriture mémoire réelle |

**Règle de priorité** : ne pas dépenser un sprint sur une nouvelle reproduction de pixels ou un meilleur prompt Qwen tant que l'**épisode préverbal avec changement réel, prédiction, écarts et transfert** n'a pas été cadré avec ses sources et ses métriques. Prévoir ensuite les adaptateurs capteurs pertinents.
