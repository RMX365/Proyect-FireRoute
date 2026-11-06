"""R6 – TERCER ALGORITMO para la tabla comparativa 4.2 (programación dinámica).

Bellman-Ford (o Floyd-Warshall si prefieren; en ese caso mantener la misma firma).
"""
from __future__ import annotations

import time  # noqa: F401

from .common import Adj, Result, not_found, reconstruct_path  # noqa: F401


def bellman_ford(adj: Adj, start: int, goal: int) -> Result:
    """TODO (R6): menor costo de start a goal relajando todas las aristas hasta V-1 veces.

    Para Bellman-Ford, explored = número de relajaciones evaluadas (NO es comparable 1 a 1 con
    los nodos de Dijkstra/A*; dejarlo documentado en el informe). Cortar antes si una pasada no mejora nada.
    """
    raise NotImplementedError
