# 77 — P2.12a : corrections gestuelles bornées (supervisées, posthoc)

STATUT : CODE_PUBLISHED / PC_TEST_PENDING / IMAGE_ONLY

La forge P2.12a tente cinq versions du même dessin composé depuis les gestes réellement mémorisés en P2.11b et transformés par P2.11c : position de base, gauche 2 px, droite 2 px, haut 2 px, bas 2 px. Chaque candidate PNG et son SHA256 sont produits **avant** l'ouverture de l'image de référence. Ensuite seulement, le banc compare chaque version à la cible et désigne a posteriori la moins mauvaise. Toutes les tentatives restent conservées, y compris les régressions. Si aucune candidate ne bat l'initiale, cette dernière reste le choix de référence.

**Limite fondamentale :** le choix de la meilleure correction utilise le score de la référence après révélation; ce n'est donc **pas encore un moteur autonome capable de choisir une correction sur TEST**. Pour en faire une compétence apprise, il faudra extraire une politique de corrections des essais TRAIN, la figer, puis la tester sans consultation de cible pendant le choix des gestes. Les références doivent être cohérentes avec les compositions demandées (audit P2.11e) ; un score sur une référence blanche contradictoire ne constitue pas une preuve d'échec de création.

Fichiers :
- `brody_world_physique/p212a_bounded_gesture_revision_v0.py`
- `tests/test_p212a_bounded_gesture_revision_v0.py`
- `docs/77_P212A_CORRECTION_GESTUELLE_BORNEE.md`

Validation sur Windows :
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p212a*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.12a échoués" }
```

Exemple sur des fichiers déjà préparés :
```powershell
py -m brody_world_physique.p212a_bounded_gesture_revision_v0 --memory "build\p211b-gestures.json" --layout "composition.json" --reference "REFERENCE_COHERENTE.png" --out "build\p212a-essai-001"
```
Le répertoire `--out` doit être absent. Le banc produit cinq PNG et un `report.json`. Aucun changement de main, aucune Native Memory, aucune promotion B8.

La phase suivante devra introduire une variante de moteur de dessin **sans mémoire** disposant des mêmes informations initiales, ainsi qu'un jeu TRAIN/TEST propre à la génération, avant toute affirmation de gain de généralisation.
