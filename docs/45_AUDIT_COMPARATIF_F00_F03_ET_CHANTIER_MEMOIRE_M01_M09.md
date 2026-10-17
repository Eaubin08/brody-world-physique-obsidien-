# 45 — AUDIT COMPARATIF F00–F03 & ARCHITECTURE MÉMOIRE MULTIDIMENSIONNELLE M01–M09

**Date :** 2026-10-17  
**Projet :** Brody World Physique Image (`brody-world-physique-obsidien-`)  
**Statut :** AUDIT RÉALISÉ · FONDATIONS VAGUE 1 & VAGUE 2 IMPLÉMENTÉES ET TESTÉES (207 TESTS PASS)  
**Autorité :** `KX108_ONLY` demeure l'autorité décisionnelle unique externe et inchangée. Aucune mutation du kernel, aucune écriture non autorisée en Native Memory.

---

## 1. Audit comparatif Anthropic / OpenAI / Obsidia (F00–F03)

| Mécanisme Externe | Équivalent Obsidia Réel | Preuve dans les Sources | Écart & Limite | Décision : Reprendre / Adapter / Ignorer |
|---|---|---|---|---|
| **Anthropic : Programmatic Tool Calling**<br>Génération d'un bloc de code (TypeScript/Python) qui orchestre plusieurs outils, boucles et conditions sans repasser par le LLM entre chaque appel. | **Obsidure Runtime Binder** + **Registre de Procédures Déterministes** | `obsidia-x108-proofs` : `CG9_GLOBAL_PROVIDER_BINDER_V1.md`, `apps/obsidia_api/brody_real_response_pipeline.py` ; `brody_world_physique/experience_memory_v1.py` | Anthropic génère du code arbitraire à la volée. Obsidia refuse l'exécution de code arbitraire issu d'un modèle ou d'une mémoire (`ALLOWED_CAPABILITIES` en liste blanche, empreintes SHA-256 des fichiers locaux). | **ADAPTER** : Réduire les allers-retours via un plan d'instruments typé et borné (`ToolPlanV1`), exécuté dans l'environnement borné Obsidure en Python natif (`MAX_STEPS = 64`). |
| **Anthropic : Claude Artifacts & Visual Code**<br>Création visuelle par code source (React, SVG, HTML5 Canvas) rendu de manière interactive. | **Brody Drawing School (V0–V4)** + **Reverso Lossless Decomposition** | `drawing_school_v1.py`, `reverso_learning_v0.py`, `image_v0.py` | Les artefacts Claude sont déclaratifs pour affichage web. Brody produit des **gestes moteurs paramétriques** (`GestureV1`) évalués pixel par pixel par calcul de delta XOR face à une image de référence. | **REPRENDRE & ÉTENDRE** : Distinguer rigoureusement **génération par code** (reconstitution géométrique exacte, vectorielle/raster déterministe) et **génération neuronale** (modèle diffusif stochastique). |
| **OpenAI : Sandbox JavaScript Tool Calling**<br>Exécution de JavaScript dans un conteneur éphémère pour filtrer les résultats d'outils et exécuter des séquences logiques. | **Obsidure Bounded Execution Environment** | `obsidia-x108-proofs` : `OBSIDURE_RUNTIME_ARCHITECTURE_V1.md` | OpenAI ajoute une dépendance runtime V8/Node.js et du JavaScript. Obsidia fonctionne déjà en Python déterministe sous budget strict d'étapes et validation d'invariants. | **IGNORER JavaScript / REPRENDRE l'exécution bornée** : Pas de nouveau runtime Node/JS. Obsidure remplit le même rôle en Python pur avec contrôle `KX108_ONLY`. |
| **OpenAI : Gestion des erreurs, coûts et tokens intermédiaires**<br>Boucles de correction avec relance du modèle en cas d'erreur d'outil. | **Strict Improvement Gate & Negative Transfer Rejection** | `experience_memory_v1.py` (`_error`, `strict_improvement=True`), `multidimensional_retrieval_v2.py` | OpenAI consomme des tokens supplémentaires pour corriger. Brody mesure directement l'erreur raster/géométrique et enregistre les échecs (`FAILURE_PATTERN_CANDIDATE`) pour interdire le réemploi sans coût de tokens. | **ADAPTER** : Mémoire des chemins refusés et rejet systématique des transferts négatifs avant toute exécution d'outil. |

---

## 2. Matrice d'état des 32 chantiers (Vagues 1 à 5)

| Code | Chantier | Source & Localisation | Preuve / Contrat | Tests | Statut |
|---|---|---|---|---|---|
| **F00** | Audit comparatif Tool Calling | Documentation technique | Normes Anthropic / OpenAI | `docs/45_...` | **EXISTE** |
| **F01** | Orchestration programmée bornée | `obsidia-x108-proofs` | `CG9_GLOBAL_PROVIDER_BINDER_V1.md` | `test_contracts_v0.py` | **EXISTE** |
| **F02** | Séparation code / neurones / boucle | `brody_world_physique` | `contracts_v0.py`, `docs/24_...` | `test_image_v0.py` | **EXISTE** |
| **F03** | Frontière de décision KX108_ONLY | `obsidia-x108-proofs` | `contracts_v0.py` (`_assert_non_sovereign`) | `test_contracts_v0.py` | **EXISTE** |
| **M01** | Frise & 6 axes temporels | `cognitive_memory_timeline_v1.py` | `TimelineEnvelopeV1` | `test_cognitive_memory_timeline_v1.py` | **EXISTE** |
| **M02** | 34 arbres cognitifs & 8 familles | `arbres_34.canon.json` | `CANONICAL_34_TREES`, `TreeProjectionV1` | `test_cognitive_memory_timeline_v1.py` | **EXISTE** |
| **M03** | Domaines spécialisés vs arbres | `PDF_C_DOMAINES_...` | `SpecializedDomainV1`, `DomainEngagementV1` | `test_cognitive_memory_timeline_v1.py` | **EXISTE** |
| **M04** | Relations multidimensionnelles | `multidimensional_retrieval_v2.py` | `ExperienceRelationLinkV1`, `MultidimensionalRelationTypeV1` | `test_multidimensional_retrieval_v2.py` | **EXISTE** |
| **M05** | Recherche par le sens (7 intentions) | `multidimensional_retrieval_v2.py` | `MeaningQueryIntentV1`, `search_by_meaning` | `test_multidimensional_retrieval_v2.py` | **EXISTE** |
| **M06** | Évolution des connaissances & Révisions | `cognitive_memory_timeline_v1.py` | `HistoricalBeliefRevisionV1`, `get_belief_prior_to_revision` | `test_cognitive_memory_timeline_v1.py` | **EXISTE** |
| **M07** | Calibration épistémique & Contre-exemples | `cognitive_memory_timeline_v1.py` | `EpistemicCalibrationV1` | `test_cognitive_memory_timeline_v1.py` | **EXISTE** |
| **M08** | Admissibilité Native Memory | `cognitive_memory_timeline_v1.py` | `NativeMemoryAdmissibilityReportV1` | `test_cognitive_memory_timeline_v1.py` | **EXISTE** |
| **M09** | Mémoire procédurale & Admissibilité tâche | `multidimensional_retrieval_v2.py` | `check_task_admissibility`, `VisualTaskAdmissibilityVerdictV1` | `test_multidimensional_retrieval_v2.py` | **EXISTE** |
| **E01** | École V0/V1 : Traits, courbes & gomme | `drawing_school_v0.py`, `v1.py` | `GestureV1`, `SkillV1`, `_error` | `test_drawing_school_v1.py` | **EXISTE** |
| **E02** | École V2 : Choix d'instruments | `instrument_school_v2.py` | `learn_tool_routing` | `test_instrument_school_v2.py` | **EXISTE** |
| **E03** | École V3 : Modèle caché & Rétention | `drawing_memory_school_v3.py` | `DrawingMemorySchoolV3` | `test_drawing_memory_school_v3.py` | **EXISTE** |
| **E04** | Éducation préverbale monde physique | `preverbal_prediction_v0.py` | `WorldStateProjectionV0` | `test_preverbal_prediction_v0.py` | **EXISTE** |
| **V01** | Observation image réelle (Jarvis Qwen-VL) | `jarvis_vision_v0.py` | Client local loopback (port 8081) | `test_jarvis_vision_v0.py` | **PARTIEL** |
| **V02** | Décomposition en couches (Reverso) | `reverso_learning_v0.py` | Décomposition lossless RGBA | `test_reverso_learning_v0.py` | **EXISTE** |
| **V03** | Relations spatiales & Invariants (V4.1) | `world_relations_school_v4_1.py` | Segmentation 8-connexe, seuil NEAR/FAR | `test_world_relations_school_v4_1.py` | **EXISTE** |
| **V04** | Orientation & Réciprocité (V4.2) | `world_orientation_school_v4_2.py` | 4 directions cardinales & réciproque | `test_world_orientation_school_v4_2.py` | **EXISTE** |
| **G01** | Intent visuel & Contraintes LOCK/FLEX | `docs/24_...` | `VisualEditIntentCandidate` | Spécifié | **DOCUMENTÉ** |
| **G02** | Générateur diffusif local (sd.cpp) | `docs/22_...` | `GeneratorAdapter` | En attente VRAM | **ABSENT** |
| **G03** | Méthode du peintre multicouches | `docs/24_...`, `drawing_school_v1.py` | Passes masse → valeur → détail | `test_drawing_school_v1.py` | **PARTIEL** |
| **G04** | Évaluation inverse (Reverse Eval) | `docs/21_...`, `docs/24_...` | `ReverseEvaluationV0` | Prototype | **PARTIEL** |
| **O01** | Orchestrateur d'instruments borné | `obsidia-x108-proofs` | `ToolOrchestratorV1` | Spécifié | **ABSENT** |
| **O02** | Rejeu déterministe & Reçus cryptographiques | `experience_memory_v1.py` | `verify_memory_bundle` | `test_experience_memory_v1.py` | **EXISTE** |
| **O03** | Correction localisée en boucle fermée | `drawing_school_v1.py` | `correct_drawing` | `test_drawing_school_v1.py` | **EXISTE** |
| **R01** | Continuité multi-vues & Reverse360 | `multirepresentation_ball_bridge_v5.py` | Bridge 4 vues balle | `test_multirepresentation_ball_bridge_v5.py` | **PARTIEL** |
| **R02** | Continuité vidéo & Invariants dynamiques | `video_observation_v0.py` | Détection d'occlusion et surprise | `test_video_observation_v0.py` | **EXISTE** |
| **T01** | Batterie d'ablations comparatives | `test_compare_experience_stages_v0.py` | Comparaison 0 vs 1 vs N leçons | `test_compare_experience_stages_v0.py` | **EXISTE** |
| **T02** | Transfert E2E sur monde inédit | `world_transfer_probe_v1.py` | 12 vidéos de transfert scellées | `test_world_transfer_probe_v1.py` | **EXISTE** |

---

## 3. Architecture Mémoire Implémentée (M01–M09)

### 3.1. M01 — Frise et Temporalités stratifiées
La classe [`TimelineEnvelopeV1`](brody_world_physique/cognitive_memory_timeline_v1.py) sépare formellement 6 dimensions temporelles :
1. `t_event_iso` : Temps du phénomène dans le monde réel ou simulé.
2. `t_observation_iso` : Temps de capture par les yeux/capteurs.
3. `t_recording_iso` : Temps d'ancrage et de hachage dans le registre immuable.
4. `validity_start_iso` / `validity_end_iso` : Fenêtre de validité épistémique.
5. `educational_stage` : Chronologie éducative de Brody (ex. `DESSIN_V1`, `ORIENTATION_V4_2`), distincte du temps cosmologique.
6. `HistoricalBeliefRevisionV1` : Journal de corrections conservant les croyances antérieures (`get_belief_prior_to_revision`).

### 3.2. M02 — Registre des 34 arbres cognitifs (8 familles)
Le registre canonique audité dans `arbres_34.canon.json` est fidèlement intégré dans `CANONICAL_34_TREES` :
- **I_FONDAMENTAUX** : 01 Humain, 02 Conscience, 03 Perception, 04 Sens, 05 Identité.
- **II_COGNITIFS** : 06 Compréhension, 07 Organisation, 08 Pensée, 09 Intelligence, 10 Langage.
- **III_CONNAISSANCE** : 11 Science, 12 Technique, 13 Art, 14 Philosophie, 15 Spiritualité.
- **IV_RELATIONNELS_SOCIAUX** : 16 Relation, 17 Collectif, 18 Transmission, 19 Culture.
- **V_ACTION_TRANSFORMATION** : 20 Action, 21 Création, 22 Transformation.
- **VI_TEMPORELS_MEMORIELS** : 23 Temps, 24 Mémoire, 25 Histoire.
- **VII_META_STRUCTURELS** : 26 Cohérence, 27 Vérité, 28 Valeur, 29 Finalité.
- **VIII_OBSIDIA_AGI** : 30 Cognitif Global, 31 Flux, 32 Connexions, 33 Optimisation, 34 Stabilité.

**Règle d'or :** Une expérience est une entité unique avec son empreinte SHA-256 stable. Elle n'est **jamais dupliquée en 34 souvenirs**. Elle porte des projections pondérées [`TreeProjectionV1`](brody_world_physique/cognitive_memory_timeline_v1.py) avec justification explicite.

### 3.3. M03 — Domaines spécialisés vs Arbres
Les domaines (`PHYSICS`, `GEOMETRY`, `DRAWING`, `ART`, `VIDEO`, `ROBOTICS_EMBODIED`) sont des disciplines opérationnelles, strictement distinctes des arbres cognitifs. Chaque domaine engage un `proof_criterion` propre (ex. décroissance stricte de l'erreur XOR, invariance euclidienne sous rotation, conservation de quantité de mouvement).

### 3.4. M04–M06 — Relations multidimensionnelles & Recherche par le sens
Le moteur [`MultidimensionalCognitiveMemoryEngineV1`](brody_world_physique/multidimensional_retrieval_v2.py) implémente les 7 requêtes cognitives :
1. `HOW_DID_I_SUCCEED` : Filtre les succès prouvés, sans contre-exemple, avec confiance élevée.
2. `WHY_DID_I_FAIL` : Isole les échecs et contre-exemples pour comprendre les ruptures.
3. `WHAT_DID_I_BELIEVE_BEFORE` : Restitue la croyance de Brody avant une correction donnée.
4. `WHAT_DOES_THIS_RESEMBLE` : Rapprochement analogique par arbre ou domaine (`causality_asserted=False`).
5. `WHICH_METHOD_IS_TRANSFERABLE` : Compétences reproductibles et vérifiées.
6. `WHAT_CONTRADICTS_MY_EXPERIENCE` : Détection des anomalies et contradictions d'observation.
7. `WHICH_KNOWLEDGE_IS_VERIFIED` : Connaissances appuyées par des hachages de preuves cryptographiques.

### 3.5. M07–M09 — Calibration, Admissibilité Native Memory & Tâches Visuelles
- `EpistemicCalibrationV1` : Porte score de confiance, preuves, incertitudes, limites de validité opérationnelle et contre-exemples.
- `NativeMemoryAdmissibilityReportV1` : Évalue en lecture seule l'admissibilité au statut `CANDIDATE_ONLY` sans écriture en base canonique.
- `check_task_admissibility` : Détecte en amont tout risque de transfert négatif (ex. réemploi d'une proximité aveugle à l'orientation sur une tâche sensible à l'inversion d'ordre) et interdit formellement l'exécution directe de code mémorisé (`code_execution_permitted = False`).

---

## 4. Preuves d'exécution et tests

- Tests unitaires Vague 1 (`test_cognitive_memory_timeline_v1.py`) : **8 / 8 PASS** (0.40s)
- Tests unitaires Vague 2 (`test_multidimensional_retrieval_v2.py`) : **7 / 7 PASS** (0.17s)
- Test suite complète du dépôt : **207 passed, 1 warning, 65 subtests passed** (1m 38s).
- Zéro régression sur les 192 tests patrimoniaux (V0–V4.2, ball bridge, reverso, vidéo, contrats F0).
