# P152 — Continuité d'identité et mémoire d'hypothèses concurrentes

## Pourquoi P152

P151 (2 500 examens, 3m23) a isolé deux défaillances : lors de l'inversion de trajectoire, erreur 40 pixels et identité correcte 0 % parmi les réponses ; lors de la superposition, couverture 100 % mais identité correcte 62,4 % parmi les réponses. Un changement de couleur seul était mieux géré, mais avec seulement 67,6 % de couverture.

## Implémentation

Le nouveau routeur reçoit **uniquement neuf images** d'une séquence de dix images. Il extrait les composantes visuelles à partir de P151 et conserve jusqu'à 12 **trajectoires d'association complètes candidates** à travers la séquence (beam search). Pour chaque image, il évalue des attributions distinctes d'objets aux pistes ou l'absence de détection, puis conserve les hypothèses diversifiées de meilleur coût. Le mouvement extrapolé intervient dans le coût d'association ; le changement de couleur ajoute une faible pénalité, jamais une interdiction. Si deux hypothèses proches impliquent des futurs divergents pour l'objet suivi, le système émet `HOLD_COMPETING_IDENTITIES`.

**Comparateur identique, mêmes images** : `P151_MOTION_ASSOCIATION_SAME_FRAMES`. Toutes les prédictions sont faites avant que les deux positions futures véritables A et B ne soient utilisées pour noter l'erreur, la couverture, le taux d'identité correcte parmi les réponses et le taux d'identité correcte rapporté à tous les examens.

Dix conditions : couleur seule, inversion seule, couleur+inversion, croisements identiques ou distincts, superposition, occultation courte ou longue, caméra+couleur, distracteur.

## Attention méthodologique

- La mémoire multi-hypothèses est ici un **algorithme de recherche**, pas une mémoire native ni une dynamique physique apprise.
- Le score d'identité est encore un indicateur géométrique (position prédite plus proche d'A que de B). Lorsque les deux objets sont proches, ce score ne suffit pas à confirmer une identité suivie.
- Ce suivi ne dispose pas encore de réassociation en arrière sur toute une vidéo ; plusieurs hypothèses peuvent être supprimées quand la largeur du faisceau est atteinte.
- Aucun résultat réel de P152 n'est connu avant le run PC. Les améliorations ne sont pas garanties.
- Aucun fichier de P151 n'est modifié ; les anciens rapports restent préservés.

## Exécution Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_identity_beam_p152.py" -v
if ($LASTEXITCODE -ne 0) { throw "P152 : tests échoués" }
py -m brody_world_physique.image_identity_beam_p152 --minutes 15 --episodes-each 250 --beam-width 12 --out "build\brody-p152-identity-001"
if ($LASTEXITCODE -ne 0) { throw "P152 : run échoué" }
Get-Content "build\brody-p152-identity-001\MASTER_REPORT.json"
```

Le temps est plafonné à 15 minutes. Si le nombre d'examens est incomplet, `stopped_by=TIME_BUDGET` et `conditions_completed` le signalent : ne pas transformer une campagne incomplète en PASS scientifique.

## Gouvernance

`decision_authority=KX108_ONLY`; `native_memory_write=false`; `canonical_promotion=false`. Toute promotion éventuelle dépend d'un audit indépendant et de tests contradictoires.
