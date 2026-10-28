# École Image Brody — identité enseignée et transfert entre vues V0

Un professeur peut regrouper explicitement les observations d'un même exemple sous une identité candidate. Le moteur extrait des parties visibles et des relations à partir des pixels, apprend les contextes de la vue d'origine et de son miroir, puis examine séparément les vues tournées de 90 et 180 degrés. Chaque observation peut changer de structure, tandis que l'identité **assignée par le professeur** demeure attachée au groupe.

**Ce que cela mesure :** une correspondance de signatures structurelles déjà vues versus des rotations retenues hors cours. Les groupes sont déclarés, non reconnus automatiquement. L'image demeure en 64×64 gris ; ceci n'est ni une vision 360° vraie, ni une inférence d'objet tridimensionnel, ni une généralisation à des objets inconnus. Un contexte identique ne prouve pas la même identité, et un contexte différent ne la réfute pas. Les identités ne sont pas automatiquement fusionnées avec la mémoire stable V1 ; ce raccordement est l'étape suivante. Aucune écriture Native Memory ni promotion canonique.

## PC : essai sur une image archive

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_multiview_identity_school_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
$image = Get-ChildItem "build\brody-images-ready" -File -Filter *.png | Select-Object -First 1
if (-not $image) { throw "Aucune image d'entrée" }
$manifest = @(@{identity="exemple-archive-01";examples=@($image.FullName)}) | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText((Join-Path (Get-Location) "build\brody-multiview-manifest.json"),$manifest,(New-Object System.Text.UTF8Encoding($false)))
py -m brody_world_physique.image_multiview_identity_school_v0 --manifest "build\brody-multiview-manifest.json" --out "build\brody-multiview-001"
if ($LASTEXITCODE -ne 0) { throw "Examen multi-vues échoué" }
Get-Content "build\brody-multiview-001\MASTER_REPORT.json"
```

Ne pas appeler un groupe « balle », « voiture », etc. sans cours ou métadonnées fiables. Prochaine intégration : graphe local de savoir (identité candidate ↔ observations ↔ transformations ↔ invariants conditionnels ↔ leçons ↔ contradictions), détection des nouvelles perspectives et doute ciblé, couleurs et images externes distinctes, recherche de données/professeurs autorisés et validation inter-runs. Le nombre d'examens seul ne constitue pas un apprentissage.
