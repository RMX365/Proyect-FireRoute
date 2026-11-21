"""R5 — A* (algoritmo elegido). Mismo contrato que Dijkstra + coordenadas y vmax."""
from __future__ import annotations

import heapq
import time
from math import inf

from .common import Adj, Coords, Result, haversine_m, not_found, reconstruct_path


def heuristic(coords: Coords, n: int, goal: int, vmax_ms: float) -> float:
    """h(n) = distancia en línea recta / velocidad máxima  (admisible y consistente si costo >= d/vmax)."""
    return haversine_m(coords[n], coords[goal]) / vmax_ms


def astar(adj: Adj, coords: Coords, start: int, goal: int, vmax_ms: float) -> Result:
    """TODO (R5): igual que Dijkstra pero la cola ordena por f(n) = g(n) + h(n).

    Con h = 0 debe comportarse como Dijkstra (útil para depurar).
    explored: nodos cerrados (extraídos de la cola y no obsoletos).
    """
    t0 = time.perf_counter()

    if start not in adj or goal not in adj:
        return not_found(0, (time.perf_counter() - t0) * 1000.0)

    g_score: dict[int, float] = {start: 0.0}
    parent: dict[int, int] = {}
    closed: set[int] = set()
    explored = 0

    h0 = heuristic(coords, start, goal, vmax_ms) if vmax_ms > 0 else 0.0
    heap: list[tuple[float, float, int]] = [(h0, 0.0, start)]

    while heap:
        f_curr, g_curr, u = heapq.heappop(heap)

        if u in closed:
            continue

        closed.add(u)
        explored += 1

        if u == goal:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            path = reconstruct_path(parent, start, goal)
            return Result(
                cost=g_curr,
                path=path,
                explored=explored,
                time_ms=elapsed_ms,
            )

        for v, weight in adj.get(u, []):
            if weight == inf or v in closed:
                continue

            tentative_g = g_curr + weight
            if tentative_g < g_score.get(v, inf):
                g_score[v] = tentative_g
                parent[v] = u
                h_v = heuristic(coords, v, goal, vmax_ms) if vmax_ms > 0 else 0.0
                heapq.heappush(heap, (tentative_g + h_v, tentative_g, v))

    return not_found(explored, (time.perf_counter() - t0) * 1000.0)