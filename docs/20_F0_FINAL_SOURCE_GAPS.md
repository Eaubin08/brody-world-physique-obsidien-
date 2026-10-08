# 20 — F0 : vérification C10, UNKNOWN et trois filiations ouvertes

**Date 2026-10-08 · AUDIT DOCUMENTAIRE / NON-FREEZE**. Cette passe réconcilie la provenance des sources et leurs frontières, **sans test runtime ni merge vers main**.

## #93 — C10, collision historiquement attestée

**Source 1 :** [Bloc 11 — Trace et Immuabilité (C10)](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/OBSIDIA_V4_STRUCTURED_FULL/02_BLOCS_17/Bloc_11__Trace_et_Immuabilite_C10.md). Le fichier expose cryptographie, Merkle Tree, auditabilité, et six pépites P13–P18 (Merkle, traduction humain↔machine, immuabilité forte, rupture data/sens, log d'audit, sémantique avant calcul).

**Source 2 :** [Éducation / Oxygen](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/EDUCATION.md). Le même identifiant `C10` renvoie ici à une future phase massive d'éducation **non encore lancée**.

**Verdict `NAME_COLLISION_SOURCES_VERIFIED` :** les deux passages primaires documentaires sont localisés et incompatibles comme dénomination unique. Le statut « pépite ancrée » attribué par un ancien pack n'est pas une vérification indépendante des théorèmes qu'il évoque. Aucune déduction de runtime.

## #47 — UNKNOWN, source contractuelle exacte

- [`WorldObservationV0` et `WorldStateV0`](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/mmonde/contracts_v0.py) : `causal_status="UNKNOWN"`, `unknowns`, candidature de réalité en lecture seule.
- [F15 Physical Evidence Plane](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/docs/architecture/PHYSICAL_EVIDENCE_PLANE_V0.md) : causalité et transformations de repères/unités non prouvées = `UNKNOWN`.

**Définition :** état épistémique de non-établissement, **pas** une décision kernel au même niveau que `ACT/HOLD/BLOCK`, pas une preuve d'erreur et pas une autorisation d'agir. **Verdict `UPSTREAM_CODE_READ`**, code inspecté, tests non relancés.

## #31 — VisualFingerprint : la filiation reste hypothétique

Sources : [invariants visuels ρ, invariant dynamique, Analyse↔Synthèse](https://docs.google.com/document/d/1ZwONI-YnrpHgMQW_iQiIlx4gaI57IEgfUOa8By6iMDU/edit) ; [Shazam Cognitif / matrice 34 Arbres](https://docs.google.com/document/d/1KshgP97PKdTZAfRxe9-YfcVnIJceKbgGCyxC-HdRj18/edit) ; [F16 vision actuelle](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/vision/contracts_v0.py).

L'idée commune est la **reconnaissance de continuité et d'invariants sous transformation**, mais Shazam extrait des caractéristiques de style/texte/rythme tandis que VisualFingerprint propose une signature visuelle d'objets/géométrie. On ne dispose ni d'une équivalence d'algorithmes démontrée, ni de tests de ré-identification, ni d'une preuve de connexion du moteur visuel.

**Propos utilisateur datés du 25 juillet 2026 (contexte conversationnel, pas verbatim exporté) :** volonté d'éduquer Brody sur images du réel, contexte physique, apprentissage humain inversé et Shazam Cognitif. La formulation exacte et son antériorité éventuelle restent à reconstituer. **Verdict `DESCENDANT_HYPOTHESIS`**, pas une invention externe revendiquée comme personnelle.

## #57 — Dreaming : atelier simulé, pas expérience réellement vécue

- [Architecture Shadow / sécurité cinématique](https://docs.google.com/document/d/1iVwqEeo2TTa3Mv6wYFdJOq_8-mAfFpz7-AJ46iMxm7o/edit) : projection d'actions hypothétiques sans action réelle.
- [Archive de World Foundry / simulations et curriculum](https://docs.google.com/document/d/1d5Gf5-r1d43wetqaANCzCff5CPyYckwTw9_AuWwicpg/edit) : WorldSpec, Curriculum Forge, tests sur variantes et récits de recherches externes.
- [Contrats F0 des projections](https://github.com/Eaubin08/brody-world-physique-obsidien-/blob/f0/learning-loop-contracts-v0/brody_world_physique/contracts_v0.py) : `PREDICTED/SIMULATED/COUNTERFACTUAL` sont des représentations candidates.

Le rapprochement entre école virtuelle gouvernée et apprentissage par simulation est un **design Obsidia** qui réemploie des méthodes de world modeling existantes, pas une découverte exclusive du dreaming. Les simulations ne sont ni une preuve physique ni un souvenir réel et ne produisent aucun ACT autonome. **Verdict `DESCENDANT_HYPOTHESIS / FUTURE`.**

## #59 — Quadrillage du monde : provenance de la vision précisée

**Contexte utilisateur reconstitué** : conversation du **8 octobre 2026 vers 02:37 UTC**, idée de quadriller le monde par classification, mémoire, historique, espace/temps, géométrie et relations ; vers 02:38 UTC, analogie de l'enfant capable d'apprendre objet/chute/trajectoire/conséquence avant de connaître une définition formelle de la gravité.

Ce sont des **paraphrases contextuelles** de messages attribués à l'utilisateur, **pas des citations verbatim signées ni des archives exportées**. Ne pas afficher dans un dépôt public l'intégralité d'une conversation privée.

Descendants fonctionnellement compatibles :
- [MMonde](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/mmonde/contracts_v0.py) — état, observations, temps, espace, relations, provenance et incertitude ;
- [F12 world dynamics](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/world_dynamics/contracts_v0.py) — transitions, trajectoires, repères et continuité ;
- [F15 evidence](https://github.com/Eaubin08/obsidia-x108-proofs/blob/5b9b72452cff7a560db992e57a43fc700dacd923/periphery/physical_evidence/contracts_v0.py) — compatibilité et provenance ;
- [Brody World Physique F0](https://github.com/Eaubin08/brody-world-physique-obsidien-/blob/f0/learning-loop-contracts-v0/brody_world_physique/contracts_v0.py) — projection, delta et expérience candidate.

**Verdict :** l'intention attribuable à l'utilisateur et l'alignement conceptuel sont mieux établis ; la **filiation historique causale**, les dates de naissance exactes et l'identité d'un hypothétique « algorithme du quadrillage » ne le sont pas. Le statut reste `DESCENDANT_HYPOTHESIS` pour la généalogie et `UPSTREAM_CODE_READ` pour les primitives présentes.

## Étiquetage des auteurs et limitation de preuve

Pour chaque innovation revendiquée, différencier :
1. `USER_IDEA_WITH_PRIMARY_UTTERANCE` : direction explicite de l'utilisateur, archive primaire identifiée ;
2. `AI_ASSISTED_FORMALIZATION` : rédaction, algorithme ou illustration proposée par assistant ;
3. `EXTERNAL_DONOR` : projet scientifique/open source attribué à ses auteurs ;
4. `CODE_PRESENT/TEST_SOURCE_READ/RUNTIME_CONFIRMED` : trois niveaux différents à ne pas fusionner ;
5. `CONVERSATION_CONTEXT_UNEXPORTED` : témoignage contextuel non citable sous forme de document public exact.

Quand les rôles sont mêlés ou non vérifiables : `AUTHORSHIP_UNRESOLVED`. Une idée utile et une preuve de nouveauté au sens de recherche scientifique ou brevet sont deux évaluations différentes.

## Verdict de cette passe

- `#93 C10` et `#47 UNKNOWN` : **sources directes retrouvées, ambiguïtés principales résolues**.
- `#31 VisualFingerprint`, `#57 Dreaming`, `#59 Quadrillage` : **hypothèses de filiation explicites maintenues**, et non falsifiées comme des équivalences complètes.
- `F0_CONCEPT_SOURCE_TRIAGE = COMPLETE FOR KNOWN FLAGS` **mais** `F0_DOCUMENTARY_FREEZE = NO`. Les 108 fiches ne possèdent pas toutes une archive primaire verbatim datée ni une attribution segmentée humain/IA ; les tests runtime n'ont pas été relancés.

Pour l'index principal, voir [matrice des concepts](18_CONCEPT_SOURCE_MATRIX.md) et [Atlas](15_CONCEPT_ATLAS.md).
