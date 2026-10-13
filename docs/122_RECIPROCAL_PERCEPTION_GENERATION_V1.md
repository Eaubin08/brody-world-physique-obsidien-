# Brody — Passe réciprocité perception ↔ génération V1

## Objectif et périmètre réellement livré

Cette passe **construit des images à partir d'un savoir candidat appris**, et les confronte à de nouvelles images sans accès aux réponses du professeur. Elle ne reproduit pas directement les pixels source : `train` lit plusieurs images par identité enseignée, en extrait la grille RGB 4×4 déjà introduite à la V2, puis calcule pour chaque identité un prototype agrégé par cellule. `generate` décode ces 48 valeurs en une image RGB 64×64 composée de 16 blocs de couleur. `exam` traite des images non présentes en cours, produit jusqu'à trois hypothèses d'identité et génère depuis **le prototype mémorisé** de la proposition retenue. La reconstruction peut alors être examinée visuellement. Reçus chaînés et mémoire à digest ; mode refus pour octets déjà vus dans le cours. Aucun accès aux étiquettes de réponse dans `exam`.

**Limites à ne pas confondre :** ces sorties sont des prototypes mosaïques, pas des rendus réalistes, ni un dessinateur autonome, ni un modèle 3D ou une compréhension de gravité/mouvement. La distance couleur constitue une heuristique élémentaire et le choix CANDIDATE sans seuil de confiance calibré ne démontre pas une reconnaissance robuste. Deux photos de la même scène légèrement modifiées ne suffisent pas à démontrer l'indépendance réelle des expériences. Les leçons antérieures ne sont pas remplacées : c'est un organe supplémentaire à raccorder à l'école V1. Les identités restent déclaratives et non authentifiées. **Aucun accès à Native Memory, aucune promotion canonique ; KX108_ONLY.**

## Tests PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_reciprocal_generation_school_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

## Campagne concrète, avec photos nouvelles

Préparer un manifeste de cours `build\\brody-v2-lessons.json` : `[{"identity":"objet-A","examples":["C:\\photos\\A1.png","C:\\photos\\A2.png"]},{"identity":"objet-B","examples":["C:\\photos\\B1.png"]}]`. Ce sont des exemples de chemin, pas un jeu de données déjà disponible. Préparer le dossier `build\\brody-v2-exam-images` avec des photos nouvelles distinctes des cours.

```powershell
py -m brody_world_physique.image_reciprocal_generation_school_v1 --mode train --lessons "build\brody-v2-lessons.json" --out "build\brody-reciprocal-memory-001.json"
py -m brody_world_physique.image_reciprocal_generation_school_v1 --mode generate --memory "build\brody-reciprocal-memory-001.json" --out "build\brody-reciprocal-render-001"
py -m brody_world_physique.image_reciprocal_generation_school_v1 --mode exam --memory "build\brody-reciprocal-memory-001.json" --images "build\brody-v2-exam-images" --out "build\brody-reciprocal-exam-001"
```

Pour obtenir des résultats probants, comparer les mosaïques générées aux vraies photos et utiliser les réponses professeur séparées de l'examen. Il reste à construire un retour de correction persistent, un générateur conditionné par la géométrie des objets et pas seulement la couleur, un protocole de multi-vues 360 fondé sur des données variées, et les premières expériences temporelles d'objets tombants.

**Statut : expérimental ; publication GitHub ne prouve pas la réussite PC.**
