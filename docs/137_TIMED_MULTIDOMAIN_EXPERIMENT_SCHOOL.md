# P137 — Vers un laboratoire multidomaine à budget temporel

Cette passe introduit un **orchestrateur de campagnes à durée bornée** `image_multidomain_timed_school_p137.py`, qui exécute neuf suites de régression hétérogènes : vision, contexte, scènes, génération, correction, examen aveugle, diversité, physique, provenance des sources. Il collecte les journaux, durées, empreintes et verdicts.

**Attention :** le paramètre `--minutes` est un budget MAXIMUM, pas une obligation de calculer pendant toute la durée. Les tâches actuellement disponibles sont rapides et le programme peut finir largement avant 5–15 minutes. Ce composant n'invente pas de nouveaux mondes physiques, de simulations 3D ni de nouveaux acquis. Il prépare la mesure fiable de campagnes plus longues ; il n'est pas encore un curriculum auto-adaptatif.

## Lancement PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m brody_world_physique.image_multidomain_timed_school_p137 --minutes 10 --out "build\brody-p137-001"
if ($LASTEXITCODE -ne 0) { throw "Certaines suites ont échoué : lire MASTER_REPORT.json" }
Get-Content "build\brody-p137-001\MASTER_REPORT.json"
```

La sortie contient le résumé des neuf familles et un log par famille. Un test échoué reste FAIL, un timeout reste TIMEOUT, et une tâche non atteinte reste NOT_RUN_BUDGET ; aucun résultat n'est converti en PASS artificiellement. La limite opérationnelle d'une suite est 120 secondes. Le programme n'efface ni n'écrase les campagnes antérieures.

## Plan scientifique pour remplir vraiment plusieurs minutes

Les prochaines extensions doivent multiplier les **tâches qualitativement nouvelles** et enrichir les jeux d'observations indépendantes : scènes naturelles RGB, couleurs et éclairages, occlusion multiobjet, reconstruction de relations, vues physiques multiangles et 360°, mouvements et interactions, analogies, raisonnement micro↔macro, apprentissage et examen différé. Pour chacune : plusieurs sources, un protocole de séparation par provenance, résultats sans mémoire/avec mémoire, contre-exemples, examen aveugle et restitution des échecs. Les nouveaux scénarios ne doivent pas être évalués comme `PASS` s'ils n'ont pas de moteur.

**Gouvernance :** branche expérimentale uniquement, `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`, aucune modification `main`.
