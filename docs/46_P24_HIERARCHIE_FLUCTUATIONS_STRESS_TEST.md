# 46 — P2.4 : fluctuations contextuelles, référentiels et hiérarchie

## Hypothèse attribuée à l'auteur (échanges du 9 octobre 2026)
Le « bruit » n'est ici qu'une analogie : un élément non utilisé par une couche n'est pas intrinsèquement du bruit. Les fluctuations de pixels / du contexte peuvent être une **donnée de précision**, utile à une autre échelle, dans un autre repère, sous un autre angle ou pour une autre tâche. Les données doivent être replacées dans **leur langage, leur hiérarchie, leur espace et leur temps** ; une interprétation locale ne doit pas devenir une suppression ou une vérité globale.

La propriété est à tester et non à proclamer : certaines fluctuations peuvent aussi être des artefacts. Ne jamais inventer une relation à partir du bruit réellement indépendant.

## Diagnostic de la P2.3
A1 vitesse, A3 raster et A6 fusion ont exactement la même moyenne de 4,092253992 px sur 49 cas communs, car des traitements différents représentent pratiquement la même mesure XY. La moyenne 50/50 ne conserve pas les contraintes du décor ou du repère. Le résultat empirique soutient seulement **aucun gain observable sur cette expérience synthétique**.

## Contrat de traduction (candidat, pas runtime MMonde)
Toute information interprétée doit conserver :
- sa provenance : source, mode d'observation, éventuelle dépendance à une même vidéo ;
- son langage : pixel caméra, position relative, mouvement apparent, vitesse ou candidat de monde ;
- son domaine spatial : coordonnées, repère et transformation explicite avant comparaison ;
- son domaine temporel : timestamp, fenêtre de validité et cutoff du pré-engagement ;
- son échelle et sa fonction : détail local, voisinage relationnel, hypothèse globale ;
- son état épistémique : observé, estimé, contradictoire, inconnu, hypothèse candidate.

Ne pas convertir « plusieurs variables » en « plusieurs preuves indépendantes ». Pas de moyennage des points appartenant à des référentiels incomparables.

## Première expérience P2.4 publiée : piste instrumentale falsifiable

`brody_world_physique/p24_contextual_fluctuation_v0.py` construit 7 cas synthétiques sur **des déplacements déjà mesurés**, avec la même translation apparente de l'objet (+10 px) mais différents déplacements de fond :
1. objet mobile, caméra fixe : candidat +10 ;
2. objet fixe, caméra mobile : candidat 0 ;
3. objet et caméra mobiles : candidat +6 ;
4. repère du fond comportant une valeur aberrante : candidat +6 ;
5. déplacements de fond contradictoires : HOLD ;
6. contexte absent : HOLD ;
7. alignement de référentiel inconnu : HOLD.

Règle instrumentale **fournie par l'ingénieur** : médiane de >=3 déplacements de fond ; accord à 1 px sur >=75 % des mesures ; déduire le mouvement de caméra et calculer mouvement relatif ; faute d'accord, HOLD. Ce n'est **pas** une règle découverte par Brody. Le générateur et ses valeurs de vérité ne doivent jamais être accessibles au modèle lors du futur essai d'apprentissage.

Comparaison cruciale : A (objet apparent seul) ne peut distinguer les cas 1 et 2 ; B (objet et contexte) le peut **dans la maquette**, à condition que les repères soient fiables ; C introduit incohérences et fausses mesures pour vérifier le refus. Le fait qu'un algorithme écrit à la main réussisse ne valide pas encore l'hypothèse d'apprentissage autonome.

## Prochaine épreuve non accomplie
- Générer des **frames brutes** avec repères non étiquetés et divers décalages de caméra, de lumière, occlusions, rotations, perspectives, changements d'échelles et asynchronismes.
- Conserver les pixels et leurs dérivations séparées ; évaluer une voie XY-seul contre pixels-contextes structurés, une voie avec contexte adversarial et des bras de retrait de vue.
- Geler avant TEST les générateurs, seuils, seuil d'amélioration, métriques et le groupe de randomisation par vidéo. Scinder par **scène / générateur**, non par frame.
- Mesurer : erreur de mouvement monde, orientation, continuité, attribution causale **hypothétique**, calibration des HOLD, précision sur échelle/caméra, coûts et résultats négatifs.
- Reverso : images reconstruites depuis les prévisions engagées, vérification ROI pré-gel ; ne pas inventer une reconstruction déjà acquise.

## Commandes PC — boucle preuves
Depuis la racine du repo, sur la branche `exp/p2-multirepresentation-ablation-20261009` :

```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
py -m unittest discover -s tests -p "test_*.py"
if ($LASTEXITCODE -ne 0) { throw "Tests en echec" }
$out = "build/p24-fluctuations-$(Get-Date -Format yyyyMMdd-HHmmss)"
New-Item -ItemType Directory -Path "$out/images" -Force | Out-Null
py -m brody_world_physique.p24_contextual_fluctuation_v0 --out "$out/evaluation.json"
if ($LASTEXITCODE -ne 0) { throw "P2.4 en echec" }
py -m brody_world_physique.p24_contextual_fluctuation_v0 --out "$out/evaluation.json" --verify
if ($LASTEXITCODE -ne 0) { throw "P2.4 verify en echec" }
notepad "$out/evaluation.json"
```

NOTE : le script de publication historique `publish_local_evidence.ps1` exige au moins un PNG. Ici le test est **non visuel**, donc ne pas feindre une preuve image ou publier avec ce script tant qu'un artefact PNG réel correspondant à la piste n'est pas produit. Le rapport JSON doit être conservé localement. La publication de preuves doit être adaptée explicitement pour cette expérience.

**Décision :** test de principe uniquement, résultat terrain en attente, aucune preuve d'apprentissage, pas de mémoire native, KX108_ONLY.

## Mise à jour — publication de preuve JSON sans image

Le script historique de publication accepte maintenant le paramètre explicite \`-AllowNoImages\`, pour ce test de contrat qui ne génère aucun PNG. Par défaut, le contrôle de présence d'images reste inchangé. Après vérification locale :

\`\`\`powershell
.\scripts\publish_local_evidence.ps1 -RunPath $out -AllowNoImages
\`\`\`

Publier uniquement le JSON authentique ; aucune image de preuve artificielle.
