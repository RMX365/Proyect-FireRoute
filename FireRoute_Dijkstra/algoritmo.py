# algoritmo.py  ->  VERSIÓN 1: DIJKSTRA (estrategia voraz)
"""
Idea (voraz): en cada paso sacamos de la cola de prioridad el nodo con MENOR
tiempo acumulado desde la estación. Esa decisión local ya es definitiva:
cuando un nodo sale de la cola, su costo es el mínimo y no cambia más.

Requisito: los costos (minutos) nunca son negativos.
NO usa las coordenadas del destino (por eso explora en todas direcciones).

Complejidad: O((V + E) log V) con cola de prioridad (heapq)
"""
import heapq

NOMBRE_ALGORITMO = "Dijkstra (voraz)"


def buscar_ruta(grafo, coords, inicio, destino, vel_max, mostrar_pasos=False):
    """Devuelve (ruta, costo_minutos, nodos_explorados).
    Si no hay camino devuelve (None, inf, nodos_explorados).
    (coords y vel_max se reciben para tener la MISMA firma que la versión A*)"""
    if inicio not in grafo or destino not in grafo:
        # Entrada inválida (nodo inexistente): no se lanza KeyError, se avisa "sin ruta"
        return None, float("inf"), 0
    costos = {}
    for nodo in grafo:
        costos[nodo] = float("inf")
    costos[inicio] = 0
    anterior = {}                     # para reconstruir la ruta
    heap = [(0, inicio)]              # (tiempo acumulado, nodo)
    explorados = 0
    if mostrar_pasos:
        print(f"Nodo de inicio: {inicio}")

    while heap:
        costo_actual, nodo_actual = heapq.heappop(heap)
        # Si sacamos un dato viejo (ya hay un camino mejor) lo ignoramos
        if costo_actual > costos[nodo_actual]:
            continue
        explorados += 1
        if mostrar_pasos:
            print(f"Visitando {nodo_actual} con tiempo {costo_actual:.2f} min")
        if nodo_actual == destino:    # llegamos: ya es el camino mínimo
            break
        for vecino, peso in grafo[nodo_actual]:
            nuevo_costo = costo_actual + peso
            if nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                anterior[vecino] = nodo_actual
                heapq.heappush(heap, (nuevo_costo, vecino))
                if mostrar_pasos:
                    print(f"   Actualizado {vecino} a {nuevo_costo:.2f} min")

    if costos[destino] == float("inf"):
        return None, float("inf"), explorados
    return reconstruir_ruta(anterior, inicio, destino), costos[destino], explorados


def reconstruir_ruta(anterior, inicio, destino):
    """Va de atrás hacia adelante usando el diccionario 'anterior'"""
    ruta = [destino]
    while ruta[-1] != inicio:
        ruta.append(anterior[ruta[-1]])
    ruta.reverse()
    return ruta
