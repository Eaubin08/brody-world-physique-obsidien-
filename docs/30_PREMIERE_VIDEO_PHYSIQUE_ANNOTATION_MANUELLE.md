# 30 — Première vidéo observée : quatre instants, première prévision précommittée

**Statut 2026-10-08 :** entrée vidéo OpenCV + annotation utilisateur implémentée et tests avec faux décodeur ; **AUCUNE vidéo physique réelle n'a encore été testée par le projet**. La provenance doit maintenant être indiquée explicitement via `--source-kind` : `SIMULATED` pour la vidéo de test, `GENERATED` pour un rendu génératif, `OBSERVED_CLAIM` pour une prise de vue prétendue réelle, qui n'est pas automatiquement certifiée. Aucun modèle neuf ni changement au kernel.

## Raison et origine

Après [29](29_PREVERBAL_PREDICTION_EXPERIENCE_V0.md), le test synthétique de l'utilisateur a répondu
`source_kind=SIMULATED`, `BETTER_THAN_LINEAR_BASELINE`,
`error_proposed=0.0` et `physics_understood=False`. Le résultat valide
**un calcul sur une trajectoire construite**, pas la compréhension de la chute réelle.

La méthode décrite par l'utilisateur est : **observer et essayer avant de nommer, anticiper une conséquence, confronter la prédiction au réel, apprendre ce qui change/reste stable et transférer sans réinventer le décodage du monde**. [28](28_APPRENTISSAGE_PREVERBAL_MONDE_PHYSIQUE.md) garde cette doctrine. Ici, on passe de quatre positions *inventées* à **quatre instants d'une vidéo choisie**.

## Réutilisation, sans réinstaller un œil

Jarvis fournit déjà un organe OpenCV dans
[`src/jarvis/integrations/opencv_camera.py`](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/fix/qwen-live-main-20261007/src/jarvis/integrations/opencv_camera.py) ;
ce fournisseur sert à capturer **une frame** et n'est pas un tracker complet.
Le nouveau module [`video_observation_v0.py`](../brody_world_physique/video_observation_v0.py) utilise la **bibliothèque OpenCV si elle est disponible dans l'environnement Python courant**, mais ne copie pas le CameraRig, ne connecte pas un service réseau et ne prétend pas utiliser les processus en cours de Jarvis.

L'utilisateur indique *au clic* la position du **même objet** dans les quatre images. Le suivi humain remplace **provisoirement** une segmentation/tracking automatique : on ne masque pas ce manque avec la description textuelle de Qwen.

## Séquence et frontière anti-triche

1. Un clip local MP4/AVI/MOV (selon codecs pris en charge par OpenCV). La vidéo est lue localement; son SHA-256 est enregistré, elle n'est pas envoyée sur GitHub.
2. Choix de 4 indices de frames, espacés suivant `--start-seconds` et `--interval-seconds`, en utilisant le FPS annoncé par le décodeur (à qualifier).
3. L'utilisateur clique **le centre d'un même objet** dans les frames 1, 2, 3.
4. Le prédicteur de [29](29_PREVERBAL_PREDICTION_EXPERIENCE_V0.md) reçoit exclusivement ces 3 positions. **Avant d'afficher la frame 4**, le programme enregistre `prediction_before_frame_4.json`. La prédiction est ainsi précommittée avant l'annotation du résultat.
5. L'utilisateur clique le même objet dans la frame 4, alors inconnue du prédicteur.
6. L'outil calcule les erreurs contre la 4e position et contre les baselines vitesse constante et immobilité.
7. Reçus locaux `source_measurements.json`, `heldout_evaluation.json` : clip hash, indices, FPS fourni par le décodeur, identification/position manuelles, caméra et temps réels **non vérifiés**, aucune causalité ou savoir promus.

### Usage Windows (PC fixe avec Brody Image)

Mettre le dépôt à jour, puis regarder si **OpenCV existe déjà dans le même Python** :

```powershell
git pull --ff-only origin main
py -c "import cv2; print('OpenCV present:', cv2.__version__)"
```

Si la seconde commande dit `ModuleNotFoundError: cv2` : **ne pas réinstaller Jarvis/Qwen-VL**. Retrouver d'abord quel environnement Python est utilisé par Jarvis ; à défaut, `opencv-python` est une bibliothèque de traitement d'image, **pas un nouveau modèle d'IA**.

Filmer ou choisir un clip court d'une **balle ou objet visible** qui se déplace, avec **caméra immobile** si possible (2–5 secondes suffisent). Le mouvement devrait commencer avant la 1re frame sélectionnée et rester visible pendant 4 frames espacées de 0,1 s environ.

Dans PowerShell :

```powershell
Add-Type -AssemblyName System.Windows.Forms
$d = New-Object System.Windows.Forms.OpenFileDialog
$d.Filter = "Vidéos|*.mp4;*.avi;*.mov;*.mkv"
if ($d.ShowDialog() -eq "OK") {
  $out = "build\\video-reelle-$(Get-Date -Format yyyyMMdd-HHmmss)"
  py -m brody_world_physique.video_observation_v0 --video $d.FileName --out $out --interval-seconds 0.1 --source-kind SIMULATED
}
```

Une fenêtre OpenCV s'ouvre **quatre fois** : cliquer le centre de la balle, vérifier la croix, puis appuyer sur **Entrée**. `R` réinitialise la sélection, `Échap` annule. Si l'on choisit une vidéo physique personnelle au lieu de la simulation, remplacer `--source-kind SIMULATED` par `--source-kind OBSERVED_CLAIM` ; cela ne prouve pas l'authenticité de la vidéo. Si la balle n'apparaît pas sur la frame 1, relancer avec `--start-seconds 0.5` (ou autre valeur). Si les frames se répètent ou sont trop rapprochées, ajuster `--interval-seconds` en fonction de la vidéo. Le fichier original n'est ni modifié ni publié.

**Interprétation honnête :** le module ne sait pas dire seul « ceci est une balle », ne mesure ni le GPS, ni la force, ni le vent. Il prédit seulement une position dans le plan image `px` à partir d'annotations humaines. C'est une observation *candidate* ; on doit encore auditer mouvement de caméra, erreur d'annotation, temps FPS, occlusions et identité du sujet.

## Prochains critères après cet essai

- Répéter plusieurs fois le même essai, puis sur des objets/situations différents, en gardant réellement une quatrième observation inaccessible lors de la prédiction.
- Raccorder chaque frame avec ses références aux contrats **F16/MMonde/F12** déjà présents en amont. Actuellement, ce module ne fabrique qu'une **vue dérivée de positions et de provenance**.
- Ajouter comparaison humaine/témoin indépendant, puis un tracker existant si un besoin réel est confirmé.
- Construire un **modèle de transition capable d'améliorer ses prédictions grâce à l'expérience** ; le prédicteur actuel est une extrapolation prédéfinie qui **n'apprend pas**.
- Tester enfin si l'ajout de signaux physiques (caméra, profondeur, GPS approprié, vent mesuré) améliore le score hors échantillon.

**Doctrine :** ne pas appeler `PASS` physique un test synthétique ou manuel à lui seul ; `KX108_ONLY`, aucune modification de mémoire/native weights automatiquement.

## Diagnostic du premier essai vidéo (sortie utilisateur)

Sur le run `build/video-test-20261008-204125`, erreurs : candidat **628,47 px**, vitesse constante **321,02 px**, position immobile **227,54 px**. Le modèle est **WORSE_THAN_LINEAR_BASELINE** ; il ne faut ni apprendre une loi ni modifier les poids. Pour la vidéo simulée distribuée pour cet exercice, les images 0, 3, 6 et 9 montrent approximativement des positions de centre `(276,106)`, `(281,109)`, `(286,116)`, `(291,129)` en pixels natifs. Cet écart indique un **problème probable dans la sélection des points, la vidéo effectivement choisie ou les coordonnées d'affichage**, à confirmer avec `source_measurements.json`. Aucune hypothèse sur le vrai fichier choisi ne doit être présentée comme un fait. Le premier outil acceptait les clics sans confirmation ; désormais la sélection est visible et confirmée explicitement. Anciennes sorties `OBSERVED_CLAIM` d'une vidéo simulée doivent être traitées comme provenance insuffisante.
