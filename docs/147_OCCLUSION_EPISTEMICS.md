# Brody — P147 | Épistémologie des objets occultés

Préparation indépendante du résultat de P146. P147 ne présume pas que le descripteur corrigé réussira son adaptation aux fonds sombres.

## Question

Que peut-on légitimement inférer d'une scène lorsqu'un objet est visible, partiellement caché ou entièrement caché ? Dans la dernière situation, l'étiquette de l'objet ne peut pas être reconstruite à partir de sa seule image visible, sans informations additionnelles.

## Protocole

Un enseignement de silhouettes visibles construit une mémoire candidate `robust_features`. La mémoire est gelée ; une nouvelle graine génère les examens sur trois conditions : objet visible, partiellement masqué par un obstacle opaque, totalement masqué par un obstacle opaque. Les décisions sont émises avant confrontation aux étiquettes et enregistrées séparément.

Les contrôles différencient précision des réponses produites, couverture et HOLD. Le programme refuse de deviner la forme d'un objet totalement masqué ; cette règle de protection est codée explicitement : elle n'est **pas** une découverte autonome. En occultation partielle, le classifieur conserve le droit de se tromper. Les examens sont **synthétiques** et ne démontrent pas l'apprentissage causal ni la compréhension du monde physique.

## Commande PC (après la fin de P146)

```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m unittest discover -s tests -p "test_image_occlusion_epistemics_p147.py" -v
if ($LASTEXITCODE -ne 0) { throw "P147 tests échoués" }
py -m brody_world_physique.image_occlusion_epistemics_p147 --minutes 10 --lessons 150 --exam-per-condition 1500 --out "build\brody-p147-occlusion-001"
if ($LASTEXITCODE -ne 0) { throw "P147 run échoué" }
Get-Content "build\brody-p147-occlusion-001\MASTER_REPORT.json"
```

**Réserves :** au plus 4500 examens ; le budget de 10 minutes est un maximum, pas une durée minimale. Le score de P147 ne doit pas être présenté comme un progrès d'apprentissage sur P146. Il faudra ensuite un vrai contre-factuel avec mêmes pixels visibles et plusieurs états cachés, des séquences temporelles et des interventions pour justifier une inférence physique. Ce futur contrat n'est pas implémenté ici.

Autorité : `KX108_ONLY`, `native_memory_write=false`, `canonical_promotion=false`.
