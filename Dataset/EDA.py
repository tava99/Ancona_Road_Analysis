import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import geopandas as gpd
import pandas as pd

# Carica il dataset
file_path = <Insert the filtered dataset's path .gpkg>
data = gpd.read_file(file_path)

# Filtra i dati per 'highway'
highway_data = data[~data['highway'].isnull()]

# Conta le occorrenze di ogni categoria di 'highway'
highway_counts = highway_data['highway'].value_counts()
highway_categories = highway_counts.index

# Colori associati alle categorie
colors = plt.cm.tab20.colors
category_colors = {category: colors[i % len(colors)] for i, category in enumerate(highway_categories)}

# Crea una figura per la mappa
plt.figure(figsize=(14, 12))
for category in highway_categories:
    subset = highway_data[highway_data['highway'] == category]
    plt.scatter(subset.geometry.x, subset.geometry.y, s=15,
                color=category_colors[category], label=category, alpha=0.6)

# Configurazione del grafico della mappa
plt.title('Distribuzione geografica dei nodi', fontsize=16)
plt.xlabel('Longitudine', fontsize=12)
plt.ylabel('Latitudine', fontsize=12)
plt.grid(True)
plt.legend(title="Highway", fontsize=10, loc="upper right", markerscale=2)

# Salva e mostra la mappa
plt.tight_layout()
plt.savefig(r"C:\Users\pc\PycharmProjects\Ancona_Road_Analysis2\results\map_highway.png") 
plt.show()

# Crea una figura separata per la tabella
fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')  

# Crea una tabella  con categorie e conteggi
table_data = pd.DataFrame({
    "Categoria": highway_counts.index,
    "Conteggio": highway_counts.values,
})

table = ax.table(
    cellText=table_data.values,
    colLabels=table_data.columns,
    loc='center',
    cellLoc='center',
)
table.auto_set_font_size(False)  # Disattiva il ridimensionamento automatico del font
table.set_fontsize(12)  # Imposta una dimensione del font leggibile
table.auto_set_column_width(col=list(range(len(table_data.columns))))

# Salva la tabella come immagine
output_path_table = <Insert the path of the 'results' folder>
plt.tight_layout()
plt.savefig(output_path_table)
plt.show()

print(f"La mappa e la tabella sono state salvate nella cartella 'results'")
