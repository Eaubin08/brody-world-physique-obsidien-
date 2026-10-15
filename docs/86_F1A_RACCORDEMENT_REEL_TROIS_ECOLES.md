# 86 — F1A : raccordement réel des trois écoles F0-B

**Implémentation :** `brody_world_physique/f1a_three_school_wiring_v1.py`  
**Tests :** `tests/test_f1a_three_school_wiring_v1.py`  
**État :** publié, exécution du run unifié non constatée. `F1_GREEN=FALSE`.

## Interfaces exactes constatées dans le code
- `image_unified_continuous_school_v1.curriculum(root, labels_path)`, `learn(root, labels, out, previous=None, max_new=None)` et `exam(state_path, images, out)` : mémoire d'identités locales et examen aveugle.
- `image_cumulative_education_p156.run(out, minutes=20, seed=156, lessons_each=24, feedback_each=24, validation_each=24, exam_each=50, retention_tolerance=.035)` : apprentissage cumulatif de lois synthétiques, sans objet physique partagé avec l'école d'images.
- `image_reciprocal_generation_school_v1.encode_training(lesson_file, out)`, `reconstruct(memory_path, out)` et `assess(memory_path, exam_dir, out)` : prototypes d'images RGB 4×4 (rendus 64×64).

## F1A est une intégration de preuves, pas une éducation physique unifiée
Le harness fait tourner les **vraies fonctions** sur un même ensemble de sources visuelles pour l'école continue et la reconstruction réciproque. Il exécute ensuite P156 avec sa propre campagne synthétique. Les mémoires restent séparées. Aucune loi de mouvement apprise dans P156 n'est réutilisée par l'école visuelle, et les prédictions de balle ne sont pas encore connectées. Ce résultat ne permettra **pas** de déclarer `F1_UNIFIED_EDUCATION_EXPERIMENT=GREEN`.

Le manifest conserve les empreintes TRAIN et TEST ; une image identique dans les deux ensembles est refusée. Les trois moteurs restent sans écriture dans Native Memory et sans promotion canonique.

## Commandes PowerShell PC fixe
Dans le dépôt, sur `exp/p2-multirepresentation-ablation-20261009` :

```powershell
git branch --show-current
git pull --ff-only
py -m unittest tests.test_f1a_three_school_wiring_v1 -v
```

Créer au préalable deux dossiers distincts `train_images` et `test_images` contenant des images locales autorisées, ainsi qu'un fichier `labels.json` qui associe **les noms relatifs des fichiers TRAIN** à l'identité enseignée. Exemple :

```json
{
  "balle_01.png": "balle",
  "balle_02.png": "balle"
}
```

Exécuter, en remplaçant les chemins par les chemins réels :

```powershell
py -m brody_world_physique.f1a_three_school_wiring_v1 --train "CHEMIN_TRAIN" --labels "CHEMIN_LABELS_JSON" --test "CHEMIN_TEST" --out "build/f1a-first-local"
```

**Important :** le répertoire de sortie doit être absent. Le programme ne réutilise ni n'efface un ancien rapport. Conserver `MASTER_REPORT.json`, `INPUT_MANIFEST.json`, les sous-répertoires d'examen et les PNG générés.

## Prochain verrou — F1B
Construire une interface commune **état temporel visuel / prédiction de balle / reconstruction de frame** avec engagement aveugle de la prédiction. Puis tester T0 → TRAIN-A → T1 → autre compétence → pause/reprise → T2, en comparant les mêmes images avec et sans expérience. Ne pas utiliser les scores P156 comme preuve de progrès sur les pixels de la balle.

**Statut :** `F1A_CODE_PUBLISHED / F1A_RUN_UNVERIFIED / F1_E2E_NOT_TESTED`.
