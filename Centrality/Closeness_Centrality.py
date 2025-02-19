import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import os
from tqdm import tqdm

def load_graph_from_gpkg(file_path):
    try:
        print("Caricamento del file GeoPackage...")
        gdf = gpd.read_file(file_path, layer="edges")  # Usare il layer "edges" del dataset tagliato

        if gdf.empty:
            print("Il layer specificato non contiene dati.")
            return None

        G = nx.Graph()
        print("Creazione del grafo...")
        for _, row in tqdm(gdf.iterrows(), total=len(gdf), desc="Aggiunta di nodi e archi"):
            if row.geometry.geom_type == 'LineString':
                coords = list(row.geometry.coords)
                for i in range(len(coords) - 1):
                    G.add_edge(coords[i], coords[i + 1])

        return G
    except Exception as e:
        print(f"Errore durante il caricamento del grafo: {e}")
        return None

def compute_closeness_centrality(G):
    print("Calcolo della centralità di closeness...")
    centrality = {}
    for node in tqdm(G.nodes, desc="Calcolo per i nodi"):
        centrality[node] = nx.closeness_centrality(G, u=node)
    return centrality

def plot_graph_with_centrality(G, centrality, title, filename):
    print("Generazione del grafico della centralità di closeness...")
    try:
        fig, ax = plt.subplots(figsize=(12, 10))
        pos = {node: node for node in G.nodes}

        norm = Normalize(vmin=min(centrality.values()), vmax=max(centrality.values()))
        cmap = cm.Blues

        nodes = nx.draw_networkx_nodes(
            G, pos, ax=ax, node_size=20, node_color=[norm(v) for v in centrality.values()], cmap=cmap
        )
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray")

        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label("Closeness Centrality")

        ax.set_title(title)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
    except Exception as e:
        print(f"Errore durante la generazione del grafico: {e}")

def plot_histogram_of_centrality(centrality, title, filename):
    """
    Genera un istogramma per i valori di closeness centrality.
    """
    print("Generazione dell'istogramma della centralità di closeness...")
    try:
        plt.figure(figsize=(10, 6))
        plt.hist(centrality.values(), bins=30, color='blue', alpha=0.7)
        plt.title(title)
        plt.xlabel("Valore di Closeness Centrality")
        plt.ylabel("Frequenza")
        plt.grid(axis='y', alpha=0.75)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
        print(f"Istogramma salvato in: {filename}")
    except Exception as e:
        print(f"Errore durante la generazione dell'istogramma: {e}")

if __name__ == "__main__":
    file_path = <Insert the filtered dataset's path .gpkg>
    output_dir = <Insert the path of the 'results' folder>

    # Assicurati che la directory di output esista
    os.makedirs(output_dir, exist_ok=True)

    # Carica il grafo dal file .gpkg
    G = load_graph_from_gpkg(file_path)

    # Controlla se il grafo è vuoto
    if G is None or len(G.nodes) == 0:
        print("Il grafo è vuoto. Controlla il file e il layer specificato.")
    else:
        # Calcola la centralità di closeness
        centrality = compute_closeness_centrality(G)

        # Genera il grafico e salva il file
        output_file = os.path.join(output_dir, "closeness_centrality.png")
        plot_graph_with_centrality(G, centrality, "Closeness Centrality", output_file)

        # Genera e salva l'istogramma della centralità di closeness
        histogram_file = os.path.join(output_dir, "closeness_centrality_histogram.png")
        plot_histogram_of_centrality(centrality, "Istogramma della Closeness Centrality", histogram_file)

        print(f"Grafico salvato in: {output_file}")
        print(f"Istogramma salvato in: {histogram_file}")
