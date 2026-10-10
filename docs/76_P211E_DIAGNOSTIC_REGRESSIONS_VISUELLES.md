# 76 — P2.11e : diagnostic des régressions de génération visuelle

STATUT : CODE_PUBLISHED / PC_TEST_PENDING / POSTHOC_ONLY / IMAGE_ONLY

## Ce que montraient vraiment les « 2 régressions » de P2.11d
Les essais P2.11d n'avaient pas des objectifs homogènes : un cas demandait deux emplacements de geste mais ne présentait qu'une référence partielle, le second prenait pour référence **une image blanche** malgré les boîtes d'éléments demandées. Une faible différence avec du blanc peut alors valoriser artificiellement l'absence de dessin. Les deux dégradations numériques restent des résultats exacts *contre le blanc*, mais ne prouvent pas que les gestes aient mal répondu à une consigne cohérente.

## Module
`brody_world_physique/p211e_regression_diagnostic_v0.py` : audite a posteriori des sorties P2.11d scellées, et vérifie les SHA256 et scores originaux. Il confronte les boîtes du layout aux pixels de la référence et de l'image produite. Verdicts :
- `INVALID_GOAL_EMPTY_TARGET` : image de référence entièrement blanche malgré les boîtes demandées;
- `INVALID_GOAL_NO_INK_IN_REQUESTED_BOXES` : aucun trait cible dans les régions demandées;
- `PARTIAL_REFERENCE` : cible partielle ou pixels cibles hors des régions;
- `CONSISTENT_LAYOUT_REFERENCE` : chaque boîte demandée contient au moins un pixel de référence, aucun trait extérieur.

Le rapport conserve les pixels cibles manquants, générés en excès, hors régions, et la différence antérieure; il marque un meilleur résultat *posthoc* uniquement si la consigne est cohérente. **Il ne modifie pas les PNG de Brody, ne fait pas apprendre Brody à partir des cibles TEST, n'effectue pas de boucle autonome de correction.** Une référence cohérente ne prouve pas à elle seule la compréhension de la scène.

## Validation PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p211e*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.11e échoués" }
```

Pour auditer des images P2.11d persistées, utiliser leur manifeste original :
```powershell
py -m brody_world_physique.p211e_regression_diagnostic_v0 --manifest "CHEMIN_MANIFESTE_P211D.json" --generated "CHEMIN_REPERTOIRE_P211D" --out "build\p211e-diagnostic.json"
```

## Prochaine forge après validation
Construire d'abord un jeu de compositions **objectivement aligné avec les layouts**, figé avant génération, puis une boucle bornée de proposition de modifications gestuelles. Préengager chaque nouvelle image avant de révéler la référence, comparer avec un moteur sans mémoire et conserver les dégradations et les rollbacks. Ne jamais transformer le diagnostic posthoc en entraînement sur TEST. Corriger séparément l'avertissement `Image.getdata()` lié à Pillow, sans confondre warning et invalidité scientifique.
