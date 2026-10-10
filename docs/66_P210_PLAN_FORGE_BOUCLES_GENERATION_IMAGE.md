# 66 — P2.10 — Plan de forge : boucle d'apprentissage par génération d'images

STATUS: DESIGN_READY / NO_RUNTIME_CLAIM / IMAGE_GENERATION_ONLY
BRANCH: exp/p2-multirepresentation-ablation-20261009
MAIN: DO_NOT_TOUCH

## Périmètre et objectif
Le but est de permettre à Brody Image d'observer une image source, de décomposer les éléments utiles, générer/reconstruire, analyser les écarts par région et couche, corriger une partie, produire une nouvelle version, conserver les échecs et les méthodes, puis réutiliser ce savoir-faire sur une autre image. **Il ne s'agit pas d'étendre ce dispositif à toute la cognition, ni de faire passer une copie supervisée pour une génération autonome.**

## Organes existants — ne pas reconstruire
- `brody_world_physique/reverso_learning_v0.py` : `decompose_reverso`, `replay_reverso`, `triage_learning`. Réciprocité raster *lossless*; la reconstruction identique n'est pas un benchmark d'amélioration visuelle.
- `brody_world_physique/image_v0.py` : `chroma_key_mask`, `run_image_edit` et contrôles des pixels.
- `brody_world_physique/drawing_school_v1.py` : `suggest_gestures_from_reference`, `correct_drawing`, `render`, fonctions internes d'effacement/remplacement; apprentissage guidé, non générateur libre.
- `brody_world_physique/drawing_memory_school_v3.py` : `observe_only`, `draw_from_snapshot`, `verify_school` — modèle caché et précommit.
- `brody_world_physique/experience_memory_v1.py` : `record_episode`, `verify_episode`, `verify_memory_bundle`, code fingerprint et registre de compétences. Ne pas exécuter du Python issu de souvenirs arbitraires.
- V4/V4.1/V4.2 : relations, proportions, orientations et inverse; 2D partiel. Les concepts 360°/symétrie/Fibonacci restent pistes à comparer sans imposer des corrections incorrectes.
- P2.9h/i/j : diagnostics de position historiques, hors périmètre runtime du loop image. Aucune dépendance fonctionnelle obligatoire à leurs bancs vidéo.

## Contrat commun à toutes les étapes
`VisualGenerationEpisodeV0` :
- source immuable: SHA256, dimensions, pixel hash, référence et intention `IN` déclarée;
- zone et couche (masque, contour, composition, texture, couleur, géométrie/perspective) avec provenance explicite; conserver l'espace source et le référentiel;
- version initiale, versions candidates, métriques *par région et fond*, masques d'erreurs et couverture; ne pas masquer un objet dégradé sous une MAE faible du fond;
- choix de méthode, capability ID/version/hash, paramètres bornés, pré-engagement, historique ordonné, état best-known et raison d'arrêt;
- suite de tests de fidélité: pixels sous protection, forme/proportion, rapports de parties, intersection de masques, raster au niveau objet et image;
- aucune vérité construite depuis l'image générée par le même moteur; oracle source seulement comme **référence de correction supervisée**, caché pendant la génération de transfert;
- local experience candidates; NO Native Memory write / B8 promotion / KX108 action.

## P2.10a — contrat de boucle
Livrables :
- `brody_world_physique/p210a_visual_loop_contract_v0.py`
- `tests/test_p210a_visual_loop_contract_v0.py`
- `docs/67_P210A_VISUAL_LOOP_CONTRACT.md`

Implémenter un épisode en états `SOURCE_LOCKED -> GENERATED -> SCORED -> CORRECTION_CANDIDATE -> ACCEPTED|ROLLED_BACK|HOLD -> EXPERIENCE_CANDIDATE`. Toute image versionnée et source inviolable. Erreurs de génération conservées; erreur de fichier/empreinte traitée séparément, sans l'apprendre comme règle visuelle. Tests de hash source, absence de score avant image générée, non-réécriture, rollback, répétition de tentative, limite d'itérations et arrêt sur stagnation.

## P2.10b — diagnostic d'erreur typée
Livrables :
- `brody_world_physique/p210b_visual_error_atlas_v0.py`
- `tests/test_p210b_visual_error_atlas_v0.py`
- `docs/68_P210B_VISUAL_ERROR_ATLAS.md`

Classes `POSITION / SHAPE / PROPORTION / ORIENTATION / COLOR / TEXTURE / BACKGROUND / PART_RELATION / OCCLUSION / UNKNOWN`; une image peut présenter plusieurs erreurs. Masques diff source-généré, scores objet et fond séparés, fidélité des pixels protégés, ordre de composition. Diagnostic `UNKNOWN` plutôt qu'attribution causale sans preuve. Enregistrer les changements perceptuels utiles même s'ils semblent être du bruit dans une autre représentation.

## P2.10c — correcteur local avec rollback
Livrables :
- `brody_world_physique/p210c_targeted_image_correction_v0.py`
- `tests/test_p210c_targeted_image_correction_v0.py`
- `docs/69_P210C_TARGETED_CORRECTION.md`

Brancher les masques et gestes réels via `image_v0` + `drawing_school_v1` + `reverso_learning_v0`. Proposer une seule modification bornée à la fois. Contrôler pixels protégés, source, aire modifiée, erreur sur région ciblée et dégradation hors-zone. Comparer version candidate vs meilleure version, rollback si régression; **conserver la tentative échouée**. Démarrer avec corrections géométriques / gestes déterministes; n'appeler aucun gros générateur externe à cette étape. Vérifier les capacités et leurs empreintes.

## P2.10d — expérience visuelle procédurale et réemploi
Livrables :
- `brody_world_physique/p210d_visual_error_memory_bridge_v0.py`
- `tests/test_p210d_visual_error_memory_bridge_v0.py`
- `docs/70_P210D_VISUAL_ERROR_MEMORY.md`

Adapter (ne pas dupliquer) `record_episode` et le système de compétences autorisées existant. Conserver tentatives, échecs, versions et paramètres, amélioration conditionnelle, résultat, contexte, alternatives, rollback. Seuls des chemins autorisés/versionnés peuvent être rejoués. Mémoire expérimentale locale et candidate, sans promotion ni écriture canonique. L'historique informe une nouvelle tentative sans transformer une corrélation en vérité de génération.

## P2.10e — examen de transfert réel image->image
Livrables :
- `brody_world_physique/p210e_visual_transfer_benchmark_v0.py`
- `tests/test_p210e_visual_transfer_benchmark_v0.py`
- `docs/71_P210E_IMAGE_TRANSFER_BENCHMARK.md`

Prédéfinir TRAIN images sources de référence et TEST entièrement distinctes (hash, formes, style, proportion et perspective contrôlés). Comparer `NO_LOOP`, `FIXED_CORRECTION`, `MEMORY_SELECTED_CORRECTION`, `ORACLE_DIAGNOSTIC_CONTROL` (oracle exclu du verdict autonome). Évaluer réduction d'erreur par image et par objet, taux de rollback, dégâts hors cible, budget calcul, taux HOLD, réemploi des expériences et erreurs répétées. Faire scorer TEST seulement après la version engagée et interdire tout ajustement de paramètres sur TEST. Rapports JSON, images versions comparées, hashes, replay indépendants. Échec de transfert = résultat expérimental conservé.

## Ordre, gates et précautions
1. a → contrat compilable et tests; aucune boucle d'entraînement revendiquée.
2. b → mesures diagnostics avec falsifications (fond dominant, zones protégées, déformation et masques vides).
3. c → première correction + rollback sur des images locales, **vraies PNG** et non seulement scores synthétiques; vérifier le rejet d'une correction destructive.
4. d → historique des démarches et leur rejouabilité; source de référence conservée en lecture seule.
5. e → jeu inconnu, sélection pré-engagée, résultats neutres et publication du rapport local; interdiction de réutiliser TEST pour améliorer artificiellement les résultats.

Règle du user: **les erreurs de génération contribuent à l'apprentissage parce que chaque tentative est réversible**. Boucles bornées et chemins de reprise; conserver l'échec et le contexte, pas uniquement le meilleur PNG.

### Critères d'acceptation finals
- Bénéfice de correction mesuré par région, pas uniquement MAE image globale.
- Bénéfice de réutilisation mesuré sur images réellement nouvelles.
- Retour arrière exact lorsque la modification est nuisible, trace d'échec conservée.
- Rejeu déterministe du journal et des images finales.
- Aucune déformation de source et intention originale; distinguer cible exacte et marge créative.
- Aucun prétendu « apprentissage général » si les corrections utilisent directement une image cible visible.

Ce plan est un document d'implémentation : **aucune fonctionnalité P2.10a-e n'est annoncée comme codée/testée** à ce stade.
