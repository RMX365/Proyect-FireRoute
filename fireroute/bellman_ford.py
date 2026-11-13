"""R6 - TERCER ALGORITMO para la tabla comparativa 4.2 (programación dinámica).
"""
from __future__ import annotations

import time  # noqa: F401

from .common import Adj, Result, not_found, reconstruct_path  # noqa: F401
INF = float("inf")

def bellman_ford(adj: Adj, start: int, goal: int) -> Result:
    """TODO (R6): menor costo de start a goal relajando todas las aristas hasta V-1 veces.

    Para Bellman-Ford, explored = número de relajaciones evaluadas (NO es comparable 1 a 1 con
    los nodos de Dijkstra/A*; dejado documentado en el informe). Cortar antes si una pasada no mejora nada.
    """
    # 1. Inicialización: solo el origen es alcanzable (costo 0).
    t0 = time.perf_counter()
    dist = {u: INF for u in adj}            # mejor costo conocido a cada nodo
    prev: dict[int, int] = {}               # prev[v] = nodo desde el que se llegó a v
    dist[start] = 0.0
    explored = 0

    # 2. Relajación repetida de todas las aristas (máximo V - 1 pasadas).
    for _ in range(len(adj) - 1):               # máximo V - 1 pasadas
        mejoro = False
        for u, vecinos in adj.items():
            if dist[u] == INF:                  # aún inalcanzable: se omite
                continue
            for v, w in vecinos:
                explored += 1                   # una relajación evaluada
                if dist[u] + w < dist[v]:       # ¿pasar por u mejora el costo de v?
                    dist[v], prev[v], mejoro = dist[u] + w, u, True
        if not mejoro:                          # corte anticipado
            break

    # 3. Entregar el resultado en el formato del proyecto.
    time_ms = (time.perf_counter() - t0) * 1000
    if dist[goal] == INF:
        return not_found(explored, time_ms)     # sin ruta: path [] y costo infinito
    return Result(reconstruct_path(prev, start, goal), dist[goal], explored, time_ms)