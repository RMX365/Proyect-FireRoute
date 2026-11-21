# algoritmo.py  ->  VERSIÓN 2: A* (A-star)
"""
Idea: igual que Dijkstra pero la cola de prioridad se ordena por
        f(n) = g(n) + h(n)
  g(n) = tiempo real acumulado desde la estación hasta n
  h(n) = tiempo ESTIMADO desde n hasta el incendio
       = distancia en línea recta / velocidad máxima permitida (en minutos)

La heurística es ADMISIBLE: nunca sobreestima, porque ningún tramo se recorre
más rápido que VEL_MAX y la línea recta es lo más corto posible
(y el tráfico y las penalizaciones solo SUMAN tiempo).
Por eso A* también garantiza la ruta de menor tiempo, pero explora menos nodos.
Con h(n) = 0 se comporta exactamente como Dijkstra.

Complejidad: O((V + E) log V) en el peor caso (igual que Dijkstra)
"""
import heapq
import math

NOMBRE_ALGORITMO = "A* (A-star)"


def heuristica(coords, nodo, destino, vel_max):
    """Minutos estimados en línea recta a velocidad máxima"""
    x1, y1 = coords[nodo]
    x2, y2 = coords[destino]
    km = math.hypot(x1 - x2, y1 - y2)
    return km / vel_max * 60


def buscar_ruta(grafo, coords, inicio, destino, vel_max, mostrar_pasos=False):
    """Devuelve (ruta, costo_minutos, nodos_explorados).
    Si no hay camino devuelve (None, inf, nodos_explorados)."""
    if inicio not in grafo or destino not in grafo:
        # Entrada inválida (nodo inexistente): no se lanza KeyError, se avisa "sin ruta"
        # (se valida ANTES de llamar a heuristica(), que también usaría coords[destino])
        return None, float("inf"), 0
    g = {}
    for nodo in grafo:
        g[nodo] = float("inf")
    g[inicio] = 0
    anterior = {}
    f_inicial = heuristica(coords, inicio, destino, vel_max)
    heap = [(f_inicial, 0, inicio)]   # (f, g, nodo)
    explorados = 0
    if mostrar_pasos:
        print(f"Nodo de inicio: {inicio}  | destino: {destino}")

    while heap:
        f_actual, g_actual, nodo_actual = heapq.heappop(heap)
        # Dato viejo (ya hay un camino mejor a este nodo): se ignora
        if g_actual > g[nodo_actual]:
            continue
        explorados += 1
        if mostrar_pasos:
            print(f"Visitando {nodo_actual} con g={g_actual:.2f} y f={f_actual:.2f} min")
        if nodo_actual == destino:
            break
        for vecino, peso in grafo[nodo_actual]:
            nuevo_g = g_actual + peso
            if nuevo_g < g[vecino]:
                g[vecino] = nuevo_g
                anterior[vecino] = nodo_actual
                f = nuevo_g + heuristica(coords, vecino, destino, vel_max)
                heapq.heappush(heap, (f, nuevo_g, vecino))
                if mostrar_pasos:
                    print(f"   Actualizado {vecino}: g={nuevo_g:.2f}, f={f:.2f} min")

    if g[destino] == float("inf"):
        return None, float("inf"), explorados
    return reconstruir_ruta(anterior, inicio, destino), g[destino], explorados


def reconstruir_ruta(anterior, inicio, destino):
    """Va de atrás hacia adelante usando el diccionario 'anterior'"""
    ruta = [destino]
    while ruta[-1] != inicio:
        ruta.append(anterior[ruta[-1]])
    ruta.reverse()
    return ruta
