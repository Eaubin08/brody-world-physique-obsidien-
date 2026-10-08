# 42 — Audit transversal : un monde, plusieurs représentations, plusieurs échelles

**Projet :** Brody World Physique Image. **Date :** 2026-10-09.  
**État :** AUDIT DOCUMENTAIRE ET CONTRAT D'INTEROPÉRABILITÉ *CANDIDAT*, **pas** un moteur implémenté.  
**Périmètre :** reprendre les quatre échanges utilisateurs du 09/10 sur (1) l'écart représentation spatiale / pixels, (2) mouvement et autres représentations, (3) micro, nano, moléculaire et totalité des échelles, (4) comment poursuivre ; les raccorder à la vision FSO / Reverso / école humaine / MMonde / F12 / F16 / SENS / GPS / preuves V1–V4.2.  
**Exécution :** audit des fichiers GitHub et conception uniquement. Aucun code opérationnel, poids, test, branche SENS/GPS ou mémoire canonique modifiés par ce chapitre.

## 0. Discipline d'attribution — ce qui vient de qui

- **U — demande utilisateur contemporaine :** l'écart spatial / pixels suggère plusieurs représentations d'une même chose ; ajouter mouvement, temps, autres descriptions ; aller du subatomique, moléculaire, nanoscopique et microscopique jusqu'au cosmique ; demander une suite qui préserve tout ce qui est déjà construit. La *direction* appartient à l'utilisateur.
- **U — archives utilisateur identifiées :** méthode analyse ↔ synthèse / réciproque, fidélité à l'IN / source, enseignement comme un enfant, éviter de refaire des routes existantes, apprentissage par essais et corrections, perspective 360°, symétrie, proportion et Fibonacci comme **pistes à étudier**, pas lois universelles prouvées. Sources [FSO](https://docs.google.com/document/d/14yk4MPqd5rd3RnB1AAyys8zHU4KD4Dq1eqNtLQFJTA0/edit), [27](27_REVERSO_WORLD_MODEL_APPRENTISSAGE_SELECTIF.md), [24](24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md). Les citations historiques et leur degré d'attribution se trouvent dans [23](23_BRODY_IMAGE_LEARNING_TRACEABILITY.md) et [18](18_CONCEPT_SOURCE_MATRIX.md).
- **C — contrats/code vérifiés dans les dépôts :** types MMonde, F6/F12/F13/F15/F16, contrats F0 de Brody, mécanismes V1–V4.2 et F19 (sur commit **épinglé**, distinct de la branche F16), documents expérimentaux SENS. La présence d'une classe prouve l'existence d'un contrat, **pas** l'activation d'une capacité scientifique générale.
- **P — propositions techniques de ce chapitre :** identifiants transversaux référencés, vues multidimensionnelles, matrice de passages entre représentations, sélection des premières expériences, scores et gates. Ces propositions **ne sont ni des paroles historiques de l'utilisateur ni des fonctions déjà opérationnelles**.
- **A — précisions/propositions précédentes de l'assistant :** les hiérarchies de sept échelles, le schéma « monde → représentation → image », et le protocole de balle commun sont des *synthèses et propositions*. La vision utilisateur dépasse une simple hiérarchie de tailles et inclut matière, vivant, énergie, information, cognition et relations.

## 1. Ce que les quatre échanges établissent

### E1 — Spatial ≠ image pixel

**Mesure sur V4.2 :** 8 leçons supervisées, 11/11 examens de classification/abstention conformes, 5 HOLD, 6 relations réciproques, reconstruction d'une relation gauche/droite correcte **mais** `pixel_xor=536`, `blank_error=536`, `pixel_iou≈0,298`. Échec de fidélité raster conservé ; **réussite relationnelle != copie exacte**, sans que cela prouve la compréhension d'objets réels.

**Décision de conception :** ne plus réduire le résultat à un unique score de pixels ni supprimer ce score. Conserver séparément :
1. valeur de relation spatiale (avec repère et orientation) ;
2. fidélité des formes/proportions ;
3. alignement spatial à transformation *autorisée* ou non ;
4. fidélité raster stricte, jamais remplacée par une métrique indulgente ;
5. intégrité de la source et statut de réalité de l'image.

Source : [V4.2](41_BRODY_V4_2_ORIENTATION_RECIPROQUE_MONDE.md), [code](../brody_world_physique/world_orientation_school_v4_2.py), [preuves CI](https://github.com/Eaubin08/brody-world-physique-obsidien-/actions/runs/37858706598), [archives PC](https://github.com/Eaubin08/brody-world-physique-obsidien-/tree/evidence/brody-local).

### E2 — Les représentations ne sont pas seulement visuelles/spatiales

**Ensemble de dimensions à permettre, sans les confondre :**
- apparence/raster/couleur/lumière/texture et production par gestes ;
- géométrie 2D/3D, topologie, proportions, occlusion, repères, transformations de point de vue ;
- temps (observation, événement, validité, acquisition du savoir — **non équivalents**) ;
- cinématique (position, trajectoire, vitesse, accélération, rotation) ;
- mécanique et causalité *hypothétique*, y compris forces, collisions et contraintes ;
- matière et thermodynamique *physiques*, chimie et matériaux ;
- information, signal, multimodalité, confiance, épistémologie ;
- savoir-faire procédural et choix d'outils ;
- vivant, émergence, comportements collectifs, niveaux planétaire/cosmique.

**Principe :** une représentation est une projection partielle d'un objet/état/événement *candidat* ; ses variables, son repère, son domaine de validité et son niveau de preuve sont explicites. L'existence d'un lien ne rend pas les représentations identiques.

### E3 — « Aller au bout de l'existence » : micro / nano / moléculaire / atomique / subatomique / macro / cosmos

Les échelles de taille **se chevauchent** et ne forment pas une échelle de vérité linéaire. Un niveau change parfois les observables, unités, instruments, descriptions statistiques ou lois applicables. Inclure :
- subatomique / quantique : variables, état et incertitude dépendant du modèle ; **aucune dérivation depuis des pixels ordinaires** ;
- atomique : structure, transitions, mesures spectrales et modèles ;
- moléculaire / nanoscopique : liaisons, structures, interactions, réactions, matériaux ;
- microscopique / biologique : microstructure, cellules, propriétés émergentes ;
- mésoscopique / macroscopique : objet, contraintes mécaniques, champ, flux, trajectoire ;
- environnement / planétaire : système ouvert, météo, géologie, écologie ;
- stellaire / cosmologique : dynamiques gravitationnelles et observations indirectes.

**Pas de faux zoom :** une vidéo macro d'une balle ne fournit pas sa structure moléculaire ni sa composition atomique. Une projection micro → macro nécessite un **opérateur/loi/modèle avec hypothèses et domaine de validité**, et une inversion macro → micro peut être impossible ou non unique. `UNKNOWN / NOT_IDENTIFIABLE_FROM_SOURCE` est une réponse correcte.

### E4 — Comment avancer sans repartir de zéro

Un même phénomène-test doit parcourir **plusieurs représentations** : image → coordonnées/repère → trajectoire/temps → prédiction → rendu futur → re-perception → écarts séparés → expérience candidate. Ensuite seulement, établir des ponts micro↔macro *quand une mesure/instrument/loi vérifiable le justifie*. Ne pas créer sept nouveaux moteurs.

## 2. Carte des propriétaires existants et état de preuve

| Porteur réel | Fichiers / contrats constatés | Réutilisation prévue | État de la couverture |
|---|---|---|---|
| **MMonde** | `WorldObservationV0`, `WorldStateV0` [code upstream](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/mmonde/contracts_v0.py) | Observation sourcée, état candidat et identité référencée | Contrat existant ; pas un moteur physique universel |
| **F6 multimodal** | `ModalityObservationV0`, [pont](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/multimodal/bridge_v0.py) | Canaux image/son/vidéo/capteurs, sources/horloges distinctes | Contrat de fusion conservatrice, pas compréhension multimodale générale |
| **F12 dynamique** | `TimeEnvelopeV0`, `SpatialFrameRefV0`, `TypedRelationV0`, `TransitionV0`, `TrajectoryV0` [code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/world_dynamics/contracts_v0.py) | Ordres et trajectoires typés, rupture/continuité candidate | Contrat vérifié dans sa branche, sans loi physique inférée |
| **F13 mesure** | `SituatedMeasurementV0`, `MeasurementContextV0`, `InstrumentRefV0` [code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/measurement/contracts_v0.py) | Grandeurs, unités, précision, calibration, limites | Contrat mesurable ; provenance ne suffit pas à prouver authenticité |
| **F15 compatibilité** | `EvidenceCompatibilityV0` [code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/physical_evidence/contracts_v0.py) | Concordance temporelle/spatiale/métrique/causale/indépendance | Candidat readonly, pas vérité |
| **F16 vision réelle** | `RealImageObservationV0`, `VisualPrimitiveV0` [code](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/vision/contracts_v0.py) | Images réellement capturées, mouvement/masque/profondeur en références, intégrité | Refuse `generated=True` ; les PNG des cours sont **SIMULATED/GENERATED**, pas F16 réel |
| **F18/F19 sciences/thermo** | F19 `PhysicalThermodynamicStateCandidateV0` [code épinglé](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/physical_thermodynamics/contracts_v0.py), [doc](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/architecture/PHYSICAL_THERMODYNAMICS_ADAPTER_V0.md) | Mesure physique + unité + modèle/applicabilité, **sans** assimiler `entropy_score` cognitif à entropie physique | Existence au commit épinglé, **pas dans la branche F16 consultée** ; raccordement runtime non vérifié |
| **GPS / signaux** | [`RecordedGpsEvidenceV0`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/gps_physical/bridge_v0.py), historique Trusted Navigation | Continuité de preuve, repères, contradiction/qualité du capteur | GPS n'est ni un simulateur d'image ni une preuve automatique de même identité |
| **Brody F0** | [`WorldTransformationV0`, `WorldStateProjectionV0`, `WorldStateDeltaV0`, `WorldExperienceCandidateV0`](../brody_world_physique/contracts_v0.py) | Création de candidats d'expériences, projections, deltas | Implémentés en local, pas nouveau root de MMonde |
| **Brody mouvement** | [`experiential_video_v0.py`](../brody_world_physique/experiential_video_v0.py), [`world_transfer_probe_v1.py`](../brody_world_physique/world_transfer_probe_v1.py), [`reverso_future_preview_v1.py`](../examples/reverso_future_preview_v1.py) | Détection 2D, prédiction d'après expériences, repère caméra, surprise, HOLD, image future recomposée | Simulateur, biais/détecteurs/découpage programmés |
| **Brody V1–V4.2** | [école instruments](37_ECOLE_INSTRUMENTS_SELECTION_EXPERIENTIELLE_V2.md), [mémoire V3](38_DESSIN_MEMOIRE_MODELE_CACHE_V3.md), [pont V4](39_BRODY_MONDE_EXPERIENCE_V4_BRIDGE.md), [V4.1](40_V4_1_RELATIONS_SPATIALES_INVARIANTS_ET_COMPOSITION.md), [V4.2](41_BRODY_V4_2_ORIENTATION_RECIPROQUE_MONDE.md) | Gestes/outils, images, relation/reciproque, preuve avant révélation, monde candidat | Validé **dans leurs exercices synthétiques bornés** |
| **SENS** | [`OrderedMeaningFlow`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/exp/semantic-grammar-cognitive-lattice-v0/docs/semantic/ORDERED_MEANING_FLOW_V0.md), [convergence](https://github.com/Eaubin08/obsidia-x108-proofs/blob/exp/semantic-grammar-cognitive-lattice-v0/docs/semantic/MEMORY_LANGUAGE_CONVERGENCE_V0.md) | Différencier objet, projection, famille temporelle/causale/épistémique, connaissances et mémoires | Documents et expériences de branche, **pas** un B8/B10 branché dans Brody |
| **Native Memory / X108** | [contrats F0](02_CONTRACTS.md) | Retenir candidats, puis adapter sous autorité propre ; `KX108_ONLY` | Aucun `memory_write`, auto-promotion, action ou mutation du kernel autorisé |

**Attention à l'état PRE-FORGE** : les **29/53 jalons fermés et le B8 au jalon 30** sont le checkpoint de pilotage rapporté par l'utilisateur, **pas** une certification externe refaite ici. L'amendement T12 `09d4fe74` est local selon l'utilisateur et son audit indépendant reste à faire. Ce chapitre ne touche **ni Class D, ni B8, ni B9/B10**.

## 3. Contrat transverse candidat — pas une nouvelle ontologie souveraine

### 3.1 Un référent, plusieurs vues *sourcées*

Plutôt que « un fichier mémoire par modalité », prendre une **référence candidate d'entité ou de phénomène**, attachée à des vues :
- **observation_ref** : source exacte, hash, `REAL_CAPTURED / SIMULATED / GENERATED / INFERRED / UNKNOWN` ;
- **entity_candidate_ref** : identité proposée, avec `identity_basis` (même SHA, suivi temporel, annotation humaine, mesures physiques, hypothèse, inconnu) ; **ne pas fusionner deux entités sur leur seule ressemblance** ;
- **representation_kind** : `RASTER`, `GEOMETRY`, `SPATIAL_RELATION`, `TEMPORAL`, `KINEMATICS`, `THERMODYNAMIC_PHYSICAL`, `MATERIAL`, `CHEMICAL`, `BIOLOGICAL`, `CAUSAL_HYPOTHESIS`, `PROCEDURAL`, etc. **Vocabulaire de vue P, pas types canoniques à créer maintenant** ;
- **reference_frame / temporal_basis / scale_scope** : repère, sens des axes, unités, horloges, domaine, résolution, échelle utile, environnement ;
- **value_or_ref** : valeurs ou références vers les contrats **existants**, pas copie mutable de leur contenu ;
- **epistemic_status / uncertainty / contradictions / evidence_refs** : observation ≠ interprétation ≠ croyance ≠ inférence ≠ connaissance vérifiée ;
- **transformation_ref / projection_ref / delta_ref / experience_candidate_ref** : suivi explicite dans les classes Brody F0 existantes.

Il s'agit d'une **vue/index local dérivé** ; MMonde conserve la propriété de `WorldStateV0`, F12 du mouvement, F16 des images réelles, F13/F19 des quantités physiques et SENS des états épistémiques. Aucun `UniversalEntity`, `GlobalMemoryWorld` ou `SuperWorldState` ne doit être codé à ce stade.

### 3.2 Passages entre représentations : quatre types distincts

| Type de passage | Exemple | Nature et limite |
|---|---|---|
| **Projection** | position 2D mesurée → masque déplacé → pixels recomposés | Le rendu ne devient pas preuve de la future scène réelle |
| **Estimation** | deux/trois observations sourcées → vitesse apparente dans un repère | Nécessite temps/repère cohérents ; pixels/s != m/s |
| **Changement de repère / point de vue** | scène fixe + caméra mobile → coordonnées ancrées | La face cachée non observée demeure `UNKNOWN` |
| **Changement d'échelle / modèle** | déformation macro → hypothèses sur un matériau et ses constituants | Souvent **non inversible**, demande modèle + paramètres + mesures indépendantes ; pas d'inférence moléculaire depuis la seule vidéo |

L'**analyse ↔ synthèse / Reverso** devient une batterie de deux parcours vérifiables `observations → vue dérivée → prédiction/génération` puis `image produite → re-perception → delta`. « Retour A→B→A » mesure des invariants, il ne prouve pas que B est la seule réalité possible.

### 3.3 Ce qui doit rester séparé

- **Image réelle** ≠ image simulée ≠ image générée ; `RealImageObservationV0` n'est jamais instanciée pour l'une des deux dernières.
- **Similitude** ≠ même identité ; même source SHA ≠ reconnaissance d'un objet physique.
- **Ordre temporel** ≠ causalité ; corrélation ≠ force identifiée ; causalité linguistique ≠ preuve physique.
- **Temps de scène** ≠ temps d'observation ≠ temps d'enregistrement mémoire.
- **Thermodynamique physique** (température, énergie, chaleur, entropie avec mesures/unités/système) ≠ coûts/entropie/« température » *cognitifs* internes.
- **Invariant géométrique** ≠ identité de pixels ; seuil appris sous supervision ≠ conception autonome.
- **Micro / macro** ≠ simple changement de zoom ; quantité absente ≠ quantité nulle.
- **WorldState** ≠ mémoire : la **mémoire doit pointer vers le monde et l'historique des transformations**, pas s'arroger l'autorité des observations ou de la promotion.
- **KX108_ONLY** reste unique frontière de décision ; aucune donnée de Brody ne devient un ordre d'action.

## 4. Ce qui manque *effectivement* aujourd'hui

1. Une **jointure exécutable et auditée** entre le pipeline vidéo expérientiel existant (V0/transfer) et les observations MMonde/F12, projections/deltas F0 et la reconstruction Reverso d'une **même expérience**. Aujourd'hui ces preuves vivent principalement dans des bancs différents.
2. Un **test d'ablation inter-représentations** qui démontre qu'image+espace+temps+mouvement fait mieux qu'une route isolée, sur **mêmes sources et mêmes instants**.
3. Un contrôle d'**inversibilité/identifiabilité** pour décider `RECONSTRUCTIBLE / MANY_POSSIBLE / UNKNOWN / CONTRADICTED`, au lieu d'inventer des caractéristiques non observées.
4. Une évaluation de **nouveaux angles** hors 0°/90°/180°/270° et, plus tard, de vrais changements de perspective — la V4.2 ne démontre ni 360° continu ni identité 3D.
5. Des **échelles scientifiques attachées à mesures et modèles** ; aucun moteur moléculaire, atomique ou quantique opérationnel n'est démontré par les cours Brody. F19 est un contrat spécialisé vérifié à son commit, pas une simulation nano↔macro fonctionnelle.
6. Des essais avec données du monde réel sourcées et la compatibilité capteur/instrument ; **ne pas réutiliser les preuves synthétiques comme observations physiques**.
7. Un adaptateur de mémoire durable **après** audit SENS/B8/B10 : aucun branchement ni « savoir autonome » inventé à l'avance.

## 5. Priorités gelées pour la préparation de la forge Brody

**P0 (ce document)** : conserver les contrats existants, cartographier les représentations/échelles, attribuer les concepts U/C/P, fixer les tests indépendants et les critères de refus. **Pas de lancement de SENS**.

**P1 (prochain code Brody uniquement)** : assembleur *readonly* d'une expérience de balle déjà disponible : `video/frame→observation/repère→trajectoire→prediction→rendu/Reverso→re-perception→delta→candidate experience`. Ne PAS recoder les décodeurs, `TransitionV0`, `WorldStateV0` ou un solver physique.

**P2 (évaluation)** : ablations pixel seul, géométrie seule, temps+mouvement, jointure, avec origines identiques, séquences tenues à l'écart, changement de caméra, occlusion, contradiction et source insuffisante. Exiger preuve de gain *mesuré*, pas supposé. Détails dans [43 — protocole expérimental](43_EXPERIENCE_COMMUNE_BALLE_REPRESENTATIONS_V0.md).

**P3 (extension contrôlée)** : protocole d'échelle `MICRO↔MACRO` lié à une mesure et à un modèle *bornés* (matériau/élasticité/thermo), puis seulement moléculaire/atomique/quantique/cosmique selon preuves d'instruments et contrats applicables. **Aucune loi ou propriété cachée fabriquée à partir des images**.

**P4 (consolidation future)** : comparaison multi-sources, capacités apprises par répétition réellement indépendante, liens de connaissances SENS seulement après certification/promotion autorisée ; aucun mélange gouvernance/trading avec Brody Image.

## 6. Gates documentaires pour la suite

- `GATE_0=NO_NEW_ROOT_ONTOLOGY`
- `GATE_1=SOURCE_KIND_AND_FRAME_EXPLICIT`
- `GATE_2=PREDICTION_PRECOMMITTED_BEFORE_HELDOUT`
- `GATE_3=JOINT_VS_ABLATION_SAME_FRAMES`
- `GATE_4=IDENTITY_NOT_INFERRED_FROM_PIXELS_ALONE`
- `GATE_5=PHYSICAL_UNITS_OR_UNKNOWN`
- `GATE_6=MICRO_MACRO_TRANSITION_REQUIRES_LAW_MEASUREMENT_SCOPE`
- `GATE_7=EXPERIENCE_CANDIDATE_ONLY_MEMORY_WRITE_FALSE`
- `GATE_8=KX108_ONLY_NO_ACT_NO_KERNEL_MUTATION`
- `GATE_9=SENS_B8_CLASS_D_PAUSED`
- `GATE_10=FAILURE_AND_HOLD_RETAINED_IN_HISTORY`

**Décision de clôture de ce document :** le bon prochain chantier est **la première expérience croisée**, pas une « V4.3 dessin seulement », ni sept modèles supplémentaires, ni une refonte de MMonde/SENS. Le document décrit une architecture cible et des critères vérifiables, **ne prétend pas que les ponts existent déjà en runtime**.
