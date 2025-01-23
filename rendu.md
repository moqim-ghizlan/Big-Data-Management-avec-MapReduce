# Rendu du projet 'Big Data Management - MapReduce'
## Rendu par : GHIZLAN Moqim


## Objectif

   - Comprendre les concepts fondamentaux de MapReduce
   - Démontrer l'importance du multi-processing dans le traitement distribué des données.
   - L'enjeux et l'avantage de la distribution

## Expliquer le processus de map-reduce

Nous allons commencer par examiner un fichier texte contenant une grande quantité de données afin d'analyser son contenu. L'objectif est de compter combien de fois chaque mot apparaît dans le fichier, en utilisant à la fois une méthode séquentielle et une méthode parallèle. Dans la méthode séquentielle, un seul processeur parcourt l'ensemble du fichier pour effectuer le comptage des mots. En revanche, dans la méthode parallèle, plusieurs processus fonctionnent en même temps pour accélérer le traitement.

Pour ce faire, le texte est découpé en segments appelés "chunks", dont la taille est déterminée en fonction du nombre total de mots et du nombre de processus disponibles sur la machine. Le choix du nombre de workers, ou processus, est directement lié au nombre de cœurs CPU disponibles. Chaque chunk est traité de manière indépendante par un processus, puis les résultats sont combinés lors d'une étape de réduction pour obtenir un comptage global des mots. Enfin, une comparaison des performances entre les deux méthodes est effectuée pour évaluer l'impact du parallélisme sur le temps d'exécution.


## Partie 1 | Code
### Fonctions utilisées pour le MapReduce

```python
# Importation des bibliothèques nécessaires
import time
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt
```

```python
def read_file(file_path):
    """
    Lit le contenu d'un fichier texte.

    Args:
        file_path (str): Le chemin du fichier à lire.

    Returns:
        str: Le contenu du fichier sous forme de texte.
    """
    with open(file_path, 'r', encoding='latin') as file:
        return file.read()

def split_text(text):
    """
    Divise le texte en une liste de mots.

    Args:
        text (str): Texte à diviser.

    Returns:
        list: Liste de mots.
    """
    return text.lower().split()

def split_into_chunks(text, num_chunks):
    """
    Divise le texte en plusieurs segments (chunks) équilibrés pour le traitement parallèle.

    Args:
        text (str): Texte à diviser.
        num_chunks (int): Nombre de segments souhaités.

    Returns:
        list: Liste de segments (chunks) de texte.
    """
    words = split_text(text)
    chunk_size = max(1, len(words) // (num_chunks * 2))
    return [" ".join(words[i * chunk_size:(i + 1) * chunk_size]) for i in range((len(words) + chunk_size - 1) // chunk_size)]

def word_count_single(text):
    """
    Compte les mots dans un texte en mode mono-processeur.

    Args:
        text (str): Texte à analyser.

    Returns:
        dict: Dictionnaire avec les mots comme clés et leur fréquence comme valeurs.
    """
    words = split_text(text)
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def map_function(segment):
    """
    Fonction Map qui compte les mots dans un segment de texte.

    Args:
        segment (str): Segment de texte à analyser.

    Returns:
        dict: Dictionnaire avec les mots comme clés et leur fréquence comme valeurs.
    """
    words = split_text(segment)
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def reduce_function(counter1, counter2):
    """
    Combine deux dictionnaires de comptage de mots.

    Args:
        counter1 (dict): Premier dictionnaire.
        counter2 (dict): Deuxième dictionnaire.

    Returns:
        dict: Dictionnaire combiné avec les mots comme clés et leur fréquence totale.
    """
    for word, count in counter2.items():
        if word in counter1:
            counter1[word] += count
        else:
            counter1[word] = count
    return counter1

def word_count_multi(text, num_processes, map_times, reduce_times):
    """
    Compte les mots dans un texte en utilisant plusieurs processus.

    Args:
        text (str): Texte à analyser.
        num_processes (int): Nombre de processus à utiliser.
        map_times (list): Liste pour sauvegarder les durées de la phase Map.
        reduce_times (list): Liste pour sauvegarder les durées de la phase Reduce.

    Returns:
        dict: Dictionnaire avec les mots comme clés et leur fréquence comme valeurs.
    """
    chunks = split_into_chunks(text, num_processes)
    print(f"Segments (chunks) créés : {len(chunks)}")

    # Phase Map
    start_map = time.time()
    with Pool(processes=num_processes) as pool:
        map_results = pool.map(map_function, chunks)
    map_duration = time.time() - start_map
    map_times.append(map_duration)
    print(f"Durée de la phase Map : {map_duration:.2f} secondes")

    # Phase Reduce
    start_reduce = time.time()
    word_count = map_results[0]
    for result in map_results[1:]:
        word_count = reduce_function(word_count, result)
    reduce_duration = time.time() - start_reduce
    reduce_times.append(reduce_duration)
    print(f"Durée de la phase Reduce : {reduce_duration:.2f} secondes")

    return word_count
```


### Application du programme

```python

# Lecture du fichier
file_path = 'large-txt.txt'
text = read_file(file_path)

time_history = {}
map_times = []
reduce_times = []

# Comptage des mots avec un seul processeur
print("Exécution du comptage des mots avec un seul processeur...")
start_time = time.time()
single_result = word_count_single(text)
single_duration = time.time() - start_time
print(f"Durée avec un seul processeur : {single_duration:.2f} secondes")
time_history['1'] = single_duration

# Nombre de cœurs CPU disponibles
num_cores = cpu_count()
print(f"Nombre de cœurs CPU disponibles : {num_cores}")

# Comptage des mots avec plusieurs processeurs
for num_processes in range(2, num_cores):
    print(f"Exécution du comptage des mots avec {num_processes} processus...")
    start_time = time.time()
    multi_result = word_count_multi(text, num_processes, map_times, reduce_times)
    multi_duration = time.time() - start_time
    print(f"Durée avec {num_processes} processus : {multi_duration:.2f} secondes")
    time_history[str(num_processes)] = multi_duration

```

### Résultats

```text
Exécution du comptage des mots avec un seul processeur...
Durée avec un seul processeur : 7.84 secondes
Nombre de cœurs CPU disponibles : 16


Exécution du comptage des mots avec 2 processus...
Segments (chunks) créés : 5
Durée de la phase Map : 5.30 secondes
Durée de la phase Reduce : 0.21 secondes
Durée avec 2 processus : 9.86 secondes


Exécution du comptage des mots avec 3 processus...
Segments (chunks) créés : 7
Durée de la phase Map : 3.97 secondes
Durée de la phase Reduce : 0.25 secondes
Durée avec 3 processus : 8.58 secondes


Exécution du comptage des mots avec 4 processus...
Segments (chunks) créés : 9
Durée de la phase Map : 3.31 secondes
Durée de la phase Reduce : 0.31 secondes
Durée avec 4 processus : 8.05 secondes


Exécution du comptage des mots avec 5 processus...
Segments (chunks) créés : 11
Durée de la phase Map : 3.03 secondes
Durée de la phase Reduce : 0.33 secondes
Durée avec 5 processus : 7.79 secondes


Exécution du comptage des mots avec 6 processus...
Segments (chunks) créés : 13
Durée de la phase Map : 2.84 secondes
Durée de la phase Reduce : 0.36 secondes
Durée avec 6 processus : 7.72 secondes


Exécution du comptage des mots avec 7 processus...
Segments (chunks) créés : 15
Durée de la phase Map : 2.82 secondes
Durée de la phase Reduce : 0.40 secondes
Durée avec 7 processus : 7.66 secondes


Exécution du comptage des mots avec 8 processus...
Segments (chunks) créés : 17
Durée de la phase Map : 2.69 secondes
Durée de la phase Reduce : 0.44 secondes
Durée avec 8 processus : 7.60 secondes


Exécution du comptage des mots avec 9 processus...
Segments (chunks) créés : 19
Durée de la phase Map : 2.69 secondes
Durée de la phase Reduce : 0.45 secondes
Durée avec 9 processus : 7.69 secondes


Exécution du comptage des mots avec 10 processus...
Segments (chunks) créés : 21
Durée de la phase Map : 2.66 secondes
Durée de la phase Reduce : 0.48 secondes
Durée avec 10 processus : 7.62 secondes


Exécution du comptage des mots avec 11 processus...
Segments (chunks) créés : 23
Durée de la phase Map : 2.60 secondes
Durée de la phase Reduce : 0.49 secondes
Durée avec 11 processus : 7.63 secondes


Exécution du comptage des mots avec 12 processus...
Segments (chunks) créés : 25
Durée de la phase Map : 2.64 secondes
Durée de la phase Reduce : 0.54 secondes
Durée avec 12 processus : 7.94 secondes


Exécution du comptage des mots avec 13 processus...
Segments (chunks) créés : 27
Durée de la phase Map : 2.59 secondes
Durée de la phase Reduce : 0.53 secondes
Durée avec 13 processus : 7.74 secondes


Exécution du comptage des mots avec 14 processus...
Segments (chunks) créés : 29
Durée de la phase Map : 2.62 secondes
Durée de la phase Reduce : 0.65 secondes
Durée avec 14 processus : 7.80 secondes


Exécution du comptage des mots avec 15 processus...
Segments (chunks) créés : 31
Durée de la phase Map : 2.62 secondes
Durée de la phase Reduce : 0.59 secondes
Durée avec 15 processus : 7.63 secondes
```

### Interpretation des résultats :

Les résultats montrent que le temps total d'exécution diminue rapidement lorsque l'on passe d'un seul processeur à plusieurs processus. Cette réduction est particulièrement marquée au début, entre deux et huit processus, ce qui indique une bonne répartition de la charge sur les cœurs disponibles. Cependant, au-delà de ce point, les gains de performance deviennent moins significatifs, et le temps total commence à se stabiliser, voire à augmenter légèrement. Cela peut être dû à l'overhead lié à la gestion de nombreux processus simultanés et aux communications nécessaires entre eux.

Pour la phase Map, le temps diminue de manière constante avec l'augmentation du nombre de processus, ce qui confirme que le travail est bien parallélisé. En revanche, la phase Reduce présente une tendance inverse, avec un temps qui augmente à mesure que le nombre de processus croît. Cette augmentation peut s'expliquer par la nécessité de combiner un nombre croissant de résultats intermédiaires, ce qui ajoute une charge supplémentaire à cette phase. Les résultats offrent ainsi un premier aperçu des tendances générales, qui seront explorées plus en détail dans l'analyse graphique.



### Analyse des temps d'exécution & Vérification des dimensions des listes
```python
processor_counts = list(range(1, num_cores))
while len(map_times) < len(processor_counts) - 1:
    map_times.append(0)  # Ajouter une valeur par défaut si des données manquent
while len(reduce_times) < len(processor_counts) - 1:
    reduce_times.append(0)

times = list(time_history.values())

```

### Graphique 1 : Temps total d'exécution

```python
plt.figure()
plt.plot(processor_counts, times, marker='o', linestyle='-', color='b')
plt.xlabel('Nombre de processeurs', fontsize=12)
plt.ylabel('Temps total (secondes)', fontsize=12)
plt.title('Temps total d\'exécution vs Nombre de processeurs', fontsize=14)
plt.grid(True)
plt.show()
```
![img](https://raw.githubusercontent.com/moqim-ghizlan/Big-Data-Management-avec-MapReduce/refs/heads/main/phraph_1.png)

### Interpretation des résultats :

Le graphique montre comment le temps total d'exécution varie en fonction du nombre de processus utilisés. Lorsque l'exécution débute avec un seul processeur, le temps total est naturellement le plus élevé, car toute la charge de travail repose sur un seul thread. En augmentant progressivement le nombre de processus, on observe une réduction significative du temps total, surtout jusqu'à environ 6 à 8 processus. Cela indique que la répartition des segments de travail entre les différents cœurs est très efficace dans cette plage, ce qui réduit considérablement la durée d'exécution.

Cependant, au-delà de ce seuil optimal, les gains en termes de réduction du temps total deviennent minimes. À partir de 8 à 10 processus, le temps total commence à se stabiliser. Dans certains cas, il peut même légèrement augmenter, probablement en raison de la surcharge liée à la gestion et à la synchronisation des processus supplémentaires. Cette surcharge comprend la communication entre les processus, le partage de données et la gestion des résultats intermédiaires, qui peuvent consommer une partie des ressources et annuler les gains escomptés.

Le graphique met donc en lumière un comportement typique des systèmes parallèles, où un point de rendement décroissant est atteint. Dans ce cas précis, l'utilisation optimale des ressources semble se situer entre 6 et 10 processus. En dessous de ce seuil, l'exécution s'accélère nettement avec chaque processus supplémentaire. Au-delà, l'ajout de nouveaux processus n'apporte pas d'amélioration significative et peut même entraîner une légère dégradation des performances globales. Ce phénomène est particulièrement visible dans les systèmes dotés d'un grand nombre de cœurs, comme c'est le cas ici avec 16 cœurs disponibles.



### Graphique 2 : Temps de la phase Map

```python
plt.figure()
plt.plot(processor_counts[1:], map_times, marker='o', linestyle='-', color='g')
plt.xlabel('Nombre de processeurs', fontsize=12)
plt.ylabel('Temps de la phase Map (secondes)', fontsize=12)
plt.title('Temps de la phase Map vs Nombre de processeurs', fontsize=14)
plt.grid(True)
plt.show()
```
![img](https://raw.githubusercontent.com/moqim-ghizlan/Big-Data-Management-avec-MapReduce/refs/heads/main/phraph_2.png)

### Interpretation des résultats :
Ce graphique montre comment le temps requis pour la phase Map évolue en fonction du nombre de processus. On observe une diminution progressive du temps de Map à mesure que le nombre de processus augmente. Cela s'explique par la capacité à diviser efficacement le travail en segments (chunks), chaque processus s'occupant d'un sous-ensemble de données. Cette réduction est particulièrement marquée au début, entre deux et six processus, où l'on constate une accélération notable de l'exécution. Cela montre que le parallélisme est particulièrement efficace dans cette plage, réduisant considérablement la durée de la phase Map.

Cependant, après environ 8 processus, la diminution du temps devient beaucoup plus lente, avec une quasi-stabilisation vers 10 ou 12 processus. Cette tendance reflète les limites de la division des données : à mesure que le nombre de processus augmente, la taille des chunks diminue, et chaque processus a de moins en moins de travail à réaliser. À ce stade, l'overhead lié à la gestion des processus supplémentaires commence à annuler les gains en temps. Cela inclut le coût des communications entre les processus et le temps nécessaire pour coordonner leurs résultats.

Le graphique montre également que l'efficacité du parallélisme atteint un plateau lorsque les données deviennent trop fragmentées pour tirer pleinement parti de l'ajout de nouveaux processus. En conclusion, la phase Map tire largement profit de la parallélisation, mais seulement jusqu'à un certain seuil, au-delà duquel les gains sont limités et peuvent même être compensés par des coûts supplémentaires.




### Graphique 3 : Temps de la phase Reduce

```python
plt.figure()
plt.plot(processor_counts[1:], reduce_times, marker='o', linestyle='-', color='r')
plt.xlabel('Nombre de processeurs', fontsize=12)
plt.ylabel('Temps de la phase Reduce (secondes)', fontsize=12)
plt.title('Temps de la phase Reduce vs Nombre de processeurs', fontsize=14)
plt.grid(True)
plt.show()
```

![img](https://raw.githubusercontent.com/moqim-ghizlan/Big-Data-Management-avec-MapReduce/refs/heads/main/phraph_2.png)

### Interpretation des résultats :
Ce graphique montre comment le temps nécessaire pour la phase Reduce évolue en fonction du nombre de processus. Contrairement à la phase Map, on constate une augmentation progressive du temps de la phase Reduce avec l'accroissement du nombre de processus. Cette tendance s'explique par la nature même de la phase Reduce, qui implique la combinaison des résultats intermédiaires issus de la phase Map. Plus il y a de processus, plus il y a de résultats partiels à fusionner, ce qui alourdit cette étape.

Au départ, avec un nombre limité de processus, le temps de Reduce reste relativement faible, car le nombre de chunks est modeste et leur fusion peut s'effectuer rapidement. Cependant, à mesure que le nombre de processus augmente, la fragmentation des données s'intensifie, entraînant un plus grand nombre de résultats intermédiaires à traiter. Cela engendre une surcharge, non seulement pour réaliser les opérations de fusion, mais aussi pour coordonner et synchroniser les communications entre les processus.

Cette augmentation devient particulièrement marquée à partir de 8 processus, où le temps de la phase Reduce réagit plus fortement à l'augmentation du nombre de processus. Cela met en lumière les limites du parallélisme pour cette phase spécifique, qui dépend largement du volume de données intermédiaires générées et de l'efficacité de leur traitement. Le graphique souligne que, bien que la parallélisation soit efficace pour la phase Map, elle introduit une surcharge qui peut nuire aux performances de la phase Reduce à mesure que le nombre de processus croît.