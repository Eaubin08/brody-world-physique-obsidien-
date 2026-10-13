# 58 — Audit d'écart : principes prévus vs P2.9c réellement branché

**Date :** 2026-10-09. **Type :** audit documentaire / code ciblé, sans mutation du moteur. **Verdict :** `ARCHITECTURAL_COVERAGE_GAP`. Aucun nouveau runtime ni test PC réalisé pour ce document.

## 1. Diagnostic reproductible
P2.9c : TRAIN 80, 18 scènes mesurées, 62 rejetées ; TEST 180, 42 acceptées (23,3 %), MAE conditionnelle 11 px, 21 erreurs >10px ; bras calibré = bras repère fixé ID4. Les phases avec repère 4 fiable sont correctes sur les scènes acceptées, les phases avec repère 0 ou 2 fiable donnent MAE 22 px. Rejeu OK et cinq tests unitaires OK selon le log opérateur. Le banc change simultanément le décor/les paramètres graphiques et l'ID du repère physiquement fiable : l'impact de chaque changement **n'est pas isolé**.

## 2. Causes du constat
`p29c_transfer_v0.py` calibre par oracle caméra simulé uniquement sur TRAIN, choisit un index via erreur médiane puis gèle cet index sur TEST. Aucun feedback TEST, aucune sélection de portée, détection de divergence d'invariants, transform repère objet/caméra ni révision sans vérité terrain. La représentation `SpatialRelations` contient un ID de référentiel déclaré et cinq déplacements, mais pas de transformation entre référentiels. Un nouveau générateur d'apparence conserve des couleurs/aires de fiduciaires connues du détecteur P2.6 : **pas de transfert perceptif ouvert**. L'échec est celui de ce banc restreint, pas réfutation du projet global.

## 3. Inventaire de correspondance — doctrine, existant, manque
| # | Source de principe | Preuve d'existence préalable | P2.9c | Suite d'intégration |
|---|---|---|---|---|
| 1 | 42/43 : vues multiples image-espace-temps-mouvement | P1 bridge doc 44 / V4 | absent de la décision | réutiliser `multirepresentation_ball_bridge_v5`, tester ablations coordonnées |
| 2 | 24/27 : analyse ↔ synthèse/réciproque | `reverso_learning_v0`, V4.2 direction réciproque | absent | boucle synthèse/re-perception sans prétendre prouver causalité |
| 3 | 41/42 : symétries, rotation, translation, miroir, perspectives 360 candidates | V4.2 quatre cardinales 2D testées ; 360° 3D non prouvé | absent | contrat de transformations et cycle A→B→A avec UNKNOWN parties cachées |
| 4 | 28/42 : objets, continuité, temps, mouvement, conséquences préverbales | F12, V3–V4, pipeline vidéo P1 | simple double frame | état/transition/trajectoire, comparer avec et sans historique |
| 5 | 50 : réutiliser savoir seulement dans portée comparable | documentation P2.8 + fenêtre de fiabilité P2.8c | absence de contrôle de portée | test de compatibilité de contexte avant reprise du repère |
| 6 | 50 : contradictions, alternatives et HOLD | `GuardedBelief` P2.8c supervisé ; essais V4.2 | retiré de P2.9c | distinction désaccord mesuré, changement d'appareil, erreur de détecteur, UNKNOWN |
| 7 | 28/42 : provenance, unités, source indépendante, incertitude | F13 / MMonde / F16 upstream ; contrats locaux F0 | ID source textuel, pas d'incertitude/calibration horodatée | adaptateurs readonly typés, hash réel, horloges et limites |
| 8 | 24/27 : source IN, fidélité des régions, couches de peintre | Reverso V0 lossless et I1/R1 editor | absent | tests édition/rendu à côté de compréhension, objectifs séparés |
| 9 | 24/42 : symétrie, proportions/Fibonacci | proposition de composition, pas loi physique | absent | pistes optionnelles à tester, **pas règle universelle préprogrammée** |
| 10 | 28/42 : micro↔macro, nano, vivant, matière, thermodynamique | architecture/contrats candidats, pas observations réelles branchées | absent | protocole future capteurs et modèles typés; interdiction d'inférer micro depuis pixels macro |
| 11 | 28/43 : adaptation et conservation procédure/échec | V3–V4.2 experiences, `WorldExperienceCandidateV0`, `WorldStateDeltaV0` | aucun rappel de procédures | réutiliser épisodes avec version, preuve et portée, sans écrire B10 |
| 12 | 50 : intention dirige chemin, pas vérité | P2.9 `GoalRouting` | routage simple | budgets et précision par domaine, mêmes preuves indépendamment du but |
| 13 | 42/43 : modèles concurrents avec ablations équitables | P1/P2 protocoles | non isolé décor vs ancre | factoriel : apparence seule, repère seul, les deux, aucun |
| 14 | 24/27 : génération/reconstruction contrôlée | editor CPU, Reverso, V4.2 composition | exclu du test | bras génération : image future vs réel, pixel/structure/identité |
| 15 | 02/50/51 : frontières d'autorité | `KX108_ONLY`, B8; Native Memory readonly | préservé en sortie P2.9c | maintenir B10/promotion HOLD, ne pas confondre logs avec mémoire |
| 16 | 42/README : compétences, procédures sans réentraîner tous les poids | modules éducatifs V1–V4 et replay | apprentissage depuis zéro d'une fiabilité seule | récupérer capacités existantes et benchmark réemploi vs reconstruction |
| 17 | 24/28 : observation d'image/vidéo réelle | Qwen-VL testé, source vidéo manuelle, adapter F16 prévu | synthétique | validation indépendante sur vraie vidéo sourcée, sans prétention générale |

## 4. Ne pas confondre trois statuts
- **Établi par les sources** : doctrine de multi-représentations, portée, temporalité, réciprocité, provenance, apprentissage préverbal; prototypes Reverso, V4.2, P1.
- **Partiellement implémenté ailleurs** : relations géométriques cardinales et réciproques, reconstruction pixel, contrats MMonde/F12/F13/F16 ; absence de preuve de capacité globale.
- **Non prouvé / non branché** : invariants physiques autonomes, 360° 3D libres, micro/macro, perception robuste inconnue, sélection sans feedback de vérité, vraie génération apprise et transfert ouvert.

## 5. Décision de reprise, sans inventer de nouveaux moteurs
**F0-P2.9d = AUDIT / GATE** avant forge : réconcilier code P1, V4.2, Reverso, F12/F13/F16 et P2.8c selon les quatre étages. Ajouter un protocole factoriel gelé : apparence seule vs fiabilité des repères seule vs les deux ; même TRAIN, aucun oracle TEST, mesures de couverture/erreurs par étage et ablation de chaque représentation. Exécuter le pipeline existant sur mêmes sources pour démontrer exactement quelle capacité est déjà utilisable. Modifier ensuite une seule interface responsable à la fois.

**Interdit :** dire que ces principes sont déjà actifs parce que les documents existent ; ajouter des seuils optimisés sur TEST ; fusionner provenances corrélées ; prétendre que Fibonacci, 360 ou la physique micro sont déjà démontrés ; écrire B8/B10/Native Memory ; pousser `main`.

## Sources
- `docs/24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md` (main)
- `docs/27_REVERSO_WORLD_MODEL_APPRENTISSAGE_SELECTIF.md` (main)
- `docs/28_APPRENTISSAGE_PREVERBAL_MONDE_PHYSIQUE.md` (main)
- `docs/41_BRODY_V4_2_ORIENTATION_RECIPROQUE_MONDE.md` (main)
- `docs/42_AUDIT_TRANSVERSAL_REPRESENTATIONS_MONDE_MULTIECHELLES.md` (main)
- `docs/43_EXPERIENCE_COMMUNE_BALLE_REPRESENTATIONS_V0.md` (main)
- `docs/44_P1_PASSERELLE_MULTIREPRESENTATIONS_VIDEO_MONDE.md` (main)
- `docs/50_P28_CONTRAT_SAVOIR_HIERARCHISE_STABILISATION_INTENTION.md` (exp P2)
- `brody_world_physique/p29c_transfer_v0.py` (exp P2)
- logs opérateur P2.9c 80 TRAIN / 180 TEST et P2.8c-P2.9b.
