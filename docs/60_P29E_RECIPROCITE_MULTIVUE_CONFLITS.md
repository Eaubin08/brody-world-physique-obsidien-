# 60 — P2.9e : réciprocité du mouvement, représentations concurrentes et contrôle de désaccord

**Statut :** première couture expérimentale publiée, tests PC NON RUN. Suite de P2.9d, sans nouveau moteur souverain.

## Ce qui est branché
`p29e_reciprocal_multiview_v0` consomme les mesures d'image déjà produites et crée une vue mouvement/repère. La réciprocité arithmétique objet↔caméra est contrôlée; elle ne constitue **pas** une preuve physique indépendante. La vue candidate de majorité des repères est confrontée à la prédiction du repère historique via `p29d_reconnect_organs_v0.reconnect` (qui réutilise les vrais contrats `WorldStateDeltaV0`, `WorldExperienceCandidateV0`, `triage_learning`). Si elles divergent, `HOLD_CONFLICT_OR_MISSING_OBSERVATION`; aucun oracle TEST consulté.

Cette politique est **conservatrice et partielle** : une majorité corrélée peut être fausse, sa concordance avec l'historique ne garantit rien. Le code émet `WORKING_CANDIDATE_UNVERIFIED`, jamais une vérité vérifiée. Le routage de l'intention ne change pas les prédictions.

## Limites non négociables
Ce build n'effectue pas encore la transformation libre 360°/3D, n'appelle pas les calculs géométriques V4.2 et ne réutilise pas encore P1 vidéo/reconstruction Reverso de bout en bout. Il ne lie pas un WorldState canonique MMonde, une trajectoire F12 ni une mesure instrumentale F13. Les doubles représentations produites depuis **les mêmes pixels sont corrélées** : pas deux preuves indépendantes. Aucun transfert réel ni gain de score revendiqué.

## Test PC fixe
```powershell
$repo = "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
Set-Location $repo
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p29e*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.9e échoués" }
```

## Raccordements suivants — jamais inventer leur activation
1. Brancher les épisodes P1 : source vidéo SHA, timestamps, repère objet/caméra, mouvement et états candidats.
2. Adapter les procédures V4.2 pour transformations réciproques sur **vues compatibles**, avec vérification des unités et origines.
3. Ajouter Reverso reconstruction et re-perception sur mêmes sources, avec scores pixels/relations séparés.
4. Protocole factoriel fixé avant scores : décor seulement, repère seulement, les deux, contrôle; mesurer les HOLD et l'erreur à couverture comparable.
5. Brancher la portée historique du savoir sans feedback TEST; les échecs restent conservés comme expériences candidates, sans B8/B10 write.
