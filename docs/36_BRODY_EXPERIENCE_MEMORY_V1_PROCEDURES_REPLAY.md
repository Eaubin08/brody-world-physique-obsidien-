# 36 — BRODY_EXPERIENCE_MEMORY_V1 : une expérience mémorise aussi la méthode et son code

**Date : 2026-10-08. Domaine : Brody Image / école de dessin V1.**  
**Statut : implémentation locale réversible + tests de contrat + replay, non canonique.**  
**Frontière : ni mutation du kernel KX108, ni écriture Native Memory, ni entraînement d'un nouveau modèle neuronal.**

## 0 — Motivation précise de l'utilisateur

Après réception des véritables dessins sur son PC, l'utilisateur explicite un principe **à conserver dans la vision du projet** : Brody ne doit pas retenir que le dessin produit ; il doit garder ensemble la **démarche**, les **mécanismes de code qui lui permettent de faire**, la **manière d'interpréter**, le **choix de méthode**, la **correction**, les échecs et les conditions de réemploi. L'ensemble perception → représentation → méthode → code → exécution → retour d'erreur → mémoire doit être **relatif aux mêmes preuves** ; sinon on ne stocke qu'une collection d'images.

Cette intention se raccorde à [34 — audit Drive](34_ECOLE_DE_DESSIN_MEMOIRE_EXPERIENTIELLE.md) et à [35 — classe de dessin V1](35_ECOLE_DESSIN_V1_COURBES_GOMME_MEMOIRE.md). Sources Drive déjà croisées :

- [FSO / Formule du Savoir Obsidia](https://docs.google.com/document/d/14yk4MPqd5rd3RnB1AAyys8zHU4KD4Dq1eqNtLQFJTA0/edit) : apprentissage humain par enseignement → pratique → vérification, réciproque image, méthode du peintre, source/IN ;
- [Mémoire d'expérience intégrée](https://docs.google.com/document/d/1SdeEtK9zpZoAgnyTSQtjbwTYO0cDG3_iFqgBof5kRPA/edit) : catégories vie/épisode/chronologie, relecture et post-mortem, concepts à distinguer du runtime ;
- [Apprentissage organique](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit) : pistes historiques de mémoire/perception/interprétation dont l'état de déploiement doit être **audité**, pas supposé.

**Attribution :** la demande de lier code, choix et mémoire est l'intention exprimée par l'utilisateur. Les noms et la sérialisation V1, les SHA-256, le rejeu vérificateur et les seuils numériques sont des **choix d'ingénierie de l'assistant**. Le système de dessin actuel ne forme pas spontanément ses propres interprétations sémantiques et ne choisit pas encore librement des outils ; **il applique un choix algorithmique déterministe fourni**.

## 1 — Ce qui est réellement enregistré

Chaque leçon **et** chaque examen du moteur [`drawing_school_v1.py`](../brody_world_physique/drawing_school_v1.py) produit désormais un épisode `experience_episodes_v1/<id>.json`, conforme au contrat codé [`experience_memory_v1.py`](../brody_world_physique/experience_memory_v1.py).

| Axe | Champs concrets | Ce qui est prouvé et ce qui ne l'est pas |
|---|---|---|
| **Observation** | `source_ref`, `source_sha256`, `source_kind=SIMULATED`, IN de copie, `teacher_source_visible` | La référence originale est préservée ; pas une photo réelle ni une preuve d'objet physique |
| **Interprétation** | nombre de pixels encrés, bbox (X/Y), signature raster 8×8, incertitudes | Mesure **algorithmique** d'un motif 2D ; `semantic_shape_understood=False` |
| **Choix** | source du souvenir, score pixel XOR, méthode retenue, alternatives comptées, gate du souvenir | Raisonnement **déterministe codé**, pas introspection d'une pensée libre |
| **Procédure / code** | `capability`, `module_path`, `symbol`, SHA-256 exact des fichiers Python, Pillow version, paramètres effectifs | La mémoire **apporte la référence au vrai code** ; elle n'embarque pas de script à exécuter |
| **Exécution** | gestes initiaux et finaux, opérations `ADD/ERASE/REPLACE`, indices, gestes retirés/ajoutés, scores avant/après | Chaque geste est rejouable indépendamment des résumés de scores |
| **Évaluation** | erreur page blanche, erreur souvenir brut, erreur après filtrage, erreur finale, modèle visible | Mesure du dessin, **pas** validation de compréhension ou de valeur artistique |
| **Compétence candidate** | séquence de gestes, référence SHA de la leçon, statut `CANDIDATE_ONLY` | Réemploi candidat ; **aucune promotion de savoir** |
| **Chemins refusés** | `NEGATIVE_SKILL_TRANSFER`, compte des gestes alternatifs non retenus, motif du refus | Les échecs sont conservés ; le détail individuel de toutes les alternatives n'est pas enregistré |
| **Autorité** | `memory_write_allowed=False`, `auto_promotion_allowed=False`, `emits_act=False`, `KX108_ONLY` | Pas de décision souveraine ou d'écriture de mémoire native |

**Important :** ne pas attribuer le terme « interprétation » à un raisonnement sémantique que le module n'effectue pas. Le champ `interpretation` de cette V1 documente ce que **l'algorithme constate**, avec `text_interpretation_claim=null`. Les capacités symboliques Brody / OS Trad-IR / F16 restent de futurs raccordements soumis à la gouvernance.

## 2 — Mémoire épisodique + mémoire des procédures + source du code

```text
source image immuable / intention de copie
      ↓ observation raster et candidat d'interprétation
      ↓ mémoire de gestes (ou zéro souvenir)
      ↓ sélection déterministe de procédure + score
      ↓ TRACE CHAQUE ADD / ERASE / REPLACE ; alternatives refusées
      ↓ image résultante / score réel
      ↓ 10 épisodes candidats + index + registre de capacités référencées
      ↓ rejouer les gestes à partir du code connu et vérifié
      ↓ consultation READONLY du savoir-faire candidat
      [PAS D'ÉCRITURE Native Memory ; PAS DE PROMOTION]
```

Un épisode garde l'empreinte **du fichier Python effectivement présent lors de l'exécution**, au lieu de recopier son texte entier dans la mémoire. Le registre `procedure_registry_v1.json` contient le vocabulaire borné des capacités réelles :

- `image-thinning` → `suggest_gestures_from_reference` ;
- `pixel-feedback-revision` → `correct_drawing` ;
- `drawing-motor-render` → `render` ;
- `image-pixel-comparison` → `black_pixels`.

À la relecture, ces références sont contrôlées **contre une liste blanche codée**, et leurs empreintes SHA-256 sont comparées aux fichiers présents. **Jamais de `eval`, de `exec` ni d'import dynamique déclenché par du texte mémorisé.** Une version modifiée, une chaîne locale altérée ou une mauvaise référence fait **échouer la vérification**, plutôt que de prétendre qu'un ancien résultat a été rejoué.

La comparaison Pillow exige aussi **la version de bibliothèque enregistrée** : elle peut être reproductible avec la même pile logicielle, mais **il n'y a pas de garantie de replay inter-version**. La chaîne JSONL locale est une vérification d'intégrité **non authentifiée** (quelqu'un qui contrôle les fichiers et recalcule toute la chaîne peut la falsifier) ; elle n'est pas le Merkle Seal canonique d'Obsidia.

## 3 — Ce qui est désormais vérifié

[`verify_memory_bundle(root)`](../brody_world_physique/experience_memory_v1.py) audite notamment :

1. **Source :** empreinte SHA de la vraie image modèle ; source originale jamais remplacée ;
2. **Code :** module, fonction, contenu SHA, dépendance Pillow, absence d'exécution de code apporté par une mémoire non fiable ;
3. **Ordre :** chaque opération est vraie et bornée, son index et son geste correspondent au dessin précédent ;
4. **Correction :** chaque geste sélectionné réduit strictement l'erreur réellement recalculée ;
5. **Sortie :** image enregistrée identique au dessin recréé en rejouant les gestes (avec la même pile logicielle) ;
6. **Mémoire :** vérification de la chaîne JSONL, lien SHA vers chacun des épisodes et vers la mémoire candidate de gestes ;
7. **Choix du souvenir :** retrouver la même compétence initiale à partir de la signature raster source, pas simplement faire confiance au récit écrit ;
8. **Droits :** pas de `PROMOTED`, pas d'`ACT`, pas de `memory_write`, pas de mutateur kernel.

L'index `experience_memory_index_v1.json` et le registre `procedure_registry_v1.json` assurent la cohérence du lot. Ils n'ont **aucune autorité autonome**.

[`candidate_skill_retrieval_v1.py`](../brody_world_physique/candidate_skill_retrieval_v1.py) montre le raccord expérimental « la mémoire apporte l'outil » : sur une **nouvelle image**, le lecteur contrôle le lot, calcule une signature, suggère une compétence passée et les **références de code autorisées**. Si l'image est vide, trop inconnue ou non vérifiable : `HOLD`. **La requête elle-même n'exécute aucun dessin et ne modifie pas la mémoire.**

## 4 — Résultats du protocole et limites

Les images que l'utilisateur a réellement fait traiter en V1 sur son PC révèlent que l'algorithme suit le contour d'un triangle et d'un cercle, mais la fidélité des courbes/angles dépend encore des outils de squelettisation et de segmentation en gestes. Les scores et échantillons de la classe sont documentés en [35](35_ECOLE_DESSIN_V1_COURBES_GOMME_MEMOIRE.md).

Dans le protocole d'intégration, **4 leçons + 6 examens = 10 épisodes**, et les échecs de rappel, notamment sur une croix et une courbe, restent des événements sourcés. Ce sont des exercices **avec l'image référence visible**, pas du dessin libre. Les 10 épisodes et leurs gestes font l'objet d'un rejeu indépendant via le lecteur vérificateur ; l'intégrité des SHA n'implique pas une compréhension du monde.

**Ce qui n'est pas implémenté ou validé ici :** compréhension du nom « triangle » sans professeur, auto-découverte d'un moteur vectoriel, apprentissage de la sélection de méthodes sans scoring fourni, apprentissage de poids de génération d'image, mémoire diachronique canonique, raisonnement d'OS Trad-IR intégré, créativité libre, composition peinture en couches, vue 360° et lois physiques.

## 5 — Compatibilité avec la vraie Native Memory d'Obsidia

Les [contrats F0](02_CONTRACTS.md) et l'audit du [fichier réel `MemoryCandidate`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/memory/memory_candidate.py) indiquent :

- `MemoryCandidate` : `candidate_id`, `source_id`, `source_type`, `content_hash`, `content_summary`, `status`, `memory_write_allowed=False`, `auto_promotion_allowed=False` ;
- `MemoryCandidateStatus` inclut `CANDIDATE_ONLY`, `NEEDS_REVIEW`, `REJECTED`, `FROZEN`, `PROMOTED_MANUAL_ONLY` ;
- la [liste `MemorySourceType`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/memory/memory_source_types.py) **dans le snapshot audité** ne propose pas encore de type `WORLD_EXPERIENCE` / `DRAWING_EXPERIENCE` spécifique ;
- le [reader Native Memory de Brody](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/apps/obsidia_api/brody_obsidia_native_memory.py) est **readonly**.

**Décision :** ne pas inventer une deuxième autorité mémoire. Une future passerelle doit auditer les branches actives et la taxonomie de source, puis traduire l'épisode local en **candidat d'entrée**, vérifiable, sous contrôle de promotion externe. Le prototype actuel écrit **uniquement** dans `build/<run>/`.

## 6 — Commandes Windows reproductibles

Depuis `C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image` :

```powershell
git pull --ff-only origin main

$out = "build\ecole-memoire-v1-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.drawing_school_v1 --out $out

# 1 — Relire TOUTE la chaîne d'expérience et les traces de code
py -m brody_world_physique.experience_memory_v1 --verify $out

# 2 — Demander à la mémoire quel geste et quelle procédure elle suggère
# sur un dessin différent de ceux de l'entraînement
py -m brody_world_physique.candidate_skill_retrieval_v1 --memory $out --image "$out\teacher_images\examen_triangle.png" --max-distance 16

# 3 — Visualiser les images, procédures et épisodes sourcés
Invoke-Item "$out\attempts"
Invoke-Item "$out\experience_episodes_v1"
notepad "$out\procedure_registry_v1.json"
```

Contenu du dossier : `teacher_images/`, `attempts/`, `candidate_skill_memory.json`, `candidate_experience_ledger.jsonl`, `experience_episodes_v1/`, `experience_memory_index_v1.json`, `procedure_registry_v1.json` et `evaluation.json`. Aucun modèle à télécharger ni serveur supplémentaire à lancer.

## 7 — Mesure suivante nécessaire

Pour démontrer autre chose que la copie guidée, il faut **cacher le modèle après une courte observation**, générer la réponse **avant** de revoir la référence, puis comparer **à référence égale** les erreurs 0 / 1 / N leçons et plusieurs stratégies. Ensuite choisir une méthode *en apprenant sur les épisodes antérieurs*, et non uniquement par un score fourni à chaque pas. À terme, connecter l'interprétation Brody/OS Trad-IR sous contrats F16 et la mémoire gouvernée, tout en préservant le choix limité de procédure et l'autorité unique KX108.
