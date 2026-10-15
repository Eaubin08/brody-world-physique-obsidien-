# École Image — référence visible contre contradiction non observable (10 000 cas)

## Expérience intégrée
La version précédente de Brody retenait les bonnes corrections grâce à une indication cachée de la famille de perturbation. L'ablation sans cet indice a révélé 94 régressions sur les consignes trompeuses. La présente campagne examine la frontière d'information qui manquait : un référent visuel effectivement accessible **avant** décision, ou son absence.

Chaque scène contient un choix entre les trois outils de dessin simulés. L'évaluateur prépare une référence, parfois contradictoire avec le style annoncé. La moitié des cas la révèle, la moitié la garde inaccessible. Ni le mot « trompeur », ni l'outil correct ne sont transmis au choix.

- Référence visible : le comparateur de pixels juge les trois rendus candidats disponibles et sélectionne un outil uniquement si l'écart est suffisamment faible ; sinon HOLD.
- Référence cachée : HOLD, qu'il y ait réellement tromperie ou non, car il n'existe aucune preuve pour trancher.
- Reçus chaînés, métriques séparées en quatre groupes visible/caché × consigne trompeuse/véridique.
- Aucune écriture Native Memory, aucune autorité, pas de modification du noyau ni de main.

**Ce que cela ne prouve pas :** le comparateur effectue une recherche exhaustive entre trois rendus issus **du même simulateur** que la cible. Il ne s'agit pas d'une perception sémantique, d'un modèle physique, ni d'un apprentissage inter-épisodes. Un bon score visible sera donc un contrôle de disponibilité de la preuve et de choix instrumental, pas une compréhension autonome du monde. Une contradiction cachée est indétectable par définition avec ces seuls inputs.

## Lancer 10 000 cas sur PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_visible_reference_abstention_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
py -m brody_world_physique.image_visible_reference_abstention_v0 --cases 10000 --out "build\brody-image-visible-vs-hidden-10k-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne échouée" }
Get-Content "build\brody-image-visible-vs-hidden-10k-001\MASTER_REPORT.json"
```

## Prochaine jonction dans le même projet
Pour un vrai test de compréhension visuelle : obtenir des images de référence d'origine indépendante, empêcher le comparateur d'énumérer le même générateur que l'examinateur, détecter objets/propriétés visuelles sans exposer la correction puis mesurer la différence et la généralisation. Ne pas annoncer ces fonctions comme implémentées par ce banc.
