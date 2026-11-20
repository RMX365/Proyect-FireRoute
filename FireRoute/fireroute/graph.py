

from pathlib import Path
import pickle

import networkx as nx
import osmnx as ox

# Carpeta principal del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Mapa descargado desde Google Colab
GRAPHML_PATH = BASE_DIR / "data" / "trujillo.graphml"

# Mapa final para el equipo
MAP_PATH = BASE_DIR / "data" / "trujillo_graph.pkl"


def build_trujillo_graph():
    """
    Construye el grafo dirigido de Trujillo
    usando el archivo GraphML descargado.
    """

    print("Cargando calles de Trujillo...")

    if not GRAPHML_PATH.exists():
        raise FileNotFoundError(
            f"No se encuentra: {GRAPHML_PATH}"
        )

    # Cargar red vial real
    G = ox.io.load_graphml(filepath=GRAPHML_PATH)

    # Asignar velocidades y tiempos
    G = ox.routing.add_edge_speeds(
        G,
        fallback=30
    )
    G = ox.routing.add_edge_travel_times(G)

    # Numerar nodos consecutivamente
    mapping = {
        nodo: i
        for i, nodo in enumerate(G.nodes)
    }

    # Coordenadas (latitud, longitud)
    coords = {
        mapping[nodo]: (
            float(G.nodes[nodo]["y"]),
            float(G.nodes[nodo]["x"])
        )
        for nodo in G.nodes
    }

    # Crear grafo dirigido
    graph = nx.DiGraph()
    graph.add_nodes_from(range(len(mapping)))

    vmax_ms = 0.0

    for u, v, datos in G.edges(data=True):

        origen = mapping[u]
        destino = mapping[v]

        longitud = float(datos["length"])
        velocidad = float(datos["speed_kph"]) / 3.6

        if velocidad <= 0:
            raise ValueError(
                "Se encontró una velocidad no válida"
            )

        # Tiempo en segundos
        costo = longitud / velocidad

        vmax_ms = max(vmax_ms, velocidad)

        # Mantener el trayecto más rápido
        if (
            not graph.has_edge(origen, destino)
            or costo < graph[origen][destino]["weight"]
        ):
            graph.add_edge(
                origen,
                destino,
                weight=costo,
                length=longitud,
                speed_ms=velocidad
            )

    print("Mapa construido correctamente.")

    return graph, coords, vmax_ms


def save_graph(graph, coords, vmax_ms):
    """Guardar el mapa final en data."""

    MAP_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    datos = {
        "graph": graph,
        "coords": coords,
        "vmax_ms": vmax_ms
    }

    with open(MAP_PATH, "wb") as archivo:
        pickle.dump(datos, archivo)

    print("Mapa guardado correctamente.")


def load_graph():
    """Cargar el mapa final guardado."""

    with open(MAP_PATH, "rb") as archivo:
        datos = pickle.load(archivo)

    return (
        datos["graph"],
        datos["coords"],
        datos["vmax_ms"]
    )
