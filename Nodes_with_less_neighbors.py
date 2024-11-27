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


    # Funzione per trovare e visualizzare i nodi con meno vicini
    def nodes_with_least_neighbors(grafo, top_n=5, num_nodi=5000):
        """
        Trova i nodi con il minor numero di vicini.
        """
        sub_grafo = grafo.subgraph(list(grafo.nodes)[:num_nodi])

        print(f"Calcolo dei {top_n} nodi con il minor numero di vicini...")
        degrees = sub_grafo.degree()
        bottom_nodes = sorted(degrees, key=lambda x: x[1])[:top_n]
        print(f"Nodi con meno vicini: {bottom_nodes}")

        # Visualizza i nodi con meno vicini
        pos = nx.spring_layout(sub_grafo)
        plt.figure(figsize=(12, 12))
        nx.draw(sub_grafo, pos, with_labels=True, node_color='lightgray', edge_color='lightgray')
        nx.draw_networkx_nodes(sub_grafo, pos, nodelist=[n[0] for n in bottom_nodes], node_color='red', node_size=500)
        plt.title(f"Top {top_n} nodi con meno vicini")
        plt.show()


    # Caricamento del grafo
    grafo = carica_grafo_da_edges(DATASET_PATH)

    # Analisi dei nodi con meno vicini
    nodes_with_least_neighbors(grafo, top_n=5, num_nodi=5000)

    print("Fine del programma.")
