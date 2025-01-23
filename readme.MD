# Big Data Management avec MapReduce

## Description
Ce projet illustre l'utilisation de MapReduce pour traiter un large ensemble de données textuelles. Il compare les performances entre une méthode séquentielle et une méthode parallèle, en utilisant le multi-processing pour exploiter plusieurs cœurs CPU.

---

## Objectifs
- Comprendre les concepts de MapReduce.
- Analyser les avantages du traitement distribué.
- Évaluer l'impact du multi-processing sur les performances.

---

## Structure du Projet
- **Code Python** : Implémentation des étapes Map et Reduce.
- **Données** : Texte à analyser (fichier `large-txt.txt`).
- **Graphiques** : Résultats visuels sur les performances des phases.
- **rendu** : Rapport sur les résultats obtenus.

---

## Installation et Prérequis

### Étape 1 : Cloner le Répertoire
Clonez ce dépôt :
```bash
git clone <url-du-dépôt>
cd big_data_mapreduce
```

### Étape 2 : Installer les Dépendances
Assurez-vous que Python et les bibliothèques nécessaires sont installés:
```bash
pip install matplotlib
```

### Étape 3 : Placement des Données
Assurez-vous que le fichier `large-txt.txt` est dans le répertoire de travail. Vous pouvez télécharger le fichier [ici](google drive link).

---

## Exécution
Lancez le script pour exécuter les analyses:
```bash
python main.py
```

## Résultats
Le projet génère :
- Temps d'exécution pour les phases Map et Reduce.
- Comparaisons entre exécution séquentielle et parallèle.
- Graphiques de performance
---

## Auteurs
- **Moqim Ghizlan**

---

## Licence
Ce projet est sous licence libre.
