# P149 — Laboratoire temporel multiaxial (12 scénarios)

## Pourquoi

P148 a traité quinze mille courtes séquences en 45 secondes. La prévision linéaire avait zéro erreur dans des cas alignés avec le générateur, mais pas d'apprentissage de physique ni de véritable identité multiple. P149 introduit des contrôles indépendants par phénomène et le contre-factuel *image finale identique / passés différents*.

## Axes de test

12 familles : croisement d'objets identiques, croisement de couleurs distinctes, occultation d'une voie, occultation simultanée, retournement, accélération, arrêt, changement de couleur, distracteur, image finale identique malgré des vitesses latentes opposées, longue occultation, mouvement apparent de caméra. Sept images sont rendues, les six premières forment l'observation et la septième sert au calcul de l'erreur.

La comparaison **historique temporel vs dernière image seule** mesure l'erreur absolue en pixels, la couverture, les refus et les prédictions à moins de 3 pixels. Les premiers échantillons de chaque famille sont enregistrés dans `samples/` pour vérification visuelle. Les 9600 épisodes par défaut sont enregistrés dans `EPISODES.jsonl`.

**Contre-factuel apparié** : un test dédié fabrique deux histoires distinctes conduisant à une même image finale pixel à pixel au moment du croisement. `COUNTERFACTUAL.json` garde la preuve d'égalité binaire et la distinction des états latents. Cela établit une ambiguïté du seul instantané, **pas** un suivi autonome d'identités.

## Limites méthodologiques

Le détecteur utilise encore les voies verticales préassignées du rendu synthétique et un seuil de couleur. En présence de deux objets, il ne résout pas réellement leur association générale. Il n'apprend aucune dynamique nouvelle : la prévision extrapole la vitesse. Les scénarios ont diverses causes programmées, et certains (p. ex. `out_of_view` de P148) étaient mal ciblés ; P149 les remplace par des facteurs de difficulté nommés. Aucun résultat ne doit être annoncé comme physique réelle, apprentissage indépendant, raisonnement causal ou identité reconstituée. **Ne pas interpréter un scénario nommé comme une compétence déjà implémentée.** Les cas `long_gap` et `occlude_both` sont similaires dans le rendu actuel ; ils doivent être séparés davantage dans une future version si les résultats sont trop proches. Le suivi d'identité sans connaissance des voies reste un jalon ultérieur.

## Lancement Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_multiangle_temporal_p149.py" -v
if ($LASTEXITCODE -ne 0) { throw "P149 tests échoués" }
py -m brody_world_physique.image_multiangle_temporal_p149 --minutes 20 --episodes-per-kind 800 --out "build\brody-p149-multiangle-001"
if ($LASTEXITCODE -ne 0) { throw "P149 run échoué" }
Get-Content "build\brody-p149-multiangle-001\MASTER_REPORT.json"
```

Le plafond est de 20 minutes, pas une durée forcée. **Si la campagne finit trop rapidement, ne pas augmenter seulement les graines** : interpréter d'abord les erreurs et construire de nouvelles épreuves réellement discriminantes. Le run reste strictement expérimental (`KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`).
