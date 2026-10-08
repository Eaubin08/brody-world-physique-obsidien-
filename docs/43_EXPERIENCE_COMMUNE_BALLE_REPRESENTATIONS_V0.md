# 43 — Préparation de la première expérience commune : un objet en mouvement, plusieurs représentations

**Statut :** PROTOCOLE PRÉ-FORGE / NON IMPLÉMENTÉ en tant que chaîne unique. 2026-10-09.  
**Source de décision :** l'utilisateur demande de reprendre l'écart **spatial ↔ pixel**, les représentations du **mouvement**, les **échelles micro/nano/moléculaire/quantique à cosmique**, puis une suite exécutable **sans reconstruire les organes de l'existant**. [Audit transversal 42](42_AUDIT_TRANSVERSAL_REPRESENTATIONS_MONDE_MULTIECHELLES.md).

## 1. Question, hypothèses et limites

**Question :** sur une même séquence vidéo tenue à l'écart, la jointure d'une représentation visuelle, d'une position spatiale située et d'une histoire temporelle de mouvement permet-elle de **mieux anticiper et reconstruire la frame suivante** qu'une route seule, dans des conditions réplicables ?

L'expérience doit pouvoir conclure **NON**, sans déclencher de « correction » opportuniste du jeu de test. Pas de claim « gravité comprise », « matière comprise », « continuum micro↔macro maîtrisé », « monde physique vérifié ».

**Hypothèses pré-enregistrées (P, à tester) :**
- H1 : aligner les repères objet/caméra améliore les prédictions quand le décor bouge ;
- H2 : une histoire spatio-temporelle de plusieurs expériences améliore certains cas par rapport à mémoire vide ou une expérience ;
- H3 : l'image reconstruite peut préserver une structure spatiale sans avoir une faible erreur pixel stricte, et inversement ;
- H4 : une source invisible, un choc imprévisible, une contradiction de futures identiques ou une hypothèse hors domaine doit donner **HOLD/UNKNOWN** avec preuve, pas une invention ;
- H5 : l'ablation de représentations pertinentes dégrade certaines mesures ; si aucune différence, le rapport le dira.

**Indépendance :** image, position et mouvement dérivés d'une **même vidéo** sont plusieurs *vues corrélées* de la même source, **pas trois preuves physiques indépendantes**.

## 2. Réutilisation précise des briques

| Étape | Code / contrat existant | Branche source propriétaire | Nouvelle écriture autorisée ? |
|---|---|---|---|
| Génération / sources synthétiques | [`generate_transfer_probes_v1.py`](../examples/generate_transfer_probes_v1.py), [33](33_EPISODES_TRANSFER_MONDE_INCONNU_V1.md) | Brody main | Réutiliser fixture et pin source SHA |
| Détection 2D et ancrage caméra | [`world_transfer_probe_v1.py`](../brody_world_physique/world_transfer_probe_v1.py) | Brody main | Appeler, ne pas cloner le détecteur |
| Historique/apprentissage expérientiel | [`experiential_video_v0.py`](../brody_world_physique/experiential_video_v0.py) | Brody main | Même entrées/sorties pour les ablations |
| Projection future | [`WorldStateProjectionV0`](../brody_world_physique/contracts_v0.py) | Brody main | Réemployer type existant |
| Rendu futur / re-perception | [`reverso_future_preview_v1.py`](../examples/reverso_future_preview_v1.py), [`reverso_learning_v0.py`](../brody_world_physique/reverso_learning_v0.py) | Brody main | Route déterministe, pas « générateur appris » |
| Observation/état/reperes/trajectoire | [MMonde](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/mmonde/contracts_v0.py), [F12](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/world_dynamics/contracts_v0.py) | Obsidia upstream, readonly | Pas de root parallèle ni de dépendance souveraine |
| Comparaison et candidat mémoire | [`WorldStateDeltaV0`, `WorldExperienceCandidateV0`](../brody_world_physique/contracts_v0.py) | Brody main | Adapter local non-souverain |
| Image réelle future | [F16](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/vision/contracts_v0.py) | Obsidia upstream, readonly | **INTERDIT** sur source synthétique |
| Références physique réelle futures | [F13 mesure](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/measurement/contracts_v0.py) | Obsidia upstream, readonly | Pas de mesure/force inventée |
| Qualification sémantique future | [OrderedMeaningFlow](https://github.com/Eaubin08/obsidia-x108-proofs/blob/exp/semantic-grammar-cognitive-lattice-v0/docs/semantic/ORDERED_MEANING_FLOW_V0.md) | SENS (pause) | **Aucune exécution** |
| Archives PC | [script d'évidence](../scripts/publish_local_evidence.ps1) | `evidence/brody-local` | Publier seulement PNG/JSON/JSONL de synthèse, jamais code sur la branche d'archive |

La **nouvelle écriture P1**, lorsque validée, doit se limiter à un **assembleur/rejeu** autour de ces briques. Le pipeline déterministe n'exige **aucun nouveau LLM, poids, téléchargement ni serveur** pour les premiers essais.

## 3. Protocole : source commune → vues distinctes → prédiction → retour

```text
SOURCE VIDÉO A (SIMULATED, SHA-256, temps image, conditions caméra)
                   │
       ┌───────────┼───────────────┐
       ↓           ↓               ↓
 PIXELS/FRAME   REPÈRE/XY      TEMPS/TRAJECTOIRE
 (décodage)     (ancrage)       (expériences train)
       └───────────┼───────────────┘
                   ↓
       CANDIDAT ÉTAT MONDE / REFERENCES
     (NE DOIT PAS devenir une mémoire vérité)
                   ↓
   PRÉDICTION t+1 + SOURCE DE LA MÉTHODE
                   ↓
      PRECOMMIT (AVANT frame t+1)
                   ↓
   RECONSTRUCTION VISUELLE (Reverso déterministe)
                   ↓
    RÉVÉLATION frame tenue à l'écart
                   ↓
  MESURES SÉPARÉES pixel / position / mouvement /
               spatial / HOLD
                   ↓
  DELTA + WorldExperienceCandidateV0 + reçus
```

**Dépendance cruciale :** si le banc utilise un *simulated teacher*, le générateur connaît la loi de mouvement mais le **student predictor** ne doit recevoir ni les formules, ni les paramètres cachés, ni la frame à prédire. Le manifest de la vérité cible doit être séparé du précommit et le reçu signé localement par les hashes du code et des sources ; il n'est pas une attestation tierce d'horodatage.

## 4. Ablations : mesurer ce que chaque représentation apporte réellement

Faire tourner **les mêmes séquences / splits / instants / conditions** dans chaque bras. Les braquages de score doivent être interdits (pas de tuning sur test ni de choix d'images favorables après coup).

| Bras | Entrées autorisées | Mesure attendue / limite |
|---|---|---|
| A0 **page / frame précédente** | dernière frame/pixels seulement | Baseline apparence (« ne bouge pas ») |
| A1 **spatial seul** | positions XY déjà extraites, sans image pour prédiction | Baseline de déplacement en repère choisi |
| A2 **temporel / mouvement** | positions + horodatages antérieurs ; sans pixels futurs | Modèle de transition expérientiel de la séquence |
| A3 **visuel + spatial** | dernier masque + position + ancrage antérieur | Rendu déplacé ; pixel/forme ≠ vérité physique |
| A4 **jointure expérimentale** | image + repère + historique temporel + mémoire candidate autorisée | Hypothèse à comparer à A0–A3 **à couverture comparable** |
| A5 **contrôle sans mémoire** | A4 mais `0` expérience | Détermine la contribution réellement mesurée des épisodes |
| A6 **1 / 4 expériences** | A4 avec `1` puis `4` épisodes train indépendants | Vérifier un effet d'accumulation sans fuite |

Interdiction : annoncer que A4 surpasse A2 à partir de metrics différentes ou parce qu'A4 a reçu plus de vérité terrain. Les méthodes peuvent effectuer **HOLD** ; conserver *taux de couverture + score conditionnel* et présenter aussi l'échec sur tous les tests, pas uniquement les prédictions acceptées.

## 5. Batterie de conditions adversariales

- Apparence changée mais mouvement comparable : carré bleu / triangle vert.
- Caméra mobile, ancre indépendante visible : raw camera coordinates contre repère stabilisé.
- Surprise : téléportation/choc non prévisible depuis histoire disponible ; ne pas « deviner » le futur.
- Deux historiques identiques à futurs contradictoires : `HOLD_CONFLICT`.
- Occlusion : aucune position future réelle inventée.
- Dérive ou changement de repère : `HOLD_FRAME_UNKNOWN` si transform non mesurable.
- Une source simulée réutilisée sous 3 projections ne compte toujours qu'une seule preuve **source indépendante**.
- Unité en `px/frame` ne se transforme pas en `m/s` sans calibration réelle.
- « Balle qui tombe » ne permet **pas** de déclarer `g=9.81m/s²`, masse, friction, composition chimique ou cause scientifique.

## 6. Critères et résultats à déposer

Pour chaque essai (TRAIN ou TEST, jamais les deux), conserver au minimum :

- `source_sha256`, `source_kind`, `frame_id`, `observed_at`, `frame_ref`, `unit`, `calibration_ref?`, `object_candidate_ref`, `identity_evidence_kind` ;
- `position`, `velocity_estimate?`, `trajectory_ref?`, `camera_transform_ref?` : UNKNOWN plutôt que remplir au hasard ;
- `model_or_rule_ref`, `code_sha256`, `episode_memory_refs`, `prior_predictions`, `precommit_sha256` ;
- `prediction_ref`, `generated_image_ref`, `teacher_revealed_ref` avec hashes distincts ;
- `pixel_xor`, `pixel_iou`, `object_center_error_px`, `trajectory_error_px?`, `spatial_relation_preserved?`, `coverage`, `HOLD_reason`, `surprise` ;
- `world_transformation_ref`, `world_state_projection_ref`, `world_delta_ref`, `world_experience_candidate_ref` ;
- `uncertainty`, `contradictions`, `source_independence_status`, `causal_proven=false`, `canonical_memory=false`, `decision_authority=KX108_ONLY`.

**Comparaison raster équitable :** publier le pixel score strict ET le pixel score *après réalignement déclaré*. Le réalignement ne doit être appris qu'à partir des **frames déjà vues**, jamais en optimisant sur les pixels de la cible cachée. L'IoU, les erreurs d'objet et la géométrie sont des résultats indépendants — aucune métrique ne remplace une autre.

## 7. Tests bloquants à écrire quand P1 sera lancé

1. **NO_FUTURE_PEEK** : toute lecture de future frame avant le reçu échoue.
2. **REPRESENTATION_ABLATION** : données de test identiques, seule représentation autorisée change.
3. **NO_SOURCE_DOUBLE_COUNTING** : trois projections d'une source ≠ trois sources indépendantes.
4. **MOVING_CAMERA_FRAME** : correction du mouvement caméra avant estimation d'objet dans le repère choisi.
5. **BIDIRECTIONAL_REPLAY** : image prédite → re-perception → delta ; aucune fuite depuis la référence cachée.
6. **PIXEL_VS_SPATIAL_SCORE** : mêmes relations ne rendent pas automatiquement `pixel_xor=0`.
7. **UNKNOWN_SCALE_FRAME** : calibration/repère/échelle manquants restent inconnus ; pas de `m/s` fictif.
8. **CONTRADICTION_HOLD** : scènes indistinguables menant à issues différentes conduisent à HOLD ou uncertainty explicite.
9. **OCCLUSION_HOLD** : conserver le masque absent et la position `UNKNOWN`.
10. **LOSSLESS_PRIOR_RECORDS** : ne modifier aucun fichier V1–V4.2 ni leur SHA ; sorties uniquement dans nouveau dossier.
11. **PHYSICAL_CAUSAL_REFUSAL** : pas de preuve de force, gravité ou matériau inventée depuis seul mouvement apparent.
12. **MEMORY_AND_AUTHORITY_BOUNDARY** : `memory_write_allowed=false`, `auto_promotion=false`, `KX108_ONLY`, `emits_act=false`, `kernel_mutation=false`.
13. **WINDOWS_314_AND_LINUX** : CI reproductible, PNG/JSON/JSONL conservés en artifact ; archive PC seulement sur `evidence/brody-local`.

**Gate sortie P1 :** le graphe des références, les projections, les précommits et le rejeu doivent être vérifiés ; aucune déclaration de gain d'apprentissage avant les résultats comparés P2.

## 8. Première vraie étape multiéchelle P3 (préparation, pas code)

Même objet d'étude **balle + collision / déformation** ; niveaux :

- **Macro observable** : déplacement/déformation image, aire/forme apparente, temps (px et frames).
- **Mécanique calibrée** *si données fournies* : masse/force, vitesse métrique, rigidité, énergie de l'impact, contraintes, unités et incertitudes.
- **Microstructure** *si source dédiée* : géométrie et paramètres d'un matériau, capteur/mesure de microstructure, provenance.
- **Moléculaire / nano** *si source dédiée* : liens/structures/modèles et conditions **qui rendent les hypothèses admissibles**.
- **Atomique / quantique** : nouveaux instruments/modèles/domaines, pas conversion magique depuis les pixels.
- **Cosmique** : **autre régime d'expérience**, avec modèles/repères/échelles propres ; pas un simple étirement des tests de balle.

Premier test négatif indispensable : **deux balles de matériaux microscopiques différents mais visuellement semblables**. Sans autre donnée, Brody doit dire *« la vidéo ne permet pas de choisir entre ces compositions »*. Une mesure indépendante et compatible pourra ensuite réduire l'incertitude ; une simulation *n'est pas* une mesure.

L'opération *macro→micro* peut être `ONE_TO_MANY`. Ne pas présumer une inversion unique et ne pas appeler « loi émergente apprise » la simple application d'une équation codée.

## 9. Reprise pratique sans consommation de crédits sur la forge SENS

- **Étape documentaire P0** : [audit 42](42_AUDIT_TRANSVERSAL_REPRESENTATIONS_MONDE_MULTIECHELLES.md) + présent protocole. Aucun build, aucun test nouveau, aucun push de branches externes.
- **Prochain ticket P1** : implémenter l'adaptateur/routage readonly de cette expérience, au plus près des modules existants, et un manifeste de dépendances/empreintes.
- **P2** : CI / tests PC / archive des images et precommits ; lire les gains et les échecs réellement obtenus.
- **P3** : micro/macro seulement après vérification de l'outillage F13/F18/F19 sur un commit/branche source applicable ; F19 était présent au **commit** `5b9b72452c...`, mais non trouvé sur la branche F16 auditée.
- **SENS** : pause inchangée. B8/T12/Class D et B9/B10 non relancés.

Ce document est un **test plan** ; il ne certifie aucune nouvelle expérience ni ne crée une nouvelle loi physique ou couche mémoire souveraine.
