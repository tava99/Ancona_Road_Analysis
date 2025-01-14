import geopandas as gpd
import networkx as nx
from shapely.geometry import Point
import matplotlib.pyplot as plt
import os

# Percorso al file GeoPackage
path = <Insert the filtered dataset's path .gpkg>

# Coordinate dei nodi di partenza e arrivo
start_node = (13.507047, 43.6135432)  # (longitudine, latitudine)
end_node = (13.5024282, 43.6084696)  # (longitudine, latitudine)

# Caricamento dei layer
nodes = gpd.read_file(path, layer='nodes')
edges = gpd.read_file(path, layer='edges')

# Converte i layer in un sistema di riferimento proiettato
projected_crs = "EPSG:32633"  # UTM zona 33N
nodes = nodes.to_crs(projected_crs)
edges = edges.to_crs(projected_crs)

# Creazione delle colonne 'source', 'target' e 'weight'
edges['source'] = edges.geometry.apply(lambda x: Point(x.coords[0]))  # Nodo iniziale
edges['target'] = edges.geometry.apply(lambda x: Point(x.coords[-1]))  # Nodo finale
edges['weight'] = edges.geometry.length  # Peso basato sulla lunghezza della geometria

# Mappatura dei nodi sorgente e destinazione con gli ID dai nodi
def find_closest_node(point, nodes_gdf):
    """Trova l'ID del nodo più vicino a un punto dato."""
    nodes_gdf['distance'] = nodes_gdf.geometry.distance(point)
    closest_node = nodes_gdf.loc[nodes_gdf['distance'].idxmin()]
    return closest_node['osm_id']  # Usa 'osm_id' come identificativo

edges['source'] = edges['source'].apply(lambda point: find_closest_node(point, nodes))
edges['target'] = edges['target'].apply(lambda point: find_closest_node(point, nodes))

# Creazione del grafo
G = nx.DiGraph()

# Aggiunta dei nodi al grafo
for _, row in nodes.iterrows():
    G.add_node(row['osm_id'], pos=(row.geometry.x, row.geometry.y))  # Usa 'osm_id' come identificativo

# Aggiunta degli archi al grafo
for _, edge in edges.iterrows():
    G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

# Converte le coordinate dei nodi di partenza e arrivo in punti nel CRS proiettato
start_point = gpd.GeoSeries([Point(start_node)], crs="EPSG:4326").to_crs(projected_crs).geometry[0]
end_point = gpd.GeoSeries([Point(end_node)], crs="EPSG:4326").to_crs(projected_crs).geometry[0]

# Trova i nodi più vicini alle coordinate di partenza e arrivo
start_node_id = find_closest_node(start_point, nodes)
end_node_id = find_closest_node(end_point, nodes)

print(f"Nodo di partenza più vicino: {start_node_id}")
print(f"Nodo di arrivo più vicino: {end_node_id}")

# Calcolo del percorso più breve
try:
    shortest_path = nx.shortest_path(G, source=start_node_id, target=end_node_id, weight='weight')
    shortest_path_length = nx.shortest_path_length(G, source=start_node_id, target=end_node_id, weight='weight')

    print(f"Percorso più breve: {shortest_path}")
    print(f"Lunghezza del percorso più breve: {shortest_path_length}")

    # Estrai le coordinate dei nodi nel percorso
    shortest_path_coords = [(G.nodes[node]['pos'][0], G.nodes[node]['pos'][1]) for node in shortest_path]
    print("Coordinate del percorso più breve:")
    for coord in shortest_path_coords:
        print(coord)

    # Directory di output per le immagini
    output_dir = <Insert the path of the 'results' folder>
    os.makedirs(output_dir, exist_ok=True)

    # Disegna il grafo e il percorso più breve
    plt.figure(figsize=(10, 10))
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, node_size=10, edge_color='gray', alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='red', node_size=50)
    nx.draw_networkx_edges(G, pos, edgelist=list(zip(shortest_path, shortest_path[1:])), edge_color='blue', width=2)
    plt.title("Grafo e percorso più breve")
    graph_path = os.path.join(output_dir, "graph_shortest_path.png")
    plt.savefig(graph_path)
    print(f"Il grafo è stato salvato in: {graph_path}")
    plt.show()

    # Calcolo e visualizzazione della distribuzione delle shortest path dal nodo di partenza
    lengths = nx.single_source_dijkstra_path_length(G, source=start_node_id, weight='weight')
    plt.figure(figsize=(10, 6))
    plt.hist(lengths.values(), bins=30, edgecolor='black')
    plt.title("Distribuzione delle shortest path dal nodo di partenza")
    plt.xlabel("Lunghezza del percorso")
    plt.ylabel("Frequenza")
    histogram_path = os.path.join(output_dir, "shortest_path_distribution.png")
    plt.savefig(histogram_path)
    print(f"L'istogramma è stato salvato in: {histogram_path}")
    plt.show()

except nx.NetworkXNoPath:
    print(f"Non esiste un percorso tra il nodo {start_node_id} e il nodo {end_node_id}.")
