# Brody — P135 : génération réciproque sans regarder l'image d'examen

## Nouveauté par rapport à P134

La P134 utilisait directement la segmentation et les contours de **l'image d'examen** avant d'en générer une version, ce qui était un biais majeur. P135 demande une **description symbolique** : label appris + emplacement (bbox) + couleur optionnelle. Elle produit une image uniquement depuis les exemplaires **de cours**, puis révèle et compare l'image cible après avoir sauvegardé les prédictions.

Le script `brody_world_physique/image_blind_symbolic_regeneration_p135.py` sépare explicitement : lecture des images d'apprentissage, constitution de la mémoire des masques, compilation des descriptions symboliques de l'examen, sauvegarde du fichier `SEALED_BEFORE_EXAM.json`, puis seulement lecture des images cibles et comparaison RGB.

Le test de capacité distingue : nouvelle observation d'une forme connue (candidat), forme non enseignée (DOUBT), composition partiellement inconnue (DOUBT), et groupe de source réutilisé (refus).

Il ne s'agit **pas** d'une génération depuis texte libre : les boîtes englobantes et les étiquettes sont fournies par le prompt. La méthode reste une composition de masques exemplaires 2D, sans vrai 360°, connaissance sémantique autonome, profondeur, causalité ou lois physiques. Le corpus de test est construit artificiellement ; les groupes sont déclaratifs et non prouvés indépendants.

## Format du manifeste

Liste JSON avec :

- Cours : `{"split":"train","group":"source-A","label":"rond","file":"images/cours-A.png"}`
- Examen : `{"split":"exam","group":"source-C","file":"images/examen-C.png","prompt":[{"label":"rond","bbox":[10,10,30,30],"rgb":[255,0,0]}]}`

Au moins deux groupes indépendants doivent enseigner chaque étiquette candidate. Les formes ambiguës et inconnues doivent être mises en doute.

## Validation PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_blind_symbolic_regeneration_p135.py" -v
if ($LASTEXITCODE -ne 0) { throw "P135 échouée" }
py -m unittest discover -s tests -p "test_image_reciprocal_shape_learning_p134.py" -v
if ($LASTEXITCODE -ne 0) { throw "Régression P134 échouée" }
```

Les sorties utilisateur : `MASTER_REPORT.json` (candidats, HOLD, erreur moyenne), `SEALED_BEFORE_EXAM.json`, `EXAM_RESULTS.json`, images générées `predicted_*.png`, `CANDIDATE_MEMORY.json`.

**À améliorer :** comparer une vraie génération d'objet composite jamais vu, rapporter une erreur conditionnelle et une couverture calibrées, prévenir également les doublons perceptuels non identiques byte-à-byte, valider la cohérence entre source_group et provenance physique, séparer couleurs et matériaux, et construire de vraies expérimentations image/vidéo libres de droits. Ne pas traiter le succès d'un test fabriqué comme preuve de généralisation réelle.

Autorité inchangée : `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false` ; branche expérimentale uniquement.
