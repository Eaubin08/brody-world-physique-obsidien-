# Brody — Passe 131 : couverture hétérogène, premier exécutable multi-compétences

**Cap fixé par la demande utilisateur :** augmenter le NOMBRE DE TYPES DE TESTS, pas le volume de variantes identiques. Le registre de 80 sujets de la passe 130 sert de backlog de couverture, et non de preuve de 80 fonctionnalités disponibles.

Ce lot apporte `image_heterogeneous_capability_audit_p131.py` : huit sondes fonctionnelles réellement différentes, couvrant la séparation de composantes, le RGB, la transformation géométrique, la génération depuis une représentation compacte, l'arbitrage des contradictions d'identité, la détection de renversement, la non-duplication d'une leçon et le refus d'un mauvais format génératif. Il signale explicitement huit autres besoins en **TODO**, sans convertir des concepts absents en PASS. Les expériences construites localement sont synthétiques, ne démontrent pas le transfert réel, et ne constituent pas à elles seules un enseignement autonome.

## Exécution PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_context_transition_transfer_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Régression 129 échouée" }
py -m unittest discover -s tests -p "test_image_heterogeneous_capability_audit_p131.py" -v
if ($LASTEXITCODE -ne 0) { throw "Validation 131 échouée" }
py -m brody_world_physique.image_heterogeneous_capability_audit_p131 --out "build\brody-heterogeneous-131-001"
if ($LASTEXITCODE -ne 0) { throw "Audit 131 échoué" }
Get-Content "build\brody-heterogeneous-131-001\MASTER_REPORT.json"
```

## Après la validation

Les prochains **lots de construction** doivent inclure des organes réellement nouveaux : segmentation multiobjet et occlusion ; générateur de silhouette/relations au lieu de mosaïque ; enseignement explicite du 360° sur séries multi-vues réelles ; séquences d'interaction et contre-exemples ; cours externes autorisés, provenance et vérification ; épreuves de mémoire différée. Les tests de robustesse ou de répétition sont utiles **au sein** de chaque compétence, mais ne doivent jamais remplacer la création d'un autre type d'apprentissage.

**Gouvernance** : expérimental, `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`. Ne pas toucher `main`.
