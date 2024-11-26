import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Percorso al file degli archi
DATASET_PATH = r"C:\Users\pc\OneDrive\Desktop\Magistrale Ancona\Data science\Progetto\Networkx\road-italy-osm.edges"


def carica_grafo_da_edges(percorso):
    """
    Carica un grafo da un file di archi (.edges) ignorando eventuali righe di intestazione.
    """
    print(f"Caricando il grafo dal file: {percorso}")
    with open(percorso, "r") as f:
        # Ignora eventuali righe di commento o intestazione
        lines = [line for line in f if not line.startswith("%")]
    # Scrive il contenuto senza intestazione in un nuovo file temporaneo
    with open("filtered_edges.txt", "w") as f:
        f.writelines(lines)
    # Legge il file filtrato come lista di archi
    grafo = nx.read_edgelist("filtered_edges.txt", nodetype=int, create_using=nx.Graph())
    print(f"Grafo caricato con successo: {grafo.number_of_nodes()} nodi, {grafo.number_of_edges()} archi.")
    return grafo


def calcola_caratteristiche_grafo(grafo):
    """
    Calcola le caratteristiche strutturali del grafo.
    """
    nodi = grafo.number_of_nodes()
    archi = grafo.number_of_edges()
    diametro = nx.diameter(grafo) if nx.is_connected(grafo) else "Non connesso"
    comunità = nx.number_connected_components(grafo)
    dimensioni_comunità = [len(c) for c in nx.connected_components(grafo)]
    dimensione_massima_comunità = max(dimensioni_comunità)
    dimensione_minima_comunità = min(dimensioni_comunità)

    # Creazione del DataFrame con le caratteristiche
    caratteristiche = {
        "Proprietà": ["Numero di nodi", "Numero di archi", "Diametro", "Numero di comunità",
                      "Dimensione massima comunità", "Dimensione minima comunità"],
        "Valore": [nodi, archi, diametro, comunità, dimensione_massima_comunità, dimensione_minima_comunità]
    }
    return pd.DataFrame(caratteristiche)


def visualizza_tabella(tabella):
    """
    Visualizza la tabella utilizzando matplotlib.
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=tabella.values, colLabels=tabella.columns, loc='center', cellLoc='center')
    plt.title("Caratteristiche strutturali della rete", fontsize=14, weight="bold")
    plt.show()


if __name__ == "__main__":
    # Carica il grafo dal file di archi
    grafo = carica_grafo_da_edges(DATASET_PATH)

    # Calcola le caratteristiche strutturali
    tabella_caratteristiche = calcola_caratteristiche_grafo(grafo)
    print(tabella_caratteristiche)

    # Visualizza la tabella
    visualizza_tabella(tabella_caratteristiche)
