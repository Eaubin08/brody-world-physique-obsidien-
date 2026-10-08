# 31 — Première correction de mesure : détecter automatiquement la balle du clip de test

**2026-10-08 — EXPÉRIENCE CONTRÔLÉE SIMULÉE.** Cette branche ne prouve ni causalité physique, ni apprentissage de Brody, ni modèle visuel généralisé. Aucun nouvel LLM ou modèle de segmentation n'est requis.

## 1. Cause du raté précédent et mesure de référence

Sur le run Windows `video-test-20261008-204125`, l'utilisateur a confirmé l'empreinte de la vidéo `a089fdff99f20df5a54e227f46f3b869feb6764b793e2c8e5e024c065b17153f`. Les clics manuels étaient :

| Temps | X/Y enregistrés | Centre de la balle dans le clip de référence, approx. |
|---|---|---|
| 0,0 s | 193 / 104 | 276 / 106 |
| 0,1 s | 379 / 323 | 281 / 109 |
| 0,2 s | 284 / 319 | 286 / 116 |
| 0,3 s | 508 / 279 | 291 / 129 |

La mauvaise prévision issue des quatre clics `WORSE_THAN_LINEAR_BASELINE`, erreur du candidat **628,47 px**, ne démontre pas que la prédiction physique est intrinsèquement mauvaise : **la localisation initiale est défectueuse**. Cause probable : erreurs humaines de clic ou de conversion écran/images ; on ne doit pas inférer davantage sans preuve.

## 2. La route choisie, sans réinventer vision ou OS

Le nouveau module [`auto_ball_demo_v0.py`](../brody_world_physique/auto_ball_demo_v0.py) réutilise **OpenCV pour ouvrir et décoder les images**, et **Pillow pour les masques chromatiques** déjà disponibles. La boule orange est un objet facile à isoler de cette scène synthétique. Le détecteur :

1. refuse toute vidéo dont le **SHA-256** diffère de l'empreinte du fixture connu ;
2. lit le flux MP4 existant ; valide 30 FPS, 960 × 540 pixels et indices attendus `(0,3,6,9)` ;
3. cherche la zone orange saturée par `HSV` et contrôle sa boîte englobante, ses proportions et sa densité ;
4. calcule des positions **x/y en pixels natifs**, sans clic manuel ni analyse textuelle de Qwen ;
5. utilise **seulement les trois premières frames** pour créer `prediction_before_frame_4.json` ;
6. lit **ensuite** la quatrième frame, détecte la balle et compare au prédicteur et aux baselines ;
7. écrit `evaluation.json` avec preuves de provenance et `SIMULATED`.

**Limite :** détecteur **spécifique à la vidéo de démonstration**, ses couleurs et sa forme. Il ne sait pas localiser tous les objets du monde. Deux orange balles, un décor orangé, un autre éclairage, un mouvement de caméra ou une vidéo inconnue ne sont pas acceptés sans nouvelle spécification/test.

## 3. Commande PC fixe (aucun nouveau modèle)

Dans PowerShell, depuis `brody-world-physique-image` :

```powershell
git pull --ff-only origin main
py -m brody_world_physique.auto_ball_demo_v0 --video "$env:USERPROFILE\Downloads\brody_balle_chute_simulee.mp4" --out "build\balle-auto-$(Get-Date -Format yyyyMMdd-HHmmss)"
```

Si la vidéo est ailleurs, remplacer seulement `--video` par son chemin. Le fichier est local, aucune image n'est envoyée sur Internet, aucun modèle n'est installé. Si `cv2` manque, l'environnement Python doit être vérifié (voir document 30).

Résultat attendu : centres proches de `(276,106)`, `(281,109)`, `(286,116)`, `(291,129)`; le candidat d'accélération constante devrait avoir **une erreur beaucoup plus faible que 628 pixels**. Ce sont des **attentes**, pas des résultats prétendument exécutés sur le PC utilisateur.

## 4. Ce que cela validera et ce qui reste à faire

**Si le programme fonctionne sur le vrai MP4 simulé :** validation de l'extraction automatique **sur ce clip** et du protocole aveugle de comparaison. Ni l'origine physique, ni l'effet de la gravité, ni une compétence acquise ne seront démontrés. Les 3 données de départ sont des mesures dérivées d'un algorithme chromatique, la 4e est issue du **même détecteur** ; ce n'est pas un évaluateur de vérité indépendant.

**Ensuite, si le pipeline fonctionne :** confirmer les mesures sur une vidéo réelle de provenance connue, généraliser à plusieurs objets/décors, séparer tracking et mouvement de caméra, relier F16/MMonde/F12 et tester une stratégie *qui s'améliore vraiment* avec plusieurs expériences. Comparer à une méthode fixe sans apprentissage, au lieu de prétendre que la prédiction mathématique actuelle apprend.
