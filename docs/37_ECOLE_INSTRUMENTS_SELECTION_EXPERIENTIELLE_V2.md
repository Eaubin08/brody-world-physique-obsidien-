# 37 — Brody Image : école des instruments et choix appris par expérience (V2)

**Date :** 2026-10-08. **Périmètre :** atelier de dessin, choix du moyen d'exécution et mémoire procédurale candidate. **Statut :** exécution et tests CI du prototype ; les sorties Windows utilisateur restent à vérifier. **Source de la demande :** l'utilisateur, après ses premiers vrais dessins sur son PC : « il pourra même choisir stylo, plume, etc. ». Cette étape prolonge directement son principe : la mémoire doit apporter les **méthodes, le code, les choix et les échecs**, pas seulement l'image finie ([36](36_BRODY_EXPERIENCE_MEMORY_V1_PROCEDURES_REPLAY.md)).

## Réconcilier avec la vision — sans remplacer les travaux antérieurs

- **U / utilisateur :** l'apprentissage comme un enfant dans des cours, tests de dessin, méthode, code d'exécution et mémoire d'expérience reliés, exploration d'outils. Définition des intentions, *pas* preuve d'une sélection d'outils autonome à ce jour.
- **Sources archivées / Drive déjà auditées :** [FSO — Formule du Savoir Obsidia](https://docs.google.com/document/d/14yk4MPqd5rd3RnB1AAyys8zHU4KD4Dq1eqNtLQFJTA0/edit) pour l'enseignement/pratique/évaluation et la réciproque ; [Architecture de mémoire — L'Expérience](https://docs.google.com/document/d/1SdeEtK9zpZoAgnyTSQtjbwTYO0cDG3_iFqgBof5kRPA/edit) pour l'épisode et les savoir-faire ; [34 — audit scolaire](34_ECOLE_DE_DESSIN_MEMOIRE_EXPERIENTIELLE.md).
- **P / proposition d'ingénierie testée ici :** trois instruments numériques, trois objectifs donnés par le professeur, un moteur de rendu connu, la moyenne empirique des erreurs par objectif, un refus `HOLD` sans observation antérieure. **Ce choix n'est pas une définition historique imposée par l'utilisateur ni une preuve de goût artistique.**

Ne pas créer un second système généraliste ni un second registre canonique : V2 importe les gestes **de la mémoire locale V1 vérifiée**, conserve les références SHA des fonctions existantes et n'écrit rien dans Native Memory.

## Les instruments réellement implémentés

Module : [`brody_world_physique/instrument_school_v2.py`](../brody_world_physique/instrument_school_v2.py). Pillow est utilisé pour tracer :

| Instrument | Outil numérique V2 | Fonctionnement *programmé*, pas appris |
|---|---|---|
| `PENCIL` / crayon | Trait gris de 3 pixels, léger flou | Simulation rudimentaire d'un rendu doux, pas du graphite réel |
| `PEN` / stylo | Trait noir uniforme de 2 pixels | Simulation d'un trait constant, pas de friction physique |
| `NIB` / plume | Trait foncé de largeur variable de 1–4 pixels selon la direction du segment | Simulation d'une plume large, **pas** dynamique réelle d'encre/pression |

La **capacité à exécuter** chaque outil reste dans le code connu. Ce que Brody teste est **le routage appris entre des outils déjà disponibles**. Le but est de savoir *quand* employer une méthode à partir d'expériences plutôt que coder `if intention == LIGHT: crayon` dans le sélecteur.

### Le professeur et l'élève n'ont pas accès aux mêmes informations

Le professeur définit une cible synthétique correspondant aux objectifs `LIGHT`, `UNIFORM` et `EXPRESSIVE`. Le mécanisme d'apprentissage reçoit l'objectif comme **consigne déclarée**, mais **pas** la table cachée objectif → instrument ; il ne voit que les erreurs mesurées de ses essais. La cible n'est pas une œuvre indépendante : elle est **générée par le même moteur** que les outils testés. Un score de 0 sur la cible attendue est donc **par construction**, non une validation du dessin réaliste ou d'un jugement artistique général.

## L'expérience — observation, choix et mémoire

1. **V1 avant V2.** Une école de dessin V1 est exécutée ou indiquée par `--prior-school` ; elle est **rejouée et vérifiée** en lecture seule : épisodes, gestes acquis, version du code, pièces originales, reçus. Les 3 leçons de traits / triangle / cercle fournissent les gestes source utilisés pour les essais.
2. **Chaque leçon V2 :** le même geste source est exécuté avec chacun des trois instruments. Le professeur montre une cible de finition et mesure la **différence absolue moyenne des pixels gris**. Le système garde dans sa mémoire candidate la table mesurée `tool -> loss`, l'intention, le SHA de l'image source, le SHA de la cible et le SHA du code.
3. **Avant un examen :** sur un nouvel exercice, le système reçoit seulement le **croquis source** et l'**objectif déclaré**. Le sélecteur recherche les expériences antérieures ayant cet objectif ; il choisit l'outil donnant la **plus petite moyenne des erreurs historiques**. Il **ne lit pas la cible future** pour décider et n'utilise pas le nom de la forme pour choisir.
4. **Preuve temporelle :** `choices_before_heldout.jsonl` est écrit et vidé sur disque **avant** que le programme crée puis ouvre la cible de test. Après seulement, le système trace, reçoit le retour et calcule le score. Le programme peut ainsi vérifier son ordre d'exécution, sans prétendre à une preuve cryptographique tierce de l'instant précis.
5. **Épreuve hors distribution :** si le cours n'a pas donné d'expérience pour la consigne, le sélecteur renvoie `HOLD_NO_MATCHING_EXPERIENCE`. Une non-prédiction n'est pas comptée comme un bon outil.
6. **Mémoire gelée pendant TEST :** aucune cible d'examen n'est ajoutée au tableau servant à choisir. Le résultat après coup est archivé comme évaluation, **pas** comme une nouvelle leçon.
7. **Relecture :** `--verify` vérifie le cours V1 amont, l'identité du code, la chaîne locale d'événements, les images d'instruments refaites à partir des gestes mémorisés, les erreurs et les choix recalculés sur mémoire gelée. Une pièce modifiée est refusée.

## Premiers résultats mesurés (suite SIMULATED)

[CI : GitHub Actions 37848120416](https://github.com/Eaubin08/brody-world-physique-obsidien-/actions/runs/37848120416), Python 3.11/3.12, **141 tests PASS** et exécution de la batterie instrumentale.

| Expériences antérieures | Choix émis sur les 4 examens | `HOLD` |
|---|---:|---:|
| 0 leçon | 0 | 4 |
| 1 leçon (intention LIGHT) | 1 | 3 |
| 9 leçons (3 intentions × 3 formes) | 3 | 1 |

Après les neuf leçons, les choix proposés sont `LIGHT→PENCIL`, `UNIFORM→PEN`, `EXPRESSIVE→NIB` ; le quatrième objectif non appris conduit à `HOLD`. Les trois réussites ont **0 erreur moyenne de gris** face à la cible du professeur parce que celle-ci provient du même outil de simulation. **Ce n'est pas de la vraie peinture ni un modèle entraîné de l'esthétique.**

**Contre-épreuve :** en test unitaire, si les expériences préalables associent artificiellement `LIGHT` à une meilleure performance du stylo, le sélecteur propose **PEN**, pas **PENCIL**. Cela montre que le choix dépend des scores mémorisés plutôt que d'un dictionnaire fixe *dans le sélecteur*. La correspondance de finition est cependant fixe **du côté du professeur**, limite essentielle de cette V2.

## Instructions PC fixe — exécution directe

Depuis `C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image` :

```powershell
git pull --ff-only origin main

$out = "build\ecole-outils-$(Get-Date -Format yyyyMMdd-HHmmss)"

# Sans --prior-school, V2 reconstruit une école V1 vérifiée dans son dossier.
py -m brody_world_physique.instrument_school_v2 --out $out --training-lessons 9

# Vérifie le cours V1 source, les essais, l'identité du code et les décisions.
py -m brody_world_physique.instrument_school_v2 --verify $out

# Affiche tous les dessins, pour une comparaison VISUELLE.
Invoke-Item "$out\instrument_art"
```

Pour isoler l'effet de l'apprentissage en **0 / 1 / 9** leçons **sans recréer le cours V1**, choisir un `--prior-school` existant :

```powershell
$prior = "$out\prior_drawing_school_v1"
py -m brody_world_physique.instrument_school_v2 --prior-school $prior --out "$out-cold" --training-lessons 0
py -m brody_world_physique.instrument_school_v2 --prior-school $prior --out "$out-one" --training-lessons 1
```

Ne pas donner aux commandes de V2 des fichiers d'anciens runs dont le code a changé sans vérifier. `--verify` refuse les SHA/procédures incompatibles et n'exécute jamais un script arbitraire provenant de la mémoire.

### Pièces de preuve

- `instrument_skill_memory.json` : expériences candidates et **scores réels par outil** ;
- `instrument_ledger.jsonl` : cours, décisions et retour d'erreur en chaîne locale ;
- `choices_before_heldout.jsonl` : décisions engagées avant les cibles ;
- `instrument_art/` : PNG sources, dessins avec les trois instruments, cibles et propositions ;
- `instrument_experience_index.json` : identifiants et SHA du code, de V1, des épisodes et du ledger ;
- `evaluation.json` : couverture, erreurs, `HOLD`, limites explicites.

## Suite scientifique nécessaire

La prochaine progression **ne devrait pas faire croire que choisir un outil synthétique construit par nous est déjà de l'intelligence artistique**. Il faut des objectifs non écrits comme des étiquettes de cours (`LIGHT`, `UNIFORM`…), des exemples externes, plusieurs façons d'obtenir un même rendu, des outils avec coûts et contraintes réels (bavure, pression, révision, précision, temps), des contre-exemples et des tests en aveugle par contexte, objet et support.

Puis cours **« modèle caché »** : observation initiale limitée → retrait de l'image → choix de méthode et d'instrument depuis les seuls souvenirs → dessin sans rétroaction instantanée → révélation du modèle et comparaison. Ce test distinguera une tentative de mémoire de la copie guidée qui bénéficie encore du modèle visible.

**Frontières inchangées :** `KX108_ONLY`, zéro `ACT` autonome, aucune mutation de kernel ou Native Memory, aucune promotion automatique, sources `SIMULATED`, gestes et code existants vérifiables ; pas de nouveau LLM installé.
