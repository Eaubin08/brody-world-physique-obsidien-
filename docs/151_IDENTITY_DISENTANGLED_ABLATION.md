# P151 — Permanence d'identité : isoler apparence, mouvement et association

## Motivation

P150 corrigée : erreur caméra 0,2323 pixel avec couverture 99 %, mais changement d'apparence 18,42 pixels d'erreur et superposition 0 % de couverture. Le scénario P150 `appearance_swap` associait un changement de couleur à une inversion de trajectoire ; les causes ne pouvaient donc pas être isolées scientifiquement.

## Contrôle expérimental

P151 sépare explicitement :

- `colour_only` : changement de couleur, vitesse conservée ;
- `motion_reverse_only` : vitesse inversée, couleur conservée ;
- `colour_and_reverse` : changements combinés ;
- `cross_equal`, `cross_color`, `overlap_equal` : association d'identités, apparences égales ou distinctes ;
- `occlude_short`, `occlude_long` : couverture et perte d'observabilité ;
- `camera_and_colour` : changement de couleur avec mouvement de caméra ;
- `distractor` : apparition d'une observation supplémentaire.

L'examinateur conserve deux identifiants cachés A et B ; les algorithmes n'en reçoivent aucun. L'identifiant A est *initialement le plus à gauche* ; ceci est une convention de mesure. Ils observent neuf images sur dix et prédisent la position d'A sur l'image suivante.

## Comparateurs

1. Association **par mouvement** : coût de distance entre position extrapolée et composantes visuelles.
2. Association **avec verrouillage de couleur** : même modèle, mais pénalité additionnelle si l'apparence change.

Les deux sont des baselines algorithmiques, non des modèles entraînés. Chaque scénario calcule couverture, erreur moyenne parmi réponses et **exactitude d'identité parmi réponses** : la prédiction doit être plus proche d'A que de B. C'est une mesure géométrique indirecte, pas une annotation explicite d'une identité dans chaque image. Les refus sont conservés.

## Limites

Les deux mobiles sont synthétiques, simples, très contrastés. L'algorithme conserve une seule association après chaque image et mesure une ambiguïté locale : **ce n'est pas encore un vrai filtrage multi-hypothèses à long terme**. L'indicateur d'identité peut surestimer la réussite si les deux objets sont proches ou se superposent. Les occultations restent artificielles et leur durée n'est pas calibrée sur des vidéos du monde réel. Les résultats des anciens tests restent intacts.

## Run Windows

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_identity_appearance_p151.py" -v
if ($LASTEXITCODE -ne 0) { throw "P151 : tests échoués" }
py -m brody_world_physique.image_identity_appearance_p151 --minutes 15 --episodes-each 250 --out "build\brody-p151-identity-001"
if ($LASTEXITCODE -ne 0) { throw "P151 : examen échoué" }
Get-Content "build\brody-p151-identity-001\MASTER_REPORT.json"
```

Dix conditions × 250 épisodes au maximum. Le budget de 15 minutes est une limite, pas une durée forcée. Le protocole est **expérimental**, `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.

Si le run révèle des erreurs, corriger avant d'avancer à P152 ; ne pas proclamer de progrès sans scores PC.
