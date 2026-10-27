# OBSIDURE — Support opérateur consolidé V2.1

**Statut :** support de reprise consolidé, non freeze canonique  
**Date :** 7 août 2026  
**Sources :** dépôt GitHub, Google Drive et mails envoyés à soi-même

> Ce support reconstruit le « bazar organisé » réellement utilisé pour Obsidure. Il distingue le manuel historique, le CLI actuel, le protocole d’apply et la campagne de branchement en cours.

## Verdict de reconstruction

- Il n’existait pas forcément un document unique dans Drive ou Gmail.
- Le mode d’emploi était réparti entre le manuel du dépôt, le protocole d’apply, les scripts CLI, les mails de reprise et les plans de campagne.
- Le manuel V1 indique encore une copie manuelle des fichiers approuvés, mais le CLI actuel expose désormais `--apply` / `-Apply`.
- Le terminal global reste principalement un cockpit readonly. Pour utiliser Obsidure maintenant, la voie fiable est le CLI standalone.

## Fiche immédiate — les 7 commandes à retenir

```powershell
# 1. Se placer à la racine du dépôt
cd "C:\Users\User\Desktop\obsidia-engine-proof-core\obsidia-x108-proofs_REMOTE_A5F21C6B"

# 2. Vérifier le dépôt avant toute opération
git status --short

# 3. Audit seul, sans création de proposal
.\scripts\run_agent_obsidure.ps1 -Objective "Auditer le branchement du domaine GPS" -Domain GPS -DryRun

# 4. Générer un proposal
.\scripts\run_agent_obsidure.ps1 -Objective "Créer le patch minimal pour ..." -Domain GPS -MaxCycles 1

# 5. Lire les résultats
Get-Content "_PATCH_PROPOSALS\<PROPOSAL_ID>\RECEIPT.md"
Get-Content "_PATCH_PROPOSALS\<PROPOSAL_ID>\proposal.json"

# 6. Appliquer le proposal approuvé
.\scripts\run_agent_obsidure.ps1 -Apply <PROPOSAL_ID>

# 7. Contrôler après apply
git diff --check
git diff --stat
git status --short
```

**Règle absolue :** proposal → contrôle humain → apply → tests → diff/status → commit séparé. Un apply n’est ni une validation finale ni un commit.

## 1. Ce qu’est Obsidure

Obsidure est le bâtisseur et brancheur périphérique d’Obsidia. Il peut auditer, proposer du code, générer des fichiers en sandbox, préparer des patches, produire des receipts et appliquer un proposal explicitement approuvé. Il ne décide pas de l’admissibilité du système.

- **Brody parle et explique.**
- **Sigma retrouve, alerte et guide.**
- **Obsidure construit et propose.**
- **Lean prouve certains invariants structurels.**
- **X108 reste seul détenteur de l’autorité de décision.**

Frontières permanentes : `kernel_mutation=false`, `x108_merge=false`, `emits_act=false`, `allowed_to_decide=false`, `decision_authority=KX108_ONLY`.

## 2. Les trois réalités à ne plus mélanger

### 2.1 Manuel historique V1
Le manuel du dépôt décrit correctement le lancement, la boucle AVDR, les domaines, les proposals et les frontières. Sa phrase « aucun fichier appliqué automatiquement, copie manuelle » est cependant antérieure au mode `--apply`.

### 2.2 CLI standalone actuel
Le CLI actuel accepte `--apply PROPOSAL_ID` et le wrapper PowerShell accepte `-Apply PROPOSAL_ID`. C’est aujourd’hui la voie utilisable pour appliquer un proposal existant.

### 2.3 Terminal global Obsidia
Le terminal global sait surtout observer, guider et lire des proposals. Il ne faut pas supposer qu’il remplace déjà le CLI standalone pour toute la construction du dépôt.

## 3. Carte des fichiers utiles

| Élément | Emplacement | Rôle |
|---|---|---|
| Agent principal | `periphery/agents/agent_obsidure.py` | Boucle AVDR, génération, proposals, apply |
| CLI Python | `scripts/obsidure_cli.py` | Entrée standalone et arguments |
| Wrapper PowerShell | `scripts/run_agent_obsidure.ps1` | Lancement Windows simplifié |
| Manuel historique | `docs/runtime/OBSIDIA_AGENT_OBSIDURE_MANUAL_V1.md` | Fonctionnement, commandes et frontières |
| Protocole d’apply | `docs/protocols/OBSIDURE_APPLY_PROTOCOL.md` | Ordre obligatoire des contrôles |
| Proposals | `_PATCH_PROPOSALS/<id>/` | `proposal.json` et `RECEIPT.md` |
| Sandbox | `_EPHEMERAL_CODE_SANDBOX_<timestamp>/` | Génération et stabilisation avant proposal |

## 4. Préflight obligatoire

Avant chaque objectif :

1. Se placer à la racine exacte du dépôt.
2. Lire `git status --short`.
3. Identifier les fichiers déjà dirty et ne pas les mélanger au proposal.
4. Définir un seul objectif, un seul périmètre et un seul résultat attendu.
5. Nommer les chemins autorisés lorsque tu les connais.
6. Définir les tests à exécuter.
7. Définir une condition STOP explicite.

Préflight recommandé :

```powershell
git status --short
git branch --show-current
git log -1 --oneline
python --version
Test-Path ".\scripts\run_agent_obsidure.ps1"
Test-Path ".\periphery\agents\agent_obsidure.py"
```

L’API sur `127.0.0.1:8000` est optionnelle : Obsidure peut basculer sur une analyse locale heuristique, mais la traduction OS_TRAD_REVERSE sera moins riche.

## 5. Modes d’utilisation

### 5.1 Mode interactif
```powershell
.\scripts\run_agent_obsidure.ps1
```
Commandes disponibles : `status`, `srl`, `domains`, `boundary`, `quit`.

### 5.2 Objectif direct
```powershell
.\scripts\run_agent_obsidure.ps1 -Objective "Créer le gate Bank P3-01" -Domain BANK
```

### 5.3 Audit seul
```powershell
.\scripts\run_agent_obsidure.ps1 -Objective "Analyser les connecteurs GPS" -Domain GPS -DryRun
```
Le dry-run ne crée ni sandbox ni proposal.

### 5.4 Limiter la boucle
```powershell
.\scripts\run_agent_obsidure.ps1 -Objective "Auditer les connecteurs Bank" -Domain BANK -MaxCycles 1
```

### 5.5 Mode silencieux
```powershell
.\scripts\run_agent_obsidure.ps1 -Objective "Créer gate Bank" -Domain BANK -Quiet
```

### 5.6 Appliquer un proposal
```powershell
.\scripts\run_agent_obsidure.ps1 -Apply <PROPOSAL_ID>
```
Équivalent Python : `python scripts\obsidure_cli.py --apply <PROPOSAL_ID>`.

### 5.7 Domaines acceptés par le CLI
`BANK`, `TRADING`, `GPS`, `ECOM`, `LEAN`, `SRL`. Si aucun domaine n’est fourni, Obsidure tente une détection automatique.

## 6. La boucle AVDR

1. **A — Audit** : lit l’objectif, traduit l’intention, identifie contraintes et risques, charge le contexte autorisé en lecture seule.
2. **V — Validation** : prépare les backups nécessaires et s’arrête en fail-closed si la protection échoue.
3. **D — Disruption** : génère dans une sandbox, teste et stabilise la proposition dans les limites du moteur.
4. **R — Réintégration** : produit un `proposal.json` et un `RECEIPT.md`, sans rendre le résultat souverain.

Important : une stabilisation technique ne signifie pas que le contenu est vrai, optimal ou prêt à intégrer. Le contrôle humain et les tests réels restent obligatoires.

## 7. Lire et juger un proposal

### 7.1 Ouvrir les deux fichiers
```powershell
$Id = "<PROPOSAL_ID>"
Get-Content "_PATCH_PROPOSALS\$Id\RECEIPT.md"
Get-Content "_PATCH_PROPOSALS\$Id\proposal.json"
```

### 7.2 Checklist de revue

- L’objectif reformulé correspond-il à ce que tu as demandé ?
- Tous les fichiers proposés sont-ils dans le scope autorisé ?
- Un chemin protégé, gelé ou lié à un autre chantier apparaît-il ?
- Les fichiers créés ont-ils un consommateur réel ou une destination explicite ?
- Les tests proposés prouvent-ils la relation recherchée ?
- Le proposal invente-t-il une route, un registre ou un fichier uniquement pour satisfaire un compteur ?
- La frontière `KX108_ONLY` reste-t-elle intacte ?
- Pour Lean : aucun `sorry`, `admit`, `unsafe` ou axiome non autorisé ?
- Le receipt signale-t-il un fallback trivial ou une capacité insuffisante ?

### 7.3 Signaux STOP

- fichier hors scope ;
- modification Kernel/X108, seal, Merkle, RFC3161 ou surface gelée sans mandat dédié ;
- remplacement d’un fichier dirty provenant d’un autre chantier ;
- tests absents ou uniquement documentaires ;
- fallback Lean trivial présenté comme preuve ;
- relation fondée seulement sur le nom du fichier ;
- proposition trop large pour être relue proprement.

## 8. Apply contrôlé

L’ordre obligatoire est : proposal → checks → approbation humaine du scope exact → apply → vérification → rapport.

```powershell
$Id = "<PROPOSAL_ID>"
.\scripts\run_agent_obsidure.ps1 -Apply $Id
```

Après l’apply, Obsidure peut annoncer des fichiers appliqués, ignorés ou en erreur. Cela ne remplace pas les contrôles Git et les tests. L’apply ne doit jamais être enchaîné automatiquement avec un commit ou un push.

## 9. Contrôles après apply

### 9.1 Contrôles génériques
```powershell
git diff --check
git diff --stat
git diff --name-only
git status --short
```

### 9.2 Vérifier le scope
```powershell
git diff -- <CHEMIN_1> <CHEMIN_2>
```
Aucun fichier hors scope ne doit apparaître. Si c’est le cas : STOP.

### 9.3 Tests Python
```powershell
python -m pytest <TESTS_CIBLES> -q
```
Toujours privilégier les tests ciblés du composant, puis la suite plus large pertinente.

### 9.4 Contrôles Lean

- lancer `lake build` dans le projet Lean concerné ;
- exiger `LEAN_EXIT=0` ;
- rechercher les tokens interdits ;
- vérifier qu’aucun manifest ou seal n’a été modifié indirectement.

Exemple de recherche :
```powershell
rg -n "\b(sorry|admit|unsafe)\b" proofs/lean
```

## 10. Commit et push

Obsidure prépare et applique. Le commit reste une opération séparée, après preuve des contrôles.

```powershell
$Files = @(
  "<CHEMIN_1>",
  "<CHEMIN_2>"
)

git diff --check
if ($LASTEXITCODE -ne 0) { throw "DIFF_CHECK_FAILED" }

python -m pytest <TESTS_CIBLES> -q
if ($LASTEXITCODE -ne 0) { throw "TESTS_FAILED" }

git status --short
git diff --stat

git add -- $Files
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "STAGED_DIFF_FAILED" }

git commit -m "<MESSAGE_INTENTIONNEL>"
if ($LASTEXITCODE -ne 0) { throw "COMMIT_FAILED" }

git push
```

Ne jamais faire `git add .` dans un dépôt contenant plusieurs chantiers ou des fichiers dirty préexistants.

## 11. Codes de sortie et pannes

| Code | Signification | Réaction |
|---:|---|---|
| 0 | Cycle ou apply terminé | Contrôler receipt, diff et tests |
| 1 | Import, proposal absent ou erreur d’entrée | Vérifier chemins, ID et environnement |
| 2 | Chemin protégé détecté | Ne pas contourner ; revoir le scope |
| 3 | Backup échoué, fail-closed | Ne rien appliquer ; corriger la cause |
| 4 | Erreur non anticipée | Conserver les logs, inspecter sans retry aveugle |

Pannes fréquentes :

- **API absente** : le mode offline peut continuer, mais la traduction d’intention est moins riche.
- **Proposal introuvable** : vérifier le dossier `_PATCH_PROPOSALS` et copier l’ID exact.
- **Dépôt dirty** : ne pas appliquer avant d’avoir distingué le chantier courant des modifications parallèles.
- **Lean indisponible ou en échec** : le résultat reste non officialisé ; aucun commit de preuve.
- **Proposal trop large** : le refaire en micro-lot plutôt que relire un bloc incontrôlable.

## 12. Rollback et récupération

Le CLI actuel ne présente pas de flag de rollback autonome. Le rollback reste une opération Git humaine et bornée.

### Avant commit
```powershell
git diff -- <CHEMINS_APPROUVES>
git restore -- <CHEMINS_APPROUVES>
```
À utiliser uniquement si ces fichiers ne contiennent pas d’autres modifications utiles non committées.

### Après commit
```powershell
git show --stat <COMMIT>
git revert <COMMIT>
```
Éviter `git reset --hard` comme réflexe : il peut détruire du travail parallèle.

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

## 14. Écrire un bon objectif

Un bon objectif Obsidure contient :

- le problème exact ;
- la famille ou le domaine ;
- les fichiers autorisés ;
- le résultat observable ;
- les tests ;
- les interdits ;
- la condition STOP.

### 14.1 Modèle audit seul
```text
Auditer <COMPOSANT/FAMILLE>.
Déterminer : source, propriétaire, loader/import/index, consommateur, tests, preuves et blockers.
Lecture seule. Aucun fichier créé. Aucun apply. STOP si la source canonique ou le consommateur n’est pas prouvé.
```

### 14.2 Modèle patch minimal
```text
Objectif : corriger <PROBLÈME EXACT>.
Scope autorisé : <LISTE DES FICHIERS>.
Résultat observable : <COMPORTEMENT ATTENDU>.
Tests : <TESTS CIBLES>.
Interdits : Kernel/X108, Sigma Core, manifests/seals, fichiers hors scope, commit, push.
STOP si un fichier supplémentaire est nécessaire ou si le consommateur réel n’est pas démontré.
```

### 14.3 Modèle Lean
```text
Créer un proposal Lean périphérique pour formaliser <INVARIANT STRUCTUREL>.
Le théorème doit porter uniquement sur <CONTRAT FORMEL>.
Exiger lake build PASS et zéro sorry/admit/unsafe.
Ne pas modifier la surface officialisée, le manifest ou les seals.
STOP si l’invariant nécessite une vérité sémantique du monde ou un axiome non autorisé.
```

### 14.4 Modèle campagne de branchement
```text
Ouvrir la famille <FAMILLE>.
1. Établir le census physique stable : PATH, SHA256, PRIMARY_OWNER, SECONDARY_RELATIONS, FILE_TYPE, ROLE, STATUS.
2. Séparer chemins primaires, relations secondaires, métadonnées et chevauchements.
3. Prouver pour chaque fichier : source/producteur → propriétaire → loader/import/index/manifeste → consommateur/destination → test/preuve.
4. Produire blockers explicites pour toute relation non résolue.
5. Aucun branchement avant stabilité du census.
6. Aucun claim FILE_EXISTS/INDEXED comme preuve de branchement.
7. Proposer un premier micro-lot de trois fichiers maximum.
STOP si la source canonique, le consommateur ou la frontière d’autorité reste ambigu.
```

## 15. Reprise actuelle de la campagne Obsidia

Dernier état sauvegardé dans le mail du 5 août 2026 :

- corpus : **4 353 items logiques** répartis en 14 familles ;
- baseline : **6 057 fichiers physiques** découverts ;
- `ARBRES_34` déjà traité ;
- `AGENTS` : 69 items logiques et 1 757 chemins physiques uniques comptabilisés ;
- 16 blockers fichiers et 3 blockers globaux persistés ;
- comptabilité primaire AGENTS terminée, mais fermeture totale non revendiquée ;
- prochaine famille autorisée : **MODULES — 36 items** ;
- reste : **4 250 items logiques dans 12 familles**.

Ordre de reprise :

1. MODULES — 36
2. CORTEX — 43
3. LOIS — 10
4. PÉPITES — 161
5. PROTOCOLES — 500
6. BALANCES — 500
7. CANON — 500
8. DOMAINES — 500
9. ROUTES_API — 500
10. BOUNDARIES — 500
11. MÉMOIRE_GRAPHITI — 500
12. PREUVES — 500

La dernière confirmation `LOCAL_HEAD = REMOTE_HEAD`, `DIVERGENCE = 0/0` et `WORKTREE_DIRTY = false` pour la clôture AGENTS n’apparaissait pas encore dans le mail inspecté. Elle doit donc être vérifiée avant reprise.

### Cycle obligatoire par famille

1. Ouvrir la famille et compter les items du ledger.
2. Construire le census physique stable.
3. Dédupliquer les chemins et documenter les chevauchements.
4. Découper en vagues fonctionnelles.
5. Prouver la relation de chaque fichier.
6. Créer un blocker explicite pour les relations non résolues.
7. Fermer localement avec un statut honnête.
8. Réconcilier les totaux.
9. Tester, diff/status, commit et push.
10. Produire un handoff pour la famille suivante.

## 16. Discipline de progression

- une seule famille ouverte ;
- un seul problème bloquant principal ;
- un seul lot de mutation à la fois ;
- trois fichiers maximum pour le premier lot ;
- dix lignes maximum pour le premier lot logique ;
- aucun nouvel audit global tant que la famille ouverte n’est pas réconciliée ;
- augmenter la taille seulement après deux lots réussis ;
- ne jamais compter « existe », « hashé » ou « indexé » comme « branché ».

## 17. Ce qu’il ne faut pas demander à Obsidure

- « Continue tout Obsidia » sans famille, scope ou gate.
- Modifier le Kernel, X108, les seals ou un freeze dans un lot ordinaire.
- Générer des centaines de fichiers pour faire correspondre un compteur.
- Appliquer plusieurs proposals non liés en une seule passe.
- Committer ou pousser sans revue du diff et des tests.
- Considérer un fallback Lean trivial comme une preuve.
- Confondre l’existence d’un fichier avec une relation runtime réelle.
- Confondre Obsidure standalone avec le terminal readonly ou Brody.

## 18. Fiche de session à remplir

```text
SESSION OBSIDURE
Date :
Branche :
HEAD initial :
Worktree propre : OUI / NON

Objectif :
Famille / domaine :
Scope autorisé :
Fichiers protégés / hors scope :
Résultat observable :
Tests requis :
Condition STOP :

DRY-RUN
Intent :
Risk flags :
Verdict : CONTINUER / REFORMULER / BLOQUER

PROPOSAL
Proposal ID :
Receipt lu : OUI / NON
proposal.json lu : OUI / NON
Scope exact validé : OUI / NON

APPLY
Apply lancé : OUI / NON
Fichiers appliqués :
Fichiers ignorés :
Erreurs :

VALIDATION
Tests ciblés :
Lean exit :
Forbidden tokens :
git diff --check :
Fichiers hors scope :
git status :

GIT
Commit :
Push :
Remote divergence :
Handoff suivant :
```

## 19. Sources consolidées

### Dépôt GitHub

- `docs/runtime/OBSIDIA_AGENT_OBSIDURE_MANUAL_V1.md`
- `docs/protocols/OBSIDURE_APPLY_PROTOCOL.md`
- `scripts/obsidure_cli.py`
- `scripts/run_agent_obsidure.ps1`
- `periphery/agents/agent_obsidure.py`

### Google Drive

- Document `obsidia suite 29.07`, contenant la carte du pack Obsidure et les références du manuel/protocole.

### Gmail — mails envoyés à soi-même

- 1er juillet 2026 — diagnostic Obsidure, capacités Lean et sources de contexte.
- 1er–2 juillet 2026 — doctrine opérateur, build protocols, apply, vérification et frontières.
- 7 juillet 2026 — proposal reader dans le terminal, sans apply automatique depuis le cockpit.
- 30 juillet 2026 — plan maître de branchement des 4 353 éléments.
- 3 août 2026 — plan complet de fermeture des 6 057 fichiers.
- 5 août 2026 — état de reprise avec Obsidure : AGENTS, 4 250 items restants et prochaine famille MODULES.

## Commandes condensées

```powershell
# Interactif
.\scripts\run_agent_obsidure.ps1

# Audit
.\scripts\run_agent_obsidure.ps1 -Objective "<OBJECTIF>" -Domain <DOMAINE> -DryRun

# Proposal
.\scripts\run_agent_obsidure.ps1 -Objective "<OBJECTIF>" -Domain <DOMAINE> -MaxCycles 1

# Revue
Get-Content "_PATCH_PROPOSALS\<ID>\RECEIPT.md"
Get-Content "_PATCH_PROPOSALS\<ID>\proposal.json"

# Apply
.\scripts\run_agent_obsidure.ps1 -Apply <ID>

# Validation
git diff --check
git diff --stat
git status --short
python -m pytest <TESTS> -q

# Rollback non committé, chemins précis uniquement
git restore -- <CHEMINS>

# Rollback après commit
git revert <COMMIT>
```

**Phrase de verrou :** Obsidure peut construire, stabiliser, proposer et appliquer un scope approuvé. Il ne transforme jamais seul un proposal en vérité canonique. La preuve vient des tests, du diff, de la frontière d’autorité et de la validation humaine.