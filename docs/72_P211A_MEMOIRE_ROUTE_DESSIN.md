# 72 — P2.11a — mémoire expérientielle raccordée à l'école de dessin

STATUS: CODE_PUBLISHED / PC_TEST_PENDING / FROZEN_ROUTING_PROBE / IMAGE_ONLY

## Ce qui est réellement branché
Le nouveau `brody_world_physique/p211a_memory_routed_drawing_v0.py` lit **et vérifie réellement** un ledger d'expériences P2.10d par `verify_ledger`, avant toute génération. Il utilise le verdict des expériences enregistrées pour router une nouvelle entrée vers `suggest_gestures_from_reference` + `render` de `drawing_school_v1` si au moins une expérience précédente est marquée `ACCEPTED`. En l'absence d'expérience améliorante, il conserve l'image initiale `PASS_THROUGH`. Le choix affecte donc réellement l'image et le moteur appelés; il ne modifie pas uniquement le rapport. Les images TRAIN et leurs pixels ne sont pas copiés dans la nouvelle génération.

Le PNG de sortie et son SHA256 sont créés **avant** l'ouverture facultative de la référence de test utilisée pour scorer l'écart. Le but est de tester la chaîne de routage et le pré-engagement; aucun gain de qualité n'est promis. Les méthodes sont très limitées et préprogrammées. La mémoire choisit une route binaire à partir de verdicts supervisés, **pas un geste ou une capacité nouvellement appris**. Cette version ne raccorde pas encore Reverso au générateur; le flag `reverso_connected=False` le rend explicite. Ni génération généralisée ni savoir visuel causal démontré.

## Validation PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p211a*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.11a échoués" }
```

## Frontières / prochaine étape
1. Brancher un véritable `GestureV1` appris et rejouable provenant de l'école de dessin et d'une expérience de correction, pas uniquement les verdicts de P2.10d.
2. Évaluer trois bras **sur les mêmes nouvelles images** : sans mémoire, route mémoire, mémoire gestuelle apprise. Mesurer fidélité visuelle, zone, dégâts et coût; publier aussi les régressions.
3. Relier une représentation Reverso à une synthèse (pas seulement Reverso lossless), avec précommit strict et génération sans pixels du teacher test.
4. Aucun chantier hors génération d'images; aucun changement de `main`, aucune promotion Native Memory.
