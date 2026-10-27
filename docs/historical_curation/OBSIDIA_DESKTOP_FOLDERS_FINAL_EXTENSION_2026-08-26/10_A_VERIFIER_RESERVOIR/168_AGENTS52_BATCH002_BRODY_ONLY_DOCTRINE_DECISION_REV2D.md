# ART168 -- AGENTS52_BATCH002_BRODY_ONLY_DOCTRINE_DECISION_REV2D

## Date : 2026-08-02T00:00:00+00:00
## Phase : RECORD_AND_CLOSE_AGENTS52_BATCH002_BRODY_ONLY_HUMAN_DECISION_001

---

## §1 Contexte

Au moment de l'audit du ledger V5, les ROW_ID 1822, 1824 et 1825 portaient le
statut `BRODY_ONLY_INTENTIONAL`. Ce statut décrivait un état constaté — attente
domaine, ancrage Brody exclusif — et non une interdiction permanente de
référencement readonly.

Le commit 26468c37246ea7ca9e78dba46ab259170e086f4f a enregistré ces trois
configurations comme entrées readonly dans `periphery/agents_obsidia_config_registry.py`
(AGENTS52_BATCH002), les exposant via l'API de configuration en lecture seule.

---

## §2 Décision humaine explicite

**DECISION : OPTION_A_KEEP_BATCH002_ALL_FIVE**

Les transitions suivantes sont **approuvées explicitement** :

| ROW_ID | AGENT_ID | Ancien statut | Nouveau statut |
|--------|----------|---------------|----------------|
| 1822 | CARTOGRAPHE_34_ARBRES | BRODY_ONLY_INTENTIONAL | WIRED_PROVED_STATICALLY |
| 1824 | CALIBRATION_PROCEDURALE | BRODY_ONLY_INTENTIONAL | WIRED_PROVED_STATICALLY |
| 1825 | NUAGE_POINTS | BRODY_ONLY_INTENTIONAL | WIRED_PROVED_STATICALLY |

**Raison** : `READONLY_REGISTRATION_AND_API_EXPOSURE_ONLY`

---

## §3 Doctrine établie

### Ce que cette décision accorde

- Enregistrement readonly de la configuration dans `agents_obsidia_config_registry.py`
- Exposition via `GET /api/periphery/governance/agents-52`
- Exposition via `GET /api/periphery/governance/agent-config/{agent_id}`
- Statut ledger `WIRED_PROVED_STATICALLY` (preuve directe = registre commité)

### Ce que cette décision n'accorde pas

- Aucune capacité d'exécution agentique
- Aucune connexion au runtime d'exécution (`EXECUTION_RUNTIME: NOT_CONNECTED`)
- Aucune validation sémantique (`NEEDS_HUMAN_VALIDATION` préservé)
- Aucun transfert d'autorité hors KX108
- Aucune écriture mémoire (`memory_write = false`)
- Aucune écriture Graphiti ou Neo4j
- Aucune émission ACT
- Aucune décision autonome

### Relation avec Brody

| Aspect | Statut |
|--------|--------|
| Provenance historique Brody | PRÉSERVÉE dans l'historique du ledger |
| Relation historique Brody | PRÉSERVÉE — le ledger V6 conserve les champs historiques |
| Autorité d'exécution Brody | NON TRANSFÉRÉE — KX108 conserve seul l'autorité |
| Rôle du registre AGENTS_52 | Consommateur de configuration readonly secondaire |

Le statut `BRODY_ONLY_INTENTIONAL` décrivait une attente de domaine, pas une
interdiction permanente. La connexion readonly ne remplace pas Brody comme
producteur historique : elle enregistre que ces configurations ont désormais
une représentation technique readonly en dehors du seul ancrage Brody.

---

## §4 Distinction de rôles post-décision

```
BRODY_ROLE:
  Historical source / prior anchor / possible future semantic context

AGENTS52_REGISTRY_ROLE:
  Readonly configuration registration and provenance exposure

API_ROLE:
  Readonly inspection only (GET endpoints)

EXECUTION_ROLE:
  None — agent-run returns HTTP 422 for all 52 agents52 IDs

KERNEL_AUTHORITY:
  Unchanged — KX108_ONLY
```

---

## §5 Distribution V6 approuvée

| Statut | V5 | V6 | Delta |
|--------|----|----|-------|
| WIRED_PROVED_STATICALLY | 82 | 87 | +5 |
| NONWIRED_UNKNOWN_DESTINATION | 69 | 67 | -2 |
| BRODY_ONLY_INTENTIONAL | 702 | 699 | -3 |
| Tous les autres | 3500 | 3500 | 0 |
| **TOTAL** | **4353** | **4353** | **0** |

La différence avec l'hypothèse initiale du mandat (NONWIRED -5) est
**volontairement acceptée** : trois lignes provenaient de `BRODY_ONLY_INTENTIONAL`
et non de `NONWIRED_UNKNOWN_DESTINATION`. Le calcul effectué depuis les fichiers
prime sur l'hypothèse initiale.

---

## §6 Ledger V6

```
ART162 : APPROVED_AS_GENERATED
LEDGER_V6_REGENERATION_REQUIRED : false
BRODY_GOVERNANCE_ELEMENT_ROWS_CHANGED : 0
AGENTS52_BRODY_ONLY_CONFIG_ROWS_RECLASSIFIED : 3
SEMANTIC_VALIDATION_PRESERVED : true
```

---

## §7 Chaîne de preuves complète Batch 002

ART115 → ART118 → ART120 → ART122 → ART123 → ART124 → ART127 →
ART128 → ART129 → ART130 → ART131 → ART132 → ART133 → ART134 →
ART135 → ART136 → ART137 → ART138 → ART139 → ART140 → ART141 →
ART142 → ART143 → ART144 → ART145 → ART146 → ART147 → ART148 →
ART149 → ART150 → ART151 → ART152 → ART153 → ART154 → ART155 →
ART156 → ART157 → ART158 → ART159 → ART160 → ART161 → ART162 →
ART163 → ART164 → ART165 → ART166 → ART167 → ART168 → ART169 → ART170

---

STATUS: AGENTS52_BATCH002_BRODY_ONLY_TRANSITIONS_HUMAN_APPROVED

NEXT_STEP: VERIFY_REMOTE_STATE_AND_DRY_RUN_AGENTS52_BATCH002_PUSH
