# 32 — Brody Image : partir sans savoir physique, apprendre des images puis tester l'inconnu

**Date :** 2026-10-08 · **Statut :** 8 vidéos de simulation créées et premier protocole expérientiel `experiential_video_v0.py` codé/testé par CI ; exécution du paquet MP4 sur le PC utilisateur **à confirmer**.

## Demande originale de l'utilisateur

> « À partir de plusieurs expériences, mais aussi sans savoir, sans data […] des exemples où il a pas la méthode mathématique et qu'il doit arriver à ce résultat […] mettre tous ces essais-là en place, créer les vidéos. »

La cible est **acquérir une capacité pratique avant d'apprendre les mots et les lois**, selon les précisions historiques de l'utilisateur : apprentissage comme un enfant, réciproque analyse⇄synthèse, données physiques, monde situé, essais/corrections, mémoire qui retient ce qui importe. [28 — préverbal](28_APPRENTISSAGE_PREVERBAL_MONDE_PHYSIQUE.md), [29 — prédiction mesurable](29_PREVERBAL_PREDICTION_EXPERIENCE_V0.md), [05 — mémoire](05_LEARNING_MEMORY.md), [23 — provenance des idées](23_BRODY_IMAGE_LEARNING_TRACEABILITY.md).

**Précision critique :** « sans data » ne peut pas signifier « sans observations ». Un système qui n'a **aucune information de départ** ne peut pas prédire une évolution spécifique du monde par magie. Nous pouvons toutefois partir **sans corpus d'apprentissage préchargé, sans étiquettes de mouvement, sans formule de gravité/vent/rebond**, puis recueillir nous-mêmes les données de ses nouvelles expériences. Le décodeur vidéo, le détecteur du marqueur orange, la représentation du temps et la règle d'apprentissage *k plus proches expériences* sont des biais **programmés au départ** : ils ne constituent pas une intelligence générale spontanée.

## Première batterie créée : 8 sources distinctes

Fichier distribué : `brody_experiences_sans_lois_v1.zip`. Il contient un répertoire `brody_experiences_sans_lois_v1` avec :

| Sources d'expérience | Sources de validation jamais utilisées pour alimenter la mémoire |
|---|---|
| `train_01.mp4` : mouvement vertical accéléré | `test_01.mp4` : autre chute |
| `train_02.mp4` : mouvement sensiblement régulier | `test_02.mp4` : autre déplacement régulier |
| `train_03.mp4` : impact/changement de direction | `test_03.mp4` : autre rebond |
| `train_04.mp4` : trajectoire oscillante | `test_04.mp4` : autre oscillation |

Le programme d'apprentissage **ne reçoit pas ces étiquettes**, uniquement des centres `(x,y,t)` extraits du marqueur orange d'une vidéo synthétique et les relations temporelles. Les noms sont neutres `train_XX`/`test_XX`. Même lorsqu'il réussit un transfert, il ne connaît pas les forces réelles et n'a pas appris une loi physique validée.

Conditions contrôlées : 480×320, 24 FPS, 72 frames/clip, marqueur orange unique et fond sombre, caméra fixe par conception, coordonnées en pixels; vidéo compressée MP4. `suite.json` porte `SIMULATED`, les empreintes SHA-256, et la partition TRAIN/TEST.

## Les six questions réellement testées

1. **Zéro expérience :** la mémoire initiale est vide ; `HOLD_NO_EXPERIENCE` plutôt qu'une prédiction gratuite. `--train-videos 0` mesure réellement ce cas.
2. **Premiers essais :** chaque clip TRAIN est observé en source, 3 instants de contexte puis un quatrième résultat connu : on retient une **relation de déplacement mesurée**, pas l'étiquette « gravité ».
3. **Accumulation :** comparer `--train-videos 1` à `--train-videos 4`. Après 4 clips, la mémoire de candidats contient des signatures de déplacements passés et leur suite observée (environ 36 transitions pour ce lot).
4. **Généralisation :** pour chaque nouvelle vidéo TEST, on prédit à partir des seules positions antérieures et d'exemples TRAIN ; l'observation suivante n'est décodée qu'**après l'enregistrement de la proposition**. Aucun échantillon TEST n'entre en mémoire pendant l'évaluation.
5. **Hésitation raisonnable :** une situation trop différente des traces connues retourne `HOLD_UNFAMILIAR_CHANGE`. La couverture et le nombre d'abstentions sont mesurés ; l'absence de prédiction n'est pas comptée comme une victoire.
6. **Comparaison honnête :** erreurs face à l'immobilité, à la vitesse constante et à l'extrapolation fixe avec accélération (celle testée précédemment). **Ces formules ne nourrissent pas le chemin d'apprentissage par voisinage** ; elles ne servent qu'au score.

**Technique proposée, pas doctrine physique :** les quatre entrées d'une expérience sont les différences `dx,dy` entre trois positions précédentes ; la cible est la différence `dx,dy` observée à l'instant suivant. Le rappel se fait par proximité numérique des signatures, non par une loi de Newton préchargée. Le modèle peut échouer malgré son apprentissage. Il faut comparer son score, sa couverture et ses HOLD, et pas seulement afficher un chiffre favorable.

### Ordre temporel des preuves

```text
MÉMOIRE VIDE → pas de modèle empirique / HOLD
   |
4 vidéos TRAIN :
   observer t0,t1,t2,t3 → créer un candidat "histoire de 3 positions -> suite"
   stocker des expériences locales, avec provenance, sans Native Memory
   |
GEL de la mémoire candidate
   |
4 vidéos TEST jamais apprises :
   lire t0,t1,t2 → prédire t3 → écrire prediction sur disque
   lire t3 → mesurer erreur → comparer les 3 références
   répéter, sans mutation mémoire sur les sources TEST
   |
rapport / candidats de transfert ≠ savoir validé
```

## Commandes Windows sur le PC fixe

1. Télécharger `brody_experiences_sans_lois_v1.zip`, par exemple dans Téléchargements.
2. Exécuter depuis `C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image` :

```powershell
git pull --ff-only origin main

Expand-Archive -Path "$env:USERPROFILE\Downloads\brody_experiences_sans_lois_v1.zip" -DestinationPath "$env:USERPROFILE\Downloads\brody_suite" -Force

$suite = "$env:USERPROFILE\Downloads\brody_suite\brody_experiences_sans_lois_v1\suite.json"
# Trois essais distincts : aucune expérience / une vidéo / quatre vidéos
$prefix = "build\experience-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.experiential_video_v0 --suite $suite --out "$prefix-cold" --train-videos 0
py -m brody_world_physique.experiential_video_v0 --suite $suite --out "$prefix-one" --train-videos 1
py -m brody_world_physique.experiential_video_v0 --suite $suite --out "$prefix-four" --train-videos 4

foreach ($stage in @('cold','one','four')) {
  $j = Get-Content "$prefix-$stage\evaluation.json" -Raw | ConvertFrom-Json
  Write-Host "=== $stage ===" $j.test_predictions "predictions /" $j.test_holds_unknown "HOLD"
  $j.test_measures | Select-Object file,learned_predictions,unknown_holds,learned_mae_px,linear_mae_px,fixed_accel_mae_px | Format-Table -AutoSize
}

# Compare seulement les instants prédits par LES DEUX expériences
py -m examples.compare_experience_stages_v0 --cold "$prefix-cold\evaluation.json" --one "$prefix-one\evaluation.json" --many "$prefix-four\evaluation.json" --out "$prefix-matched.json"
```

**Si le ZIP n'est plus disponible**, les huit fichiers peuvent être recréés directement depuis le dépôt, avec les codecs locaux (les SHA-256 du MP4 peuvent varier selon l'encodeur, mais le générateur construit un manifeste cohérent) :

```powershell
py -m examples.generate_experience_suite_v0 --out "build\videos-neuves"
py -m brody_world_physique.experiential_video_v0 --suite "build\videos-neuves\suite.json" --out "build\essai-videos-neuves" --train-videos 4
```

Le code du **générateur** contient nécessairement les trajectoires synthétiques ayant servi à fabriquer les vidéos ; **le code du learner ne l'importe pas**. Ces formules ne sont ni des données physiques réelles, ni des lois accessibles à l'agent pendant le test.

Le programme requiert `cv2` (OpenCV déjà installé pour le test précédent sur ce même PC). Aucun modèle à télécharger et aucune nouvelle API cloud.

**Lecture honnête des chiffres :** le nombre d'abstentions (couverture) change lorsque la mémoire augmente. Une erreur moyenne sur 13 prédictions ne se compare pas directement à une erreur moyenne sur 34 prédictions différentes. Le script `compare_experience_stages_v0` évalue donc les **mêmes images tenues secrètes aux deux variantes**, puis sépare victoires, défaites, baselines et couverture. Cela peut montrer qu'une variante plus entraînée répond davantage mais se trompe plus souvent sur certains cas ; ce n'est pas une anomalie à masquer.\n\n**Sorties locales :** `learning_candidates.json` (expériences candidates à audit, pas mémoire native), `predictions_before_heldout.jsonl` (engagements datés par source vidéo et index), `evaluation.json` (scores, couverture, abstentions, résultats tous cas). Aucune photo/vidéo privée n'est commitée.

## Statut et ce qui reste non prouvé

- Le paquet est **entièrement SIMULATED**, construit pour l'épreuve ; cela ne constitue ni un corpus de réalité biologique, ni des mesures GPS, ni un apprentissage des forces physiques.
- Le détecteur de marqueur est **codé**, donc ce test ne démontre pas qu'un modèle peut découvrir les objets sans biais perceptifs. Et kNN est une règle d'association, pas une conscience.
- Les baselines mathématiques doivent pouvoir **battre** l'apprentissage candidat sur certains cas ; le rapport ne doit pas cacher ces échecs.
- Il manque encore : nouvelles vidéos faites de vraies scènes, objets variés sans marqueur orange imposé, adaptation de perception, choix expérimental autonome, mémoire sélective après validation, réciproque image et représentation F16/MMonde/F12 intégrées.

**Jalon après cette batterie :** comparer *aucune expérience / 1 expérience / plusieurs expériences*, puis un changement de contexte (caméra, vitesse, apparence, bruit et occlusion), et vérifier le réemploi de compétences sur plusieurs épisodes avant toute promotion de savoir. Ne pas redévelopper l'OS, Qwen-VL ou les organes existants ; ils restent donneurs externes.
