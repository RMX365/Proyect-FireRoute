

import math
import networkx as nx
from fireroute.graph import load_graph

graph, coords, vmax_ms = load_graph()

print("=== VALIDACION FIREROUTE R2 ===")

# 1. Grafo dirigido
assert isinstance(graph, nx.DiGraph)
print("OK: Grafo dirigido")

# 2. Nodos consecutivos
n = graph.number_of_nodes()
assert set(graph.nodes) == set(range(n))
print("OK: Nodos consecutivos")

# 3. Coordenadas
assert set(coords.keys()) == set(graph.nodes)

for lat, lon in coords.values():
    assert -90 <= lat <= 90
    assert -180 <= lon <= 180

print("OK: Coordenadas validas")

# 4. Costos y velocidades
for u, v, datos in graph.edges(data=True):
    costo = datos["weight"]
    longitud = datos["length"]
    velocidad = datos["speed_ms"]

    assert costo > 0
    assert longitud > 0
    assert velocidad > 0
    assert math.isclose(
        costo,
        longitud / velocidad,
        rel_tol=1e-6
    )

print("OK: Costos en segundos")

# 5. Velocidad maxima
assert graph.number_of_edges() > 0

velocidad_maxima = max(
    datos["speed_ms"]
    for _, _, datos in graph.edges(data=True)
)

assert math.isclose(
    vmax_ms,
    velocidad_maxima,
    rel_tol=1e-6
)

print("OK: Velocidad maxima")

print("\n=== RESULTADOS ===")
print("Nodos:", graph.number_of_nodes())
print("Aristas:", graph.number_of_edges())
print("Velocidad maxima:", vmax_ms, "m/s")

print("\nVALIDACION COMPLETADA")
