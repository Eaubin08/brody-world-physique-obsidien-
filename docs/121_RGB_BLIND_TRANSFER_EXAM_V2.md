# Grande passe Brody — V2 : couleur, géométrie et examen à l'aveugle séparé

Cette version conserve l'école V1 inchangée et ajoute trois opérations indépendantes :

1. `train` : un professeur déclare des identités et leurs fichiers de cours dans un JSON. Une mémoire candidate comporte la **grille RGB 4×4**, le nombre de composantes sombres et le contexte structurel. Deux fichiers identiques ne valent pas deux expériences ; un même fichier ne peut appartenir à deux identités enseignées.
2. `exam` : on fournit **seulement** les nouvelles images et la mémoire candidate, **pas le JSON des corrections**. Le moteur calcule la distance descriptive, produit soit `CANDIDATE` soit `DOUBT`, avec trois hypothèses maximum, et scelle chaque prédiction dans `sealed_predictions.jsonl`. Identité de professeur strictement absente de cette opération. Rejet des octets d'image identiques à un cours.
3. `grade` : **dans une autre invocation** et après fermeture des résultats, le professeur fournit les réponses correctes `labels.json` ; rapport correct/wrong/doubt/unlabeled sans modifier la mémoire ni les résultats scellés.

## Exécution Windows — tests

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_real_transfer_exam_v2.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

## Campagne indépendante réelle

Préparer `build\\brody-v2-lessons.json` comme une liste : `[{"identity":"objet-A","examples":["C:\\images\\A1.png","C:\\images\\A2.png"]},{"identity":"objet-B","examples":["C:\\images\\B1.png"]}]`.

Préparer ensuite **un dossier différent** contenant des photos d'examen nouvelles et **distinctes des cours** : `build\\brody-v2-exam-images`.

```powershell
py -m brody_world_physique.image_real_transfer_exam_v2 --mode train --lessons "build\brody-v2-lessons.json" --out "build\brody-v2-memory.json"
py -m brody_world_physique.image_real_transfer_exam_v2 --mode exam --memory "build\brody-v2-memory.json" --images "build\brody-v2-exam-images" --out "build\brody-v2-blind-001"
```

**Seulement après l'examen**, préparer `build\\brody-v2-answer-key.json` comme dictionnaire relatif des chemins d'examen : `{"image-A-test.png":"objet-A","image-B-test.png":"objet-B"}`. Puis :

```powershell
py -m brody_world_physique.image_real_transfer_exam_v2 --mode grade --predictions "build\brody-v2-blind-001" --labels "build\brody-v2-answer-key.json" --out "build\brody-v2-grade-001.json"
```

**Interprétation :** les tests unitaires vérifient uniquement que le protocole fonctionne. Aucune généralisation ni reconnaissance réelle n'est établie avant de fournir plusieurs sources photographiques indépendantes, d'autres objets ressemblants et les résultats gradés. La distance RGB 4×4 n'est pas un réseau multimodal et reste fragile aux variations d'éclairage, cadrage, arrière-plan et point de vue. Les groupes d'identité sont enseignés, non découverts. Aucune enquête Internet, aucun modèle de causalité, aucune connaissance physique ou inférence 3D dans cette passe. Les résultats restent des candidats locaux ; `native_memory_write=False`, `canonical_promotion=False`, `KX108_ONLY`.

**Prochaine intégration** : véritables séries multiangle/vidéo, enseignant vérifiable, cours de transfert avec négatifs difficiles, propriétés RGB au graphe de connaissances, diagnostic ciblé des erreurs et mémoire de correction persistante. La couleur et la séparation examen/correction constituent ici la progression réelle.
