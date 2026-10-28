# F1 — Première séance éducative unifiée de Brody Image

**Statut : SPECIFICATION EXECUTABLE A RACCORDER — aucun E2E validé**  
**Base F0-B :** `3037810`, branche `exp/p2-multirepresentation-ablation-20261009`, 9/9 tests ciblés (3/3 école continue, 4/4 éducation cumulative P156, 2/2 génération réciproque).  
**Autorité :** `KX108_ONLY`; `NATIVE_MEMORY_WRITE=FALSE`; `CANONICAL_PROMOTION=FALSE`.

## But unique
Tester si un **même élève expérimental** anticipe et reconstruit le mouvement d'une balle, progresse après des leçons, réemploie une compétence dans une situation inconnue, puis la conserve après une autre leçon et une interruption. Ne pas confondre la réussite séparée des trois organes F0-B avec un apprentissage unifié.

## Parcours figé
1. **T0 — Baseline aveugle** : état de départ scellé, mémoire éducative absente; observation limitée aux images passées; prévision d'une position future **et** reconstruction de l'image future. Sceller prédictions, PNG, configuration et SHA256 avant évaluation.
2. **TRAIN-A — Leçons de balle** : observations et feedback datés; apprentissage expérimental de représentation, mouvement, temporalité et reconstruction réciproque; checkpoints versionnés. Distinguer données vues, heuristiques programmées, corrections du professeur et hypothèses découvertes.
3. **T1 — Examen aveugle** : balle dans trajectoire non vue; même budget et même entrée que T0; prédiction et PNG avant révélation de la cible; examiner erreur de position, géométrie, fond et objet.
4. **TRAIN-B — Interférence** : autre compétence visuelle non identique à TRAIN-A (par exemple relation entre deux formes); ne montrer aucune référence T1 ni future épreuve de rappel.
5. **PAUSE / REPRISE** : arrêter puis restaurer l'état éducatif candidat depuis un checkpoint scellé; garantir mêmes capacités et preuves, sans réinjecter de vérité TEST.
6. **T2 — Rappel et transfert** : un nouveau mouvement de balle inconnu, incluant une variation de forme, de caméra ou de contexte; mesurer compétence A après B et après reprise, en comparaison avec le checkpoint précédent.
7. **AUDIT** : vérifier provenance, rejouabilité, absence de fuites, versions de procédure, surprises, HOLD et dégradations. Ne jamais promouvoir automatiquement.

## Ablations obligatoires (mêmes exemples, mêmes seeds, même budget)
- `BASELINE_NO_MEMORY` : aucun savoir expérientiel réutilisé.
- `FROZEN_MEMORY` : état acquis à la fin de TRAIN-A, sans correction ultérieure.
- `CUMULATIVE_MEMORY` : état éducatif cumulatif proposé.
- `NO_RECIPROCAL_RECONSTRUCTION` : prédiction spatiale sans moteur visuel réciproque.
Les résultats des méthodes sont reportés sur les **mêmes cas effectivement évalués** et avec les couvertures et HOLD séparés. Un gain issu seulement d'un algorithme programmé ou d'une mémoire de trajectoire spécifique n'est pas annoncé comme acquisition de physique.

## Frontière du professeur
TRAIN : les cibles peuvent être révélées **après** engagement de la tentative et consignées comme feedback. TEST : images futures, positions véritables, paramètres du simulateur servant d'oracle, barèmes et étiquettes de réponses doivent être inaccessibles au moteur élève jusqu'à l'engagement immuable. Le vérificateur est un processus logique distinct; aucune sortie de l'évaluateur ne revient dans l'examen en cours.

## Contrat d'épisode minimal
`episode_id, phase, split, source_sha256, observations_ref, available_until_t, checkpoint_before_sha256, method_ref, method_sha256, prediction_committed_at, predicted_state, predicted_image_sha256, evaluator_reveal_at, ground_truth_sha256, position_error_px, reconstruction_error, reference_frame, abstention_reason, learning_delta_ref, checkpoint_after_sha256, replay_verified`.

Les champs de note sont **absents/null** avant l'ouverture de l'évaluation. Les preuves portent leurs identifiants d'origine; une empreinte identique ne prouve pas deux observations indépendantes.

## Gates F1
- `G1_INTEGRITY` : refus d'altération mémoire, image ou journal.
- `G2_BLIND` : contrôle automatisé anti-fuite avant toute note.
- `G3_UNIFIED_E2E` : trois écoles utilisées pendant **une seule histoire éducative**; une exécution séparée de tests ne suffit pas.
- `G4_TRANSFER` : mesure aveugle sur trajectoires inédites et variations définies avant le TEST.
- `G5_RETENTION` : checkpoint A restitué après interférence et reprise; mesurer gains et régressions.
- `G6_ATTRIBUTION` : comparer baseline/no-memory, frozen-memory et cumulative sur cas appariés et couverture.
- `G7_PROOF` : rejeu, sources, images comparatives, rapports et résultats négatifs archivés.

**F1_GREEN** est interdit tant que G1–G7 ne sont pas tous attestés par les artefacts du run. Un test d'intégrité PASS ou une excellente métrique synthétique ne suffit pas à prouver une compréhension physique, une généralisation 3D ou une école autonome.

## Arborescence de sortie attendue
```
build/f1-unified/<run_id>/
  manifest.json
  episodes.jsonl
  checkpoints/
  source_images/
  student_images/
  teacher_sealed/
  comparisons/
  metrics.json
  replay_report.json
```
Les vérités TEST restent dans `teacher_sealed` et ne sont ouvertes qu'au vérificateur après l'engagement.

## Raccords à réaliser
- Identifier les **chemins et APIs réels**, pas des noms déduits, de l'école continue V1, de P156 et de la génération réciproque V1 à la base `3037810`.
- Ajouter un adaptateur par composant sans modifier son algorithme, un orchestrateur local, des tests anti-fuite et un replay end-to-end.
- Conserver les expériences V0–V4.2, F3c/F4/F5/F6 et P2 en références; ne pas les reconstruire, ni modifier SENS, B8, Native Memory ou `main`.

**Verdict actuel :** `F0B_GREEN / F1_SPEC_READY / F1_E2E_NOT_TESTED`.
