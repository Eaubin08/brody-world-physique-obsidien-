# 38 — BRODY DRAWING SCHOOL V3 : dessiner sans conserver le modèle sous les yeux

**Source du cahier des charges :** formulation utilisateur du 08/10/2026, à partir de la classe de dessin V1, de la sélection d'instruments V2 et de la mémoire procédurale : « dessiner immédiatement après observation, refaire après plusieurs autres exercices, construire une forme nouvelle en réutilisant les gestes appris ; conserver représentation, choix de l'instrument, procédure, corrections ; dessiner avant de revoir la référence ». Ce document décrit la **proposition d'ingénierie implantée** ; il ne réécrit pas les concepts historiques de l'auteur.

**Fichiers :** [`drawing_memory_school_v3.py`](../brody_world_physique/drawing_memory_school_v3.py), [tests V3](../tests/test_drawing_memory_school_v3.py). Sources doctrinales et expériences préalables : [34 — école et mémoire](34_ECOLE_DE_DESSIN_MEMOIRE_EXPERIENTIELLE.md), [35 — gestes/gomme](35_ECOLE_DESSIN_V1_COURBES_GOMME_MEMOIRE.md), [36 — procédure/code/choix](36_BRODY_EXPERIENCE_MEMORY_V1_PROCEDURES_REPLAY.md), [37 — crayon/stylo/plume](37_ECOLE_INSTRUMENTS_SELECTION_EXPERIENTIELLE_V2.md).

## Les trois examens ne sont pas interchangeables

| Niveau | Information donnée à Brody lors du dessin | Ce qu'on vérifie | Ce qu'on ne peut PAS conclure |
|---|---|---|---|
| **V3-A — immédiat** | Une représentation en **gestes** extraite d'un pentagone synthétique inédit, après que la référence a été retirée de l'interface élève | Le dessin peut-il être reproduit **depuis la représentation sauvegardée uniquement** ? | Ce n'est pas une mémoire biologique : l'encodeur humain a déjà vectorisé le contour |
| **V3-B — différé** | **Le même souvenir de gestes rechargé depuis un fichier**, après trois autres exercices d'observation/représentation distincts | La trace reste-t-elle récupérable et utilisable malgré trois interférences ? | Ce n'est **pas un délai réel chronométré**, ni un test d'oubli spontané : les représentations sont identifiées par des clés fiables |
| **V3-C — transfert** | Les **gestes candidats** des anciennes leçons `cours_carre` et `cours_triangle`, et une **consigne explicite de placement en rectangles**. Aucune image du dessin final n'est montrée | Peut-il recombiner des procédures déjà apprises et produire une **nouvelle composition** avant la révélation ? | Le système ne découvre pas librement un objet « maison » ou son sens : le plan de composition est fourni par le professeur |

Le **pentagone** est une nouvelle référence dessinée uniquement par le professeur, absente des leçons et examens V1/V2. Le **transfert** combine un carré et un triangle pour produire un petit assemblage de type maison, mais l'image cible est dessinée par une fonction professorale distincte de la fonction de transformation des gestes du système.

## Cycle d'expérience réellement exécuté

```text
V1 : gestes vécus + corrections + références du vrai code
      ↓ audit mémoire V1 en lecture seule
V2 : scores vécus crayon / stylo / plume
      ↓ audit mémoire V2 en lecture seule
V3 : révélation brève d'une nouvelle image au MODULE OBSERVATEUR
      ↓ extraction de segments/contours par algorithme existant
      ↓ représentation persistée + SHA (PAS de pixels PNG copiés)
      ↓ le MODULE DESSIN reçoit représentation + choix outil V2, pas image source
      ↓ production de dessin et écriture du reçu AVANT l'évaluation
      ↓ seulement ensuite : ouverture de la référence professeur
      ↓ erreur de pixels binaires / IoU + provenance
      ↓ rapport local de candidat, sans modification Native Memory
```

La séparation est une **frontière d'interface et d'ordre d'appel dans un même processus Python**, pas une sandbox sécurisée : le générateur de test possède le code des références, les gestes sont une compression potentiellement très fidèle des contours et il n'existe pas encore de séparation physique de processus ou de machine entre professeur et élève. C'est une limite de validité du test, pas un détail caché.

Le module apprenant reçoit uniquement un vocabulaire de gestes compatible avec V1 et un choix d'instrument calculé d'après la mémoire gelée V2 ; il n'est pas formé de poids neuronaux ni ne dispose de représentations artistiques sémantiques. Le retour d'erreur sur une image **n'est utilisé qu'après** le reçu enregistré ; il n'influence aucun dessin de la batterie en cours.

## Pièces et contrôles

- `representations/immediate_pentagon.json` et `delayed_pentagon.json` : mémoire détaillée d'un contour ; empreintes et géométrie bornées, sans bitmap brut ;
- `interference/task_01.json` ... `task_03.json` : trois nouveaux épisodes intercalés, sans création de nouvelle représentation du pentagone ;
- `student_images/` : les trois dessins produits avant de révéler les références ;
- `committed_before_teacher_reveal.jsonl` : engagement ordonné de l'outil, des gestes, de la procédure (fichier SHA), des distractions et de la sortie ;
- `teacher_revealed/` : vérités synthétiques ouvertes **après** production et engagement ;
- `candidate_experience_ledger.jsonl` : épisodes d'évaluation candidats, sans promotion ;
- `evaluation.json` : niveaux, erreurs, comparaison à la feuille blanche et limites.

Le vérificateur relit les **mémoires V1 puis V2**, recalcule les gestes proposés, leur rendu, les SHA des images et des procédures, les expériences d'interférence et les choix d'instrument. Une référence ou un engagement modifié entraîne un rejet. **Ce mécanisme vérifie la cohérence de l'ordre de la boucle et de ses artefacts, pas une garantie tierce d'horodatage ni une preuve de raisonnement intérieur.**

## Tests de validité à conserver

- Comparer la sortie mémoire à **une feuille blanche** et utiliser la même métrique sur les trois niveaux ;
- Lorsqu'on remplace la référence **après** observation, l'élève doit produire **le même dessin** puisqu'il n'a plus accès à ses pixels originaux par l'interface de dessin ;
- Rejeter des gestes ou sources modifiés, une empreinte faussée, un nouveau type de dessin non autorisé ou une tentative de mutation Native Memory ;
- Ne pas appeler « généralisation » la simple recomposition d'une recette de placement ;
- Ne pas déclarer « progrès de mémoire » quand la reproduction immédiate et différée sont identiques : le stockage garantit une conservation sans dégradation **dans ce cas contrôlé**, pas une amélioration cognitive.

### Commandes PowerShell sur le PC fixe

Depuis le dépôt Windows `brody-world-physique-image`, après le prochain commit validé :

```powershell
git pull --ff-only origin main

# Garder les cours V2 réussis : les réutiliser en lecture seule.
$prior = "build\ecole-outils-20261008-234818"
$out = "build\dessin-memoire-v3-$(Get-Date -Format yyyyMMdd-HHmmss)"

py -m brody_world_physique.drawing_memory_school_v3 --prior-v2 $prior --out $out
if ($LASTEXITCODE -ne 0) { throw "Échec V3" }

py -m brody_world_physique.drawing_memory_school_v3 --verify $out
if ($LASTEXITCODE -ne 0) { throw "Rejeu mémoire V3 échoué" }

Invoke-Item "$out\student_images"
Invoke-Item "$out\teacher_revealed"
```

**Important :** un ancien dossier V2 peut être refusé si la version des fonctions de V1/V2 épinglées a changé depuis la sauvegarde. Dans ce cas, ne pas supprimer ou modifier les preuves antérieures ; créer un nouveau dossier V2 avec la version courante puis rejouer la V3.

## Prochaine progression une fois V3 lue

1. **Séparer matériellement professeur et élève** : le premier donne un paquet signé/figé de représentation, le second dessine dans un processus ayant strictement **aucun accès** à la référence, et le jury compare hors ligne.
2. **Dessin sans contour vectorisé complet** : mémoriser des primitives plus abstraites, tester une compression volontairement bornée et comparer le coût du souvenir à la qualité du dessin.
3. **Rappel avec vraie distraction** : plusieurs sources semblables, noms cachés et sélection de souvenir nécessaire, plutôt que reprise directe par ID.
4. **Transfert sans recette géométrique explicite** : intention sous forme de description, hypothèses de composition candidates, comparaison différée, puis correction mesurée.
5. **Cours de dessin réels** : images/tâches externes et annotateurs humains ; différencier copie exacte, qualité esthétique, proportions, invariants, style, textures, outils, rotations 360°, réciproque et couches du peintre.
6. **Gouvernance mémoire** : l'expérience restera une proposition candidate en local jusqu'à audit de l'adaptateur canonique. `KX108_ONLY`, `memory_write=False`, `auto_promotion=False`.
