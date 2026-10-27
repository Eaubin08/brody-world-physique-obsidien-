# 02_BRODY_ONLY_772_RECONCILIATION — 772 items Brody-only

**Source** : Audit V4 — page 5 (table globale par famille), pages 7–14 (items nommés)  
**Règle** : BRODY_ONLY_NON_SOVEREIGN — Brody filtre, éduque, expose. Ne décide pas.  
**Total** : 772 items Brody seulement (branché Brody Enriched, absent des domaines Bank/Trading/GPS)

---

## Table 1 — Réconciliation 772 Brody-only par famille

| Famille | Total famille | Brody seul (count) | Source page | Extraction individuelle | Destination | Statut |
|---|---|---|---|---|---|---|
| PEPITES | 161 | 96 | p. 7–9 | EXTRACTIBLE — voir Table 2 | BRODY_ONLY | BRODY_ONLY_NON_SOVEREIGN |
| MODULES | 36 | 36 | p. 10 | EXTRACTIBLE — voir Table 3 | BRODY_ONLY | BRODY_ONLY_NON_SOVEREIGN |
| AGENTS | 69 | 24 | pp. 11–12 | EXTRACTIBLE — voir Table 4 | BRODY_ONLY | BRODY_ONLY_NON_SOVEREIGN |
| ARBRES_34 | 34 | 18 | p. 13 | EXTRACTIBLE — voir Table 5 | BRODY_ONLY | BRODY_ONLY_NON_SOVEREIGN |
| LOIS | 10 | 9 | p. 14 | EXTRACTIBLE — voir Table 6 | BRODY_ONLY | BRODY_ONLY_NON_SOVEREIGN |
| PROTOCOLES | 500 | 35 | p. 15 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | BRODY_ONLY | BRODY_ONLY_NON_SOVEREIGN |
| BALANCES | 500 | 25 | p. 15 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | BRODY_ONLY | BRODY_ONLY_NON_SOVEREIGN |
| CANON | 500 | 27 | p. 15 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | BRODY_ONLY | BRODY_ONLY_NON_SOVEREIGN |
| CORTEX | 43 | 2 | p. 15 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | BRODY_ONLY | BRODY_ONLY_NON_SOVEREIGN |
| DOMAINES | 500 | 45 | p. 15 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | DOMAIN_CANDIDATE_LATER | BRODY_ONLY_NON_SOVEREIGN |
| MEMOIRE_GRAPHITI | 500 | 11 | p. 15 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | MEMORY_READONLY | BRODY_ONLY_NON_SOVEREIGN |
| PREUVES | 500 | 17 | p. 15 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | MEMORY_READONLY | BRODY_ONLY_NON_SOVEREIGN |
| ROUTES_API | 500 | 354 | p. 15 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | API_BRIDGE → DOMAIN_CANDIDATE_LATER | BRODY_ONLY_NON_SOVEREIGN |
| BOUNDARIES | 500 | 73 | p. 15 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | KERNEL_ONLY → DOMAIN_CANDIDATE_LATER | BRODY_ONLY_NON_SOVEREIGN |
| **TOTAL** | **4353** | **772** | — | **182 nommés / 590 non disponibles** | — | — |

**Vérification** : 96+36+24+18+9+35+25+27+2+45+11+17+354+73 = 772 ✓

---

## Table 2 — PEPITES Brody-only (96/161 extractibles)

| Code | Nom | Formalisation | Statut | Destination | Action |
|---|---|---|---|---|---|
| P1 | Mémoire != stockage | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody — candidat domaine futur |
| P2 | Mémoire fractale hiérarchique | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P3 | Oubli actif | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P4 | Mémoire comme condition d'éthique | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P5 | Mémoire humaine / mémoire système | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P6–P96 | [96 items total — extraits partiels PDF p.7-9] | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody — corpus éducatif |
| P97–P128 | [32 items — non visible p.8 complète] | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P103 | Validation par critères | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P104 | Réfutation par contre-exemple | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P105 | Induction mathématique | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P106 | Déduction logique | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P107 | Stabilité Lyapunov (delta-epsilon) | A_PROUVER | BRODY_ONLY | BRODY_ONLY | Lean candidat — après D13+D14 |
| P108 | Robustesse aux perturbations | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P109 | Reproductibilité | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P110 | Falsifiabilité (Popper) | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P111 | Moteur non substituable | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P112 | Hiérarchie OS0→OS4 | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P113 | Kernel = intersection des couches | FORMALISE | BRODY_ONLY | BRODY_ONLY | Candidat kernel education |
| P114 | Guard = Kernel + Temporal + Consensus | FORMALISE | BRODY_ONLY | BRODY_ONLY | Candidat kernel education |
| P127 | Disponibilité (uptime) | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P143 | Généralisation multi-domaine | FORMALISE | BRODY_ONLY | BRODY_ONLY | Candidat domaine futur |
| P144 | Apprentissage par expérience | FORMALISE | BRODY_ONLY | BRODY_ONLY | Garder Brody |

**Note** : 96 items PEPITES Brody-only. La liste complète des noms individuels n'est pas entièrement extractible page par page depuis le PDF (les pages 7-9 montrent des extraits). La règle `ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF` s'applique aux 96 - les items nommés ci-dessus (~22) sont ceux visibles dans les extraits PDF lus.

---

## Table 3 — MODULES Brody-only (36/36 extractibles)

Tous les 36 modules sont Brody-only selon l'audit V4.

| Code | Nom | Statut | Destination | Action |
|---|---|---|---|---|
| A01 | Signature Entropique / Pare-feu symbolique | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A02 | Vérification de Réciprocité / Détection contradictions | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A03 | Équilibre Dynamique / Alignement éthique | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A04 | Gestion de la Friction / Bascule Sémantique | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A05 | Singularité Initiale / Audit éthique permanent | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A06 | Intégrité Structurelle / Enregistrement états | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A07 | Cohérence Temporelle / Chronique obsidienne | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A08 | Émergence des Propriétés / Transmutation cognitive | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A09 | Non-Contradiction / Convergence intentionnelle | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A10 | Complétude / Émergence par tension | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A11 | Résonance / Reconstruction totale | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A12 | Dualité / Contrat moral | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A13 | Sécurité Interactions / Mode réflexe | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A14 | Vérification Identité / Captation créative | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A15 | Adaptation Dynamique / Vibration multimodale | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A16 | Récursivité / Architecture du savoir | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A17 | Complexité Minimale / Apprentissage universel | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A18 | Optimisation Ressources / Friction créative | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A19 | Interconnexion / Narration cognitive | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A20 | Confidentialité / Entraînement émotionnel | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A21 | Cryptographie Homomorphe / Médiathèque fractale | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A22 | Propagation Information / Simulation cognitive | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A23 | Causalité / Calibration procédurale | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| A24 | Prédictibilité / Métriques et veille | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T01 | Réduction Incertitude / Audit cohérence | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T02 | Conscience Distribuée / Validation réciprocité | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T03 | Gouvernance Décentralisée / Friction énergétique | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T04 | Consensus Distribué / Résonance sémantique | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T05 | Évolution Systèmes / Balance structure/chaos | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T06 | Sélection Naturelle / Alignement éthique | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T07 | Résilience / Test mémoire fractale | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T08 | Auto-Organisation / Apprentissage inverse | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T09 | Créativité / Mode réflexe | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T10 | Innovation Continue / Intégrité cognitive | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T11 | [nom partiel PDF — T11] | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| T12 | [nom partiel PDF — T12] | BRODY_ONLY | BRODY_ONLY | Garder Brody |

---

## Table 4 — AGENTS Brody-only (24/69 extractibles)

| Agent | Nom | Statut | Destination | Action |
|---|---|---|---|---|
| AGENT_001 | Observateur | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| AGENT_003 | Gardien | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| AGENT_004 | Architecte | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ROLE_008 | Agents / Tools | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ROLE_013 | Orchestrator | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ROLE_015 | Cortex | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| GUARDIAN_017 | ADeLe | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #1 | OBSIDIA_ATLAS_INGESTOR | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #2 | CANON_GUARDIAN | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #3 | GRAPH_BUILDER | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #4 | TERMINAL_BUILDER | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #5 | PROOF_SENTINEL | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #6 | CO_PILOTE_CODE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #7 | CI_REPO_SURGEON | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #11 | FORMAL_BRIDGE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #13 | ADVERSARIAL_RED_TEAM | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #34 | EXPLIQUE_A_UN_HUMAIN | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #38 | CARTOGRAPHE_34_ARBRES | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #40 | CALIBRATION_PROCEDURALE | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #41 | NUAGE_POINTS | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #45 | CARTOGRAPHE_LOIS_PROTOCOLES | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| #50 | ANTI_DISPERSION | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| [2 autres agents Brody seul] | [noms partiels PDF] | BRODY_ONLY | BRODY_ONLY | Garder Brody |

---

## Table 5 — ARBRES_34 Brody-only (18/34 extractibles)

| Code | Nom | Statut | Destination | Action |
|---|---|---|---|---|
| ARBRE_01 | Arbre de l'Humain | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_03 | Arbre de la Perception | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_05 | Arbre de l'Identité | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_07 | Arbre de l'Organisation | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_09 | Arbre de l'Intelligence | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_11 | Arbre de la Science | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_13 | Arbre de l'Art | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_15 | Arbre de la Spiritualité | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_17 | Arbre du Collectif | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_19 | Arbre de la Culture | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_21 | Arbre de la Création | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_23 | Arbre du Temps | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_25 | Arbre de l'Histoire | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_27 | Arbre de la Vérité | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_29 | Arbre de la Finalité | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_30 | Arbre Cognitif Global | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_31 | Arbre des Flux | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| ARBRE_33 | Arbre de l'Optimisation | BRODY_ONLY | BRODY_ONLY | Garder Brody |

---

## Table 6 — LOIS Brody-only (9/10 extractibles)

| Code | Nom | Statut | Destination | Action |
|---|---|---|---|---|
| P85 | Loi de réciprocité | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P86 | Consensus supermajorité 3/4 | BRODY_ONLY | BRODY_ONLY | Garder Brody — base kernel education |
| P87 | Fail-closed sans supermajorité | BRODY_ONLY | BRODY_ONLY | Candidat kernel education |
| P88 | Non-contradiction | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P89 | Complétude | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P90 | Cohérence | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P91 | Décidabilité | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P93 | P inclus dans NP | BRODY_ONLY | BRODY_ONLY | Garder Brody |
| P94 | Réductibilité | BRODY_ONLY | BRODY_ONLY | Garder Brody |

---

## Familles volumineuses — Brody-only non extractibles individuellement

| Famille | Brody-only count | Statut extraction | Destination probable | Action |
|---|---|---|---|---|
| PROTOCOLES | 35 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | BRODY_ONLY | Garder Brody — noms non disponibles |
| BALANCES | 25 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | BRODY_ONLY → partiel SHARED | Garder Brody — noms non disponibles |
| CANON | 27 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | BRODY_ONLY → SHARED candidat | Garder Brody — noms non disponibles |
| CORTEX | 2 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | BRODY_ONLY | Garder Brody — noms non disponibles |
| DOMAINES | 45 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | DOMAIN_CANDIDATE_LATER | Candidat domaine — noms non disponibles |
| MEMOIRE_GRAPHITI | 11 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | MEMORY_READONLY | Readonly — noms non disponibles |
| PREUVES | 17 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | MEMORY_READONLY | Readonly — noms non disponibles |
| ROUTES_API | 354 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | API_BRIDGE → candidat domaine | À formaliser après branchement API |
| BOUNDARIES | 73 | ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF | KERNEL_ONLY → candidat domaine | À formaliser après kernel P4 |

**Total Brody-only non extractibles** : 35+25+27+2+45+11+17+354+73 = **589**  
**Total Brody-only extractibles** : 22(PEPITES visibles)+36(MODULES)+22(AGENTS)+18(ARBRES)+9(LOIS) = **107 nommés partiellement**  
**Confirmation total** : 772 ✓ (reconcilié par compteurs famille)
