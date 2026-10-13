# Image : galerie visuelle des différences (archives Brody)

Nouvelle campagne sur les 63 PNG déjà extraits dans `build\\brody-images-ready`. Cinq variantes pour chaque source : originale, miroir, rotation, flou, contraste. Chaque cas écrit une planche PNG de quatre panneaux : référence, première tentative (PENCIL fixe), meilleure correction parmi les trois outils simulés et différence visuelle amplifiée ×3. Le journal JSONL chaîné contient les hash SHA256 et les métriques avant/après, sans modifier les preuves des campagnes précédentes.

**Portée :** Première tentative figée = PENCIL, ce n'est pas une décision de politique apprise. Correction = sélection supervisée après comparaison à la référence visible, ce n'est pas une génération libre ni une prédiction aveugle. Dessins archivés du projet, provenance sensorielle non attestée. Le modèle ne comprend pas encore les objets ni la physique.

## PC Windows — lancer le test et ouvrir les images
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_external_visual_gallery_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
if (-not (Test-Path "build\brody-images-ready\image_0001.png")) { throw "Images absentes du dossier build\brody-images-ready" }
py -m brody_world_physique.image_external_visual_gallery_v0 --images "build\brody-images-ready" --out "build\brody-external-gallery-315-001"
if ($LASTEXITCODE -ne 0) { throw "Galerie échouée" }
Get-Content "build\brody-external-gallery-315-001\MASTER_REPORT.json"
explorer "build\brody-external-gallery-315-001\gallery"
```

Suite : trier les plus grands écarts et les HOLD, choisir de nouvelles sources vraiment indépendantes, puis construire une évaluation perceptive et générative distincte du correcteur à référence visible.
