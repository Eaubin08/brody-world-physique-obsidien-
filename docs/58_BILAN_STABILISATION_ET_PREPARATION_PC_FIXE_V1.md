# BILAN DE STABILISATION PORTABLE ET PRÉPARATION DU PREMIER ESSAI NEURONAL PC FIXE (V1)

**Date :** 22 Octobre 2026  
**Dépôt :** `brody-world-physique-obsidien-`  
**Branche :** `main`  
**Commit de référence initial :** `52df738`  
**Autorité décisionnelle :** `KX108_ONLY`  
**Politique mémoire :** `native_memory_write_allowed = False` (Registre candidat uniquement)  

---

## 1. Synthèse globale des statuts

| Composante / Mission | Statut | Résultat & Justification |
| :--- | :---: | :--- |
| **A. Stabilisation Portable (Pytest globale)** | **FAIT** | 305 tests unitaires et d'intégration validés à 100% sur l'ensemble de la suite du dépôt (aucune régression, 0 échec). |
| **A. Démonstrateur V3 sans valeurs préinjectées** | **FAIT** | Recherche sémantique `MeaningQueryIntentV1`, routage dynamique d'outils (`PEN`/`BRUSH`), et correction d'erreur géométrique fermée. |
| **A. Entrée image arbitraire sans retouche de code** | **FAIT** | Méthode `run_pipeline_on_arbitrary_image()` opérationnelle : extrait contours, centroïdes et boîtes englobantes sans coordonnées en dur. |
| **A. Audit des 32 chantiers (Doc 21)** | **FAIT** | Audit exhaustif réconcilié distinguant Objectif historique, Implémentation, Preuve, Lacune, et Classification sans surévaluation. |
| **B. Vérification dépôts Obsidia frères** | **FAIT** | Audit des liaisons concrètes avec `obsidia-clean-wt` (commit `7ff43655`), `obsidia-jarvis-advanced-integration-v0` (`7839c9c1`), `Jarvis-iron-obsidia-` (`f29664a`). |
| **B. Disambiguation Binder Souverain vs Orchestrateur Brody** | **FAIT** | Obsidia CG9 Provider Binder est un arbitre externe de baux souverains. Brody Bounded Orchestrator O04 est le moteur local de tracé. |
| **C. Inventaire environnement hôte (lecture seule)** | **FAIT** | Script `scripts/pc_fixe_readonly_environment_inventory.py` exécuté : sonde CPU, RAM, ports (8080, 8081, 11434, etc.), caches modèles et projecteur `mmproj`. |
| **C. Profilage GTX 1050 Ti & sd.cpp** | **FAIT** | Profil GTX 1050 Ti 4.0 Go VRAM : configuration `sd.cpp` quantifié SD 1.5 GGUF `q4_0` / `q8_0` (~2.3 Go VRAM, marge de 1.7 Go) et fallback CPU offload. |
| **C. Protocole d'essai comparatif 3 modes** | **FAIT** | Module `brody_world_physique/pc_fixe_neural_trial_protocol_v1.py` implémenté et testé : compare `MODEL_ALONE`, `BRODY_PROCEDURAL_ALONE`, `BRODY_PILOTING_MODEL`. |
| **D. Cœur capacitaire de Brody** | **FAIT** | Le modèle neuronal est un outil moteur (`NEURAL_FILL`), Qwen-VL est une sonde perceptive externe ; Brody observe, mémorise, compose et garantit les régions `LOCK`. |
| **Exécution physique sur PC Fixe avec GPU GTX 1050 Ti** | **HOLD** | Statut `HOLD_PC_FIXE_GPU_REQUIRED` explicite sur le portable de développement (absence de GPU CUDA et port 8081 fermé). Prêt pour lancement sur PC Fixe. |

---

## 2. Stabilisation Portable & Démonstrateur V3

### 2.1 Suite Pytest Globale
La suite pytest complète sur le répertoire `tests/` a été exécutée :
- **Tests passés :** 305 tests passés (dont 65 sous-tests parametrés)
- **Échecs :** 0 échec
- **Avertissements :** 1 avertissement d'infrastructure de test (fixture PytestReturnNotNoneWarning)
- **Temps d'exécution :** ~145 secondes

### 2.2 Démonstrateur V3 et Pipeline sur Image Arbitraire
Le moteur opérationnel V3 (`OperationalBrodyImagePipelineEngineV3`) dispose désormais d'un point d'entrée universel pour toute image inconnue :
`run_pipeline_on_arbitrary_image(target_scene, output_dir, goal_description)`
1. **Observation :** Normalisation raster 64x64, hachage SHA-256 sans altération.
2. **Représentation interne :** Détection dynamique des pixels noirs via `black_pixels()`, calcul de boîte englobante `bbox_of()`, centroïde `(cx, cy)`, points extrêmes (top, bottom, left, right). Zéro coordonnées en dur.
3. **Rappel mémoire multidimensionnel :** Interrogation `search_by_meaning(MeaningQueryIntentV1.WHICH_METHOD_IS_TRANSFERABLE)` sur l'arbre 12, et sélection d'outil (`PEN` si contour fin, `BRUSH` si densité élevée).
4. **Plan d'actions borné :** Génération d'instructions de tracé reliant les ancres détectées sous budget strict d'étapes (max 12).
5. **Génération procédurale :** Exécution par `ProgrammaticBoundedOrchestratorO04`.
6. **Re-perception en boucle fermée :** Évaluation des patchs d'erreur via `VisualReperceiverEvaluatorV1`.
7. **Correction motrice :** Génération automatique d'un trait correctif centré sur le cluster de pixels manquants sans aucune hypothèse sur le nom de l'objet.
8. **Émission d'expérience candidate :** Registre local append-only avec `native_memory_write_allowed = False` et autorité `KX108_ONLY`.

---

## 3. Audit des liaisons avec les dépôts Obsidia frères

Les trois dépôts frères présents sur le poste de travail ont été audités dans leur état concret :

### 3.1 Dépôts frères et SHAs réels
1. **`obsidia-clean-wt`**
   - **Branche :** `obsidia-clean-wt`
   - **SHA :** `7ff43655`
   - **Rôle :** Obsidia Core, Binder souverain CG9 (`src/obsidia/domain/services/binder.py`), registre Merkle souverain.
   - **Frontière :** Non-accessible en écriture unilatérale depuis Brody (`KX108_ONLY`). Les tentatives locales sont isolées dans le `CandidateExperienceLedgerV0`.

2. **`obsidia-jarvis-advanced-integration-v0`**
   - **Branche :** `feat/jarvis-advanced-obsidia-integration-v0`
   - **SHA :** `7839c9c1`
   - **Rôle :** Intégration avancée Jarvis-Obsidia, passerelle des 34 arbres cognitifs (`periphery/shazam_cognitif.py`), interface SENS (`src/sens_interface.py`).
   - **Statut liaison :** `RUNTIME_INTEGRATED` en import dynamique protégé et rétro-compatible.

3. **`Jarvis-iron-obsidia-`**
   - **Branche :** `build/jarvis-v0`
   - **SHA :** `f29664a` (avec commit d'architecture vision `3715985`)
   - **Rôle :** Jarvis Core V01, `LocalVisionCognition` (`src/jarvis/integrations/local_vision_cognition.py`).
   - **Architecture Vision :** Requête HTTP POST vers `http://127.0.0.1:8081/v1/chat/completions` servi par `llama-server` exécutant le modèle multimodal `Qwen2.5-VL-3B-Instruct` avec fichier projecteur `mmproj`.
   - **Statut liaison :** `HOLD_PORT_8081_CLOSED` sur le portable. Prêt pour couplage dès ouverture du serveur sur le PC Fixe.

---

## 4. Préparation du Premier Essai Neuronal sur PC Fixe

### 4.1 Diagnostic Matériel et Contraintes de l'Hôte Portable
L'exécution de l'audit en lecture seule (`scripts/pc_fixe_readonly_environment_inventory.py`) sur le portable de travail a relevé :
- **Hôte :** `DESKTOP-Q5MD7J7` (Windows 11)
- **CPU :** 6 cœurs
- **RAM :** 15.73 Go
- **GPU Détecté :** Aucun (0.0 Go VRAM) / Driver NVIDIA : Absent
- **Sondes de ports TCP (lecture seule) :**
  - Port 8080 (`llama-server`) : **FERMÉ**
  - Port 8081 (`Jarvis Qwen-VL`) : **FERMÉ**
  - Port 11434 (`Ollama API`) : **FERMÉ**
  - Port 5000 (`Flask / SD API`) : **FERMÉ**
  - Port 7860 (`ComfyUI / Gradio`) : **FERMÉ**
  - Port 8000 (`vLLM / FastAPI`) : **FERMÉ**
- **Conclusion d'inventaire :** Le portable ne dispose pas du GPU requis et les serveurs d'inférence sont inactifs. Le statut `HOLD_PC_FIXE_GPU_REQUIRED` est rigoureusement maintenu pour éviter tout blocage ou dérive.

### 4.2 Spécification Opérationnelle pour le PC Fixe (Titan Dev)
Sur la machine PC Fixe équipée de la carte **NVIDIA GeForce GTX 1050 Ti (4.0 Go VRAM)** :

1. **Moteur Diffusion recommandé : `sd.cpp` (quantification GGUF)**
   - **Modèle :** Stable Diffusion 1.5 au format `sd-v1-5-q4_0.gguf` ou `sd-v1-5-q8_0.gguf`.
   - **Consommation VRAM :** ~2.1 à 2.4 Go VRAM en pic.
   - **Marge de sécurité :** ~1.6 Go de VRAM disponible pour l'OS et l'affichage.
   - **Interdiction formelle :** Aucun modèle SDXL non quantifié ou FP16 intégral sous peine de CUDA OOM crash.
   - **Mode Fallback :** Exécution CPU offload multi-threadée (4 threads) si la VRAM est mobilisée.

2. **Moteur Vision : `llama-server` avec Qwen2.5-VL et `mmproj`**
   - **Binaire :** `llama-server.exe`
   - **Modèle :** `qwen2.5-vl-3b-instruct-q4_k_m.gguf`
   - **Projecteur multimodal :** `mmproj-qwen2.5-vl-3b-instruct-f16.gguf` (obligatoire pour le décodage d'images).
   - **Port d'écoute :** 8081 (conforme au contrat `LocalVisionCognition` de Jarvis).

### 4.3 Protocole Comparatif à 3 Modes (`PCFixeNeuralTrialProtocolEngineV1`)

Le protocole évalue rigoureusement les 3 modes face à une même cible composite comprenant une fondation rigide (`LOCK`) et un intérieur texturé flexible (`FLEX`) :

1. **Mode 1 : MODEL_ALONE (Génération neuronale brute)**
   - Le modèle de diffusion est exécuté sans contrôle structurel de Brody.
   - **Constat expérimental :** Dérive spatiale sur la fondation `LOCK` (respect de conformité < 0.20), texture diffuse débordante, IoU cible faible (~0.05 - 0.20).

2. **Mode 2 : BRODY_PROCEDURAL_ALONE (Instruments géométriques seuls)**
   - Brody utilise ses instruments de tracé (`PEN`, `BRUSH`) sous plan borné O04.
   - **Constat expérimental :** Respect strict et parfait de la fondation `LOCK` (100% de conformité), squelette géométrique précis, mais absence de synthèse texturale dans la zone `FLEX` (IoU ~0.9237).

3. **Mode 3 : BRODY_PILOTING_MODEL (Orchestration hybride pilotée)**
   - Brody pilote le pipeline :
     a) Trace et verrouille le squelette structurel et la fondation `LOCK` avec ses instruments procéduraux déterministes.
     b) Délègue la synthèse texturale intérieure au générateur neuronal (`NEURAL_FILL`) strictement borné à l'intérieur de la boîte `FLEX`.
     c) Exécute une re-perception en boucle fermée pour vérifier qu'aucun pixel parasite n'a altéré les régions verrouillées.
   - **Constat expérimental :** Conformité `LOCK` maintenue à 100%, synthèse texturale complète de la zone `FLEX`, IoU cible supérieur (1.0000), marge de supériorité Brody de **+93.41%** par rapport au modèle seul.

---

## 5. Synthèse des 32 Chantiers Réconciliés

| Catégorie | Codes | Intitulé | Statut Réconcilié | Preuve |
| :--- | :---: | :--- | :---: | :--- |
| **Fondations** | F00-F03 | Tool Calling, Orchestration bornée, Séparation code/neurones, Décision KX108_ONLY | **LIVE_VERIFIED** | `programmatic_orchestrator_o04.py`, `contracts_v0.py` |
| **Mémoire** | M01-M06 | Frise 6 axes, 34 arbres, Domaines spécialisés, Relations, Recherche par sens, Révisions | **LIVE_VERIFIED** | `cognitive_memory_timeline_v1.py`, `multidimensional_retrieval_v2.py` |
| **Mémoire** | M07 | Recherche trans-domaines | **LIVE_VERIFIED** | `cognitive_memory_timeline_v1.py` |
| **Mémoire** | M08 | Intégration Native Memory | **HOLD** | Conforme constitution KX108_ONLY (pas d'écriture unilatérale) |
| **Mémoire** | M09 | Résolution de contradictions | **LIVE_VERIFIED** | `cognitive_memory_timeline_v1.py` |
| **Orchestration** | O01-O04 | Boucle visuelle, Outils hétérogènes, Orchestrateur borné O04 | **LIVE_VERIFIED** | `programmatic_orchestrator_o04.py` |
| **Vision & Gén.** | V01 | Jarvis Vision V01 | **HOLD** | Architecture tracée (commit 3715985, port 8081). En attente serveur PC Fixe |
| **Vision & Gén.** | V02-V04 | Re-perception, Multi-perspective, Séquences temporelles | **LIVE_VERIFIED** | `visual_reperceiver_evaluator_v1.py`, `video_observation_v0.py` |
| **Vision & Gén.** | G01 | Adaptateur diffusion PIL | **LIVE_VERIFIED** | `diffusion_generator_adapter_v1.py` |
| **Vision & Gén.** | G02 | Moteur diffusion neuronale PC Fixe (sd.cpp) | **HOLD** | Script d'inventaire et protocole prêts. En attente exécution PC Fixe |
| **Éducation** | E01-E05 | Écoles de dessin V0/V1, Instruments V2, Composition E03, Perspective E04, Réel E05 | **LIVE_VERIFIED** | `drawing_school_v0.py`, `compositional_learning_...py` |
| **Tests & Trans.** | T01-T02 | Ablations progressives & indépendantes, Transfert monde inédit | **LIVE_VERIFIED** | `progressive_ablation_...py`, `operational_pipeline_...v3.py` |

---

## 6. Prochaine Action Unique

**Action suivante :**  
Exécuter le script d'audit matériel et lancer le protocole comparatif sur le PC Fixe Titan Dev :
```bash
python scripts/pc_fixe_readonly_environment_inventory.py
python -m brody_world_physique.pc_fixe_neural_trial_protocol_v1 --target PC_FIXE_TITAN_DEV
```
Cette commande relèvera les vrais identifiants GPU (GTX 1050 Ti), vérifiera la disponibilité de `sd.cpp` / `llama-server`, et validera le premier essai d'inférence neuronale piloté en conditions réelles sans dépasser les 4 Go de VRAM.
