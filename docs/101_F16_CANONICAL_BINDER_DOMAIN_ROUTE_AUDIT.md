# F16 — Audit du domaine et Binder canoniques avant intégration Brody Image

**Contexte :** F15B a exécuté le vrai Guard et le vrai Sigma via un domaine de diagnostic META, avec HOLD obligatoire ; cela ne certifie pas un domaine Brody Image.

Audit GitHub (dépôt `Eaubin08/obsidia-x108-proofs`) :
- `scripts/providers/brody_runtime_adapter_v1.py` : Brody est déjà un *provider* sans autorité, écriture mémoire, émission ACT ni mutation kernel.
- `docs/CG9_GLOBAL_PROVIDER_BINDER_V1.md` : le Binder enregistre des providers, **pas des domaines**.
- `sigma/contracts.py` : l'enum Domain du code audité ne contient pas `brody_image`.
- `periphery/sigma_bridge.py` : Bank, Trading, Ecom, GPS présents ; pas de route `run_brody_with_periphery` visible.
- `docs/runtime/POST_CG100_RUNTIME_INTEGRATION_TRUTH.md` : le cycle canonique R4–R7 refuse un domaine non pris en charge avant tout verdict et avant invocation du provider ; ne pas lui faire passer un test de domaine META pour une exécution Brody.

## Nouveau préflight F16
`fusion_f16_canonical_route_inventory_v0.py` inspecte **en lecture seule** les fichiers locaux, leurs SHA256 et les domaines enregistrés, signale tout écart et sauvegarde un rapport. Il ne crée pas de domaine fictif, n'appelle ni Guard ni Sigma, n'exécute ni provider ni action. Des tests unitaires exigent un refus quand les fichiers essentiels manquent.

### Commandes PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f16_canonical_route_inventory_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F16 invalide" }
py -m unittest discover -s tests -p "test_fusion_f16*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F16 échoués" }
py -m brody_world_physique.fusion_f16_canonical_route_inventory_v0 --obsidia-repo "C:\OBSIDIA_WORK\obsidia-x108-proofs" --out "build\fusion-f16-contract-audit-001"
if ($LASTEXITCODE -ne 0) { throw "Contrats F16 divergents : examiner le rapport" }
Get-Content "build\fusion-f16-contract-audit-001\report.json"
```

## Décision à prendre après ce contrôle
Soit Brody Image produit un `AgentResult` ou `ContextPacket` sans posséder de domaine d'action, et un domaine déjà inscrit exerce la gouvernance ; soit un nouveau domaine est véritablement nécessaire. Dans ce second cas, il faut un contrat, un DomainState, des agents, une agrégation, une route Binder et des tests de régression du *cycle canonique*, le tout dans **une branche Obsidia distincte**, sans contourner `is_supported_domain`. Garder les 1000 reçus F14 en régression. Ne pas inventer un ALLOW de confort ni faire passer un champ JSON pour une preuve d'authenticité.

Le préflight est **audit de présence/source**, non preuve de câblage ou de conformité runtime. Ne pas reporter PASS global avant la validation PC.
