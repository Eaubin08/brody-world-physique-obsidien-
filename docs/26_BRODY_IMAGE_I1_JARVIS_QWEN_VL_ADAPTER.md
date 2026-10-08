# 26 — Brody Image I1 : réutilisation du Qwen-VL de Jarvis (sans nouvel appareil ni modèle)

**2026-10-08 — Périmètre :** observation descriptive d'une **image utilisateur sélectionnée explicitement**.  
**État exact :** client local OpenAI-compatible **codé** dans ce repo ; tests avec **faux service HTTP** ; essai avec le Qwen-VL **réel du PC fixe pas encore prouvé ici** ; connexion au chat Brody et au Binder Obsidia **NON** faite.

## Source de vérité : on ne réinstalle pas Qwen-VL

Le fournisseur est déjà implémenté côté Jarvis dans
[`src/jarvis/integrations/local_vision_cognition.py`](https://github.com/Eaubin08/Jarvis-iron-obsidia-/blob/main/src/jarvis/integrations/local_vision_cognition.py).
Jarvis utilise un endpoint OpenAI-compatible local, généralement
`http://127.0.0.1:8081/v1/chat/completions`, `JARJAR_VISION_URL` pour l'URL,
`JARJAR_VISION_MODEL` pour le nom réellement servi, avec des messages `system` +
`user` contenant `type=image_url` / `data:image/...;base64,`.

Le module [`jarvis_vision_v0.py`](../brody_world_physique/jarvis_vision_v0.py)
**réutilise exactement cette interface réseau** sans copier/importer les services caméra et timeline de Jarvis, et **sans lancer/installer un autre Qwen-VL**. C'est un adaptateur de test distinct et limité, non une duplication du cerveau, de la mémoire ou du modèle.

## Ce qui est implémenté

- Une photo de référence PNG/JPEG/WebP nommée explicitement → prétraitement RGB/JPEG (max 1280 px par défaut) → demande locale à Qwen-VL → **description candidate non vérifiée** dans un JSON.
- Hash SHA-256 de l'original et **hash différent de l'image compressée envoyée** au modèle ; distinction `USER_IMAGE_FILE` et `GENERATED_ARTIFACT`. Un fichier fourni par l'utilisateur **n'est pas attesté réel par son nom**.
- Statuts et pouvoir : `MODEL_DESCRIPTION_UNVERIFIED`, `real_image_observation=false`, `semantics_verified=false`, `memory_write_allowed=false`, `KX108_ONLY`, aucune capacité ACT ; **pas d'identification automatique** et pas de prétention de profondeur/causalité prouvée.
- URL HTTP **loopback uniquement**, sans proxy ni redirection, limitation taille entrée/sortie et délai, refus des réponses invalides. **Aucune image n'est transmise à un service public** par ce module.
- Il n'invente aucun masque : Qwen-VL **décrit** ; isoler précisément un sujet de photo complexe exigera ensuite un vrai modèle de segmentation ou un masque manuel.

## Premier essai sur le PC fixe (PowerShell Windows)

Depuis le dépôt cloné localement et avec le **serveur Qwen-VL Jarvis habituel déjà démarré** :

```powershell
py -m pip install -r requirements-image.txt
py -m unittest discover -s tests -p "test_*.py" -v

# Vérifier le modèle exposé : pas d'installation
Invoke-RestMethod http://127.0.0.1:8081/v1/models

# Si Jarvis utilise un endpoint ou un nom différent, réutiliser SA configuration :
$env:JARJAR_VISION_URL="http://127.0.0.1:8081/v1/chat/completions"
$env:JARJAR_VISION_MODEL="Qwen2.5-VL-3B-Instruct"

# Fournir une vraie photo personnelle explicitement choisie et présente localement :
py -m brody_world_physique.jarvis_vision_v0 --image "C:\\photos\\test.jpg" --out "build\\vision-candidate.json"
```

Le `model` est une valeur de configuration : adapter `JARJAR_VISION_MODEL` à ce que renvoie `/v1/models` ou aux réglages déjà validés de Jarvis. Si le serveur n'est pas lancé : échec explicite, **sans fallback silencieux vers le cloud**. Le résultat écrit la réponse descriptive et son statut de candidate ; il ne passe pas par le chat Brody.

Pour **une image générée**, utiliser `--source-kind GENERATED_ARTIFACT` : ne jamais la faire entrer dans F16 en tant qu'observation de la réalité.

## Portable et PC fixe

- **Fixe :** conserve l'instance Qwen-VL de Jarvis et reçoit les calculs du modèle ; on ne change pas les ports du service sans connaître le launcher réel.
- **Portable :** peut exécuter Python/Pillow et la V0 d'édition de pixels **sans connexion au fixe**.
- **Portable avec Qwen-VL distant :** seul un accès sécurisé **tunnellisé sur localhost** devrait donner accès au `8081` du fixe. Exemple conditionnel **si un serveur SSH est déjà configuré** sur le fixe :

```powershell
ssh -N -L 8081:127.0.0.1:8081 utilisateur@adresse-du-fixe
```

Maintenir ce tunnel ouvert, puis lancer **la même commande** vision depuis une autre fenêtre du portable ; `127.0.0.1:8081` du portable représente alors le service du fixe. **Ne pas ouvrir 8081 directement sur le réseau ou Internet** : Qwen/OpenAI-compatible peut être sans authentification. Sans SSH existant, ne rien exposer ; tester directement sur le fixe jusqu'à disposer d'un accès sûr.

## Ce qui manque précisément

| Frontière | Réalité |
|---|---|
| Python image → Jarvis/Qwen-VL | Client **implémenté** ; simulation HTTP couverte en tests ; **preuve endpoint PC physique attendue** |
| Jarvis camera/screen → Brody Image | **Non raccordé** : l'exemple emploie un fichier explicite, sans détourner la timeline de Jarvis |
| Image → F16 `RealImageObservationV0` | **Non raccordé** : provenance d'un fichier seule ne prouve pas l'observation physique |
| Image → Brody chat API | **Non raccordé** : éviter la concaténation sauvage de prompts/contexte dans `/api/brody/chat` |
| Binder/Guard/KX108 | **Inchangés** : la mention `KX108_ONLY` dans le reçu est une borne de contrat, **pas** une autorisation réelle du kernel |
| Segmentation, profondeur, génération | **Non raccordées**, choisir les poids en fonction du matériel fixe (GTX 1050 Ti 4 Go d'après l'inventaire utilisateur) |
| Apprentissage / Native Memory | **Non raccordé** : ne pas convertir la description du modèle en fait validé ou en mémoire |

**Prochain critère de fermeture I1 :** envoyer une **vraie photo** au Qwen local installé sur le fixe, obtenir un `vision-candidate.json` avec ses 2 hashes, vérifier sa description à l'œil, tester ensuite un contre-exemple (ambiguïté, objet partiellement occulté). Seulement après, aborder l'adaptateur Brody + F16 en respectant leurs contrats.
