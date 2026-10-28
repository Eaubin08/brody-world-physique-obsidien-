# Brody — Passe 129 : contextes + transitions physiques + transfert

Cette passe ajoute un organe expérimental de **mémoire des événements de mouvement**, complémentaire du modèle de prévision physique de la passe 128. Les contextes ne sont plus uniquement une étiquette `vertical|reversal` : l'observation conserve un événement, l'axe dominant, la vitesse locale, la vitesse antérieure et la taille apparente. Les événements détectés sont REVERSAL, STOP, START, SPEED_UP, SLOW_DOWN, STEADY. Ils sont calculés à partir des positions visibles et des temps, pas d'une connaissance fournie de la gravité ou d'un rebond.

Le module `image_context_transition_transfer_v1.py` fonctionne en deux phases **distinctes** :
- `forecast` : observe au moins quatre images, établit le contexte et propose une prévision. Sans deux groupes de sources corrigés possédant le même événement : `DOUBT` et simple extrapolation locale. Avec au moins deux groupes distincts, il transfère une correction de vitesse médiane selon un repère relatif à la direction du mouvement : une transition verticale peut contribuer à une transition horizontale, mais l'identité causale des événements n'est pas affirmée. La prévision est **scellée avant révélation** de l'image suivante ; elle est rendue en PNG.
- `correct` : lit le forecast scellé, observe la cinquième image, calcule l'erreur et enregistre un épisode candidate avec contexte, provenance de groupe, delta de vitesse et empreinte. `--previous` restaure les expériences d'un run précédent (digest vérifié). Une correction contradictoire du même forecast est refusée. Aucun apprentissage à partir de l'examen n'a lieu avant la prévision.

**Limites majeures** : (1) les six types d'événement sont des définitions déjà programmées ; Brody ne découvre pas une taxonomie entièrement nouvelle ; (2) deux groupes déclarés ne prouvent pas une indépendance réelle ; (3) le transfert d'un même nom d'événement entre axes est un **candidat**, pas une loi ; (4) il n'y a pas encore de segmentation d'obstacles, collisions, connaissance de matériaux, géométrie 3D ou identification d'objets multiples ; (5) la règle de transfert est un prototype mathématique, pas un entraînement neuronal. Les connaissances antérieures ne sont jamais modifiées ; aucune promotion canonique, `native_memory_write=false`, `KX108_ONLY`.

## Tests PC

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_context_transition_transfer_v1.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests échoués" }
```

## Expérience réelle minimale

Créer au moins trois prises de vue/films distincts d'un objet sur fond clair, cinq images par séquence. Les deux premières servent de cours corrigés ; la dernière sert d'examen. Chacune doit avoir un identifiant de source différent et une géométrie suffisamment observable. Pour un manifeste `build\\transition-A.json` :

```json
{"source_group":"tournage-A","observations":[{"t":0,"file":"build/A/0.png"},{"t":1,"file":"build/A/1.png"},{"t":2,"file":"build/A/2.png"},{"t":3,"file":"build/A/3.png"}],"predict_t":4}
```

```powershell
py -m brody_world_physique.image_context_transition_transfer_v1 --mode forecast --manifest "build\transition-A.json" --out "build\transition-forecast-A"
py -m brody_world_physique.image_context_transition_transfer_v1 --mode correct --forecast "build\transition-forecast-A\sealed_forecast.json" --observed "build\A\4.png" --out "build\transition-correction-A"
```

Pour B, utiliser `--previous "build\\transition-correction-A\\candidate_transition_memory.json"` sur **les deux** invocations ; pour C, charger la mémoire après B dans `forecast` mais garder sa cinquième image secrète jusqu'à l'examen. Le champ `source` vaut alors `TRANSFERRED_TRANSITION` uniquement si le contexte est assez proche et au moins deux groupes distincts ont enseigné le même événement.

## Lecture critique attendue

Comparer erreurs avant/après transfert, et en particulier les inversions de direction. Ne pas forcer un avantage : le transfert peut empirer une prévision si les contextes partagent un nom mais pas les mêmes causes. Les étiquettes communes ne remplacent pas les preuves réelles. Prochaine intégration : campagne A/B automatisée de cette mémoire de transitions, contrôle de provenance au niveau enregistrement, géométrie multi-objet, révision localisée du savoir après erreurs.
