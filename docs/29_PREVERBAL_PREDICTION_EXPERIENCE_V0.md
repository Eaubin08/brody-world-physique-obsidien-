# 29 — Brody Image : première anticipation préverbale mesurable (F12/MMonde)

**Date :** 2026-10-08. **Phase :** instrument d'expérimentation du World Model.  
**Statut :** **code et tests synthétiques implémentés** ; **apprentissage physique réel et transfert entre scènes non validés**.

Voir [28 — expérience avant les mots](28_APPRENTISSAGE_PREVERBAL_MONDE_PHYSIQUE.md) et [27 — réciproque / savoir](27_REVERSO_WORLD_MODEL_APPRENTISSAGE_SELECTIF.md). Cette réalisation ne vise ni la rédaction d'une meilleure description Qwen ni un nouveau moteur graphique.

## Pourquoi cette étape

L'utilisateur veut que Brody anticipe ce qu'un objet va faire **avant de savoir le nommer**. Pour le tester sans confondre langage, pixels et physique, il faut un protocole dans lequel le modèle reçoit trois positions observées et **doit prévoir la quatrième avant d'y avoir accès**.

Le contrat source Obsidia F12 [`TimeEnvelopeV0`, `SpatialFrameRefV0`, `TransitionV0`, `TrajectoryV0`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/world_dynamics/contracts_v0.py) **représente** temps, cadre et transitions, mais ne calcule pas de prédiction. MMonde [`WorldObservationV0`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/mmonde/contracts_v0.py) porte les observations. **On les réutilise**, sans créer de nouveau `WorldState` racine.

## Ce qui est codé

[`brody_world_physique/preverbal_prediction_v0.py`](../brody_world_physique/preverbal_prediction_v0.py) fournit :

- `PositionMeasurementV0` : vue **dérivée**, non canonique, d'une position sourcée (objet, temps, repère, unité, nature de la source) ;
- `measurement_from_mmonde_world_observation()` : extraction stricte depuis un objet déjà conforme aux champs MMonde `state.position.{x,y,unit}`, `space.frame_ref`, `observed_at` avec fuseau et `source_refs` ; elle n'altère pas MMonde et ne suppose pas que tout WorldObservation possède un point mesuré ;
- `predict_from_three()` : prend **exactement trois observations passées**, extrapole les positions X/Y à partir des différences temporelles sous une hypothèse *locale d'accélération constante*, et calcule également deux contrôles : vitesse constante et position inchangée ;
- `evaluate_with_heldout()` : reçoit **ensuite**, séparément, la quatrième mesure et compare les erreurs spatiales, sans attribuer automatiquement une cause physique ;
- `evaluate_four_measurements()` et CLI : protocole en une commande pour fichier JSON avec **3 mesures d'historique + 1 mesure cachée à la fonction de prédiction**.

Ce modèle numérique est un **benchmark expérimental**, pas un modèle du vent, de la gravité, de la biologie ni une IA qui a appris la loi du monde. Un résultat ponctuel correct ne suffit pas à « apprendre » ou à établir une vérité.

### Contraintes non négociables

- Référence de source et identité de l'objet requises pour chaque position.
- Les unités et le **référentiel spatial** doivent être les mêmes ; mélange `px` / `m` ou caméra fixe / mobile : rejet. Une étiquette de repère ne prouve pas, à elle seule, que la caméra était vraiment immobile : **à auditer séparément**.
- Chronologie strictement croissante ; sortie future indépendante de la position future ; ref de la frame d'évaluation distincte.
- `OBSERVED_CLAIM`, `SIMULATED`, `GENERATED` restent distincts. Une `OBSERVED_CLAIM` **n'est jamais promue automatiquement en preuve physique réelle**.
- Aucun lien automatique vers Native Memory, Broker/Binder, modèle Qwen ou décision KX108. Tout le pipeline est **read-only / candidate**.

## Lancer maintenant, sans modèle à installer

Sur ton portable ou PC fixe, depuis le bon dépôt Brody Image :

```powershell
git pull --ff-only origin main
py -m unittest discover -s tests -p "test_*.py" -v

# Démonstration entièrement SYNTHÉTIQUE, sans réseau ni accès caméra :
py -m examples.demo_preverbal_world_v0 --out build/preverbal-world-demo

# Ré-évaluer explicitement ces positions d'essai :
py -m brody_world_physique.preverbal_prediction_v0 --input build/preverbal-world-demo/source_measurements.json --out build/preverbal-world-demo/verified.json
```

Fichiers : `source_measurements.json`, `heldout_evaluation.json`, `verified.json`. Les résultats comportent l'erreur du prédicteur et de deux baselines, l'indication d'une seule expérience et les limites de preuve.

## Prochaine épreuve RÉELLE (encore non exécutée)

1. Dans Jarvis/CameraRig ou un clip réel, suivre **un même objet visible** sur au moins quatre instants correctement horodatés. Réutiliser une extraction existante (OpenCV/Jarvis/outil choisi) ; **Qwen-VL seul ne fournit pas les positions de référence avec précision garantie**.
2. Fournir les positions `x,y` sourcées et le référentiel de caméra dans le contrat de vue ; contrôler manuellement au moins une séquence témoin, exclure le mouvement de caméra non mesuré.
3. Envoyer les trois premières positions au prédicteur, garder la suivante indépendante, mesurer l'écart ; comparer à la vitesse constante et à l'absence de mouvement.
4. Faire varier la taille, l'objet, la caméra ou une condition physique et répéter le test **sans réutiliser le même résultat comme validation**. Tester ainsi le transfert et les limites : ce qui améliore une vidéo ne doit pas être proclamé vrai pour tout le monde physique.
5. Relier les expériences validables à la représentation objet/temps/position MMonde et à [l'apprentissage sélectif](27_REVERSO_WORLD_MODEL_APPRENTISSAGE_SELECTIF.md). Conserver le contexte et la décision de revue, **aucune écriture mémoire sans gate**.

**Lien avec Reverso :** l'aller-retour pixel exact garde un témoin sur la source ; l'anticipation spatio-temporelle teste une autre compétence. Il faut les relier par source, objet et repère **sans réduire le world model à des pixels ni faire passer les données de simulation pour la réalité**.

**Le test de transfert, la prise de mesures vidéo réelles, l'intégration F16/F12/MMonde de bout en bout et le modèle apprenant restent `NOT_RUN`.**
