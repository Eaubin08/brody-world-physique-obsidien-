# École Image — transfert inter-épisodes et examen aveugle

Ce module prolonge les campagnes précédentes sans les relancer. Il charge le snapshot de 10 000 leçons, effectue **10 000 épisodes supervisés supplémentaires**, accumule des compétences *candidates locales*, fige l'état, puis réalise **10 000 examens sans apprentissage**, avec scènes et graines différentes. La référence de test est ouverte seulement après scellement de la réponse initiale. Les scores avant/après sont calculés sur les **mêmes scènes de test** pour éliminer une comparaison entre jeux différents.

Familles conservées : géométrie inédite, translation, miroir, rotation, contraste, flou, bruit synthétique, masquage, intention trompeuse, intention inconnue. Métriques : erreur initiale témoin, erreur avec mémoire candidate, amélioration, régression, abstention. Le banc accepte que le progrès soit absent ou négatif ; aucune réussite n'est codée en dur.

**Frontière critique** : le modèle reçoit l'étiquette expérimentale `family` comme indice dans sa clé d'apprentissage, et les données sont générées par le même moteur synthétique de rendu. La correction sur `wrong_intent` exploite ce contexte; elle ne prouve donc PAS qu'un système visuel détecte seul une consigne fausse. La persistance ici est locale et candidate, sans écriture Native Memory. Aucun nouveau domaine ni action canonique Obsidia. Pas de perception visuelle autonome générale ni de physique réelle prouvée.

## Une commande PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_persistent_transfer_exam_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
py -m brody_world_physique.image_persistent_transfer_exam_v0 --snapshot "build\brody-image-school-20k-001\training\snapshot-010000.json" --train 10000 --exam 10000 --out "build\brody-image-transfer-20k-001"
if ($LASTEXITCODE -ne 0) { throw "Examen transfert échoué" }
Get-Content "build\brody-image-transfer-20k-001\MASTER_REPORT.json"
```

Ne pas réutiliser le même dossier d'output, pour conserver les preuves passées. Une ablation indispensable après ce test est la suppression de `family` du contexte : sans elle, le transfert observé reste conditionné à un indice construit par le banc.
