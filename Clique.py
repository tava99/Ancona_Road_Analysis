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


    # Funzione per l'analisi delle clique
    def clique_analysis(grafo, num_nodi=5000):
        """
        Trova tutte le clique nel grafo e visualizza la più grande.
        """
        print(f"Creazione del sottografo con i primi {num_nodi} nodi...")
        sub_grafo = grafo.subgraph(list(grafo.nodes)[:num_nodi])
        print(f"Sottografo creato: {sub_grafo.number_of_nodes()} nodi, {sub_grafo.number_of_edges()} archi.")

        print("Calcolo delle clique...")
        cliques = list(nx.find_cliques(sub_grafo))
        print(f"Numero totale di clique: {len(cliques)}")

        # Trova la clique più grande
        max_clique = max(cliques, key=len)
        print(f"Clique più grande (dimensione {len(max_clique)}): {max_clique}")

        # Visualizza il grafo con la clique più grande evidenziata
        pos = nx.spring_layout(sub_grafo)
        plt.figure(figsize=(12, 12))
        nx.draw(sub_grafo, pos, with_labels=True, node_color='lightgray', edge_color='lightgray')
        nx.draw_networkx_nodes(sub_grafo, pos, nodelist=max_clique, node_color='purple', node_size=300)
        nx.draw_networkx_edges(sub_grafo, pos, edgelist=list(zip(max_clique, max_clique)), edge_color='purple', width=2)
        plt.title("Clique più grande nel grafo")
        plt.show()


    # Caricamento del grafo
    grafo = carica_grafo_da_edges(DATASET_PATH)

    # Analisi delle clique
    clique_analysis(grafo, num_nodi=5000)

    print("Fine del programma.")
