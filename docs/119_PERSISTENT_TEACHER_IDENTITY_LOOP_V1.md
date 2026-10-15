# Brody — boucle enseignement des identités candidates persistantes V1

Cette étape relie l'examen sans étiquette à une mémoire expérimentale **persistante entre sessions**. Avant tout feedback, le moteur lit l'image, compare avec les observations déjà enseignées et scelle sa proposition (ou un doute limité à 3 hypothèses). Ensuite seulement, l'étiquette du professeur est utilisée pour **ajouter** une observation à la même identité candidate. Les fichiers identiques ne sont pas des expériences indépendantes ; si le même contenu reçoit une identité incompatible, le conflit est mis en quarantaine sans effacer l'identité précédente.

Le fichier `identity_memory_candidate.json` contient les connaissances locales et leur digest ; utiliser `--previous` pour le cycle suivant. Le professeur est déclaratif et non authentifié, les propriétés sont des signatures 16 valeurs de pixels et non des concepts sémantiques ou des propriétés d'un objet 3D. L'identité reste candidate, jamais une vérité canonique. **Limite importante :** le module écrit son état seulement à la fin du run, contrairement à la boucle de leçons visuelles V1 qui dispose d'un checkpoint par leçon. Aucune intégration de recherche de données automatique dans cette étape.

## Tests sur le PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_persistent_identity_teacher_loop_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

Pour utiliser un exemple réel, écrire un JSON `[{"file":"chemin-vers-image.png","teacher_identity":"objet-A","teacher_ref":"professeur-ou-source"}]`, puis appeler `py -m brody_world_physique.image_persistent_identity_teacher_loop_v1 --exam chemin.json --out build\\brody-identite-cycle-001`. Pour une nouvelle leçon, créer un autre manifeste et appeler avec `--previous build\\brody-identite-cycle-001\\identity_memory_candidate.json --out build\\brody-identite-cycle-002`.

Les résultats à établir ensuite : vraie correction après erreur, stabilisation à travers vues variées réellement indépendantes, désambiguïsation de deux objets semblables, contrôle du professeur, sauvegardes pendant chaque run et graphe de savoir commun inter-écoles.
