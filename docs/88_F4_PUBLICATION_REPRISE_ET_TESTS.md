# 88 — F4, reprise de publication : journal éducatif F3c vérifié

**Branche :** exp/p2-multirepresentation-ablation-20261009. **Statut : CODE PUBLIÉ, TESTS PC NON ENCORE EXÉCUTÉS.** Ne pas modifier main.

## Pourquoi cette publication
Le premier essai F4 avait échoué lors de l'écriture GitHub. Les fichiers F4 n'avaient pas été publiés. Cette reprise est distincte : elle est maintenant associée à un commit vérifiable.

## Ce qui a été branché
`fusion_f4_education_journal_v0.py` réutilise explicitement `fusion_f3c_cumulative_skill_archive_v0.teach`, `.exam` et `.load_registry`. Il n'introduit PAS un autre extracteur de gestes. La seule nouveauté est un **journal de reçus des expériences candidates**, numérotées, chaînées par empreintes et contrôlées avant ajout. Deux types séparent le TRAIN qui produit une compétence candidate et le TEST tenu à l'écart qui note un dessin déjà scellé.

`teach_recorded` : entraîne une compétence candidate et émet un reçu `TRAIN_CANDIDATE` lié à la version du registre. `test_recorded` : exige un épisode TRAIN précédent, utilise la mémoire figée et consigne le score dans un reçu `HELD_OUT_TEST`. `readonly_context` : expose une vue de la progression au consommateur sans accorder de modification.

## Ce qui reste manquant (ne pas lisser)
Cette couche est un **journal expérimental local** ; elle n'est PAS l'index `experience_memory_v1` et ne se substitue PAS au `Native Memory` d'Obsidia. Elle ne fait pas encore d'admission MEMZUM, de validation humaine ni de promotion canonique. Elle ne réalise pas l'éducation préverbale, l'identification d'objets, la mise à jour de la compétence après correction, l'apprentissage inter-domaines ou la fusion V4.1/V4.2. Les champs d'un événement TEST ne servent jamais à apprendre une compétence.

Un échec après la création d'un fichier conserve ses traces ; la reprise doit utiliser un autre dossier. Tous les essais se déroulent en sandbox locale, `native_memory_write=false`, `canonical_promotion=false`, `KX108_ONLY`.

## Validation Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_fusion_f4*.py" -v
if ($LASTEXITCODE -ne 0) { throw "F4 échoué" }
py -m unittest discover -s tests -p "test_fusion_f3c*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Régression F3c" }
```

Après PASS de ces tests ciblés, rejouer le contrôleur complet 15 suites avec un nouveau chemin de sortie si nécessaire :
```powershell
py -m brody_world_physique.fusion_f2_school_regression_v0 --repo . --out "build\fusion-f4-regression-001"
```

**ATTENTION :** les 15 suites sont celles du manifeste F2 actuel. Elles ne contiennent pas automatiquement F3c/F4 ; les tests F3c/F4 ci-dessus restent obligatoires.

## Prochain palier
Réconcilier les reçus expérimentaux avec `experience_memory_v1` et le read-only de M4D4 Native Memory **sans coupler un writer cognitif**. Ajouter sélection contextuelle non souveraine des compétences, nouvelles versions correctives uniquement sur TRAIN, tests HOLD/negative transfer, composition multi-formes V4.1/V4.2 et observation réelle. Ne pas annoncer l'intégration complète avant qu'une preuve E2E existe.
