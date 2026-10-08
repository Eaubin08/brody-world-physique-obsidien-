# 35 — Atelier de dessin V1 : reprendre le crayon, effacer, tracer des courbes, réutiliser ses gestes

**2026-10-08 — Brody Image.** Suite aux images et à la sortie Windows `ecole-dessin-20261008-225534` partagées par l'utilisateur (V0, 3 leçons, 4 examens). **V1 codée et testée en CI ; reproduction sur le PC fixe de l'utilisateur à faire.**

## 1. Pourquoi cette passe : le contre-exemple du triangle

Les images réellement communiquées montrent un **triangle à segments irréguliers** et un carré/trait correctement dessinés. La V0 utilisait surtout un répertoire de petits segments tracés et ne savait pas rectifier efficacement un geste ancien. L'essai V0 `exam_03` restait à 168 pixels d'erreur avant ET après la correction. De plus, la V0 renvoyait une copie vide si un souvenir faisait pire qu'une page blanche : bon refus, mais pas encore apprentissage de l'effacement.

La solution n'est pas d'annoncer que Brody « connaît le triangle » ni d'injecter le modèle vectoriel original à la place de l'élève. Il faut **modifier son atelier de dessin**, lui donner des gestes plus riches et un protocole de retour d'erreur mémorisé.

## 2. Origine documentaire et frontière utilisateur/ingénierie

Les archives Drive précédemment relues confirment :
- **U / FSO :** apprentissage humain comme une école, leçon/pratique/évaluation ; source [Formule du Savoir Obsidia](https://docs.google.com/document/d/14yk4MPqd5rd3RnB1AAyys8zHU4KD4Dq1eqNtLQFJTA0/edit), formulations utilisateur ~lignes 1 et 179.
- **U / FSO :** réciproque lecture ⇄ génération, ne pas réinventer la lecture/affichage déjà fournis par l'informatique, ~350 et ~450.
- **U / FSO :** construire *couche par couche et dans le bon ordre* comme le peintre ; garder le master et respecter l'IN, ~626 et ~1275.
- **A / archive historique** : descriptions de boucle mémoire vive, mémoire diachronique, friction, post-mortem, mémoire à couches ; distinguer ces descriptions **de l'implémentation effective**. Voir [34 — école et mémoire](34_ECOLE_DE_DESSIN_MEMOIRE_EXPERIENTIELLE.md) et [05 — learning loop](05_LEARNING_MEMORY.md).
- **P / choix techniques de cette version :** squelettisation raster, chemins connectés, simplification, commande de tracé, recherche d'opérations ADD/ERASE/REPLACE, seuil d'abstention. Ce sont des outils **fournis par l'ingénierie** : pas une découverte autonome de formes géométriques par Brody.

## 3. Implémentation effective

Module : [`brody_world_physique/drawing_school_v1.py`](../brody_world_physique/drawing_school_v1.py). Seule dépendance : Pillow déjà présent. Aucun modèle à installer.

- **Feuille et crayon :** images 64×64 ; chaque geste est un tracé de points 2D, droit ou non rectiligne. Le tracé utilise Pillow (ne recrée ni Windows ni le GPU).
- **Regard :** le professeur montre des pixels noirs sur blanc ; l'élève reçoit les **pixels**, pas les étiquettes sémantiques `triangle` ou `cercle`, ni la liste des segments du professeur.
- **Recherche de geste :** squelettisation du dessin, parcours de chemins, simplification d'un tracé. Une courbe peut être conservée en un geste poly-ligne à plusieurs points ; **aucun moteur Bézier paramétrique/neural entraîné n'est revendiqué**.
- **Rappel :** la mémoire candidate garde une empreinte 8×8 d'encre relative à sa boîte englobante, puis la séquence de points tracés. La reprise peut changer d'échelle et de place. Ce n'est pas un identifiant d'objet sémantique.
- **Correction :** l'élève essaie **ADD** (ajouter), **ERASE** (retirer un tracé posé) et **REPLACE** (substituer un nouveau geste). Une modification n'est conservée que si l'erreur mesurée diminue strictement.
- **Rejet :** si un souvenir brut produit plus de pixels erronés qu'une feuille blanche, il est classé comme **transfert négatif** ; on refuse ses traits sans effacer la trace de l'échec.
- **Examen :** de nouvelles images apparaissent après construction de la mémoire d'entraînement ; cependant les **pixels de référence sont visibles pendant la correction**. C'est de la copie guidée, PAS une capacité à générer un dessin inédit sans modèle.

**Évaluation :** distance en **pixels binaires** entre le tracé et la référence. Elle ignore la beauté, la ressemblance sémantique, les matériaux, la pression du crayon, la couleur et la profondeur.

## 4. Observations expérimentales sur la CI

Résultats calculés dans [GitHub Actions](https://github.com/Eaubin08/brody-world-physique-obsidien-/actions/runs/37845031970) : 4 cours et 6 examens synthétiques, sans modifier l'autorité ni les poids.

| Épreuve inédite | Feuille blanche, erreur | Mémoire filtrée, erreur | Après corrections, erreur |
|---|---:|---:|---:|
| Trait horizontal déplacé | 132 | 9 | 9 |
| Carré déplacé | 380 | 2 | 2 |
| Triangle nouveau | 421 | 132 | **66** |
| Cercle nouveau | 288 | 64 | **60** |
| Croix nouvelle | 413 | 413 (mémoire rejetée) | **56** |
| Courbe nouvelle | 250 | 250 (mémoire rejetée) | **28** |

Les valeurs représentent **des pixels erronés sur un dessin 64×64**, et non un score de qualité visuelle perçue ni une validation sur photographies. Tous les examens ont eu accès au modèle dessiné. Le triangle progresse mais n'est pas exact, le cercle reste imparfait, et les transferts de mémoire ne sont pas tous positifs. **Une erreur réduite n'est pas une preuve que l'algorithme sait ce qu'est un triangle**.

La CI teste les **opérations effectives d'effacement ou de remplacement**, les cas de mauvais rappel, la détection de trajets droits/courbes et la provenance de l'épisode. Le dépôt complet a passé 119 tests sur Python 3.11 et 3.12 à la version de ce protocole.

## 5. À lancer sur le PC fixe

Depuis `C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image` :

```powershell
git pull --ff-only origin main
$out = "build\ecole-dessin-v1-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.drawing_school_v1 --out $out
Invoke-Item $out
```

Dossiers :
- `teacher_images/` : références originales du professeur (pas modifiées) ;
- `attempts/` : `*_souvenir_brut.png`, `*_memoire_filtrée.png`, `*_apres_correction.png`, `cours_*_dessin.png` ;
- `candidate_experience_ledger.jsonl` : événements sourcés chaînés et échecs gardés ;
- `candidate_skill_memory.json` : gestes à réutiliser, **candidats**, pas savoir canonique ;
- `evaluation.json` : résultats complets, statuts, limites et chemins.

Le warning Pillow `Image.Image.getdata` de V0 a été supprimé par le passage à `tobytes()` en niveaux de gris. Ce changement préserve le test de pixels noirs et évite l'API dépréciée.

## 6. Ce qu'il reste à apprendre réellement

**Prochain jalon mesurable :** séparer la copie guidée (modèle visible) du dessin de mémoire (modèle masqué après observation), du transfert de stratégie (image différente, même structure), et de la génération libre (nouvelle composition sans modèle de réponse).

Les versions suivantes devront comparer plusieurs pédagogies — pointillés/gestes guidés, observation seule, mémoire différée, apprentissage par correction, esquisses en couches et transfert de compétences — sans supposer que tous les concepts historiques sont déjà disponibles. Ajouter ensuite des couleurs, ombres, perspective, objets multi-parties, rotation/symétrie et 360° sourcés. Les pistes φ/Fibonacci restent des **contraintes de composition optionnelles**, pas une règle universelle.

**Mémoire :** le moteur `CandidateExperienceLedgerV0` écrit exclusivement dans le dossier local de l'essai. L'index Obsidia Native Memory externe est readonly, `KX108_ONLY`, et ne reçoit **aucune mutation**. Toute passerelle future doit reprendre les vrais types `MemoryCandidate`/`MemoryCandidateStatus` et passer par leurs contrôles de promotion existants ; voir [34](34_ECOLE_DE_DESSIN_MEMOIRE_EXPERIENTIELLE.md).
