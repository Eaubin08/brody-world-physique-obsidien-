# Brody — mouvement observé, génération d'image suivante, correction V1

Grande passe orientée physique *apprise depuis une observation*, sans prétendre découvrir les lois de Newton : `image_observed_motion_school_v1.py` reçoit une séquence de **3 images ou plus** d'un objet sombre sur fond clair, chaque image accompagnée de son temps d'observation. Il calcule le centre des pixels sombres, une taille apparente et une trajectoire, ajuste un modèle local d'accélération 2D sur les trois dernières positions, prévoit la position suivante et **dessine** une image `predicted_next.png` 64×64. Après réception d'une image réellement observée à cet instant (`--feedback`), il mesure l'écart de position et **réajuste** le modèle candidat avec l'observation nouvelle. La prédiction initiale demeure immuable. Les deux modèles et l'erreur sont conservés dans un artefact à digest.

L'accélération n'est **pas** fixée à 9,81 : la trajectoire et l'accélération sont inférées à partir des positions mesurées. Le *choix de la famille quadratique* (accélération constante) est cependant une hypothèse programmée. Le système ne connaît ni la gravité, ni l'identité de la balle, ni la profondeur, ni la vitesse réelle en mètres/seconde. Il repose sur une segmentation heuristique (objet sombre, fond clair) et suppose un seul objet suivi ; en cas de fond complexe, plusieurs objets ou occultation, le résultat n'est pas fiable. Le modèle est un premier outil de la boucle perception → modèle → anticipation → génération → erreur → correction. Cette étape ne sait pas encore détecter les collisions, changements de loi ou mettre en doute le modèle physique. Aucune action KX108, Native Memory, promotion canonique. Résultats PC encore non vérifiés.

## Tests

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_observed_motion_school_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests mouvement échoués" }
```

## Expérience de 4 images indépendantes

Préparer trois images `frame0.png`, `frame1.png`, `frame2.png` (fond blanc, balle sombre, positions réellement successives ; aucun besoin de savoir le mot « gravité »). Indiquer les temps dans un manifeste `build\\brody-motion-lesson.json` :

```json
{
  "observations": [
    {"t": 0, "file": "build/frames/frame0.png"},
    {"t": 1, "file": "build/frames/frame1.png"},
    {"t": 2, "file": "build/frames/frame2.png"}
  ],
  "predict_t": 3
}
```

Premier passage (sans révéler la quatrième image) :

```powershell
py -m brody_world_physique.image_observed_motion_school_v1 --manifest "build\brody-motion-lesson.json" --out "build\brody-motion-001"
```

Ensuite seulement, comparer à une vraie observation `frame3.png` en relançant dans un **nouveau dossier** (les preuves précédentes ne sont jamais écrasées) :

```powershell
py -m brody_world_physique.image_observed_motion_school_v1 --manifest "build\brody-motion-lesson.json" --feedback "build\frames\frame3.png" --out "build\brody-motion-corrected-001"
```

Comparer `predicted_next.png`, `MASTER_REPORT.json` et `candidate_motion_memory.json`. La même image de feedback ne doit pas déjà exister dans les observations de cours (SHA refusé). Le reçu de la prévision initiale et le modèle corrigé se trouvent côte à côte ; la correction ne réécrit pas le passé.

À construire ensuite : mise en mémoire inter-sessions pour plusieurs trajectoires ; segmentation à objets multiples ; hypothèses en concurrence pour accélération, vitesse constante, rebond, disparition ; tests de mouvement réel hors des exemples artificiels ; génération de séquences plus fines et apprentissage 360°/profondeur. Aucune preuve de compréhension physique générale n'est revendiquée.
