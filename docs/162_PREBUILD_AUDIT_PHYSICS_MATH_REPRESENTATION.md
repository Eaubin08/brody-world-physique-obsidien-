# 162 — AUDIT DE CONNEXION AVANT P162 : représentation physique et mathématique ↔ image ↔ génération

**État : AUDIT READ_ONLY des fichiers sur la branche expérimentale, sans raccordement implémenté.**
**Motif :** question utilisateur après P161 : pourquoi les invariants physiques/mathématiques prévus ne donnent-ils pas une excellente précision ?
**Périmètre réellement inspecté :** `README.md`, `docs/02_CONTRACTS.md`, `docs/21_BRODY_IMAGE_MASTER_PLAN.md`, `docs/24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md`, `docs/27_REVERSO_WORLD_MODEL_APPRENTISSAGE_SELECTIF.md`, `docs/42_AUDIT_TRANSVERSAL_REPRESENTATIONS_MONDE_MULTIECHELLES.md`, `docs/43_EXPERIENCE_COMMUNE_BALLE_REPRESENTATIONS_V0.md`, `docs/44_P1_PASSERELLE_MULTIREPRESENTATIONS_VIDEO_MONDE.md`, et code `world_orientation_school_v4_2.py`, `multirepresentation_ball_bridge_v5.py`, `reverso_learning_v0.py`, `image_full_education_p154.py`, `image_hard_visual_ood_p161.py`. Pas d'audit exhaustif des dépôts Obsidia externes dans cette passe.

## 1 — La vision originale à conserver

Selon le plan maître (21), l'audit de fidélité (24), Reverso (27) et l'audit multidimensionnel (42), la représentation n'est **pas seulement la reconnaissance d'un dessin**. Le cycle attendu est :

```text
source/IN, identité, provenance (réel / simulé / généré)
  → observation visuelle F16 / capteurs
  → repères et transformations spatiales F12 / MMonde
  → hypothèses d'état physique, cinématique, contraintes et incertitudes
  → prédictions situées AVANT observation future
  → génération/reconstruction de vue candidate, depuis cet état
  → re-perception, comparaison aux observations indépendantes
  → delta, expérience candidate, replay et rétention gouvernée
```

**Analyse ↔ synthèse et réciproque ; micro↔macro avec modèle explicitement valable ; points de vue 360 ; symétrie/proportion/Fibonacci comme outils potentiels, pas des lois universelles garanties ; apprentissage humain par expérience, friction et correction ; pluralité de connaissances contextuelles.** L'IN et la source ne doivent pas être dénaturés. Ces principes sont documentés ; ils ne constituent pas à eux seuls un runtime unifié.

## 2 — Inventaire : existant vs raccordé

| Couche | Élément réellement présent | Présence dans P161 | Verdict |
|---|---|---|---|
| Source/provenance | Contrats F16, image source/hashes dans P1 ; discipline SIMULATED vs REAL | P161 génère des PNG en mémoire avec style connu du générateur ; aucune admission F16 ni hashing par épisode | **EXISTE PARTIELLEMENT, NON RACCORDE** |
| Décomposition/identité | V4.2 relations orientées ; Reverso V0 décomposition RGBA lossless et replay | Extraction de pixels saturés puis médiane horizontale ; pas de segmentation d'instances ni maintien d'identité multi-objet | **ROUTE PARTIELLE, P161 COURT-CIRCUITE** |
| Géométrie/repères | `SpatialFrameRefV0`, `TrajectoryV0`, dynamique F12 ; P1 repère ancré sur fiduciel de vidéo synthétique | Coordonnées image en px seulement, caméra simulée et non corrigée | **CONTRATS EXISTANTS, PAS DE NORMALISATION P161** |
| Modèle mathématique | Cinématique `forecast` dans P154, modèles de trajectoire de V1/P1 ; accélération moyenne/médiane | Médiane des secondes différences temporelles seulement | **BASELINE CINEMATIQUE, PAS MODELE PHYSIQUE GENERAL** |
| Lois/contraintes | Contrats de mesure F13 et compatibilité F15 ; hypothèses/invariants de world-model dans docs | Pas de force, interaction, matière, collision, masse, caméra extrinsèque/3D ou loi gouvernant les scènes | **NON RACCORDE** |
| Multireprésentation | P1 `multirepresentation_ball_bridge_v5.py` : image, espace, temps, mouvement, delta/experience candidate | P161 ne réutilise pas la passerelle P1 ; seul facteur style change la rasterisation | **PASSERELLE REELLE MAIS NON REUTILISEE** |
| Génération/réciproque | `reverso_learning_v0.py` replay exact RGBA ; P1 future-preview PNG prédictif | P161 n'impose aucune génération depuis état physique, puis re-perception à comparer au frame futur | **RECONSTRUCTION PARTIELLE, BOUCLE NON RACCORDEE** |
| Apprentissage/mémoire | F0 `WorldExperienceCandidateV0`, P155–P160 gates expérimentaux | P161 fige une banque de moyennes et calcule des résultats ; pas de consolidation de compétence ou mémoire native | **CANDIDATS ET TESTS, PAS COGNITION NATIVE CONNECTEE** |
| Autorité | `KX108_ONLY`, observation≠vérité, projection≠preuve, no ACT | P161 conserve les flags de non-écriture et non-promotion | **FRONTIERE DECLAREE RESPECTEE SUR CETTE PASSE** |

## 3 — Diagnostic causal de l'échec P161

Le module `image_hard_visual_ood_p161.py` applique la route `extract(frames) → centre_x → secondes différences → médiane → comparaison banque d'accélérations`. Cela **écrase** plusieurs dimensions pertinentes : vitesse, rythme, accélérations changeantes, identité multi-objets, repère caméra, géométrie profonde, événements, causalité et incertitude de segmentation.

**Exemple falsifiable :** `still` et `linear` ont toutes deux une accélération estimée à 0. Un classificateur qui ne regarde que l'accélération ne peut pas les distinguer, même sur pixels parfaitement extraits. Cela explique que P161 donne des `MULTI` sur des scènes pourtant non ambiguës quand la vitesse serait incluse.

**Échec visuel sous `clutter`/`combined` :** la médiane des pixels saturés est polluée par des distracteurs ; aucune piste d'identité/stabilité de l'objet ni transformation de caméra n'est imposée. Ainsi, une erreur apparente de physique peut découler **en amont** d'une perception incorrecte. Le score `perception_coverage` basé sur le nombre de centres non-None n'est pas une mesure de précision de segmentation : une position fausse peut compter comme « couverte ».

**Inconnus :** une inversion de vitesse ou un saut peut présenter une accélération médiane compatible avec un modèle connu ; `MULTI` n'est donc pas détection prouvée de nouveauté.

**Conclusion : P161 teste un raccourci cinématique, pas l'hypothèse complète du projet.** Son RED ne réfute pas les ambitions mathématiques de la vision utilisateur ; il ne les valide pas non plus.

## 4 — Sur la précision « parfaite » : contrat testable

La fidélité exacte peut être exigée sur un **objet mathématique discret et connu** (par exemple : reconstruction RGBA décodée sans perte depuis des tuiles). Elle ne peut pas être promise sans conditions pour toute observation physique partielle.

- `PIXEL_EXACT` : reconstruction sans perte de mêmes pixels décodés et même cadre ;
- `GEOMETRIC_EXACT_WITHIN_MODEL` : transformation/rendu déterministes et paramètres/repères connus, tolérance numérique définie ;
- `PHYSICS_CONSISTENT` : résidus de contrainte faibles sous hypothèses explicites ;
- `OBSERVATIONALLY_UNIDENTIFIABLE` : plusieurs états du monde produisent les mêmes observations ; la réponse adéquate est MULTI/HOLD ou recherche de nouvelle preuve.

Aucune formule (Fibonacci, symétrie, etc.) ne peut créer l'information absente d'une mesure. Sa valeur est de fournir des **contraintes vérifiables**, pas de forcer une solution unique.

## 5 — Préconditions obligatoires de P162 (ne pas reconstruire toute la stack)

1. **Réemployer la route P1/F0** (ou, si empêchée, enregistrer le blocage) et produire des références compatibles aux mêmes observations image/espace/temps/mouvement. Aucun nouvel objet root concurrent de `WorldStateV0`.
2. **Remplacer les seules moyennes d'accélération** par observations datées, vitesses, accélérations, événements de rupture, identité, visibilité et qualité de perception, avec repère caméra explicite.
3. **Comparer deux prédictions séparées** : observables image/px et état spatial compensé caméra ; ne pas mélanger les repères.
4. **Créer le reverse réel du test** : un état estimé → image candidate sans lecture du futur → nouvelle perception de l'image synthétisée → delta contre une image tenue secrète.
5. **Conserver exactement les cellules RED de P161**, les mêmes splits/Seeds autant que possible et des baselines appariées. Ne jamais entraîner P162 sur les examens P161 utilisés pour la sélection.
6. **Garder un examen inédit scellé** avec styles composés, plusieurs objets, changement de repère et séquences ambiguës. Distinguer erreur perceptive, erreur de loi, erreur de rendu, erreur de décision.
7. **Evaluer au moins 4 sorties épistémiques :** SELECT connu, MULTI alternatives compatibles, HOLD source pauvre, et `NOVELTY_CANDIDATE` (sans élévation en vérité).
8. **Garder lecture seule externe** : native memory write=false ; canonical promotion=false ; no ACT ; KX108_ONLY ; code dans la branche expérimentale uniquement.

## 6 — Gates de reprise

- **AUDIT_CONTRACTS:** références amont prouvées, pas de duplication F12/F16/MMonde ;
- **PERCEPTION_GATE:** métriques d'identité, precision de centre et erreurs de caméra séparées du taux de réponse ;
- **WORLD_GATE:** conversion repères/temps/unités cohérente, hypothèses et rang d'observabilité ;
- **REVERSE_GATE:** prediction précommit, image générée, re-perception et comparaison indépendante ;
- **HARD_OOD_GATE:** ne pas classer des événements inédits en lois connues avec assurance non calibrée ;
- **NO_REGRESSION_GATE:** ablation P161 baseline sur scènes équivalentes, aucun succès de segmentation cachant un échec de dynamique ;
- **GOVERNANCE_GATE:** aucune mémoire canonique modifiée ni autorité d'action.

### Verdict de cet audit
`PRE_P162_AUDIT_READ_ONLY_COMPLETE / PHYSICAL_MATHEMATICAL_VISION_DOCUMENTED / PARTIAL_EXECUTABLE_BRIDGES_EXIST / P161_BYPASSES_BRIDGES / PHYSICS_3D_CAMERA_WORLD_GENERATOR_NOT_INTEGRATED / P162_BUILD_NOT_STARTED`.

**Ce rapport est un audit des fichiers listés dans l'en-tête ; il ne prétend pas valider l'état actuel des autres repos Obsidia ni le branchement GPU/LLM du PC.**
