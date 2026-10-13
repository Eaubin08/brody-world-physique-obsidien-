# P150 — Suivi sans voies imposées, caméra observée, hypothèses concurrentes

## Critique des campagnes précédentes

P149 a montré une erreur de 12 px en mouvement de caméra, une augmentation d'erreur lors des occultations et des prédictions parfaites artificiellement favorisées par les voies préassignées. P150 modifie **la représentation de perception et l'association temporelle**, plutôt que d'ajouter de nouvelles graines aux expériences identiques.

## Implémentation

- Détecte les taches rouges/bleues par composantes connexes **sur toute l'image**, sans utiliser des coordonnées de voies de déplacement connues.
- Récupère le déplacement apparent de caméra **uniquement à partir de trois repères verts dessinés dans les images**. L'inférence ne reçoit pas l'offset fourni par le générateur.
- Maintient jusqu'à six hypothèses concurrentes d'association objet↔observation ; estime les vitesses et attribue une pénalité au fait de perdre une observation. S'il existe deux hypothèses trop proches, l'algorithme **HOLD**.
- Prévoit le prochain centre de l'objet initialement situé le plus à gauche ; l'ID de vérité reste réservé à la correction, et la définition « initialement à gauche » est une convention d'évaluation, non une reconnaissance d'identité permanente.
- Évalue séparément couverture, erreur absolue moyenne et proportion à ±4 pixels, sur huit familles : mouvement distinct, croisement, superposition, occultation d'un objet, occultation des deux, caméra mobile, changement d'apparence, distracteur.

**Écart important :** la sélection par faisceau et le HOLD sont **des algorithmes programmés**, pas des lois physiques apprises. Les objets sont de petits disques 2D de couleurs contrôlées ; le segmentateur dépend toujours de seuils de couleur. Le suivi d'identité n'est pas prouvé, et le faisceau peut produire des refus en excès. Les occultations restent simplifiées. Il ne faut pas comparer les erreurs de P149 et P150 sans noter la modification de la génération, de la cible et des conditions d'observation.

## Run Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_tracking_beam_p150.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P150 échoués" }
py -m brody_world_physique.image_tracking_beam_p150 --minutes 15 --episodes-each 300 --out "build\brody-p150-tracking-001"
if ($LASTEXITCODE -ne 0) { throw "Run P150 échoué" }
Get-Content "build\brody-p150-tracking-001\MASTER_REPORT.json"
```

La limite est de 2400 épisodes ou 15 minutes, selon la première atteinte. Chaque épisode contient neuf images dont huit sont observées, avec des images de contrôle sous `examples/` et le registre `EXAMS.jsonl`. Aucun temps de calcul artificiellement prolongé.

**À analyser en priorité :** le taux de HOLD par scénario ; l'erreur du suivi de caméra sur les cas répondus ; le cas de superposition et les erreurs d'association. Les résultats de P150 doivent déterminer si P151 doit privilégier l'apprentissage de représentation, la gestion probabiliste des hypothèses ou la vidéo réelle.

Gouvernance préservée : `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
