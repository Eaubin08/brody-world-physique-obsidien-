# 59 — Réintégration Brody : première couture exécutée, suite par propriétaire

## Statut précis
Premier adaptateur **implémenté et publié** : `brody_world_physique/p29d_reconnect_organs_v0.py` et `tests/test_p29d_reconnect_organs_v0.py`. **Tests non exécutés sur le PC opérateur à cette rédaction.** Ceci n'est ni le raccordement global achevé ni un nouveau world model.

## Implémentation effectuée
`PixelObservation` → `SpatialRelations` → `WorkingBelief` → `GoalRouting` P2.9, avec la **réutilisation directe des classes déjà présentes** `WorldStateDeltaV0` et `WorldExperienceCandidateV0` (`contracts_v0`), et `LearningEpisodeSignalV0` / `triage_learning` (`reverso_learning_v0`). Contradiction d'une prédiction ancienne vs courante conservée comme **désaccord non causal**, provenance d'entrée conservée, HOLD propagé, expérience candidate non souveraine, proposition de rétention = revue d'hypothèse, aucune écriture mémoire. L'adaptateur n'appelle PAS Reverso de reconstruction pixel, n'instancie PAS un vrai état MMonde ni F12, et ne découvre PAS les lois physiques.

## Pourquoi ne pas assembler tout en une fonction géante
Les propriétaires déjà inventoriés dans les docs 42/43 et audit 58 :
- **P — perception F16** : source physique et qualité; ici seules les mesures de `PixelObservation` P2.9 sont consommées.
- **R — MMonde/F12/F13** : observation située, temps/coordonnées/unités/transformation; interfaces readonly, non rattachées au runtime expérimental.
- **Reverso** : reconstruction/re-perception et fidélité IN, avec pixels source, masques et tests séparés; `triage_learning` réutilisé seulement pour le savoir candidat.
- **V4.2** : orientations, transformations cardinales et réciprocité 2D; pas encore adaptateur vers les repères P2.9c.
- **P1 bridge** : jointure multi-vues vidéo, spatial, temps et mouvement; pas encore réutilisée en bout-en-bout dans la boucle P2.9.
- **E — apprentissage** : Delta/ExperienceCandidate réemployés; contexte de réutilisation, contradicteurs indépendants et vrai transfert restent à construire.
- **I — intention/IN** : routage basique branché; profils de rigueur par régions pour génération à brancher côté éditeur.
- **G — B7/B8/B10/KX108** : aucune promotion, persistance ou décision transférée à Brody.

## Ordre d'intégration à tester, sans perdre la méthode initiale
1. Valider ce petit adaptateur et ses invariants sur PC. Puis le faire fonctionner à travers le banc P2.9c sans injecter la vérité du simulateur.
2. Reprendre le même matériel `multirepresentation_ball_bridge_v5` et `world_transfer_probe_v1` pour adapter vidéo+temps+repère, au lieu d'utiliser des déplacements disjoints détachés des événements.
3. Reprendre transformations/orientation de V4.2; distinguer les transformations de caméra vs mouvement d'objet vs transformation de représentation; double sens / inverse seulement si admissible. Toute transformation manquante => UNKNOWN.
4. Reconnecter Reverso image/source et re-perception sur exactement les mêmes séquences; maintenir scores raster, géométrie, trajectoire et causalité séparés.
5. Séparer par protocole factoriel : décor graphique seul, source d'ancrage seule, les deux, aucun, avec et sans historique. Aucun changement de politique selon la vérité TEST.
6. Étendre au-delà de la simulation avec sources datées et indépendantes lorsqu'elles sont disponibles (GPS/GNSS/micro/biologie/thermodynamique), sans inventer ce qu'un pixel ne montre pas.
7. Pour la génération, définir conservation exacte de l'IN et contraintes par zone, réutiliser `image_v0` et Reverso; distinguer synthèse artistique de connaissance physique.
8. Mettre un gate de promotion B8 seulement après audit formel B8/B10 et autorisations canoniques; Native Memory readonly et KX108_ONLY restent invariants.

## Test — PowerShell PC fixe, bonne branche
```powershell
$repo = "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
Set-Location $repo
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p29d*.py" -v
if ($LASTEXITCODE -ne 0) { throw "P2.9d reconnect test FAIL" }
```

## Limites
- Le résultat `WorkingBelief` est une hypothèse d'après repère donné ; **ne détecte pas lui-même** quel repère est fiable.
- `state_before_ref` et `state_after_ref` sont des références candidates locales, pas des états MMonde réellement validés.
- Source hash passée par appelant : l'adaptateur ne contrôle pas les octets d'une vidéo ou image.
- La contradiction relevée compare deux prédictions, pas une prédiction avec vérité physique indépendante.
- Aucun test de généralisation nouveau n'est effectué par cette couture.
- Ne pas déclarer « tous les principes reconnectés » avant les intégrations vidéo/représentations/transformations/Reverso/perception réelle.
