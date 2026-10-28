# École Image — première campagne sur des images externes au simulateur instrumental

Cette campagne introduit des fichiers PNG/JPG/BMP/WEBP que le laboratoire des trois outils de dessin n'a pas générés. On réutilise la réduction à 64×64 et le tracé générique `suggest_gestures_from_reference` déjà présent dans l'école dessin, puis on produit et mesure une reconstruction instrumentale. Chaque source est examinée à l'identique, en miroir, rotation 90°, flou et contraste : cinq évaluations par fichier.

**Entrée externe ≠ preuve de capteur réel.** Le programme ne télécharge pas d'images et ne prétend pas que les fichiers viennent d'une caméra indépendante ou que leurs licences et provenances ont été certifiées. L'opérateur sélectionne de vrais fichiers distincts des sorties du générateur d'instruments. Les chemins et empreintes SHA256 sont consignés dans le journal local, jamais poussés vers GitHub.

**Limites objectives :** l'examen voit le référent pour proposer un tracé et évaluer les trois outils, donc il mesure reconstruction supervisée, pas génération aveugle. Les images couleur sont réduites en niveaux de gris 64×64. La sémantique, la causalité physique, la profondeur et l'apprentissage permanent ne sont pas évalués par ce code. Les scènes inconnues ou qui ne fournissent pas de traits traçables sont explicitement consignées comme HOLD.

## Exécution
Mettre quelques images PNG/JPG personnelles, dessins scannés ou photos dans `assets\\external-image-exam` (dossier uniquement local, ne pas committer les fichiers).

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_external_source_school_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests infrastructure échoués" }
New-Item -ItemType Directory -Force "assets\external-image-exam" | Out-Null
if (-not (Get-ChildItem "assets\external-image-exam" -File -ErrorAction SilentlyContinue)) { Write-Host "Ajoute tes PNG/JPG dans assets\external-image-exam puis relance uniquement la commande ci-dessous."; return }
py -m brody_world_physique.image_external_source_school_v0 --images "assets\external-image-exam" --out "build\brody-external-images-001"
if ($LASTEXITCODE -ne 0) { throw "Examen d'images externes échoué" }
Get-Content "build\brody-external-images-001\MASTER_REPORT.json"
```

**Vers l'étape produit :** passer de tracing 64×64 à observation non supervisée via le Qwen-VL local de Jarvis et à la reconstruction/image générée, avec jeux de données à provenance établie, comparaison de plusieurs vues d'un même objet, et un examinateur indépendant du moteur candidat. La présente campagne n'est que l'entrée de fichiers indépendants du générateur de l'école.
