# 67 — P2.10a : contrat exécutable de boucle visuelle réversible

STATUS: CODE_PUBLISHED / PC_TEST_PENDING / SUPERVISED_ONLY

## But
Lancer la forge de la génération et correction d'image en traçant une tentative existante, pas en reconstruisant un moteur de synthèse. La source est la référence immuable; l'image initiale et une candidate sont déjà produites par un outil extérieur **avant** le score. Le résultat peut être `ACCEPTED`, `ROLLED_BACK`, ou `HOLD_EQUAL`. Un rollback ne détruit pas la tentative: sa valeur d'erreur et son empreinte restent dans le journal. Le script n'écrit jamais dans la mémoire native.

## Implémentation et fichiers
- `brody_world_physique/p210a_visual_loop_contract_v0.py`: `evaluate`, `verify`, format `BRODY_P210A_VISUAL_LOOP_V0`, hash SHA256 des 3 images, comptage des pixels RGBA différents, verdict et chemin vers la meilleure version.
- `tests/test_p210a_visual_loop_contract_v0.py`: 5 tests d'acceptation/rollback/HOLD/falsification/bornes.
- Docs de suite: `docs/66_P210_PLAN_FORGE_BOUCLES_GENERATION_IMAGE.md`.

Le suivi versionné est à ce stade **un essai unique**, sans vrai sélecteur de méthodes ni score régional, sans génération automatique. `max_attempts` borne le contrat d'appel (1..64) mais le moteur ne boucle pas encore automatiquement; demander davantage ne déclenche pas de nouvelles étapes. La référence visible au score signifie apprentissage **supervisé**, pas génération autonome. Les chemins d'images et leur empreinte sont vérifiés sur rejeu; si le fichier image a été modifié, le rejeu échoue.

## Tests PC — branche expérimentale
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p210a*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.10a échoués" }
```

## Essai avec 3 images sources existantes
La commande n'est exécutable qu'avec trois chemins PNG de mêmes dimensions; `--initial` est une production initiale et `--candidate` une autre production **faite avant** le contrôle. Ne pas donner la source comme candidate: cela donnerait artificiellement zéro erreur.

```powershell
py -m brody_world_physique.p210a_visual_loop_contract_v0 --source "CHEMIN_SOURCE.png" --initial "CHEMIN_IMAGE_INITIALE.png" --candidate "CHEMIN_CORRECTION.png" --out "build\p210a-premier-essai.json"
py -m brody_world_physique.p210a_visual_loop_contract_v0 --out "build\p210a-premier-essai.json" --verify
```

## Conditions de passage à b / c
1. 5/5 unit tests Windows sur les PNG effectifs.
2. Rejeu et source hash vérifiés.
3. Une correction vraie améliorante ET une dégradante testées, avec rollback.
4. P2.10b ajoute métriques par région/objet et taxonomie; P2.10c branchera `reverso_learning_v0`, `image_v0` et `drawing_school_v1` pour **générer réellement** la candidate.
5. Pas d'affirmation d'apprentissage transférable avant l'examen P2.10e sur des images nouvelles.
