# 90 — F6 : choix d'instrument historique V2 raccordé à F5/F4

**Branche expérimentale uniquement. Statut : code publié, validation locale PC en attente.**

## Causalité effective du test
Cette étape raccorde les deux écoles EXISTANTES plutôt que réinventer l'apprentissage :
1. F5 apprend trois formes (rectangle, triangle, ellipse), historise les compétences candidates dans F3c et les événements dans F4.
2. L'école V2 historique `instrument_school_v2.run_school` enseigne séparément neuf épisodes TRAIN (LIGHT, UNIFORM, EXPRESSIVE, trois formes) après vérification de son bundle V1.
3. Le pont F6 vérifie le résultat V2, lit ses épisodes TRAIN figés, choisit la forme via F5 et l'outil via `select_tool` de V2. Le but inconnu reste HOLD.
4. Le pont récupère réellement les gestes du snapshot F3c avec `p211b.read` et dessine via `render_instrument` de V2 ; un reçu `sealed_choice.json` est écrit avant de produire la cible professeur.
5. Le résultat de l'examen est mesuré puis enregistré dans le journal éducatif F4, sans modifier la compétence candidate ni promouvoir le score TEST.
6. Les PNG `candidate.png`, `teacher-after-seal.png`, `comparison.png` sont conservés pour chacun des trois examens connus.

## Ce que ce test ne doit PAS prétendre
- Les deux entraînements V2 (instrument) et F5 (formes) restent historiquement **séparés** ; F6 démontre leur raccordement pendant le choix et la génération, pas une mémoire native Obsidia fusionnée.
- Le choix V2 s'appuie sur une intention de style **déclarée** et ses erreurs moyennes TRAIN, pas sur une interprétation autonome de l'image.
- Le professeur synthétique génère les styles sur la même géométrie gestuelle que l'élève : **ce banc mesure surtout la sélection/rendu des instruments**, pas la précision de reconstruction des objets.
- PENCIL/PEN/NIB sont des moteurs de tracés simulés ; aucun pinceau physique ni peinture multicouche.
- Pas de MEMZUM, de correction progressive du geste, ni d'écriture Native Memory ; `KX108_ONLY` inchangé.
- Si V2 instrument-school échoue sur les versions locales de code, le pont échoue aussi : ne pas transformer l'échec en PASS documentaire.

## Tests PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }

py -m unittest discover -s tests -p "test_fusion_f6*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F6 échoués" }

py -m unittest discover -s tests -p "test_fusion_f5*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Régression F5" }

py -m brody_world_physique.fusion_f6_instrument_education_v0 --out "build\fusion-f6-tools-001"
if ($LASTEXITCODE -ne 0) { throw "Démo F6 échouée" }

Get-Content "build\fusion-f6-tools-001\summary.json"
Invoke-Item "build\fusion-f6-tools-001\exam-02-triangle\comparison.png"
```

Lancer avec `-002` en cas de reprise pour conserver les anciennes traces.
