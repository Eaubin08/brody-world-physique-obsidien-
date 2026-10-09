# 80 — P2.12d : gate conservateur ACT / HOLD et statistiques visuelles

Statut : CODE PUBLIE / TESTS PC A CONFIRMER, branche exp/p2-multirepresentation-ablation-20261009.

## Portée
On apprend sur les reçus TRAIN P2.12a déjà utilisés pour figer la politique P2.12b. Le gate autorise **ACT** uniquement si la correction retenue améliore strictement **chaque** exemple TRAIN. Dans tout autre cas : **HOLD** (image initiale conservée). Le gate et ses preuves sont figés par empreinte. La décision pour TEST est prise avant toute ouverture de la référence. Un rapport visuel montre **CIBLE / INITIAL / CHOISI**, avec erreur absolue, différence et IMPROVED/WORSENED/TIE par cas. Aucune expérience TEST ne change la politique.

## Ce qu'il ne démontre pas
C'est un gate **global et non contextuel**, pas encore la reconnaissance des situations visuelles dans lesquelles la correction convient. Si l'entraînement est entièrement homogène, ACT peut encore empirer certains TEST ; si l'entraînement est contradictoire, HOLD évite des changements mais ne crée aucun gain. La réussite des unit tests indique que le banc respecte les règles et mesure ces limites, pas que Brody généralise. Pas de perception avancée ni de Reverso ici, aucune écriture Native Memory.

## Validation sur PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p212d*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.12d échoués" }
```

## Deux modes CLI
TRAIN : `py -m brody_world_physique.p212d_conservative_correction_gate_v0 --policy policy.json --train-receipts run_train1/report.json run_train2/report.json --out gate.json`.

TEST : `py -m brody_world_physique.p212d_conservative_correction_gate_v0 --policy policy.json --gate gate.json --memory mem.json --manifest manifest-test.json --out rapport-visuel-p212d`.

Le dossier TEST contient `comparison.png`, `summary.json` et les PNG des épisodes.

## Statistiques fiables à tenir
Jusqu'à P2.12c : **27/27 tests ciblés PC réussis**, sur les jalons P2.11a à P2.12c. Résultat synthétique de P2.12c : 1 cas amélioré, 2 dégradés, mais les écarts exacts de pixels n'ont pas été fournis dans la conversation. P2.12d : 3 nouveaux tests publiés, validation PC attendue. Aucun pourcentage d'achèvement global n'est encore démontré.

Prochain verrou : construire un **sélecteur contextuel** dont les features viennent uniquement de l'image/consigne initiale ; comparer dans un protocole de test aveugle avec et sans gate, et mesurer les retours d'image.
