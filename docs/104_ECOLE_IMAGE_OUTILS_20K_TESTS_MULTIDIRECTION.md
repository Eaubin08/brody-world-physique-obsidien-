# École Image & Outils — campagne unique 10 000 leçons + 10 000 examens

**Produit prioritaire :** capacités de Brody à expérimenter, comparer et choisir les outils image existants. Aucune autorité supplémentaire, aucune écriture mémoire native, aucune modification d'Obsidia ou de `main`.

## Réutilisation, pas de nouvelle école parallèle
- `fusion_f9_intensive_education_v0.run` : entraînement réel du routeur instrumental, états des 12 contextes forme/style, correction EWMA, examen à l'aveugle et snapshots hashés.
- `drawing_school_v1.GestureV1` : représentation des gestes existante.
- `instrument_school_v2.render_instrument` : 3 outils informatiques simulés (PENCIL/PEN/NIB), pas de simulation de leur physique réelle.
- `verify_chain` : empreintes et chaîne des reçus.
- Nouvelle orchestration `image_tool_school_20k_campaign_v0.py` : une campagne avec un rapport commun et des familles différenciées.

## Programme
10 000 leçons d'entraînement réparties sur les 3 objectifs d'encrage et 4 familles de gestes. Snapshots + examens aveugles périodiques; figer le dernier modèle de routage avant l'examen final.

10 000 tests séparés, **1 000 par famille** :
1. géométries inédites
2. translation
3. symétrie miroir
4. rotation 90°
5. contraste réduit
6. flou
7. bruit de capteur *simulé*
8. masquage partiel
9. consigne trompeuse (contradiction intention / cible)
10. intention inconnue (abstention attendue)

Dans chaque test, le candidat est généré avant la cible d'évaluation. Toute perturbation stochastique emploie une graine fixe commune à toutes les propositions et à la cible. Rapport par famille: nombre évalué, abstentions, erreur pixel moyenne, regret face au meilleur outil oracle, concordance oracle. Les tests contradictoires ne sont pas comptés comme succès sans examen différencié.

## Commande PowerShell unique

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\image_tool_school_20k_campaign_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe invalide" }
py -m unittest discover -s tests -p "test_image_tool_school_20k_campaign_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests d'infrastructure échoués" }
py -m brody_world_physique.image_tool_school_20k_campaign_v0 --train 10000 --exams 10000 --checkpoint 1000 --out "build\brody-image-school-20k-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne image échouée : conserver sortie et trace" }
Get-Content "build\brody-image-school-20k-001\MASTER_REPORT.json"
```

## Frontières
Ceci teste **le choix d'outils de dessin sur images synthétiques 64×64**, ni apprentissage physique réel, ni perception Qwen-VL réelle, ni vidéo, ni génération libre, ni indépendance d'évaluation (moteur de rendu partagé). Ne pas déduire des scores synthétiques que les mécanismes multivues, 360°, réciproques, physiques ou cognitifs sont démontrés. Ce premier batch de 20 000 mesures est une base contrôlée ; la même campagne maître devra ensuite recevoir des jeux de données réels, des scènes physiques et une évaluation indépendante. Comparer `mean_regret` et `holds` *par famille*, surtout consigne trompeuse, masque et inconnus. Prévenir tout faux PASS global.
