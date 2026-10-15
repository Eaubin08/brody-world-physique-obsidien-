# Brody — Comparatif A/B physique à mémoire figée (passe 126)

## Objectif

Mesurer si le choix de modèle amélioré par mémoire de corrections V2 apporte **effectivement une diminution de l'erreur de prévision**, en comparaison avec le moteur sans cette mémoire, sur exactement les mêmes trajectoires inédites. Le script ne réentraîne pas pendant l'examen. L'analyse n'est pas une démonstration de connaissance physique universelle.

## Module

`image_motion_memory_ablation_v1.py`, `--cases` manifeste JSON de séquences nouvelles, `--memory` mémoire V2 vérifiée par digest, `--out` répertoire inédit. Le module procède ainsi :
1. Lit la mémoire `candidate_physics_memory.json` d'anciens épisodes corrigés, en lecture seule.
2. Charge pour chaque cas au moins quatre images successives et la cinquième observation de vérité (`actual`), avec horodatages croissants et instant `predict_t`.
3. **Avant de révéler la vérité au comparateur**, calcule les choix sans mémoire et avec mémoire, sur la même séquence. Les trois familles STILL, VELOCITY, ACCELERATION sont identiques des deux côtés.
4. Calcule ensuite l'erreur en pixels des modèles retenus à partir de l'image observée réservée.
5. Enregistre tous les résultats cas par cas dans `EVIDENCE.json` scellé et les statistiques dans `MASTER_REPORT.json`.

Le protocole refuse le réemploi d'images de cours connues de la mémoire ou du dernier cadre comme observation test. Il ne garantit pas à lui seul des scènes réellement indépendantes : ce point doit être vérifié au niveau de la préparation du corpus. La moyenne affichée est calculée **sur les seuls cas où un modèle a été choisi** et rapporte séparément les HOLD ; `mean_paired_advantage_px` couvre uniquement les cas **communs** sélectionnés par les deux méthodes. Une amélioration strictement positive signifie une différence observée dans cet échantillon, **pas une généralisation démontrée**. Des doublons perceptuels ou des scènes apparentées de manière non triviale peuvent fausser la mesure.

**Important :** les contextes `stationary`, `steady`, `speeding_up`, `slowing_down`, `reversal` sont déjà calculés dans la V2. La V2 ne possède pas encore de modèle explicite de collision ou de rebond. Ce comparateur permet néanmoins de faire entrer dans l'examen des séquences contenant un arrêt ou une inversion, afin de mesurer les limites de ces trois hypothèses existantes sans prétendre que le système sait traiter un rebond. Aucun nouveau modèle physique codé dans ce module.

## Validation PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_motion_memory_ablation_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

## Examen A/B sur des séquences indépendantes

```json
[
  {
    "observations":[
      {"t":0,"file":"build/episode-test-a/frame0.png"},
      {"t":1,"file":"build/episode-test-a/frame1.png"},
      {"t":2,"file":"build/episode-test-a/frame2.png"},
      {"t":3,"file":"build/episode-test-a/frame3.png"}
    ],
    "predict_t":4,
    "actual":"build/episode-test-a/frame4.png"
  }
]
```

Étendre le manifeste `build\\brody-ablation-cases.json` avec plusieurs épisodes réels et réellement distincts ; conserver un groupe de cas d'arrêt et de retournement. Utiliser **une mémoire d'anciennes corrections**, jamais des corrections issues des épisodes d'examen.

```powershell
py -m brody_world_physique.image_motion_memory_ablation_v1 --cases "build\brody-ablation-cases.json" --memory "build\brody-guided-correction-previous\candidate_physics_memory.json" --out "build\brody-ablation-001"
Get-Content "build\brody-ablation-001\MASTER_REPORT.json"
```

## Limites de preuve

Cette passe apporte le **comparatif mesurable** qui manquait. Les tests unitaires ne démontrent pas un avantage empirique ; ils vérifient que les deux conditions sont comparées et que la fuite de données est refusée. En présence de modèles mal adaptés (rebond, collision, perte de suivi), l'apprentissage peut **dégrader** les résultats et il faudra le dire. La prochaine étape est une collecte de séquences visuelles indépendantes, un contrôleur de source et une politique de révision des connaissances avec HOLD en cas d'incertitude. Les permissions sont toujours : `native_memory_write=False`, `canonical_promotion=False`, `KX108_ONLY`.
