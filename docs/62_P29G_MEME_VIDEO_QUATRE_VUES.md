# 62 — P2.9g : une source vidéo, quatre vues + réciprocité + Reverso

**État :** code et trois tests unitaires publiés, non exécutés sur le PC à la rédaction.

P2.9g exige le rejeu original `multirepresentation_ball_bridge_v5.verify` (même vidéo P1, prévisions pré-engagées, images et comparaison Reverso). Il relit les quatre vues RASTER, SPATIAL, TEMPORAL et MOTION d'une seule source synthétique. Il contrôle la cohérence des vitesses dérivées de trois observations temporelles avec la vue MOTION conservée; il reconstruit la relation inverse comme opération algébrique et lie l'ensemble aux **classes existantes** `WorldStateDeltaV0`, `WorldExperienceCandidateV0`, `triage_learning`. Il ne traite pas quatre vues corrélées comme quatre sources indépendantes.

**Limite majeure :** la relation réciproque est mathématique en 2D (ancien→nouveau et nouveau→ancien), **pas le classificateur V4.2**. Les résultats P1 sont déjà évalués après révélation de l'image future et P2.9g **n'émet aucune nouvelle prévision**. Cette couture ne prouve donc pas encore une meilleure généralisation, ni un modèle physique ou un 360°. Le nouveau rapport est une recomposition et un audit de cohérence de preuves existantes.

## Tests PC
```powershell
$repo = "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
Set-Location $repo
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "pull failed" }
py -m unittest discover -s tests -p "test_p29g*.py" -v
if ($LASTEXITCODE -ne 0) { throw "P2.9g test failed" }
```

## Exécution sur les VRAIES preuves P1 existantes (ne pas inventer les chemins)
```powershell
# Remplacer par les chemins exacts des anciens runs :
$suite = "CHEMIN_SUITE_P1\suite.json"
$forecasts = "CHEMIN_PREVISIONS_P1\forecasts_precommitted.jsonl"
$preview = "CHEMIN_PREVIEW_REVERSO"
$p1 = "CHEMIN_RESULTAT_P1"
$out = "build/p29g-p1-$(Get-Date -Format yyyyMMdd-HHmmss).json"
py -m brody_world_physique.p29g_one_video_bridge_v0 --suite $suite --forecasts $forecasts --preview $preview --p1-out $p1 --out $out
py -m brody_world_physique.p29g_one_video_bridge_v0 --suite $suite --forecasts $forecasts --preview $preview --p1-out $p1 --out $out --verify
```

L'utilisateur peut donner les quatre chemins ou retrouver les anciens rapports localement. Si les originaux ne sont plus disponibles, ne pas présenter des mocks de tests unitaires comme preuves opérationnelles.

**Suite :** produire une vraie nouvelle prédiction avant la frame future sur le même flux, en réutilisant les règles et les vues d'origine, puis ablations équitables et changements décor/référentiel indépendamment.
