# SAMI — Navigation autonome de robot avec motion capture

## 1. Présentation

SAMI est un projet de robotique ayant pour objectif de faire naviguer de manière autonome un robot Lego EV3 entre différents points dans un environnement réel

Le robot doit :

* déterminer un ordre de visite optimal des points
* suivre une trajectoire
* s’adapter en temps réel grâce à un système de localisation externe (OptiTrack)

Le projet est structuré en trois parties principales :

* **Motion capture** : localisation du robot en temps réel
* **Contrôle** : suivi de trajectoire et génération des commandes moteurs
* **Planification de trajectoire** : optimisation de l’ordre de visite des points

Ma contribution s’est concentrée sur la partie **planification**, en particulier la résolution d’un **problème du voyageur de commerce (TSP)**

---

## 2. Résultats

* Le robot est capable de parcourir un ensemble de points dans une arène équipée de motion capture
* Le système est complet : de la capture de position jusqu’à l’action des moteurs via TCP
* L’approche combinant **plus proches voisins + 2-opt** permet de réduire significativement la distance totale parcourue par rapport à un ordre naïf

---

## 3. Méthode

### Motion capture

* Position et orientation (yaw) obtenues en temps réel via OptiTrack
* Données reçues en UDP et traitées via un client NatNet

### Planification de trajectoire

* Les points sont modélisés comme un **problème du voyageur de commerce (TSP)**

* Une première solution est obtenue avec l’heuristique des **plus proches voisins**
  -> Rapide mais produit des trajets sous-optimaux (croisements, détours)

* Cette solution est améliorée avec l’algorithme **2-opt (implémenté from scratch)**
  -> Suppression des croisements et réduction de la distance totale

* La combinaison des deux méthodes offre :

  * une bonne efficacité de calcul
  * une amélioration significative de la qualité du trajet

### Contrôle

* Contrôleur de feedback non linéaire
* Commandes moteurs calculées à partir de l’erreur de position et d’orientation

### Communication

* PC : client TCP (décision + calcul)
* Robot : serveur TCP (exécution des commandes)

---

## 4. Remarques

Ce projet met en évidence les limites des heuristiques gloutonnes : une méthode comme les plus proches voisins fournit rapidement une solution, mais souvent de qualité médiocre

L’utilisation d’une optimisation locale comme 2-opt permet d’améliorer significativement cette solution en corrigeant ses défauts structurels

Plus généralement, ce travail illustre l’intérêt de combiner :

* une heuristique rapide pour initialiser
* une méthode d’optimisation pour affiner

afin d’obtenir une solution efficace dans un contexte réel

Pour plus de visualisations, voir le notebook associé
