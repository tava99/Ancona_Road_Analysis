import geopandas as gpd
import networkx as nx
import os


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


def analyze_cliques(G, output_dir):
    """
    Analizza le clique del grafo.

    :param G: Grafo NetworkX.
    :param output_dir: Directory per salvare i risultati.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Trova tutte le clique
    cliques = list(nx.find_cliques(G))
    num_cliques = len(cliques)
    max_clique_size = max(len(c) for c in cliques)
    largest_cliques = [c for c in cliques if len(c) == max_clique_size]

    print(f"Numero totale di clique: {num_cliques}")
    print(f"Dimensione massima delle clique: {max_clique_size}")
    print(f"Clique più grandi ({max_clique_size} nodi): {largest_cliques}")

    # Salva i risultati in un file di testo
    output_file = os.path.join(output_dir, "cliques_analysis.txt")
    with open(output_file, "w") as f:
        f.write(f"Numero totale di clique: {num_cliques}\n")
        f.write(f"Dimensione massima delle clique: {max_clique_size}\n")
        f.write(f"Clique più grandi ({max_clique_size} nodi):\n")
        for clique in largest_cliques:
            f.write(f"{clique}\n")

    print(f"Analisi delle clique salvata in: {output_file}")


if __name__ == "__main__":
    # Percorso del dataset
    file_path = r"C:\Users\pc\PycharmProjects\Social_Network_Analysis\data\filtered_ancona.gpkg"
    output_dir = r"C:\Users\pc\PycharmProjects\Social_Network_Analysis\results\cliques"

    # Carica il grafo dal dataset
    G = load_graph_from_gpkg(file_path, layer_name="edges")

    # Analizza le clique
    analyze_cliques(G, output_dir)
