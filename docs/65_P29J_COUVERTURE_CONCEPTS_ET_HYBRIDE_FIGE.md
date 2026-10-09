# 65 — Couverture des recherches et P2.9j hybride figé

## Réponse documentaire
**NON : toutes les recherches personnelles ne sont PAS encore réintégrées au runtime.** Les tests P2.9h/i ne portent que sur la position spatiale et le rappel expérientiel sur vidéos synthétiques.

### Concepts reconnus et statut honnête
| Concept/source | État dans Brody P2.9j | Blocage ou prochain test |
|---|---|---|
| Apprentissage préverbal type enfant, école/expérience | simulation partielle V1–V4, P1 | autonomie des stratégies non prouvée |
| Mémoire des procédures, erreurs, instruments, savoir-faire | V1–V4 existants; P2.9j n'en réutilise pas la totalité | rattacher capacité + code + version + contexte |
| Historiquement fiable / données nouvelles / vérité vérifiée | P2.8–2.9i tests partiels | preuve de portée, révision sans oracle TEST |
| Connaissance provisoire, stabilisation, intention humaine | contrats P2.8, séparation P2.9 | valider B7/B8/B10 puis préserver KX108_ONLY |
| Chaque étage son langage, sa hiérarchie, espace et temps | couches P2.9, ponts P2.9d–g | transformations typées avec provenance/horloge |
| Fluctuation dite « bruit » = données de précision contextualisées | P2.4–P2.6 partiels | scènes visuelles changées et faux repères corrélés |
| Invariants, symétrie, Fibonacci, proportion | relations V4.2 2D; autres idées documentées | tester utilité, pas forcer une loi universelle |
| 360°, perception réciproque, inverse | orientations cardinales V4.2 et inverse algébrique | monde 3D et perspectives non démontrés |
| Analyse↔synthèse, décomposition, couches du peintre | Reverso + école de dessin | raccordement de re-perception et édition |
| Fidélité pixels, source et IN, précision variable par zone | éditeur/Reverso disponibles | contrat multi-régions et conservation de la source |
| Shazam visuel, signatures, 34 arbres | pistes historiques | interfaces précises et tests absents du P2 actuel |
| World Foundry, multiples versions/formes d'entraînement | conceptuel/documentaire | catalogue exhaustif des configurations non gelé |
| Multidimensionnel, micro↔macro, matière, thermodynamique | contrats/propositions | dépend de mesures/variables distinctes selon échelles |
| F16, F12, MMonde, SENS, GPS comme organes | contrats et certaines représentations candidates | adaptation runtime explicite sans fusion des autorités |
| Représentations en circulation, mutualisation sans double compter | P1 et P2.9g quatre vues d'une source | vraie ablation multimodale sur mêmes frames |
| Génération visuelle apprise, contrôle par Reverso | images Reverso synthétiques | pas encore un générateur autonome de qualité |

**Ne pas présenter cette table comme l'inventaire exhaustif de toutes les archives**, notamment des 81+ variantes d'apprentissage évoquées dans d'autres travaux : attribution et définition d'origine doivent être réconciliées séparément. Les scripts P2.9d-g ne constituent pas l'activation générale de ces organes.

## P2.9j : ce qui est effectivement développé
`p29j_frozen_hybrid_audit_v0.py` évalue une **règle figée avant lecture des scores de cette analyse** : si A4 mémoire a proposé, choisir A4; sinon A1 spatial; sinon HOLD. Les prédictions A4/A1 viennent du fichier P2.9h déjà pré-engagé. L'analyse utilise les erreurs uniquement pour mesurer la politique, pas pour la choisir. Politique suggérée après inspection de P2.9i : **post-hoc sur le même banc, pas preuve prospective indépendante**. Aucune nouvelle perception, apprentissage ou génération; score attendu à mesurer, pas anticiper. Documenter les 50 cas, couverture/erreur, variantes de baselines, provenance et replay.

## PC fixe — sans changer de branche ni modifier main
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p29j*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
$source = "build\p29h-ablation-20261009-061517.json"
$out = "build\p29j-hybrid-$(Get-Date -Format yyyyMMdd-HHmmss).json"
py -m brody_world_physique.p29j_frozen_hybrid_audit_v0 --source $source --out $out
if ($LASTEXITCODE -ne 0) { throw "P2.9j échoué" }
py -m brody_world_physique.p29j_frozen_hybrid_audit_v0 --source $source --out $out --verify
if ($LASTEXITCODE -ne 0) { throw "Rejeu échoué" }
Write-Host "RESULTATS=$out"
```

## GATE suivant
Ne pas retoucher le choix hybride à la vue du score. Tester sur nouvelles familles d'images et changements d'environnement, en réintroduisant effectivement P1 raster, Reverso et les outils F12/F16/MMonde avant de déclarer un gain multimodal. Aucun B8/B10 write et KX108_ONLY.
