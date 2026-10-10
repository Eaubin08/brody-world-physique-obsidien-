# 75 — P2.11d : audit apparié de recomposition sur dispositions inédites

STATUS: CODE_PUBLISHED / PC_TEST_PENDING / CONTROLLED_TRANSFER_ONLY

## Protocole
Le module `brody_world_physique/p211d_paired_composition_audit_v0.py` reçoit une mémoire motrice P2.11b figée et des cas contenant **disposition / image de référence**. Pour chaque cas, le moteur P2.11c dessine les gestes mémorisés selon la disposition nouvelle, génère un PNG et un témoin **blanc**, puis seulement le banc ouvre l'image cible et compte les différences pixel par pixel. On conserve les cas améliorés, dégradés et inchangés, et leur score apparié. Les empreintes TRAIN/TEST identiques et les réutilisations évidentes de disposition/référence sont rejetées.

IMPORTANT : « sans mémoire » signifie ici **image blanche**, pas un second générateur sans mémoire doté des mêmes capacités. Un avantage contre le blanc est un résultat de baseline contrôlée, pas une preuve d'utilité de la mémoire comparée à un générateur compétitif. L'instruction de composition (positions et proportions) est fournie par l'humain : pas de choix autonome d'une nouvelle scène. Ces transformations restent géométriques; ne pas conclure à une généralisation perceptive ou sémantique.

## Input
Créer `build/p211d-manifest.json` :
```json
{
  "schema":"BRODY_P211D_MANIFEST_V0",
  "memory":"build/p211b-gestures.json",
  "cases":[
    {"layout":"build/layout-test-1.json","reference":"build/reference-test-1.png"},
    {"layout":"build/layout-test-2.json","reference":"build/reference-test-2.png"}
  ]
}
```
Les dispositions sont au format `BRODY_P211C_LAYOUT_V0`, avec des boîtes **strictement dans les limites `SIDE`** du moteur historique. Les références TEST doivent avoir les dimensions du canevas et différer de TRAIN.

## Test Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p211d*.py" -v
if ($LASTEXITCODE -ne 0) { throw "P2.11d échoué" }
```
Examen réel une fois les données prêtes :
```powershell
py -m brody_world_physique.p211d_paired_composition_audit_v0 --manifest "build\p211d-manifest.json" --out "build\p211d-run-001"
```

## Conditions pour dépasser ce stade
Remplacer le témoin blanc par un **moteur sans mémoire capable de dessiner**, attribuer les nouvelles compositions sans lire les images de référence, produire un dataset d'images variées et figé avant l'essai, vérifier l'intégrité complète des sorties et reconnecter Reverso aux représentations nécessaires. Les résultats dégradés restent des expériences exploitables par des boucles futures; ils ne doivent pas être effacés ni promus en vérité.
