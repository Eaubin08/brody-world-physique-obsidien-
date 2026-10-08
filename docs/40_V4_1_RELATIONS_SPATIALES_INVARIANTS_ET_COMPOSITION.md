# 40 — Brody Image V4.1 : observer des parties, proposer des relations, reconstruire

**Date : 2026-10-09.** **Statut : première classe expérimentale locale, non canonique.**  
**Auteur de l'intention :** l'utilisateur (monde + apprentissage + SENS), dans la suite des dessins V1–V3 et du pont MMonde V4.  
**Outils concrets :** [`world_relations_school_v4_1.py`](../brody_world_physique/world_relations_school_v4_1.py), [tests V4.1](../tests/test_world_relations_school_v4_1.py).

## Pourquoi ce nouveau cours, au lieu d'une nouvelle mémoire autonome ?

Le [pont V4](39_BRODY_MONDE_EXPERIENCE_V4_BRIDGE.md) exposait bien des objets candidats, des transformations et des preuves. Mais pour la maison il **déduisait l'association « toit au-dessus de la base » des coordonnées transmises par le professeur**. On ne peut pas attribuer cette relation à une observation de Brody.

V4.1 supprime ce raccourci pour **une première relation quantitative bornée** : l'élève reçoit uniquement des images 64×64 et extrait, directement depuis les pixels, les composants et leur séparation normalisée. Le professeur fournit une consigne de classification `NEAR` ou `FAR` **après l'observation pendant les leçons**. Le système apprend un seuil de séparation **à partir de leurs résultats**, puis classe des images nouvelles avant de recevoir les étiquettes de test.

Cette réduction est volontaire : **proximité entre deux composants ≠ compréhension de la maison / « toit » / identité / causalité**. Il est plus utile de tester une vraie petite compétence bornée que de coder d'avance une relation riche puis de l'appeler apprentissage.

## Propriété et frontières des autres chantiers

- **MMonde** ([contrat upstream](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-mmonde-v0/periphery/mmonde/contracts_v0.py)) : observations et états du monde, **world state != memory**. V4.1 reste un candidat expérimental lié au V4, pas un `WorldStateV0` canonique.
- **F12** ([dynamique située](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-situated-world-dynamics-v0/periphery/world_dynamics/contracts_v0.py)) : trajectoires, continuité, repères, transformations et distinctions épistémiques. La classe teste uniquement des invariants géométriques simples, **pas** une loi physique ni la continuité d'un même objet dans une vidéo.
- **F16** ([contrat vision](https://github.com/Eaubin08/obsidia-x108-proofs/blob/feat/premiere-mise-au-monde-vision-real-image-v0/periphery/vision/contracts_v0.py)) : `RealImageObservationV0` n'est pas utilisé ; les images sont **SIMULATED** et générées avec Pillow.
- **SENS** ([branche sémantique expérimentale](https://github.com/Eaubin08/obsidia-x108-proofs/tree/exp/semantic-grammar-cognitive-lattice-v0)) : aucun `EventRef`, `OccurrenceClaim`, pipeline de promotion B8 ou classe D n'est importé ou exécuté. Aucun sens d'objet n'est validé.
- **GPS** ([état de navigation](https://github.com/Eaubin08/obsidia-gps-defense-/blob/native-builder-trusted-navigation-v1/server/navigation/trusted-state-ledger.mjs)) : inspiration **uniquement** sur la traçabilité et la continuité des preuves ; pas de nouvelle dépendance GPS.
- **Native Memory** : pas d'écriture, pas de promotion, pas de second gestionnaire canonique. Les observations sont un **registre candidat local**.

La pause de SENS au checkpoint B8/09d4fe74 local est respectée ; **aucune branche SENS ou GPS n'est modifiée par ce développement**.

## Cours V4.1 — observations sans boîtes fournies

```text
Images de deux formes disjointes produites par le professeur
                ↓
ÉLÈVE : pixels seulement (pas de boite / pas de nom de forme)
                ↓
Extraction générique des composantes connexes (8 voisins)
                ↓
Centre, aire, boîte DÉDUITE de la segmentation, signature
                ↓
Distance normalisée par racines des aires
                ↓
6 expériences guidées (proches / éloignées)
                ↓
Seuil empirique appris à partir des retours du professeur
                ↓
Décisions sur images de TEST enregistrées AVANT les étiquettes
                ↓
Comparer aux tests de translation / taille / quart de tour /
réarrangement contradictoire / observation non prise en charge
                ↓
Mémoire candidate + erreurs + sources + code SHA + vérification
```

Le logiciel ne reçoit pas les boîtes professorales dans `inspect_pixels(image)`. Il **calcule néanmoins ses propres boîtes à partir des pixels**, ce qui est un instrument de vision programmé. L'algorithme de composantes connexes et la définition de distance normalisée sont des choix d'ingénierie : la compétence qui s'adapte est le **seuil de distinction des groupes proches ou éloignés**, pas l'invention de la segmentation.

**Domaine strict :** images binaires, deux composants disjoints, noirs sur blanc, 64×64 ; `HOLD` si le nombre de parties diffère. La méthode n'a ni sens sémantique, ni profondeur, ni calibration probabiliste, ni reconnaissance d'objet réel.

### Transformations

La translation change les coordonnées sur la page, pas les aires ou l'écart des centres ; une rotation de 90° conserve la distance euclidienne ; le redimensionnement approximatif change peu la distance **normalisée**. Ces invariances géométriques sont **codées**, et on mesure seulement si le seuil appris reste exploitable après ces transformations.

**Ne pas confondre avec une compréhension des relations directionnelles.** Une rotation transforme « au-dessus » en « à côté ». Notre critère de proximité ne porte pas l'information de dessus/dessous : une image avec les mêmes parties inversées peut être classée comme une relation connue. Ce cas adversarial est conservé comme **échec explicite**, afin de savoir ce qu'il manque au prochain jalon.

## Résultats observés (CI Linux / Windows)

[Run 37854023079](https://github.com/Eaubin08/brody-world-physique-obsidien-/actions/runs/37854023079) : **170 tests Python PASS** sur Linux 3.11/3.12 et Windows 3.14 ; le simulateur V4.1 a exécuté six leçons et six examens, puis vérifié intégralement les artefacts.

| Examen | Verdict comparé à l'étiquette révélée |
|---|---|
| Relation proche translatée | Correct |
| Relation proche tournée de 90° | Correct |
| Relation proche agrandie | Correct |
| Relation éloignée translatée | Correct |
| Relation avec un seul composant | `HOLD` correct |
| **Même proximité, composants dans l'ordre inversé** | **ÉCHEC (faux positif)** |

Soit **5 / 6** classements ou abstentions corrects, avec un échec adversarial conservé **dans le rapport**. Cela invalide toute conclusion du type « compréhension complète d'une relation spatiale orientée ». La réutilisation de pixels mémorisés a produit une image avec **262 pixels d'erreur binaire**, meilleure qu'une page blanche contre la variante cible, sans être un dessin exact. Les mesures restent internes à un simulateur 2D ; **ni identité, ni sens, ni invariance 360° générale, ni transfert au monde physique ne sont démontrés**.

Les tests ont notamment contrôlé la séparation non étiquetée des composants, le comportement sous translation/rotation 90°/échelle, le refus `HOLD`, la résistance aux falsifications des images et à une fausse promotion de connaissance, l'ordre des décisions enregistrées et la lecture seule de V3/V4.

## Composition nouvelle sans boîtes de test

La dernière expérience n'envoie **aucune position de composant au module élève**. Elle lui demande de reproduire un assemblage proche depuis sa mémoire candidate de composants et de leur placement observé. L'élève conserve les pixels des petites formes source et leur disposition mesurée. Il recentre sa production sur le canevas 64×64 et écrit `composition_before_reveal.json` avec le SHA de l'image et la procédure.

**Seulement ensuite** le professeur révèle une nouvelle variante synthétique, créée avec d'autres taille/position. On compare le dessin produit avec cette référence et une page blanche.

Il s'agit d'une **recomposition de pixels mémorisés**, pas d'une conception spontanée d'objet. Ce protocole ne certifie pas que Brody connaît la définition d'une maison ou sait résoudre une scène réelle.

## Mesures et preuves

Sorties de `--out` :

- `images/train_*.png` : six exemples de cours, utilisés avec leurs étiquettes de retour ;
- `world_relation_memory_candidate.json` : pixels des composants, géométrie mesurée, étiquettes de cours, seuil appris et SHA du V4 source ;
- `choices_before_teacher_feedback.jsonl` : six décisions sans vérité de test ;
- `images/exam_*.png` : images de test déplacées, redimensionnées, tournées, éloignées, inversées ou non prises en charge ;
- `images/composition_candidate.png` : la proposition de l'élève sans référence de test ;
- `composition_before_reveal.json` : choix et SHA scellés avant révélation ;
- `images/composition_teacher_revealed.png` : référence révélée et évaluée après la proposition ;
- `evaluation.json` : réussites/échecs réels, scores de composition, code/provenance, frontières de savoir.

`--verify` relit l'intégralité de V3+V4, regénère les exemples professeur à partir de la source du test, recalcule les composants, la classification, toutes les images de l'élève et compare les empreintes des archives. Il **ne prouve pas une date externe d'engagement** : tout fonctionne encore dans un même processus et le scénario reste synthétique. Les SHA-256 locaux ne sont pas une signature externe infalsifiable.

## Commandes PowerShell sur le PC

Depuis `C:\Users\Aubin\Desktop\OBSIDIA_WORLDS\brody-world-physique-image` :

```powershell
git pull --ff-only origin main

$v3 = "build\dessin-memoire-v3-20261009-000320"
$v4 = "build\monde-brody-v4-20261009-002625.json"
$out = "build\relations-v4-1-$(Get-Date -Format yyyyMMdd-HHmmss)"

py -m brody_world_physique.world_relations_school_v4_1 --prior-v3 $v3 --prior-v4 $v4 --out $out
if ($LASTEXITCODE -ne 0) { throw "Cours V4.1 échoué" }

py -m brody_world_physique.world_relations_school_v4_1 --prior-v3 $v3 --prior-v4 $v4 --verify $out
if ($LASTEXITCODE -ne 0) { throw "V4.1 : rejeu incohérent" }

Invoke-Item "$out\images"
notepad "$out\evaluation.json"
```

Si `--verify` refuse de relire un ancien V3 à cause d'un changement de code épinglé, il ne faut pas modifier les preuves, mais recréer un nouveau run de référence.

## Décision pour la V4.2

Tester explicitement la **relation orientée et la structure**, pas seulement la distance : inférer une disposition relative dans un repère qui peut tourner, distinguer deux parties identiques mais inversées, gérer l'occlusion et l'ambiguïté, puis confronter des objets inconnus hors simulateur. Ne pas attribuer le succès d'une heuristique d'image binaire à une compréhension générale du monde.
