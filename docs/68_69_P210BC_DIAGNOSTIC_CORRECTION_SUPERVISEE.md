# 68–69 — P2.10b/c : analyse régionale et première correction PNG

STATUS: CODE_PUBLISHED / PC_TEST_PENDING / SUPERVISED_DEMO

## Modules
- `brody_world_physique/p210b_visual_error_atlas_v0.py` : compare image source, image candidate et masque d'objet. Compte séparément pixels erronés de l'objet, du fond et de la région protégée; refuse les masques objet/protection qui se recouvrent. `error_type=UNKNOWN` est intentionnel : les causes POSITION/SHAPE/PROPORTION/COLOR ne peuvent pas être inférées de simples différences binaires, sans caractérisation supplémentaire.
- `brody_world_physique/p210c_targeted_image_correction_v0.py` : corrige **une zone** avec `Image.composite(source,initial,mask)`, écrit `candidate.png` et `candidate.json`. Un score supervisé choisit la meilleure version; le rejeu contrôle image, masques, reçus et immutabilité des entrées. Les pixels hors masque ne sont pas modifiés, mais l'image source sert d'oracle pour la zone traitée.
- `tests/test_p210bc_visual_correction_v0.py` : quatre tests dédiés aux erreurs par région, masque protégé, égalité HOLD, falsification et erreurs d'entrées.

## Sens des résultats
Une correction qui recopie un fragment **visible de la source** n'est **pas un apprentissage**, ni une génération autonome. C'est un premier test de l'infrastructure de correction locale, du contrôle de fidélité et de la provenance. Le futur P2.10d devra mémoriser la procédure, le contexte et les erreurs. P2.10e devra mesurer son transfert sur une source réellement nouvelle sans lui offrir ses pixels cibles pendant la génération.

## Instructions PC fixe
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p210bc*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.10b/c échoués" }
```

## Essai avec trois PNG locaux de même taille
L'image source, l'image initiale, et un masque en noir et blanc (blanc = région autorisée à corriger) doivent exister. Utiliser des chemins distincts et un nouveau nom de sortie.
```powershell
py -m brody_world_physique.p210c_targeted_image_correction_v0 --source "CHEMIN_SOURCE.png" --initial "CHEMIN_INITIALE.png" --mask "CHEMIN_MASQUE.png" --out "build\p210c-apres.png"
py -m brody_world_physique.p210c_targeted_image_correction_v0 --source "CHEMIN_SOURCE.png" --initial "CHEMIN_INITIALE.png" --mask "CHEMIN_MASQUE.png" --out "build\p210c-apres.png" --verify
```

## Prochain seuil
Ne pas qualifier le résultat d'« apprentissage image » tant qu'un correcteur ne propose pas lui-même le geste depuis une représentation non triviale (Reverso/école de dessin), avec engagement avant retour de référence et test hors distribution. La phase b/c est une **base vérifiable de traitement d'erreur**. Aucune modification de main, Native Memory ou SENS.
