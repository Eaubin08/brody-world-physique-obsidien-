# 21 — BRODY IMAGE : PLAN MAÎTRE VISUEL / APPRENTISSAGE / GÉNÉRATION

**Date :** 2026-10-08 · **Position :** document directeur pour ce dépôt · **État :** DESIGN / GATES NON GELÉS · **Aucune installation modèle ni modification des autres dépôts.**

## 1. Mission, objet du projet

Le but principal est de faire évoluer **Brody Image** :

1. **voir** des images réelles, vidéos, écrans ou scènes simulées ;
2. **décomposer** les objets, formes, éléments visuels et relations ;
3. **comprendre et apprendre** les invariants d'identité, de forme, de mouvement, d'espace et de conséquence, y compris avant de savoir formuler la loi scientifique générale ;
4. **générer / reconstruire / modifier** des images pertinentes à partir de la représentation acquise ;
5. **re-percevoir, comparer, corriger** les résultats et capitaliser uniquement des épisodes d'apprentissage admissibles.

**Analogie originale conservée :** un enfant reconnaît le déplacement puis la chute d'un objet avant de connaître l'équation de la gravité. Ne pas confondre une corrélation apprise avec une loi physique prouvée.

L'Atlas Obsidia à 108 entrées et les archives ont le rôle **bibliothèque de concepts au service du moteur image**. Ils ne deviennent ni la roadmap centrale ni un critère de complétion d'un modèle visuel.

### Sources de la vision

- [Doctrine fondatrice locale](00_VISION_DOCTRINE.md) et [architecture visuelle initiale](01_ARCHITECTURE.md).
- [Document personnel — Éveil de l'OS cognitif](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit) : invariants ρ, analyse ↔ synthèse, génératif procédural, FaceLock comme **vision à tester**, pas fonctionnalité déjà disponible.
- [Framework de décomposition du corpus visuel](https://docs.google.com/document/d/14eT3B2ZTD15DiSRKSNUjpfaRZQBj3LSmwW8QaIPUgKI/edit).
- [Shazam cognitif / 34 arbres](https://docs.google.com/document/d/1KshgP97PKdTZAfRxe9-YfcVnIJceKbgGCyxC-HdRj18/edit) : filiation conceptuelle possible, **pas** un moteur de fingerprint visuel démontré.
- [Reverse OS](https://docs.google.com/document/d/1L_LG0UE4vyLn-iXF0pvjc94owZCI3McF2SWJo3TG8nY/edit), dont l'usage image est une **extension future**, non déjà une route générative.

## 2. Le pipeline cible, image en premier

```text
INPUT : image réelle / vidéo / caméra / capture écran / scène de labo
       |
       v
A. INGRESS + PROVENANCE (sépare RÉEL / SIMULÉ / GÉNÉRÉ)
       |
       v
B. PERCEPTION
   yeux spécialisés : description si nécessaire, segmentation, depth,
   tracking, features; chaque résultat reste candidate / uncertain
       |
       v
C. IR VISUEL DÉRIVÉ (sur F16), MMonde, espace/temps et identité
       |
       v
D. BRODY — lecture / rapprochement / hypothèses / invariants
       |                     |
       v                     v
E. APPRENTISSAGE         F. PLAN DE GÉNÉRATION
   transitions,             propriétés LOCK/FLEX/IGNORE,
   expériences candidates   référence de scène, contraintes
       |                     |
       |                     v
       |                G. GENERATOR ADAPTER
       |                  image / édition / multivues / vidéo future
       |                     |
       |                     v
       +----------- H. ARTEFACT GÉNÉRÉ (pas preuve du réel)
                             |
                             v
                     I. RE-PERCEPTION + CONTRÔLES
                       identité, proportions, profondeur,
                       présence/absence, conséquences
                             |
                             v
                     J. ÉCARTS + REPLAY + CORRECTION
                             |
                             v
                     K. CANDIDAT D'EXPÉRIENCE
                       (pas écriture mémoire automatique)
```

**Pas de nouvelle ontologie image concurrente** : `VisualIR` décrit au plus une vue dérivée sur `RealImageObservationV0 / VisualPrimitiveV0 / WorldObservationV0`, selon [contrats F0](02_CONTRACTS.md). Les images *générées* empruntent un contrat `GeneratedArtifactV0` distinct ; elles ne doivent jamais être introduites sous `RealImageObservationV0` (`generated=true` y est rejeté).

**Contrainte Brody :** Brody est l'organisateur / interprète interne. Les outils visuels externes sont des organes remplaçables. Ne pas empiler par défaut plusieurs LLM de dialogue ; Qwen-VL, **si déjà calibré et disponible**, est un prestataire de perception optionnel via l'entrée locale Jarvis. Aucun nouveau LLM général requis pour F1.

## 3. Concepts utilisateur sélectionnés **par utilité à l'image**

| Concept | Fonction dans la boucle image | Source / développement | Niveau actuel |
|---|---|---|---|
| **Analyse ↔ Synthèse** | Décomposer le réel puis reconstruire et comparer | Source utilisateur Éveil de l'OS | direction documentée, pipeline image complet non branché |
| **Invariants visuels ρ** | Distinguer identité conservée, attribut modifiable, erreur | source Éveil ; `VisualInvariantV0` projet | contrat cible non implémenté en F0 |
| **Invariant dynamique** | Continuité objet / changement légitime sur vidéo | F12 + EfficientTAM candidat | F12 existe, tracker non intégré |
| **Signature / Shazam** | Pistes de reconnaissance structure/motif ; pas pixel-hash seulement | 34 arbres + décomposition corpus | hypothèse VisualFingerprint, métriques non démontrées |
| **Espace / temps / transformation** | Décrire scène et trajectoire, éviter causalité inventée | MMonde/F12 / expérience F0 | contrats de représentation trouvés |
| **Quadrillage du monde** | Situer chaque expérience dans espace/temps/relations | idée utilisateur, formulation précise à archiver | filiation MMonde partielle, non prouvée |
| **Reverse360** | Tester survie de l'identité sous changement de point de vue | architecture visuelle du dépôt | validation à construire |
| **Friction / évaluation** | Rejeter changements incohérents et conserver erreur utile | corpus utilisateur et ReverseEvaluation | mécanisme projet, pas test établi |
| **Mémoire / expériences** | Retenir contexte et échecs validés, pas images brutes ni vérité | Native Memory + Candidate | source présente ; bridge image non réalisé |

**Audit ciblé de la vision image — SOURCE/IN → COUCHES → RIGUEUR → GÉNÉRATION :** [24 — Audit de fidélité Brody Image et spécification fonctionnelle](24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md). Ce document tranche les écarts documentaires **propres à l'image** (méthode du peintre, source non dénaturée, verrous par zone, identité de tout objet, restitution vs diffusion, tests BIMG). **Il prime pour le périmètre Brody Image** sur les détours d'archives liés aux 81 versions générales.

**Contrôle de fidélité avant forge :** [23 — Traçabilité des méthodes d'apprentissage vers les tests](23_BRODY_IMAGE_LEARNING_TRACEABILITY.md). Les méthodes **isolation/restitution/transposition**, **Fibonacci et grilles de composition**, **curriculum humain**, **variantes d'entraînement**, et **non-répétition des échecs** ont des voies et tests séparés. Il s'agit de cibles documentées, non de fonctions implémentées ; la source historique des **81 combinaisons théoriques (9 × 9)** a été retrouvée dans l'archive *Civilisation Cognitive*, mais la liste finale approuvée et les extensions 81+/90/100 restent à réconcilier (voir §6 du document 23).

**Secondaires maintenant :** GNSS/RF, reconnaissance gestuelle, interface Pokémon, agents bureaucratiques, ERA, AVDR/Gencoin, anciens packs scientifiques. Ils peuvent fournir un contrat, une preuve ou une interface, mais **ne dirigent pas la roadmap image**. **Trading hors périmètre.**

## 4. Deux voies de réalisation en parallèle

**Voie V — comprendre les images :**
image test réelle → F16 observation → adapter vision/masque/profondeur → primitives/relation MMonde → Brody → invariants + hypothèses.

**Voie G — produire les images rapidement :**
`GenerationIntentV0` cible → générateur via `GeneratorAdapter` → image/seed/version/hash → `GeneratedArtifactV0` (généré uniquement).

**Réunion V+G :**
demander à Brody « conserve le même objet et ses proportions, change seulement l'éclairage », générer deux variantes, mesurer ce qui est vraiment resté constant. L'apprentissage commence par la différence constatée et l'adaptation de la route/stratégie, **pas** par une prétendue réécriture automatique des poids de Brody.

Ainsi la **première image générée et son retour visuel arrivent tôt**, sans attendre d'avoir construit Dreaming, toute l'éducation Obsidia ou le monde physique global.

## 5. Roadmap révisée — spécifique image (ordres de chantier)

| Gate | Travail | Résultat exigé | Interdiction |
|---|---|---|---|
| **I0 — CARTO / FREEZE IMAGE** | Sources, branches, composants, contrats, licences, matériel PC | carte de branchement et tests de référence approuvés | pas de téléchargement massif ni nouveau runtime |
| **I1 — PREMIER ŒIL** | image réelle + observations sourcées ; description/masque/depth optionnels | JSON visuel candidate avec refs/erreurs, 1 image réelle | pas de vérité automatique |
| **G1 — PREMIÈRE GÉNÉRATION** | 1 moteur et 1 modèle compatibles avec le PC | image reproductible + modèle/poids/seed/hash | pas de sélection matériel inventée |
| **IG2 — BOUCLE MINIMALE** | Brody impose LOCK/FLEX/IGNORE ; G1 produit, I1 re-lit | rapport de violation sur 2–3 transformations | pas d'apprentissage proclamé sur une simple démo |
| **I3 — IDENTITÉ / VIDÉO** | masques, tracking, relation de frames, signature candidate | suivi sur occlusion/rotation et métriques de continuité | aucun face-ID automatique |
| **I4 — SCÈNES / TRANSITIONS** | monde(s) de labo, force/trajectoire/point de vue, EB-JEPA éventuel | prédiction puis comparaison à état observé indépendant | hypothèse != causalité prouvée |
| **I5 — EXPÉRIENCE RÉUTILISABLE** | épisode validé, deltas, replay, règles/stratégies | même erreur de génération mieux corrigée après contexte validé | mémoire sans promotion automatique |
| **I6 — REVERSE360** | WorldFM ou équivalent sous contrôle de licence | vues multiples, identités/proportions contrôlées | image créée != observation réelle |
| **I7 — VIDÉO / GÉNÉRALISATION** | invariant dynamique, génération vidéo optionnelle | cohérence multi-frames, drift mesuré | pas de promesse généralisation sans benchmark |
| **I8 — INTERFACES** | Jarvis capteur, Monde écran d'inspection ; éventuellement GPS capteur | adaptateurs typés + test cross-repo | pas de fusion automatique ni pouvoir ACT |

**Relation à l'ancien plan :** [docs/06_FORGE_PLAN.md](06_FORGE_PLAN.md) reste le calendrier historique F0–F10 ; cette feuille **I/G** est l'ordre prioritaire pour le chantier image. F0 des contrats décrit les fondations et n'est pas, à lui seul, un système de vision/génération testé.

## 6. Démonstrations et tests utiles

**Démonstrateur A :** balle dans trois images : chute réelle vs mouvement de caméra ; identité, position, temps, source et causalité `UNKNOWN` tant que non prouvée. Mesurer localisation, erreurs, conservation des contradictions.

**Démonstrateur B :** un objet de référence → génération « change la lumière » / « change l'angle » → re-détection → comparaison des proportions, forme et relations conservées. S'il n'est pas observablement comparable, marquer `EVALUATION_INCONCLUSIVE`, non PASS.

**Démonstrateur C :** même objet au cours de vidéo avec occlusion ; tracking et invariants dynamiques avant de parler de génération vidéo.

**Métriques minimales :** taux de LOCK conservés, taux de changements FLEX corrects, faux ajouts/suppressions, erreur de masque/position/depth si vérité de référence, continuité d'identité, robustesse aux vues, ratio inconnus/erreurs justifiés, reproductibilité par seed, durée/VRAM/RAM mesurées.

## 7. Les éléments qui empêchent le gel et le build

- Confirmation du matériel PC réel et versions/poids open source licites pour usage envisagé.
- Création d'adapters image explicites et testés ; les fonctions upstream actuelles ne constituent pas ce pipeline.
- `VisualInvariantV0 / VisualFingerprintV0 / GenerationIntentV0 / GeneratedArtifactV0 / ReverseEvaluationV0` : **cibles**, pas déjà actives.
- Vérification du trajet Jarvis → Brody pour données multimodales ; le fournisseur Qwen-VL décrit dans Jarvis n'est pas une preuve qu'il tourne sur PC.
- Politique de passage des épisodes à la Native Memory (`WORLD_EXPERIENCE` absent de l'enum auditée).
- Références exactes, statut de licence et tests de non-contamination si tout composant image est ensuite envisagé pour GPS/Défense.

**Voir [22 — Carte de branchement réelle](22_IMAGE_BRANCH_AND_DONOR_MAP.md).** Le code source, le contrat, le modèle tiers et le statut de connexion ne doivent plus jamais être présentés comme un seul « module prêt ».
