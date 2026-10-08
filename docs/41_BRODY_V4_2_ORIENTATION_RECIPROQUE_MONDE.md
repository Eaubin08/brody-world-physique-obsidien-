# 41 — Brody Image V4.2 : orientation, réciproque, reconstruction, monde

**Projet :** Brody World Physique Image (09/10/2026). **Statut :** prototype expérimental synthétique, candidat et non promu. **Suite :** leçons V1–V3 → pont MMonde V4 → proximité visuelle V4.1 → orientation V4.2.

## Intention de l'auteur et décision de conception

L'utilisateur souhaite que Brody apprenne à représenter les objets du **monde**, avec leur identité candidate, leurs positions, relations, points de vue, la **symétrie/réciproque et les perspectives 360°**, et qu'il mémorise non seulement les images mais les **procédures, méthodes, erreurs et transformations**. Ce n'est **pas** l'autorisation de réécrire une deuxième mémoire canonique dans ce dépôt : MMonde/F12/F16, SENS/B8/B9/B10 et la Native Memory ont leurs propriétaires propres.

La V4.1 a appris une séparation quantitative proche/loin depuis huit-composantes connexes et six retours d'expériences. Son échec enregistré (**parties inversées classées proches**) appelle un nouveau cours sur l'**orientation d'une relation**. Un objet proche peut être en haut, en bas, à gauche ou à droite : la proximité seule ne suffit pas.

## Ce que V4.2 implémente effectivement

Code : [`world_orientation_school_v4_2.py`](../brody_world_physique/world_orientation_school_v4_2.py). Tests : [`test_world_orientation_school_v4_2.py`](../tests/test_world_orientation_school_v4_2.py).

1. **Prérequis réels** : lecture seule et rejeu obligatoire de V3, V4, V4.1 ; empreintes des preuves et code contrôlées.
2. **Observation depuis les pixels** : utilisation de l'algorithme V4.1 de composantes connexes. Les coordonnées des composants **ne sont pas fournies à l'élève lors du test**.
3. **Huit leçons supervisées** : le professeur fournit, **pendant l'apprentissage seulement**, le rôle visuel des deux parties (« composant pointu » / « composant plein ») et la direction de la première par rapport à la seconde. Quatre directions : TOP, LEFT, BOTTOM, RIGHT, chacune en deux exemples.
4. **Apprentissage mesuré** : moyenne des signatures de remplissage des deux rôles, et vecteurs unitaires moyens de chaque direction ; le seuil de proximité V4.1 est réutilisé. Les algorithmes de segmentation, distance, rotation et association au plus proche prototype sont **programmés**, pas inventés par le modèle.
5. **Réciproque** : en inversant les vecteurs, le système cherche la direction de l'autre partie par rapport à la première. Exemple conceptuel : POINTED_TOP_OF_BLOCK → BLOCK_BOTTOM_OF_POINTED. La correspondance est une inférence géométrique candidate à partir du vecteur opposé et des exemples appris, **pas** une loi sémantique générale de la réciprocité.
6. **Onze examens conservés** : translation, changement d'échelle, 0°/90°/180°/270°, miroir, composants inversés ; abstention si distance trop grande, un composant unique, rôles identiques, orientation oblique hors de la classe connue, observation occultée.
7. **Nouvelle reconstruction** : objectif relationnel `LEFT` donné sans boîtes de positionnement ; l'élève transforme les pixels des composants précédemment observés, les repositionne selon le vecteur appris et **enregistre son dessin avant révélation** d'une nouvelle référence fabriquée séparément.
8. **Mesures séparées** : erreur pixel XOR et meilleur/moins bon qu'une page blanche **ET**, indépendamment, conformité de la relation directionnelle et de sa réciproque. Ne jamais remplacer le score négatif de dessin par le score positif de relation.
9. **Traçabilité du monde** : les 11 essais sont instanciés dans les contrats locaux existants `WorldTransformationV0`, `WorldStateDeltaV0`, `WorldExperienceCandidateV0`; y compris HOLD et contradiction. Candidate-only, aucun `WorldStateV0` canonique ni autre mémoire souveraine.

### Ne pas surestimer

- **Quatre rotations cardinales en 2D ne sont pas « apprendre 360° »** : ni transformation libre sous toutes les valeurs d'angle, ni changement de perspective 3D, ni identité d'un objet physique à travers plusieurs images réelles.
- « POINTED / BLOCK » sont des **rôles morphologiques enseignés**, pas « toit », « maison », ni types d'objets découverts dans le monde réel.
- **Proximité/orientation ≠ causalité ou identité**. Le choix du repère 64×64 est explicite ; en repère inconnu, la procédure répond HOLD.
- Une **occlusion** peut rendre la segmentation impossible : abstention obligatoire, pas complétion imaginée.
- Le rapport de classement et les engagements JSONL sont reproductibles mais **ne prouvent pas un ordre temporel externe cryptographiquement attesté** : professeur et élève partagent toujours le même processus de simulation.
- **La mémoire du monde** : nos expériences V4.2 sont des candidates reliées au monde représenté. `WORLD_STATE != MEMORY` et `OBSERVATION != TRUTH` restent vrais. Native Memory non écrite, B8 non appelé.
- **SENS** est en pause sur son B8/09d4fe74 local selon le checkpoint fourni. Pas de modification de SENS, GPS, kernel, Trading ou Brody runtime externe.

## Résultats reproductibles et lecture honnête

La première batterie CI du cours a obtenu **8 leçons, 11 examens, 11 réponses/abstentions conformes, 5 HOLD et 6 relations réciproques** (Windows Python 3.14 et Linux 3.11/3.12). Elle a également mesuré une **reconstruction non meilleure qu'une page blanche en comparaison pixel exacte** : 536 pixels de différence, contre 536 pixels d'encre sur la référence. Ceci constitue un **échec de fidélité pixel**, et non un problème de rejeu. Il reste enregistré.

Pour la reconstruction, une deuxième métrique structurelle vérifie séparément, après révélation de la référence, si les deux images satisfont l'orientation relative LEFT et son inverse RIGHT. Ce test ne doit **jamais** masquer l'échec de fidélité pixel. Des formes éloignées de quelques pixels peuvent respecter la relation tout en étant mal alignées dans la métrique XOR.

Voir [l'exécution CI](https://github.com/Eaubin08/brody-world-physique-obsidien-/actions/runs/37858203571).

## Commandes sur ton PC fixe (reprise des preuves existantes)

Depuis `C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image` :

```powershell
git pull --ff-only origin main

$v3  = "build\dessin-memoire-v3-20261009-000320"
$v4  = "build\monde-brody-v4-20261009-002625.json"
$v41 = "build\relations-v4-1-20261009-003945"
$out = "build\orientation-v4-2-$(Get-Date -Format yyyyMMdd-HHmmss)"

py -m brody_world_physique.world_orientation_school_v4_2 --prior-v3 $v3 --prior-v4 $v4 --prior-v4-1 $v41 --out $out
if ($LASTEXITCODE -ne 0) { throw "V4.2 cours en échec" }

py -m brody_world_physique.world_orientation_school_v4_2 --prior-v3 $v3 --prior-v4 $v4 --prior-v4-1 $v41 --verify $out
if ($LASTEXITCODE -ne 0) { throw "V4.2 rejeu en échec" }

Invoke-Item "$out\images"
notepad "$out\evaluation.json"

# Publie seulement PNG et JSON/JSONL du dossier choisi, sur la branche
# evidence/brody-local existante ; jamais sur main. Identité issue du
# précédent commit d'archives, sans exposer d'e-mail dans ce script.
.\scripts\publish_local_evidence.ps1 -RunPath $out
```

La publication se fera depuis le **worktree d'archives** déjà créé par l'utilisateur. Ce script n'envoie pas les autres fichiers du PC ; **les résultats et images synthétiques publiés sont visibles si le dépôt est public**. Il faut lire les JSON avant de publier toute future expérience contenant de vraies images/données personnelles.

## Next : V4.3 après lecture des preuves du PC

Faire varier l'angle entre 0 et 360° hors des quatre orientations enseignées ; distinguer **transformation du repère** et **transformation de l'objet**, identifier les parties à travers rotations avec bruit et occlusions, confronter les hypothèses à des événements du monde réel quand les interfaces F16 le permettent. Conserver les échecs, ne pas coder à l'avance des étiquettes d'examen comme des lois apprises.
