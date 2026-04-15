# SAMI — Navigation autonome de robot avec motion capture

## 1. Présentation

SAMI est un projet de robotique dont l’objectif est de faire naviguer de manière autonome un robot Lego EV3 entre différents points dans un environnement réel.

Le robot doit :

* déterminer un ordre de visite des points aussi efficace que possible
* suivre une trajectoire
* s’adapter en temps réel grâce à un système de localisation externe (OptiTrack)

Le projet s’organise autour de trois parties principales :

* **Motion capture** : localisation du robot en temps réel
* **Contrôle** : suivi de trajectoire et génération des commandes moteurs
* **Planification de trajectoire** : optimisation de l’ordre de visite des points

Ma contribution s’est concentrée sur la partie **planification**, à travers la résolution d’un **problème du voyageur de commerce (TSP)**.

---

## 2. Résultats

* Le robot est capable de parcourir un ensemble de points dans une arène équipée de motion capture
* Le système fonctionne de bout en bout, de la capture de position jusqu’à l’action des moteurs via TCP
* L’approche combinant **plus proches voisins et 2-opt** permet de réduire nettement la distance totale parcourue par rapport à un ordre naïf

On observe notamment une diminution des croisements et des détours, ce qui rend les trajectoires plus naturelles et cohérentes.

---

## 3. Méthode

### Motion capture

* Position et orientation (yaw) obtenues en temps réel via OptiTrack
* Données reçues en UDP et traitées via un client NatNet

### Planification de trajectoire

Les points sont modélisés comme un **problème du voyageur de commerce (TSP)**.

Une première solution est obtenue avec l’heuristique des **plus proches voisins**.
Cette méthode est rapide, mais elle produit souvent des trajets imparfaits, avec des croisements et des détours.

La solution est ensuite améliorée à l’aide de l’algorithme **2-opt (implémenté from scratch)**, qui permet de corriger progressivement le trajet en réduisant sa longueur.

La combinaison de ces deux approches offre un bon compromis entre simplicité de calcul et qualité du résultat.

### Contrôle

* Contrôleur de feedback non linéaire
* Commandes moteurs calculées à partir de l’erreur de position et d’orientation

### Communication

* PC : client TCP (décision et calcul)
* Robot : serveur TCP (exécution des commandes)

---

## 4. Remarques

Ce projet met en évidence les limites des heuristiques gloutonnes : une méthode comme les plus proches voisins permet d’obtenir rapidement une solution, mais celle-ci reste souvent éloignée d’un bon résultat.

L’ajout d’une optimisation locale comme 2-opt permet d’améliorer significativement cette solution en corrigeant ses défauts les plus visibles.

Plus largement, ce travail montre l’intérêt de combiner une approche simple pour initialiser un problème, puis une méthode d’optimisation pour l’affiner, afin d’obtenir une solution efficace dans un contexte réel.

Pour davantage de visualisations, le notebook associé permet de suivre plus en détail les différentes étapes.
