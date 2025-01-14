import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import os
from shapely.geometry import LineString


def load_graph_from_gpkg(file_path, layer_name="edges"):
    """
    Carica un grafo da un file GeoPackage.

    :param file_path: Percorso del file GeoPackage.
    :param layer_name: Nome del layer da utilizzare (default: "edges").
    :return: Un grafo NetworkX.
    """
    gdf = gpd.read_file(file_path, layer=layer_name)

    G = nx.Graph()
    for _, row in gdf.iterrows():
        if row.geometry.geom_type == 'LineString':
            coords = list(row.geometry.coords)
            for i in range(len(coords) - 1):
                G.add_edge(coords[i], coords[i + 1], weight=row.geometry.length)

    return G


def nodes_with_less_neighbors(G):
    """
    Trova i nodi con il minor numero di vicini.

    :param G: Grafo NetworkX.
    :return: Lista di nodi con il minor numero di vicini.
    """
    degrees = dict(G.degree())
    min_neighbors = min(degrees.values())

    nodes_min = [node for node, degree in degrees.items() if degree == min_neighbors]

    print(f"Nodi con meno vicini ({min_neighbors}): {nodes_min}")

    return nodes_min


def plot_graph_with_low_degree_nodes(G, low_degree_nodes, output_path):
    """
    Crea un'immagine del grafo con i nodi a basso grado evidenziati.

    :param G: Grafo NetworkX.
    :param low_degree_nodes: Lista di nodi a basso grado.
    :param output_path: Percorso di output per salvare l'immagine.
    """
    pos = {node: (node[0], node[1]) for node in G.nodes}

    plt.figure(figsize=(10, 10))

    # Disegna il grafo completo
    nx.draw(G, pos, node_size=10, edge_color='gray', alpha=0.7, with_labels=False)

    # Evidenzia i nodi con meno vicini
    nx.draw_networkx_nodes(G, pos, nodelist=low_degree_nodes, node_size=50, node_color='blue')

    plt.title("Grafo con nodi a basso grado evidenziati")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Immagine salvata in {output_path}")


if __name__ == "__main__":
    file_path = <Insert the filtered dataset's path .gpkg>
    layer_name = "edges" 
    output_image = <Insert the path of the 'results' folder>

    # Carica il grafo dal dataset
    G = load_graph_from_gpkg(file_path, layer_name)

    # Trova i nodi con il minor numero di vicini
    low_degree_nodes = nodes_with_less_neighbors(G)

    # Crea il grafico e salva l'immagine
    plot_graph_with_low_degree_nodes(G, low_degree_nodes, output_image)
