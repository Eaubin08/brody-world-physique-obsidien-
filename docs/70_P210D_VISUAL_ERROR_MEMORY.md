# 70 — P2.10d : mémoire candidate des corrections visuelles

STATUT : CODE_PUBLISHED / PC_TEST_PENDING / IMAGE_ONLY / NON_AUTONOMOUS

## Contrat effectif
Le module `brody_world_physique/p210d_visual_error_memory_bridge_v0.py` conserve localement le contexte et le résultat d'une correction P2.10c vérifiée. Il mémorise source, tentative initiale, masque, PNG généré, fichier reçu, hash SHA256 des artefacts, erreurs avant/après, méthode déclarée, verdict et lien cryptographique avec l'essai précédent. Il conserve aussi les essais `HOLD_EQUAL`, pas seulement les améliorations. Aucun savoir n'est automatiquement promu; aucune écriture Native Memory.

Le ledger est un fichier JSON réécrit atomiquement **non garanti** : la chaîne de hashes détecte la modification interne d'un épisode sans réécriture des liens, mais ne garantit pas à elle seule qu'un adversaire ne remplacera pas toute la chaîne. Une version ultérieure devra ajouter une racine de confiance externe et une écriture résistante aux interruptions.

## Ce que P2.10d ne sait pas faire
- Ne sélectionne pas encore des gestes Reverso pour une nouvelle image.
- Ne produit pas de correction : il archive et vérifie les tentatives réellement exécutées par P2.10c.
- N'effectue pas de test de transfert P2.10e et n'entraîne pas de modèle.
- P2.10c utilise les pixels de référence; un `ROLLED_BACK` par dégradation de qualité **ne peut pas être observé avec son opérateur de substitution actuel**, qui remplace uniquement des pixels par ceux de la vérité. L'API du journal accepte ce verdict si un correcteur futur le produit et le démontre; la preuve de rollback de P2.10a reste séparée.

## Commandes PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p210d*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.10d échoués" }
```

Après une correction P2.10c réelle, remplacer les chemins :
```powershell
py -m brody_world_physique.p210d_visual_error_memory_bridge_v0 --ledger "build\p210d-ledger.json" --source "SOURCE.png" --initial "INITIAL.png" --mask "MASK.png" --candidate "build\p210c-apres.png"
py -m brody_world_physique.p210d_visual_error_memory_bridge_v0 --ledger "build\p210d-ledger.json" --verify
```

## Prochain verrou scientifique
Pour P2.10e : figer entraînement/candidatures, transférer **uniquement des gestes/paramètres déjà appris** à de nouvelles sources, engagement avant accès à l'image cible, mesure du gain contre baselines sur cas appariés. Copier les pixels de la nouvelle source n'est pas un transfert d'apprentissage.
