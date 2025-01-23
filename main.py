import time
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt

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

if __name__ == "__main__":
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

    # Vérification des dimensions des listes
    processor_counts = list(range(1, num_cores))
    while len(map_times) < len(processor_counts) - 1:
        map_times.append(0)  # Ajouter une valeur par défaut si des données manquent
    while len(reduce_times) < len(processor_counts) - 1:
        reduce_times.append(0)

    # Analyse des temps d'exécution
    times = list(time_history.values())

    # Graphique 1 : Temps total d'exécution
    plt.figure()
    plt.plot(processor_counts, times, marker='o', linestyle='-', color='b')
    plt.xlabel('Nombre de processeurs', fontsize=12)
    plt.ylabel('Temps total (secondes)', fontsize=12)
    plt.title('Temps total d\'exécution vs Nombre de processeurs', fontsize=14)
    plt.grid(True)
    plt.show()

    # Graphique 2 : Temps de la phase Map
    plt.figure()
    plt.plot(processor_counts[1:], map_times, marker='o', linestyle='-', color='g')
    plt.xlabel('Nombre de processeurs', fontsize=12)
    plt.ylabel('Temps de la phase Map (secondes)', fontsize=12)
    plt.title('Temps de la phase Map vs Nombre de processeurs', fontsize=14)
    plt.grid(True)
    plt.show()

    # Graphique 3 : Temps de la phase Reduce
    plt.figure()
    plt.plot(processor_counts[1:], reduce_times, marker='o', linestyle='-', color='r')
    plt.xlabel('Nombre de processeurs', fontsize=12)
    plt.ylabel('Temps de la phase Reduce (secondes)', fontsize=12)
    plt.title('Temps de la phase Reduce vs Nombre de processeurs', fontsize=14)
    plt.grid(True)
    plt.show()