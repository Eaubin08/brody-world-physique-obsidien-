# P2.8 — Contrat candidat : hiérarchisation, stabilisation, révision et intention
Statut : **PROPOSITION À VALIDER** — documentaire seulement, non implémentée dans Brody.
Origine : précisions directes de l'auteur après les expériences P2.6/P2.7.

## 1. Intention initiale de l'auteur — à préserver
Tout ce qui est conservé doit être **rangé, hiérarchisé et recontextualisable**. Une donnée ou un savoir conservé n'a pas besoin d'être une vérité absolue de la réalité : c'est ce que Brody **a appris et retient à un instant donné**, avec son état de confiance, ses conditions et ses limites. Un repère suffisamment connu et stabilisé doit pouvoir être réutilisé, sans refaire systématiquement toute sa route d'apprentissage. Ensuite, **ce que veut la personne** oriente l'usage et l'approfondissement du savoir (comprendre, générer, explorer, tester, préciser) ; cela ne transforme jamais un souhait en vérité physique.

L'auteur insiste aussi sur le fait que des fluctuations qualifiées localement de « bruit » peuvent être **des données de précision** ailleurs dans la hiérarchie des représentations, selon le point de vue, l'espace, le temps et l'échelle.

## 2. Lois invariantes candidates
- OBSERVATION != INTERPRÉTATION != EXPÉRIENCE != SAVOIR_RETENU != VÉRITÉ_ABSOLUE.
- FIABILITÉ_HISTORIQUE != VÉRITÉ_ACTUELLE ; NOUVELLE_DONNÉE != VÉRITÉ ; MAJORITÉ != VÉRITÉ.
- STABILISÉ != IRRÉVOCABLE ; MÉMOIRE != VÉRIFICATION ; CONFIANCE != AUTORITÉ.
- INTENTION_UTILISATEUR != PREUVE ; ORIENTATION_COGNITIVE != AUTORISATION_DE_MUTATION.
- DÉTAIL_IGNORÉ_PAR_UNE_COUCHE != DONNÉE_SANS_UTILITÉ_GLOBALE.
- PRÉCISION_PAR_CONTEXTE est une hypothèse expérimentale, pas une propriété acquise.

## 3. Organisation du savoir : quatre plans à ne pas écraser en un score
**A. Plan documentaire / provenance** : observation ou expérience d'origine, chaîne de transformation, auteur ou système, conditions de capture, version et dépendances.

**B. Plan représentatif** : langage de chaque couche, coordonnées et transformations, référentiel, échelle micro/macro, temporalité, relations/superpositions. Ne pas convertir de force tout en XY ; conserver le lien aux informations périphériques et aux fluctuations.

**C. Plan épistémique** : type de proposition, statut candidat, niveau de vérification, cas réussis ET échecs, domaine de validité, contradictions ouvertes, stabilité locale, incertitude et possibilité d'obsolescence.

**D. Plan d'usage / intention** : but fourni par la personne, niveau de précision attendu, budget d'exploration, activité (comprendre, créer, tester, approfondir), permissions et limites de gouvernance. Ce plan sélectionne les savoirs utiles, mais ne réécrit pas leurs preuves.

## 4. Cycle candidat des informations
1. `OBSERVED` : événement/data brute conservé(e), avec provenance et contexte, sans affirmation causale.
2. `DERIVED` : représentation traduite ou relation inférée, avec hypothèses et références d'entrée.
3. `EXPERIENCED` : essai/action/observation de conséquence ; noter les résultats, réussites, échecs et conditions. Un épisode d'expérience n'est pas une vérité à lui seul.
4. `RETAINED_WORKING` : meilleure connaissance provisoire actuellement retenue, explicite et révisable.
5. `STABILIZED_CANDIDATE` : repère durablement utile après répétitions variées et absence de contre-exemples non résolus dans un domaine identifié.
6. `VERIFIED_SCOPED` : connaissance vérifiée selon un protocole **précisé**, dans une portée déterminée ; ce statut n'implique jamais universalité.
7. `CHALLENGED` / `SUPERSEDED` : conflit nouveau ou révision ; on conserve les versions et la chaîne des explications, jamais de suppression silencieuse.

Ces noms sont une **terminologie proposée** pour discussion. Ils ne doivent pas écraser les états canoniques déjà définis dans B7/B8/B10, Native Memory et KX108. Avant toute implémentation, faire le mapping formel vers les contrats existants.

## 5. Règle de hiérarchie dynamique
Ne pas classer par ordre fixe « ancien > nouveau » ou « nouveau > ancien ». À chaque situation, évaluer la correspondance de portée entre savoir retenu et observation : source, indépendance des preuves, repère, temps, échelle, transformations, similarité des conditions et historique des contradictions. Quand les indices s'opposent, générer des hypothèses distinctes et expliciter l'observation qui pourrait les départager. Si impossibilité de conclure : `HOLD` explicite, sans inventer une vérité.

Un signal minoritaire historiquement fiable peut être retenu contre une majorité trompeuse, **mais ne gagne pas automatiquement**. Une expérience passée peut être invalidée par une nouvelle vérification reproductible ; une contradiction ponctuelle peut simplement révéler un changement de référentiel.

## 6. Stabilisation et économie d'apprentissage
Une stabilisation n'est pas un nombre magique de réussites. Exiger une diversité de cas, contre-épreuves, contrôle des dépendances, portée déclarée, incertitude calibrée et recul temporel quand pertinent. Réutiliser l'acquis pour les objectifs courants ; ne rouvrir que la partie contestée, modifiée ou demandée. Garder le chemin de preuve, sans imposer de recalcul permanent.

Le seuil de stabilisation doit être **pré-gelé par domaine et par usage**, mesuré sur des données inédites, et ne doit pas découler des résultats TEST.

## 7. Intention humaine et autorité
L'utilisateur peut choisir l'objectif : exploiter les connaissances disponibles, créer une image ou une scène, explorer d'autres angles, exiger plus de précision, apprendre ou provoquer un test adversarial. Brody sélectionne les repères et l'effort selon cet objectif. Il **ne doit pas changer le niveau de vérité d'une donnée pour satisfaire la demande**. Les propositions cognitives restent distinctes de l'autorité de décision : `KX108_ONLY`; aucune mutation de mémoire implicite. Toute promotion durable emprunte les contrats existants B7/B8/B10 et les voies gouvernées, jamais ce document seul.

## 8. Test P2.8 à construire AVANT toute affirmation de capacité
Comparer sur exactement les mêmes observations et sur des séquences temporelles :
- A : majorité de repères, sans historique.
- B : historique figé, priorité au repère ancien.
- C : nouvelles observations prioritaires, oublie trop vite l'historique.
- D : portée + preuve + contradiction + révision contrôlée.
- E : D + intention de la personne : même statut de vérité, mais effort/chemin d'apprentissage ou génération différents.

**Adversaires nécessaires** : renverser quel repère est fiable après TRAIN ; changer de caméra/référentiel ; faire mentir la majorité ; rendre incohérents des historiques apparemment robustes ; mélanger signaux faiblement informatifs et vrais artefacts ; répéter les mêmes données pour simuler fausse indépendance ; proposer un nouvel objectif utilisateur qui ne doit changer QUE le chemin d'usage ; tester l'absence de vérité TEST en amont ; contrer toute promotion durable non autorisée.

**Mesures** : erreur de prédiction à couverture identique, HOLD justifiés/abusifs, détection de changement de régime, délai de révision, contamination par données corrélées, taux de fausses promotions, réutilisation sans réentraînement, qualité de provenance/rejeu, adaptation à l'objectif sans réécriture de statut.

## 9. Leçons des expérimentations disponibles
P2.6 : cohérence majoritaire de repères trompeurs conduit à des erreurs importantes.
P2.7 : sur 480 TEST, `hierarchy` et `experience` ≈0,329 px ; `majority` ≈19,672 px sur 323 acceptés ; `hierarchy_experience` ≈13,290 px, dont 245 erreurs >10 px. Ce protocole a **un biais intentionnel** : le dernier repère est fiable par construction ; `experience` est calibrée avec vérité simulateur. Les scores ne démontrent ni hiérarchie autonome ni savoir stabilisé. Publication P2.7 sur GitHub **non confirmée** au moment de la rédaction (script Windows bloqué).

## 10. Décisions à geler
Avant forge P2.8 : vérifier compatibilité avec contrats cognitifs et mémoire (B7/B8/B10), définir le schéma d'un savoir structuré et ses relations, fixer le protocole d'autorisation des mutations, établir les tests adversariaux avec TRAIN/TEST distincts et générateur nouveau, valider que l'intention pilote l'usage sans fabriquer la vérité.

**Résumé canon candidat :** « Brody conserve des observations, expériences, interprétations et savoirs dans une hiérarchie contextualisée. Sa meilleure connaissance à l'instant t est un état révisable, non une vérité absolue. Des repères suffisamment stabilisés deviennent réutilisables sans refaire toutes les expériences. L'intention humaine dirige leur usage et leur approfondissement ; la vérification, la provenance et la gouvernance encadrent toujours leur statut et leur persistance. »
