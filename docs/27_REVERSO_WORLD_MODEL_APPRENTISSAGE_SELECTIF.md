# 27 — Reverso ↔ World Model ↔ apprentissage sélectif : première implémentation testable

**Date :** 2026-10-08 · **Périmètre : Brody Image**, méthode originale de l'utilisateur.  
**Statut :** V0 **pixel réversible** + **contrats de relation physique candidate** + **tri des traces d'apprentissage**. Ce n'est PAS une reconstruction sémantique par couches, un World Model appris, ni un apprentissage automatique de Brody.

## 1. Source utilisateur, décisions et attribution

Référence primaire : [FSO — « Formule du Savoir Obsidia et apprentissage full auto »](https://docs.google.com/document/d/14yk4MPqd5rd3RnB1AAyys8zHU4KD4Dq1eqNtLQFJTA0/edit) ; audit de provenance [23](23_BRODY_IMAGE_LEARNING_TRACEABILITY.md), audit visuel [24](24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md) et politique expérience historique [05](05_LEARNING_MEMORY.md).

- **U (utilisateur), FSO ~450 :** isoler une image/objet, la recréer par réciproque, le replacer, changer sa dimension, ajouter des éléments.
- **U, FSO ~626 :** préserver les pixels de l'original après une isolation exacte, travailler « couche par couche ou dans le bon ordre » comme les peintres et l'affichage informatique.
- **U, FSO ~767 :** explorer proportions, art, nombre d'or/Fibonacci ; **hypothèse**, pas formule de perfection démontrée.
- **U, FSO ~850 et ~1009 :** rigueur et liberté stylistique adaptées aux régions et au résultat demandé, tout en préservant la ressemblance avec l'original.
- **U, FSO ~1176 :** appliquer la fidélité d'identité à **tout objet**, pas seulement au visage.
- **U, FSO ~1275 :** « retenir la source ne pas la dénaturer » et respecter l'« IN ».
- **U, FSO ~179 et ~350 :** comprendre *comment on enseigne/apprend* ; ne pas réinventer l'existant, utiliser lecture et création visuelles.
- **U, échanges projet récents :** croiser reproduction de pixels, World Model physique et apprentissage humain — décision de méthode réaffirmée aujourd'hui.
- **P (proposition technique, PAS règle psychologique validée) :** les statuts `KEEP_SOURCE_REFERENCE`, `REFERENCE_ONLY`, `REVIEW_VALIDATED_PATTERN`, `REVIEW_HYPOTHESIS` et `OMIT_FROM_LEARNING_CANDIDATE` ci-dessous sont des **gates candidats** déduits des objectifs, pas des paroles textuelles du concepteur.
- **A (ancienne proposition IA) :** BF/HF, pyramides, FaceLock, exactes formules ρ, etc. ne sont pas revendiqués comme créations originales ou validations empiriques par l'utilisateur.

## 2. La chaîne voulue, sans confondre trois tâches

```text
Image/source + IN
  │
  ├─ REVERSO, pixel/forme :
  │    analyse par parties et couches (V0 = tuiles spatiales SANS sémantique)
  │    reconstruction lossless → comparer chaque valeur RGBA du master
  │
  ├─ WORLD MODEL, sens/physique :
  │    entités / repères / distances / temps / contraintes
  │    preuves indépendantes / lois connues vs hypothèses vs UNKNOWN
  │    F16 / MMonde / F12 existants sont les propriétaires, pas ce module
  │
  └─ APPRENTISSAGE :
       intention → tentative → résultat → écart → explication candidate
       → sélection de ce qu'il est utile de retenir → replay/contre-exemple
       → revue humaine/observation indépendante → mémoire canonique éventuelle
```

Le passage **pixel exact** ne signifie pas que le système *comprend* la gravité ou l'identité de l'objet. Le passage **world model** ne doit pas transformer les opinions du VLM en lois physiques. Le passage **mémoire** ne veut pas dire stocker tous les pixels et toutes les réponses de Qwen : conserver **références, invariants validés, compétences, échecs mesurés, limites/conditions d'application** est une stratégie à tester.

## 3. Premier programme réellement écrit dans ce repo

[`brody_world_physique/reverso_learning_v0.py`](../brody_world_physique/reverso_learning_v0.py).

**Pixel Reverso V0 :**

1. charge une image JPEG/PNG/WebP dans une matrice `RGBA` décodée ;
2. la divise en tuiles **sans perte**, avec référence, ordre, coordonnées et hash SHA-256 individuels ;
3. écrit `lossless_layers/*.png` et `manifest.json` ;
4. reconstruit **depuis les seules tuiles enregistrées**, sous `reconstructed.png` ;
5. vérifie la couverture intégrale, l'absence de chevauchement, les hashes et l'identité de **tous les pixels RGBA décodés** ; échoue si divergence ;
6. permet un **replay ultérieur** à partir du manifeste et des seules tuiles même si le fichier source initial a été retiré.

**Limite :** ce sont des *tuiles spatiales*, PAS des objets identifiés, des couches de peintre BF/HF, un masque IA, une structure 3D ou de la nouvelle création générative. Pour une photo JPEG, **données RGBA décodées identiques**, pas octets JPEG identiques. Une transformation de cadrage, d'ombre ou de perspective impose des critères de fidélité adaptés, pas l'égalité brute des pixels.

**World relation candidate :** `WorldRelationCandidateV0` propose une relation sourcée (ex. `object:A left_of object:B`) sans autorité d'énoncer une loi universelle ; `world_law_proven=True` est rejeté. À raccorder un jour aux identifiants F16/MMonde/F12, pas nouvelle ontologie racine.

**Sélection de savoirs candidats :** `LearningEpisodeSignalV0` + `triage_learning`. Ce tri ne mémorise rien, il étiquette une *proposition de rétention* à examiner.

| Type de contenu | Proposition de traitement | Pourquoi |
|---|---|---|
| Source originale et intention | `KEEP_SOURCE_REFERENCE` | Pouvoir revenir à la référence sans altérer l'IN |
| Pixels bruts et longue description Qwen | `REFERENCE_ONLY` | Garder l'artefact dans son espace source, éviter d'en faire une connaissance canonique |
| Invariant / compétence / échec **confirmé par replay + référence indépendante** | `REVIEW_VALIDATED_PATTERN` | Proposer un savoir réutilisable pour revue, pas écriture automatique |
| Phénomène incertain, loi physique imaginée, invariant non vérifié | `REVIEW_HYPOTHESIS` | Ne pas oublier l'inconnu mais ne pas le transformer en vérité |
| Information sans lien avec l'IN | `OMIT_FROM_LEARNING_CANDIDATE` | Ne pas encombrer une mémoire de travail pertinente |
| Route connue pour échouer, à nouveau proposée | `should_propose_alternate_route=true` | Éviter de répéter une méthode inefficace, après preuve |

Ce **prototype de sélection** ne constitue ni un algorithme humain complet de mémoire, ni la grille finale de l'utilisateur, ni une décision KX108. Son effet réel sur la qualité des réponses/générations **n'a pas encore été benchmarké**.

## 4. Essai sur PC fixe ou portable, sans nouveau modèle

Sur chaque machine, dans le dépôt Brody Image mis à jour :

```powershell
git pull --ff-only origin main
py -m pip install -r requirements-image.txt
py -m unittest discover -s tests -p "test_*.py" -v

# Sur un fichier photo choisi localement. Aucun appel à Qwen, Internet ou Obsidia :
py -m brody_world_physique.reverso_learning_v0 --image "C:\\photos\\reference.jpg" --out "build\\reverso-photo"
```

**Artefacts :** `build/reverso-photo/manifest.json`, `lossless_layers/*.png`, `reconstructed.png`, avec verdict `PASS_EXACT_DECODED_RGBA` uniquement après comparaison réellement calculée.

Attention à la confidentialité : **ne pas committer les photos privées, tuiles, traces de visages ou reçus personnels sur GitHub**. Les sorties restent sur le PC.

## 5. Ce que l'on doit implémenter APRÈS ce premier socle, sans remplacer ta méthode

1. **Reverso sémantique :** segmentation des personnes/objets et régions, couches de peintre ordonnées, relations de position, masques testés ; comparer le coût et les erreurs de plusieurs ordres de reconstruction. Aucun texte Qwen n'est accepté comme masque exact.
2. **World model connecté :** mapper candidats `WorldRelation` sur F16/MMonde/F12, gérer position/temps/changement de point de vue ; évaluer par observations distinctes. **Une photo seule ne démontre pas la dynamique/causalité d'un objet qui tombe.**
3. **Rigueur par région :** propriétés `LOCK / FLEX / IGNORE`, fidélité identité de tout objet, mode artistique, propriétés physiques, grilles Fibonacci/symétrie facultatives, chacune avec protocoles témoins.
4. **Reconstruction/génération réelle :** un générateur adapté au GPU du fixe, sous contraintes et source d'origine ; conserver ses modèles/licences/seed/provenance. Pas besoin de dupliquer Qwen-VL déjà disponible chez Jarvis.
5. **Cycle pédagogique :** démonstration → tentative → erreur → correction/replay → nouvelle situation → revue de l'expérience → Native Memory **si autorisée** ; mesurer ce qui a été retenu utilement et ce qui aurait dû être ignoré. Pas de fine-tuning ni de vérité automatique.
6. **Variant training et monde plus vaste :** reprendre la liste réelle des variantes documentées sans inventer ni lancer 81 entraînements ; comparer les chemins pertinents pour l'image d'abord.

**Critères testables :** BIMG-01/02/03/04/06/09/10 de [24](24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md), en précisant ce qui est disponible vs manquant.

**Frontières :** `KX108_ONLY`, pas de mutation du kernel, mémoire en candidate, providers image non souverains. Le code n'invoque pas de Binder ; un champ `decision_authority` n'équivaut pas à son autorisation.
