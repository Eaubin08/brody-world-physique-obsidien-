# OBSIDURE — Fiche de promptage V1

## 13. Grammaire de prompt Obsidure

C’est la partie qui manquait. Les anciens runs utilisaient une **carte opérateur structurée** : `Mode`, `Layer`, `Scope`, `Risk`, `Files touched`, puis l’objectif, les contraintes, les contrôles, la sortie attendue et les conditions d’arrêt.

Cette structure n’est pas une grammaire machine obligatoire du CLI actuel. Obsidure transmet le texte complet à OS_TRAD_REVERSE ; si l’API est absente, le fallback classe surtout l’intention par mots-clés et extrait les chemins cités. Les deux-points et points-virgules servent donc à rendre l’instruction stable, lisible et beaucoup moins ambiguë.

### 13.1 Règles de ponctuation

- `:` attribue une valeur à un champ : `MODE: READ_ONLY`.
- `;` sépare deux champs dans une instruction compacte sur une seule ligne.
- `,` sépare plusieurs valeurs appartenant au même champ.
- `/` précise une couche et sa sous-couche : `OBSIDURE/MODULES`.
- `=` est réservé aux résultats techniques ou invariants attendus : `TEST_EXIT=0`.
- Le point final termine l’instruction complète ; il ne remplace pas un séparateur de champ.

**Règle PowerShell essentielle :** tout le prompt compact doit rester entre les guillemets de `-Objective`. Un point-virgule placé hors des guillemets devient un séparateur de commandes PowerShell.

```powershell
# Correct : les points-virgules appartiennent au texte transmis à Obsidure
.\scripts\run_agent_obsidure.ps1 -Objective "MODE: READ_ONLY ; LAYER: OBSIDURE/MODULES ; SCOPE: MODULES_OPENING_GATE ; OBJECTIVE: AUDITER la famille MODULES ; OUTPUT: REPORT_ONLY" -DryRun

# Incorrect : le premier point-virgule termine la commande PowerShell
.\scripts\run_agent_obsidure.ps1 -Objective "MODE: READ_ONLY" ; LAYER: OBSIDURE/MODULES
```

Éviter les guillemets doubles à l’intérieur de l’objectif. Utiliser des apostrophes simples pour un nom cité, ou supprimer les guillemets internes.

### 13.2 Ordre canonique des champs

Utiliser toujours le même ordre :

1. `MODE`
2. `LAYER`
3. `SCOPE`
4. `RISK`
5. `OBJECTIVE`
6. `BASE` ou `CONTEXT`
7. `FILES_ALLOWED`
8. `NO_TOUCH`
9. `EXPECTED`
10. `CHECKS`
11. `STOP_IF`
12. `OUTPUT`
13. `AUTHORITY`

Modèle compact canonique :

```text
MODE: <READ_ONLY|PATCH_PROPOSAL|LEAN_SANDBOX> ;
LAYER: OBSIDURE/<FAMILLE_OU_DOMAINE> ;
SCOPE: <IDENTIFIANT_UNIQUE_DU_LOT> ;
RISK: <NONE|LOW|MEDIUM|HIGH> ;
OBJECTIVE: <UN VERBE + UNE CIBLE EXACTE> ;
BASE: <ÉTAT, HEAD, TAG OU SOURCE ATTENDUE> ;
FILES_ALLOWED: <CHEMINS AUTORISÉS SÉPARÉS PAR DES VIRGULES> ;
NO_TOUCH: <ZONES PROTÉGÉES OU HORS SCOPE> ;
EXPECTED: <RÉSULTAT OBSERVABLE> ;
CHECKS: <TESTS ET CONTRÔLES> ;
STOP_IF: <CONDITION D’ARRÊT> ;
OUTPUT: <REPORT_ONLY|PATCH_PROPOSAL_ONLY> ;
AUTHORITY: KX108_ONLY.
```

Une instruction Obsidure doit idéalement respecter la règle : **un mode, une couche, un scope, un objectif principal, une sortie**.

### 13.3 Les modes à ne pas mélanger

- `MODE: READ_ONLY` ou `AUDIT_ONLY` : inspection et rapport, aucun fichier touché.
- `MODE: PATCH_PROPOSAL` : création d’un proposal et d’un receipt, sans intégration canonique automatique.
- `MODE: LEAN_SANDBOX` : génération et test d’un candidat Lean périphérique.
- `APPLY` : ne pas l’enfouir dans un long prompt. Utiliser directement `-Apply <PROPOSAL_ID>` après revue humaine.

Ne jamais demander dans le même objectif : audit global, génération, apply, commit et push. Chaque transition doit être séparée et contrôlée.

### 13.4 Mots qui routent l’intention actuelle

Le fallback local actuel reconnaît surtout les mots suivants :

- Audit : `AUDITER`, `SCAN`, `VÉRIFIER`, `CHECK`, `INSPECTER`.
- Patch : `CRÉER`, `GÉNÉRER`, `BRANCHER`, ou la présence de chemins/extensions comme `.py`, `.json`, `.md`.
- Lean : `LEAN`, `THÉORÈME`, `PREUVE`, `PROOF`.
- Mémoire : `MÉMOIRE`, `MEMORY`, `SRL`, `SESSION`.

**Cas Lean hors ligne :** commencer l’objectif par `THÉORÈME LEAN:` ou `PREUVE LEAN:` plutôt que par `Créer un théorème...`. Dans le fallback actuel, les mots de création sont évalués avant le mot Lean ; une formulation mal ordonnée peut donc être routée comme patch générique.

Toujours citer les chemins exacts quand ils sont connus. Le moteur extrait les chemins présents dans le texte et les ajoute à la cible du proposal.

### 13.5 Format développé pour les gros lots

Pour un chantier important, utiliser la carte développée plutôt qu’une phrase compacte :

```text
MODE: READ_ONLY
LAYER: OBSIDURE / MODULES
SCOPE: MODULES_FILE_WIRING_FAMILY_OPENING_GATE
RISK: NONE
FILES TOUCHED: none

OBJECTIVE
Auditer la famille MODULES et établir son census physique stable.

BASE EXPECTED
Branche, HEAD, ledger et état Git attendus.

FILES ALLOWED
Chemins ou répertoires consultables dans ce lot.

ABSOLUTE CONSTRAINTS
Aucune mutation ; aucune création ; aucune modification Kernel/X108 ; aucun apply.

CHECKS
Sources, propriétaires, imports/loaders, consommateurs, tests, preuves, chevauchements et blockers.

STOP CONDITIONS
STOP si la source canonique, le propriétaire ou le consommateur réel reste ambigu.

REQUIRED OUTPUT
Rapport uniquement avec totaux, chemins primaires, relations secondaires, blockers et décision de passage au micro-lot suivant.
```

C’est cette forme qui correspond le mieux aux anciens prompts de travail : en-tête de situation, périmètre, contraintes absolues, phases, contrôles, sortie imposée et verdict.

### 13.6 Exemples prêts à utiliser

#### Audit readonly d’une famille

```powershell
.\scripts\run_agent_obsidure.ps1 -Objective "MODE: READ_ONLY ; LAYER: OBSIDURE/MODULES ; SCOPE: MODULES_FILE_WIRING_FAMILY_OPENING_GATE ; RISK: NONE ; OBJECTIVE: AUDITER la famille MODULES et établir le census physique stable ; BASE: ledger canonique et dépôt courant ; FILES_ALLOWED: lecture du dépôt, registres, tests et documents liés à MODULES ; NO_TOUCH: NO_GIT_MUTATION, KERNEL_X108, SEALED_PROOFS, PARALLEL_DIRTY_FILES ; EXPECTED: total items, chemins physiques, propriétaires, loaders, consommateurs, tests, relations secondaires, chevauchements et blockers ; CHECKS: aucune relation fondée uniquement sur le nom ou l’existence du fichier ; STOP_IF: source canonique, propriétaire ou consommateur ambigu ; OUTPUT: REPORT_ONLY ; AUTHORITY: KX108_ONLY" -DryRun
```

#### Proposal Python minimal

```powershell
.\scripts\run_agent_obsidure.ps1 -Objective "MODE: PATCH_PROPOSAL ; LAYER: OBSIDURE/MODULES ; SCOPE: MODULES_WAVE001_MINIMAL ; RISK: LOW ; OBJECTIVE: BRANCHER le premier micro-lot MODULES vers un consommateur existant ; BASE: census MODULES validé ; FILES_ALLOWED: path/to/module.py, path/to/consumer.py, tests/test_module_wiring.py ; NO_TOUCH: KERNEL_X108, SIGMA_CORE, SEALED_PROOFS, MANIFESTS, PARALLEL_DIRTY_FILES ; EXPECTED: import réel, consommation observable et test de non-souveraineté ; CHECKS: py_compile, pytest ciblé, diff check et scope exact ; STOP_IF: un quatrième fichier, une nouvelle route artificielle ou un consommateur non prouvé devient nécessaire ; OUTPUT: PATCH_PROPOSAL_ONLY ; AUTHORITY: KX108_ONLY" -MaxCycles 1
```

#### Proposal Lean périphérique

```powershell
.\scripts\run_agent_obsidure.ps1 -Objective "MODE: LEAN_SANDBOX ; LAYER: OBSIDURE/LEAN ; SCOPE: P107_TEMPORAL_GUARD ; RISK: LOW ; OBJECTIVE: THÉORÈME LEAN sur la monotonie structurelle de beforeTau ; BASE: Obsidia.Basic et TemporalKernel en lecture seule ; FILES_ALLOWED: proofs/lean/Obsidia/GeneratedPeripheral/P107.lean ; NO_TOUCH: OFFICIALIZED_LEAN_SURFACE, MANIFESTS, SEALS, KERNEL_X108 ; EXPECTED: théorème périphérique compilable sans vérité sémantique du monde ; CHECKS: lake build, zéro sorry, zéro admit, zéro unsafe ; STOP_IF: axiome non autorisé ou modification d’une surface scellée nécessaire ; OUTPUT: PATCH_PROPOSAL_ONLY ; AUTHORITY: KX108_ONLY" -Domain LEAN -MaxCycles 1
```

#### Apply après validation humaine

```powershell
# Pas de long prompt : l’ID exact suffit
.\scripts\run_agent_obsidure.ps1 -Apply <PROPOSAL_ID>
```

### 13.7 Les pièges de formulation

- Point-virgule hors des guillemets PowerShell : la commande est coupée.
- Plusieurs verbes souverains dans le même objectif : `auditer + corriger + appliquer + committer`.
- Scope sans chemins ni famille identifiée.
- Sortie floue : « fais au mieux », « continue », « branche tout ».
- Condition STOP absente.
- Mention de `PUSH`, `MERGE`, `KERNEL`, `LEAN` ou `PROOF` interprétée comme risk flag par le fallback, même dans une interdiction. Un risk flag signale une zone sensible ; il ne prouve pas à lui seul que l’objectif est mauvais.
- Formulation Lean commençant par `Créer` lorsque l’API est hors ligne.
- `FILES_ALLOWED` trop large, tel que `apps/` ou `periphery/` entier.

### 13.8 Générateur de prompt à remplir

```text
MODE: __________ ;
LAYER: OBSIDURE/__________ ;
SCOPE: __________ ;
RISK: __________ ;
OBJECTIVE: __________ ;
BASE: __________ ;
FILES_ALLOWED: __________ ;
NO_TOUCH: __________ ;
EXPECTED: __________ ;
CHECKS: __________ ;
STOP_IF: __________ ;
OUTPUT: __________ ;
AUTHORITY: KX108_ONLY.
```

Après remplissage, placer tout le bloc compact entre les guillemets de `-Objective`, puis garder les options CLI comme `-Domain`, `-DryRun` et `-MaxCycles` à l’extérieur des guillemets.

