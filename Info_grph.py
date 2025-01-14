import geopandas as gpd
import fiona
import pandas as pd
import matplotlib.pyplot as plt

# File path per il dataset filtrato
gpkg_file = <Insert the filtered dataset's path .gpkg>

# Elenca tutti i layer nel GeoPackage
layers = fiona.listlayers(gpkg_file)

# Inizializza una lista per salvare le informazioni sui layer
layer_info = []

# Processa ogni layer
for layer in layers:
    # Carica il layer come GeoDataFrame
    gdf = gpd.read_file(gpkg_file, layer=layer)

    # Colleziona informazioni sul layer
    layer_info.append({
        'Layer': layer,
        'Number of Rows': len(gdf),
        'Number of Columns': len(gdf.columns),
        'Non-Zero Values': gdf.notnull().sum().sum()
    })

# Converte le informazioni raccolte in un DataFrame
layer_info_df = pd.DataFrame(layer_info)

# Plotta la tabella riepilogativa come immagine
fig, ax = plt.subplots(figsize=(8, len(layers) * 0.5))
ax.axis('off')  # Disattiva gli assi

table = ax.table(cellText=layer_info_df.values, colLabels=layer_info_df.columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(layer_info_df.columns))))

# Salva la tabella come immagine
output_image_path = <Insert the path of the 'results' folder>
plt.savefig(output_image_path, dpi=300, bbox_inches='tight')

# Mostra conferma
print(f"Tabella salvata come immagine in: {output_image_path}")

# Carica e stampa informazioni sul layer "lines"
gdf_lines = gpd.read_file(gpkg_file, layer="edges")  # Cambiato da "lines" a "edges" se necessario
print(f"Numero di righe (archi): {len(gdf_lines)}")
