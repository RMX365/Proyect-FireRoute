

import osmnx as ox

from fireroute.graph import GRAPHML_PATH, load_graph

# Cargar el mapa original de OpenStreetMap
G = ox.io.load_graphml(filepath=GRAPHML_PATH)

# Cargar el grafo procesado
graph, coords, vmax_ms = load_graph()

# Reconstruir la numeración utilizada en graph.py
mapping = {
    nodo: i
    for i, nodo in enumerate(G.nodes)
}

total = 0
correctas = 0

for u, v, datos in G.edges(data=True):
    # Revisar calles marcadas como unidireccionales
    if datos.get("oneway") is True:
        total += 1

        origen = mapping[u]
        destino = mapping[v]

        if graph.has_edge(origen, destino):
            correctas += 1

print("=== VERIFICACION DE SENTIDOS ===")
print("Aristas originales de sentido unico:", total)
print("Aristas conservadas:", correctas)

assert total == correctas, (
    "ERROR: Faltan conexiones de sentido unico"
)

print("VERIFICACION COMPLETADA")
