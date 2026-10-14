# P165 — HARD++ : scène contextuelle, plans relationnels, identité, occultation, événements

**Statut : protocole expérimental spécifié, implémentation HARD++ non encore validée.**
**Motivation utilisateur :** « différencier le monde comme 1 plan, second plan … sur l'image de fond … ça dépend des contextes », compléter les quatre réparations P164 et tester **encore plus hard**.

## 1. Principes de conception, attribution
- **Direction utilisateur :** un objet doit être situé dans un monde composé de plans, arrière-plan et contexte ; nombre et nature des plans non figés ; association ne doit pas dépendre de la couleur ; préserver les discontinuités ; conserver les pistes et contradictions ; comparer après réapparition ; aller bien au-delà du test de deux objets qui se croisent.
- **Proposition technique expérimentale (non déjà prouvée) :** `SceneGraphCandidate`, `LayerCandidate`, `EntityTrackCandidate`, `RelationalOcclusionCandidate`, `CameraMotionCandidate`, `EventHypothesisCandidate`, avec incertitudes et provenance. Ce sont des **vues dérivées**, pas de nouvelles ontologies racines. Réutiliser F16/MMonde/F12 lors du raccordement futur.

### 1.1 Un « plan » n'est pas un nombre fixe de couches
Le plan peut être une **relation d'ordre locale** : A devant B, B masque C ; à un autre instant A est derrière C. D'autres contextes nécessitent un graphe de surfaces, profondeur 3D ou une hiérarchie de régions ; ne pas promettre une profondeur métrique depuis une seule image.

### 1.2 Une même cause, plusieurs projections
Séparer états monde candidats (géométrie, objets, caméra, temps) des pixels produits par observation. La scène n'est pas égale au raster. La caméra est un agent de projection, pas une loi physique de l'objet. Référentiels annotés IMAGE vs SCENE et transformations vérifiables, avec unités.

## 2. Pipeline HARD++ cible

```text
captation + source hash + temps + cadre
  → régions/fond/mouvement global candidats
  → segmentation en entités et surfaces (sans couleur figée)
  → scene graph candidat : devant/derrière/cache/touche/lointain/UNKNOWN
  → pistes multiples avec identité, provenance, score et contradictions
  → événements : position/vitesse/accélération/discontinuité (jamais lissées)
  → hypothèses concurrentes scène/caméra/physique
  → états futurs précommittés + render multivues
  → images tenues secrètes, réapparitions, nouveaux angles/capteurs
  → re-perception ; scores séparés
  → SELECT / MULTI / HOLD / NOVELTY_CANDIDATE
```

## 3. Matrice adverse HARD++ : conserver les 77 cellules P161–P164 + étendre

| Famille | Épreuve réellement contradictoire | Erreur à interdire |
|---|---|---|
| H01 — apparence | Balle rouge → bleue, ombre/lumière, changement de taille et texture | Perdre identité car couleur différente |
| H02 — distracteurs | 30 objets visuellement plausibles avec tailles/teintes recouvrantes | Centroïde du décor pris pour cible |
| H03 — croisement | Deux objets identiques se croisent, vitesses opposées ; identité **non observable** | Inventer une identité unique |
| H04 — caméra | Pan, zoom, rotation, accélération de caméra, fond dynamique | Confondre déplacement monde/image |
| H05 — plans | Masquage partiel/total, ordre des plans changeant, vitres/transparence | Plan figé « avant/milieu/arrière » |
| H06 — événement masqué | Saut, rebond, accélération, inversion pendant absence | Interpolation autoritaire |
| H07 — réapparition | Objet transformé, objet substitué, deux candidats réapparaissent | Déclarer « même objet » sans preuve |
| H08 — physique inattendue | Accélération impulsionnelle, collision, oscillations irrégulières, freinage asymétrique | Tout reclasser en loi connue |
| H09 — contexte | Même image mais caméra fixe/mobile et repères distincts ; source non identifiable | Faux SELECT en cas d'équivalence observationnelle |
| H10 — profondeur | Échelles/objets superposés, perspective, profondeur relative vs métrique | Déduire des mètres sans calibration |
| H11 — reconstruction | Projection future et re-render sans future frame en entrée | Fuite de vérité du simulateur |
| H12 — indépendance | Renderer différent, trajectoires de provenance distincte, changements hors entraînement | Surapprentissage au style du générateur |
| H13 — multi-objets | Collision/échange d'apparence puis séparation | Échanger les identités silencieusement |
| H14 — fond trompeur | Parallaxe : fond proche et lointain n'ont pas le même flux | Supposer que tous les pixels de fond ont même déplacement |
| H15 — image contradictoire | Reflet, ombre portée, affichage sur écran et objet physique | Confondre reflet et autre entité réelle |
| H16 — perte de signal | Images corrompues, cadence irrégulière, absence de frame, timestamp incertain | Calculer vitesse avec dt=1 implicite |

**Contrôles négatifs indispensables :** le même rendu peut être produit par un objet mobile sur caméra fixe ou par objet fixe sur caméra mobile sans fond visible ; deux identités strictement indistinguables après crossing ne sont pas mathématiquement distinguables à partir du seul raster. Ces cas DOIVENT produire MULTI/HOLD, et non un score de « 100 % de précision » artificiel.

## 4. Quatre réparations prioritaires de P164
1. **Perception polymorphe :** ne pas programmer « rouge seulement ». Décomposer d'abord fond/foreground et instances, puis associer selon forme/trajectoire/relations/compatibilité, avec fiabilité de chaque indice.
2. **Discontinuité non effaçable :** distinguer observation, suivi, extrapolation ; garder un événement saut ou direction inversée comme possible nouveauté, même si un lissage rendrait la piste plus probable.
3. **Beam honnête :** ne jamais nommer « quatre hypothèses » les quatre variantes d'un même appariement si l'alternative vitale a été éliminée. Mesurer le rappel de la **véritable piste** dans le beam et la diversité d'identités.
4. **Réapparition falsifiable :** séparer `SAME_IDENTITY_SUPPORTED`, `POSSIBLE_IDENTITY`, `INSUFFICIENT_EVIDENCE`, `CONTRADICTED`. Une continuité cinématique seule n'est pas preuve d'identité.

## 5. Gate système, sans auto-promotion
- RASTER_GATE : précision position ET recall de présence + faux objets + segmentation IoU.
- SCENE_GATE : ordre des plans et relations, statut UNKNOWN explicite.
- ID_GATE : pureté d'identité après croisement, top-k true-track recall ; impossible-cases abstention.
- TIME_GATE : temps réels/timestamps et discontinuités non supprimées.
- CAM_GATE : erreur de mouvement de caméra sur fond indépendant, états non identifiables HOLD.
- PHYSICS_GATE : erreur de trajectoire, nouveauté fausse vs non détectée, lissage adversarial.
- REVERSE_GATE : image future candidate précommit, source indépendante, re-perception et différence image/monde distinctes.
- UNCERTAINTY_GATE : erreurs confiantes, couverture vs précision et calibration.
- NO_REGRESSION_GATE : exactement les 77 conditions existantes avec baseline P163/P164 et seed scellée, plus 16 familles adverses.
- GOV_GATE : readonly, provenance, `native_memory_write=false`, `canonical_promotion=false`, `KX108_ONLY`.

## 6. Séquence d'implémentation recommandée
**P165-A (prochain build) :** nouvelles fixtures visuelles et épreuves impossibles/indiscernables ; conservation de la baseline 77, métriques par couche.
**P165-B :** perception indépendante de couleur et association multi-objets, *sans oracle* de segment ou d'identité.
**P165-C :** graphe contextuel des plans et caméra avec incertitude d'observabilité.
**P165-D :** continuité sous occultation + événements contradictoires + vraie évaluation de réapparition.
**P165-E :** génération/ré-perception externe des scènes et épreuves cachées indépendantes.

Chaque étape doit avoir des tests RED/GREEN explicites et un rapport séparé. NE PAS annoncer HARD++ GREEN en se basant sur des tests unitaires d'infrastructure ou des images produites par un seul renderer.

## Verdict
`P165_HARD_PLUS_PLUS_PROTOCOL_SPECIFIED / ORIGINAL_CONTEXT_LAYER_IDEA_PRESERVED / P164_RED_COLOR_AND_NOVEL_JUMP / HARD_PLUS_PLUS_VALIDATION_NOT_STARTED`.
