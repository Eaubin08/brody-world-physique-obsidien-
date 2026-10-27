# 05_OK_61_BRODY_DOMAIN_RECONCILIATION — 61 items OK Brody + domaine

**Source** : Audit V4 — page 4 (verdict global), page 5 (OK complet par famille), pages 11–12 (AGENTS OK)  
**Définition** : OK = retrouvé à la fois côté Brody ET dans au moins une surface Bank / Trading / GPS.  
**Total** : 61 items — base de départ de tout branchement domaine.

---

## Table 1 — Répartition des 61 OK par famille

| Famille | OK complet | Bank | Trading | GPS | Note |
|---|---|---|---|---|---|
| PEPITES | 0 | — | — | — | Aucune pépite OK domaine |
| MODULES | 0 | — | — | — | Tous Brody seul |
| AGENTS | 10 | Oui (plusieurs) | Oui | Oui | Famille la mieux branchée |
| ARBRES_34 | 0 | — | — | — | Aucun arbre OK domaine |
| LOIS | 0 | — | — | — | Aucune loi OK domaine |
| PROTOCOLES | 0 | — | — | — | Aucun protocole OK |
| BALANCES | 3 | ? | ? | ? | 3 balances OK — items non identifiables individuellement |
| CANON | 16 | Oui | Oui | Oui | Famille CANON la plus OK — 16 items toutes instances |
| CORTEX | 0 | — | — | — | Aucun |
| DOMAINES | 6 | Oui | Oui | Oui | 6 items domaines OK |
| MEMOIRE_GRAPHITI | 1 | Oui | Oui | Oui | 1 seul item OK mémoire + domaine |
| PREUVES | 0 | — | — | — | Aucune preuve OK domaine |
| ROUTES_API | 2 | ? | ? | ? | 2 routes OK — items non identifiables individuellement |
| BOUNDARIES | 23 | Oui | Oui | Oui | BOUNDARIES = famille la + OK après CANON |
| **TOTAL** | **61** | — | — | — | — |

**Vérification** : 0+0+10+0+0+0+3+16+0+6+1+0+2+23 = 61 ✓

---

## Table 2 — AGENTS OK (10 items — extractibles individuellement)

Ces 10 agents sont les seuls items nommés individuellement confirmés OK Brody + au moins un domaine.

| Agent | Nom | Bank | Trading | GPS | Statut |
|---|---|---|---|---|---|
| AGENT_002 | Sentinelle | OK | OK | OK | OK Brody + Bank + Trading + GPS |
| ROLE_005 | Human Operator | OK | OK | OK | OK toutes instances — autorité humaine |
| ROLE_006 | Governance Layer | OK | OK | OK | OK toutes instances |
| ROLE_007 | OS3 Audit Layer | OK | OK | OK | OK toutes instances |
| GUARDIAN_009 | Sigma Verifier | OK | OK | OK | OK Brody + Bank + Trading + GPS |
| GUARDIAN_010 | Merkle Verifier | OK | OK | OK | OK toutes instances |
| GUARDIAN_011 | RFC3161 Verifier | OK | OK | OK | OK Brody + Bank + Trading + GPS |
| GUARDIAN_012 | TLA Verifier | OK | OK | OK | OK Brody + Bank + Trading + GPS |
| ROLE_014 | Adapter MCP | OK | OK | OK | OK toutes instances |
| GUARDIAN_016 | GPS Gardien / Guide / Alerteur | OK | OK | OK | OK Brody + Bank + Trading + GPS |

---

## Table 3 — Paliers P01→P80 — seul item OK avec domaine visible

| Palier | Statut domaine | Brody | Kernel | Graphiti | Runtime refs | Commit refs | Statut |
|---|---|---|---|---|---|---|---|
| P03 | OK | OK | OK | OK | 12 | 1 | OK - P visible Brody + domaine |
| P01 | — | OK | OK | — | 1 | 12 | ATTENTE DOMAINE |
| P02 | — | OK | OK | OK | 21 | 26 | ATTENTE DOMAINE |
| Tous autres P04→P80 | — | OK | partiel | partiel | var. | var. | ATTENTE DOMAINE |

**Note** : P03 est le seul palier OK Brody + domaine. Il est inclus dans les 61 items OK (probablement dans la famille CANON ou MEMOIRE_GRAPHITI).

---

## Table 4 — Items non nommés individuellement dans les 61 OK

| Famille | OK count | Extractible ? | Note |
|---|---|---|---|
| BALANCES | 3 | NON | Items dans compteur seulement — noms dans fichiers scan locaux |
| CANON | 16 | NON | Items dans compteur seulement |
| DOMAINES | 6 | NON | Items dans compteur seulement |
| MEMOIRE_GRAPHITI | 1 | NON | Item dans compteur seulement |
| ROUTES_API | 2 | NON | Items dans compteur seulement |
| BOUNDARIES | 23 | NON | Items dans compteur seulement |

**Total OK non nommés** : 3+16+6+1+2+23 = **51 items** → ITEM_LEVEL_NOT_AVAILABLE_IN_SOURCE_PDF  
**Total OK nommés** : 10 (AGENTS) → extractibles individuellement

---

## Ces 61 items comme base de branchement

| Rôle | Valeur |
|---|---|
| Socle existant | Ces 61 items prouvent que le branchement Brody+domaine est possible |
| Familles cibles prioritaires | CANON (16 OK) et BOUNDARIES (23 OK) = familles les plus avancées |
| AGENTS (10 OK) = agents de gouvernance opérationnels | ROLE_005, GUARDIANS = déjà branchés tous domaines |
| Base d'expansion | Partir des 23 BOUNDARIES OK + 16 CANON OK pour étendre vers les 355+449 non branchés |
| DOMAINES (6 OK) | Base minimale pour Bank/Trading/GPS — à faire monter vers > 100 après P3 |

---

## Séparation stricte : 61 OK ≠ 772 Brody seul

| Catégorie | Count | Signification | Ne pas mélanger |
|---|---|---|---|
| OK Brody + domaine | 61 | Branché des deux côtés | Base d'expansion |
| Brody seul | 772 | Branché Brody uniquement — pas domaine | À garder Brody ou candidat futur |
| Partiel runtime | 204 | Branchement incomplet | À résoudre via P3 + lancement |
| Non branchés strict | 3316 | Aucun branchement | À prioriser par famille |
