import folium
import geopandas as gpd
from shapely.geometry import LineString

# Percorso al file di Ancona
gpkg_file = <Insert the dataset's path .gpkg>

def load_graph_from_gpkg_interactive(gpkg_file, layer_name="lines"):
    """
    Carica un grafo a partire da un file geopackage e restituisce una lista di nodi e archi.
    """
    gdf = gpd.read_file(gpkg_file, layer=layer_name)
    gdf = gdf.to_crs(epsg=4326)  # Converte il CRS in WGS84

    nodes = set()
    edges = []
    for _, row in gdf.iterrows():
        line = row.geometry
        if isinstance(line, LineString):
            coords = list(line.coords)
            for i in range(len(coords) - 1):
                edges.append((coords[i], coords[i + 1]))
                nodes.add(coords[i])
                nodes.add(coords[i + 1])
    return list(nodes), edges

def plot_graph_on_interactive_map(nodes, edges, location=(43.615, 13.518), zoom_start=14):
    """
    Disegna il grafo su una mappa interattiva con Folium.
    """
    # Crea la mappa centrata su una posizione specifica
    m = folium.Map(location=location, zoom_start=zoom_start)

    # Aggiungi gli archi del grafo
    for edge in edges:
        line = [edge[0][::-1], edge[1][::-1]]  # Inverti ordine per (lat, lon)
        folium.PolyLine(locations=line, color="blue", weight=2).add_to(m)

    # Aggiungi i nodi del grafo
    for node in nodes:
        folium.CircleMarker(
            location=node[::-1],  # Inverti ordine per (lat, lon)
            radius=2,
            color="red",
            fill=True,
            fill_opacity=0.7
        ).add_to(m)

    return m

if __name__ == "__main__":
    try:
        # Carica i nodi e gli archi dal file .gpkg
        nodes, edges = load_graph_from_gpkg_interactive(gpkg_file, layer_name="lines")

        # Calcola il numero di nodi e archi
        num_nodes = len(nodes)
        num_edges = len(edges)

        print(f"Numero di nodi: {num_nodes}")
        print(f"Numero di archi: {num_edges}")

        # Crea una mappa interattiva centrata su Ancona
        map_graph = plot_graph_on_interactive_map(nodes, edges, location=(43.615, 13.518), zoom_start=14)

        # Salva la mappa come file HTML
        map_graph.save("grafo_ancona.html")
        print("Mappa interattiva salvata in 'grafo_ancona.html'")
    except Exception as e:
        print("Errore:", e)
