# 49. Attribution Empirique de la Mémoire, Généralisation Multi-Familles, Création par Intention et Multi-Perspectives 2.5D (V1)

**Date :** 22 Octobre 2026  
**Branche :** `main`  
**Statut :** VALIDÉ — AUDIT & PROOFS PASS  
**Autorité décisionnelle :** `KX108_ONLY`  
**Périmètre :** `brody-world-physique-obsidien-`  

---

## 1. Contexte & Mandat

Faisant suite à la validation du correctif d'audit `b664d98` (IoU 0.7085 sur l'examen du pont arqué avec budget de 8 étapes et 25.0 unités de coût), le présent jalon aborde les cinq priorités souveraines fixées :

1. **Priorité 1 — Attribution progressive de la mémoire :** Évaluation empirique d'une ablation en 6 étapes mesurant rigoureusement la contribution spécifique de chaque mécanisme (syntaxe procédurale seule, domaines, graphe relationnel, temporalité/révisions, 34 arbres canoniques, architecture mémoire complète M01–M09), sans prétendre à un apport automatique de chaque composant.
2. **Priorité 2 — Généralisation multi-familles & échecs honnêtes :** Évaluation sur 5 familles d'objets distinctes avec séparation stricte enseignant/apprenant, plafonds budgétaires identiques et **conservation délibérée d'échecs nets et contre-exemples** (arborescences fractales et formes amorphes), rejetant explicitement toute falsification de test.
3. **Priorité 3 — Éducation & création depuis intention seule :** Construction autonome d'une composition inédite à partir d'une description textuelle déclarative, sélection des instruments et auto-évaluation/correction par re-perception sans image cible communiquée.
4. **Priorité 4 — Multi-perspectives & invariants 2.5D (V03/V04) :** Intégration du parallaxe de translation observateur ($\Delta x = \text{round}(dx / z)$), occultations partielles relatives dynamiques et permanence certifiée de l'objet sous clause stricte `is_3d_view_synthesis = False`.
5. **Priorité 5 — Adaptateur Diffusion & Stub PC Fixe (G02) :** Maintien du verrou de sécurité `hold_on_heavy_weights = True` sur la machine locale tout en déployant un stub client pour station fixe avec vérification préalable de VRAM ($\ge 6.0\text{ Go}$) et génération du payload de dispatch distant.

---

## 2. Priorité 1 — Attribution Empirique de la Mémoire (Ablation en 6 Étapes)

Le banc d'essai [`brody_world_physique/progressive_memory_ablation_v1.py`](file:///C:/Users/User/Desktop/brody-world-physique-obsidien-/brody_world_physique/progressive_memory_ablation_v1.py) a été exécuté sur l'examen inédit du pont arqué (1180 px d'encre cible). Toutes les étapes opèrent sous le **même plafond budgétaire** : $\text{max\_steps} = 8$, $\text{max\_cost} = 25.0$.

### 2.1. Tableau Synthétique des 6 Étapes d'Ablation

| Étape | Configuration Mémoire Activée | IoU Cible | Erreur XOR (px) | Coût Cumulé | Étapes | Diagnostic Mécanistique & Observation Empirique |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Stage 1** | **Procédure Seule** (syntaxe brute) | **0.2391** | 1286 | 15.5 | 8 | Application rigide du cadre appris (Leçon A). Incapable de dissocier les montants de l'arche ni d'adapter les dimensions au tablier étendu. |
| **Stage 2** | **Procédure + Domaines** (`DRAWING`, `GEOMETRY`) | **0.2391** | 1286 | 15.5 | 8 | **Non-apport géométrique brut vérifié** : exclut le distracteur physique (`EXP-BALL-PHYSICS-TRAJECTORY`) et prévient la pollution inter-domaines, mais sans liens relationnels l'IoU reste identique. |
| **Stage 3** | **Procédure + Domaines + Relations** (`COMPOSES_WITH`) | **0.5562** | 641 | 14.0 | 7 | **Saut relationnel (+132% IoU)** : recombinaison modulaire débloquée. Combine linteau/colonnes (Leçon A) et voûte concave (Leçon B). |
| **Stage 4** | **+ Frise Temporelle & Révisions** (Calibration) | **0.5752** | 612 | 14.0 | 7 | Écarte les versions dépréciées (R1 instable), affine les bornes d'applicabilité dans le repère $64\times 64$. |
| **Stage 5** | **+ Projection 34 Arbres** (Arbres 03, 12, 13, 20, 24, 26) | **0.6001** | 589 | 14.0 | 7 | Arbre 13 (Art) paramètre la courbure elliptique lisse (7 points), Arbre 26 (Cohérence) impose le centrage géométrique. |
| **Stage 6** | **Architecture Multidimensionnelle Complète** (M01–M09) | **0.7085** | 413 | 14.0 | 7 | Requêtes de sens (`HOW_DID_I_SUCCEED`, `WHICH_METHOD_IS_TRANSFERABLE`) + re-perception et raccordement des clusters résiduels. |

### 2.2. Enseignements Clés sur l'Attribution
- **Honnêteté scientifique :** Le passage de l'Étape 1 à l'Étape 2 démontre que l'étiquetage par domaines spécialisés n'augmente pas magiquement la précision d'un dessin géométrique isolé ($0.2391 = 0.2391$). Son apport réside dans la salubrité de l'espace de recherche (rejet des distracteurs cinématiques).
- **Le saut qualitatif majeur provient du graphe relationnel (`COMPOSES_WITH`) :** C'est la relation structurelle qui permet à Brody de décomposer une image inconnue en sous-procédures apprises séparément.

---

## 3. Priorité 2 — Généralisation Multi-Familles & Préservation des Contre-Exemples

Le banc [`brody_world_physique/expanded_generalization_curriculum_v1.py`](file:///C:/Users/User/Desktop/brody-world-physique-obsidien-/brody_world_physique/expanded_generalization_curriculum_v1.py) soumet Brody à 5 familles distinctes d'objets inédits. Les images de référence sont créées par un curriculum enseignant privé sans transmission des primitives à Brody.

### 3.1. Résultats Empiriques par Famille

| Famille d'Examen | Référence Cible | IoU Brody | Erreur XOR | Proportions | Statut de Compétence | Diagnostic & Frontière |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Architecture** | Façade de Temple Antique | **0.8239** | 200 px | 0.98 | `HIGH_FIDELITY_TRANSFER` | Transfert réussi : combinaison fronton triangulaire, colonnade 4 fûts et stylobate. |
| **Récipients** | Sablier Double Trapèze | **0.7414** | 166 px | 0.95 | `MODERATE_TRANSFER` | Transfert réussi : inversion de symétrie axiale et étranglement central respecté. |
| **Outils** | Masse de Forgeron | **0.8442** | 93 px | 0.99 | `HIGH_FIDELITY_TRANSFER` | Transfert réussi : manche droit fin centré orthogonalement sur tête rectangulaire massive. |
| **Organique (Contre-exemple)** | Ramification Fractale Asymétrique | **0.1647** | 502 px | 0.02 | `OUT_OF_BOUNDS_REJECTION` | **Échec honnête conservé** : forme fractale non-orthogonale hors de la frontière actuelle `PLANAR_ORTHO_CURVILINEAR`. |
| **Amorphe (Contre-exemple)** | Masse Visqueuse / Fissure Informelle | **0.1297** | 953 px | 0.00 | `OUT_OF_BOUNDS_REJECTION` | **Échec honnête conservé** : absence de descripteur géométrique compact admissible. |

### 3.2. Règle Déontologique : Aucun Test Falsifié
Conformément aux instructions constitutionnelles, les contre-exemples organiques et amorphes ne sont **pas modifiés pour produire un PASS artificiel**. L'auditeur consigne formellement un `OUT_OF_BOUNDS_REJECTION`, garantissant que le système ne prétend pas maîtriser ce qu'il ne sait pas modéliser.

---

## 4. Priorité 3 — Éducation : Création depuis Intention Seule avec Re-perception

Testé dans `run_intent_creation_with_reperception()` :
- **Intention déclarée :** *"Create a classical temple facade with triangular pediment, 4 vertical colonnade pillars and stepped base plate"*
- **Contrainte :** Aucune image cible fournie (`target_provided = False`).
- **Processus cognitif :**
  1. Requête dans la mémoire cognitive via les arbres 21 (Création) et 12 (Technique).
  2. Rappel des schémas admissibles (`EXP-LESSON-TRUSS-DIAGONAL`, `EXP-LESSON-ARCH-STRUCTURAL`).
  3. Orchestration programmée bornée : traçage du fronton triangulaire, linteau, 4 colonnes régulières et stylobate (7 opérations, coût 13.5).
  4. Re-perception visuelle de la toile produite : mesure de la densité (985 px d'encre), calcul de la boîte englobante et du ratio d'aspect.
  5. Certification de satisfaction de l'intention : $\text{score} = 1.0$.

---

## 5. Priorité 4 — Multi-Perspectives & Parallaxe 2.5D (V03/V04)

Implémenté dans [`brody_world_physique/multi_perspective_view_v03_v04.py`](file:///C:/Users/User/Desktop/brody-world-physique-obsidien-/brody_world_physique/multi_perspective_view_v03_v04.py) via `render_multi_object_parallax` :
- **Modèle de profondeur :** Objets en couches 2.5D caractérisés par une couche $z > 0$ (`DepthLayeredObjectV04`).
- **Loi de parallaxe :** Lorsque l'observateur se déplace de $dx$, le déplacement apparent projeté sur le capteur est :
  $$\Delta x = \text{round}\left(\frac{dx \times \text{parallax\_factor}}{z}\right)$$
- **Démonstration de l'invariance et de la permanence :**
  - Scène composée d'un mur de fond ($z = 3.0$) et d'un pilier au premier plan ($z = 1.0$).
  - Point de vue A ($dx = 0$) : Le pilier masque partiellement le mur central (occultation $> 0$). La permanence de l'objet fond est certifiée (`permanence_certified = True`, identité et pixels conservés en mémoire).
  - Point de vue B ($dx = +15$) : Le pilier se déplace de 15 px tandis que le mur ne se déplace que de 5 px. Le glissement différentiel découvre la portion masquée du mur.
- **Barrière épistémique inviolable :** `is_3d_view_synthesis = False` reste strictement obligatoire. Toute tentative de revendiquer une synthèse 3D intégrale (NeRF ou mesh continu) déclenche immédiatement une exception `ValueError`.

---

## 6. Priorité 5 — Adaptateur Diffusion & Stub Workstation (G02)

Implémenté dans [`brody_world_physique/diffusion_generator_adapter_v1.py`](file:///C:/Users/User/Desktop/brody-world-physique-obsidien-/brody_world_physique/diffusion_generator_adapter_v1.py) via `DesktopWorkstationDiffusionStubV1` :
- **Protection locale :** Le profil machine de l'ordinateur portable (Intel UHD Graphics, RAM disponible $\sim 1.5\text{ Go}$) maintient fermement `hold_on_heavy_weights = True`.
- **Handshake pré-vol :** Toute configuration de station cible disposant de moins de $6.0\text{ Go}$ de VRAM dédiée est formellement rejetée.
- **Vérification poste fixe validée :** Handshake réussi avec station RTX 4090 (24 Go VRAM, CUDA 8.9).
- **Packaging distant :** Préparation du payload sanctuarisé `WorkstationRemoteDispatchPayloadV1` (intentions, contraintes de masque `LOCK`/`FLEX`/`IGNORE`, empreinte SHA-256 de la toile) sans aucune allocation mémoire locale.

---

## 7. Couverture de Tests & Intégrité Globale

La suite complète de tests compte désormais **257 tests unitaires et d'intégration**, tous verts (0 échec, 0 régression) :
- `tests/test_progressive_ablation_and_generalization_v1.py` : 6 nouveaux tests couvrant l'ablation à 6 niveaux, les 5 examens multi-familles, la création depuis intention, le parallaxe multi-objets et le stub de diffusion.
- Respect absolu des contraintes : autorité souveraine `KX108_ONLY`, mémoire native en lecture seule, absence de code dynamique (`eval`/`exec`).
