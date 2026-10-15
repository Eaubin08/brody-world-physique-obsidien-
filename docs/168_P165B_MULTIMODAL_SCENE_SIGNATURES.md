# P165-B — Cartographie multimodale, signatures et monde contextuel

## Origine / vision
**Utilisateur :** au-delà de la scène (premier plan, second plan, fond selon contexte), intégrer « les spectres style Shazam », plusieurs types de vision pour cartographier radar, infrarouge, etc. Puis : « tous d'un coup go ». Les familles concernent RGB, spectres, thermique, radar, LiDAR, acoustique, flux optique et géométrie, plus leurs interactions contextuelles.

**Interprétation technique expérimentale, non démontrée :** organiser chaque observation en `{mode, valeurs, source, time_id, frame, quality}`. Les signatures sont des **indices multiples**, jamais des preuves absolues d'identité. Le graph de scène des plans est relationnel, à construire suivant P165-C; ne pas figer trois plans.

## Ce qui est réellement publié maintenant
`brody_world_physique/modal_signature_fusion_p165b.py` et `tests/test_modal_signature_fusion_p165b.py` : laboratoire minimal de huit modalités, neuf cas opposables, comparaison à temps et repère identiques, preuve auto-générée rejetée, contradictions conservées. Les chiffres sont des tableaux de **fixtures simulées**, PAS des images mesurées par des capteurs et PAS une fusion multisensorielle calibrée.

- `color_changed` : RGB contradictoire, géométrie/thermique/... cohérentes : MULTI (pas suppression de contradiction).
- `thermal_contradiction`, `multi_conflict` : capteurs en conflit : MULTI.
- `radar_hidden` : RGB absent, autres signatures restent candidates.
- `generated_forgery` : signaux de source GENERATED ne constituent jamais la vérité indépendante : HOLD.
- `time_mismatch`, `camera_frame_mismatch` : comparaison interdite sans alignement explicite.
- `same_signature_distinct_entities` : même empreinte n'est pas identité unique prouvée.
- `no_sensor_available` : HOLD.

**Limites supplémentaires :**
- Les étiquettes OBSERVED/SIMULATED restent fournies par l'appelant : le module seul n'authentifie aucun capteur.
- Les seuils numériques .12 et .5 sont heuristiques non calibrés (pas d'unité physique, pas de preuve de fiabilité).
- Aucun spectrogramme audio/Shazam réel, aucune formation d'empreinte spectrale, aucune caméra thermique, aucun radar, aucun LiDAR connecté. Les types de capteurs listés indiquent des interfaces cibles, non des implémentations d'acquisition.
- Les relations de plan, occlusion et graphe physique ne sont pas intégrées à ce laboratoire P165-B et P164 garde ses erreurs; le protocole P165 Hard++ 16 familles n'est pas entièrement exécuté.
- Les 77 scénarios historiques et les 150 scénarios P165-A ne sont pas rejoués dans cette commande.

## Cible architecturale à poursuivre sans perdre la vision

```
RGB, spectral, acoustique, IR, radar, LiDAR, etc.
    -> source/provenance + temps synchronisé + repère/spatialisation
    -> représentation spécifique pour chaque capteur
    -> fond / foreground / surfaces / relations de plans [contextuels]
    -> entités candidates + empreintes conditionnelles multi-vues
    -> identité candidate et contradictions, trajectoires multiples
    -> physique, événements, hypothèses
    -> projection par modalité + génération de vues candidates
    -> confrontation indépendante observée vs générée
    -> HOLD / MULTI / NOVELTY_CANDIDATE; KX108_ONLY
```

### Attention aux distinctions physiques
Un spectrogramme acoustique indique un contenu fréquence-temps ; il ne donne pas à lui seul une identité unique. Un radar mesure des retours électromagnétiques, l'information dépend de la configuration. L'infrarouge thermique ne mesure pas toujours directement une température sans hypothèses d'émissivité/calibration. Une image RGB ne contient pas automatiquement une mesure radar/thermique fiable. Une modalité générée est une hypothèse, pas un sensor truth.

## Commande Windows PowerShell — arrêt si échec

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/modal_signature_fusion_p165b.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe P165-B échouée" }
py -m unittest discover -s tests -p "test_modal_signature_fusion_p165b.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P165-B échoués : STOP" }
py -m brody_world_physique.modal_signature_fusion_p165b --out "build\brody-p165b-modal-signatures-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne P165-B échouée" }
Get-Content "build\brody-p165b-modal-signatures-001\MASTER_REPORT.json"
```

## Critère de reprise et suite
`P165B_LAB` sert à éprouver les **contrats** de données et les contradictions avant une vraie architecture multisensorielle. Les prochains builds doivent : faire des entrées RGB/audio/radar/thermique réelles avec provenance vérifiée ; aligner temps/référentiels ; baser les empreintes sur des signaux extraits ; construire le graphe contextuel des plans ; maintenir pistes d'identité adverses ; produire une prédiction/génération indépendante et la confronter à une nouvelle mesure ; rejouer 77 + 150 + la suite 16 familles.

`native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`.

**Verdict avant run :** `P165B_MULTIMODAL_CONTRACT_LAB_PUBLISHED / EIGHT_MODALITY_INTERFACES / SENSOR_HARDWARE_AND_WORLD_FUSION_NOT_CONNECTED / PC_VALIDATION_PENDING`.
