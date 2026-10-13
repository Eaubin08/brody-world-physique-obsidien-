# Brody P144 — Routage sans connaissance de la transformation

## Hypothèse testée

P143 a obtenu 85,12 % de bonnes réponses sur 30 000 examens et une couverture de 96,67 %, mais recevait **le nom de la transformation**. P144 n'utilise plus ce nom pour sélectionner RGB, géométrie ou majorité en phase d'examen. Elle exploite plutôt les statistiques de l'image observée et un historique de validation distinct. Elle connaît toujours **la question posée** (forme, couleur, quantité, disposition, orientation).

### Protocole

- Cours : images synthétiques non transformées avec variation de difficulté, entraînement RGB et géométrique.
- Validation : images avec six transformations, calcul des succès par représentation et stockage du contexte visuel ; ce corpus construit le routeur.
- Examen : nouveau flux de graines ; à chaque image, le routeur sélectionne un modèle à partir du contexte visuel, sans recevoir la transformation et sans observer l'étiquette cible.
- Contre-factuel : le programme évalue aussi un routeur informé des conditions (issu de la validation) pour mesurer le prix de l'ignorance de la transformation.
- Les images réellement achromatiques peuvent conduire à HOLD pour une question portant sur la couleur. Cette règle est programmée, non apprise.
- Rapport : `CELL_REPORT.json` conserve les résultats par condition ; `MASTER_REPORT.json` résume accuracy du routeur aveugle, accuracy du comparateur informé, couverture et durée.

**Limites importantes :** le nom de la transformation reste disponible *pour organiser les fichiers d'examen et le comparateur*, mais il n'est pas transmis à la fonction `pick_router`. Les étiquettes de question restent connues. Toutes les scènes viennent du même générateur procédural. Ce n'est ni de l'exploration physique, ni du 360° réel, ni une preuve d'intelligence générale.

## Test PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_blind_router_p144.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P144 échoués" }
py -m brody_world_physique.image_blind_router_p144 --minutes 15 --train-per-family 300 --validation-per-condition 100 --exam-per-condition 1000 --out "build\brody-p144-blind-router-001"
if ($LASTEXITCODE -ne 0) { throw "Examen P144 échoué" }
Get-Content "build\brody-p144-blind-router-001\MASTER_REPORT.json"
```

P144 est un test de transfert de routage, pas un nouveau savoir physique. **Si le routeur aveugle est inférieur au routeur informé, c'est une information utile à conserver, pas une erreur à masquer.** Une itération future devra varier le générateur et mesurer les sources externes indépendantes.
