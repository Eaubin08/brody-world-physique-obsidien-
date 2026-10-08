# 23 — BRODY IMAGE : TRAÇABILITÉ DES MÉTHODES D'APPRENTISSAGE VERS LA FORGE

**Date :** 2026-10-08 · **État :** AUDIT DE SOURCES PARTIEL ET PLAN DE TESTS · **Portée :** Brody Image I0 → I1/G1/IG2 puis I3–I7.  
**Autorité :** aucune modification KX108, aucune auto-promotion mémoire, aucun modèle déclaré installé. `main` ne fait pas partie de cette passe.

## 0. Pourquoi ce document

[21 — plan maître](21_BRODY_IMAGE_MASTER_PLAN.md) relie déjà Brody, perception, monde, génération et re-perception. Cette passe examine les **mécanismes originaux d'apprentissage et de création** et les traduit en **tests falsifiables** plutôt que de supposer qu'ils sont déjà réalisés. Elle n'ajoute pas ces mécanismes à l'Atlas comme preuve de leur existence runtime.

**Provenance des formulations :**
- **U — formulation utilisateur retrouvée** : phrase ou intention présente dans une source de conversation archivée ; ceci n'attribue pas les détails techniques adjacents à l'utilisateur.
- **A — élaboration de l'assistant retrouvée** : décomposition, algorithme, chiffres ou pseudo-code proposés dans une réponse IA.
- **C — contrat existant lu en dépôt** : source de code ou documentation GitHub, différent d'une installation.
- **P — proposition de test de cette passe** : protocole de vérification, non résultat scientifique.

Les documents Drive ci-dessous sont parfois des **conversations copiées** incluant des tours utilisateur *et* assistant : ne jamais attribuer l'intégralité d'un document à l'utilisateur.

## 1. Sources relues et périmètre réel

| ID | Source exacte | Ce qu'on peut lui attribuer | Limite |
|---|---|---|---|
| **FSO** | [Formule du Savoir Obsidia et apprentisage full auto](https://docs.google.com/document/d/14yk4MPqd5rd3RnB1AAyys8zHU4KD4Dq1eqNtLQFJTA0/edit) | U : apprentissage humain/école, accélération par réciproque, non-réinvention, isoler/recréer/transporter un sujet, question sur Fibonacci/nombre d'or ; A : détaillages ρ, curriculum, algorithmes d'isolation/composition, Harmonic Composer, familles de variantes | Archives mêlant auteurs ; ce parcours cible des passages précis, pas une relecture ligne à ligne des 244k caractères |
| **ÉVEIL** | [L'Éveil de l'OS Cognitif et Apprentissage Organique](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit) | A/synthèse historique : invariants ρ, analyse/synthèse, invariant dynamique, FaceLock, Zone Latente, Shazam, friction | Ce document commence comme réponse de synthèse, pas citation directe de toutes les paroles de l'auteur |
| **VISUEL** | [Framework de décomposition du corpus visuel](https://docs.google.com/document/d/14eT3B2ZTD15DiSRKSNUjpfaRZQBj3LSmwW8QaIPUgKI/edit) | Index de 43 sources/images et cartographie des couches conceptuelles | Exégèse secondaire ; ne prouve ni modèle visuel entraîné ni origine exclusive |
| **FOUNDRY** | [World Foundry / archive éducative](https://docs.google.com/document/d/1d5Gf5-r1d43wetqaANCzCff5CPyYckwTw9_AuWwicpg/edit) | Éducation par mondes, expériences, conséquences, curricula, replay, compétence candidate | Document composite, vision éducative plus large que V0 image |
| **ATLAS** | [15 — Atlas](15_CONCEPT_ATLAS.md), [18 — Matrice](18_CONCEPT_SOURCE_MATRIX.md), [20 — gaps F0](20_F0_FINAL_SOURCE_GAPS.md) | États et généalogies des concepts | Des rapprochements restent hypothétiques ; ne pas combler les trous par inférence |
| **CODE** | [22 — Carte des vraies branches](22_IMAGE_BRANCH_AND_DONOR_MAP.md), [02 — Contrats](02_CONTRACTS.md) | Contrats MMonde/F12/F16/Native Memory identifiés, raccords manquants | Présence source ≠ branchement fonctionnel ≠ benchmark PC |

## 2. Matrice « idée → interface → épreuve »

| Méthode à préserver | Lecture fidèle de la source | Traduction Brody Image, cible et non implémentation | Premier test exigible |
|---|---|---|---|
| **Apprendre comme un enfant, puis formaliser** | U/FSO : donner des savoirs et exemples, laisser apprendre, évaluer ; comprendre une conséquence avant l'équation | `LearningEpisodeCandidate` : démonstration → exercice guidé → exercice nouveau → explication → évaluation ; situations visuelles datées et sourcées | Objet en chute : distinguer observation de mouvement, prédiction et explication ; garder causalité UNKNOWN sans témoins indépendants |
| **Réciproque / analyse ⇄ synthèse** | U/FSO : réutiliser les capacités de lecture/visuel au lieu de réinventer ; A/ÉVEIL : invariants ρ, round-trip | `AnalysisCandidate` → `GenerationIntentV0` → `GeneratedArtifactV0` → `ReverseEvaluationV0` ; comparer au référent et aux invariants | Reconstruire un objet masqué ; re-percevoir le rendu ; FAIL si structure absente, INCONCLUSIVE si perception incertaine |
| **Isoler → recréer → transporter → ajouter** | U/FSO : extraire un sujet, le refaire « tel quel », pouvoir le placer ailleurs/à d'autres dimensions et ajouter au corps ou décor | **Deux voies distinctes** : (A) *cutout/alpha/compositing* pour conservation pixel/région, (B) *génération/édition conditionnée* pour variations et nouvelles vues ; identifier laquelle a produit l'artefact | Sujet détouré inséré dans deux fonds avec changement d'échelle : masque/alpha, occlusion, placement ; comparer à un témoin pixel-conservé pour A ; jamais promettre fidélité pixel parfaite par B |
| **Invariants ρ / identité / rigueur modulée** | A/ÉVEIL et A/FSO décrivent LOCK/FLEX par type de propriété, avec `FaceLock` comme cible | `VisualInvariantV0` avec `LOCK`, `FLEX`, `IGNORE`, tolérance, autorisation, provenance ; privilégier objets ordinaires pour les premiers tests | Éclairage FLEX : objet, silhouette, proportion LOCK ; comparer évaluateur + référence indépendante ; `UNKNOWN` n'est pas un succès |
| **Symétries / proportions / Fibonacci / nombre d'or** | U/FSO **pose une hypothèse** de composition harmonieuse ; A/FSO distingue φ de la suite de Fibonacci et propose plusieurs grilles (tiers, diagonales, symétries) | `CompositionConstraintCandidate` **facultatif**, jamais loi physique, jamais critère de vérité ni garantie du « beau » ; chaque grille explicitement choisie puis soumise au test | Sur mêmes 8 images : comparer cadrage original, grille φ, règle des tiers, symétrie, contrôle sans grille ; mesures de pertes d'objets + préférence humaine ; aucune sélection imposée |
| **Reconstruction de points de vue / 360°** | Atlas #39 : Reverse360 mesure persistance d'identité, et non panorama ; source historique exacte encore à retrouver | `ViewpointTransformCandidate` : caméra/source, angle, repère, occlusions ; `ViewConsistencyEvaluation` | Vues A/B/C + retour A, pénaliser incohérences géométriques ; si la face cachée n'a pas de vérité de référence : INCONCLUSIVE, non PASS |
| **Flux dynamique / vidéo** | A/ÉVEIL : invariant dynamique et continuité d'objet entre frames | Associer source F12 `TrajectoryV0/TransitionV0`, timestamps, tracking, occlusion, changement caméra | Clip avec même sujet, rotation/occlusion et témoin de changement caméra ; taux de switches d'identité, dérive et contradictions |
| **Mémoire : pas refaire la même route** | U/FSO : tirer parti de capacités déjà existantes ; FOUNDRY : histoire des essais/échecs et pédagogie par conséquence | `WorldExperienceCandidateV0` + hash/source/écart/stratégie, déduplication d'un échec **sans** dépôt de mémoire automatique | Exécuter deux fois le même cas : rejouer route antérieure, détecter répétition et proposer une correction ; vérifier qu'aucune expérience non qualifiée ne devient vérité |
| **Variantes d'entraînement / cerveaux divers** | U/FSO mentionne « une 100 de version d'entraînement prévue » ; A/FSO propose axes domaines, types de cerveau, apprentissages, exécution, niveaux N0–N4 | `TrainingVariantRegistryCandidate` (identifiant, source, domaine, cognition, méthode, matériel, coût, statut de preuve), **aucune liste inventée** | Exécuter seulement 2 variantes comparables (méthode fixée à la source) sur mêmes données/contrôles ; enregistrer coût, erreurs, transfert ; promotion manuelle |
| **Multimodal, hiérarchie et flux** | ÉVEIL et FOUNDRY : représentation adaptée par couche, image/vidéo/texte/son et expérience située | F16 → MMonde → Brody avec refs source, niveau d'abstraction et incertitude ; pas d'ontologie concurrente souveraine | La description textuelle doit rester reliée à un objet/source image, sans convertir l'interprétation du VLM en fait physique |
| **Quantique / diffusif / architectures différentes** | Archives historiques présentent des pistes de cerveaux spécialisés ; aucune variante quantique entraînée ici n'est démontrée | Registre de **recherche future**, distinct du générateur diffusif G1 ; « quantique » ne signifie pas accélération disponible | Gate de revue de source, ressources, hypothèse et métrique **avant** planification technique ; hors prérequis I1/G1 |

## 3. Deux chemins de création à NE PAS fusionner

### R — Restitution/édition sous fidélité de source
`real_source_asset + subject_mask + permitted_transform + placement_constraints → composited_asset`.

- Un masque/alpha exploitable et un témoin de référence (quels pixels sont conservés) précèdent l'évaluation.
- Le transport d'un sujet en 2D peut réutiliser exacts pixels sur une zone ; une nouvelle perspective, un corps modifié ou des parties invisibles ne le peut pas automatiquement.
- Les modifications de corps/décor doivent être explicitement identifiées comme éditées, pas « identité pixel-per-pixel prouvée ».

### G — Génération / généralisation à partir des contraintes
`source_refs + GenerationIntent + LOCK/FLEX/IGNORE + generator_adapter → GeneratedArtifact`.

- La génération est stochastique selon moteur/modèle/seed et ne garantit pas la restitution d'un original.
- Le test essentiel n'est pas « image jolie » mais *quels invariants, transformations et relations survivent*.
- Le généré peut ré-entrer dans la perception **uniquement comme GENERATED**, jamais sous `RealImageObservationV0`.

### Sens de l'aller-retour

Re-percevoir une image générée mesure d'abord la **cohérence et les erreurs observables** de la chaîne. Un cycle analyse→synthèse→analyse réussi ne prouve **ni compréhension causale complète, ni loi physique, ni indépendance de l'évaluateur**. Ajouter des témoins, des cas tenus secrets et des vues indépendantes avant de conclure.

## 4. Protocoles de tests I/G — spécification, non résultats

| ID | Entrée | Changement voulu | Invariant attendu | Verdict si source insuffisante |
|---|---|---|---|---|
| **T-R1** | Sujet source + segmentation témoin | Découper et recoller sans édition | Zone conservée, bords/alpha contrôlés | INCONCLUSIVE si témoin masque absent |
| **T-R2** | Même sujet + 2 fonds documentés | Échelle/placement, occlusion autorisée | Identité sur zone recopiée, géométrie localisée | FAIL si pixels verrouillés dérivent sans autorisation |
| **T-G1** | Sujet + 2 intentions LIGHT | Éclairage FLEX seulement | Silhouette/structure LOCK | INCONCLUSIVE si evaluateurs non calibrés |
| **T-G2** | Sujet + rotation de point de vue | Perspective FLEX | Relations/identité LOCK quand observables | UNKNOWN pour faces non vues |
| **T-H1** | 8 scènes et grilles pré-choisies | Cadrage optionnel φ, tiers, symétrie | Aucun sujet important découpé | Mesures + revue humaine, pas « perfection » |
| **T-L1** | Séquence multi-frame sourcée | Chute vs mouvement caméra | Temps, track, référentiel | CAUSALITY_UNKNOWN si ambigu |
| **T-M1** | Répétition d'un échec enregistré | Corriger une route / choisir autre chemin | Pas de promotion sans gate, replay conservé | FAIL si échec répété sans être détecté |
| **T-V1** | Variantes de méthode décrites et autorisées | Apprentissage sur même jeu borné | Score/cout/temps traçables | NOT_RUN si variantes non matérialisées |

**Règle d'évaluation commune** : `PASS` exige source+critère+mesure reproductible et indépendant de la sortie textuelle de Brody ; sinon `FAIL`, `UNKNOWN` ou `INCONCLUSIVE`. Un évaluateur VLM seul n'est pas un oracle. Ne pas mélanger reproduction d'image, préférence esthétique et vérité physique.

## 5. Passage exact vers la forge

1. **I0.DOC (ici) :** tracer sources U/A/C/P et conserver les pistes en suspens ; cette carte ne proclame pas le freeze F0.
2. **I0.PC (nécessaire avant G1) :** GPU, VRAM, RAM, OS, moteur image présent, endpoint Qwen local, outils de capture, licences par *poids et variantes*. N'inventer aucune configuration PC.
3. **I1 minimal :** image-fichier réelle avec identité de fichier/hash, source, timestamp et primitive candidate ; caméra Jarvis facultative si non disponible.
4. **G1 minimal :** un seul `GeneratorAdapter` choisi d'après I0.PC ; artefact généré séparé avec `model/version/weights_hash/seed/params/file_hash`.
5. **IG2 court :** T-R1, T-G1, T-L1 ; rapport LOCK/FLEX/UNKNOWN et `ReverseEvaluationV0` ; aucun apprentissage revendiqué avant réplication.
6. **IG3 physique/vidéo + mémoire :** T-G2, T-M1, traçage multi-vues et scénarios non vus ; bridge mémoire seulement après revue des contrats et du gate.

### Les lacunes toujours ouvertes

- **Les 81 variantes : SOURCE HISTORIQUE RETROUVÉE** : l'archive de Civilisation Cognitive présente explicitement les 3 couches (9 blocs perceptifs × 9 paradigmes = 81 combinaisons) et une matrice proposée par l'assistant. Toutefois la liste intégralement **validée par l'utilisateur** et l'extension exacte à 90 / 100+ ne sont pas gelées ; voir §6. Ne pas présenter les 81 comme un programme d'entraînement déjà exécuté.
- **Fibonacci / symétrie** sont bien présents dans une source utilisateur, mais leurs paramètres, domaines d'application et priorités ne sont **pas déjà validés** scientifiquement ni comme moteur.
- **Reverse360**, **Shazam visuel/VisualFingerprint**, et les filiations historiques mentionnées par [20](20_F0_FINAL_SOURCE_GAPS.md) conservent leurs incertitudes ; pas de réparation par reformulation.
- **I1/G1/IG2** restent non exécutés sur images et modèles réels. Les tests Python F0 actuels vérifient schémas / documentation, pas les résultats visuels.
- **Tout choix de modèle, weights/licence, GPU et performance** demeure conditionnel au PC.

**Décision documentaire :** ce document est une **base d'exécution testable**, pas un F0 gelé, ni un moteur Brody Image fonctionnel. Les preuves observables seront livrées gate par gate.


## 6. RÉCONCILIATION ADDITIVE : source retrouvée sur les « 81 versions et + » (2026-10-08)

**Source primaire retrouvée :** [🧠 Obsidia – Civilisation Cognitive Complète (Cartographie Master)](https://docs.google.com/document/d/14WUSNQPcZ4MsNP0lfpHT2PkfEJxiHhGvdcdNefqSbOE/edit) ; source recoupée : [Obsidia – Architecture Cognitive Multiverselle](https://docs.google.com/document/d/1lsxNC3K_3rACpnZQkzj4L9oqPM8I6mqJBnZSOB5SWnA/edit) et [Matrice des Cerveaux — 100 versions](https://docs.google.com/document/d/15mn-qh0SDUWkqDUFAgB-RbsWFtp_fGqv/edit). **Documents conversationnels : texte « Vous avez dit » = formulation utilisateur ; « ChatGPT a dit » = construction de l'assistant.** Pas de fusion anachronique avec le runtime actuel.

### 6.1 Ce que l'utilisateur définit explicitement (U)

- Passage proche de **« Vous avez dit : » avant 1919–1922** : les **modules/cerveaux internes d'une même Obsidia peuvent coopérer** ; **les versions entraînées d'Obsidia ne coopèrent pas entre elles**. Cette correction explicite de l'utilisateur prévaut sur les résumés contradictoires de l'assistant.
- Passages « Vous avez dit » proches de **1795, 2003–2007 et 2245** : approches multiples, blocs sensoriels distincts comparables aux parties du cerveau humain, paradigmes (fractal, ludique, empathique, lymphatique, moteur, symbolique, quantique, diffusif, token), et distinction entre les couches nécessaires pour former des versions d'Obsidia.
- Passage **2585–2591** : l'utilisateur juge encore les reformulations inexactes et demande les **trois couches et leur titre** ; donc une réponse IA qui suit n'est pas automatiquement une validation canonique par l'auteur.
- Passage **3838–3840** : l'utilisateur demande de produire rapidement une matrice ; celle-ci est ensuite décrite par l'assistant, non attestée comme registre de 81 entraînements effectivement réalisés.

### 6.2 Structure des trois couches **décrite par l'assistant historique (A)**

| Couche | Fonction décrite dans l'archive | 9 familles proposées dans la réponse historique (à qualifier, non figer comme choix définitifs auteur) |
|---|---|---|
| **1 — Blocs perceptifs internes** | Organes de perception et traitement des entrées dans une même Obsidia | textuel ; visuel/spatial ; sonore/tonal ; moteur/action ; émotionnel ; symbolique/archétypal ; sensoriel brut ; social/intentionnel ; méta-réflexif |
| **2 — Paradigmes d'apprentissage** | Style dominant de traitement/entraînement de ces blocs | tokenisé ; diffusif ; quantique ; symbolique ; fractal ; ludique ; moteur ; lymphatique ; empathique |
| **3 — Versions entraînées** | Instances formées par combinaison d'un bloc perceptif dominant et d'un paradigme dominant | **9 × 9 = 81 combinaisons théoriques** ; peut s'étendre après définition vérifiée d'autres axes |

**Frontière décisive :** les 81 sont ici une **matrice combinatoire d'architectures/entraînements proposés**, pas 81 modèles déployés, ni un essaim de 81 agents connectés, ni une garantie que toutes les variantes sont utiles. Le document historique mélange par endroits « 81 », « 90 » et « 100 versions » dans des réponses IA ; ces nombres **ne doivent pas être normalisés artificiellement**. En particulier, les appels à « faire coopérer les versions » dans des réponses historiques ultérieures **contredisent la correction utilisateur** : ils restent marqués **A-DRIFT**, et non doctrine.

### 6.3 Traduction utile au seul moteur Brody Image (P)

**Une version complète d'Obsidia entraînée ≠ un simple modèle d'image.** Pour Brody Image, le registre doit garder trois clés sans confondre leurs niveaux :

```text
ImageTrainingCandidate
  user_source_ref
  perceptual_block_ref    # une partie perceptive, ex. visuel/spatial
  learning_paradigm_ref   # forme d'entraînement, ex. diffusif / symbolique
  version_ref?            # version entraînée distincte, PAS agent coopérant par défaut
  input_domain            # image / vidéo / scène située
  episode_and_replay_refs
  evaluation_protocol_ref
  result_status           # NOT_RUN / INCONCLUSIVE / FAIL / PASS
  promotion_authority     # aucun apprentissage canonique automatique
```

**Première preuve à demander, sans entraîner 81 modèles :** deux voies bornées pour le même objet et même jeu de contrôle, avec segmentation/source/provenance constantes, métriques d'identité/transfert/temps/VRAM, différence de paradigme explicite et comparaisons archivées. Si l'essai n'est pas réalisé : `NOT_RUN`. `Quantique` ne désigne pas par défaut un ordinateur quantique installé.

**Reste non résolu :** savoir si l'utilisateur a ultérieurement validé la matrice 9×9 telle que proposée, quelles familles s'ajoutent pour « 81+ », et quelle est la **liste finale** approuvée. Le document FSO et ces archives ne suffisent pas à attribuer tous les paramètres proposés par les IA à la doctrine de l'utilisateur.
