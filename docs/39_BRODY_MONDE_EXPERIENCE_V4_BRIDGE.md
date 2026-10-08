# 39 — Brody V4 / représentation du monde : les expériences ne restent plus isolées

**Date : 2026-10-09.** **Chantier : Brody World Physique Image.** **Statut : premier pont expérimental intégré, pas une fusion SENS.**

L'utilisateur a demandé de poursuivre les tests de dessin en tenant compte des **véritables contrats MMonde/GPS/F12/F16 et du chantier SENS**, au lieu de fabriquer une deuxième « mémoire des formes » sans lien avec le projet. L'intention forte est : **les expériences prennent sens dans le monde, ses objets, ses relations et leurs transformations**. Il ne faut pourtant pas confondre un état du monde avec une mémoire persistante, ni confondre perception/attribution et connaissance validée.

## 1. Sources retrouvées et propriétaires des contrats

| Propriétaire réel | Type / principe à préserver | Décision pour Brody |
|---|---|---|
| [MMonde — contrats V0](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-mmonde-v0/periphery/mmonde/contracts_v0.py) | `WorldObservationV0`, `WorldStateV0` ; **observation != vérité** ; **world state != mémoire** | Exposer une **vue dérivée** des observations, sans nouveau type racine WorldState |
| [F12 — dynamique située](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-situated-world-dynamics-v0/periphery/world_dynamics/contracts_v0.py) | `TimeEnvelopeV0`, `SpatialFrameRefV0`, `TypedRelationV0`, `TransitionV0`, `TrajectoryV0`, distinction temporel/corrélé/dérivé/causal | Ne déduire ni causalité ni continuité physique d'un simple rejeu du dessin |
| [F16 — vision réelle](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/vision/contracts_v0.py) | `RealImageObservationV0` rejette les images générées ; `VisualPrimitiveV0` prévoit géométrie/masque/profondeur/mouvement/features | Les PNG du cours sont `SIMULATED` ou `GENERATED`, **jamais** des observations d'image réelle F16 ; utiliser des signatures dérivées |
| [SENS — OccurrenceClaim, branche expérimentale](https://github.com/Eaubin08/obsidia-x108-proofs/blob/exp/semantic-grammar-cognitive-lattice-v0/app/semantic/lattice/occurrence_derivation.py) | Claim sémantique != réalisation vérifiée, et `NO_ASSERTION` != `UNRESOLVED` | Ne fabriquer aucune occurrence SENS factice ni certifier le sens « maison » depuis un dessin |
| [GPS Trusted-State Ledger](https://github.com/Eaubin08/obsidia-gps-defense-/blob/native-builder-trusted-navigation-v1/server/navigation/trusted-state-ledger.mjs) | Continuité, état et nouvelles preuves situées ; ne pas écraser une histoire cohérente par une source contradictoire | Conserver liens de preuve, contradictions et incertitudes par épisode ; pas de transfert de la logique GNSS au dessin |
| [Brody — contrats F0 existants](../brody_world_physique/contracts_v0.py) | `WorldTransformationV0`, `WorldStateDeltaV0`, `WorldExperienceCandidateV0` déjà présents | **Réutilisés** comme dataclasses existantes, pas re-définis |

### Situation SENS / PRE-FORGE

Le checkpoint communiqué par l'utilisateur indique **B8, jalon 30/53**, amendement T12 local `09d4fe74` **pas encore certifié** ; Class D puis B9/ARM/B10 à venir. Ceci est une **information de pilotage fournie par l'utilisateur**, non une certification tirée du dépôt distant. Aucune branche SENS n'a été poussée, fusionnée, modifiée ou utilisée pour exécuter du code ici. Brody Image peut avancer sans promouvoir une leçon visuelle comme un savoir canonique B8/B10.

## 2. Implémentation : une vue du monde issue de V3 réellement vérifié

Module [`world_experience_bridge_v4.py`](../brody_world_physique/world_experience_bridge_v4.py).

Le module **vérifie intégralement les trois examens V3 enregistrés** avant de produire une représentation :

1. Observation synthétique de l'image de référence **du professeur**, sourcée et horodatée par un **rang de séquence synthétique, pas une horloge**.
2. Observation de la sortie **générée par l'élève**, dans le même repère 64×64, avec nombre de pixels et géométrie du trait.
3. Pour chaque épisode, un **`WorldTransformationV0`** référencé avec instrument, nombre de gestes, provenance et statut `SIMULATED`.
4. Un **`WorldStateDeltaV0`** portant l'erreur pixel-à-pixel et les limites épistémiques ; ce n'est ni une loi de la physique ni une cause démontrée.
5. Un **`WorldExperienceCandidateV0`** du dépôt Brody existant, avec `state_before_ref`, `state_after_ref`, `transformation_ref`, `delta_ref`, preuves et liens de rejeu. Les champs `validation_status=CANDIDATE`, `memory_eligibility=CANDIDATE_ONLY`, `memory_write_allowed=False` et `auto_promotion_allowed=False` restent obligatoires.
6. Une **vue de graphe candidate**, avec entités, observations, relations et liens de procédure, reprenant la forme des champs MMonde **sans** importer/doubler sa classe racine.

Les vues sont reconstruisibles à partir des preuves V3 ; le fichier JSON V4 est contrôlé par un calcul indépendant depuis ces preuves.

## 3. Distinctions nécessaires pour ne pas fabriquer de fausse compréhension

**Les deux pentagones (immédiat/différé)** peuvent appartenir au même *groupe de référence* seulement parce que le SHA-256 de l'image modèle est **strictement identique**. Ce n'est **pas** un suivi autonome de l'identité d'un objet physique. La continuité reste `CANDIDATE_SAME_REFERENCE_ACROSS_TRIALS` avec `physical_identity_proven=False`.

**La maison (composée)** contient une relation `ABOVE_WITH_HORIZONTAL_OVERLAP` entre « toit » et « base ». Le pont V4 la calcule sur les **boîtes de placement que le professeur a déjà imposées en V3**, et garde explicitement `DERIVED_FROM_TEACHER_PLACEMENT`. Ce n'est **PAS** une relation découverte par vision autonome. Elle est une hypothèse de structure utile pour le futur cours, pas encore une connaissance « une maison possède un toit ».

**Le sens des objets** reste inconnu : `semantic_label_predicted=null`, `sens_pipeline_executed=False`, `occurrence_claim_generated=False`. Les données sont synthétiques et générées ; aucune instance `RealImageObservationV0` n'est construite.

**La mémoire est liée au monde, mais reste distincte** : une `WorldExperienceCandidateV0` pointe vers des états de référence, transformations et preuves. Elle **n'est pas** la vérité du monde ni l'index Native Memory, et aucun flux d'écriture/promotion n'est ouvert.

## 4. Commandes sur ton PC Windows

La V3 réussie sur ton PC peut être réutilisée directement **en lecture seule** :

```powershell
git pull --ff-only origin main

$v3 = "build\dessin-memoire-v3-20261009-000320"
$out = "build\monde-brody-v4-$(Get-Date -Format yyyyMMdd-HHmmss).json"

py -m brody_world_physique.world_experience_bridge_v4 --v3 $v3 --out $out
if ($LASTEXITCODE -ne 0) { throw "V4 : reconstruction du monde impossible" }

py -m brody_world_physique.world_experience_bridge_v4 --v3 $v3 --verify $out
if ($LASTEXITCODE -ne 0) { throw "V4 : preuves et monde incohérents" }

notepad $out
```

Un dossier V3 construit sous une autre version de code peut être refusé par ses contrats de SHA ; ne pas le modifier à la main. Relancer alors les étapes de référence dans de **nouveaux dossiers**.

## 5. Prochain test réellement nouveau : plus de monde, moins de recettes imposées

Cette V4 est une **réconciliation exécutable** des couches, pas encore un moteur d'apprentissage sémantique.

La suite expérimentale doit tester sous double aveugle :
- **Vision F16-type** : identifier des parties sur **plusieurs images inconnues**, sans recevoir les boîtes professorales au moment de proposer les relations ;
- **MMonde** : suivre l'identité d'une entité candidate à travers translation, rotation, occlusion et contradiction, avec des hypothèses concurrentes ;
- **SENS** : conserver les statuts `proposé`, `déduit`, `attribué`, `observé` sans les convertir en vérité ni en réalisation sémantique ;
- **Mémoire expérientielle** : revoir ce qui a été appris, à quel prix, par quelle procédure, sous quelles conditions ; les répétitions exactes ne deviennent pas de nouvelles preuves indépendantes ;
- **Reverso et dessin** : reconstruire un objet à partir de parties et relations, mesurer les écarts face à une nouvelle source révélée seulement après le rendu.

B8, B9 et B10 restent propriétaires de la promotion/qualification de connaissances et de la mémoire durable lorsqu'ils seront effectivement validés et raccordés. Le projet Brody n'invente aucune autorité alternative.
