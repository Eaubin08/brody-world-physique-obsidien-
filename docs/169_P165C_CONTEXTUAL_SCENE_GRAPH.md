# 169 — P165-C Graphe relationnel de scène, provenance multimodale

**Statut : laboratoire publié, exécution PC en attente.**

## Intention conservée
L'utilisateur demande une représentation du monde par contexte de fond, plans éventuellement multiples mais non figés, objets, événements, signatures multispectrales/acoustiques, radar, infra, LiDAR, etc. La scène ne doit pas être réduite à trois couches constantes.

## Livrable de ce jalon
- `brody_world_physique/contextual_scene_graph_p165c.py` : `node` (entité candidate, observations, temps, repère), `edge` (relations contextuelles candidates), `assess` (contradictions explicites), `fuse_scene` (relations + règles de signatures P165-B), `run` (preuves append-only dans un dossier nouveau).
- `tests/test_contextual_scene_graph_p165c.py` : 7 tests unitaires.
- Relations illustratives : `IN_FRONT_OF`, `BEHIND`, `OCCLUDES`, `OVERLAPS`, `UNKNOWN`. Il s'agit d'arêtes locales et non d'une pile de profondeur en trois plans.
- 7 cas synthétiques : ordre d'occultation, profondeur inconnue, ordre contradictoire, caméra non résolue, conflit modal, signatures identiques non suffisantes, repères incompatibles.

## Garde méthodologique
La réussite d'un `SCENE_CANDIDATE` **ne prouve pas** qu'un objet est réellement devant un autre. Pour l'instant les arêtes sont construites directement par la fixture et la fusion compare des vecteurs artificiels. Aucune extraction de relations depuis pixels/images naturelles ; aucune estimation métrique de profondeur ; aucune calibration réelle de capteur. Le module illustre la **grammaire et l'interdiction de promotion**, pas un SLAM, pas une perception multispectrale réelle, pas la compréhension physique complète. Le graph P165-C ne se branche pas encore automatiquement au tracker P164 ni au rendu/reverse.

Noter distinctement :
1. **Relation spatiale candidate** (topologie des objets) ;
2. **Comparabilité des signatures** (mode, temps, source, référentiel, qualité) ;
3. **Identité** (toujours non démontrée dans cette première version) ;
4. **Causalité du mouvement caméra/objet** (toujours hypothèse) ;
5. **Profondeur métrique** (non prouvée par ordre avant/arrière).

Aucun résultat P165-B validé sur neuf cas ni P165-A sur 150 ni les 77 cellules historiques n'est changé/rerun par cette passe.

## Commande PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/contextual_scene_graph_p165c.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P165-C échouée" }
py -m unittest discover -s tests -p "test_contextual_scene_graph_p165c.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P165-C échoués — STOP" }
py -m brody_world_physique.contextual_scene_graph_p165c --out "build\brody-p165c-scene-graph-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P165-C échouée" }
Get-Content "build\brody-p165c-scene-graph-001\MASTER_REPORT.json"
```

**Verdict avant run :** `P165C_SCENE_GRAPH_LAB_PUBLISHED / RELATIONAL_AND_MODAL_CONTRACTS / REAL_PERCEPTION_PENDING / PC_TEST_PENDING`.

`native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.
