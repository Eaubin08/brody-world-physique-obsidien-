# 25 — Brody Image I1/R1 : premier prototype CPU exécutable

**Date :** 2026-10-08 · **Sur `main`** · **Portée strictement visuelle** · **Statut :** un outil réel d'édition **déterministe 2D**, pas un générateur neuronal, ni un moteur de compréhension physique.

## Ce qui est effectivement implémenté

Le module Python [`brody_world_physique/image_v0.py`](../brody_world_physique/image_v0.py) sait :

1. lire une image de référence réelle en PNG/JPEG **fournie par l'utilisateur** ;
2. **isoler** un sujet soit avec un masque de référence fourni (gris/alpha), soit avec une **couleur de fond uniforme connue** (chroma key simple) ;
3. **conserver les pixels RGB** du sujet dans un master PNG RGBA quand le masque est complètement opaque ;
4. **replacer** ce master à une position `x,y` dans une image de fond ; mise à l'échelle optionnelle avec interpolation ;
5. sauvegarder `cutout.png`, `composite.png`, `report.json` (empreintes SHA-256 source/fond/masque/sorties, contraintes, statut) ;
6. **vérifier la conservation RGB exacte** sur les seuls pixels **entièrement opaques**, **sans rescaling** et avec **source entièrement opaque**. Avec un changement de taille ou un alpha source partiel, cette métrique est `NOT_COMPARABLE`, jamais `PASS` artificiel ;
7. empêcher un masque manquant/ambigu, un sujet vide, un masque de mauvaise taille, une insertion hors cadre ou l'écrasement des fichiers sources.

**Aucune segmentation générale par IA.** Le fond vert explicite fonctionne sur décor uni seulement ; les objets verts pourraient être écartés du masque. Sur scènes complexes, **fournir un masque** ou attendre l'adaptateur de segmentation I1 réel. Ne pas qualifier cette méthode d'apprentissage.

**Aucune prétention de 3D, nouvelles vues, ombres physiques, mouvement/gravité, contrôle sémantique ou génération libre.** L'entrée peut être une photo réelle, mais l'artefact composite demeure **EDITED_COMPOSITE** — jamais `RealImageObservationV0`. Le reçu ne s'insère pas automatiquement en mémoire ni dans le noyau.

## Installation minimale

Depuis la racine du dépôt :

```sh
python -m pip install -r requirements-image.txt
python -m unittest discover -s tests -p "test_*.py" -v
```

**Essai avec de vrais fichiers utilisateur et un masque PNG** (blanc = conserver le sujet, noir = retirer le fond, gris = transparence partielle) :

```sh
python -m brody_world_physique.image_v0 --source photo.png --mask masque.png --background scene.png --x 80 --y 35 --out build/essai
```

**Essai avec un fond uniforme de couleur connue (rouge, vert, bleu 0–255)** :

```sh
python -m brody_world_physique.image_v0 --source photo_fond_vert.png --key-rgb 0,255,0 --tolerance 10 --background scene.png --x 80 --y 35 --out build/essai
```

Pour montrer qu'il existe de **vrais pixels édités par le code**, mais **pas** pour démontrer une vraie perception d'image naturelle, exécuter le **jeu de données synthétique** :

```sh
python -m examples.demo_image_v0 --out build/brody-image-demo
```

Le script écrit des entrées synthétiques, `result/cutout.png`, `result/composite.png`, `result/report.json` et `comparison.png` (avant / arrière-plan / assemblage). Les métadonnées marquent expressément qu'aucun modèle image n'est intervenu.

### Critères de réussite observables

| Cas | Verdict attendu |
|---|---|
| Masque connu, source pixel original non modifié, copie 1:1 | `PASS`, `rgb_mismatched_pixels=0` sur **pixels comparables** |
| Masque semi-transparent | Métrique limitée aux pixels opaques du masque, sans conclure sur les autres |
| Mise à l'échelle | `NOT_COMPARABLE` pour égalité stricte des pixels |
| Masque absent, mélange des deux méthodes, masque vide | Rejet explicite |
| Sujet déborde de la scène | Rejet explicite |
| Provenance et frontière de pouvoir | Entrées/sorties hashées, `KX108_ONLY`, aucune écriture mémoire et pas d'observation réelle fabriquée |

Les tests `tests/test_image_v0.py` sont distincts des contrats F0 existants. La GitHub Action est configurée pour **`push` sur `main` et PR** avec Python 3.11 et 3.12, installation explicite de Pillow, exécution de la démonstration et artefact téléchargeable limité à **7 jours** (si la CI réussit).

## Position dans la méthode d'origine

Correspondance avec [24 — Audit image](24_AUDIT_FIDELITE_BRODY_IMAGE_ET_SPEC_FONCTIONNELLE.md) :

- `IMG-01` **source/IN** : la commande et les fichiers d'entrée sont conservés avec SHA256 ;
- `IMG-02` **isoler** : masque connu ou chroma key déterministe, sans leurrer sur une vraie IA de segmentation ;
- `IMG-05` **tout objet** : aucun verrou artificiel spécialisé visage ;
- `IMG-07` **transport 2D** : transfert et placement mesuré ;
- `IMG-06` **reconstruction par réciproque** : **seulement un premier aller-retour pixel**, pas compréhension sémantique ou apprentissage ;
- `IMG-03` **peintre**, `IMG-04` **rigueur régionale évoluée**, `IMG-08` **Fibonacci/composition**, `IMG-09` **360°** et `IMG-10` **dynamique vidéo** : **PAS ENCORE IMPLÉMENTÉS**, à traiter séparément.

## Suite — dans l'ordre pour Brody Image

1. **I1 réel :** brancher un adaptateur de segmentation (poids/licence/GPU à vérifier) capable de proposer des masques sur **photos à arrière-plan complexe**. Garder un masque étalon pour l'évaluation.
2. **R1+ :** couche « peintre » non destructive : sous-couches, bords, détail, lumière, modes de rigueur par zone. Comparer sans prétendre que le protocole est toujours supérieur à une voie globale.
3. **G1 :** un `GeneratorAdapter` **réel** choisi en fonction du PC et de la licence des poids, donnant un **nouvel artefact image**, hash/seed/modèle/version et référence à `IN`.
4. **IG2 :** produire → ré-observer → mesurer invariants et erreurs → `ExperienceCandidate` ; replay avec sources indépendantes. **Aucune promotion automatique en Native Memory.**

**Décision d'intégration :** conserver ce module comme premier adaptateur R1 local réutilisable, pas comme remplacement des types F16, de Brody, de SENS ou du générateur futur.
