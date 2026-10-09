# P2.8b — Pixel reversal diagnostic

## But
Vérifier sur images réellement **rendues** et **analysées par détecteur couleur P2.6** si une fiabilité historique peut être révisée lorsque le repère fiable passe de ID 4 à ID 0, puis ID 2. Déplacements physiques simulés ; l'estimation est issue des pixels, pas de l'accès aux positions de vérité.

## Code
- `brody_world_physique/p28b_pixel_reversal_v0.py`
- `tests/test_p28b_pixel_reversal_v0.py`

## Exécuter sur le PC fixe
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
git branch --show-current
git pull --ff-only
py -m unittest discover -s tests -p "test_p28b*.py" -v
if ($LASTEXITCODE -ne 0) { throw "P2.8b tests failed" }
$out = "build/p28b-pixels-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.p28b_pixel_reversal_v0 --out $out --count 180 --delay 2
if ($LASTEXITCODE -ne 0) { throw "P2.8b run failed" }
py -m brody_world_physique.p28b_pixel_reversal_v0 --out $out --verify
if ($LASTEXITCODE -ne 0) { throw "P2.8b replay failed" }
Write-Host "EVIDENCE_PATH=$out"
```
Exécuter seulement sur la branche `exp/p2-multirepresentation-ablation-20261009`, avec un worktree propre pour `git pull --ff-only`.

## Critères de lecture
Publier **les trois fenêtres temporelles**, leurs couvertures, erreurs conditionnelles aux prédictions émises et nombres d'erreurs >10px. Les HOLD visuels comptent dans la couverture. Examiner les changements de repère choisi et les erreurs juste après chaque inversion. La comparaison entre algorithmes à couverture différente n'est pas un avantage démontré sans analyse à couverture comparable.

## Limites non négociables
- Représentation visuelle artificielle ; détection de pixels fondée sur couleurs programmées, non acquises par apprentissage.
- Images double-frame synthétiques, 5 repères explicitement indexés, perturbation opposée de 24 pixels, vérité caméra transmise après chaque prédiction retenue si feedback disponible ; ce n'est pas une compréhension autonome du monde.
- La caméra / vérité de monde est dans le simulateur, jamais dans l'entrée `decide()`. Les reçus de prédiction sont inscrits en mémoire de processus avant supervision ; **les fichiers de preuve ne sont scellés sur disque qu'après la simulation complète**. Il s'agit de vérification déterministe, pas de preuve cryptographique d'une séparation runtime forte.
- Groupement d'évidence par paire d'images seulement, pas de preuve d'indépendance physique des mesures.
- Aucun write dans Native Memory, aucune promotion B8, aucune persistance B10, aucune décision action. `KX108_ONLY`.
- B10 : toujours HOLD pour le raccordement de persistance réelle.
