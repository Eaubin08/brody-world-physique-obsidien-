# Brody P2.8c — garde de révision, ablation appariée

But : tester si une fiabilité récente, basée uniquement sur les retours supervisés déjà disponibles, limite les erreurs pendant le changement de repère. P2.8b reste intact. P2.8c ne change **pas** le détecteur d'image P2.6 : la perte de couverture causée par l'éclairage et les occultations reste mesurable.

## Méthodes comparées
Sur chaque *même* paire d'images synthétiques :
- historique figé ;
- majorité ;
- P2.8b historique global ;
- P2.8c fenêtre glissante de 8 vérifications, avec HOLD sans calibration, si historique peu fiable ou si les candidats historiques se contredisent.

Retour de vérité du simulateur différé (2 épisodes), parfois absent. L'intention utilisateur ne fournit aucune vérité. Les mesures proviennent des pixels, via le détecteur programmé.

## Protocole fixe

```powershell
$repo = "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
Set-Location $repo
git branch --show-current
git pull --ff-only
py -m unittest discover -s tests -p "test_p28c*.py" -v
if ($LASTEXITCODE -ne 0) { throw "P2.8c TEST FAIL" }
$out = "build/p28c-guard-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.p28c_guarded_reversal_v0 --out $out --count 180 --delay 2 --window 8
if ($LASTEXITCODE -ne 0) { throw "P2.8c RUN FAIL" }
py -m brody_world_physique.p28c_guarded_reversal_v0 --out $out --verify
if ($LASTEXITCODE -ne 0) { throw "P2.8c REPLAY FAIL" }
Write-Host "EVIDENCE_PATH=$out"
```

**Auditer** : couverture, MAE conditionnelle, erreurs >10px, et MAE appariée P2.8b vs P2.8c. Plus de HOLD peut artificiellement diminuer la MAE : ne pas conclure sur cette seule moyenne. Comparer les erreurs autour des changements de régime. Ne pas considérer une fenêtre de 8 choisie ici comme un hyperparamètre validé hors distribution. Les scénarios et inversions demeurent artificiels et prévisibles ; aucun apprentissage autonome de physique.

Aucun accès à B8, B10, Native Memory ; `memory_write=False`, `KX108_ONLY`. Les reçus pré-feedback sont accumulés en RAM, puis enregistrés et hachés après le run : **pas de scellement indépendant en ligne**.

Statut au commit documentaire : code + tests publiés, résultats locaux **non exécutés**.
