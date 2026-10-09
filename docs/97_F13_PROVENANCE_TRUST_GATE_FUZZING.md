# F13 — Réconciliation observation / preuve de fiabilité / décision (contre F12)

**Branche** `exp/p2-multirepresentation-ablation-20261009`. **Code publié, tests PC en attente.**

## Constat d'architecture
`docs/05_LEARNING_MEMORY.md` prévoit déjà provenance, contradictions, Source Reliability Evidence, ExperienceCandidate et validation. `docs/21_BRODY_IMAGE_MASTER_PLAN.md` prévoit lui aussi de séparer compréhension, savoir, vérité et confiance. F11/F12 avaient **contourné** cette distinction en utilisant le seul marqueur visuel pour émettre une proposition de contexte. Ce n'est pas une découverte de doctrine, mais un raccordement incomplet.

## F13
F13 réutilise **exactement les 10 familles de F12** : 1000 essais par défaut, avec proposition perceptive brute, preuve de provenance distincte (ou `UNAVAILABLE`), décision provisoire, verdict de la campagne, et reçu chaîné. Une proposition du pixel seul n'est pas admise ; si l'observation et une preuve indépendante vérifiée se contredisent, `HOLD_SOURCE_CONTRADICTION`. Les cas sans preuve aboutissent à `HOLD_UNVERIFIED_ORIGIN`. La campagne expose le nombre de fausses décisions avant/après le garde et le coût en refus. Aucun entraînement ni accès à Native Memory.

**Limites impératives :** la source indépendante est une **fixture contrôlée par le banc de test**, pas une signature de capteur authentifiée. Seules les catégories `baseline` et `border_noise` ont une référence dite vérifiée par le banc. Les autres ne disposent pas de cette preuve et sont refusées. Le banc peut donc mesurer la séparation observation/confiance sans démontrer la résistance à un attaquant qui falsifie également la deuxième source. Un `0` d'erreur après refus massifs ne signifie pas que Brody sait reconnaître les images falsifiées. Il faudra ensuite brancher la véritable provenance autorisée d'Obsidia / F16 et les verdicts de gouvernance, jamais laisser le demandeur définir lui-même `independent_verified`.

## Campagne PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f13_provenance_guard_audit_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F13 incorrecte" }
py -m unittest discover -s tests -p "test_fusion_f13*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F13 échoués" }
py -m brody_world_physique.fusion_f13_provenance_guard_audit_v0 --cases 1000 --out "build\fusion-f13-trust-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne F13 échouée" }
$report=Get-Content "build\fusion-f13-trust-001\report.json" -Raw | ConvertFrom-Json
$report | Select-Object cases,old_wrong_total,accepted_wrong_total,hold_total,corroborated_total
$report.families | Format-List
```

## Étape suivante
1. Vérifier l'intégrité des reçus et le passage de toutes les suites F8–F13.
2. Raccorder le gate à l'enveloppe de provenance effective d'Obsidia, et refuser toute attribution sans ancre vérifiée.
3. Augmenter le fuzzing sur des indices perturbés, doubles sources falsifiables, temporalité et composition ; mesurer faux refus et fausses validations séparément.
