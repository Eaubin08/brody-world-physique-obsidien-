# Boucle enseignement visuel → savoir procédural local → sauvegarde durant le run

Le module `image_visual_reflex_teacher_loop_v1.py` raccorde des références image 64x64 au registre de savoirs stabilisés. Un contexte perceptif rudimentaire (`flat`, `dark-dense`, `drawing`) sert d'index. Si un savoir est déjà STABLE, sa procédure est choisie directement ; sinon Brody hésite localement entre au plus trois stratégies, confronte leur dessin à l'image de référence, puis ajoute un exemple de cours `pixel-feedback-simulated`. Ce « professeur » automatique n'est **pas** un enseignant humain authentifié. Il n'apprend pas l'identité des objets et n'infère pas la physique.

Chaque leçon produit un reçu avec empreinte de source et de dessin, puis un `checkpoint.json` écrit atomiquement après synchronisation du reçu. Une interruption contrôlée après un checkpoint permet de relancer **la même commande** avec le même `--out` : les reçus et le digest du checkpoint sont vérifiés avant reprise au prochain exemple. Une coupure entre reçu et checkpoint déclenche un refus de reprise, sans promettre un rejeu automatique. La sortie inclut `knowledge_candidates_snapshot.json` expérimental et `MASTER_REPORT.json`. Ce snapshot n'est pas le fichier natif `knowledge_candidates.json` du moteur documentaire V1 ; l'option `--previous` de ce module attend actuellement le format de ce dernier. Ne pas fournir le snapshot à `--previous` tant qu'un adaptateur de format n'a pas été validé. **La reprise garantie par cette version concerne un run interrompu dans le même dossier.**

Les dossiers `build` restent locaux, sans synchronisation GitHub. Aucun droit d'écriture Native Memory / kernel / promotion canonique n'est accordé. Les anciens scores et expériences ne sont ni effacés ni remplacés. Les tests doivent être exécutés sur Windows avant de prétendre que la campagne est validée.

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_visual_reflex_teacher_loop_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
py -m brody_world_physique.image_visual_reflex_teacher_loop_v1 --images "build\brody-images-ready" --out "build\brody-visual-reflex-loop-001" --limit 63
if ($LASTEXITCODE -ne 0) { throw "Boucle échouée" }
Get-Content "build\brody-visual-reflex-loop-001\MASTER_REPORT.json"
```

Travail restant : provenance vérifiée des professeurs et cours ; contextes hiérarchiques objets/parties/angles/couleurs ; transfert entre images et cycles ; adaptation des exemples aux lacunes ; restauration transactionnelle après coupure au milieu d'une écriture ; liaison du snapshot de fin de cycle avec le prochain cycle ; compréhension du monde et apprentissage multisensoriel. Les preuves de stabilisation de procédure ne suffisent pas à valider ces capacités.
