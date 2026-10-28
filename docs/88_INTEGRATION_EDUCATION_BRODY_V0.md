# 88 — Intégration pédagogique Brody / restauration de la boucle complète

**Statut : premier parcours unifié candidat publié; tests d'exécution PC à confirmer.**
**Source de reprise :** audits Gmail 8–14 octobre; audit « Monde, mémoire et école » 212 pages, EXP-WF-001; parcours E0–E7; F1A/F1B/F1C; P140–P165.
**Branche :** `exp/p2-multirepresentation-ablation-20261009`. **Aucune modification de `main`.**

## Ce qui est vraiment implémenté maintenant
`brody_world_physique/integrated_education_v0.py` orchestre des APIs **existantes** de `image_experience_guided_motion_v2` et `image_observed_motion_school_v1`, via l'adaptateur F1B :
1. Images passées d'une séquence -> extraction de positions candidates.
2. Plusieurs hypothèses de mouvement -> engagement dans `sealed_forecast.json`.
3. Reconstruction PNG depuis chaque hypothèse -> nouvelle perception par l'analyseur existant -> erreur de reconstruction comparée aux paramètres attendus.
4. Révélation du feedback d'enseignement -> erreur -> candidat de mémoire scellé.
5. Leçon distincte, conservation des épisodes antérieurs et rédaction du **dossier de dépendances de compétence** (`education_checkpoint.json`).
6. Vérification de restauration de l'état expérimental.
7. Examens nouveaux appariés avec/sans mémoire, sans injection du feedback TEST dans TRAIN; mesures y compris abstentions.
8. Contrat LOCK/FLEX/IGNORE figurant explicitement dans les preuves comme obligation de conservation conceptuelle, **non** comme mécanisme de vérification complet.

## Ce qui reste non intégré et ne doit pas être revendiqué
- L'apprentissage autonome d'une loi physique à partir d'images réelles.
- L'intégration des représentations de SENS/Cognition, F12 et MMonde via leurs véritables contracts et SHAs.
- Un Reverse 360 spatial et perceptif complet : seul un **retour perception du PNG de modèle** est testé.
- Une vraie adaptation/révision des méthodes à partir de la friction; actuellement les trois familles d'hypothèses sont programmées.
- Un transfert entre la mémoire P156 et la mémoire de mouvement.
- Le rejeu d'une compétence complète après plusieurs séances et environnement différent.
- La preuve de dépendances transversales (localisation -> suivi -> modèle -> projection caméra).
- Le routage de l'observation selon un but dynamique.
- Une phase d'évaluation sur images/vidéos réellement captées.
- L'exécution de Brody LLM lui-même : ce banc reste un composant éducatif.

## Suite de raccords (ordre strict)
A. Lire les documents d'origine et le registre existant des compétences; figer leurs définitions sans réinventer les structures.
B. Intégrer le graphe de dépendances réel et le replay de compétences en remplaçant le simple dossier déclaratif.
C. Brancher l'analyse et la reconstruction sur une représentation commune réversible et typée, avec provenance/unknowns/invariants.
D. Contrôler les frontières SENS / F12 / MMonde / UDIP par contrats versionnés et tests anti-perte.
E. Mettre EXP-WF-001 sous curriculum progressif E0–E7, observation et génération réciproques, contradiction et révision, interruption/reprise réelle puis transfert inédit.
F. Ablations, images réelles, mesures de couverture vs risque, transfert positif et négatif. Validation humaine avant toute promotion.

## Commandes PowerShell (une seule séquence depuis le dépôt Brody)
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
if ($LASTEXITCODE -ne 0) { throw "PULL_FAILED" }
py -m unittest discover -s tests -p "test_integrated_education_v0.py" -v
if ($LASTEXITCODE -ne 0) { throw "INTEGRATED_TEST_FAILED" }
py -m brody_world_physique.integrated_education_v0 --out "build/integrated-education-v0"
if ($LASTEXITCODE -ne 0) { throw "INTEGRATED_RUN_FAILED" }
Get-Content "build/integrated-education-v0/MASTER_REPORT.json"
```

Le répertoire `build/integrated-education-v0` doit être absent avant exécution; une tentative précédente reste intacte.

## Verdict
`INTEGRATED_EDUCATION_V0_CODE_PUBLISHED`; `PC_TESTS_PENDING`; `FULL_CONCEPT_FIDELITY_HOLD`; `NATIVE_MEMORY_WRITE=FALSE`; `CANONICAL_PROMOTION=FALSE`; `DECISION_AUTHORITY=KX108_ONLY`.
