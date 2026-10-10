# P2.8 — premier build diagnostique, branche expérimentale

## Statut vérifiable
Code et tests publiés sur la branche `exp/p2-multirepresentation-ablation-20261009`.
**Aucun test local certifié lors de cette publication GitHub.** Exécution à effectuer dans un clone Python qui possède les dépendances du projet.

## Ce qui est fait
- Simulation séquentielle sur 70 épisodes, avec renversement du repère fiable à l'épisode 30.
- Historique de fiabilité par repère, hypothèse provisoire `WORKING_EXPERIMENTAL_ONLY`.
- Prédictions d'abord, vérité de simulateur fournie avec retard ensuite : supervision explicitement déclarée.
- Baselines historique figé (repère 4) et majorité ; politique provisoire qui peut changer son repère préféré.
- Dédoublonnage des preuves selon leur `group_id` (pas un audit de dépendances générales).
- Changement d'intention `generate/explore/explain` modifie le parcours demandé, jamais la prédiction ni son statut de vérité.
- `HOLD_UNCALIBRATED` sans preuve préalable ; `HOLD_CONFLICT` entre repères réputés fiables.
- Reçu pré-feedback et hash SHA-256 ; replay déterministe comparant les octets des sorties.

## Ce qui n'est PAS démontré
- Le générateur fournit directement les cinq déplacements mesurés ; **ce banc ne traite pas les pixels**. Ne pas le décrire comme apprentissage autonome des images, monde ou physique.
- L'apprentissage est **supervisé par caméra-vérité simulée**, avec oracle différé. Il ne résout pas comment obtenir la vérité physique indépendante en pratique.
- Les erreurs de capteurs sont artificiellement corrélées ; la politique actuelle peut continuer à faire confiance à un mauvais repère durant le basculement.
- Ce n'est **pas** une transition B8 ni une persistance B10 ; `memory_write=False`, `KX108_ONLY`.
- Le statut expérimental est distinct des `ClaimState` fermés B8. Pas d'injection dans Native Memory.
- La compatibilité B8 conceptuelle a été contrôlée contre le contrat local de l'opérateur et `app/knowledge/b8/contracts.py` sur `obsidia-x108-proofs`. B10 reste non localisé / non audité : **F0 persistance = HOLD**.

## Commandes sur le clone Brody (PowerShell)
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
git branch --show-current
git pull --ff-only
py -m unittest discover -s tests -p "test_p28*.py" -v
$out = "build/p28-reversal-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.p28_epistemic_reversal_v0 --out $out --n 70 --delay 2
py -m brody_world_physique.p28_epistemic_reversal_v0 --out $out --verify
```
Sur le PC portable le clone Brody peut ne pas exister ; exécuter seulement dans un clone sur la **bonne branche**. Aucun push vers `main`. Ne pas utiliser `git pull` si la branche courante diffère, ou si le worktree contient des modifications à protéger.

## Test suivant (P2.8b)
Brancher la même politique sur les vraies mesures pixel P2.6/P2.7 ; introduire des changements de fiabilité indépendants des IDs ; contrôler une preuve externe réellement indépendante ; mesurer la précision **avant** et **après** basculement, le délai d'adaptation et les faux HOLD. Fixer les paramètres de seuil sur TRAIN avant TEST.
