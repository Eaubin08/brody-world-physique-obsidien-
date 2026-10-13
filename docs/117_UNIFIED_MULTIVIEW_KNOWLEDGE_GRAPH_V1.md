# Brody — unification du savoir multi-vues V1 (candidat)

L'identité enseignée n'est plus décomposée en connaissances indépendantes selon la perspective. Un graphe local regroupe `identity` (assignée dans un manifeste professeur), ses observations, propriétés, parties visibles, relations spatiales, transformations 2D et leçons. `knowledge_graph_candidates.json` est un artefact documentaire avec `digest`; les observations sont accompagnées de reçus chaînés. Les vues originales et miroir sont des **cours**, 90° et 180° des **examens** : le moteur n'utilise pas les examens pour stabiliser un nouveau réflexe.

Le graphe est distinct du moteur souverain Obsidia. Un groupe d'identité déclaré reste **candidat non authentifié**. Le même fichier sous plusieurs rotations ne prouve ni reconnaissance indépendante, ni monde 3D. Les mécanismes de mémoire stable sont pour l'instant un premier lien procédural local (procédure `raw` pour le contexte identité) ; les relations d'objets, invariants et la vérification inter-runs restent à construire. Une seule image initiale produit au plus deux cours sous transformations, pas trois expériences indépendantes : le savoir ne doit pas être présenté comme stabilisé.

Exécution PC avec le manifeste déjà créé :

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_unified_multiview_knowledge_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
py -m brody_world_physique.image_unified_multiview_knowledge_v1 --manifest "build\brody-multiview-manifest.json" --out "build\brody-unified-knowledge-001"
if ($LASTEXITCODE -ne 0) { throw "Unification échouée" }
Get-Content "build\brody-unified-knowledge-001\MASTER_REPORT.json"
```

**Prochaines frontières :** plusieurs images indépendantes d'un objet, correction professeur authentifiable, connaissance stable à travers la diversité réelle des sources, désambiguïsation de plusieurs objets semblables, capacité à douter localement sur 2–3 hypothèses, suivi inter-séances et provenance du contenu récolté automatiquement. Le nombre d'arêtes du graphe n'est pas un score d'intelligence.
