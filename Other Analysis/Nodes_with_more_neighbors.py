import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import os
from shapely.geometry import LineString


def load_graph_from_gpkg(file_path, layer_name="edges"):
    """
    Carica un grafo da un file GeoPackage.

    :param file_path: Percorso del file GeoPackage.
    :param layer_name: Nome del layer da utilizzare.
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


def nodes_with_more_neighbors(G):
    """
    Trova i nodi con il maggior numero di vicini.

    :param G: Grafo NetworkX.
    :return: Lista di nodi con il maggior numero di vicini.
    """
    degrees = dict(G.degree())
    max_neighbors = max(degrees.values())

    nodes_max = [node for node, degree in degrees.items() if degree == max_neighbors]

    print(f"Nodi con più vicini ({max_neighbors}): {nodes_max}")

    return nodes_max


def plot_graph_with_high_degree_nodes(G, high_degree_nodes, output_path):
    """
    Crea un'immagine del grafo con i nodi ad alto grado evidenziati.

    :param G: Grafo NetworkX.
    :param high_degree_nodes: Lista di nodi ad alto grado.
    :param output_path: Percorso di output per salvare l'immagine.
    """
    pos = {node: (node[0], node[1]) for node in G.nodes}

    plt.figure(figsize=(10, 10))

    # Disegna il grafo completo
    nx.draw(G, pos, node_size=10, edge_color='gray', alpha=0.7, with_labels=False)

    # Evidenzia i nodi con più vicini
    nx.draw_networkx_nodes(G, pos, nodelist=high_degree_nodes, node_size=50, node_color='red')

    plt.title("Grafo con nodi ad alto grado evidenziati")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Immagine salvata in {output_path}")


if __name__ == "__main__":
    # Configura i percorsi
    file_path = r"C:\Users\pc\PycharmProjects\Social_Network_Analysis\data\filtered_ancona.gpkg"
    layer_name = "edges"  # Sostituisci con il nome corretto del layer
    output_image = r"C:\Users\pc\PycharmProjects\Social_Network_Analysis\results\graph_high_degree_nodes.png"

    # Carica il grafo dal dataset
    G = load_graph_from_gpkg(file_path, layer_name)

    # Trova i nodi con il maggior numero di vicini
    high_degree_nodes = nodes_with_more_neighbors(G)

    # Crea il grafico e salva l'immagine
    plot_graph_with_high_degree_nodes(G, high_degree_nodes, output_image)
