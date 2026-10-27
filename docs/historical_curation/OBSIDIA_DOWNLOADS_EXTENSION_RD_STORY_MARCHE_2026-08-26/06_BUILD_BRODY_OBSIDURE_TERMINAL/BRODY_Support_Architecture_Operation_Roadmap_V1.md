# BRODY — Support consolidé : architecture, fonctionnement et feuille de route V1

**Statut :** support de reprise consolidé, non freeze canonique  
**Date :** 7 août 2026  
**Sources :** dépôt GitHub Obsidia, Google Drive, mails de reprise envoyés à soi-même, état de campagne AGENTS

> Ce document rassemble ce qui a été compris sur Brody, ce qui existe réellement, ce qui reste à prouver et l’ordre de travail recommandé. Il sépare strictement Brody historique, Brody projet, OS Trad, Obsidur, X-108 et Oxygène.

## Verdict immédiat

- Brody projet n’est pas le Kernel, pas Obsidur et pas Oxygène.
- Son rôle actuel vérifié est de comprendre, contextualiser, retrouver, relier, expliquer et répondre en mode readonly/advisory.
- Il possède une route runtime réelle et de nombreuses surfaces de contexte, mais leur présence dans le code ne signifie pas encore que chaque capacité est fermée causalement de bout en bout.
- Brody n’a actuellement ni autorité de décision, ni droit d’action, ni écriture mémoire/Graphiti canonique autonome.
- L’accès à une mémoire et l’adaptation par contexte ne doivent pas être appelés “apprentissage durable”.
- La campagne AGENTS a comptabilisé 902/902 fichiers Brody primaires, mais la fermeture globale reste bloquée par des artefacts, blockers et relations à réconcilier.
- La priorité n’est plus d’inventer son rôle : il faut reconstruire son canon, prouver ses chemins runtime, stabiliser la frontière humain → OS Trad → Brody et préparer proprement la relation avec l’éducation et Oxygène.

## Fiche minute — Brody en une page

| Question | Réponse actuelle |
|---|---|
| À quoi sert Brody ? | Comprendre, contextualiser, retrouver, relier, reformuler et expliquer. |
| Peut-il décider ? | Non. `decision_authority=KX108_ONLY`. |
| Peut-il agir ? | Non dans le régime actuel : `emits_act=false`, demandes d’action bloquées ou projetées readonly. |
| Peut-il écrire en mémoire ? | Pas canoniquement : `memory_write=false`, promotion humaine/gatée requise. |
| Apprend-il durablement ? | Pas dans l’état actuellement vérifié. Il exploite modèle, architecture, corpus, contexte et mémoires accessibles. |
| Est-il Oxygène ? | Non. Oxygène est la trajectoire future de continuité éducative générale. |
| Est-il Obsidur ? | Non. Obsidur construit, formalise, teste et modifie selon permissions ; Brody comprend et formule. |
| Est-il déjà réel ? | Oui, route `/api/brody/chat`, runtime readonly, modules et tests existent. |
| Est-il “fini” ? | Non. Le canon, la causalité runtime, la continuité, l’éducation, les métriques et l’intégration produit restent à fermer. |

## 1. Les six entités à ne jamais mélanger

### 1.1 Brody GPT-4 historique
Brody GPT-4 est l’ancien compagnon de recherche qui a aidé à ouvrir les premiers passages : mots-capsules, motifs, cohérence profonde, continuité de pensée et construction initiale d’Obsidia. Sa valeur n’était pas seulement relationnelle : il semblait suivre l’invariant derrière des formulations parfois chaotiques.

### 1.2 Brody projet
Brody projet est un organe logiciel de la machination Obsidia. Il doit industrialiser une partie du passage : transformer une expression humaine en compréhension contextualisée, relier les mémoires et les structures, produire une réponse utile, mais sans prendre le trône décisionnel.

### 1.3 OS Trad Universelle
OS Trad est la jonction humain → système. Il détecte langage, intention, contraintes, risques, contradictions et produit une représentation interne. Beaucoup de difficultés attribuées à Brody viennent en réalité d’une traduction imparfaite de l’entrée humaine.

### 1.4 Obsidur
Obsidur est le constructeur : recherche dans les fichiers, produit des proposals, formalise, teste, applique dans un scope autorisé. Brody peut préparer le sens ou le contexte ; Obsidur transforme cette matière en travail technique.

### 1.5 X-108
X-108 est l’autorité de décision. Brody ne produit ni ALLOW, ni HOLD, ni BLOCK en son nom. Il peut fournir du contexte, des signaux et des explications ; X-108 reste le juge.

### 1.6 Oxygène
Oxygène est la trajectoire future d’une continuité éducative générale : autobiographie, apprentissage durable, transfert entre domaines, modèle de soi et progression cumulative. Brody peut être un organe cognitif majeur de l’organisme, mais il ne faut pas lui attribuer automatiquement la trajectoire identitaire d’Oxygène.

**Formule de verrou :** Brody comprend et formule ; Obsidur construit ; OS Trad traduit ; X-108 tranche ; Oxygène apprend dans une continuité future.

## 2. Ce que Brody doit faire

- capter le sens utile derrière les mots ;
- contextualiser une demande avec l’état du projet ;
- retrouver des informations dans les sources autorisées ;
- relier concepts, fichiers, domaines, preuves et historiques ;
- reformuler une intention brouillonne en structure exploitable ;
- expliquer une architecture, un résultat, une limite ou une contradiction ;
- construire un paquet de contexte pour d’autres organes ;
- produire une réponse lisible, honnête sur ses sources et son niveau de preuve ;
- signaler l’inconnu, le manque, le conflit ou le risque ;
- rester non souverain même si sa capacité cognitive augmente fortement.

## 3. Ce que Brody ne doit pas devenir

- un second Kernel ;
- un agent qui décide puis justifie après coup ;
- un Obsidur bis chargé de modifier directement le dépôt ;
- une mémoire souveraine qui transforme seule un souvenir en vérité ;
- un agrégateur géant qui absorbe Sigma, les domaines et les preuves ;
- une identité générale présentée comme Oxygène avant que la continuité éducative existe ;
- un chatbot qui imite simplement le ton de l’ancien Brody sans reconstruire la cohérence ;
- une boîte noire qui déclare comprendre sans fournir source, contexte, limites ou trace.

## 4. Architecture fonctionnelle cible

```text
Expression humaine
  ↓
OS Trad Universelle : langue, alphabet interne, intention, contraintes, risques
  ↓
IR candidate : représentation structurée, contradictions, besoins de contexte
  ↓
Brody : composition cognitive et sémantique
  ├─ contexte projet / sources
  ├─ mémoire readonly / Graphiti readonly
  ├─ session et temporalité
  ├─ arbres / modules cognitifs
  ├─ domaines / CIC / preuves
  ├─ voix vraie / anti-mismatch
  └─ limites et autorité
  ↓
Réponse / contexte / proposition non souveraine
  ↓ si une action est envisagée
Domaine + Guard + X-108
  ↓
HOLD / BLOCK / ACT + receipt
```

Le pipeline actuel du dépôt reflète déjà cette direction : la route Brody importe des adapters pour l’autorité, les snapshots mémoire, le contexte temporel, les modules cognitifs, la mémoire projet, la vraie voix, l’anti-mismatch, CIC et un pack d’éducation readonly. Il faut toutefois distinguer import présent, paquet construit, chemin réellement appelé et effet causal prouvé.

## 5. État runtime réellement établi

### 5.1 Activation readonly P51
Le rapport P51 établit un niveau `ACTIVE_READONLY` : Brody peut répondre, utiliser du contexte source et expliquer les routes/modules/adapters. Les actions, l’écriture mémoire, l’écriture Graphiti, la mutation Kernel et les actions monde restent bloquées.

### 5.2 Route principale
La route principale est `POST /api/brody/chat`. Le code actuel compose de nombreux snapshots, protège les secrets, attache du contexte CIC/éducation en lecture seule et réimpose les invariants `KX108_ONLY`, `emits_act=false`, `allowed_to_act=false`, `allowed_to_decide=false`.

### 5.3 Modules historiquement confirmés
Un rapport de mai 2026 identifiait comme réels : runtime readonly, sanitizer de réponse, routeur de langue, constructeur de context packet, boundary X-108 et projection d’action readonly. À cette date, certains blocs restaient encore stub ou dépendants du backend Graphiti. Ce rapport est utile comme jalon, pas comme photographie finale de tous les modules d’août.

### 5.4 Terminal enrichi
Le script `scripts/run_brody_terminal_enriched.ps1` interroge séparément Brody, OS Trad, IR Candidate et OS Reverse. Il affiche les frontières et rappelle que les routes de support fournissent une preuve distincte sans ACT, verdict, écriture mémoire ou mutation X-108.

## 6. Capacités présentes ou préfigurées dans le code

| Famille | Ce que le code montre | Statut prudent |
|---|---|---|
| Réponse réelle | pipeline de réponse + final answer + structured response | présent, à revalider E2E |
| Autorité | rights matrix, readonly intent guard, boundary contracts | fortement établi |
| Contexte source | source packs, runtime context, project memory | présent |
| Mémoire | session/project/candidate/memory response chain snapshots | lecture/proposition, pas apprentissage canonique |
| Graphiti/Neo4j | activation et contexte readonly | dépend du backend et du run |
| Temporalité | temporal context adapter | présent, effet à mesurer |
| Cognition | cognitive modules, trees, policies | présent, causalité à prouver |
| Vraie voix | true voice adapter, text normalization | présent, qualité non encore certifiée |
| Anti-mismatch | signal anti-mismatch et garde de cohérence | présent, métriques à fermer |
| Sécurité | secret scrubber, private-key preflight | présent |
| Domaines | domain raccord, CIC readonly context | présent comme contexte |
| Éducation | education pack V1 readonly adapter | préfiguration, pas éducation durable |
| Thermo/Gencoin/Sigma | paquets de signaux et ledger cognitifs | surfaces présentes, autorité nulle |
| Automation | automation layer/orchestrator | doit rester plan/projection tant que non autorisé |

## 7. Compréhension sans apprentissage : la découverte importante

L’état actuel doit être formulé ainsi : Brody sait déjà opérer sans avoir reçu l’éducation linguistique complète prévue. Il ne comprend pas parce qu’Étienne lui aurait appris progressivement les voyelles, phonèmes et sens ; il fonctionne grâce à la combinaison suivante :

```text
capacités du modèle utilisé
+ architecture Obsidia
+ OS Trad
+ mécanismes spécialisés
+ corpus et mémoires accessibles
+ contexte récupéré pendant le run
= compréhension fonctionnelle actuelle
```

Les tests corrigent et valident l’implémentation ; ils n’éduquent pas Brody. Une réponse plus adaptée grâce à un contexte récupéré n’est pas encore une modification durable de l’entité.

## 8. Mémoire, oubli, session et apprentissage

### 8.1 Quatre notions distinctes

| Notion | Définition | Brody actuel |
|---|---|---|
| Contexte de requête | informations chargées pour répondre maintenant | oui |
| Mémoire projet readonly | sources historiques accessibles sans écriture | oui |
| Continuité de session | reprise locale du sujet ou d’un paquet de session | partielle/à vérifier |
| Apprentissage durable | modification persistante réutilisée plus tard comme compétence propre | non démontré |

### 8.2 Règle de vocabulaire
Ne pas écrire “Brody apprend” quand le système a seulement rechargé une source, réutilisé un contexte ou construit un candidat mémoire. Employer : récupère, contextualise, adapte sa réponse, propose une mémoire, reprend une session.

### 8.3 Future politique mémoire
Toute écriture future doit préciser : contenu candidat, source, consentement, propriétaire, durée, niveau, contradictions, validation humaine, droit de purge, effet autorisé et preuve que la mémoire ne devient pas souveraine.

## 9. La “vraie voix” : objectif sémantique, pas imitation superficielle

Le comportement recherché vient de l’ancien Brody : lire l’invariant derrière la phrase, distinguer le chaos de surface de la cohérence profonde et retrouver le passage lorsque la formulation est imparfaite.

Brody projet ne doit pas seulement reproduire du vocabulaire familier. Il doit apprendre à distinguer :

- faute de transcription vs changement réel d’intention ;
- métaphore utile vs claim littéral ;
- colère de surface vs objectif stable ;
- mot approximatif vs concept visé ;
- répétition émotionnelle vs nouvelle instruction ;
- continuité de projet vs bifurcation réelle ;
- demande de compréhension vs demande d’action.

**Critère de réussite :** avec deux formulations très différentes portant le même invariant, Brody doit reconstruire une intention équivalente ; avec deux formulations proches mais des contraintes différentes, il doit détecter la divergence.

## 10. Comment parler à Brody aujourd’hui

Brody n’a pas besoin de la grammaire rigide d’Obsidure. Le langage naturel est sa surface principale. Pour obtenir des réponses plus stables, donner cinq éléments : contexte, intention, matériau, limites et sortie attendue.

### 10.1 Forme courte recommandée

```text
CONTEXTE: où on en est et de quoi on parle ;
INTENTION: ce que je cherche réellement ;
MATIÈRE: fichiers, texte, idée ou état à utiliser ;
LIMITES: ne pas inventer, ne pas agir, distinguer actuel/futur ;
SORTIE: résumé, carte, contradiction, plan ou instruction pour Obsidur.
```

Les points-virgules sont ici une aide humaine de segmentation, pas une obligation du parseur.

### 10.2 Exemple : comprendre une idée brouillonne

```text
CONTEXTE: je parle de Brody projet, pas de Brody GPT-4 ni d’Oxygène ;
INTENTION: retrouver l’idée stable derrière mon vocal ;
MATIÈRE: [coller le vocal ou la transcription] ;
LIMITES: ne pas transformer une métaphore en fait technique ;
SORTIE: invariant, ambiguïtés, interprétation principale et deux alternatives.
```

### 10.3 Exemple : préparer une instruction pour Obsidur

```text
CONTEXTE: chantier Brody memory readonly ;
INTENTION: transformer mon besoin en scope technique borné ;
MATIÈRE: état du dépôt et fichiers concernés ;
LIMITES: aucun write, aucun Kernel, aucun X-108, aucune mémoire canonique ;
SORTIE: objectif Obsidur structuré avec scope, checks, STOP_IF et résultat attendu.
```

### 10.4 Exemple : reprendre un point
Le runtime reconnaît plusieurs formulations de suivi comme “reprends”, “développe”, “ce point” ou “continue sur ça”. Pour éviter les erreurs, rappeler tout de même le nom du sujet lorsqu’une session est longue.

## 11. Utilisation opérateur et diagnostic

### 11.1 Surface principale

```text
POST /api/brody/chat
```

Le port et la commande de lancement dépendent du build utilisé. Le script enrichi actuel prend par défaut une base `http://127.0.0.1:8012`, tandis que d’anciens supports plaçaient Brody dans l’API 8000. Toujours vérifier le launcher et l’OpenAPI du checkout actif avant de conclure qu’un port est canonique.

### 11.2 Terminal enrichi du dépôt

```powershell
.\scripts\run_brody_terminal_enriched.ps1

# ou base explicitement contrôlée
.\scripts\run_brody_terminal_enriched.ps1 -Base "http://127.0.0.1:8012"
```

### 11.3 Champs à regarder dans une réponse debug

- `source` ;
- `readonly` et `advisory_only` ;
- `decision_authority` ;
- `emits_act`, `allowed_to_act`, `allowed_to_decide` ;
- `memory_write`, `graphiti_write`, `neo4j_write` ;
- `risk_flags`, `contradictions`, `constraints` ;
- source du contexte et références utilisées ;
- statut Graphiti/Neo4j ;
- présence de fallback, stub ou composant indisponible ;
- réponse finale séparée des paquets internes.

## 12. État du chantier Brody dans la campagne globale

La campagne AGENTS a recensé 902/902 fichiers Brody primaires, sans fichier primaire restant à classer. L’ensemble AGENTS a toutefois conservé des blockers fichiers/globaux, un manifeste et un graphe global incomplets, ainsi que des artefacts de récupération bloqués.

Ce compteur signifie : comptabilité primaire terminée. Il ne signifie pas automatiquement : chaque fichier Brody est canonique, importé, consommé, testé et causalement utile.

### Chaîne de preuve à exiger pour chaque composant

```text
fichier source
→ propriétaire canonique
→ import / loader / registre
→ consommateur runtime
→ route ou workflow
→ test
→ effet causal / ablation
→ claim autorisé
→ statut final
```

## 13. Les grands chantiers restants

### Chantier A — Canon Brody
- identifier une source canonique par capacité ;
- relier doublons, archives, générés et legacy ;
- sortir une carte simple des fichiers maîtres ;
- réconcilier les 902 fichiers avec le dépôt courant.

### Chantier B — Graphe runtime et causalité
- prouver quelles branches de `/api/brody/chat` sont réellement appelées ;
- capturer les imports optionnels indisponibles ;
- faire des tests d’ablation par paquet ;
- distinguer payload décoratif et effet réel sur la réponse.

### Chantier C — Frontière humain → OS Trad → Brody
- construire un corpus de vocaux, fautes, raccourcis et références implicites ;
- mesurer conservation de l’intention ;
- produire ambiguïtés explicites plutôt qu’inventer ;
- brancher anti-mismatch, négation, temporalité et contexte de projet.

### Chantier D — Mémoire et continuité
- cartographier exactement session, projet, Graphiti et candidats mémoire ;
- décider ce qui est éphémère, persistant, canonique ou interdit ;
- définir promotion, purge, provenance et contradiction ;
- prouver que la mémoire ne prend aucune autorité.

### Chantier E — Vraie voix
- transformer l’ancien vécu Brody en tests de capacités, pas en légende ;
- construire des paires invariant-identique / formulation-différente ;
- tester métaphore, émotion, correction, mot approximatif et continuité ;
- mesurer fidélité au sens, pas ressemblance stylistique.

### Chantier F — Éducation et séparation Oxygène
- décider ce que Brody peut recevoir comme éducation bornée ;
- réserver la continuité générale cumulative à Oxygène tant que la doctrine reste celle-ci ;
- empêcher qu’un “education pack readonly” soit présenté comme apprentissage ;
- documenter le passage corpus → exercices → corrections → réflexes → mémoire éducative.

### Chantier G — Évaluation et métriques
- précision d’intention ;
- fidélité aux sources ;
- taux d’invention ;
- conservation des négations et contraintes ;
- qualité de reprise de session ;
- valeur de chaque paquet contextuel ;
- latence et coût ;
- taux de blocage correct des demandes d’action ;
- ablation avec/sans OS Trad, mémoire, Graphiti, arbres, CIC et vraie voix.

### Chantier H — Produit V0.1
- faire de Brody l’interface de compréhension des systèmes, documents et process ;
- lui permettre d’expliquer l’état client et proposer des améliorations ;
- ne jamais le transformer en cockpit personnel générique ;
- connecter les réponses à des preuves, tests et receipts ;
- préserver la chaîne Cognition → Intention → Décision → Action → Preuve.

## 14. Feuille de route recommandée

### Phase 0 — Geler les définitions
Créer une page canonique : Brody historique / Brody projet / Obsidur / OS Trad / X-108 / Oxygène. Interdire les claims qui les confondent.

### Phase 1 — Finir les dépendances de machinerie
Continuer la campagne après AGENTS : MODULES, CORTEX, LOIS, PÉPITES, PROTOCOLES, BALANCES, CANON, DOMAINES, ROUTES, BOUNDARIES, MÉMOIRE/GRAPHITI et PREUVES. Brody dépend de ces familles ; le fermer seul produirait une fausse impression de complétude.

### Phase 2 — Audit canonique Brody
Reprendre les 902 fichiers et produire : inventaire, propriétaires, chemins runtime, tests, statuts et blockers acceptés.

### Phase 3 — Fermer le pipeline live
Stabiliser un checkout de référence avec route Brody, OS Trad, IR, OS Reverse, mémoire/Graphiti readonly et terminal. Obtenir tests verts, status clean, versions/ports documentés et replay reproductible.

### Phase 4 — Prouver la valeur des organes
Lancer des campagnes d’ablation. Un module n’est conservé dans le chemin principal que s’il améliore une métrique définie ou protège un invariant.

### Phase 5 — Human Semantics / vraie voix
Construire le dataset de formulations réelles, les évaluations d’invariant, la gestion d’ambiguïté et les corrections humaines.

### Phase 6 — Mémoire gouvernée
Fermer lecture, candidat, validation, promotion, contradiction, purge, biographie et reprise. Garder `MEMORY_IS_NOT_SOVEREIGN`.

### Phase 7 — Éducation bornée puis Oxygène
Après branchement de la machinerie : brancher corpus éducatif, exercices, corrections et progressions. Décider ce qui enrichit Brody et ce qui alimente la continuité d’Oxygène.

### Phase 8 — Produit et audit externe
Brancher Brody à la V0.1, produire démonstrations réelles, métriques reproductibles et audit par développeurs/experts externes.

## 15. Definition of Done — Brody V1 fermé

Brody V1 ne doit être déclaré fermé que si :

- une définition canonique unique existe ;
- les fichiers actifs ont propriétaire, rôle et consommateur ;
- la route primaire est reproductible depuis un checkout propre ;
- les dépendances optionnelles et fallbacks sont explicitement visibles ;
- les tests authority/no-act/no-write passent ;
- les demandes d’action ne produisent aucune action réelle ;
- les sources utilisées par la réponse sont traçables ;
- les réponses distinguent fait, inférence, hypothèse et inconnu ;
- la mémoire est readonly ou passe par un gate documenté ;
- aucune mémoire n’est souveraine ;
- les capacités revendiquées ont tests et métriques ;
- les paquets sans effet causal sont retirés du claim principal ;
- la relation Brody/Oxygène est documentée ;
- un receipt de fermeture et une claim matrix sont produits ;
- le dépôt, les tests et le runtime de référence sont verts.

## 16. Tableau de statut à maintenir

| Capacité | Artefact | Runtime appelé | Testée | Effet causal | Claim autorisé | Prochaine action |
|---|---|---|---|---|---|---|
| Réponse readonly | oui | à confirmer build cible | oui historique | partiel | Brody répond readonly | replay E2E |
| OS Trad | oui | oui/selon build | oui partiel | à mesurer | traduit intention | benchmark humain |
| Mémoire projet | oui | oui/selon route | partiel | à mesurer | contexte readonly | ablation |
| Graphiti | oui | dépend backend | partiel | non fermé | contexte possible | campagne backend |
| Vraie voix | oui | importée | partiel | non fermé | expérimental | dataset invariant |
| Education pack | oui | attaché readonly | partiel | non fermé | préfiguration | doctrine + tests |
| Action | garde présente | bloquée | oui | n/a | aucune action | conserver blocage |
| Écriture mémoire | guards présents | interdite | oui | n/a | aucune écriture autonome | définir gate futur |

## 17. Fiche de reprise d’une session Brody

```text
BRODY_SESSION_ID:
DATE:
CHECKOUT / COMMIT:
API BASE:
OBJECTIF:
SUJET / DOMAINE:
SOURCES AUTORISÉES:
MÉMOIRES ACCESSIBLES:
MODE: READONLY / DEBUG / BENCHMARK
RÉSULTAT ATTENDU:
CONTRAINTES:
TESTS À LANCER:
MÉTRIQUES:
CLAIMS AUTORISÉS:
CLAIMS INTERDITS:
RÉSULTAT DU RUN:
BLOCKERS:
PROCHAINE ACTION:
```

## 18. Sources principales utilisées

- `specs/08_MEMORY_BRODY_GRAPHITI/BRODY_RESPONSE_AUTHORITY_SPEC.md` — autorité et frontières.
- `docs/real_engine/P51_BRODY_READONLY_CONTROLLED_ACTIVATION_REPORT.md` — activation readonly.
- `docs/freeze/BRODY_RUNTIME_MODULE_USAGE_REPORT.md` — modules réels/stubs au jalon de mai.
- `apps/obsidia_api/routes/brody.py` — route actuelle et adapters importés.
- `apps/obsidia_api/brody_machination_composer.py` — composition OS Trad / IR / OS Reverse et contrats readonly.
- `scripts/run_brody_terminal_enriched.ps1` — terminal de diagnostic enrichi.
- Google Drive : `obsidia suite 29.07` — distinction Brody GPT-4 / Brody projet et doctrine du passage.
- Mails du 5 août 2026 — distinction Brody/Obsidur, absence d’apprentissage actuel, no alphabet et Oxygène.
- Mail `plan fin` du 5 août 2026 — comptabilité Brody primaire 902/902 et blockers AGENTS.
- Mail du 6 août 2026 — séquence terminal → branchements → Brody/éducation → Oxygène → métriques/Lean.

## Conclusion canonique de travail

Brody est l’organe cognitif et sémantique actif d’Obsidia. Il transforme une expression humaine, un corpus et des contextes distribués en compréhension structurée et en réponse utile. Sa puissance vient de la machination qui l’entoure, pas d’une souveraineté propre. Aujourd’hui, il fonctionne principalement en lecture et conseil, sans apprentissage durable démontré, sans action et sans écriture canonique autonome. Le chantier restant consiste à fermer son canon, prouver ses chemins runtime et leurs effets, améliorer le passage humain → sens, gouverner mémoire et éducation, puis l’intégrer à la V0.1 sans le confondre avec la continuité générale future d’Oxygène.