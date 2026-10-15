# 92 — F8 : campagne de régression et cas adversariaux en une commande

**Code publié, résultats PC non encore validés.** Branche `exp/p2-multirepresentation-ablation-20261009`. Ne pas toucher `main`.

F8 évite la succession de mini-jalons de test. Il lance **12 suites distinctes** (V2 instruments, Fusion F1/F2/F3/F3b/F3c/F4/F5/F6/F7, cas adversariaux), puis le **vrai rejeu F2 des 15 suites d'écoles historiques**. Chaque processus écrit un log; le bilan central `report.json` inclut statuts PASS/FAIL/MISSING/TIMEOUT, retours système et durées. Toute suite non PASS provoque un verdict global `FAIL_CLOSED` et un code sortie non nul.

Cas adversariaux ajoutés : inversion d'un vainqueur lorsque le TRAIN contredit le souvenir, données d'expérience invalides, intention inconnue HOLD, isolation des versions mémoires, historique de six épisodes, conservation de l'ancienne version corrigée, et rappel explicite que le TEST F7 reste favorable à la correction et ne démontre pas la généralisation.

**Ce que ce gros test ne prétend pas démontrer :** ni compréhension réelle des objets/physique, ni autonomie d'apprentissage ouverte, ni correction du geste moteur, ni couplage Native Memory/MEMZUM. Les résultats F6 et F7 à zéro erreur utilisent des cibles synthétiques partageant le moteur graphique ; conserver cette limite.

## Une commande PowerShell, avec vérification de branche

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }

py -m brody_world_physique.fusion_f8_large_regression_v0 --repo . --out "build\fusion-f8-large-001"
if ($LASTEXITCODE -ne 0) { Write-Warning "Campagne F8 avec échecs : lire les logs ci-dessous" }
Get-Content "build\fusion-f8-large-001\report.json"
```

Les logs détaillés se trouvent dans `build\fusion-f8-large-001\*.log`. Pour relancer, changer uniquement `-001` en `-002`, ne jamais effacer les preuves d'échec.

## Suite technique après ce diagnostic
Ne plus ajouter une école nominale à chaque palier. Selon les résultats de F8, corriger les vraies régressions ; puis intégrer **la correction des gestes**, les relations visuelles, et le contrôle du transfert contradictoire dans une boucle d'éducation persistante avec des cas réels/externes et une véritable séparation TRAIN/TEST. L'architecture existante `experience_memory_v1` reste la référence et doit être raccordée, sans nouveau canon concurrent.
