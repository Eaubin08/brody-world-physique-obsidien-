# 92 — F1F : enrichir l'observation avant de prédire

## Portée
Réutilise le moteur de prévision existant et le détecteur de pixels pour démontrer un **apprentissage conditionné par un indice observable dans l'image passée**. Ce laboratoire ne prétend pas réutiliser P149/P150/P152 : leurs fichiers exacts et leurs contrats d'API n'ont pas encore été localisés/confirmés dans cette passe.

## Construction
Deux contextes de formation synthétiques : sans indice et avec une ligne bleue visible dans la dernière image, installée avant la prédiction. Chaque contexte a deux retours de professeur. Le moteur apprend un résidu de position par contexte et écrit une compétence scellée à autorité limitée. Les tests nouveaux comportent :
1. Prolongement régulier sans indice.
2. Changement de trajectoire avec indice.
3. Faux indice sans changement de trajectoire (contrôle négatif).
4. Inversion cachée sans indice (contrôle de non-identifiabilité).

Les fichiers de prédiction et de proposition candidate sont enregistrés avant de révéler la cinquième image. Les erreurs et les régressions sont consignées, sans cacher les échecs. Le marquage bleu est **un indice synthétique corrélé à l'expérience**, pas une simulation fiable d'obstacle ou de collision; même sa présence ne prouve pas la suite du mouvement.

## Interprétation
La démarche teste si une observation *supplémentaire* permet l'apprentissage d'une règle conditionnelle; elle ne démontre ni causalité physique, ni compréhension visuelle générale, ni adaptation autonome du choix de capteur. Le succès est évalué avec les deux contrôles négatifs pour montrer les conditions d'applicabilité.

## Autres représentations à raccorder après audit réel
- P149 : contre-factuels temporels, histories concurrentes, non-identifiabilité.
- P150 : référence caméra et mouvement apparent distincts.
- P152 : hypothèses concurrentes d'association/identité.
- Indices supplémentaires testables ensuite : contexte de scène, contours d'obstacles, occultation, point de vue, éclairage, profondeur, RF/CSI, acoustique, température. Aucune de ces sources n'est présentée comme déjà branchée.
- Composants réciproques : VisualFingerprint, LOCK/FLEX/IGNORE, OS Trad/Reverse OS, MMonde/F12, historique et dépendances de compétences, progression E0–E7.

## PC PowerShell
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_observed_cue_education_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "TEST_FAILED" }
py -m brody_world_physique.observed_cue_education_v1 --out "build/f1f-observed-cue-v1"
if ($LASTEXITCODE -ne 0) { throw "RUN_FAILED" }
Get-Content "build/f1f-observed-cue-v1/MASTER_REPORT.json"
```
Le dossier de sortie doit être inexistant. `KX108_ONLY`; `NATIVE_MEMORY_WRITE=FALSE`; `CANONICAL_PROMOTION=FALSE`. PC run non confirmé.
