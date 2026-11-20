

from fireroute.graph import load_graph

graph, coords, vmax_ms = load_graph()

latitudes = [lat for lat, lon in coords.values()]
longitudes = [lon for lat, lon in coords.values()]

print("=== COBERTURA DEL MAPA ===")
print("Nodos:", graph.number_of_nodes())
print("Aristas:", graph.number_of_edges())

print("\nLIMITES GEOGRAFICOS")
print("Latitud minima:", min(latitudes))
print("Latitud maxima:", max(latitudes))
print("Longitud minima:", min(longitudes))
print("Longitud maxima:", max(longitudes))

print("\nVELOCIDAD MAXIMA")
print(vmax_ms, "m/s")

print("\nCOBERTURA CALCULADA")
