# 182 — P165-D11 / Gate C : contre-exemples de mouvement indépendants

## But
Après 653/653 tests unittest GREEN sur 148 fichiers, tester la généralisation du suivi plutôt que sa seule conformité. P165-D9 a révélé 324 échecs sur 1350 : 270 sauts, 36 accélérations sous occultation totale, 18 déplacements linéaires sous occultation totale.

## Implémentation initiale
`brody_world_physique/independent_gate_c_p165d11.py` utilise un nouveau rendu PIL **sans appeler le générateur de scènes D2**. Dix familles, douze graines par famille (120 examens) : saut, accélération rapide, freinage, inversion, mouvement caméra apparent, substitution, croisement indiscernable, occultation tardive, occultation prolongée, distracteur trompeur.

Les images seules sont transmises au `infer` P165-D6 existant ; le type de scénario et les positions véritables restent exclusivement pour notation. Chaque rapport enregistre anciens quatre points corrects, succès avant, succès après et **même piste compatible avant/après**. La liste des 8 hypothèses n'est pas une preuve d'identité physique. Le tracker est inchangé. Les jeux de tests sont toujours synthétiques, 2D et conçus avec des formes simples, sans Wi-Fi réel/radar/LiDAR/caméra 3D calibrée.

**Limite critique** : même avec un générateur de scènes différent, cet examen réutilise le détecteur et le tracker anciens, des objets dessinés sous forme d'ellipses et la métrique existante d'identité. Le banc n'est pas encore suffisamment indépendant pour démontrer une compréhension de la physique, et il ne vérifie pas une identification unique après substitution. `camera_pan` n'utilise pas une rotation 3D calibrée ; cette famille est une translation d'objet sur l'image et ne suffit pas à identifier un mouvement de caméra. Les libellés des familles correspondent au scénario de génération, **pas à une causalité identifiée par le moteur**.

## Procédure PC
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique/independent_gate_c_p165d11.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe Gate C échouée" }
py -m unittest discover -s tests -p "test_independent_gate_c_p165d11.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests Gate C échoués — STOP" }
py -m brody_world_physique.independent_gate_c_p165d11 --beam 8 --seeds 12 --out "build\brody-p165d11-gate-c-001"
if ($LASTEXITCODE -ne 0) { throw "Gate C ne s'est pas exécuté — STOP" }
Get-Content "build\brody-p165d11-gate-c-001\MASTER_REPORT.json"
```

L'état d'exécution du Gate C doit être séparé des **performances du tracker**. Un rapport créé avec succès peut contenir de nombreux échecs de continuité. Ne pas appeler cette campagne GREEN tant que les résultats adversariaux ne sont pas analysés.

Gouvernance : `native_memory_write=false`, `canonical_promotion=false`, `decision_authority=KX108_ONLY`. Branche expérimentale uniquement.

**Verdict publication** : `P165D11_GATE_C_CODE_PUBLISHED / PC_VALIDATION_PENDING / TRUE_IDENTITY_AND_3D_UNPROVEN`.
