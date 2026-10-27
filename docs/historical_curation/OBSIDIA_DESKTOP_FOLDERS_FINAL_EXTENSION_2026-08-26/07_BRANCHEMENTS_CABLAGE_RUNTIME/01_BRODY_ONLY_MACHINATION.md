# 01_BRODY_ONLY_MACHINATION — Ce qui reste branché uniquement à Brody

**Règle** : Brody = machination / interface / filtre / corpus / éducation. Brody ne décide pas.  
**Source** : Audit V4 (772 items Brody seulement) + Checklist V3.2.3 P6 + Plan action R-07

---

## Ce que Brody PEUT faire

- Parler, exposer, contextualiser, éduquer
- Filtrer le contenu selon le niveau de divulgation (PUBLIC / INVESTOR / TECHNICAL_AUDIT / INTERNAL_FULL)
- Router une requête vers le kernel ou un domaine
- Lire la mémoire Graphiti (readonly seulement)
- Présenter les résultats d'une décision kernel
- Exposer le corpus, les pepites, les modules, les arbres, les lois comme contenu conversationnel
- Appliquer `BrodyDisclosureGuard` pour éviter les fuites de projet (RISK_SECRET_LEAKAGE)

## Ce que Brody NE PEUT PAS faire

- Prendre une décision (BLOCK / HOLD / ALLOW) — autorité KX108_ONLY
- Écrire dans Graphiti — memory_write=false permanent
- Autoriser une action sans passer par le kernel gate
- Divulguer des informations sensibles sans filtre de niveau
- Contourner `RuntimeBehaviorGate` pour les agents externes
- Promouvoir un candidat ODL ou NPL sans validation Etienne

---

## Table — Composants Brody Core et machination

| ID | Composant | Source PDF | Statut actuel | Destination | Rôle Brody | Interdit | Priorité | Dépendance |
|---|---|---|---|---|---|---|---|---|
| BC-01 | API 8000 / Brody Core | Audit V4 p.3 | ACTIF VERT | BRODY_ONLY + API_BRIDGE | Point d'entrée principal, surface API | Décider sans kernel | R-01 (kernel first) | P4-01 gardien_amont |
| BC-02 | Brody V1 Terminal | Audit V4 p.3 | ACTIF VERT | BRODY_ONLY | Instance terminal conversationnelle | Écrire en mémoire | — | API 8000 |
| BC-03 | Brody Enriched | Audit V4 p.3 | ACTIF VERT | BRODY_ONLY | Instance enrichie / corpus publication | Autoriser des actions | — | API 8000 |
| BC-04 | brody/disclosure_guard.py | Checklist P6-01 | A_CREER | BRODY_ONLY | BrodyDisclosureGuard 4 niveaux | Fuiter sans filtre | R-07 | D20 requis |
| BC-05 | brody/brody_education_curriculum_v1.py | Checklist P6-02 | A_CREER | BRODY_ONLY | Curriculum éducation Brody | Décider du contenu final | R-07 | D20 requis |
| BC-06 | brody/project_leakage_filter.py | Checklist P6-03 | A_CREER | BRODY_ONLY | Filtre anti-fuite projet | Bypasser sans approbation | R-07 | — |
| BC-07 | brody/investor_safe_mode.py | Checklist P6-04 | A_CREER | BRODY_ONLY | Mode investisseur sécurisé | Révéler données internes | R-07 | D20 |
| BC-08 | brody/public_demo_mode.py | Checklist P6-05 | A_CREER | BRODY_ONLY | Mode démo public | Exposer secrets projet | R-07 | D20 |
| BC-09 | brody/internal_operator_mode.py | Checklist P6-06 | A_CREER | BRODY_ONLY | Mode opérateur interne | Bypasser disclosure guard | R-07 | D20 |

---

## Table — Corpus, Pépites, Modules, Arbres, Lois (Brody seulement)

| ID | Composant | Source PDF | Statut actuel | Destination | Rôle Brody | Interdit | Priorité | Dépendance |
|---|---|---|---|---|---|---|---|---|
| BR-01 | PEPITES (161 items P1–P161) | Audit V4 p.5–9 | 96 Brody seul / 65 non branchés | BRODY_ONLY | Contenu conversationnel / éducation | Promotion kernel sans décision | LONG TERME | Brody Enriched actif |
| BR-02 | MODULES A01–A24 / T01–T12 (36) | Audit V4 p.10 | 36 Brody seul | BRODY_ONLY | Modules cognitifs — référence Brody | Connexion domaine sans validation | MOYEN TERME | Brody Enriched |
| BR-03 | ARBRES_34 ARBRE_01–ARBRE_34 | Audit V4 p.13 | 18 Brody seul / 16 PAS BON | BRODY_ONLY | Arbres cognitifs humains — corpus | Connexion directe kernel | LONG TERME | Brody Enriched |
| BR-04 | LOIS P85–P94 (10 lois) | Audit V4 p.14 | 9 Brody seul / 1 PAS BON (P92) | BRODY_ONLY | Lois logiques formelles — éducation | Décision basée sur loi seule | MOYEN TERME | Brody Enriched |
| BR-05 | PROTOCOLES (500) | Audit V4 p.5 | 35 Brody seul / 465 PAS BON | BRODY_ONLY | Protocoles — corpus éducatif | Exécution protocole sans kernel | LONG TERME | Brody Enriched |
| BR-06 | BALANCES (500) | Audit V4 p.5 | 3 OK / 25 Brody seul / 418 PAS BON | BRODY_ONLY → partiel SHARED | Balances — exposées via Brody | Décision sur balance sans kernel | LONG TERME | Kernel + Brody |
| BR-07 | Corpus publication / Brody Enriched | Audit V4 p.2 | ACTIF VERT | BRODY_ONLY | Interface conversationnelle enrichie | Écriture mémoire | — | — |

---

## Table — Agents Brody seulement (issus du registre 52)

| ID | Agent | Source PDF | Statut actuel | Destination | Rôle Brody | Interdit | Priorité | Dépendance |
|---|---|---|---|---|---|---|---|---|
| AG-B01 | #1 OBSIDIA_ATLAS_INGESTOR | Audit V4 p.11 | Brody seul | BRODY_ONLY | Ingestion corpus atlas — lecture | Connexion kernel directe | MOYEN TERME | Brody Enriched |
| AG-B02 | #4 TERMINAL_BUILDER | Audit V4 p.11 | Brody seul | BRODY_ONLY | Génère commandes safe | Exécuter sans approbation | — | — |
| AG-B03 | #6 CO_PILOTE_CODE | Audit V4 p.11 | Brody seul | BRODY_ONLY | Co-pilote code / repo | Merger sans review | — | — |
| AG-B04 | #7 CI_REPO_SURGEON | Audit V4 p.11 | Brody seul | BRODY_ONLY | Chirurgie repo CI | Modifier kernel/proof | — | — |
| AG-B05 | #11 FORMAL_BRIDGE | Audit V4 p.11 | Brody seul | BRODY_ONLY | Bridge formel — lecture | Modifier preuves Lean | — | DO_NOT_TOUCH Lean |
| AG-B06 | #13 ADVERSARIAL_RED_TEAM | Audit V4 p.11 | Brody seul | BRODY_ONLY | Test adversarial — Brody uniquement | Accès kernel en écriture | — | — |
| AG-B07 | #34 EXPLIQUE_A_UN_HUMAIN | Audit V4 p.12 | Brody seul | BRODY_ONLY | Vulgarisation — interface humaine | Décider pour l'humain | — | — |
| AG-B08 | #38 CARTOGRAPHE_34_ARBRES | Audit V4 p.12 | Brody seul | BRODY_ONLY | Cartographie arbres cognitifs | Connexion domaine | — | Arbres 34 |
| AG-B09 | #45 CARTOGRAPHE_LOIS_PROTOCOLES | Audit V4 p.12 | Brody seul | BRODY_ONLY | Cartographie lois / protocoles | Connexion domaine | — | — |
| AG-B10 | #50 ANTI_DISPERSION | Audit V4 p.12 | Brody seul | BRODY_ONLY | Anti-dispersion contexte | Connexion kernel | — | — |

---

## Résumé Brody

- **772 items** restent actuellement Brody seulement (source audit V4)
- **Objectif** : ne pas tous les brancher aux domaines — statuer lesquels restent BRODY_ONLY
- **Règle fondamentale** : tout item BRODY_ONLY peut parler, exposer, éduquer — jamais décider
- **Niveau de disclosure** géré par `BrodyDisclosureGuard` (P6-01) après D20 validé par Etienne
