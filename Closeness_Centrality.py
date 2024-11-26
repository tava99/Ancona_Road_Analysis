import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

def carica_grafo_da_edges(percorso):
    """
    Carica un grafo da un file di archi (.edges) ignorando eventuali righe di intestazione.
    """
    print(f"Caricando il grafo dal file: {percorso}")
    with open(percorso, "r") as f:
        lines = [line for line in f if not line.startswith("%")]
    with open("filtered_edges.txt", "w") as f:
        f.writelines(lines)
    grafo = nx.read_edgelist("filtered_edges.txt", nodetype=int, create_using=nx.Graph())
    print(f"Grafo caricato con successo: {grafo.number_of_nodes()} nodi, {grafo.number_of_edges()} archi.")
    return grafo

def closeness_centrality_analysis(grafo, num_nodi=5000):
    """
    Analisi della Closeness Centrality per i primi num_nodi del grafo.
    """
    print(f"Analisi Closeness Centrality per i primi {num_nodi} nodi...")
    sub_grafo = grafo.subgraph(list(grafo.nodes)[:num_nodi])
    centrality = nx.closeness_centrality(sub_grafo)

    print(f"Centralità calcolata per {len(centrality)} nodi. Visualizzazione in corso...")
    pos = nx.spring_layout(sub_grafo)
    plt.figure(figsize=(12, 12))
    nx.draw(sub_grafo, pos, node_size=np.array([v * 1000 for v in centrality.values()]),
            node_color='red', with_labels=False)
    plt.title("Grafo basato sulla Closeness Centrality")
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(centrality)), list(centrality.values()), color='red')
    plt.title("Istogramma della Closeness Centrality")
    plt.xlabel("Nodi")
    plt.ylabel("Centralità")
    plt.show()

if __name__ == "__main__":
    DATASET_PATH = r"C:\Users\pc\OneDrive\Desktop\Magistrale Ancona\Data science\Progetto\Networkx\road-italy-osm.edges"
    print("Inizio del programma.")
    grafo = carica_grafo_da_edges(DATASET_PATH)
    closeness_centrality_analysis(grafo)
    print("Fine del programma.")
