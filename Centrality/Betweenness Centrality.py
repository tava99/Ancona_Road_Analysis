import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from tqdm import tqdm
import os
from shapely.geometry import LineString

def load_graph_from_gpkg_interactive(gpkg_file, layer_name="edges"):
    """
    Carica un grafo da un file GeoPackage tagliato e restituisce nodi e archi con una barra di caricamento.
    """
    print("Caricamento del file GeoPackage...")
    gdf = gpd.read_file(gpkg_file, layer=layer_name)  # Usare il layer "edges" del dataset tagliato
    if gdf.crs is None:
        raise ValueError("Il CRS del file GeoPackage non è definito.")
    gdf = gdf.to_crs(epsg=4326)

    nodes, edges = set(), []
    print("Estrazione dei nodi e degli archi...")
    for _, row in tqdm(gdf.iterrows(), total=len(gdf), desc="Processamento geometrie"):
        line = row.geometry
        if isinstance(line, LineString):
            coords = list(line.coords)
            for i in range(len(coords) - 1):
                edges.append((coords[i], coords[i + 1]))
                nodes.update([coords[i], coords[i + 1]])
    return list(nodes), edges

def create_networkx_graph_from_edges(edges):
    """
    Crea un grafo NetworkX a partire da una lista di archi.
    """
    print("Creazione del grafo NetworkX...")
    G = nx.Graph()
    G.add_edges_from(edges)
    return G

def compute_betweenness_centrality(G, k=None):
    """
    Calcola la Betweenness Centrality per un grafo, con supporto per campionamento approssimativo.
    """
    print("Calcolo della Betweenness Centrality...")
    try:
        # Usa il parametro `k` per un calcolo approssimativo se specificato
        centrality = nx.betweenness_centrality(G, k=k, normalized=True)
        return centrality
    except Exception as e:
        print(f"Errore durante il calcolo della Betweenness Centrality: {e}")
        return {}

def plot_graph_with_centrality(G, centrality, title, filename):
    """
    Genera un grafico statico del grafo con colori che rappresentano la Betweenness Centrality.
    """
    print("Generazione del grafico della Betweenness Centrality...")
    try:
        fig, ax = plt.subplots(figsize=(12, 10))
        pos = {node: node for node in G.nodes}
        norm = Normalize(vmin=min(centrality.values()), vmax=max(centrality.values()))
        cmap = cm.Blues
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=20,
                               node_color=[norm(centrality[node]) for node in G.nodes], cmap=cmap)
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray")
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label("Betweenness Centrality")
        ax.set_title(title)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
    except Exception as e:
        print(f"Errore durante la generazione del grafico: {e}")

def plot_centrality_histogram(centrality, filename):
    """
    Genera un istogramma della distribuzione della Betweenness Centrality.
    """
    print("Generazione dell'istogramma della Betweenness Centrality...")
    try:
        values = list(centrality.values())
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(values, bins=30, color="blue", edgecolor="black", alpha=0.7)
        ax.set_title("Distribuzione della Betweenness Centrality")
        ax.set_xlabel("Betweenness Centrality")
        ax.set_ylabel("Numero di nodi")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.show()
    except Exception as e:
        print(f"Errore durante la generazione dell'istogramma: {e}")

if __name__ == "__main__":
    gpkg_file = <Insert the filtered dataset's path .gpkg>
    output_dir =<Insert the path of the 'results' folder>
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Caricamento e processamento del file GeoPackage
        nodes, edges = load_graph_from_gpkg_interactive(gpkg_file, layer_name="edges")

        # Creazione del grafo NetworkX
        G = create_networkx_graph_from_edges(edges)

        # Determina il campionamento per grafi grandi
        k_sample = 1500 if len(G.nodes) > 500 else None
        print(f"Utilizzando campionamento di {k_sample} nodi per la centralità." if k_sample else "Calcolo esatto della centralità.")

        # Calcolo della Betweenness Centrality con barra di caricamento
        centrality = compute_betweenness_centrality(G, k=k_sample)

        # Salvataggio del grafico della Betweenness Centrality
        plot_filename = os.path.join(output_dir, "betweenness_centrality_graph.jpg")
        plot_graph_with_centrality(G, centrality, "Grafo con Betweenness Centrality", plot_filename)

        # Salvataggio dell'istogramma
        hist_filename = os.path.join(output_dir, "betweenness_centrality_histogram.jpg")
        plot_centrality_histogram(centrality, hist_filename)

        print(f"Grafico salvato in: {plot_filename}")
        print(f"Istogramma salvato in: {hist_filename}")
    except Exception as e:
        print("Errore:", e)
