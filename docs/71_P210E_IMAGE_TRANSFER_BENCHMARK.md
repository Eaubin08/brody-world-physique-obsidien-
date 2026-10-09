# 71 — P2.10e : examen de transfert visuel TRAIN -> TEST

STATUT : CODE_PUBLISHED / PC_TEST_PENDING / FROZEN_GEOMETRIC_BASELINE_ONLY

## Question mesurable
Une procédure dérivée de plusieurs **images d'apprentissage** peut-elle améliorer une **image différente** sans lire les pixels de sa cible avant de produire la candidate ?

## Ce qui a réellement été codé
`brody_world_physique/p210e_visual_transfer_benchmark_v0.py` mesure un transfert **très restreint** : une translation entière (dx,dy), déterminée avec les centres du premier plan sombre de couples TRAIN `initial/reference`. Si les corrections TRAIN ne sont pas identiques, l'étape refuse le transfert. La méthode choisie est figée pour toute la suite TEST. Pour chaque image de TEST, la candidate est générée et son SHA256 conservé avant l'utilisation de l'image `reference` pour scorer le résultat. Une erreur qui s'aggrave est enregistrée, pas effacée.

Le transfert ne sait pas encore reconstruire une image complexe, sélectionner une méthode issue de P2.10d, effectuer Reverso, reconnaître des objets, généraliser à la perspective ou aux textures. Il sert de **premier contrôle technique de transfert de procédé** sans pixels source copiés depuis la cible TEST; il ne démontre pas la compréhension visuelle de Brody.

## API
Manifeste JSON :
```json
{
  "schema": "BRODY_P210E_INPUT_V0",
  "train": [
    {"initial": "chemin_train_avant.png", "reference": "chemin_train_apres.png"}
  ],
  "test": [
    {"initial": "chemin_test_avant.png", "reference": "chemin_test_reference_cachee.png"}
  ]
}
```
Les fichiers doivent exister et être de mêmes dimensions au sein de chaque paire. La cible TEST n'est ouverte qu'au moment de l'évaluation. L'algorithme est une baseline « silhouette sombre sur fond clair », pas un générateur photo.

Exécution :
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p210e*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.10e échoués" }
```
Puis, seulement avec un manifeste préparé à l'avance :
```powershell
py -m brody_world_physique.p210e_visual_transfer_benchmark_v0 --manifest "CHEMIN_MANIFESTE.json" --out "build\p210e-report.json"
```

## Limites et suites
- Les tests unitaires contrôlent des figures simples créées localement. La seule augmentation mesurée est un transfert d'offset, pas un résultat expérimental général.
- `test_feedback_used_for_learning=False` empêche seulement l'utilisation des scores TEST dans `learn_offset`. Une vraie preuve de précommit indépendant exigera une séparation et des empreintes contrôlées de manière externe.
- Avant de conclure à un apprentissage Brody Image : connecter les gestes Reverso/école de dessin et le ledger P2.10d comme **entrée réelle de choix**, produire des PNG sans référence, ablater les méthodes et comparer sur des images inédites variées, sans glisser vers un score de balle.
- Aucune écriture Native Memory, aucun accès à KX108 pour autorisation d'action, aucune modification de `main`.
