# Ablation anti-fuite d'indice de famille — Brody Image

Ancien benchmark (`image_persistent_transfer_exam_v0.py`) : le learner exploitait `family|style|shape` et l'examen ne prouvait donc pas de détection autonome. Cette édition ajoute un banc **sans accès learner à `family`**, avec tirage équilibré des familles et variation indépendante des styles/formes : pas d'indice de type `index % 10` lisible par le modèle.

- La clé de politique ne contient que `intent_visible|shape`.
- `family`, `true_style`, transformation et correction ne servent que dans l'évaluateur, après décision scellée.
- 10 000 épisodes supervisés pour mémoire candidate locale, puis 10 000 scènes neuves en examen sans écriture ni feedback vers learner.
- Même scène d'examen pour les deux prédictions : base initiale et modèle enrichi.
- Rapport comprenant erreur avant/après, améliorations et régressions par famille ; score défavorable admis sans contournement.
- Limite : les instructions de style/forme restent lisibles, le même moteur de rendu génère train/test. L'image cible n'est pas visible avant le choix. Pour `wrong_intent`, le modèle ne dispose donc pas d'une observation authentique lui permettant de détecter la tromperie. Aucun score flatteur attendu ou garanti. Cela ne remplace pas les expérimentations sur vraies images.

## Exécution sur PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_family_blind_ablation_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
py -m brody_world_physique.image_family_blind_ablation_v0 --snapshot "build\brody-image-school-20k-001\training\snapshot-010000.json" --train 10000 --exam 10000 --out "build\brody-image-ablation-no-family-20k-001"
if ($LASTEXITCODE -ne 0) { throw "Ablation échouée" }
Get-Content "build\brody-image-ablation-no-family-20k-001\MASTER_REPORT.json"
```

**Comparabilité honnête :** nouvel échantillonnage famille/style/forme = score à confronter à l'ancien comme résultat d'ablation, mais l'écart agrégé ne peut pas être attribué exclusivement à l'étiquette sans comparaison appariée sur les mêmes scènes des deux modèles. Le contrôle apparié est base vs ablation **dans cette nouvelle campagne**. L'ablation ne prouve pas à elle seule une perception sémantique.
