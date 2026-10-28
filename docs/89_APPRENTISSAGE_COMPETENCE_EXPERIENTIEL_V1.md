# 89 — Apprentissage de compétence par expérience (candidat expérimental)

Ce développement répond au défaut mesuré dans F1B/F1C et Integrated Education V0 : une mémoire consultée sans modification observable de la prédiction.

## Mécanisme
L'expérience débute avec une prédiction *scellée* du moteur existant. Après une observation de correction TRAIN, elle mesure le vecteur d'écart (dx,dy). Des corrections de même régime alimentent une **compétence candidate** distincte, scellée et retrouvable sur disque. À l'examen, une nouvelle scène est prédite, puis une correction moyenne est appliquée uniquement si ses préconditions de contexte sont remplies. Les deux prévisions et le PNG candidat sont enregistrés avant la révélation de la vérité TEST. Le rapport conserve les gains ET pertes.

Une troisième leçon de mouvement différent est enseignée entre la correction et l'examen, pour tester la rétention élémentaire du candidat. Le mécanisme ne modifie pas les paramètres du moteur de mouvement, ni Native Memory, ni les décisions KX108.

## Fidélité aux concepts
- **Expérience distincte de connaissance** : chaque correction demeure candidate.
- **Friction** : le résidu numérique vient de l'écart entre prédiction et observation, pas d'une règle physique injectée.
- **Mémoire de compétences** : préconditions, dépendances, provenance SHA256, état immuable.
- **Rétention / transfert** : leçons séparées et TEST inédit scellé; positive/negative transfer comptabilisés.
- **LOCK/FLEX/IGNORE et Reverse 360** : les contrats restent à raccorder véritablement, sans affirmation de réalisation complète.
- **Multicouche** : les frontières SENS/MMonde/OS Trad et P156 demeurent non raccordées.

## Limites
La compétence créée est un estimateur supervisé très simple d'un biais résiduel dans un contexte 2D. Elle n'est pas une loi physique inventée par Brody, ni un algorithme auto-découvert. Les scènes sont artificielles; le laboratoire ne constitue pas une validation sur images réelles. Le jeu de test est encore petit, et certaines séquences restent imprévisibles au moment de la prédiction. Ce test est un jalon de boucle d'apprentissage, pas une fermeture du programme E0–E7.

## Test local
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_experiential_skill_learning_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.experiential_skill_learning_v1 --out "build/experiential-skill-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/experiential-skill-v1/MASTER_REPORT.json"
```
Sortie non destructive uniquement sur un dossier inexistant.

## Garde
`NATIVE_MEMORY_WRITE=FALSE`
`CANONICAL_PROMOTION=FALSE`
`DECISION_AUTHORITY=KX108_ONLY`
`FULL_EDUCATION_E2E=NOT_PROVEN`
