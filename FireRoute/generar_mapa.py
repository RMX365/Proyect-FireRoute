

from fireroute.graph import (
    build_trujillo_graph,
    save_graph,
    load_graph
)

print("================================")
print("     FIREROUTE - R2 MAPA")
print("================================")

# PASO 1: Construir el mapa
graph, coords, vmax_ms = build_trujillo_graph()

# PASO 2: Guardar el mapa
save_graph(graph, coords, vmax_ms)

# PASO 3: Mostrar información
print("\nRESULTADOS DEL MAPA")
print("-------------------------------")
print("Cantidad de nodos:", graph.number_of_nodes())
print("Cantidad de aristas:", graph.number_of_edges())
print("Velocidad máxima:", vmax_ms, "m/s")

# PASO 4: Comprobar que se puede cargar
grafo_cargado, coordenadas, velocidad = load_graph()

assert set(grafo_cargado.nodes) == set(
    range(len(coordenadas))
)
assert velocidad > 0

print("\nMapa cargado correctamente.")
print("PROYECTO R2 EJECUTADO CON EXITO")
