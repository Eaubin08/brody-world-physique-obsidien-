# F17 — Câblage cognitif Brody vers runtime canonique (dry-run)

Audit réalisé sur `Eaubin08/obsidia-x108-proofs` :
- `periphery/agent_contracts.py` définit `AgentResult` / `AgentLayer.PROVENANCE`.
- `periphery/context/agent_result_context_adapter.py` contient `agent_result_to_context_packet`.
- `periphery/context/agent_x108_context_flow.py` contient `admit_agent_context`, lequel applique les validations de contexte puis le **stub d'admission X108 dry-run**.
- Ce chemin **ne signifie ni GuardX108 souverain ni Sigma**, et ne certifie pas une route Binder/action du domaine brody_image.

Le code F17 convertit les 1000 paquets F15 en authentiques `AgentResult` puis `ContextPacket` et appelle l'admission de contexte *du dépôt local Obsidia*. Chaque cas est critique, non souverain ; toute réponse `ALLOW_CONTEXT_ONLY` inattendue pour ces preuves synthétiques non attestées fait échouer le rejeu. `HOLD` n'équivaut pas à un apprentissage validé. Aucun provider invoqué, aucun domaine déclaré, aucun write mémoire, aucune modification kernel.

## PC Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f17_agent_context_dryrun_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F17 invalide" }
py -m unittest discover -s tests -p "test_fusion_f17*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F17 échoués" }
py -m brody_world_physique.fusion_f17_agent_context_dryrun_v0 --f15-packets "build\fusion-f15-periphery-contract-001\periphery_packets.jsonl" --obsidia-repo "C:\OBSIDIA_WORK\obsidia-x108-proofs" --out "build\fusion-f17-agent-context-001"
if ($LASTEXITCODE -ne 0) { throw "F17 échoué" }
Get-Content "build\fusion-f17-agent-context-001\report.json"
```

Si F17 bloque sur un contrat runtime ou sur l'admission, rapporter la trace complète, ne pas autoriser artificiellement. La prochaine phase devra mesurer une voie de confiance vérifiée et une route de domaine supportée, pas seulement les HOLD.
