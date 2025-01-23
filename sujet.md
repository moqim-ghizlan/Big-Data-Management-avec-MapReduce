---
noteId: "8a02a680d9cc11efa109f38b507ddb01"
tags: []

---

# Big Data - TD 01 : Map reduce

## Objectif
   
    - Comprendre les concepts fondamentaux de MapReduce
    - Démontrer l'importance du multi-processing dans le traitement distribué des données.
    - L'enjeux et l'avantage de la distribution

## Calcul de la fréquence des mots dans un grand ensemble de documents

Dans cet exercice, nous allons simuler le traitement d'un grand ensemble de documents textuels pour calculer la fréquence des mots à l'aide de la technique MapReduce, tout en exploitant le multi-processing pour accélérer le traitement.


## 1. Processus de map-reduce

Proposez la démarche à suivre pour effectuer la tache de comptage des mots dans le cas d'un grand nombre.

## Programmation 

### 1. Préparation des données :

Téléchargez ce document texte [__ici__](https://moodle.univ-lyon2.fr/mod/resource/view.php?id=222816) que vous utiliserez pour cet exercice.



### 2. Développement du programme : 

#### Mono processeur

- Ecrivez le programme qui vous permet de calculer pour chaque mot du document le nombre d'occurrences où il apparait.

- Mesurez le temps nécessaire que le programme à pris

#### Multi-processeurs

1. Écrivez une fonction Map qui prend un segment de document et produit une liste de paires clé-valeur, où la clé est un mot et la valeur est 1 (pour chaque occurrence du mot).

1. Écrivez une fonction Reduce qui prend une clé et une liste de valeurs (1 pour chaque occurrence du mot) et renvoie la somme des valeurs, représentant la fréquence du mot.

1. Implémentez une fonction principale qui divise les données en segments, applique la fonction Map à chaque segment en parallèle à l'aide du multi-processing, puis applique la fonction Reduce pour agréger les résultats finaux.

1.  Mensurez le temps nécessaire que le programme à pris avec différents nombre de processeurs (c.-à-d. avec 2,3 et 4 processeurs)


__Hint:__

1. Pour le multi-processing nous allons utiliser la fonction python ````Pool```` de ```multiprocessing```
1. Pour le reduce des résultats des maps on utilisera  ````reduce``` de ``` functools```


### 3. Questions supplémentaires :

1. Utilisez une bibliothèque de visualisation pour représenter graphiquement les résultats obtenus.

1. Comment le multi-processing affecte-t-il les performances de votre programme par rapport à une exécution séquentielle ?

1. Quels sont les avantages de l'utilisation de MapReduce pour ce type de traitement de données distribuées ?