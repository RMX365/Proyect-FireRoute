""""R4 – DIJKSTRA (estrategia voraz). Algoritmo de referencia."""
from __future__ import annotations

import heapq
import math
import time

from .common import Adj, Result, not_found, reconstruct_path


def dijkstra(adj: Adj, start: int, goal: int) -> Result:
    """Ruta de menor costo (segundos) de start a goal."""
    t0 = time.perf_counter()

    dist: dict[int, float] = {start: 0.0}
    prev: dict[int, int] = {}
    closed: set[int] = set()
    heap: list[tuple[float, int]] = [(0.0, start)]
    explored = 0

    while heap:
        cost, u = heapq.heappop(heap)
        if u in closed:            # entrada obsoleta
            continue
        closed.add(u)
        explored += 1

        if u == goal:
            time_ms = (time.perf_counter() - t0) * 1000
            return Result(
                path=reconstruct_path(prev, start, goal),
                cost=cost,
                explored=explored,
                time_ms=time_ms,
            )

        for v, w in adj.get(u, ()):
            if v in closed:
                continue
            nd = cost + w
            if nd < dist.get(v, math.inf):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    time_ms = (time.perf_counter() - t0) * 1000
    return not_found(explored, time_ms)
