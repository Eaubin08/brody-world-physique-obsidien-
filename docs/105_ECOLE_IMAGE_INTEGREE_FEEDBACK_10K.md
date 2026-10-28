# École intégrée Image : dessin → re-perception → contradiction → correction → reconstruction

Campagne expérimentale de 10 000 épisodes qui réutilise les 10 000 leçons / snapshot du banc de 20 000 déjà exécuté sur PC. Pas de nouveau modèle, de duplication de kernel ni d'écriture Native Memory.

Chaque épisode : outil choisi **avant** présentation de la cible, création d'une image, empreinte visuelle (pixels noirs, bbox et SHA256), comparaison à la cible après scellement, mesure d'écart, détection de contradiction et recherche supervisée du meilleur outil parmi les trois outils existants. Le résultat reconstruit est réévalué ; les transformations sont translation, symétrie miroir, rotation, contraste, flou, bruit, masquage, géométrie nouvelle, fausse consigne et contexte inconnu. Rapports par famille et reçus chaînés.

**Important :** la correction reçoit le référent et explore les trois outils. Un `after_loss=0` ne prouve pas une compréhension générative autonome. Le vérificateur est une mesure pixel, pas une rétine sémantique. Le modèle de choix demeure figé entre épisodes ; aucune preuve d'apprentissage continu ou de généralisation physique. Le benchmark indépendant précédent reste la référence de résistance hors correction.

### Commande PC (à exécuter en une fois)
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_integrated_feedback_school_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests infrastructure échoués" }
py -m brody_world_physique.image_integrated_feedback_school_v0 --snapshot "build\brody-image-school-20k-001\training\snapshot-010000.json" --cases 10000 --out "build\brody-image-integrated-10k-001"
if ($LASTEXITCODE -ne 0) { throw "École intégrée échouée" }
Get-Content "build\brody-image-integrated-10k-001\MASTER_REPORT.json"
```

Suite unique : dans ce même banc, raccorder les données images/vidéos réelles, un outil visuel réel vérifié, une boucle de correction inter-épisodes et un examen indépendant caché, avant toute revendication d'apprentissage du monde. La campagne actuelle ne prétend pas franchir ces étapes.
