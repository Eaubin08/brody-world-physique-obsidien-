# 22 — CARTE DE BRANCHEMENT : TES BRANCHES, NOS CONTRATS, LES MOTEURS OPEN SOURCE

> **Mise à jour I1 (2026-10-08) :** l'utilisateur confirme que Qwen-VL fonctionne déjà avec Jarvis sur le PC fixe. Un [client local compatible Jarvis](../brody_world_physique/jarvis_vision_v0.py) est maintenant codé dans ce dépôt et testé par **service simulé**. La description JSON reste une candidate non vérifiée. **Connexion physique PC, admission F16, passage Binder/Brody et mémoire non testés/non raccordés.** Voir [26 — Qwen-VL existant](26_BRODY_IMAGE_I1_JARVIS_QWEN_VL_ADAPTER.md). Aucun poids téléchargé.\n\n**Audit : 2026-10-08.** Vérification par lecture de fichiers des branches indiquées, et liens de donneurs externes officiels. **Présence dans GitHub ≠ déploiement PC ≠ moteur raccordé ≠ capacité évaluée.** Aucun composant tiers téléchargé durant cette passe.

## 1. Dépôts et branches retenus pour **Brody Image**

| Dépôt / branche lue | SHA audité | Ce qui nous intéresse | État |
|---|---|---|---|
| [obsidia-x108-proofs](https://github.com/Eaubin08/obsidia-x108-proofs/tree/5b9b72452cff7a560db992e57a43fc700dacd923) `feat/r6-sens-cognition-canonical-audit-v0` | `5b9b72452cff7a560db992e57a43fc700dacd923` | MMonde, F12, F16 image réelle, multimodal, mémoire, OS Trad/IR/Reverse, Brody | **CONTRATS/CODE SOURCE PRÉSENTS** — pas de générateur image intégré prouvé |
| [Jarvis-iron-obsidia-](https://github.com/Eaubin08/Jarvis-iron-obsidia-/tree/8fad2f434e458f8f3aa5fb7b49240c253e7d843d) `fix/qwen-live-main-20261007` | `8fad2f434e458f8f3aa5fb7b49240c253e7d843d` | CameraRig, OpenCV capture, écran, `LocalVisionCognition` | **INGRESS STRUCTUREL PRÉSENT** — réponse Brody avec images non prouvée |
| [monde-obsidia](https://github.com/Eaubin08/monde-obsidia/tree/8aaec21138772803a22cf69f08d7a5d8dc4fcf37) `feat/native-operations-world-projection-v0` | `8aaec21138772803a22cf69f08d7a5d8dc4fcf37` | UI / écran d'opération, Brody API sur 8000, sessions | **VISUALISATION / LANCEMENT**, pas moteur d'image |
| [obsidia-gps-defense-](https://github.com/Eaubin08/obsidia-gps-defense-/tree/d1221fce6914274f7b0c445a829739367b0c6abb) `feat/c41-gps-kernel-response-and-claim-boundary-v0` | `d1221fce6914274f7b0c445a829739367b0c6abb` | provenance physique, gate de réalité, claims | **DOMAINE ADJACENT**, ne pas contaminer par résultats générés |
| [agi-vison](https://github.com/Eaubin08/agi-vison/tree/34849650a81c72bd63459f37872b1fa5dd7a0a1a) `main` | `34849650a81c72bd63459f37872b1fa5dd7a0a1a` | idées générales AGI / gouvernance | **ARCHIVE CONCEPTUELLE**, non-base technique vision |
| [ce dépôt](https://github.com/Eaubin08/brody-world-physique-obsidien-/tree/f0/document-source-reconciliation-20261008) `f0/document-source-reconciliation-20261008` | branche documentaire | boucle transformation / projection / delta / expérience F0 + plan image | **FONDATION LOCALE**, générateur/œil/bridge image pas encore réalisés |

**Cas spécial SENS :** `obsidia-x108-proofs/exp/semantic-grammar-cognitive-lattice-v0` au commit [`85d55e3538f1`](https://github.com/Eaubin08/obsidia-x108-proofs/tree/85d55e3538f1b049f2f9eb7f12892928187d3de4/app/semantic/lattice). Branche expérimentale sans ancêtre commun avec la lignée runtime inspectée ; `EventRef` est une identité locale à la frame, `OccurrenceClaim` une proposition linguistique, pas preuve physique. **RESEARCH / PAS DE MERGE AS-IS**.

## 2. Branchements précis **dans tes dépôts**

| Entrée/sortie Brody Image | Déjà présent — chemin source et branche fixe | Branchement image à réaliser | Statut |
|---|---|---|---|
| **Caméra / écran** | [`camera_rig.py`](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/8fad2f434e458f8f3aa5fb7b49240c253e7d843d/src/jarvis/camera_rig.py), [`opencv_camera.py`](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/8fad2f434e458f8f3aa5fb7b49240c253e7d843d/src/jarvis/integrations/opencv_camera.py) et [F11 caméra](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/8fad2f434e458f8f3aa5fb7b49240c253e7d843d/docs/F11_CAMERA_PHYSICAL.md) | CameraFrame/ScreenCapture → asset/hash/time/source + provenance F16, en lecture seule | **SOURCE PRÉSENT / ADAPTATEUR BRODY IMAGE À FAIRE** |
| **Œil Qwen-VL local (facultatif)** | [`local_vision_cognition.py`](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/8fad2f434e458f8f3aa5fb7b49240c253e7d843d/src/jarvis/integrations/local_vision_cognition.py), [route locale](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/8fad2f434e458f8f3aa5fb7b49240c253e7d843d/docs/LOCAL_VISION_ROUTE_V0.md) | Reprendre l'endpoint configuré de Jarvis comme fournisseur `VisionDescriptionCandidate`, **pas** moteur de connaissance finale | **ADAPTER SOURCE PRÉSENT / INSTALL ET CAUSALITÉ NON PROUVÉS** |
| **Transport multimodal** | [`ModalityObservationV0`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/multimodal/bridge_v0.py) | adapter sortie vision (features/masks/source) → modality candidate → MMonde | **CONTRAT PRÉSENT / TEST TRANSVERSE À FAIRE** |
| **Image réelle F16** | [`RealImageObservationV0`, `VisualPrimitiveV0`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/vision/contracts_v0.py) | mapper bbox/masque/depth/motion + interprétation candidates sans créer `VisualIR` souverain | **CONTRAT PRÉSENT / EXTRACTEURS DONNEURS À CONNECTER** |
| **État du monde** | [`WorldObservationV0`, `WorldStateV0`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/mmonde/contracts_v0.py) | relier images et objets situés (identité **candidate**, pas inventée) | **CONTRAT PRÉSENT** |
| **Temps, repères, mouvement** | [F12 `TransitionV0 / TrajectoryV0`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/world_dynamics/contracts_v0.py) | observations multi-images → transformation descriptive F0 + tracking | **CONTRAT PRÉSENT / ALGORITHME VISION FUTUR** |
| **Comparer hypothèses et perception** | [`WorldStateDeltaV0` local](../brody_world_physique/contracts_v0.py) ; [sources F0](02_CONTRACTS.md) | `VisualInvariantV0`, `VisualFingerprintV0`, comparaison `LOCK/FLEX/IGNORE` | **BOUCLE MONDE F0 PRÉSENTE / INVARIANTS IMAGE PLANNED** |
| **Brody raisonneur/routeur** | [Brody pipeline](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_real_response_pipeline.py) ; [API locale et service Brody de Monde](https://github.com/Eaubin08/monde-obsidia/blob/8aaec21138772803a22cf69f08d7a5d8dc4fcf37/server/brody-service.mjs) | adapter image→Brody contextualisé et sortie `GenerationIntentV0` typed | **BRODY PRÉSENT / VISUAL INTENT SEAM NON PROUVÉ** |
| **Entrée OS Trad / IR / Reverse** | [routes OS Trad/IR/Reverse](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/routes/os_trad_ir_reverse.py), [bridge Reverse text](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_existing_reverse_os_bridge.py) | **nouveau** Visual Reverse projection → `GeneratorAdapter`. Ne pas présenter la route textuelle comme moteur image | **SURFACES READONLY PRÉSENTES / BRIDGE IMAGE ABSENT** |
| **Génération d'image** | **aucun `GeneratorAdapter` Brody Image implémenté dans le nouveau repo** | adapter vers sd.cpp ou ComfyUI, prompt/conditionnement, modèle/seed/hash/workflow, résultat `GeneratedArtifactV0` | **À CONSTRUIRE** |
| **Évaluation inverse** | F16 + F12 + F0 Delta existent en parties | re-perception des *artéfacts générés* comme `GENERATED`, sans utiliser `RealImageObservationV0` ; `ReverseEvaluationV0` | **À CONSTRUIRE** |
| **Mémoire candidate** | [`MemoryCandidate`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/memory/memory_candidate.py) ; [Native Memory Brody](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_obsidia_native_memory.py) | épisode évalué → candidate revue ; `MemorySourceType` world experience manque dans le snapshot audité | **LIFECYCLE PRÉSENT / BRIDGE IMAGE MANQUANT** |
| **Vue utilisateur** | [Monde Obsidia](https://github.com/Eaubin08/monde-obsidia/blob/8aaec21138772803a22cf69f08d7a5d8dc4fcf37/README.md) | écran visualisant source image, masque, état, génération, deltas et learning candidates | **UI EXISTE / ÉCRAN IMAGE SPÉCIFIQUE FUTUR** |
| **GPS physique** | [claims GPS](https://github.com/Eaubin08/obsidia-gps-defense-/blob/d1221fce6914274f7b0c445a829739367b0c6abb/docs/CLAIM_MATRIX.md) | lecture future d'observations typées ; ne jamais injecter les images générées comme evidence/authenticité GPS | **UTILISATION FUTURE / AUCUNE FUSION** |

### Constats importants de l'audit Jarvis

- [F11 CAMERA](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/8fad2f434e458f8f3aa5fb7b49240c253e7d843d/docs/F11_CAMERA_PHYSICAL.md) signale captures locales et un mapping cible caméras 0 et 1 validé **dans ce rapport historique**. Cela ne prouve pas qu'elles sont allumées maintenant.
- [`LIVE_MULTIMODAL_CONTEXT_V0.md`](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/8fad2f434e458f8f3aa5fb7b49240c253e7d843d/docs/LIVE_MULTIMODAL_CONTEXT_V0.md) dit explicitement **contexte caméra/écran assemblé = IMPLEMENTED**, mais **causalité du contexte dans la réponse Brody = NOT YET PROVEN**. L'API Brody n'a pas encore de champ canonique d'injection du packet live dans le bridge Jarvis.
- Le fournisseur Jarvis [`LocalVisionCognition`](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/8fad2f434e458f8f3aa5fb7b49240c253e7d843d/src/jarvis/integrations/local_vision_cognition.py) vise une URL locale configurable (`JARJAR_VISION_URL`) et un label Qwen-VL (`JARJAR_VISION_MODEL`). Ce n'est **ni un modèle installé garanti**, ni une deuxième autorité cognitive, ni une instruction d'installer un autre LLM.
- L'API Obsidia OS Trad / Reverse est **textuelle/read-only** à cette version : ne pas attribuer à `/api/os-reverse/project` une génération d'images qu'elle n'effectue pas.

## 3. Moteurs open source déjà sélectionnés — **qui produit quoi et où brancher**

L'ensemble était déjà inventorié dans [docs/04_EXTERNAL_COMPONENTS.md](04_EXTERNAL_COMPONENTS.md). Cette passe ne remplace pas les candidats par de nouveaux modèles au hasard : elle les range selon les véritables raccords.

| Fournisseur / lien officiel | Capacité | Point de raccord | Choix actuel |
|---|---|---|---|
| [MiniCPM-V](https://github.com/OpenBMB/MiniCPM-V) | description visuelle image/vidéo candidate | `VisionDescriptionAdapter -> VisualPrimitive/CandidateInterpretation` | **OPTION**, ne pas doubler Qwen local déjà calibré sans benchmark |
| [MobileSAM](https://github.com/ChaoningZhang/MobileSAM) | masques image | `SegmentationAdapter -> VisualPrimitive.mask_ref` | **CANDIDAT I1** |
| [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO) | localiser objet à partir de concepts | `GroundingAdapter -> bbox candidate -> segmentation` | **CANDIDAT I1/I3** |
| [EfficientTAM](https://github.com/yformer/EfficientTAM) | suivi masque/ID au fil de vidéo | `TrackingAdapter -> F12 Trajectory / visual continuity` | **CANDIDAT I3** ; code et checkpoints Apache-2.0 déclarés amont |
| [Depth Anything 3](https://github.com/ByteDance-Seed/Depth-Anything-3) | profondeur / structure de scène | `DepthAdapter -> VisualPrimitive.depth_ref / SpatialFrame` | **CANDIDAT I1** : choisir modèle précis, les grands poids sont **CC BY-NC 4.0**, BASE/SMALL annoncés **Apache-2.0** ; attention aux droits, tailles et VRAM |
| [EB-JEPA](https://github.com/facebookresearch/eb_jepa) | prédiction de représentation et action-conditioned world modeling | `TransitionPredictor -> WorldStateProjectionV0` | **LAB I4** (ce n'est pas générateur pixel) |
| [TD-MPC2](https://github.com/nicklashansen/tdmpc2) | modèle dynamique/contrôle compact | `TransitionPredictorBenchmark` | **LAB I4**, pas moteur image à brancher directement |
| [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp) | runtime local diffusion/image | `GeneratorAdapter -> GeneratedArtifact` | **PREMIER CANDIDAT G1** après inventaire machine, code MIT selon amont |
| [Z-Image](https://github.com/Tongyi-MAI/Z-Image) | poids/modèle de génération et variantes édition | *à l'intérieur du runtime diffuseur* | **CANDIDAT G1/G2** ; **6B paramètres**, ne pas promettre « léger » sur PC inconnu ; licences exactes poids à figer |
| [SANA](https://github.com/NVlabs/Sana) | autre moteur/architecture image | `GeneratorAdapter` alternatif | **BENCH / OPTION**, non requis en premier |
| [ComfyUI](https://github.com/Comfy-Org/ComfyUI) | orchestration visuelle de workflows génératifs | `WorkflowGeneratorAdapter` | **OUTIL DE LABO**, pas cognition centrale ; code **GPL-3.0**, implications à examiner |
| [WorldFM](https://github.com/inspatio/worldfm) | images de vues caméra cibles | `Reverse360Adapter` | **LAB I6** : code Apache-2.0 selon amont, sous-modules HunyuanWorld/MoGe/Real-ESRGAN/ZIM sous **licences séparées** |
| [DreamerV3](https://github.com/danijar/dreamerv3) | imagination/replay dans world model | `SimulationReference` | **RÉFÉRENCE APRÈS I4**, pas composant de génération photo |
| [LeRobot / SmolVLA](https://github.com/huggingface/lerobot) | mouvement/contrôle incarné | compétence future | **LATER / REFERENCE**, robotique non préalable au moteur image |
| [InSpatio World](https://github.com/inspatio/inspatio-world) | monde persistant et rendu spatial | labo spatial futur | **PLUS TARD**, dépendances/poids à auditer séparément |

**Nouvelle observation fournisseur vérifiée :** le [README officiel Depth Anything 3](https://github.com/ByteDance-Seed/Depth-Anything-3) distingue explicitement licences des poids selon tailles ; ne pas adopter `DA3-LARGE/GIANT` comme modèle commercial par simple analogie avec la licence Apache du dépôt. Le [README officiel WorldFM](https://github.com/inspatio/worldfm) fait la même distinction de dépendances. stable-diffusion.cpp annonce plusieurs familles dont Z-Image mais le **runtime MIT ne transfère pas ses droits au modèle**, ni ne garantit la VRAM.

### Carte de branchement logique

```text
JARVIS caméra / écran ─────┐   fichier image test / vidéo ─┐
                           └──────────────┬────────────────┘
                                          v
        EXTERNAL VISION ORGANS: Qwen-VL / MobileSAM / GroundingDINO /
                 EfficientTAM / DA3 (activer seulement le nécessaire)
                                          |
                                          v
      EXISTING OBSIDIA F16 RealImageObservation + ModalityObservation
                                          |
                         MMonde + F12 + Evidence refs
                                          |
                                BRODY (propositions)
                                 /             \
                 invariant/expérience           GenerationIntent
                       candidate                       |
                                             GENERATOR ADAPTER
                                       (sd.cpp / ComfyUI, poids)
                                                      |
                                              GeneratedArtifact
                                                      |
                                      reverse perception & evaluation
                                                      |
                                            candidate delta/skill
                                                      |
                                        Native Memory (candidate)
```

Ne pas utiliser la source image **générée** comme entrée de `RealImageObservationV0`. Elle peut être *analysée*, mais toujours comme artefact généré avec ses provenance/labels.

## 4. Décisions techniques et points d'arrêt

**À réutiliser :** MMonde / F16 / F12 / F0 Learning contracts / OS Trad-IR / Brody / Native Memory / Jarvis CameraRig / UI Monde.  
**À coder ici :** adaptation perception image, invariants, fingerprint expérimental, `GenerationIntent`, adapter diffusion, `GeneratedArtifact`, re-perception générée, scoring comparatif, image-to-experience candidate.  
**À ne PAS reconstruire :** WorldState racine, Temporal/Transition racine, canon memory, authentification physique GPS, kernel.  
**À ne PAS installer par défaut :** un autre LLM général alors que Brody est le raisonneur interne et la voie locale Qwen est la solution visuelle candidate à vérifier.

**Reste à vérifier sur PC :** GPU/VRAM/RAM/OS, endpoints réellement disponibles, compatibilité stable-diffusion.cpp et checkpoint retenu, coût des deux moteurs de perception, source/poids/licences, latence, quotas éventuels. **Aucun lancement automatique avant une sélection explicite.**

## 5. État de preuve final

```text
OWN_REPO_SOURCE_READ           YES
OWN_IMAGE/WORLD_CONTRACTS      YES (F16, MMonde, F12)
JARVIS_CAMERA_VISION_SEAMS     YES (source)
BRODY_IMAGE_INGRESS_CAUSAL     NOT_PROVEN
BRODY_IMAGE_GENERATOR_ADAPTER  NOT_IMPLEMENTED
CLOSED_IMAGE_GENERATION_LOOP   NOT_PROVEN
EXTERNAL_MODELS_INSTALLED      NOT_VERIFIED
LICENSES_FROZEN_PER_WEIGHT     NO
KX108_AUTHORITY_CHANGED        NO
```

La véritable fermeture F0 pour ce chantier exige donc **une carte de flux image testable**, pas une quatrième passe encyclopédique des 108 concepts. [Plan image prioritaire](21_BRODY_IMAGE_MASTER_PLAN.md).
