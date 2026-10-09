# 79 — P2.12c : les vraies statistiques ET les images côte à côte

**CODE_PUBLISHED / PC_TEST_PENDING**. Sans changement de main.

## Pourquoi
Un compteur de tests PASS ne décrit pas la qualité des images. Le benchmark garde une politique de décalage P2.12b figée, applique la même procédure sur plusieurs cibles TEST de nature contradictoire, et produit un **PNG comparatif** avec trois colonnes : cible / dessin initial / dessin corrigé. Il génère également `scores.csv` et `summary.json`. Les images originales `caseN/baseline.png`, `caseN/frozen-policy.png` et empreintes restent consultables.

## Indicateurs
`cases`, `improved`, `worsened`, `ties`, `mean_delta` (erreur corrigée moins erreur initiale; négatif = mieux), `mean_baseline_error`, `mean_corrected_error` et score individuel. Il ne s'agit pas d'une métrique perceptuelle avancée : comparaison brute des pixels. La correction n'est **pas réapprise** à partir du TEST. Les changements de scène/contextes complexes ne sont pas prouvés.

## Validation
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_p212c*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests P2.12c échoués" }
```

## Utilisation
Un manifeste TEST fixé avant la génération :
```json
{"schema":"BRODY_P212C_CASES_V0","cases":[
 {"layout":"build/layout1.json","reference":"build/target1.png","label":"decalage identique"},
 {"layout":"build/layout2.json","reference":"build/target2.png","label":"pas de decalage"},
 {"layout":"build/layout3.json","reference":"build/target3.png","label":"decalage inverse"}
]}
```
Puis :
```powershell
py -m brody_world_physique.p212c_mixed_visual_benchmark_v0 --memory "build\p211b-gestures.json" --policy "build\policy-p212b.json" --manifest "build\manifest-p212c.json" --out "build\p212c-examen-001"
```
Ouvrir `build\p212c-examen-001\comparison.png` pour voir le résultat réel et `summary.json` pour les chiffres. Les références peuvent être des dessins synthétiques ou des images utilisateur adaptées à la taille SIDE, mais jamais des cibles déjà vues pendant TRAIN.

## Grille du projet (tests PC connus au 09/10)
P2.11a 3/3, b 4/4, c 4/4, d 4/4, e 3/3, P2.12a 3/3, b 4/4 : **25/25 tests ciblés PASS**. P2.12c en attente. Les 2 dégradations P2.11d ont été diagnostiquées comme cibles incompatibles avec les consignes; P2.12b a 1 cas de transfert synthétique amélioré. Aucun score global de fidélité ni pourcentage de réalisation de la vision n'est encore justifié.

Après P2.12c : corriger les régressions **sur TRAIN seulement**, ajouter des moteurs témoins de qualité similaire, intégrer vraiment les vues décomposées/Reverso/multi-échelle, et tester en aveugle sur un lot d'images variées.
