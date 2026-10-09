# P2.9b — Raccordement end-to-end des étages (comparaison contrôlée)

Statut : **code et tests publiés, exécution PC non encore vérifiée**.

## But exact
Faire passer chaque scène du banc pixel P2.8c par des contrats distincts :
`p28b.observe` (pixels) → `PixelObservation` (mesures et provenance) → `SpatialRelations` (référentiel explicitement déclaré) → `GuardedBelief.predict` (savoir de travail non promu) → `WorkingBelief` → `GoalRouting` (intention humaine). Le calcul du prédicteur P2.8c est conservé ; sur chaque scène, une seconde instance P2.8c reçoit exactement les mêmes observations et retours de vérification différés. La **parité obligatoire** prouve seulement que l'architecture en étages ne change pas par erreur le raisonnement de base.

## Tests à lancer sur le PC fixe
```powershell
$repo = "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
Set-Location $repo
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull en erreur" }
py -m unittest discover -s tests -p "test_p29b*.py" -v
if ($LASTEXITCODE -ne 0) { throw "P2.9b tests en erreur" }
$out = "build/p29b-layer-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.p29b_layer_wiring_v0 --out $out --count 180 --delay 2 --window 8
if ($LASTEXITCODE -ne 0) { throw "P2.9b banc en erreur" }
py -m brody_world_physique.p29b_layer_wiring_v0 --out $out --verify
if ($LASTEXITCODE -ne 0) { throw "P2.9b replay en erreur" }
Write-Host "EVIDENCE_PATH=$out"
```

## Résultats attendus
La couverture et la MAE doivent être **identiques** à P2.8c car ce build ne change pas le détecteur ni le modèle de fiabilité. Tout écart produit un échec de parité par épisode. Cette égalité ne prouve ni apprentissage nouveau ni amélioration ; elle prouve seulement que les contrats sont branchés sans changer le comportement.

## Limitations et frontière d'autorité
Les images sont synthétiques, le détecteur de couleurs est programmé, le retour de vérité de caméra est simulé et différé. Les reçus sont accumulés en RAM et scellés après coup. L'implémentation `PixelObservation.source_ref` est un identifiant synthétique **et non** un hash d'image vérifiable. `SpatialRelations.coordinate_frame` est déclaratif, les transformations multi-référentiels ne sont pas implémentées. L'expérience d'apprentissage réel sur générateur inédit **n'est pas encore ce build**. Ne pas l'annoncer comme P2.9 complet.

Le code n'appelle ni B7/B8/B10, ni Native Memory ; il ne possède aucun pouvoir de promotion ou écriture (`memory_write=False`, `b8_promotion=False`, `KX108_ONLY`).
