# Plan maître unique — Brody World Physique Image × Obsidia

## Objectif final
Brody apprend à partir d'images, du mouvement, d'expériences temporelles et physiques, compare une prédiction au constat, retient une compétence transférable et sait distinguer preuve, hypothèse, simulation et observation réelle. Les couches Obsidia gouvernent toute conséquence sensible. Il n'est pas demandé de construire une nouvelle autorité dans Brody.

## Périmètre, en une campagne
1. **Perception** : localisation, association temporelle, suivi d'objet, changement de perspective, transformation 2D/3D, symétrie, trajectoire, causalité ; validation sur images réelles tenues à l'écart de l'entraînement.
2. **Expérience physique** : anticipation de chute et collision, mouvement, résistance, conservation et contradictions ; calibration des incertitudes et observables. Un exercice synthétique n'est pas une découverte physique.
3. **Apprentissage humain guidé** : observer → agir/essayer → comparer → expliquer → enregistrer une *candidate* → replay → généraliser → retester. Séparer identité des épisodes, véracité des sources et compétence acquise.
4. **Représentations** : recouper les pistes documentaires multi-échelle, multidimensionnelles, angle 360°, réciproque, symétrie, Fibonacci et versions d'entraînement du projet. Aucun terme ne doit être déclaré implémenté sur la base du seul vocabulaire.
5. **Preuve et adversarial** : F14 (10 familles, 1000 cas), F15/F15B, attaquants coordonnés, provenance indépendante et authentifiée, falsification horodatage, source compromise, dépendances cachées.
6. **Autorité** : Brody provider non souverain → périphérie/contextes → domaine supporté → GuardX108/KX108 → Sigma veto post-Guard → receipts et gates. Interdiction d'une décision canonique venant d'une simple observation. Pas de contournement META.
7. **Mémoire** : candidate et relecture en lecture seule ; aucune promotion native sans gate, traçabilité ni preuve.
8. **Examens** : vrais cas fiables autorisés au niveau *contexte* quand les garanties existent, attaques HOLD/BLOCK, omissions explicites, faux positifs/faux négatifs, oubli, généralisation à un contexte non vu, risque de sur-refus.
9. **Livrables** : tests régression, reçus chaînés, scores par famille, contrôle d'intégrité, matrice de compétences PRESENT/WIRED/CALLED/CAUSAL/TESTED/PROVED et rapport global GO/HOLD avec blockers.

## État honnête
Les campagnes F9–F17 existent et plusieurs ont été exécutées sur PC. F17 a parcouru 1000 cas avec 1000 HOLD. Ce résultat **ne suffit pas** à attester apprentissage physique, capteurs réels, indépendance d'attestation, différenciation contextuelle ou domaine Brody opérationnel.

## Exécution groupée — sans nouvelle prolifération de phases
Le runner `brody_obsidia_single_campaign_v0.py` enchaîne tests, intégrité F14, mapping F15, moteurs réels F15B, inventaire F16, dry-run F17. Il sauvegarde tous les logs et produit un **MASTER_REPORT.json**, qui marque explicitement les capacités non établies : pas de GO artificiel.
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m brody_world_physique.brody_obsidia_single_campaign_v0 --obsidia-repo "C:\OBSIDIA_WORK\obsidia-x108-proofs" --out "build\brody-obsidia-global-001"
if ($LASTEXITCODE -ne 0) { throw "La campagne a échoué : consulter les logs de son dossier" }
Get-Content "build\brody-obsidia-global-001\MASTER_REPORT.json"
```

Ce runner **n'implémente pas encore** les capacités physiques et perceptives manquantes : celles-ci devront être intégrées avec les vrais datasets et capacités du projet, puis validées dans le même banc unique, pas dans un chapelet de petites campagnes. Ne jamais traiter `DIAGNOSTICS_PASS_FULL_LEARNING_NOT_VALIDATED` comme une validation scientifique.
