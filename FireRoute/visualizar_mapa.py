


import matplotlib.pyplot as plt
import networkx as nx

from fireroute.graph import load_graph

# Cargar el mapa de Trujillo
graph, coords, vmax_ms = load_graph()

print("Visualizando mapa de Trujillo...")

# Coordenadas para dibujar el grafo
pos = {
    nodo: (lon, lat)
    for nodo, (lat, lon) in coords.items()
}

plt.figure(figsize=(12, 10))

# Dibujar las calles
nx.draw_networkx_edges(
    graph,
    pos,
    edge_color="blue",
    width=0.8,
    arrows=True,
    arrowsize=6
)

# Dibujar las intersecciones
nx.draw_networkx_nodes(
    graph,
    pos,
    node_size=5,
    node_color="red"
)

plt.title("FireRoute - Mapa de Trujillo")
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.axis("equal")
plt.grid(True, alpha=0.3)

# Guardar imagen del mapa
plt.savefig(
    "data/mapa_trujillo.png",
    dpi=300,
    bbox_inches="tight"
)

# Mostrar mapa
plt.show()
