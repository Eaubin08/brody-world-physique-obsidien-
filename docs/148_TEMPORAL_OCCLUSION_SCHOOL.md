# P148 — École temporelle des occultations (simulation 2D)

## Nouvelle question expérimentale

P147 mesurait des silhouettes ponctuelles et des refus pour objets complètement cachés. P148 évalue désormais **cinq images successives** par essai : les quatre premières servent à prédire le centre du mobile à la cinquième ; l'image future sert exclusivement à évaluer. Deux mécanismes sont confrontés : **instantané** (centre à la dernière image) et **historique** (vitesse extrapolée depuis les deux dernières positions observées). Quand il manque des observations, l'historique renvoie HOLD.

## Dix familles de mouvement

Mouvement régulier, inversion, arrêt, accélération, entrée derrière un écran, sortie d'écran, image courante ambiguë, second objet, occultation totale et sortie du champ (contrôles expérimentaux). Ces noms indiquent des *cas de générateur*, pas des compétences physiques déjà acquises.

Chaque épisode produit des images procédurales 96×64 avec masque opaque et centre de cible connu du générateur. Les scores montrent l'erreur absolue en pixels du prochain centre et la proportion de prévisions effectivement possibles. Les premiers exemples de chaque famille sont sauvegardés en PNG pour inspection ; les autres examens sont consignés dans `EPISODES.jsonl` et un `MASTER_REPORT.json`.

**Limites à ne pas masquer** : plusieurs familles sont encore conçues avec des règles simplifiées ; la cinquième observation sert à l'oracle générateur et non à une perception automatique de la cible future. L'historique n'apprend pas encore une nouvelle loi et ne met pas à jour une mémoire. La simulation n'est pas une expérience physique réelle, et la stabilité de l'identité lors de deux objets n'est pas prouvée. Les scénarios d'« image identique, histoire différente » demandent encore un test contre-factuel apparié avec égalité pixel à pixel : ce n'est pas prouvé ici.

## Run PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_temporal_occlusion_p148.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P148 échoués" }
py -m brody_world_physique.image_temporal_occlusion_p148 --minutes 15 --episodes-per-kind 1500 --out "build\brody-p148-temporal-001"
if ($LASTEXITCODE -ne 0) { throw "Run P148 échoué" }
Get-Content "build\brody-p148-temporal-001\MASTER_REPORT.json"
```

Budget de quinze minutes au maximum, quinze mille épisodes au plus. Aucun remplissage artificiel du temps de calcul. Examiner les `history_mae`, `snapshot_mae` et `history_holds` séparément, jamais le seul nombre de PASS.

**Gouvernance** : branche expérimentale ; `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
