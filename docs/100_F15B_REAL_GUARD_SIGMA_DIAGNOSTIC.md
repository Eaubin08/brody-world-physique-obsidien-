# F15B — Diagnostic via vrais moteurs périphérie / GuardX108 / Sigma

Les contrats consultés dans `Eaubin08/obsidia-x108-proofs` confirment que `Domain` ne contient pas `BRODY_IMAGE` ; `periphery/sigma_bridge.py` ne possède pas de `run_brody_with_periphery`. F15B ne prétend donc **pas** certifier une chaîne Brody opérationnelle.

Le diagnostic lit la **chaîne F14 existante de 1 000 reçus**, réutilise le packet Brody F15, appelle réellement `_merge_periphery_into_aggregate`, `GuardX108().decide` et `apply_sigma` avec `ObsidiaSigmaMonitor`. Il utilise `Domain.META` uniquement pour le test négatif, avec confiance nulle et deux inconnues explicites `BRODY_DOMAIN_UNREGISTERED` et `BRODY_NO_VERIFIED_PROVENANCE`. Il n'exécute aucune action et ne modifie pas les dépôts Obsidia. Tout `ALLOW` détecté devient une anomalie bloquante.

Le résultat signale les vrais appels, le verdict Guard par cas, le traitement Sigma, l'absence de route Binder certifiée et la distinction entre diagnostic et exécution autorisée. Le banc est fail-closed : une réussite ne constitue pas une preuve de raccordement Brody.

## Commande Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f15b_real_guard_sigma_diagnostic_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F15B invalide" }
py -m unittest discover -s tests -p "test_fusion_f15b*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F15B échoués" }
py -m brody_world_physique.fusion_f15b_real_guard_sigma_diagnostic_v0 --f14-receipts "build\fusion-f14-multisource-001\receipts.jsonl" --obsidia-repo "C:\OBSIDIA_WORK\obsidia-x108-proofs" --out "build\fusion-f15b-real-001"
if ($LASTEXITCODE -ne 0) { throw "Diagnostic F15B échoué ou autorisation dangereuse" }
Get-Content "build\fusion-f15b-real-001\report.json"
```

La fermeture définitive exige de définir une route de domaine Brody validée dans l'architecture Obsidia après audit Binder et branche active. Ne pas transformer ce test META en domaine opérationnel.
