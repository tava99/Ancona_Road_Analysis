import geopandas as gpd
from shapely.geometry import Polygon

# Percorso del file e definizione dell'output
gpkg_path = r"C:\\Users\\pc\\OneDrive\\Desktop\\Magistrale Ancona\\Data science\\Progetto\\Networkx\\042002_Ancona-2024-11-12T08Z.gpkg"
output_path = r"C:\\Users\\pc\\OneDrive\\Desktop\\Magistrale Ancona\\Data science\\Progetto\\Networkx\\filtered_ancona.gpkg"

# Definizione del poligono per la zona centrale di Ancona
central_zone_coords = [
    (13.463565, 43.608519),
    (13.528788, 43.583681),
    (13.548080, 43.605045),
    (13.526033, 43.624111),
    (13.484141, 43.629730),
    (13.463565, 43.608519)
]
central_zone = Polygon(central_zone_coords)

# Caricamento dei layer corretti
nodes = gpd.read_file(gpkg_path, layer='points')  # Nodi: layer 'points'
edges = gpd.read_file(gpkg_path, layer='lines')   # Archi: layer 'lines'

# Assicurarsi che i dati abbiano lo stesso sistema di coordinate (CRS)
if edges.crs != nodes.crs:
    raise ValueError("I layer di nodi e archi hanno CRS diversi.")

# Filtrare i nodi e gli archi all'interno del poligono
filtered_nodes = nodes[nodes.geometry.within(central_zone)]
filtered_edges = edges[edges.geometry.within(central_zone)]

# Salvare i dati filtrati
filtered_nodes.to_file(output_path, layer='nodes', driver='GPKG')
filtered_edges.to_file(output_path, layer='edges', driver='GPKG')

print("Filtraggio completato. I dati sono stati salvati in:", output_path)
