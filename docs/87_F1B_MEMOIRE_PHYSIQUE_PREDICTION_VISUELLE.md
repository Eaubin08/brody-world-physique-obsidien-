# 87 — F1B / Mémoire physique et prédiction visuelle

**Statut : code publié, exécution sur PC en attente.**  
**Branche :** `exp/p2-multirepresentation-ablation-20261009`; `main` inchangée.

## Organes réellement réutilisés
- `image_experience_guided_motion_v2.forecast` : émet des prévisions candidates préalablement scellées; méthodes comparées par contexte.
- `image_experience_guided_motion_v2.correct` : ouvre une observation de feedback distincte, conserve erreurs et mémoire candidate, sans modifier la prévision.
- `image_observed_motion_school_v1.analyze` : extrait la position depuis les pixels du prototype 2D.
- `image_observed_motion_school_v1.render` : produit les PNG prédits.

## Épreuve bornée
Deux trajectoires TRAIN synthétiques à trois images observées + quatrième image réservée au retour du professeur. Les corrections alimentent une mémoire candidate historique de mouvement. Une séquence TEST différente est ensuite évaluée à entrée identique avec `NO_MEMORY` et `WITH_MEMORY`. Les modèles signent leurs prévisions avant le calcul des erreurs. Le test consigne les erreurs **par modèle**, et le modèle effectivement sélectionné; un changement de sélection n'est pas imposé artificiellement.

## Interprétation interdite
Un excellent résultat ne démontre ni gravité apprise, ni causalité, ni transfert réel hors simulateur. Le banc utilise des objets 2D artificiels et des procédures programmées. La mémoire n'est pas raccordée au modèle P156, à la reconstruction de prototypes de F1A, à une pause/reprise éducative commune, ni à Native Memory. Ces champs restent explicitement `false` dans le rapport.

## Commandes sur Windows PowerShell
```powershell
git pull --ff-only origin exp/p2-multirepresentation-ablation-20261009
py -m unittest discover -s tests -p "test_f1b_physical_memory_bridge_v1.py" -v
py -m brody_world_physique.f1b_physical_memory_bridge_v1 --out "build/f1b-physical-v1"
Get-Content "build/f1b-physical-v1/MASTER_REPORT.json"
```
Les commandes sont à exécuter depuis la racine du dépôt. Le dossier de sortie doit être absent pour préserver toute preuve existante.

## Gates
`F1B_CODE=PUBLISHED`, `F1B_PC_RUN=UNVERIFIED`, `F1B_SHARED_FULL_EDUCATION=NOT_PROVEN`. Conserver toute régression ou HOLD. Les tests unitaires mesurent ici le fonctionnement du protocole, pas la qualité générale des images.
