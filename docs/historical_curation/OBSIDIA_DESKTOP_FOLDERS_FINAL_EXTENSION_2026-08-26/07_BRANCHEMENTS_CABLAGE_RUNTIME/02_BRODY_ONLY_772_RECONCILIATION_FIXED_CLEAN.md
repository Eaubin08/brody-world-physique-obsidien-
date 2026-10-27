# 02_BRODY_ONLY_772_RECONCILIATION_FIXED_CLEAN — 772 items Brody-only (V2.1 clean patch)

**Correction V2.1** : CANON Brody-only corrigé de 11 → **27** (audit V4 page 5)  
**Clean patch** : Section "Familles avec 0 Brody-only" supprimée (contradictoire)  
**Source** : Audit V4 — page 5 (colonne "Brody seul"), pages 8–15 (détail par famille)  
**Total corrigé** : 772

---

## Table principale — 772 Brody-only par famille (CORRIGÉE)

| Famille | Brody-only | Items nommés extractibles | Items aggregate | Destination |
|---|---|---|---|---|
| PEPITES | 96 | ~22 visibles dans PDF | ~74 aggregate | BRODY_CORPUS — corpus éducatif |
| MODULES | 36 | 36 (tous nommés) | 0 | BRODY_CORPUS — A01-A24, T01-T12 |
| AGENTS | 24 | 22 nommés | 2 aggregate | BRODY_REGISTRY — agents éducation/registre |
| ARBRES_34 | 18 | 18 (tous nommés) | 0 | BRODY_CORPUS — arbres impairs |
| LOIS | 9 | 9 (tous nommés) | 0 | BRODY_CORPUS — L01-L09 |
| PROTOCOLES | 35 | 0 | 35 | BRODY_CORPUS — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF |
| BALANCES | 25 | 0 | 25 | DOMAIN_CANDIDATE_LATER — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF |
| CANON | **27** | 0 | **27** | SHARED_INFRA — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF |
| CORTEX | 2 | 0 | 2 | BRODY_CORPUS — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF |
| DOMAINES | 45 | 0 | 45 | DOMAIN_CANDIDATE_LATER — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF |
| MEMOIRE_GRAPHITI | 11 | 0 | 11 | MEMORY_READONLY — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF |
| PREUVES | 17 | 0 | 17 | MEMORY_READONLY — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF |
| ROUTES_API | 354 | 0 | 354 | API_BRIDGE — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF |
| BOUNDARIES | 73 | 0 | 73 | KERNEL_ONLY — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF |
| **TOTAL** | **772** | **107** | **665** | — |

**Vérification formule corrigée** :  
96+36+24+18+9+35+25+**27**+2+45+11+17+354+73 = **772** ✓

*(Formule V2 erronée : 96+36+24+18+9+35+25+**11**+2+45+11+17+354+73 = 756 ❌)*

---

## MODULES (36 — tous nommés)

A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, A11, A12,  
A13, A14, A15, A16, A17, A18, A19, A20, A21, A22, A23, A24,  
T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12

---

## LOIS (9 — toutes nommées)

L01, L02, L03, L04, L05, L06, L07, L08, L09

---

## ARBRES_34 Brody-only (18 — tous nommés — arbres impairs)

ARBRE_01, ARBRE_03, ARBRE_05, ARBRE_07, ARBRE_09, ARBRE_11, ARBRE_13, ARBRE_15,  
ARBRE_17, ARBRE_19, ARBRE_21, ARBRE_23, ARBRE_25, ARBRE_27, ARBRE_29, ARBRE_31,  
ARBRE_30, ARBRE_33

---

## AGENTS Brody-only (24 — 22 nommés)

AGENT_001, AGENT_003, AGENT_004, AGENT_005, AGENT_006, AGENT_007, AGENT_008,  
ROLE_001, ROLE_002, ROLE_003, ROLE_004,  
GUARDIAN_001, GUARDIAN_002, GUARDIAN_003, GUARDIAN_004, GUARDIAN_005,  
GUARDIAN_006, GUARDIAN_007, GUARDIAN_008,  
BRODY_CORE_AGENT, BRODY_ENRICHED_AGENT, BRODY_V1_AGENT  
+ [2 agents aggregate — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF]

---

## PEPITES Brody-only (96 — ~22 nommées visibles)

P01, P02, P03, P04, P05, P06, P07, P08, P09, P10,  
P11, P12, P13, P14, P15, P16, P17, P18, P19, P20,  
P21, P22  
+ [74 pépites aggregate — ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF]

---

## CANON Brody-only (27 — aggregate, correction V2.1)

**Valeur corrigée** : 27 (était 11 dans V2 originale)  
**Source** : Audit V4 page 5 — colonne "Brody seul", ligne CANON  
**Items individuels** : ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF  
**Destination** : SHARED_INFRA — présents dans Brody mais pas encore dans aucune instance kernel/domaine

---

## Note sur les familles Brody-only permanentes

Certaines familles ont la totalité ou la quasi-totalité de leurs items en statut Brody-only. Ce statut n'est pas un défaut — il reflète leur rôle permanent dans le corpus Brody.

| Famille | Brody-only | Statut permanent | Raison |
|---|---|---|---|
| MODULES | 36 / 36 | BRODY_ONLY_PERMANENT | Modules cognitifs — pas vocation domaine |
| ARBRES_34 (Brody) | 18 / 34 | BRODY_ONLY_PERMANENT | Arbres humains — corpus éducatif |
| LOIS | 9 / 10 | BRODY_ONLY_PERMANENT | Lois logiques — corpus éducatif |
| ROUTES_API | 354 / 500 | BRODY_ONLY + API_BRIDGE | Majorité routes Brody — candidats API |
| PROTOCOLES | 35 / 500 | BRODY_ONLY | Protocoles non encore formalisés |

**Règle** : BRODY_ONLY_PERMANENT = ces items n'ont pas vocation à être branchés domaine. Ils alimentent Brody Enriched / éducation uniquement.
