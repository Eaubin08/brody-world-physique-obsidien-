# 81 — BRODY IMAGE : RÉUNIFICATION DE L'ÉCOLE HISTORIQUE ET DES BOUCLES P2

**Statut : PLAN D'INTÉGRATION / AUCUN RUNTIME UNIFIÉ REVENDIQUÉ**  
**Branche de travail :** `exp/p2-multirepresentation-ablation-20261009` ; `main` intouchée.

## Décision
**Ne pas remplacer l'éducation historique par les micro-tests P2.12.** Réutiliser l'école V0–V4.2 comme parcours d'observation / imitation / rappel / relations / monde, et **insérer les outils P2.10–P2.12 comme moyens de correction, comparaison, contrôle et apprentissage** à chaque stade. Ni retour en arrière ni simple empilement de tests : un même épisode pédagogique doit traverser les capacités disponibles et laisser des preuves comparables.

Sources canoniques : [21](21_BRODY_IMAGE_MASTER_PLAN.md), [23](23_BRODY_IMAGE_LEARNING_TRACEABILITY.md), [24](24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md), [65](65_P29J_COUVERTURE_CONCEPTS_ET_HYBRIDE_FIGE.md), [66](66_P210_PLAN_FORGE_BOUCLES_GENERATION_IMAGE.md), [80](80_P212D_GATE_CONSERVATEUR_STATS_VISUELS.md).

## 1. Inventaire des organes — réutiliser, ne pas recoder
| Organe | Compétence / preuve à revoir | Rôle dans l'école fusionnée |
|---|---|---|
| `drawing_school_v0` | forme, copie, feedback, correction, rappel, échec du souvenir | alphabet visuel et première tentative |
| `drawing_school_v1` | trajectoires du trait, rendu, corrections REMOVE/REPLACE | moteur gestuel |
| `instrument_school_v2` | choix et adaptation des outils de tracé | compétence procédurale, contexte d'instrument |
| `drawing_memory_school_v3` | représentation conservée, image du professeur cachée, délai, interférences, composition inédite | rappel autonome contrôlé |
| `world_relations_school_v4_1` | relations spatiales simulées entre composants | topologie et composition |
| `world_orientation_school_v4_2` | orientations, réciproques et transformations 2D | invariances et points de vue partiels |
| `reverso_learning_v0`, `image_v0` | décomposition/rejeu raster, zones et masques | analyse ⇄ synthèse, conservation de source |
| P2.4–P2.9 | fluctuations, contraste, observations multiples, anticipation vidéo, statuts épistémiques | contexte, temps et changement |
| P2.10a–e | comparaison d'images, erreur par zone, correction, journal, transfert | évaluation et retour d'expérience |
| P2.11a–e | mémoire de geste, recomposition, benchmark et diagnostic | réutilisation sous nouvelles contraintes |
| P2.12a–d | propositions bornées, transfert TRAIN→TEST, rapports comparatifs, ACT/HOLD | choix prudent et mesure des régressions |
| F16, F12, MMonde/SENS, Native Memory | contrats externes existants / intégration variable | données situées et provenance, sans dupliquer les ontologies |

**Attention :** la présence de code ou d'un contrat n'est pas une preuve d'intégration runtime ; les raccords effectifs sont à mesurer. Le `30/30` des tests ciblés P2.11a–P2.12d ne démontre pas l'apprentissage d'objets ni la qualité générale d'images.

## 2. Curriculum fusionné : une école du monde, par expériences
| Stade | Question que Brody doit apprendre à traiter | Exercices | Garde-fous/mesures |
|---|---|---|---|
| E0 — primitives | Qu'est-ce qui est vu et où ? | ligne, carré, X, vide, contour discontinu ; originaux locaux `lesson_01_first_drawing`, `exam_01_from_memory` etc. | source initiale conservée, pixels, formes, faux positifs |
| E1 — rappel et action | Puis-je refaire ce que j'ai observé ? | montré→caché, immédiat→différé, interférences, choix d'instrument | comparatif avant/après, seed mémoire absent, rejets nuisibles |
| E2 — formes et objets | Quelles parties composent un objet, qu'est-ce qui reste invariant ? | décomposer/recomposer formes, objets simples avec fonds/occlusions et variations contrôlées | identité = candidate, masques, parties, proportions, erreurs par région |
| E3 — relations | Où sont les éléments les uns par rapport aux autres ? | voisinage, inclusion, dessus/dessous, relations réciproques, ordre des plans | V4.1/V4.2, comparaison par objet et scène |
| E4 — transformations | Qu'est-ce qui change et qu'est-ce qui reste ? | déplacement, rotation, taille, angle, symétrie, transformations réversibles | épreuves inédites, orientation 2D ≠ vision 360° prouvée |
| E5 — situations / monde | Que peut-on anticiper avant de savoir formuler une loi ? | temps, balle en chute, contact, obstacles, mouvement, causalité inconnue | observations passées seules, précommit, preuves causales distinctes |
| E6 — génération et création | Puis-je recomposer une scène fidèle à l'IN sans recopier sa cible ? | couches du peintre, variations de décor et style, reconstruction puis nouvelle composition | cible TEST masquée, SOURCE et IN, fidélité par zones, Reverso |
| E7 — transfert | Quelle compétence choisir et quand s'abstenir ? | nouvelles scènes, fautes de méthode, reprise d'expériences utiles et négatives | ACT/HOLD, politique figée TRAIN, erreurs/regressions conservées |

Les étages E0–E7 sont un **curriculum d'intégration proposé**, pas une preuve de niveau scolaire atteint. La reconnaissance d'objets réels et la compréhension physique restent non démontrées.

## 3. Une épreuve = même observation, trois chemins
- **HISTORIQUE** : école V0–V4.2 exécutée telle quelle, avec prérequis et sorties originales.
- **FUSIONNÉ** : mêmes entrées permises + capacités P2 de mémoire, Reverso applicable, choix et correction.
- **ABLATION** : même chemin fusionné en retirant successivement la mémoire, le gate, le moteur Reverso ou la vue spatiale, sans ajouter une autre information.

**Ne pas comparer naïvement :** une école supervisée qui voit la cible pendant la correction et une école aveugle à la cible. Rapport distinct `GUIDED`, `HIDDEN_TARGET`, `UNSEEN_TRANSFER`; condition d'observation explicitée. Même budget de temps/essais et mêmes données TRAIN quand les modes sont comparables.

## 4. Contrat commun d'un examen
`source_ref`, `source_sha256`, `intent_IN`, `lesson_id`, `stage`, `allowed_observations`, `teacher_reveal_time`, `train_or_test`, `prior_experience_refs`, `representation_refs`, `method_refs+sha256`, `draft_png_sha256`, `final_png_sha256`, `baseline_png_sha256`, `error_by_region`, `geometry_relation_scores`, `memory_reuse_proof`, `rollback_history`, `epistemic_status`, `decision_authority`.
D'abord dessiner/sceller, ensuite ouvrir la référence TEST pour la note. Sur TRAIN, l'aide du professeur est permise et enregistrée comme telle. Pas d'écriture Native Memory/B8 ; `KX108_ONLY`.

Sortie obligatoire par examen : **planche visuelle** `SOURCE / PREMIER ESSAI / APRÈS FEEDBACK / DE MÉMOIRE / TRANSFERT` (cases marquées NON_APPLICABLE si le mode ne le permet pas), `metrics.json`, `episodes.jsonl`, `manifest.json`. Afficher les erreurs négatives et les corrections rejetées.

## 5. Recouvrer les premières preuves
L'utilisateur dispose localement de onze PNG des premiers examens : `lesson_01_first_drawing(1).png`, `lesson_02_first_drawing(1).png`, `lesson_03_first_drawing(1).png` et `exam_01...04_{from_memory,after_feedback}(1).png`. **Ne pas les traiter comme un jeu complet de référence/ground-truth :** l'image du professeur, les reçus et les métadonnées d'époque doivent être retrouvés dans `build` ou `evaluation.json` pour attribuer des notes fiables. Préserver les fichiers bruts et SHA256.

Preuves distantes identifiées sur `evidence/brody-local` : `evidence/relations-v4-1-20261009-003945`, `evidence/orientation-v4-2-20261009-012020`, `evidence/p2-evidence`. Le rapport V4.2 comporte 11/11 examens synthétiques corrects, ce qui ne signifie pas reconnaissance générale d'objets.

## 6. Ordre de forge et gates
**FUSION-F0 — lecture seule :** inventaire détaillé des fonctions, branches et épreuves V0–V4.2 ; recoupement des onze premiers PNG, données de professeur et historiques `build`. Validation : aucune perte de provenance.
**FUSION-F1 — adaptateurs :** faire converger les entrées/sorties des écoles et des bancs P2 sur le contrat d'épisode, *sans modifier les algorithmes* ; ne pas faire entrer le feedback TEST dans TRAIN.
**FUSION-F2 — replay scolaire :** rerun exact V0→V4.2 et tests P2.10→P2.12d, avec sorties conservées, diff de versions et tests anti-régression.
**FUSION-F3 — formation progressive :** E0→E7 avec difficulté graduelle, échec, aide du professeur, rappel différé, nouveau contexte ; prérequis évalués.
**FUSION-F4 — ablations :** historique / fusionné / composants retirés, mêmes ressources et mêmes contraintes d'observation ; scores visuels et conceptuels.
**FUSION-F5 — extensions :** vrais objets/vidéos, points de vue, matériaux, perception dynamique, seulement après contrôles de fuite et cohérence.

**Critère d'arrêt :** un stade ne passe pas parce que les tests unitaires passent; il passe si l'élève réussit plusieurs exercices nouveaux, avec métriques et images visibles, et ne régresse pas par rapport au palier précédent.

## 7. Statuts au départ de la fusion
- Tests ciblés PC P2.11a→P2.12d : **30/30 PASS** (retours utilisateur) ; autres tests du dépôt non comptés.
- P2.12c TEST synthétique contradictoire : **1/3 amélioré, 2/3 dégradés**, pas de gain de généralisation universel.
- V4.2 ancien rapport : **11/11 examens synthétiques corrects**, périmètre orientation 2D/réciproque.
- Retour à la vraie pédagogie et fusion E0–E7 : **PLAN**, pas encore exécuté.
- POURCENTAGE GLOBAL D'UNE « IA QUI COMPREND LE MONDE » : **NON ÉTABLI**.

Prochaine action : compiler le registre de tests historiques et créer le protocole d'export des premières images locales, sans pousser les fichiers bruts ni modifier `main` par défaut.
