# Brody — passe physique : plusieurs modèles, prévision scellée, mémoire de correction

Nouveau module `image_multihypothesis_motion_memory_v1.py` sur **branche expérimentale exclusivement**. Il reçoit quatre images 2D ou plus avec leurs horodatages et extrait les positions observées (un objet sombre sur fond clair). Trois hypothèses **définies à l'avance** sont comparées : STILL (immobile), VELOCITY (vitesse constante) et ACCELERATION (accélération constante). Le choix est établi sur une prédiction rétrospective du dernier point observé, à partir des points antérieurs. En cas d'égalité, DOUBT ; jamais plus de trois hypothèses. Il génère ensuite **trois images candidates distinctes** pour un instant ultérieur, et sauvegarde le résultat avant de voir l'image réelle.

La correction constitue une opération séparée : `feedback` vérifie l'empreinte du forecast, refuse le réemploi d'une image source, mesure les trois écarts en pixels et ajoute un épisode **local** à `candidate_experience_memory.json`. `--previous` permet de réimporter les épisodes du cycle précédent (duplicatas ignorés). Les prévisions initiales ne sont pas réécrites ; mémoire à digest et dossiers de sortie nouveaux.

**Ce n'est pas une découverte libre des lois physiques :** seules trois familles de modèles déjà codées sont en compétition. Une seule erreur rétrospective ne garantit pas la qualité du choix, le mécanisme de mémoire conserve des expériences mais n'ajuste pas encore automatiquement la sélection selon des contextes appris. Aucun rebond explicite, aucune segmentation multi-objet/3D, aucun rapport entre pixels et secondes/mètres réels. Les photographies réelles de scènes complexes restent hors preuve. Aucun accès à Native Memory, KX108 restant seul décisionnaire.

## Commande PC, validation de la passe

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_multihypothesis_motion_memory_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

## Expérience sur une séquence réelle

Créer un JSON `build\\brody-motion-four.json` :

```json
{"observations":[
 {"t":0,"file":"build/frames/frame0.png"},
 {"t":1,"file":"build/frames/frame1.png"},
 {"t":2,"file":"build/frames/frame2.png"},
 {"t":3,"file":"build/frames/frame3.png"}
],"predict_t":4}
```

Prévision initiale, **sans quatrième observation future** (`frame4.png`) :

```powershell
py -m brody_world_physique.image_multihypothesis_motion_memory_v1 --mode forecast --manifest "build\brody-motion-four.json" --out "build\brody-multimotion-forecast-001"
```

Révéler ensuite `frame4.png` pour comparer :

```powershell
py -m brody_world_physique.image_multihypothesis_motion_memory_v1 --mode feedback --forecast "build\brody-multimotion-forecast-001\sealed_forecast.json" --observed "build\frames\frame4.png" --out "build\brody-multimotion-feedback-001"
```

Au prochain cycle, passer `--previous "build\\brody-multimotion-feedback-001\\candidate_experience_memory.json"` et utiliser un dossier inédit. Les images de sortie `still.png`, `velocity.png` et `acceleration.png` montrent les trois anticipations. Le verdict d'un véritable transfert requiert plusieurs séquences indépendantes et des objets/situations différents.

**Statut : code publié, tests PC en attente.**
