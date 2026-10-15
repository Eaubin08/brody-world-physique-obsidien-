# 96 — Brody P0–P5 : livraison groupée, protocole et limites

**Branche :** `exp/p2-multirepresentation-ablation-20261009`.
**Contrats :** `KX108_ONLY`, aucune promotion canonique, aucune écriture Native Memory; aucune modification des dépôts SENS/MMonde.
**Principe :** six chantiers, une seule commande Windows. Les résultats scientifiques et d'intégration ne doivent pas être surévalués.

## P0 : régression globale
`scripts/RUN_BRODY_P0_P5_ALL.ps1` exécute `py -m unittest discover -s tests -v` avant le banc intégré. Il s'arrête en cas d'échec. Le champ `P0.full_regression_executed=false` dans le rapport du module n'est pas une erreur : le module ne peut pas certifier lui-même l'exécution PowerShell qui lui précède. **Vérifier la sortie PowerShell intégrale.** Les tests distants ne sont pas annoncés PASS tant que le PC ne les a pas exécutés.

## P1 : perception structurelle
Réemploi réel de `image_reciprocal_shape_learning_p134.scene` et `paint` ; comparaison au décodeur RGB 4×4. Une image d'entraînement (deux formes) et une image différente d'examen sont segmentées. Les masques, les boîtes englobantes et la composition sont visibles dans les artefacts. L'identité sémantique des objets reste non démontrée.

## P2 : perception ↔ génération ↔ confrontation
Sur une image différente contenant un cercle plutôt qu'un carré, reconstruire d'abord depuis le prototype de l'image d'entraînement en utilisant les positions/tailles observées, **sceller cette proposition**, puis afficher l'image d'examen pour corriger le masque expérimental. Mesure MAE avant/après. La correction exploite l'image observée : ce n'est ni une prédiction aveugle de futur, ni une preuve de généralisation après réentraînement. La forme corrigée n'est pas promue à une mémoire canonique.

## P3 : acquisition, interférence et rétention
Réemploi de `image_education_retention_gate_p155.choose`. Une correction favorable au contexte de feedback est testée sur un jeu indépendant de rétention propre; elle doit être rejetée si elle détériore cet acquis. Trois événements scellés sont écrits avec le digest précédent. L'expérience mesure une **décision de rétention**, et non un système complet de poids/mémoires partagés apprenant plusieurs domaines.

## P4 : observation et incertitude physique
Réemploi de `image_tracking_beam_p150.build/observe/infer`. La décision est prise avec le nombre d'objets visibles dans les dernières images, avant de révéler les coordonnées réelles. Les occultations ou associations ambiguës peuvent déclencher HOLD, sans interdire systématiquement toutes les situations. Une amélioration statistique du risque n'est pas prouvée par quatre exemples.

## P5 : monde et images indépendantes
Réemploi `image_active_context_probe_p158.decide` : les hypothèses compatibles conduisent à PROBE quand une observation discriminante est possible, sinon HOLD. **La requête PROBE n'exécute pas une action physique**, et ne raccorde pas encore SENS/MMonde. Un dossier `--external-images` est traité par des descripteurs sans étiquettes ; aucun score de généralisation n'est calculé. Reverse 360 complet non implémenté.

## Une seule commande sur le PC Windows
À lancer dans la racine du repository, après récupération des commits :
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/RUN_BRODY_P0_P5_ALL.ps1
```
Option supplémentaire avec des images personnelles indépendantes (dossier EXISTANT) :
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/RUN_BRODY_P0_P5_ALL.ps1 -Output "build/p0-p5-real-v1" -ExternalImages "C:\\chemin\\vers\\images"
```
Chaque sortie doit être nouvelle. La commande exécute toute la suite de tests du dépôt, **qui peut être longue** : ne pas utiliser comme simple vérification rapide.

## Statuts de fermeture
- P0 : prêt à exécuter, PASS seulement lorsque toute la régression est verte.
- P1 : structure visible et reconstruction candidate mesurées, pas d'identité 3D.
- P2 : correction par feedback implémentée, pas de généralisation autonome prouvée.
- P3 : garde anti-régression réutilisée, pas de mémoire multi-compétence partagée.
- P4 : couverture sélective à mesurer, pas de calibration générale.
- P5 : PROBE/HOLD et lecture optionnelle d'images, raccordement SENS/MMonde et Reverse 360 complets restent BLOQUÉS.

**Suite:** dès que la régression est verte, audit des métriques, puis amélioration du noyau éducatif partagé et contrat interbranches SENS/MMonde. Pas de fermeture définitive E0–E7 avant preuves sur transfert, rétention, nouvelles scènes et mémoire cumulative.
