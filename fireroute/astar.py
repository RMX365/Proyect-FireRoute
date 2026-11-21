"""R5 – A* (algoritmo elegido). Mismo contrato que Dijkstra + coordenadas y vmax."""
from __future__ import annotations

import heapq  # noqa: F401
import time   # noqa: F401

from .common import Adj, Coords, Result, haversine_m, not_found, reconstruct_path  # noqa: F401


def heuristic(coords: Coords, n: int, goal: int, vmax_ms: float) -> float:
    """h(n) = distancia en línea recta / velocidad máxima  (admisible y consistente si costo >= d/vmax)."""
    return haversine_m(coords[n], coords[goal]) / vmax_ms


def astar(adj: Adj, coords: Coords, start: int, goal: int, vmax_ms: float) -> Result:
    """TODO (R5): igual que Dijkstra pero la cola ordena por f(n) = g(n) + h(n).

    Con h = 0 debe comportarse como Dijkstra (útil para depurar).
    explored: nodos cerrados (extraídos de la cola y no obsoletos).
    """
    raise NotImplementedError
