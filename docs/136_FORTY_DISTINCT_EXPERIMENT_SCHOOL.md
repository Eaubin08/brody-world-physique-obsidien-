# Brody — P136 : école transversale, 40 questions falsifiables

## Pourquoi ce changement

Ne plus proposer deux tests puis considérer une capacité comme acquise. La passe fournit un point d'entrée unique pour **40 questions de vérification distinctes** (et non 40 tirages d'une trajectoire), regroupées en **8 familles**. Le programme exécute 35 sondes sur les briques réellement disponibles et marque 5 capacités comme **TODO**. Les sondes ne sont pas toutes des entraînements et certaines restent très élémentaires ; le compteur n'est pas une preuve d'intelligence ou d'apprentissage généralisé.

## Huit familles couvertes

- Vision : composantes, différences RGB, structure en niveaux de gris, évolution du nombre d'objets, disposition.
- Géométrie : miroir, appariement par silhouette, propriétés d'aire/proportions, refus de déduire la profondeur.
- Génération : rectangles, ellipses, triangles, composition colorée, limites spatiales.
- Éducation : dédoublonnage, contradiction pédagogique, mémoire de forme à deux origines déclarées, doute si preuves insuffisantes, refus forme inconnue.
- Mémoire : associations de scènes, source unique versus multisource, composition de masques, symbole inconnu et empreinte d'intégrité.
- Mouvement : inversion, arrêt, départ, accélération apparente, non-attribution de causalité.
- Robustesse : empreintes, fichier rendu non vide, dépassement interdit, forme inconnue, distinction de groupes.
- Frontières TODO : véritable 360° 3D, physique terrain indépendante, découverte sémantique autonome, reconstruction d'occlusion réelle, exploration externe autonome.

Les intitulés ne doivent pas masquer leurs limites : l'appariement actuellement utilisé n'établit **pas** l'identité physique, les groupes déclarés ne garantissent pas indépendance réelle, et les modes de génération restent des prototypes 2D sur fonds simples.

## Exécuter toute la campagne en une fois sur PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_forty_distinct_school_p136.py" -v
if ($LASTEXITCODE -ne 0) { throw "Validation P136 échouée" }
py -m brody_world_physique.image_forty_distinct_school_p136 --out "build\brody-school-p136-run001"
if ($LASTEXITCODE -ne 0) { throw "École P136 échouée" }
Get-Content "build\brody-school-p136-run001\MASTER_REPORT.json"
```

`EVIDENCE.json` : une entrée par protocole, avec verdict individualisé. `MASTER_REPORT.json` : familles, nombre PASS/FAIL/HOLD/TODO et limites. Les images de travail sont sous `assets/`.

Le dossier de sortie est protégé contre l'écrasement. Utiliser un nouveau suffixe `run002` au besoin.

## Condition de validation

On n'annonce pas 35/35 sans exécution sur le PC. Si une sonde échoue, il faut corriger son mécanisme ou consigner son échec, sans transformer une approximation en preuve. Les 5 TODO restent fermés. Avant tout avis sur l'apprentissage, il faut une campagne avec données réelles issues de sources indépendantes, comparaison A/B de la mémoire et corrections différées.

## Plan de continuation substantiel

1. École d'images issues de sources authentifiées et adaptées au matériel local ; provenance et licences, cas hors distribution et contre-exemples.
2. Segmentation couleur multiobjet incluant chevauchement et occlusion ; mesure de séparation de vrais objets.
3. Génération apprise d'arrangements nouveaux sans segmentation de la cible, puis examen réellement aveugle.
4. Vues indépendantes 3D/360° avec relation réciproque perception ↔ génération ; ne pas confondre rotation 2D et vraie vue 3D.
5. Savoir des interactions physiques par expériences et continuité temporelle.
6. Connaissance consolidée, transfert analogique, rétention, détection de contradiction et suivi des corrections.

**Autorité** : branche expérimentale ; pas de modification `main` ; `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
