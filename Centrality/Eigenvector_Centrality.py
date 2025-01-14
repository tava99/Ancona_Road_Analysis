import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import os

def load_graph_from_gpkg(file_path):
    import fiona
    try:
        # Elenca i layer disponibili
        layers = fiona.listlayers(file_path)
        print("Layer disponibili:", layers)

        # Usa il layer corretto
        if "edges" in layers:
            layer_name = "edges"
        elif "lines" in layers:
            layer_name = "lines"
        elif "multilinestrings" in layers:
            layer_name = "multilinestrings"
        else:
            raise ValueError("Nessun layer compatibile trovato nel file .gpkg.")

        gdf = gpd.read_file(file_path, layer=layer_name)
        print(f"Layer '{layer_name}' caricato con successo.")

        G = nx.Graph()
        for _, row in gdf.iterrows():
            if row.geometry.geom_type == 'LineString':
                coords = list(row.geometry.coords)
                for i in range(len(coords) - 1):
                    G.add_edge(coords[i], coords[i + 1])
        return G
    except Exception as e:
        print(f"Errore durante il caricamento del grafo: {e}")
        return None

def compute_eigenvector_centrality(G):
    return nx.eigenvector_centrality(G, max_iter=1000)

def plot_graph_with_centrality(G, centrality, title, filename):
    fig, ax = plt.subplots(figsize=(12, 10))
    pos = {node: node for node in G.nodes}

    norm = Normalize(vmin=min(centrality.values()), vmax=max(centrality.values()))
    cmap = cm.Blues  # Cambiato al colore blue

    nx.draw_networkx_nodes(
        G, pos, ax=ax, node_size=20,
        node_color=[norm(v) for v in centrality.values()], cmap=cmap
    )
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray")

    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("Eigenvector Centrality")

    ax.set_title(title)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

def plot_centrality_histogram(centrality, title, filename):
    """
    Crea e salva un istogramma dei valori di centralità.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    centrality_values = list(centrality.values())
    ax.hist(centrality_values, bins=20, color='blue', alpha=0.7, edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel("Valore di Centralità")
    ax.set_ylabel("Frequenza")
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    file_path = <Insert the filtered dataset's path .gpkg>
    output_dir = <Insert the path of the 'results' folder>
    os.makedirs(output_dir, exist_ok=True)

    # Verifica se il file esiste
    if not os.path.exists(file_path):
        print(f"Errore: Il file '{file_path}' non esiste. Verifica il percorso.")
        exit()

    # Carica il grafo
    G = load_graph_from_gpkg(file_path)

    # Verifica se il grafo è vuoto
    if G is None or len(G.nodes) == 0 or len(G.edges) == 0:
        print("Il grafo è vuoto. Controlla i dati nel file .gpkg.")
        exit()

    # Calcola l'eigenvector centrality
    centrality = compute_eigenvector_centrality(G)

    # Salva il grafico del grafo con centralità
    plot_filename = os.path.join(output_dir, "eigenvector_centrality_graph.jpg")
    plot_graph_with_centrality(G, centrality, "Grafo con Eigenvector Centrality", plot_filename)

    # Salva l'istogramma dei valori di centralità
    histogram_filename = os.path.join(output_dir, "eigenvector_centrality_histogram.jpg")
    plot_centrality_histogram(centrality, "Istogramma di Eigenvector Centrality", histogram_filename)

    # Conferma la generazione dei file
    if os.path.exists(plot_filename):
        print(f"Grafico del grafo salvato correttamente in {plot_filename}.")
    else:
        print(f"Errore: il file grafico non è stato salvato in {plot_filename}.")

    if os.path.exists(histogram_filename):
        print(f"Istogramma salvato correttamente in {histogram_filename}.")
    else:
        print(f"Errore: il file istogramma non è stato salvato in {histogram_filename}.")
