# 78 — P2.12b : correction apprise sur TRAIN, figée puis transférée sur TEST

**Statut : CODE_PUBLISHED / PC_TEST_PENDING**. Branche expérimentale exclusivement, jamais `main`.

## Hypothèse testée
Les gestes mémorisés P2.11b servent à dessiner une composition P2.11c. Une correction motrice universelle simple (déplacement du dessin de ±2 px sur un axe) est sélectionnée en minimisant **la somme des erreurs pixel sur plusieurs épisodes TRAIN supervisés P2.12a**, puis enregistrée dans une politique figée avec SHA256 et empreinte de provenance.

Sur un layout TEST distinct, le moteur applique cette politique **sans ouvrir la cible** : il enregistre une image initiale (sans correction) et une image corrigée. La référence facultative ne sert qu'au score postgénération; les expériences TEST ne mettent jamais à jour la politique.

Ce protocole démontre au mieux un **transfert contrôlé d'un décalage systématique**. Il ne démontre pas encore la création d'une politique visuelle contextuelle, la généralisation à d'autres objets/scènes ni la découverte autonome des règles de dessin. Le moteur sans mémoire concurrent est ici la génération avec les mêmes gestes mémorisés mais **sans la correction apprise**; on isole donc l'effet de la correction, pas l'utilité de l'ensemble de la mémoire de Brody.

## Interfaces
- `brody_world_physique/p212b_frozen_shift_transfer_v0.py`
- `tests/test_p212b_frozen_shift_transfer_v0.py`

TRAIN : `--memory chemin.json --train-receipts chemin_run1/report.json chemin_run2/report.json --policy chemin_policy.json`.

TEST : `--memory chemin.json --policy chemin_policy.json --layout test-layout.json --out repertoire-nouveau [--reference reference-test.png]`.

Les épisodes TRAIN doivent provenir du même moteur P2.11b, contenir cinq candidates intègres P2.12a et des dispositions différentes. Une politique déjà présente, la modification des rapports/candidates et la réutilisation de la référence TRAIN côté TEST sont refusées.

## Validation PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p212b*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.12b échoués" }
```

Après validation ciblée, relancer la suite élargie pour déceler des régressions de l'école de dessin. Les résultats de ces tests synthétiques ne constituent pas une démonstration de perception ou de génération visuelle générale.

## Tableau de bord des étapes
- P2.11a : routage mémoire vers dessin — 3/3 tests PC PASS.
- P2.11b : enregistrement/rejeu des gestes — 4/4 PC PASS.
- P2.11c : recomposition par zones — 4/4 PC PASS.
- P2.11d : évaluation appariée, deux cas dégradés contre le blanc — 4/4 PC PASS (le verdict comparatif est négatif).
- P2.11e : diagnostic d'objectifs incohérents — 3/3 PC PASS.
- P2.12a : cinq corrections supervisées, conservation des échecs — 3/3 PC PASS.
- P2.12b : politique TRAIN figée puis TEST aveugle — tests PC EN ATTENTE.

**Interdit de déduire un pourcentage global de capacité de ces réussites unitaires.** Le ratio succès/total n'a de sens que pour un périmètre de tests identifié.

## Suite recommandée
Ablations de politique et des gestes, conditions de transfert nouvelles, calibration et incertitude, représentation du monde visuel en plusieurs couches, Reverso effectif, multi-échelle, cinématique/360° selon les contrats du projet. Chaque gain doit être constaté sur des cas TEST qui n'ont jamais déterminé la politique.
