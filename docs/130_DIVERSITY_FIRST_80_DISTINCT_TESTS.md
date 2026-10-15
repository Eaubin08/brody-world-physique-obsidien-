# Brody — Matrice de 80 tests DISTINCTS (P130)

Priorité: couverture de compétences, PAS répétition d'une balle ou variations de seeds. Chaque essai doit avoir corpus de provenance contrôlée, cours et examen séparés, prédiction avant correction, contre-exemple, verdict PASS/FAIL/HOLD et savoir conservé.

## Perception
- [ ] Perception-01 : couleur vs éclairage
- [ ] Perception-02 : contours vs texture
- [ ] Perception-03 : ombres
- [ ] Perception-04 : multi-objets
- [ ] Perception-05 : occlusion
- [ ] Perception-06 : parties manquantes
- [ ] Perception-07 : fond et sujet
- [ ] Perception-08 : matériaux

## Multivue
- [ ] Multivue-01 : rotation
- [ ] Multivue-02 : profil vs face
- [ ] Multivue-03 : échelle
- [ ] Multivue-04 : miroir
- [ ] Multivue-05 : déformation
- [ ] Multivue-06 : 2D vs 3D
- [ ] Multivue-07 : vues partielles
- [ ] Multivue-08 : changement lumière

## Génération
- [ ] Génération-01 : silhouette mémorisée
- [ ] Génération-02 : couleur enseignée
- [ ] Génération-03 : nouvel angle
- [ ] Génération-04 : composition relationnelle
- [ ] Génération-05 : correction de dessin
- [ ] Génération-06 : complétion occultation
- [ ] Génération-07 : variation originale
- [ ] Génération-08 : qualité géométrique

## Physique
- [ ] Physique-01 : chute
- [ ] Physique-02 : rebond
- [ ] Physique-03 : collision
- [ ] Physique-04 : friction
- [ ] Physique-05 : rotation
- [ ] Physique-06 : équilibre
- [ ] Physique-07 : flottabilité
- [ ] Physique-08 : objet caché

## Temps-causalité
- [ ] Temps-causalité-01 : ordre événements
- [ ] Temps-causalité-02 : cause vs corrélation
- [ ] Temps-causalité-03 : action et conséquence
- [ ] Temps-causalité-04 : rupture de séquence
- [ ] Temps-causalité-05 : vitesse de vidéo
- [ ] Temps-causalité-06 : événement masqué
- [ ] Temps-causalité-07 : chronologie inversée
- [ ] Temps-causalité-08 : micro vers macro

## Éducation
- [ ] Éducation-01 : cours professeur
- [ ] Éducation-02 : imitation
- [ ] Éducation-03 : enseignement différé
- [ ] Éducation-04 : induction de règle
- [ ] Éducation-05 : contradiction
- [ ] Éducation-06 : transfert inter-domaines
- [ ] Éducation-07 : rétention
- [ ] Éducation-08 : faux professeur

## Mémoire
- [ ] Mémoire-01 : après redémarrage
- [ ] Mémoire-02 : doublon vs nouveau
- [ ] Mémoire-03 : préservation acquis
- [ ] Mémoire-04 : révision localisée
- [ ] Mémoire-05 : checkpoint
- [ ] Mémoire-06 : provenance
- [ ] Mémoire-07 : rappel analogique
- [ ] Mémoire-08 : rappel différé

## Raisonnement
- [ ] Raisonnement-01 : analogie
- [ ] Raisonnement-02 : propriétés et relations
- [ ] Raisonnement-03 : invariant
- [ ] Raisonnement-04 : trois hypothèses
- [ ] Raisonnement-05 : refus sans preuve
- [ ] Raisonnement-06 : décomposition
- [ ] Raisonnement-07 : recomposition
- [ ] Raisonnement-08 : transfert spatial

## Exploration
- [ ] Exploration-01 : choisir expérience
- [ ] Exploration-02 : demander donnée manquante
- [ ] Exploration-03 : source fiable
- [ ] Exploration-04 : éviter redondance
- [ ] Exploration-05 : nouveauté structurelle
- [ ] Exploration-06 : expérience discriminante
- [ ] Exploration-07 : expliquer limite
- [ ] Exploration-08 : exploration gouvernée

## Robustesse
- [ ] Robustesse-01 : bruit
- [ ] Robustesse-02 : hors domaine
- [ ] Robustesse-03 : fuite de données
- [ ] Robustesse-04 : mémoire altérée
- [ ] Robustesse-05 : licences
- [ ] Robustesse-06 : enseignant adversarial
- [ ] Robustesse-07 : machine modeste
- [ ] Robustesse-08 : frontière KX108

## État honnête

Partiel: images gris/RGB, contextes pixel, identité enseignée, mosaïque de génération, suivi mono-objet 2D, mémoire candidate, reçus, splits de source déclarés. Non prouvé: reconnaissance sémantique, vrai 360, compréhension 3D, multiobjet, génération fidèle, causalité, exploration externe autonome, enseignants authentifiés, lois physiques générales et transfert réel.

## Exécution

Chaque compétence exige un test distinct, pas 100 déclinaisons d'un même scénario. Ne jamais annoncer PASS sans code exécuté et données adaptées. Préférer 10 tests transversaux livrés ensemble à 10 000 cas quasi identiques. Distinguer tests de code, apprentissage, transfert, robustesse, sécurité et expérience terrain. Les 80 lignes sont un backlog: leur publication ne signifie pas qu'elles sont implémentées.

Autorité KX108_ONLY ; native_memory_write=false ; canonical_promotion=false. Ne pas modifier main.
