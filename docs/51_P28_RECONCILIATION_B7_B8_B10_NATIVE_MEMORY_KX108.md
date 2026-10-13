# P2.8 — Matrice de réconciliation avant forge (F0)
Statut : **AUDIT PARTIEL — BLOQUÉ POUR IMPLÉMENTATION PERSISTANTE**.
Ce document complète `docs/50_P28_CONTRAT_SAVOIR_HIERARCHISE_STABILISATION_INTENTION.md` sans changer le moteur, ni les contrats canoniques.

## Sources réellement consultées
- `obsidia-x108-proofs/apps/obsidia_api/brody_obsidia_native_memory.py` (lecture GitHub) : `NATIVE_MEMORY_BOUNDARY` impose readonly, memory_write=false, canonical_write=false, auto_promotion=false, allowed_to_decide=false, allowed_to_act=false, emits_verdict=false, kernel_mutation=false, KX108_ONLY. `build_native_memory_retrieval_snapshot` obéit à `memory_required` décidé par MEMZUM. Il fait du retrieval, **pas** de promotion de savoir.
- Les résultats de P2.7 communiqués par l'opérateur : 480 TEST, 120 TRAIN, publication des preuves GitHub en échec sur une policy PowerShell ; 3 tests locaux OK. `experience` supervisé par la vérité du simulateur, indice fiable fixé par construction.
- `docs/50_...md` de ce dépôt sur la branche de travail : proposition d'auteur, non preuve de capacité.
- **B7/B8/B10 : texte canonique intégral et branches actives non vérifiés dans cet audit.** La nomenclature disponible dans la conversation : B7_ACCEPT != DURABLE_KNOWLEDGE ; VALIDATED_WORKING_CONTEXT != MEMORY ; BELIEF != KNOWLEDGE ; OBSERVED != VERIFIED ; CONFIDENCE != TRUTH ; CONFIDENCE != AUTHORITY ; CANDIDATE != PROMOTED ; COGNITIVE_PROPOSAL != MEMORY_AUTHORITY ; HUMAN_APPROVAL != TRUTH. Ce sont des références documentaires à confirmer contre les fichiers canoniques, pas une preuve de code actuel.

## Correspondances obligatoires — pas de nouvelles autorités
| P2.8 (concept candidat) | Relation recherchée | Frontière conservée | Statut audit |
|---|---|---|---|
| OBSERVED / DERIVED | observation ou dérivation de travail, jamais vérité | aucune promotion automatique | PROPOSÉ |
| EXPERIENCED | épisode avec conditions, observations, réussite ET échecs | expérience != preuve de vérité universelle | PROPOSÉ |
| RETAINED_WORKING | meilleure hypothèse active, révisable | ne vaut pas mémoire durable ni B7_ACCEPT | PROPOSÉ |
| STABILIZED_CANDIDATE | repère réutilisable dans un périmètre | stabilisé != vérifié/promu | PROPOSÉ |
| VERIFIED_SCOPED | vérification dans un domaine explicite | passerelle B8 à auditer ; pas de promotion implicite | BLOQUÉ B8 |
| CHALLENGED / SUPERSEDED | contradiction, historique et non-effacement | ne pas modifier la mémoire canonique sans gate | PROPOSÉ |
| Intention utilisateur | choisit but, précision, exploration/génération | désir != vérité, approbation != vérification | PROPOSÉ |
| Recherche mémoire native | lecture de repères déjà autorisés | MEMZUM décide activation ; Brody retrieval readonly | **VÉRIFIÉ SOURCE** |
| Écriture/promotion B10 | procédure persistante gouvernée | aucun memory_write ni canonical_write côté Brody | BLOQUÉ B10 |
| Décision finale | pas un service cognitif ni son score | KX108_ONLY, fail-closed | **VÉRIFIÉ SOURCE** |

## Conditions avant tout code de promotion
1. Localiser **sur branches effectives** les sources B7/B8/B10 et leurs schemas, invariants, tests et point d'entrée write-gate. Vérifier le nom/chemin/commit ; ne pas mapper sur supposition.
2. Faire un tableau de compatibilité champ par champ : état cognitif vs evidence vs knowledge vs mémoire vs décision ; preuves de non-mutation, liens de replay et règles temporelles.
3. Garder tous les registres P2.8 en **sandbox d'expérimentation, éphémères, non souverains** : candidats de savoir, provenance et historique de contradictions en fichiers de preuve de test seulement.
4. Pré-geler les scénarios de changement de repère et de dépendances corrélées (TRAIN/TEST disjoints), modes d'intention, faux signaux majoritaires, HOLD, réouverture, et cas d'échec volontaire.
5. Tests de sécurité : intention ne change jamais la vérité ; une contradiction ne déclenche pas un write ; source readonly reste readonly ; confiance haute ne confère pas autorité ; les preuves de succès anciennes demeurent consultables après révision ; toute dépendance à un autre repère est explicitée.
6. Aucun merge main, aucun runtime KX108/Native Memory/B7-B10 modifié sur cette base.

## Critère de sortie F0
F0 = OUI seulement quand les contrats B7/B8/B10 actuels ont été lus depuis leurs branches effectives, qu'un mapping de schéma et de transitions est signé, et qu'aucune violation d'autorité ou de mutation n'est observée. Actuellement : **F0 INCOMPLET / HOLD**.

Prochaine action permise sans F0 : implémenter **uniquement des simulations P2.8 sans aucune persistance ni promotion réelle**, ou poursuivre la recherche documentaire B7/B8/B10.
