import geopandas as gpd
import fiona
import pandas as pd
import matplotlib.pyplot as plt

# Percorso del file
gpkg_file = "C:\\Users\\pc\\OneDrive\\Desktop\\Magistrale Ancona\\Data science\\Progetto\\Networkx\\042002_Ancona-2024-11-12T08Z.gpkg"

# Elenco di tutti i layer nel GeoPackage
layers = fiona.listlayers(gpkg_file)

# Inizializza una lista vuota per memorizzare le informazioni sui layer
informazioni_layer = []

# Processo per ogni layer
for layer in layers:
    # Carica il layer come GeoDataFrame
    gdf = gpd.read_file(gpkg_file, layer=layer)

    # Raccogli informazioni sul layer
    informazioni_layer.append({
        'Layer': layer,
        'Numero di Righe': len(gdf),
        'Numero di Colonne': len(gdf.columns),
        'Valori Non Nulli': gdf.notnull().sum().sum()
    })

# Converti le informazioni raccolte in un DataFrame
informazioni_layer_df = pd.DataFrame(informazioni_layer)

# Crea la tabella riassuntiva come immagine
fig, ax = plt.subplots(figsize=(8, len(layers) * 0.5))
ax.axis('off')  # Disattiva gli assi

table = ax.table(cellText=informazioni_layer_df.values, colLabels=informazioni_layer_df.columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(informazioni_layer_df.columns))))

# Salva la tabella come immagine nella cartella specificata
output_path = "C:\\Users\\pc\\PycharmProjects\\Social_Network_Analysis\\results\\initial_info_table.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')

# Conferma salvataggio
print(f"Tabella salvata come '{output_path}'")
