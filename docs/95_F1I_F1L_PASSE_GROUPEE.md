# 95 — F1I à F1L : passe groupée, bilan et frontières de preuves

F1H a été exécuté sur PC : 2/2 tests PASS, 11 réponses / 12 cas, 1 HOLD. Cet état constitue la référence de départ. Le module `f1i_f1l_batch_v1.py` est une livraison **en une fois** de quatre composants bornés, pas une preuve que l'école complète est terminée.

## F1I — observabilité physique
Réutilise `image_tracking_beam_p150.build/observe/infer` dans quatre régimes (séparation, mouvement de caméra, occultation, recouvrement). Les repères sont **détectés dans les images** avant la prévision. Résultats : repères disponibles, cause de HOLD, erreur et provenance. **Pas encore de détection d'un vrai événement de contact** : le jeu historique ne fournit pas une scène de collision réelle avec événement observable validé. `true_contact_observability_implemented=false`.

## F1J — perception ↔ génération élémentaire
Réutilise `image_multiangle_temporal_p149.render` pour produire les observations et `image_real_transfer_exam_v2.features` ainsi que `image_reciprocal_generation_school_v1.decode` pour reconstruire une image **à partir du prototype couleur 4×4**. Une seconde extraction mesure l'écart de représentation et de parties candidates. Ce cycle n'est pas un Reverse 360 géométrique et ne modifie pas les poids ni les représentations après erreur. La réciprocité ici est **un aller-retour instrumenté** et non une croissance cognitive prouvée.

## F1K — historique de compétences
Écrit un journal expérimental à trois états scellés : acquisition P150, interférence P152 et retour P150; provenance, dépendances, préconditions et SHA du précédent. Il démontre la conservation du registre, **pas** la rétention de performance d'un véritable apprenant. Les différences de score et l'oubli restent à tester avec une mémoire partagée non canonique.

## F1L — ensemble indépendant
Sans `--external-images`, la passe indique `HOLD_NO_INDEPENDENT_IMAGES`. Si un dossier d'images est fourni, on calcule uniquement empreintes, descripteurs visuels et nombre d'images. Aucune étiquette enseignante, aucun score d'identification, aucune validation du caractère réel de la source, aucune généralisation revendiquée. Le protocole ne touche ni aux fichiers d'origine ni à Native Memory.

## Non couverts
- Physique causale autonome, événement de contact visible et significatif.
- Reconstruction spatiale 3D / 360 et comparaison des invariants géométriques.
- Choix actif de nouveaux points de vue ou d'expériences par Brody.
- WorldState SENS/F12/MMonde interbranches.
- Apprentissage paramétrique, transfert cognitif entre compétences, vraie rétention et anti-oubli.
- Validation humaine / vidéos réelles indépendantes avec étiquettes et protocole.

## Commandes PowerShell (UN bloc)
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_f1i_f1l_batch_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.f1i_f1l_batch_v1 --out "build/f1i-f1l-batch-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/f1i-f1l-batch-v1/MASTER_REPORT.json"
```

**Option images indépendantes** : `--external-images "C:\\chemin\\vers\\images"`, utiliser un `--out` distinct et inexistant pour chaque exécution.

## Plan de reprise après cette livraison
1. Exécuter toute la suite de régression Brody, y compris F1A à F1L, et diagnostiquer la CI qui échouait sur GitHub.
2. Transformer F1I en scénario instrumenté avec contact visible / sans contact, tests appariés et contrôles négatifs.
3. Transformer F1J en boucle complète avec comparaison d'invariants LOCK/FLEX/IGNORE, hypothèses spatiales et adaptation mesurée.
4. Transformer F1K en mémoire éducative partagée avec épreuves réelles de rétention/transfert, pas seulement un registre.
5. Raccorder les contrats versionnés SENS/F12/MMonde et évaluer F1L sur un corpus indépendant, avec provenance, annotations et métriques préenregistrées.
6. Faire une revue de fidélité conceptuelle transversale avant toute annonce de fermeture E0–E7.

`NATIVE_MEMORY_WRITE=FALSE`
`CANONICAL_PROMOTION=FALSE`
`DECISION_AUTHORITY=KX108_ONLY`
`FULL_EDUCATION_E2E=NOT_PROVEN`
