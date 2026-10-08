# 24 — Audit de fidélité : vision de Brody pour apprendre et générer des images

**Date :** 2026-10-08 · **Branche :** `main` · **Périmètre :** **Brody Image uniquement** (images, édition, reconstruction, premières notions de vidéo et monde physique visuel).  
**Statut :** audit ciblé, spécification de comportement et plan de tests ; **aucun moteur de génération ou apprentissage visuel end-to-end validé**.

## 0. Verdict de l'audit : ce que décrivait réellement l'utilisateur

Brody Image **n'est ni un simple chatbot avec caméra ni un filtre diffusion text-to-image**. La cible décrite par l'utilisateur est un système qui :

1. **prend un réel ou une référence** et en isole les éléments utiles ;
2. **décompose correctement** les sujets et leurs caractéristiques (formes, proportions, identité, relations, perspectives, lumière) ;
3. **retient ce qui doit rester fidèle** à la source et à l'**IN (intention) utilisateur**, propriété par propriété et zone par zone ;
4. **reconstruit** le sujet à partir de cette analyse, **puis** le déplace, modifie, ajoute ou combine avec un autre décor ;
5. choisit **la bonne séquence de travail** (référence utilisateur à la peinture traditionnelle, au rendu informatique et aux couches) au lieu de faire d'emblée une création globale ;
6. accepte une **liberté variable** — restitution stricte, rendu photo, manga, autre style artistique — tout en respectant les invariants réellement demandés ;
7. **réobserve et compare** les résultats, puis apprend des erreurs vérifiées sans prétendre connaître une loi physique ou modifier automatiquement ses poids ;
8. étend le raisonnement aux **angles de vue, au temps et aux changements réels** quand les observations le permettent.

**Résultat :** [21 — Plan maître](21_BRODY_IMAGE_MASTER_PLAN.md) avait déjà les pièces **perception → génération → reverse evaluation**, mais ne précisait pas assez **la méthode couche-par-couche, l'IN/source comme contrainte explicite, la rigueur par région et l'opposition entre copie fidèle et synthèse inférée**. Ce document corrige ces omissions. **Ne pas confondre « vision documentée » et « méthode techniquement démontrée ».**

## 1. Sources et attribution : U / A / C / P

- **[FSO — Formule du Savoir Obsidia et apprentissage full auto](https://docs.google.com/document/d/14yk4MPqd5rd3RnB1AAyys8zHU4KD4Dq1eqNtLQFJTA0/edit)** : archive de conversation combinant **« Vous avez dit » (U)** et **« ChatGPT a dit » (A)**. Les sections visuelles et artistiques sont la source **primaire** de cet audit ; ancrages repérables par formulation.
- **[Éveil de l'OS Cognitif / apprentissage organique](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit)** : **synthèse IA / source secondaire** pour « invariant dynamique », `FaceLock`, les invariants ρ, la réciproque et la multimodalité ; ce n'est pas une transcription verbatim des paroles utilisateur.
- **[Framework de déconstruction du corpus visuel](https://docs.google.com/document/d/14eT3B2ZTD15DiSRKSNUjpfaRZQBj3LSmwW8QaIPUgKI/edit)** : exégèse de 43 représentations ; utile à la traçabilité des idées, **pas** preuve de la capacité d'un générateur.
- **[Outil photo IA — archive fonctionnelle](https://docs.google.com/document/d/1NlgM81M3aZxeycPSbt9R4fqCIqXfToC5/edit)** : U réclame photo produit, retouche existante, avatars et shorts ; ce sont **cas d'usage** d'un moteur image, **pas** ordre de construction d'une application e-commerce ou sociale.
- **C — Code/contrats** : [02 — Contrats](02_CONTRACTS.md), [22 — branchements](22_IMAGE_BRANCH_AND_DONOR_MAP.md), [05 — expérience/mémoire](05_LEARNING_MEMORY.md), [07 — tests](07_TEST_STRATEGY.md). Code local F0 disponible ; adaptateurs image, poids et boucles Brody réelles manquants.
- **P — propositions ci-dessous** : noms de contrats, ordres techniques, métriques, expériences. Ne jamais les faire passer pour des affirmations historiques de l'utilisateur.

**Règle de traçabilité :** chaque exigence ci-après distingue la **formulation utilisateur U**, la **solution technique suggérée historiquement A**, et la **traduction testable P**. Une équation ρ, un seuil ou une fidélité « garantie » écrits par l'IA historique restent des **hypothèses/propositions**, jamais une preuve.

## 2. Audit détaillé — les mécanismes image, sans dérive vers le reste d'Obsidia

| ID | Intention originale retrouvée (U) / source | Traduction fonctionnelle Brody (P) | État actuel |
|---|---|---|---|
| **IMG-01 — SOURCE & IN** | FSO, tour utilisateur « En plus pour l'art tu peut faire du procédurale... retenir la source, ne pas la dénaturer... IN ... respecté » | Toute commande avec référence porte `source_asset_refs`, `intent_text_ref`, zones à conserver et libertés autorisées. L'absence de source doit être explicite en pure génération. | **MANQUAIT COMME GATE EXPLICITE** |
| **IMG-02 — DÉCOMPOSITION** | FSO : « isoler une certaine image ... la recréer ... remplacer n'importe où ... ajouter des éléments au corps ou au décor » | Une `SubjectCardCandidate` dérivée (masque, alpha, bbox, contour, couleur, proportions, profondeur facultative, occlusions et provenance), sans ontologie concurrente. | **PARTIEL** dans doc 23 ; extraction réelle absente |
| **IMG-03 — MÉTHODE DU PEINTRE / COUCHES** | FSO : « couche par couche ou dans le bon ordre », techniques de peintres et rendu des ordinateurs. | Mode `LAYERED_RECONSTRUCTION` : forme globale → valeurs/lumière → couleur → bords → détails, avec conservation du master et tests à chaque passage. | **OUBLI OPÉRATIONNEL IMPORTANT** |
| **IMG-04 — FIDÉLITÉ ADAPTÉE** | FSO : « pixel-pixel » selon le besoin, ou plus « libre-arbitre » pour l'art ; exemples visages, manga, autres styles. | `RigorProfileCandidate` réglé **par propriété/région**, pas par sortie globale : `EXACT_REGION`, `STRICT_IDENTITY`, `STYLE_BOUNDED`, `FREE`. C'est une **proposition P**, pas les noms utilisés historiquement. | **PRINCIPE CONNU, COMMANDE TYPÉE ABSENTE** |
| **IMG-05 — GÉNÉRALISER L'IDENTITÉ** | FSO : « pour tout objet ou toute chose qu'on veut garder », le visage n'était qu'un exemple. | Identifier les contraintes propres aux produits, animaux, objets, logos, personnages, scènes (ne pas imposer un face embedding). | **À EXPLICITER** |
| **IMG-06 — RÉCIPROQUE** | FSO : apprendre à isoler puis recréer « par réciproque » ; réutiliser la capacité informatique de lire/créer du visuel. | Aller-retour `analyse → représentation → reconstruction → re-perception` ; mesurer conservation des aspects observables, réviser les hypothèses. | **CONCEPT DOCUMENTÉ, BOUCLE NON BRANCHÉE** |
| **IMG-07 — TRANSPORT / AJOUTS** | FSO : déplacer le sujet à toute position/dimension et ajouter au corps ou au décor. | Séparer `COMPOSITE_2D`, `EDIT_REGION` et `NOVEL_VIEW`/3D. Permettre occlusion, perspective, ombres et contraintes d'échelle. | **PLANIFIÉ, NON PROUVÉ** |
| **IMG-08 — PROPORTION/ART** | FSO : question utilisateur sur nombre d'or, Fibonacci et bases de la peinture. | Grilles de composition **optionnelles** (φ, tiers, symétrie et alternatives), jamais loi du beau ni contrainte de vérité physique ; évaluer contre l'intention et les objets importants. | **DOCUMENTÉ, PAS EXPÉRIMENTÉ** |
| **IMG-09 — PERSPECTIVE/360°** | FSO : meilleur résultat avec scan 3D, mais indisponible pour beaucoup ; représentations multi-vues ; [01 — architecture](01_ARCHITECTURE.md) propose Reverse360. | Mono-vue = structure cachée `UNKNOWN`; multi-vue/3D si sources suffisantes ; cycle A→B→A pour comparer sans inventer des côtés absents. Origine verbatim de « Reverse360 » pas rétablie. | **ARCHITECTURE PARTIELLE** |
| **IMG-10 — TEMPS/VIDÉO/PHYSIQUE** | Source Éveil (A) : « invariant dynamique », flux spatio-temporel plutôt que frames indépendantes ; analogie utilisateur enfant et objet qui tombe conservée dans 00/21. | Frames sourcées → identité/temps/repère → changements attendus/observés ; distinguer mouvement caméra/objet et hypothèse de force non prouvée. | **CONTRATS AMONT RELEVÉS, E2E ABSENT** |
| **IMG-11 — AMÉLIORATION** | FSO : ne pas refaire les roues / utiliser les capacités existantes ; autres sources projet : correction d'erreur et mémoire d'épisode. | Rejouer échec de masque, identité, ombre ou point de vue ; tester correction ciblée et réutiliser stratégie après revue ; ne pas promettre auto-entraînement des poids. | **BOUCLE F0 NON CONNECTÉE À L'IMAGE** |

### Attribution précise de quelques passages décisifs

Les phrases suivantes se trouvent sous les tours **« Vous avez dit » de FSO** :
- « isoler une certaine image ... la recréer tel quel ... remplacer n'importe où » → IMG-02/06/07.
- « couche par couche ou dans le bon ordre » → IMG-03.
- « plus ou moins laxiste », « pixel-pixel » et « plus d'art » → IMG-04.
- « toujours ... ressembler à l'original » même lors de transformations de style → IMG-01/04.
- « pour tout objet ou toute chose qu'on veut garder » → IMG-05.
- « retenir la source ne pas la dénaturer ... IN de l'utilisateur » → IMG-01.

**En revanche**, les détails « pyramide laplacienne », `RGBA prémultiplié`, `ArcFace/CLIP`, « Harmonic Composer », « SRS », seuils `SSIM`/ΔE et architecture `NeRF/mesh/splats` figurent **dans les réponses historiques de l'assistant**. Ce sont des **donneurs techniques A à évaluer**, pas des inventions/validations attribuées à l'utilisateur.

## 3. Contrat du résultat visuel : préserver la source avant de fabriquer

**Candidate P (pas encore schéma Python implémenté) :**

```text
VisualEditIntentCandidate
  intent_id / original_user_instruction_ref
  input_kind = REFERENCE_IMAGE | VIDEO | TEXT_ONLY | MULTIVIEW
  source_asset_refs[] + immutable hashes (vide si TEXT_ONLY)
  requested_output = RECONSTRUCTION | COMPOSITE | EDIT | NOVEL_IMAGE | NOVEL_VIEW
  subject_refs[] + region_refs[]
  invariants[]  # property, region, LOCK/FLEX/IGNORE, tolerance, provenance
  rigor_per_region[]  # EXACT_REGION | STRICT_IDENTITY | STYLE_BOUNDED | FREE
  allowed_transformations[] + forbidden_transformations[]
  visual_style_ref? / composition_guide? / constraints_3d?
  evaluation_requirements[] / unknowns[]
  proposal_only = true
```

**Ne pas dupliquer** les racines F16/MMonde existantes : ceci est une vue dérivée que le futur `GenerationIntentV0` pourra référencer. Les noms de profil ci-dessus ne sont pas déjà canoniques.

Exemples falsifiables :

- **Photo produit** : marque/texte/forme sous `LOCK`, fond et ombre sous `FLEX` ; test de glyphes/contours sur la référence réelle.
- **Portrait stylisé** : caractéristiques d'identité réellement décrites `LOCK`, texture pinceau `FLEX` ; contrôle humain et géométrique, **pas** « pixel-pixel » compatible avec le changement intégral de style.
- **Création sans référence** : intention et contraintes seulement ; **ne pas inventer un original absent**.
- **Rotation 120° depuis une seule photo** : faces cachées inconnues ; image plausible possible, **vérité géométrique non démontrée**.

**Principe physique et graphique :** conserver exactement les pixels d'une portion recopiée est parfois possible en édition 2D. Mais après changement d'échelle, lumière, perspective ou style, l'égalité pixel à pixel avec l'image originale **n'est pas mathématiquement attendue**. Le verrou se déplace vers la propriété observable demandée (silhouette, proportion, inscription, apparence, etc.).

## 4. Trois voies à séparer, et où la méthode « peintre » intervient

```text
[ORIGINAL + IN] ou [INTENTION PURE]
        |
        v
SOURCE ANCHOR / ZONES / PROVENANCE
        |
        v
SEGMENTATION + PROPRIÉTÉS + INVARIANTS
        |
        +-------- RESTITUTION R (2D) --------------------+
        | masque -> alpha -> cutout -> composition       |
        | pixel source connu conservable                 |
        |                                                 |
        +-------- RECONSTRUCTION L (par couches) --------+
        | forme / masses -> lumière -> couleur -> bords  |
        | -> détails -> ombres/occlusions -> comparaison  |
        |         (ordre et tests par passes)            |
        |                                                 |
        +-------- GÉNÉRATION G (modèle externe) ---------+
          contraintes -> adapter -> nouveau visuel
          (pas de garantie de copie exacte)
                              |
                              v
       GENERATED / EDITED ARTIFACT + HASH + PROVENANCE
                              |
                              v
         RE-PERCEPTION ET CONTRÔLES PAR PROPRIÉTÉ
                              |
                     erreurs et inconnus
                              |
                EXPERIENCE CANDIDATE / REPLAY
```

**R**, **L** et **G** ne sont pas des niveaux d'autorité : ce sont des routes de traitement. Brody peut proposer une route selon la demande et le coût. **Aucune voie ne s'autorise à déclarer un artefact généré comme observation physique réelle.**

Le « protocole peintre » est une **méthode de décomposition/rendu historiquement proposée par l'assistant**, inspirée de l'idée utilisateur ; son efficacité doit être comparée à une route de génération globale. Il ne doit pas être imposé à tous les modèles de diffusion qui n'exposent pas de couches internes.

## 5. Les tests que l'audit impose **avant** la prétention « Brody sait générer fidèlement »

| Test image | Référence + instruction | Ce qu'il démontre s'il réussit | Piège à refuser |
|---|---|---|---|
| **BIMG-01 / ANCRE-IN** | Image A, « garde cet objet, change le décor » | Source/hashes/invariants/intent remontent jusqu'à l'artefact | génération sans attribution du bon original |
| **BIMG-02 / EXTRACTION** | Image objet avec masque de référence | Masque, limites, alpha et incertitudes évalués | texte VLM considéré comme segmentation exacte |
| **BIMG-03 / PEINTRE** | Même objet, route layered vs route globale | Comparaison de qualité, détails conservés, coût, erreurs par passe | présumer que « layered » gagne sans mesure |
| **BIMG-04 / RIGUEUR** | Même image, demandes strict et style libre | Seules les propriétés autorisées changent ; critères par zone | un unique score esthétique cache dérive identité |
| **BIMG-05 / OBJET GÉNÉRIQUE** | Produit ou jouet, sans visage | Verrouillage d'identité ne dépend pas d'ArcFace | validation seulement sur portraits |
| **BIMG-06 / TRANSPORT 2D** | Sujet A, fonds B/C, taille et lumière variables | Découpe/placement/occlusions corrects et changements déclarés | promettre pixels identiques après warping |
| **BIMG-07 / HARMONIE** | Divers cadrages φ, tiers, symétrie ou aucun | Comparaison sans suppression du sujet, préférence humaine | « nombre d'or = perfection » |
| **BIMG-08 / 360** | Références mono-vue / multi-vue | Erreurs d'identité/occlusion et inconnus reconnus | « côté caché » annoncé comme vu |
| **BIMG-09 / VIDÉO PHYSIQUE** | Objet + caméra en mouvement | Séparer changement objet et mouvement caméra | conclure « gravité » depuis une seule séquence ambiguë |
| **BIMG-10 / RÉPÉTITION** | Rejeu d'un artefact raté connu | Brody propose une meilleure route et conserve preuve du delta | « apprentissage des poids » annoncé sans entraînement |

**Verdicts :** `PASS` seulement après mesure traçable ; sinon `FAIL`, `UNKNOWN`, `INCONCLUSIVE`, `NOT_RUN`. Le succès documentaire ne vaut pas `PASS` de ces tests. Utiliser des masques/captures de référence ou évaluations humaines indépendantes pour éviter que le même modèle se juge lui-même.

## 6. Dépendances nécessaires, et uniquement celles utiles à l'image

| Sous-tâche | Sources techniques déjà identifiées | Décision avant forge |
|---|---|---|
| Entrée image | F16 `RealImageObservationV0`, Jarvis camera/screenshot, fichier local | commencer avec **fichier de test** ; caméra non obligatoire |
| Segmentation/alpha | MobileSAM, Grounding DINO (candidats) | choisir extracteur par compatibilité PC, licence et vraie qualité de masque |
| Descripteur / hypothèses | Brody, Qwen-VL local Jarvis **si disponible** | ne pas installer un second chatbot par défaut |
| Profondeur et vues | DA3/2D-to-3D multi-vues et éventuellement WorldFM (plus tard) | droits des poids et ambiguïtés mono-vue à qualifier |
| Rendu 2D fidèle | composition alpha, transformée image déterministe | **pas besoin d'un gros générateur pour BIMG-01/02/06** |
| Génération | stable-diffusion.cpp + checkpoint **après inventaire GPU/VRAM** | `GeneratorAdapter` et poids/source/seed/hashes nécessaires |
| Retour visuel | F16/modality GENERATED + `ReverseEvaluationV0` cible | séparations GENERATED/REAL strictes, rapports par propriété |
| Expérience | F0 `WorldExperienceCandidateV0`, Native Memory candidate | aucune promotion automatique ; retenue de réussite/échec après validation |

**Hors du chantier actuel :** 81 versions, architecture civilisation cognitive, trading, kernel, CRM, GPS/Défense, interface Pokémon, évaluation des problèmes mathématiques. Ils ne servent ici que d'interfaces **déjà existantes**, lorsqu'elles sont strictement indispensables. Ce document **n'ordonne ni audit Obsidia global ni entraînement de 81 modèles**.

## 7. Verdict de fidélité documentaire

| Question | Verdict honnête |
|---|---|
| La demande d'isolement, reproduction, déplacement et ajout est-elle retrouvée dans les paroles utilisateur ? | **OUI — U/FSO** |
| Le travail dans l'ordre / en couches comme un peintre est-il exprimé par l'utilisateur ? | **OUI — U/FSO**, mais la séquence d'opérations précise vient de **A** |
| L'intention et le respect du sujet d'origine sont-ils des exigences explicites ? | **OUI — U/FSO** |
| La rigueur par région, identité généralisable, liberté stylistique sont-elles demandées ? | **OUI — U/FSO** ; noms et seuils d'adapter restent proposés |
| Fibonacci/symétrie garantissent-ils une image parfaite ? | **NON**, hypothèse artistique à tester |
| Réversibilité signifie-t-elle inverse exacte d'un générateur stochastique ? | **NON**, c'est une boucle d'analyse/reconstruction/contrôle à mesurer |
| Les modèles entraînés, générateurs, moteurs 3D et outils perception sont-ils installés et testés ? | **PAS DÉMONTRÉ** |
| La vision Brody Image est-elle désormais couverte **pour les sources relues** ? | **OUI, au niveau fonctionnel**, avec incertitudes listées ; aucune exhaustivité sur des archives non relues |

**Next step produit sans dérive** : `BIMG-01` puis `BIMG-02` / `BIMG-06` (une vraie image-source et une découpe/composition mesurée), puis `BIMG-03` layered et premier `GeneratorAdapter` G1 en parallèle. **La démonstration** décidera quels mécanismes de ta méthode améliorent réellement Brody.
