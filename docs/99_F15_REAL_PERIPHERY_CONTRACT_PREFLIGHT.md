# F15 — Réconciliation Brody ↔ Périphérie Obsidia : contrat réel, pas autorité fictive

## Résultat de l'audit GitHub
Dépôt `Eaubin08/obsidia-x108-proofs` :
- `periphery/common.py` expose `PeripheralSignalPacket`, les champs `unknowns`, `contradictions`, `risk_flags`, `evidence_refs`, `recommended_gate` et l'invariant `can_emit_act=False`.
- `periphery/sigma_bridge.py` agrège ces signaux aux domaines Bank/Trading/Ecom/GPS et appelle GuardX108. **Il n'existe pas de branche Brody Image dans ce bridge consulté.**
- `sigma/run_pipeline.py` contient `apply_sigma` après Guard ; `P56D` impose `SIGMA_POST_GUARD_VETO_ONLY`.
- Donc il serait faux de déclarer une évaluation Guard + Sigma de Brody fonctionnelle simplement en sérialisant un paquet.

## Ce que fait F15
Lit les reçus F14 existants, en vérifie la chaîne SHA256, produit les vrais champs du paquet périphérique et instancie la vraie classe `PeripheralSignalPacket` **depuis une copie locale distincte d'Obsidia**. Ne transforme pas une attestation synthétique en confiance vérifiée. Les cas de spoofing coordonné sont tracés comme risques. Tout packet reste `HOLD`, non souverain. Aucun appel Guard ou Sigma : la sortie mentionne explicitement `real_guard_invoked=false` et `real_sigma_invoked=false`.

Il s'agit d'un premier **préflight de contrat**, et non d'une véritable fermeture de F15. L'intégration demandera un `DomainState` Brody conforme et une route Binder/Meta/Guard/Sigma gouvernée dans Obsidia, après audit de la branche active et autorisation distincte de modifier son dépôt. Ne pas toucher Sigma, Guard, main ou Native Memory.

## Sur PC — test de contrat + réutilisation des 1 000 reçus F14

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f15_periphery_contract_bridge_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F15 incorrecte" }
py -m unittest discover -s tests -p "test_fusion_f15*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F15 échoués" }

# Remplacer ce chemin uniquement si le dépôt Obsidia réel est ailleurs.
$obsidia = "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\obsidia-x108-proofs"
if (!(Test-Path "$obsidia\periphery\common.py")) { throw "Chemin du dépôt Obsidia à préciser : $obsidia" }

py -m brody_world_physique.fusion_f15_periphery_contract_bridge_v0 --f14-receipts "build\fusion-f14-multisource-001\receipts.jsonl" --obsidia-repo "$obsidia" --out "build\fusion-f15-periphery-contract-001"
if ($LASTEXITCODE -ne 0) { throw "Audit de contrat F15 échoué" }
Get-Content "build\fusion-f15-periphery-contract-001\report.json"
```

Les 1 000 attaques ne sont pas relancées : ce sont **les mêmes 1 000 preuves F14** qui sont confrontées au contrat périphérique réel, sans apprentissage à partir des examens.
