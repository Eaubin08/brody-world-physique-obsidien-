# 174 — P165-D5 : liaison perception raster → hypothèses temporelles → état persistant

**Statut : code publié, validation PC en attente.**

## Contrat
Le nouveau module `image_persistent_tracks_p165d5.py` reçoit des images PIL et applique la détection de candidats P165-D3, sans recevoir la vérité du simulateur ni l'étiquette de condition. Il étend une liste bornée de pistes candidates, conserve des absences d'observation sans les déclarer inexistences physiques, puis calcule des sorties `CANDIDATE`, `MULTI` ou `HOLD`. Chaque piste porte positions, observations et coût d'association. Les candidats ne sont PAS des identités reconnues.

`state_from_path` injecte **la meilleure piste hypothétique** dans P165-D4 comme séquence de positions en pixels traitées selon une convention **1D synthétique**. Il distingue l'observation du `PREDICTED` entre frames manquantes et conserve les contradictions de D4. Cette convention `IMAGE_X_AS_SYNTHETIC_1D` n'est **pas une géométrie de monde**. Les valeurs de caméra ne sont pas compensées. L'adaptateur utilise une source `SIMULATED_SENSOR`, jamais une vraie mesure terrain. La liste des autres pistes reste disponible comme alternatives mais n'est pas encore propagée via D4.

## Évaluation adversariale
Rejouer la même matrice factorielle P165-D2 : 675 conditions × deux graines = 1 350 épisodes, 7 images par épisode. La vérité reste uniquement dans `EXAMS.jsonl` pour le score :
- rappel top-k : une des pistes conservées contient au moins quatre positions à 6 px ou moins des centres véritables ;
- erreur top-1 sur toutes les positions observées de la première piste ;
- nombre de HOLD, MULTI, CANDIDATE par famille couleur/occultation.

**Attention :** top-k n'est pas une preuve d'identité, et la « meilleure piste » n'est pas forcément celle de l'objet voulu. Le beam peut éliminer une trajectoire correcte ; les critères sont expérimentaux, pas calibrés. Le simulateur crée des objets factices, sans identité réelle vérifiée à la réapparition. Le rapport n'est pas une preuve d'inférence causale d'événement, de 3D ni de vraie cartographie radio. Il n'exécute pas la suite historique de 77 conditions ; celle-ci reste un gate distinct à rejouer.

## Suite architecturale, selon la vision utilisateur
Conserver contexte fond/avant/arrière relationnel, multiplicité d'objets, spectres acoustiques type Shazam, Wi-Fi/CSI, radio, radar, thermique, LiDAR, météo et représentations déterminées par l'objectif. Ces domaines nécessitent une vraie provenance, synchronisation, calibration, et observation : ne rien simuler et appeler « sensor truth ». P165-C et B fournissent des contrats, pas de la fusion matérielle. Le prochain gate devrait comparer plusieurs hypothèses d'état persistantes plutôt que seulement convertir la première.

## Commande PC Windows PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/image_persistent_tracks_p165d5.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P165-D5 échouée" }
py -m unittest discover -s tests -p "test_image_persistent_tracks_p165d5.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P165-D5 échoués — STOP" }
py -m brody_world_physique.image_persistent_tracks_p165d5 --seeds 2 --beam 8 --out "build\brody-p165d5-tracks-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P165-D5 échouée" }
Get-Content "build\brody-p165d5-tracks-001\MASTER_REPORT.json"
```

Gouvernance : `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

**Verdict avant run :** `P165D5_PUBLISHED / D3_TO_D4_ADAPTER_BOUNDED / MULTI_ID_UNPROVEN / PC_VALIDATION_PENDING`.
