import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString, MultiLineString
import matplotlib.pyplot as plt
import os


def analyze_ego_networks_from_geometry(file_path, layer, ego_node, radius=1):
    """
    Analizza le ego networks usando dati geometrici per estrarre nodi e archi.

    :param file_path: Percorso del file geopackage contenente i dati.
    :param layer: Nome del layer da utilizzare nel file geopackage (es: 'edges').
    :param ego_node: Nodo di cui calcolare la ego network.
    :param radius: Raggio della ego network (default = 1).
    """
    # Leggi il layer specificato dal file geopackage
    gdf = gpd.read_file(file_path, layer=layer)

    print(f"Dataset caricato dal layer '{layer}': {len(gdf)} righe.")

    # Verifica che la colonna 'geometry' esista
    if 'geometry' not in gdf.columns:
        print("Errore: Il dataset non contiene una colonna 'geometry'.")
        return

    # Estrai nodi e archi dalla colonna 'geometry'
    edges = []
    for _, row in gdf.iterrows():
        geom = row['geometry']
        if isinstance(geom, LineString):
            coords = list(geom.coords)
            edges.append((coords[0], coords[-1]))
        elif isinstance(geom, MultiLineString):
            for line in geom:
                coords = list(line.coords)
                edges.append((coords[0], coords[-1]))

    # Crea un grafo da archi
    G = nx.Graph()
    G.add_edges_from(edges)

    print(f"Il grafo contiene {G.number_of_nodes()} nodi e {G.number_of_edges()} archi.")

    # Controlla se il nodo esiste
    if ego_node not in G:
        print(f"Errore: il nodo '{ego_node}' non è presente nel grafo.")
        print("Ecco un esempio di nodi disponibili:")
        print(list(G.nodes)[:100])
        return

    # Estrazione della ego network
    ego_net = nx.ego_graph(G, n=ego_node, radius=radius)

    print(f"L'ego network del nodo '{ego_node}' (raggio={radius}) contiene:")
    print(f"- {ego_net.number_of_nodes()} nodi")
    print(f"- {ego_net.number_of_edges()} archi")

    # Disegno della ego network
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(ego_net)
    nx.draw(ego_net, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10)
    plt.title(f"Ego Network di '{ego_node}' (raggio={radius})")

    # Salvataggio dell'immagine
    output_dir = r"C:\Users\pc\PycharmProjects\Social_Network_Analysis\results"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"ego_network.png")
    plt.savefig(output_file)
    print(f"L'immagine della ego network è stata salvata in: {output_file}")

    # Mostra il grafico
    plt.show()


# Configurazione del file e layer
file_path = r"C:\Users\pc\PycharmProjects\Social_Network_Analysis\data\filtered_ancona.gpkg"
layer = "edges"  # Specifica il layer degli archi
ego_node = ((13.507047, 43.6135432))  # Esempio di nodo come coordinate (longitudine, latitudine)
radius = 3  # Scegliere il raggio

# Esecuzione dell'analisi
analyze_ego_networks_from_geometry(file_path, layer, ego_node, radius)

