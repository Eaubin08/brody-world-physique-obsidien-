# Brody P132 — Construction multi-capacités : scènes, relations, mémoire et génération

Cette passe ajoute une **nouvelle capacité exécutable**, en complément des tests existants : mémoire de **scènes comportant plusieurs composantes visuellement séparées**. Elle travaille sur les données d'image et les relations spatiales sans supposer qu'elle connaît les noms réels des objets.

## Capacités intégrées

1. Perception : composantes connexes sombres sur fond clair (contrat d'observation existant), limites strictes à 8 composantes.
2. Relations : disposition horizontale/verticale/diagonale et proximité, constat observable et non relation causale.
3. Enseignement : professeur associe une étiquette symbolique aux observations ; contradiction sur les mêmes octets = erreur explicite ; doublon exact = aucune nouvelle leçon.
4. Mémoire : enregistrement séparé de provenance, contexte, géométrie et relations ; digest de vérification.
5. Rappel : un candidat n'est proposé que si au moins deux groupes de source distincts soutiennent un même étiquetage pour le graphe relationnel. Si plusieurs étiquettes ou preuves insuffisantes : DOUBT.
6. Génération réciproque : reconstitution PNG des rectangles englobants appris sans recopier les pixels sources ; **pas** une génération photographique ou une vraie composition sémantique.
7. Évaluation : le test exam reste hors apprentissage ; séparation des groupes et hashes entre cours et examen ; nombre de candidats, succès et HOLD rapporté.

**Limites** : ce premier organe est une représentation **2D noir/blanc**, exige des composantes séparées, un enseignement explicite et ne connaît ni identité autonome ni profondeur ni 360° physique. Le graphe relationnel grossier peut confondre des scènes différentes : les fausses reconnaissances doivent être mesurées, non dissimulées. Deux noms de groupes différents ne démontrent pas deux captations indépendantes.

## Commande PC : régression + nouvelle capacité

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_scene_relational_school_p132.py" -v
if ($LASTEXITCODE -ne 0) { throw "P132 échouée" }
py -m unittest discover -s tests -p "test_image_heterogeneous_capability_audit_p131.py" -v
if ($LASTEXITCODE -ne 0) { throw "P131 régression échouée" }
py -m unittest discover -s tests -p "test_image_context_transition_transfer_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "P129 régression échouée" }
```

## Corpus réel possible

Un fichier JSON contenant au minimum deux cours d'étiquette commune venant de groupes distincts, et des examens d'autres groupes ; chaque ligne :

```json
{"file":"build/scenes/photo_01.png","split":"train","source_group":"tournage-01","teacher":"symbole-A"}
```

Après préparation des lignes, lancer :

```powershell
py -m brody_world_physique.image_scene_relational_school_p132 --scenes "build\scenes-p132.json" --out "build\scenes-p132-results"
```

Les résultats comprennent `candidate_scene_memory.json`, `reconstruction.png`, `SEALED_EXAM_RESULTS.json` et `MASTER_REPORT.json`. Le champ `SEALED_EXAM_RESULTS` désigne un examen prédit avant lecture de l'étiquette, et non un système de confidentialité cryptographique.

## Périmètre de test et TODO

Cette passe teste : plusieurs objets séparés, relations, étiquetage pédagogique, mémoire intègre, refus de fuite entre groupes, examen inédit, HOLD si inconnu et image recomposée. Elle n'annonce **pas** les capacités plus larges du backlog des 80 expériences : occlusion, changement d'échelle invariant, couleurs/matériaux, profondeur, interprétation causale, conception de forme réaliste restent à construire.

**Autorité** : `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`, branche expérimentale seulement.
