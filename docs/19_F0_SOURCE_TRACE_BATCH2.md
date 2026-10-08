# 19 — F0 deuxième passe : sources réelles, collisions et lecture des contrats

**Date : 2026-10-08 · Mode : DOCUMENTARY READ-ONLY · Statut : NON FREEZE.**

## 1. Portée et niveau de preuve

Lectures directes de documents historiques dans Google Drive et des **fichiers précis** du dépôt upstream `obsidia-x108-proofs` figés pour cette passe au commit [`5b9b72452cff`](https://github.com/Eaubin08/obsidia-x108-proofs/commit/5b9b72452cff7a560db992e57a43fc700dacd923). Un fichier Python lu démontre une *présence de code*, pas nécessairement un runtime connecté. Un fichier de tests lu démontre une *intention/présence de tests*, pas leur réussite actuelle. Aucun test n'a été relancé et aucune autorité KX108 n'a été modifiée.

## 2. Source officielle externe : ADeLe ≠ concept inventé par Obsidia

- [Microsoft Research, mai 2025](https://www.microsoft.com/en-us/research/blog/predicting-and-explaining-ai-model-performance-a-new-approach-to-evaluation/).
- [Microsoft Research, avril 2026](https://www.microsoft.com/en-us/research/blog/adele-predicting-and-explaining-ai-performance-across-tasks/).
- [ADeLe official academic project](https://kinds-of-intelligence-cfi.github.io/ADELE/).
- [ADeLe research source code](https://github.com/Kinds-of-Intelligence-CFI/ADeLe-AIEvaluation).
- [Archive utilisateur de la proposition ADeLe × AVDR × Obsidia](https://docs.google.com/document/d/15pZLOlYVu2POMMbU6nztWlAOIaGlnhjIa5-X9q4dtE4/edit).

**Corrigé :** ADeLe est une méthode de profil des exigences de tâches et des aptitudes des modèles sur 18 dimensions, issue de la recherche académique externe. Les sources de différentes époques emploient les expansions *Annotated-Demand-Levels* et *AI Evaluation with Demand Levels*; il faut conserver leur contexte. La contribution conceptuelle retrouvée dans les archives Obsidia est **une proposition de combinaison** avec AVDR et l'architecture, pas l'invention de l'instrument externe. Le document fourni est un dialogue avec réponses d'assistant : proposition, rédaction et auteur originel de chaque segment restent distingués.

**A2DR :** l'archive [Loi de cohérence et sélection structurelle du réel](https://docs.google.com/document/d/1eHi6LmYA-1XG94u_jau1f8vqv7Zgy76dzI1vxz-cGss/edit) cite « ADeLe / A2DR » et un « papier chinois ». Il n'y a **pas** dans cette lecture de correspondance primaire démontrée établissant identité, auteur, formule ou relation exacte A2DR ↔ ADeLe. Ne pas les assimiler. `A2DR = SOURCE_RECOVERY_REQUIRED`.

## 3. Collision ERA : atelier versus indicateur

- [Carte B9 ERA](https://docs.google.com/document/d/1Que8iatRKSCtGwuFaIHAOFQHGU4_aMn4EKRydYktfQU/edit) : **ERA-A / mental workspace**. Un espace temporaire où agents/mémoires collaborent pour une tâche. Cette définition est explicitement architecturale/interface.
- [Le Reverse OS](https://docs.google.com/document/d/1L_LG0UE4vyLn-iXF0pvjc94owZCI3McF2SWJo3TG8nY/edit) : **ERA-B / metric projection**. Ratio indicatif « Mémoire + Raisonnement + Auto / Friction » destiné à la visualisation.
- [Brody cognitive modules code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_cognitive_modules_adapter.py) : `ERA` classé `DESIGN_SPEC_NOT_IMPLEMENTED` / `active=false` dans cette version.

**Verdict :** `ERA = NAME_COLLISION`, ne pas dire que le tableau de bord numérique prouve un atelier d'agents vivant, ni l'inverse. Nulle autorité de décision.

## 4. Collision ancienne : OS Trad / Reverse

- [Souveraineté Sémantique](https://docs.google.com/document/d/1ZTisSqVwl4SUyp3T_BjZr2OxCkKaMmoUtY9W8X8oyYE/edit) : une traduction de l'entrée externe vers l'IR en amont.
- [Reverse OS](https://docs.google.com/document/d/1L_LG0UE4vyLn-iXF0pvjc94owZCI3McF2SWJo3TG8nY/edit) : un document historique emploie **OS Trad = Reverse OS = SSR**, et précise que SSR projette un état gouverné en sortie.
- [Audit canon actuel de pipeline OS Trad/IR/Reverse](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/architecture/F72_OS_TRAD_IR_REVERSE_DEEP_PIPELINE_AUDIT.md) : sépare les étapes, avec audit readonly et décisions KX108 externes.

**Verdict :** documenter la synonymie historique, mais conserver deux directions aujourd'hui : traduction entrante `input → IR`, projection sortante `état stabilisé → Reverse/SSR`. Ne pas affirmer que la séparation actuelle rendait l'ancienne terminologie fausse à sa date.

## 5. Sources contractuelles/code actuelles vérifiées par lecture


### World state / transition contracts — entrées 5–7, 13

- [MMonde code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/mmonde/contracts_v0.py)
- [Situated dynamics code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/world_dynamics/contracts_v0.py)
- [MMonde doctrine](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/architecture/MMONDE_V0_CONTRACT.md)
- [F12 report](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/architecture/SITUATED_WORLD_DYNAMICS_V0.md)

Read code: WorldObservationV0 and WorldStateV0 are readonly representation; TimeEnvelopeV0, SpatialFrameRefV0, TransitionV0 and TrajectoryV0 are situated-world contracts. No real-world truth or action authority. Legacy idea/origin may require separate user-archive genealogy.

### Brody-World F0 new contracts — entrées 8, 10–12, 14

- [F0 contracts local code](https://github.com/Eaubin08/brody-world-physique-obsidien-/blob/f0/learning-loop-contracts-v0/brody_world_physique/contracts_v0.py)
- [F0 negative tests, source](https://github.com/Eaubin08/brody-world-physique-obsidien-/blob/f0/learning-loop-contracts-v0/tests/test_contracts_v0.py)

Checked local package source and tests: four dataclass families plus additive TransitionTransformationBindingV0. Tests are present and verify negative authority boundaries, but were NOT re-executed in this pass. See exact links below.

### World Action gate — entrées 9

- [World action gateway](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/engine_gates/world_action_gateway.py)

Inspected a dry-run gateway: it reads X108 gate and proof ticket; never treat descriptive WorldTransformation as ACT. A gateway present in source is not evidence of enabled physical actuation.

### MemoryCandidate / manual promotion — entrées 24–25

- [Memory candidate code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/memory/memory_candidate.py)
- [Memory candidate ledger doctrine](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/memory/MEMORY_CANDIDATE_LEDGER_V1.md)
- [Non-promotion test source](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/tests/non_sovereignty/test_memory_candidate_ledger_no_promotion.py)

Code and test source checked; candidate memory is not promoted without controlled review. Native Memory is a broader subsystem; its end-to-end runtime has NOT been independently re-tested here.

### Real images, signal, evidence — entrées 40, 43, 45–46

- [F16 vision code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/vision/contracts_v0.py)
- [F16 report](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/architecture/VISION_REAL_IMAGE_V0.md)
- [Physical signals code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/physical_signal/contracts_v0.py)
- [Physical evidence code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/physical_evidence/contracts_v0.py)
- [F15 report](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/architecture/PHYSICAL_EVIDENCE_PLANE_V0.md)

Code provides RealImageObservationV0, physical signal candidate objects, EvidenceCompatibilityV0; provenance, candidate status and compatibility are not equal to true physical state. This is narrower than a complete physical Reality Gate implementation.

### KX108/Sigma advisory — entrées 51–53, 73, 94

- [KX108 authority](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/scripts/kernel/kx108_decision_authority_v1.py)
- [Sigma boundary](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/core_import/P56D_SIGMA_POST_GUARD_VETO_BOUNDARY.md)
- [Vote implementation](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/sigma/contracts.py)
- [Vote test source](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/tests/sigma/test_f25b_immutable_vote_minimal.py)

Sigma post-Guard may annotate/downgrade but cannot promote HOLD/BLOCK to ACT; calculate_immutable_vote is readonly advisory and preserves KX108 authority. Test file presence ≠ tests executed in this audit.

### OS3, trace and replay — entrées 55–56, 75–76, 100

- [OS3 proof ticket code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/os3_ticket.py)
- [OS3 test source](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/tests/periphery/test_os3_ticket.py)
- [OS3 schema](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/schemas/os3_proof_ticket.schema.json)

Read OS3ProofTicket builder: hashes input/output/trace and derives hash root. This provides integrity linkage of recorded objects, NOT Lean proof, physical truth, or proof that replay ran.

### Brody cognitive peripheral readers — entrées 84–89, 95

- [Fast Path code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_v3_fastpath_response.py)
- [Path Compute disabled boundary](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/path_compute_v0/boundary.py)
- [MEMZUM adapter](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_memzum_activation_adapter.py)
- [21D selector](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_point_cloud_21d_selector.py)
- [True Voice adapter](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_true_voice_adapter.py)
- [SRL audit](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/runtime/OBSIDIA_SRL_SESSION_REGISTRY_LAYER_AUDIT_V0.md)

Fast Path provides readonly responses; Path Compute's boundary has runtime_enabled=false; MEMZUM routes activation rather than memory provider retrieval; 21D selector is a bounded vector selector; True Voice is an expression adapter; SRL audit reports FOUNDATION_PRESENT_NOT_CANONICAL. No claim they are all live-wired at this commit.

### Provider boundary, CG9 — entrées 54, 77–78, 99

- [CG9 binder architecture](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/CG9_GLOBAL_PROVIDER_BINDER_V1.md)
- [Provider binder code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/scripts/providers/provider_binder_v0.py)
- [Provider binder tests](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/tests/cli/providers/test_provider_binder_v0.py)

Providers can execute bounded workloads but are non-sovereign. The phrases Runtime Binder, Provider Cognitive Binder and Global Provider Binder must not silently collapse to one implementation; compare exact interfaces before freeze.

### Oxygen education and C10 current label — entrées 61–66, 90, 93, 101–103

- [Education doctrine and C10](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/EDUCATION.md)

The file distinguishes training/calibration, education and unique identity birth; C10 here is Education/Oxygen, not the old C10 immutability block. Existing doc is explicitly doctrine+code+vision, not proof that Oxygen exists.

### Physical versus computational thermodynamics — entrées 108

- [F19 adapter doctrine](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/architecture/PHYSICAL_THERMODYNAMICS_ADAPTER_V0.md)
- [F19 code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/physical_thermodynamics/contracts_v0.py)

The physical adapter treats measurements, physical quantities, model refs and evidence as distinct from computational cost proxies (entropy_score/dissipation_score/coherence_temperature/etc.). Neither channel is a universal theory of thermodynamics.

## 6. Sources non suffisantes / incompatibles

| Entrée | Source inspectée | Verdict |
|---|---|---|
| #58 Weight-last learning | « Module 5 — cinématique » | La source discute au contraire un ajustement de poids ; elle ne prouve pas la doctrine `weight-last` actuelle. Trouver la source canon d'éducation. |
| #71 ADeLe / A2DR | « Cartographie Master » | Le texte trouvé contient AVDR mais pas la définition primaire ADeLe/A2DR. Source de l'entrée initiale inadéquate, remplacée par Microsoft + archive fusion Obsidia. |
| #93 C10 | « Constitution X108 » | Aucun C10 exact repéré dans la lecture correspondante. C10 actuel Éducation/Oxygen sourcé dans `docs/EDUCATION.md`; C10 immuabilité historique à récupérer précisément. |
| #40 RealImageObservationV0 | Master GPS de Drive | Le terme exact absent du support historique. F16 code sert de source contractuelle, pas d'origine intellectuelle de ce type. |
| #44 Physical Reality Gate | Master GPS | Un support narratif de GPS physique ne suffit pas à établir la gate exacte de runtime. Reste à auditer source du domaine GPS. |

## 7. Recommandations de continuation

1. Pour chaque `UPSTREAM_CODE_READ`, ajouter un lien d'origine intellectuelle *seulement si trouvable*, sinon écrire `ORIGIN_NOT_YET_TRACED`.
2. Vérifier les concepts expérimentaux SENS `EventRef / OccurrenceClaim / OccurrenceDerivation` à partir de la branche source, **sans confondre identité linguistique et événement physique**.
3. Séparer les collisions historiques ERA / AVDR / C10, comme déjà fait pour Balance.
4. Décomposer les vastes transcriptions Drive par date et par interlocuteur, sans publication publique brute.
5. Ne pas fusionner les PR F0 et ne pas déclencher F1 sur la seule présence documentaire.

**Conclusion de cette passe :** de nombreuses fiches disposent maintenant d'une preuve de *source* ou de *code*, mais cela ne complète ni la recherche d'origine individuelle ni une revalidation des tests runtime.
