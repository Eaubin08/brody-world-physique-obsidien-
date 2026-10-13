# 63 — P2.9h : ablation comparative pré-engagée, première phase position

État : module et deux tests publiés sur branche expérimentale; **aucune mesure PC obtenue au moment du commit**.

Le module `p29h_position_ablation_v0.py` relit les vidéos TRAIN/TEST déclarées dans `suite.json` via `_load_probe_suite`, `iter_video_points`, `acquire_experiences` et `propose_with_conflict_gate` déjà existants. Les expériences TRAIN sont figées avant toute lecture TEST. Pour chaque frame future, toutes les variantes proposent en amont, puis la frame est révélée pour évaluation. Aucun retour TEST n'est donné à la mémoire. Toutes les variantes utilisent le même historique et la même mesure de position (erreur Euclidienne en px), avec couverture et MAE conditionnel séparés.

Les variantes réelles de cette phase :
- A0 : dernière position, mouvement nul
- A1 : extrapolation du dernier déplacement spatial
- A2 : vitesse temporelle calculée sur les mêmes points
- A4* : prédicteur mémoriel existant avec toutes les expériences TRAIN
- A5 : même prédicteur avec zéro expérience
- A6 : expériences TRAIN limitées aux 1 et 4 premières

**A4* n'est pas encore la fusion visuelle+spatiale+temporelle** du contrat 43 : c'est le prédicteur d'expérience existant, marqué comme tel. A3 image+spatial et la métrique pixel Reverso ne sont pas encore comparées dans ce banc. Avec les vidéos échantillonnées à intervalle constant, A1=A2 algébriquement : ce contrôle est utile mais ne prouve aucun bénéfice du temps. A5 HOLD sans expérience est attendu, pas une défaite de la vision. Ni l'apprentissage autonome ni la robustesse multi-environnement ne sont encore démontrés.

## Commande PC fixe
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p29h*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
$suite = "build\brody-p2-20261009-015858\suite\suite.json"
if (-not (Test-Path $suite)) { throw "Suite historique absente" }
$out = "build\p29h-ablation-$(Get-Date -Format yyyyMMdd-HHmmss).json"
py -m brody_world_physique.p29h_position_ablation_v0 --suite $suite --out $out
if ($LASTEXITCODE -ne 0) { throw "Ablation échouée" }
py -m brody_world_physique.p29h_position_ablation_v0 --suite $suite --out $out --verify
if ($LASTEXITCODE -ne 0) { throw "Rejeu échoué" }
Write-Host "RESULTATS=$out"
```

## Résultat à examiner avant la suite
Comparer la couverture, le MAE conditionnel et le nombre d'échecs >10px par bras. **Ne pas déclarer meilleur le bras qui HOLD le plus et n'a presque aucune prédiction acceptée**. Contrôler le même nombre de cas. Une vraie seconde phase devra introduire la sortie image/masque Reverso et des transformations caméra valides, puis décors/repères changés séparément, sans fuite TEST. L'absence de gain est un résultat admissible.
