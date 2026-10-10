# Brody — observation structurelle visuelle V1

L'étape remplace le contexte ultra-grossier (`flat` / `dark-dense` / `drawing`) dans la boucle visuelle par une description **fondée uniquement sur des pixels visibles** : composantes sombres connexes, bounding boxes, centres, densité, orientation dominante et relations de proximité/orientation entre composantes.

Chaque reçu de cours conserve `observed_properties`, `observed_parts` et `observed_relations`. Le contexte de procédure stabilisée dépend d'une signature descriptive non fondée sur le nom de fichier. Le mécanisme de cours, doute local, dédoublonnage par SHA et checkpoints reste inchangé. **Ce n'est pas encore une identification sémantique d'objets, une compréhension de couleurs ou une inférence 3D.** Les composantes sombres ne sont pas nécessairement des objets ; elles peuvent représenter les traits d'un même objet ou des artefacts. La représentation reste limitée à 64×64 niveaux de gris.

Pour préserver les reçus antérieurs, exécuter dans un **nouveau dossier**. L'ancien dossier `brody-visual-reflex-loop-001` utilise une version précédente des contextes. Ne pas tenter de reprendre un checkpoint ancien avec les nouvelles règles de description.

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_structural_observation_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
py -m unittest discover -s tests -p "test_image_visual_reflex_teacher_loop_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Régression échouée" }
py -m brody_world_physique.image_visual_reflex_teacher_loop_v1 --images "build\brody-images-ready" --limit 63 --out "build\brody-structural-lesson-001"
if ($LASTEXITCODE -ne 0) { throw "École structurelle échouée" }
Get-Content "build\brody-structural-lesson-001\MASTER_REPORT.json"
```

Prochain jalon requis : ajouter de vrais concepts enseignés (objet, partie, couleur, orientation, invariance) et leurs relations d'équivalence à travers les perspectives, au-delà des seules composantes foncées ; conserver provenance et correction des professeurs et démontrer le transfert sur de nouvelles images. Pas de modification kernel/Native Memory ni de promotion canonique.
