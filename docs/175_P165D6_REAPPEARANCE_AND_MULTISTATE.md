# 175 — P165-D6 : contrôle de réapparition, pistes persistantes concurrentes

## Origine du verrou
P165-D5 : 1350 examens, top-k quatre points 1242/1350 (92 %), mais seulement 342/450 sur occultation totale. Le seuil de quatre images correctes pouvait masquer un échec d'identité au moment de la réapparition. Il fallait dissocier le rappel avant occultation, le rappel après, et la continuité dans **une même piste**.

## Implémentation publiée
`brody_world_physique/reappearance_gate_p165d6.py` importe l'extraction visuelle P165-D3 via `associate` P165-D5, puis propage chaque chemin de son beam borné via `state_from_path` P165-D4. La vérité demeure exclusivement réservée à l'évaluation, jamais passée à `infer(frames,beam)`.

Les scores sont explicitement différents :
- `pre_visible_recall` : au moins deux localisations correctes dans les frames 0,1,2 sur une piste ;
- `post_reappearance_recall` : deux localisations correctes en frames 5,6 sur une piste ;
- `same_path_pre_post_recall` : ces deux conditions **sur une seule et même piste** ;
- `topk_four_frame_recall` : ancien seuil compatible avec D5 pour constater les divergences.

La même piste qui est bonne avant et après n'est PAS pour autant la preuve de la même identité physique : le simulateur expose une cible par ses centres, la scène contient des distracteurs, et les signatures/capteurs/contextes ne tranchent pas encore la réidentification. Les hypothèses D4 sont en coordonnées d'image 1D synthétiques, sans calibration monde/caméra. Les dates sont des indices de frames, pas des timestamps réels.

## Design des examens
Même génération, mêmes graines et même facteur 675×2 que D5. Épreuve comparative appariée, sortie `EXAMS.jsonl` et `MASTER_REPORT.json` dans un dossier inédit. Chaque cas enregistre le verdict du tracker, les pistes, les états persistants, les scores et l'oracle réservé à la notation. Aucun fichier précédent écrasé.

## Limites / prochaine vraie intégration
P165-D6 n'utilise toujours pas directement le graphe contextuel P165-C ni les signatures multimodales P165-B ; aucun Wi-Fi/CSI, radio, radar, thermique ou LiDAR réel n'est capté. Propager huit pistes améliore l'honnêteté du suivi mais peut propager huit erreurs. Un bon `same_path_pre_post` ne prouve ni identité, ni causalité du phénomène pendant occultation. Le prochain contrôle doit appliquer des signatures **observées et synchronisées**, construire un graphe de visibilité depuis pixels et vérifier la calibration des coordonnées et les objectifs.

## Windows PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/reappearance_gate_p165d6.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P165-D6 échouée" }
py -m unittest discover -s tests -p "test_reappearance_gate_p165d6.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P165-D6 échoués — STOP" }
py -m brody_world_physique.reappearance_gate_p165d6 --seeds 2 --beam 8 --out "build\brody-p165d6-reappearance-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P165-D6 échouée" }
Get-Content "build\brody-p165d6-reappearance-001\MASTER_REPORT.json"
```

Gouvernance : `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

**Avant run :** `P165D6_CODE_PUBLISHED / REAPPEARANCE_SCORING_PUBLISHED / ALL_BEAM_STATES_PROPAGATED / PC_VALIDATION_PENDING / REAL_IDENTITY_UNPROVEN`.
