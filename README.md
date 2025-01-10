
<div align="center"> 
  <img src="Ancona_NetworkX.png" alt="Logo project NetworkX" width="200" height="200"/>
</div>

<h1 align="center">Social Network Analysis and NetworkX</h1>

# 🗺️ Road Network of Ancona

This repository contains the analysis and scripts related to the road network of Ancona, based on the **Estratti OpenStreetMap (OSM) Italia** dataset. The project uses the road network graph for analysis and visualization purposes.

---

## 📊 Dataset

The dataset of the Ancona road network is available at the following link:  
🌐 [**Estratti OpenStreetMap Italia - Wikimedia Italia**](https://osmit-estratti.wmcloud.org/).

---

## 🚀 Usage Instructions

Follow these instructions to make the best use of this project. 🛠️

### 📥 Download the Dataset  
To download the dataset related to the Ancona road network:  
1️⃣ Select the region **Marche**.  
2️⃣ Choose the province **Ancona**.  
3️⃣ Finally, select the city **Ancona**.  
4️⃣ Save the file from the right column by clicking on the **💾 GPKG** button.

---

### 📦 Installing Dependencies

To run the project, it is necessary to install some essential Python libraries.

The required libraries are:  
- **fiona**  
- **folium**  
- **geopandas**  
- **matplotlib**  
- **networkx**  
- **numpy**  
- **osmnx**  
- **pandas**  
- **pillow**  
- **pyogrio**  
- **tqdm**  

You can install them one by one by running the following command in the terminal:

```bash
pip install library_name
```

For example, to install **fiona**:  

```bash
pip install fiona
```
---

### 🌐 Visualizing the Graph and Dataset Information

🔍 **Exploring the dataset** is easy! Follow these steps:

1. **📈 Visualizing the Interactive Graph**  
   Run the file `Graph_Ancona.py` to generate and visualize the interactive graph related to the first point.

2. **📋 Visualizing the Information Table**  
   Run the file `Info_initial_graph.py` to display a table containing detailed information about the dataset.

---

### ✂️ Preparing the Dataset  

💡 **Before starting any analysis**, run the script **`Ancona_center.py`**.  
This script filters the dataset to include only the central area of Ancona.

➡️ You can customize the filter by directly modifying the **geographic coordinates** (longitude and latitude) in the script.

---

### 🔬 Running Analyses  

After downloading and preparing the dataset, follow these simple steps:

1️⃣ Open the script corresponding to the analysis you want to perform.  
2️⃣ Update the **initial path** in the script to point to the directory where you saved the downloaded dataset.  
3️⃣ Run the script to obtain your results! ✅

### 🧠 Overview of Scripts and Functionalities

Below is a detailed overview of the scripts in this repository and their functionalities:

---

### 🎯 **Centrality**  

- **📌 Betweenness Centrality**  
  Computes nodes' importance based on their position in the shortest paths.  
  **Code file**: `betweenness_centrality.py`
---
- **📌 Closeness Centrality**  
  Measures how close a node is to all other nodes.  
  **Code file**: `closeness_centrality.py`
---
- **📌 Degree Centrality**  
  Calculates node importance based on the number of direct connections.  
  **Code file**: `degree_centrality.py`
---
- **📌 Eigenvector Centrality**  
  Identifies influential nodes based on their neighbors' importance.  
  **Code file**: `eigenvector_centrality.py`
---

---
### 🔬 **Other Analyses**
- **🌟 Cliques**  
  Finds groups of fully connected nodes in the graph.  
  **Code file**: `cliques_analysis.py`
---
- **🌐 Ego Networks**  
  Generates subgraphs centered on a single node with its direct connections.  
  **Code file**: `ego_networks.py`
---
- **📈 Shortest Paths**  
  Identifies the shortest paths between selected pairs of nodes.  
  **Code file**: `shortest_paths.py`
---
- **🌍 Nodes with More Neighbors**  
  Identifies nodes with the highest number of direct neighbors.  
  **Code file**: `nodes_with_more_neighbors.py`
---
- **🗺️ Nodes with Less Neighbors**  
  Identifies nodes with the fewest number of direct neighbors.  
  **Code file**: `nodes_with_less_neighbors.py`
---

## 👩‍💻👨‍💻 Authors  

This project is developed and maintained by the following authors:

- **Antonio Antonini** - [GitHub Profile](https://github.com/tava99) 🌟  
- **Zazzarini Micol** - [GitHub Profile](https://github.com/MicolZazzarini) ✨  
- **Fiorani Andrea** - [GitHub Profile](https://github.com/125ade) 🚀  

---

## 📜 License  

This project is released under the **[MIT License](LICENSE)**. 📝
