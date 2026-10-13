# Brody — Grande passe d'intégration : école continue unifiée V1

Cette passe remplace la multiplication de modules isolés par un **parcours unique** qui réutilise les organes déjà testés :
- découverte de sources **locales approuvées et étiquetées** (`--images` répertoire + `--labels` JSON du professeur ; sous-dossiers inclus) ;
- observation des éléments/propriétés/relations des images via `image_structural_observation_v1` ;
- identité candidate regroupant les observations sous le même enseignement (pas un nouveau savoir par photo) ;
- reconnaissance avant correction via `image_blind_identity_transfer_v1.classify` ; au plus trois possibilités, doute conservé ; distance de pixels uniquement pour hypothèses incertaines ;
- correction enseignée ensuite via `image_persistent_identity_teacher_loop_v1.remember`, doublons et contradictions en quarantaine ;
- mémoire candidate `identity_memory_candidate.json`, rechargée explicitement avec `--previous` entre sessions ;
- reçus chaînés + `checkpoint.json` durable après chaque leçon, reprise dans le même dossier à la même commande ;
- examen séparé sur fichiers hors cours, avec refus d'identiques SHA256 et aucune mise à jour de mémoire.

**Vérité/savoir :** l'étiquette du professeur reste une connaissance *candidate et locale* ; le professeur n'est pas authentifié et aucune procédure sémantique n'est stabilisée par défaut. Un examen peut retourner DOUBT sans être un échec de sécurité. Ce n'est pas un modèle de monde 3D ni une école de couleur, mouvement ou causalité ; les images restent 64×64 niveaux de gris et la recherche de données est limitée aux dossiers explicitement autorisés. Le moteur ne télécharge rien sur Internet et ne touche ni main, ni kernel KX108, ni Native Memory.

**Mécanique de reprise :** le checkpoint est écrit après fsync du reçu. Une coupure entre les deux entraîne un refus explicite au redémarrage et nécessite une opération de réparation auditée ; aucune preuve n'est réécrite implicitement. Les dossiers complets antérieurs restent intacts.

## Test rapide sur Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_unified_continuous_school_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

## Cours sur les 63 archives

Les 63 images ne sont pas actuellement annotées par identité fiable. **Ne pas inventer des étiquettes « balle », « voiture » ou « objet unique » pour fabriquer une réussite.** Créer un fichier `build\brody-identity-labels.json` contenant des associations `"image_0001.png": "identite-verifiee-par-prof"`, une entrée seulement par image dont l'identité a été effectivement vérifiée. Les fichiers sans étiquette sont volontairement ignorés. Lancer :

```powershell
py -m brody_world_physique.image_unified_continuous_school_v1 --mode learn --images "build\brody-images-ready" --labels "build\brody-identity-labels.json" --out "build\brody-unified-school-001"
```

Pour un nouveau dossier de cours, garder `--previous "build\brody-unified-school-001\identity_memory_candidate.json"` et choisir un `--out` inédit. Pour examiner sans étiquette les nouvelles images dans `assets\unseen-images` :

```powershell
py -m brody_world_physique.image_unified_continuous_school_v1 --mode exam --images "assets\unseen-images" --previous "build\brody-unified-school-001\identity_memory_candidate.json" --out "build\brody-unified-exam-001"
```

## Critères de la prochaine grande passe

Enrichir l'organisation en objets / parties / propriétés / couleurs / géométrie / transformations / mouvement / relation temporelle ; fournir un vrai mécanisme de professeur vérifiable et une correction du savoir, pas seulement des signatures de pixels ; apprendre à rechercher la bonne source externe après identification d'un manque, sous provenance ; établir rétention et transferts sur plusieurs images indépendantes, avec comparaison à des négatifs difficiles. Ne pas confondre grandeur de campagne et progrès.
