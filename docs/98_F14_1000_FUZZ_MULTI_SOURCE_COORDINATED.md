# F14 — 1 000 essais de fuzzing multi-source et spoofing coordonné

Publication sur branche expérimentale uniquement. F14 prolonge F13 en ajoutant une matrice de 10 attaques : observations propres à 2 et 3 sources, une source falsifiée, deux sources falsifiées, contradiction, preuve absente, preuve périmée, deux canaux partageant la même origine, falsification de toutes les sources et contexte absent.

Séparation explicite : observation brute, ID de canal, ID d'origine indépendant, fraîcheur temporelle, attestation du banc, proposition corroborée ou HOLD, reçu. Aucune majorité n'écrase une contradiction entre origines admises. Les preuves données au garde sont synthétiques, non signées. L'attaque `all_spoof` doit **montrer l'échec** d'une corroboration trompée par deux sources conjointement falsifiées : ne jamais maquiller ce résultat en succès de sécurité.

Mesures : faux positifs (fausses acceptations), acceptations correctes et HOLD par famille ; 1000 reçus chaînés SHA256, comparaison possible à F13. Aucun TRAIN, aucune mutation Native Memory, aucune promotion automatique, `KX108_ONLY`. Ce banc est une simulation de la logique de confiance, pas une preuve de sécurité réelle ni un raccordement aux capteurs d'Obsidia.

## Commandes Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f14_multisource_fuzz_1000_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F14 invalide" }
py -m unittest discover -s tests -p "test_fusion_f14*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F14 échoués" }
py -m brody_world_physique.fusion_f14_multisource_fuzz_1000_v0 --cases 1000 --out "build\fusion-f14-multisource-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne échouée" }
$r=Get-Content "build\fusion-f14-multisource-001\report.json" -Raw | ConvertFrom-Json
$r | Select-Object cases,accepted_correct,accepted_wrong,held
$r.by_family | Format-List
```
