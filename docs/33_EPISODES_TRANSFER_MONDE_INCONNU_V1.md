# 33 — Brody Image : apprendre sans formule de domaine, puis tester le transfert réel *dans la simulation*

**Date :** 2026-10-08. **Statut :** 12 clips synthétiques créés, détecteur plus général sur formes/couleurs saturées, passage par ancrage visuel, prévisions sans futur, gardes de contradiction, surprise et occlusion. **Aucune connaissance générale de la physique démontrée.**

## Demande, source et attribution

La demande de l'utilisateur est de vérifier l'approche d'**apprentissage par expérience comme un enfant** : apprendre à anticiper avant d'avoir la formule ou les mots, réutiliser les capacités graphiques existantes, lier le monde physique, les objets, les points de vue et la réciproque, construire un savoir utilisable sans confondre compréhension, vérité, preuve et certitude. Les références historiques et leurs attributions sont dans [23](23_BRODY_IMAGE_LEARNING_TRACEABILITY.md), [24](24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md), [27](27_REVERSO_WORLD_MODEL_APPRENTISSAGE_SELECTIF.md), [28](28_APPRENTISSAGE_PREVERBAL_MONDE_PHYSIQUE.md) et [32](32_EXPERIENCES_ZERO_SAVOIR_SANS_LOI.md).

Les **algorithmes précis** (segmentation de saturation, ancre cyan, seuil de contradiction, kNN, écart de 15 pixels, fenêtres de trois observations) sont des **propositions d'ingénierie de l'assistant**. Ils ne sont ni des lois apprises de manière autonome, ni une revendication d'invention de chaque primitive informatique par l'utilisateur.

## Sources visuelles V1

Générateur reproductible : [`examples/generate_transfer_probes_v1.py`](../examples/generate_transfer_probes_v1.py). Pack `brody_transfert_monde_v1.zip` (6 TRAIN + 6 TEST). Chaque source possède une empreinte SHA-256 locale vérifiée dans `suite.json`. La création des mouvements utilise des formules **dans le générateur uniquement** ; le moteur apprenant n'importe pas ce générateur et ne reçoit aucune étiquette de phénomène.

| Clip TEST | Changement non communiqué au prédicteur | Vérification attendue |
|---|---|---|
| `test_01.mp4` | marqueur **bleu et carré** au lieu d'orange rond | position utilisable malgré l'apparence |
| `test_02.mp4` | **triangle vert** | anticipation malgré la nouvelle silhouette |
| `test_03.mp4` | caméra se déplace, deux repères colorés fixés à la scène | corriger les coordonnées dans le repère choisi, comparer aux pixels bruts |
| `test_04.mp4` | déplacement brutal invisible avant qu'il se produise | mesurer la surprise ; ne pas prétendre pouvoir deviner l'imprévisible |
| `test_05.mp4` | histoires initiales identiques aux vidéos TRAIN avec suites incompatibles | s'abstenir plutôt que prétendre que la cause/loi est certaine |
| `test_06.mp4` | objet temporairement masqué | refuser d'inventer une position réelle non observée |

**Contrainte connue :** fond simple, scène artificielle, objet coloré saturé unique, repère cyan fourni *dans le dessin*, caméra rectilinéaire, vidéo MP4. L'algorithme ne sait pas détecter tous les objets d'une vraie photo, ni inférer un monde 3D, ni expliquer le GPS, les forces ou la biologie. Le terme « transfert » porte ici sur quelques invariances contrôlées entre ces clips, pas sur le monde entier.

## Ce qui est réellement implémenté

[`world_transfer_probe_v1.py`](../brody_world_physique/world_transfer_probe_v1.py) :

1. observe les séquences TRAIN via OpenCV, et ne retient que les écarts de positions entre images horodatées ;
2. utilise une **vue de position candidate** compatible avec le principe de MMonde/F12, mais sans modifier les contrats ni les raccorder officiellement au runtime canonique ;
3. gèle les expériences avant d'ouvrir les TEST ; chaque position future est observée après émission écrite de sa prévision ;
4. applique une **détection de zone saturée** tolérant couleurs/formes différentes et une **compensation par repère fixe visible**. Comparaison avec/sans repère disponible par `--camera-mode anchored` / `raw_diagnostic` ;
5. applique `HOLD_CONFLICTING_EXPERIENCES` si plusieurs histoires très proches mènent à des suites incompatibles, ou `HOLD_UNFAMILIAR_CHANGE` si le chemin est inconnu ;
6. retourne `SURPRISE` pour une prédiction suivie d'une erreur supérieure au seuil candidat de 15 pixels. **Il ne l'avait pas prédit :** cela n'est pas une victoire de l'anticipation ;
7. sur occlusion, interrompt la série de points. Il ne reconstruit pas la « vérité cachée » à partir d'une supposition ;
8. enregistre des reçus `forecasts_precommitted.jsonl` et `evaluation.json`, sans entraîner de poids ni écrire dans Native Memory.

[`reverso_future_preview_v1.py`](../examples/reverso_future_preview_v1.py) prend une **position future déjà prédite** et une **image passée**, déplace la région de l'objet par des outils OpenCV (décodage, masque, inpainting et composite), puis compare la nouvelle image à la frame cachée. C'est une **visualisation de prévision et une évaluation inverse**, pas un générateur neuronal entraîné, ni une preuve de fidélité au réel. Une reconstruction exacte pixel-par-pixel n'est pas revendiquée dans ce passage.

## Résultats mesurés initialement en CI

Sur la suite générée par le même script dans GitHub Actions (Python 3.11), le mode ancré a produit les erreurs moyennes suivantes sur **les prédictions effectivement émises** :

| Épreuve | Erreur moyenne (px) | Constat |
|---|---:|---|
| Objet bleu carré | 1,14 | transfert visuel borné sur marqueur saturé |
| Triangle vert | 0,42 | transfert visuel borné |
| Caméra mobile **avec repère** | 1,17 | contre 3,35 px en coordonnées brutes |
| Changement brutal | 9,97 | au moins **1 surprise** supérieure à 15 px |
| Histoires contradictoires | Pas de prévision | **9 HOLD de conflit**, mesure d'erreur non applicable |
| Occlusion | 0,82 sur observations utilisables | **1 futur non observable** ; pas d'évaluation inventée |

**Ce tableau n'est pas une preuve de généralisation universelle :** il utilise des films qui suivent les hypothèses d'instrumentation et l'erreur moyenne exclut les HOLD. Les valeurs sont un point de départ pour des comparaisons, non une calibration démontrée de certitude. Comparer couverture et erreurs sur sources identiques avant de modifier un seuil.

## Essais à lancer sur le PC fixe (pas de nouveau modèle)

Dans `C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image`, télécharger le ZIP ci-dessus, puis :

```powershell
git pull --ff-only origin main
Expand-Archive "$env:USERPROFILE\Downloads\brody_transfert_monde_v1.zip" "$env:USERPROFILE\Downloads\brody_transfert_suite" -Force
$suite = "$env:USERPROFILE\Downloads\brody_transfert_suite\brody_transfert_monde_v1\suite.json"
$prefix = "build\transfert-$(Get-Date -Format yyyyMMdd-HHmmss)"

py -m brody_world_physique.world_transfer_probe_v1 --suite $suite --out "$prefix-ancre" --camera-mode anchored
py -m brody_world_physique.world_transfer_probe_v1 --suite $suite --out "$prefix-brut" --camera-mode raw_diagnostic
py -m examples.reverso_future_preview_v1 --suite $suite --forecasts "$prefix-ancre\forecasts_precommitted.jsonl" --out "$prefix-reverso" --clip test_01.mp4
```

Regarder `evaluation.json` dans les deux répertoires, et les quatre PNG dans `*-reverso` : dernière image observée, future prédite, vraie future et différence.

Si le ZIP n'est plus accessible, le générateur peut tout refaire localement (MP4 et `suite.json` à SHA cohérents) :

```powershell
py -m examples.generate_transfer_probes_v1 --out "build\transfer-suite-neuve"
```

**Gardes** : `SIMULATED` partout, entraînement sur TRAIN seulement, test gelé, aucun accès autonome à un monde physique réel, aucune décision d'action, aucun kernel modifié, `KX108_ONLY`, aucune vérité physique promue. Le moyen de progresser est de remplacer ensuite les contraintes artificielles par des observations vraies avec qualité/temps/repère/identité et des expériences répétées et contrôlées, pas de multiplier les étiquettes.
