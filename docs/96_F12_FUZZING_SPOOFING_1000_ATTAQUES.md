# F12 — Fuzzing et spoofing 1 000 essais de la perception F11

**Publication sur `exp/p2-multirepresentation-ablation-20261009` ; pas de modification de main.** Campagne à exécuter sur le PC avant tout verdict.

## Périmètre
Audit offensif **local** du mécanisme F11 de lecture des marqueurs visuels et d'association au contexte OLD/NEW. Dix familles équilibrées : référence, déplacement du marqueur, effacement, affaiblissement de contraste, marque partielle, deux marqueurs contradictoires, absence totale, inversion adverse du marqueur, fausse métadonnée de contexte, bruit périphérique.

L'attaquant manipule des pixels synthétiques ou une déclaration non fiable. On mesure les décisions incorrectes, les décisions non justifiées malgré une ambiguïté, les HOLD et le taux de substitution de contexte. Aucun accès à une cible d'examen pour apprendre et aucun entraînement pendant le test.

**Attention :** les familles `opposite` et `spoof_metadata` sont distinctes : une métadonnée non fiable est incluse au reçu, sans être utilisée par le détecteur. Inverser les pixels d'un marqueur de confiance peut faire choisir une mauvaise classe. C'est une faiblesse attendue à mesurer, pas un exploit d'un système de sécurité extérieur. Ce banc **ne teste pas** GNSS, RF ni une cible réseau. 

Chaque cas a une empreinte de l'image, et chaque événement est chaîné par SHA256 dans `attack_receipts.jsonl`. Le rapport `report.json` donne les comptes par attaque et des exemples des échecs. Ne pas confondre `NO_FAILURE_IN_COVERED_CASES` avec une sécurité globale. Le statut `VULNERABILITIES_FOUND` est un résultat scientifique du test, pas un crash technique.

## Lancement Windows
```powershell
Set-Location "$env:USERPROFILE\Desktop\OBSIDIA_WORLDS\brody-world-physique-image"
if ((git branch --show-current) -ne "exp/p2-multirepresentation-ablation-20261009") { throw "Mauvaise branche" }
git pull --ff-only
if ($LASTEXITCODE -ne 0) { throw "Pull échoué" }
py -m py_compile brody_world_physique\fusion_f12_adversarial_spoof_1000_v0.py
if ($LASTEXITCODE -ne 0) { throw "Syntaxe F12 invalide" }
py -m unittest discover -s tests -p "test_fusion_f12*.py" -v
if ($LASTEXITCODE -ne 0) { throw "Tests F12 échoués" }
py -m brody_world_physique.fusion_f12_adversarial_spoof_1000_v0 --cases 1000 --out "build\fusion-f12-fuzz-spoof-001"
if ($LASTEXITCODE -ne 0) { throw "Campagne F12 échouée" }
Get-Content "build\fusion-f12-fuzz-spoof-001\report.json"
```
Conserver les dossiers de preuves : nouveau chemin `-002` pour toute relance. Interdire l'écriture Native Memory, la promotion canonique et toute mutation d'autorité (`KX108_ONLY`).

## Suite
Définir d'abord le correctif sur la base des vraies défaillances et **réutiliser les attaques inchangées** comme TEST de régression. Ensuite étendre les perturbations aux formes, transformations et compositions de Brody. Ne pas entraîner sur les réponses des examens d'attaque.
