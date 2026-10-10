# 49 — P2.7 ordre, hiérarchie, expérience : ablation à pixels identiques

## Origine de l'hypothèse (auteur)
L'échec P2.6 peut venir de l'ordre de classement des données, de la confiance qu'on leur accorde, et des expériences retenues. La fréquence/cohérence d'une observation n'est pas la vérité. La « donnée qui paraît du bruit » peut être le seul repère pertinent si elle est correctement située dans la hiérarchie, dans l'espace et dans le temps.

## Expérience falsifiable
Comparer sur exactement les mêmes images et mouvements mesurés :
- `majority` : médiane de 5 repères avec seuil fixe de consensus ;
- `hierarchy` : priorité du repère d'identité 4, règle préprogrammée, aucune expérience ;
- `experience` : choix du repère ayant l'erreur médiane la plus faible sur des épisodes TRAIN antérieurs ;
- `hierarchy_experience` : n'émettre que si >= 2 repères ont un historique fiable ; sinon HOLD.

Important : les repères sont identifiés par leur place horizontale dans cette maquette 2D. Le générateur corrompt prioritairement les premiers indices. Le dernier repère est intact **par construction**. Ainsi le bras hierarchy est fortement avantagé artificiellement. Le savoir TRAIN utilisé par experience correspond à la **vérité de déplacement caméra donnée par le simulateur** : c'est une calibration supervisée, PAS un apprentissage autonome du monde. Le modèle ne reçoit aucune vérité TEST avant fermeture des reçus.

### Sorties
`evaluation.json` : couverture, erreur moyenne, prédictions catastrophiques (>10 px), comparaison sur les mêmes épisodes et détail par scénario.
`predictions_pre_scoring.jsonl` : les quatre sorties pour chaque observation avant évaluation par vérité du simulateur.
`images/train_test_pairs.png` : une planche réelle des premières paires TEST.

L'expérience s'appuie sur `render` et `detect` de P2.6 (vraies images synthétiques en mémoire), sans modifier P2.6. Elle ne teste PAS encore l'illumination, le 3D, les angles arbitraires, ni la fiabilité apprise sans étiquettes.

### Commandes PowerShell PC
```powershell
$ErrorActionPreference="Stop"
Set-Location "C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) {throw "Git failed"}
py -m unittest discover -s tests -p "test_p27*.py"
if ($LASTEXITCODE -ne 0) {throw "P2.7 tests failed"}
$out="build/p27-hierarchy-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.p27_experience_hierarchy_v0 --out $out --train 120 --test 480
if ($LASTEXITCODE -ne 0) {throw "P2.7 failed"}
py -m brody_world_physique.p27_experience_hierarchy_v0 --out $out --verify
if ($LASTEXITCODE -ne 0) {throw "P2.7 replay failed"}
Invoke-Item "$out/images"
notepad "$out/evaluation.json"
.\scripts\publish_local_evidence.ps1 -RunPath $out
if ($LASTEXITCODE -ne 0) {throw "Publication failed"}
```

Aucun push main. Ne pas confondre score d'un modèle guidé par un simulateur et validation d'une représentation physique autonome.
