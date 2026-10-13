# 91 — F7 : correction TRAIN, ancien souvenir préservé, examen différé

**Branche** `exp/p2-multirepresentation-ablation-20261009`. **Statut : code publié ; exécution PC à valider.** Main intacte.

## Protocole
Cette expérience utilise les composants V2 `select_tool`, `render_instrument`, `_gray_pixel_loss` et le journal F4 `append_event`/`verify_journal`. Une première expérience TRAIN fait préférer PENCIL. De nouvelles observations TRAIN confrontent les instruments à un professeur PEN ; elles alimentent une version candidate corrigée sans détruire l'ancienne. Les deux versions choisissent leur outil, puis produisent leurs images sur une géométrie TEST différente. Les **deux PNG sont enregistrés et scellés** avant génération/consultation de la référence tenue à l'écart. Le journal conserve TRAIN ancien, TRAIN correction, puis TEST de comparaison. Le résultat est mesuré par erreur moyenne en niveaux de gris.

## Ne pas surestimer la démonstration
Il s'agit d'une **correction du routage d'outil pour une intention déclarée**, pas d'une correction des gestes, de compréhension préverbale ou de compétence artistique. L'exercice est synthétique et la cible TEST est rendue avec le même moteur PEN que le candidat corrigé, ce qui favorise ce dernier. Une éventuelle erreur zéro ne prouverait ni généralisation générale ni apprentissage autonome du réel. Aucun write Native Memory, aucun B8, aucune promotion canonique. La mémoire de F7 contient des snapshots d'expériences instrumentales distincts, **non encore fusionnés dans le registre de compétences géométriques F3c/F5**.

## Commandes PC Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_fusion_f7*.py" -v
if ($LASTEXITCODE -ne 0) { throw "F7 tests échoués" }
py -m unittest discover -s tests -p "test_fusion_f6*.py" -v
if ($LASTEXITCODE -ne 0) { throw "F6 régression" }
py -m brody_world_physique.fusion_f7_train_only_correction_v0 --out "build\fusion-f7-train-correction-001"
if ($LASTEXITCODE -ne 0) { throw "F7 demo échouée" }
Get-Content "build\fusion-f7-train-correction-001\summary.json"
Invoke-Item "build\fusion-f7-train-correction-001\old-candidate.png"
Invoke-Item "build\fusion-f7-train-correction-001\new-candidate.png"
```
Conserver toute sortie défectueuse et réexécuter avec `-002` ; ne pas effacer les preuves.

## Fermeture suivante
Tester la robustesse de correction sous des cas contradictoires, la conservation d'anciennes compétences et le HOLD quand la preuve TRAIN est insuffisante. Puis une correction du **geste visuel** et non seulement de l'outil, reliée aux snapshots F3c/F5 et au contrat `experience_memory_v1`, avant de prétendre à une éducation cumulative complète.
