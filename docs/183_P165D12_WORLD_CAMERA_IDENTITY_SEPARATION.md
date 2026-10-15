# 183 — P165-D12 : monde / caméra / identité / image — découplage minimal

## Motif
Gate C D11: 120 examens exécutés, 60/120 trajectoires compatibles avant/après; saut 0/12, réapparitions sous occultation tardive/longue 0/12, swap et distracteurs 0/12. Certains noms de scènes D11 (camera_pan/target_swap) ne correspondent pas à une simulation physique suffisamment explicite. Ne pas faire passer ces résultats pour une preuve de compréhension d'objets réels.

## D12 initial
`brody_world_physique/world_camera_identity_p165d12.py` introduit des états latents distincts :
1. coordonnées de monde synthétique 1D `main_x` et `world_x_b`;
2. translation de caméra `camera_x`;
3. identité utilisée pour rendre la cible `rendered_main_identity`;
4. projection raster `main_x - camera_x`, en pixels;
5. visibilité via occultation et points de repère dans les images.

Familles initiales : OBJECT_MOVES, CAMERA_MOVES, COMPENSATED_MOTION, OCCLUSION, IDENTITY_SWAP, CROSSING. 12 graines × 6 familles = 72 épisodes. Seules les images sont transmises à `D6.infer()`. Les variables latentes et labels restent pour analyse **a posteriori**. D6 garde sa logique inchangée.

### Précautions épistémiques
D12 est encore un monde synthétique **1D projeté en raster 2D**, et non une simulation 3D, un simulateur de caméra complet ou une preuve de causalité physique. Les repères fixes sont visibles en pixels, mais D6 ne résout pas encore automatiquement l'ego-mouvement caméra. `IDENTITY_SWAP` bascule un identifiant de cible rendu et met en concurrence deux ellipses, mais cela n'est pas un test exhaustif de remplacement d'entité avec suivi d'identité stricte. Le score `same_path` est seulement une continuité de points projetés; pour une substitution, un score élevé serait même compatible avec une **fausse continuité d'identité**. Toute assertion `identity_proven` est interdite.

La représentation doit encore s'étendre à (x,y,z), profondeur, projection intrinsèque/extrinsèque, rotations, parallax, échelle des objets et occlusions par vraie géométrie. Pas de signaux Wi-Fi/CSI, radar, LiDAR, IR ou sources externes connectés.

## Run sur PC — PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }

py -m py_compile brody_world_physique/world_camera_identity_p165d12.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe D12 RED — STOP" }
py -m unittest discover -s tests -p "test_world_camera_identity_p165d12.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests D12 RED — STOP" }
py -m brody_world_physique.world_camera_identity_p165d12 --beam 8 --seeds 12 --out "build\brody-p165d12-world-camera-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne D12 RED — STOP" }
Get-Content "build\brody-p165d12-world-camera-001\MASTER_REPORT.json"
```

## Actions après résultats
- Lire les échecs en différenciant observation de position, hypothèse de continuité et identité.
- Construire des couples contrefactuels dont l'image est identique alors que l'état latent (caméra/objet) est différent, pour obliger un HOLD sans source extérieure.
- Avant toute nouvelle couche « world model », démontrer une équivalence de projection et la non-identifiabilité physique depuis l'image seule.
- Préserver le protocole de régression globale (dernier résultat PC : 653/653 PASS), et réexécuter après toute modification des modules.

Gouvernance `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY` ; branche expérimentale uniquement.

**Verdict:** `P165D12_MINIMAL_LATENT_SEPARATION_PUBLISHED / PC_VALIDATION_PENDING / TRUE_3D_AND_IDENTITY_UNPROVEN`.
