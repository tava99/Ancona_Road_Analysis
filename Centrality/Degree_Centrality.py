import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import os

def load_graph_from_gpkg(file_path):
    """Carica il grafo dal file GPKG tagliato e verifica le geometrie."""
    gdf = gpd.read_file(file_path, layer="edges")  # Usare il layer "edges" del dataset tagliato
    print(gdf.head())  # Visualizza le prime righe per controllare le geometrie

    G = nx.Graph()
    for _, row in gdf.iterrows():
        if row.geometry.geom_type == 'LineString':
            coords = list(row.geometry.coords)
            for i in range(len(coords) - 1):
                G.add_edge(coords[i], coords[i + 1])

    print(f"Numero di nodi: {G.number_of_nodes()}")
    print(f"Numero di archi: {G.number_of_edges()}")
    return G

def plot_graph_with_centrality(G, centrality, title, filename=None):
    """Visualizza il grafo con i nodi colorati in base alla centralità e salva il risultato."""
    fig, ax = plt.subplots(figsize=(12, 10))
    pos = {node: node for node in G.nodes}

    norm = Normalize(vmin=min(centrality.values()), vmax=max(centrality.values()))
    cmap = cm.Blues

    nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_size=20,
                                   node_color=[norm(v) for v in centrality.values()], cmap=cmap)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray")

    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label("Centralità")

    ax.set_title(title)

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Grafo salvato come: {filename}")

    plt.show()

def plot_centrality_histogram(centrality, title, filename=None):
    """Genera e salva l'istogramma della centralità."""
    plt.figure(figsize=(10, 6))
    plt.hist(centrality.values(), bins=50, color='skyblue', edgecolor='black')
    plt.xlabel("Valore di Centralità")
    plt.ylabel("Frequenza")
    plt.title(title)

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Istogramma salvato come: {filename}")

    plt.show()

def compute_and_plot_degree_centrality(file_path, output_dir):
    """Calcola, visualizza la degree centrality e l'istogramma."""
    G = load_graph_from_gpkg(file_path)
    centrality = nx.degree_centrality(G)

    # Salva il grafo con degree centrality
    graph_filename = os.path.join(output_dir, "degree_centrality_graph.jpg")
    plot_graph_with_centrality(G, centrality, "Grafo con Degree Centrality", filename=graph_filename)

    # Salva l'istogramma della centralità
    hist_filename = os.path.join(output_dir, "degree_centrality_histogram.jpg")
    plot_centrality_histogram(centrality, "Istogramma della Degree Centrality", filename=hist_filename)

if __name__ == "__main__":
    file_path = <Insert the filtered dataset's path .gpkg>
    output_dir = <Insert the path of the 'results' folder>
    os.makedirs(output_dir, exist_ok=True)

    compute_and_plot_degree_centrality(file_path, output_dir)
