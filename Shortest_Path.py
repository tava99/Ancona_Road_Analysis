import networkx as nx
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    DATASET_PATH = r"C:\Users\pc\OneDrive\Desktop\Magistrale Ancona\Data science\Progetto\Networkx\road-italy-osm.edges"
    print("Inizio del programma.")


    # Funzione per caricare il grafo da un file di archi
    def carica_grafo_da_edges(percorso):
        if not os.path.exists(percorso):
            raise FileNotFoundError(f"Il file {percorso} non esiste.")

        print(f"Caricando il grafo dal file: {percorso}")
        with open(percorso, "r") as f:
            lines = [line for line in f if not line.startswith("%")]

        if not lines:
            raise ValueError("Il file fornito non contiene archi validi.")

        with open("filtered_edges.txt", "w") as f:
            f.writelines(lines)

        grafo = nx.read_edgelist("filtered_edges.txt", nodetype=int, create_using=nx.Graph())
        print(f"Grafo caricato con successo: {grafo.number_of_nodes()} nodi, {grafo.number_of_edges()} archi.")
        return grafo


    # Funzione per calcolare e visualizzare la rete ego
    def ego_network_analysis(grafo, nodo, num_nodi=5000):
        """
        Trova e visualizza la rete ego di un nodo specifico.
        """
        print(f"Creazione del sottografo con i primi {num_nodi} nodi...")
        sub_grafo = grafo.subgraph(list(grafo.nodes)[:num_nodi])
        print(f"Sottografo creato: {sub_grafo.number_of_nodes()} nodi, {sub_grafo.number_of_edges()} archi.")

        if nodo not in sub_grafo.nodes:
            print(f"Errore: il nodo {nodo} non esiste nel sottografo.")
            return

        print(f"Calcolo della rete ego per il nodo {nodo}...")
        ego_net = nx.ego_graph(sub_grafo, nodo)
        print(f"Rete ego di {nodo} contiene {ego_net.number_of_nodes()} nodi e {ego_net.number_of_edges()} archi.")

        # Visualizza la rete ego
        pos = nx.spring_layout(ego_net)
        plt.figure(figsize=(12, 12))
        nx.draw(ego_net, pos, with_labels=True, node_color='orange', edge_color='black')
        plt.title(f"Rete ego per il nodo {nodo}")
        plt.show()


    # Caricamento del grafo
    grafo = carica_grafo_da_edges(DATASET_PATH)

    # Analisi della rete ego
    nodo = 1  # Sostituire con il nodo desiderato
    ego_network_analysis(grafo, nodo=nodo, num_nodi=5000)

    print("Fine del programma.")
