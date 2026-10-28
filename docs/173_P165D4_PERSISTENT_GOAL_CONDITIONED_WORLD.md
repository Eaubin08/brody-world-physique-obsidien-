# 173 — P165-D4 : représentation persistante du monde et attention orientée par le but

## Vision de l'utilisateur (origine)
Le monde ne se limite pas aux pixels : cartographie Wi-Fi/ondes, spectres acoustiques, radar/infra, météo, angles de vue, mouvement et vitesse, couches 2D/3D, expérience acquise et perception humaine sélective. Un objet visuellement masqué reste une **hypothèse persistante** ; la représentation détaillée dépend de la demande et du but. L'utilisateur propose que le manque principal soit la représentation plutôt que le simple nombre de tests.

## Contrat implémenté dans cette première tranche
`brody_world_physique/persistent_world_state_p165d4.py` et tests associés :
- Etat `UNINITIALIZED` puis `OBSERVED` ; temps et positions 1D numériques, avec source de provenance.
- Propagation `PREDICTED` pendant absence de mesures selon **hypothèse vitesse constante** ; incertitude croissante avec la durée (croissance jouet, sans calibration probabiliste).
- Réapparition contradictoire : note `POSITION_PREDICTION_MISMATCH`, **sans** réécrire le passé pour cacher l'erreur.
- Rejet des mesures de provenance `GENERATED`/`INFERRED` et des référentiels non alignés.
- Vues sélectives `AVOID_COLLISION`, `REIDENTIFY`, `RENDER`, `EXPLAIN`. Chaque vue lit un sous-ensemble d'un même état ; elle ne modifie pas la vérité.
- SIX fixtures numériques : occlusion, réapparition cohérente, réapparition inattendue, génération non probante, mauvais référentiel, délai sans observation.
- Les preuves sont écrites dans `EXAMS.jsonl` et `MASTER_REPORT.json` dans un dossier neuf, sans écrasement.

## Limites factuelles
- **Données 1D synthétiques et événements explicitement fournis par l'examen.** Pas de capteur Wi-Fi/CSI, radar, LiDAR, thermographie, spectre ou météo réellement connecté.
- Pas de perception depuis des pixels, pas de graphe de scène 3D, pas d'identité multi-objet, pas de collision modélisée ni d'apprentissage autonome.
- La vitesse initiale est dérivée de deux observations ; les événements non observés sont hypothèses, pas vérités.
- La dérive croissante de l'incertitude exprime une règle heuristique. La mesure peut être fausse, le modèle physique insuffisant et le monde partiellement indiscernable.
- Une disparition de la caméra ne signifie ni disparition de l'objet ni mesure garantie par les ondes.
- Les tests ne prouvent pas la continuité d'identité ni la causalité des anomalies observées.
- Contrat gouverné : `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

## Etape suivante après validation
Brancher une sortie d'observation P165-D3 (positions candidates **et provenance/visibilité**, plusieurs pistes) sur l'état persistant ; placer repères/temps à l'interface ; exploiter le graphe P165-C et les signatures P165-B sans leur donner artificiellement des valeurs de capteurs absents ; comparer plusieurs modèles dynamiques en cas de contradictions et évaluer en aveugle sur P165-A et les 675 configurations HARD+++.

## Commande Windows PowerShell
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/persistent_world_state_p165d4.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P165-D4 échouée" }
py -m unittest discover -s tests -p "test_persistent_world_state_p165d4.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P165-D4 échoués — STOP" }
py -m brody_world_physique.persistent_world_state_p165d4 --out "build\brody-p165d4-persistent-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P165-D4 échouée" }
Get-Content "build\brody-p165d4-persistent-001\MASTER_REPORT.json"
```

**Verdict pré-validation :** `P165D4_WORLD_STATE_LAB_PUBLISHED / GOAL_CONDITIONED_VIEWS / REAL_MULTISENSOR_AND_3D_PENDING / PC_VALIDATION_PENDING`.
