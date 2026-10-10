# 47 — P2.5 : lecture contextuelle depuis les pixels

## But
Tester, dans une expérience **synthétique et bornée**, la proposition de l'auteur : les variations de l'environnement jugées accessoires par une représentation peuvent préciser l'interprétation du mouvement selon le repère, la temporalité et la hiérarchie des informations.

## Contrôle expérimental
Le même déplacement **apparent** de balle (+10 pixels) est rendu dans cinq paires de PNG (avant/après) :
- objet mobile et caméra fixe : déplacement monde +10 ;
- objet fixe et caméra mobile : déplacement monde 0 ;
- les deux mobiles : déplacement monde +6 ;
- une balise du décor volontairement déplacée : estimation robuste attendue +6 ;
- trois balises déformées : **HOLD** attendu si les mesures de fond sont contradictoires.

Le logiciel produit et relit de vrais PNG 360×220. La localisation de l'objet et des cinq balises provient de masques couleur OpenCV, pas des valeurs du simulateur. Le déplacement monde de référence n'est utilisé que dans le bilan **après** le traitement des images.

Deux lectures : **objet seul** (déplacement image apparent) et **objet+contexte** (déplacements des balises et règle de cohérence de P2.4). Un désaccord grave provoque HOLD plutôt qu'une moyenne aveugle.

## Limites / revendications interdites
Il s'agit de frames rendues par notre propre générateur, avec seuils couleur connus, géométrie simple, mouvement horizontal, balises séparées. La logique de correction est codée par un humain, non apprise. Ce n'est ni une preuve de monde physique compris, ni un test de vidéo réelle, ni une fusion F16/MMonde/F12 opérationnelle, ni une généralisation à des angles 3D. Cinq paires ne constituent pas un jeu TEST indépendant. Il faudra ensuite vraiment geler un entraînement puis tester d'autres textures, lumières, occultations, caméras, référentiels et générateurs.

## Commandes PC / publication
Depuis le repo Brody, sur `exp/p2-multirepresentation-ablation-20261009` :

```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
py -m unittest discover -s tests -p "test_*.py"
if ($LASTEXITCODE -ne 0) { throw "Echec tests" }
$out = "build/p25-pixels-$(Get-Date -Format yyyyMMdd-HHmmss)"
py -m brody_world_physique.p25_pixel_context_v0 --out $out
if ($LASTEXITCODE -ne 0) { throw "Echec P2.5" }
py -m brody_world_physique.p25_pixel_context_v0 --out $out --verify
if ($LASTEXITCODE -ne 0) { throw "Echec rejeu" }
Invoke-Item "$out/images"
notepad "$out/evaluation.json"
.\scripts\publish_local_evidence.ps1 -RunPath $out
```

Les dix PNG sont à plat dans `images/` pour être inclus dans le script de preuve actuel. Le rapport conserve les SHA-256 de chaque image et le rejeu les contrôle.

**Statut : code expérimental livré, exécution PC encore nécessaire.**
