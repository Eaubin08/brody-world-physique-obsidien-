# École des savoirs stabilisés — prototype procédural V1

Nouvel organe expérimental séparé du moteur de scores (qui reste archivé pour comparaison). L'enseignement est un événement explicite : contexte, méthode/procédure, référence du professeur, référence unique de l'exemple, éventuelle correction. Après trois exemples concordants distincts, le savoir procédural local est marqué STABLE ; une situation connue applique directement la procédure sans reclassement des scores. Une contradiction rouvre **le seul contexte concerné**. Pour un contexte incertain, l'appelant fournit des contextes apparentés et le moteur retourne au maximum trois méthodes candidates.

La vérité stabilisée signifie « acquis opérationnel sous ces conditions », non vérité générale ou physique. Les références `teacher_ref` sont déclaratives et **non authentifiées**. Trois exemples cohérents ne prouvent pas à eux seuls la qualité du professeur. Il n'y a ici ni moteur d'inférence géométrique, ni exploration internet, ni apprentissage des objets à partir des pixels, ni génération d'images indépendante ; il s'agit du socle procédural à raccorder aux écoles visuelles existantes. Pas d'écriture Native Memory, de modification du kernel ou de promotion canonique.

## Démonstration Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_stabilized_knowledge_school_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
@'
[
 {"context":"trait-observe/contraste-normal","procedure":"raw","teacher_ref":"prof-demo","example_ref":"cours-1"},
 {"context":"trait-observe/contraste-normal","procedure":"raw","teacher_ref":"prof-demo","example_ref":"cours-2"},
 {"context":"trait-observe/contraste-normal","procedure":"raw","teacher_ref":"prof-demo","example_ref":"cours-3"}
]
'@ | Set-Content -Encoding UTF8 "build\brody-lessons-demo.json"
py -m brody_world_physique.image_stabilized_knowledge_school_v1 --lessons "build\brody-lessons-demo.json" --out "build\brody-knowledge-demo-001"
Get-Content "build\brody-knowledge-demo-001\MASTER_REPORT.json"
```

**Note Windows :** le JSON écrit avec `Set-Content -Encoding UTF8` peut porter un BOM selon PowerShell 5.1 ; si le chargement échoue, remplacer par `[System.IO.File]::WriteAllText(...,[System.Text.UTF8Encoding]::new($false))`.

La suite n'est pas plus de tests de moyenne : raccordement de ces concepts aux images, relations, parties d'objets, invariants, transformations 360°, boucle du professeur/correction et examens de transfert sans oublier le savoir stabilisé.

## Mémoire pendant le run, sauvegarde et reprise — état réellement implémenté

**Mémoire de travail (RAM).** Pendant l'appel à `run()`, les événements d'enseignement modifient l'objet local `state` : contextes, procédures, exemples, contradictions, exceptions et états `LEARNING` / `STABLE` / `DOUBT`. Le savoir reconnu `STABLE` est appliqué directement par `apply()`, sans classement permanent de scores. Une contradiction ne rouvre que le contexte concerné. Il s'agit du registre procédural **expérimental** de Brody, non d'une connaissance universellement vérifiée.

**Écriture pendant l'exécution.** Le moteur produit progressivement `receipts.jsonl` (événements chaînés) dans le nouveau dossier `--out`. Ces reçus servent de preuves, **pas** de sauvegarde de l'état `state` prêt à être rechargé. Le moteur ne relit pas automatiquement ce journal pour reconstruire un run interrompu.

**Sauvegarde en fin de run.** Une fois tous les cours traités et la chaîne des reçus vérifiée, `save()` écrit `knowledge_candidates.json` avec un `digest` d'intégrité, puis le moteur écrit `MASTER_REPORT.json`. Aucun checkpoint intermédiaire de `knowledge_candidates.json` n'est produit par la version actuelle. Une interruption avant la sauvegarde finale peut donc faire perdre les nouveaux acquis de ce run, même si des reçus partiels restent sur disque.

**Reprise entre runs.** Le run suivant peut utiliser `--previous <dossier-précédent>/knowledge_candidates.json`. `load()` vérifie le schéma, le digest et les interdictions d'écriture/promotion canonique avant de récupérer les contextes. La reprise est **explicite**, non automatique ; elle fonctionne seulement si le fichier d'état final existe et est intègre. Les dossiers de sortie existants sont refusés afin de préserver les preuves.

**GitHub / PC.** GitHub versionne les programmes, contrats, tests et documents. Les expériences et fichiers JSON produits sur le PC ne sont pas automatiquement envoyés à GitHub. La mémoire de travail n'est pas synchronisée entre PC par GitHub.

**Limite et suite exigée.** Prévoir des checkpoints transactionnels progressifs, une reprise après interruption par vérification/rejeu des reçus et la conservation des savoirs stabilisés sans confusion avec Native Memory. Un savoir local `STABLE` reste révisable sur correction contradictoire ; aucun résultat expérimental n'autorise sa promotion canonique. Les données de professeur (`teacher_ref`) ne sont actuellement pas authentifiées : la stabilité de procédure n'est pas une certification de vérité.
