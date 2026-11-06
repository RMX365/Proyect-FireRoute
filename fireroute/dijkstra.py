"""R4 – DIJKSTRA (estrategia voraz). Algoritmo de referencia."""
from __future__ import annotations

import heapq  # noqa: F401  (cola de prioridad)
import time   # noqa: F401  (time.perf_counter para medir)

from .common import Adj, Result, not_found, reconstruct_path  # noqa: F401


def dijkstra(adj: Adj, start: int, goal: int) -> Result:
    """TODO (R4): ruta de menor costo de start a goal.

    Pasos: dist = {start: 0}; cola (costo, nodo); extraer mínimo; si ya está cerrado, saltar
    (entrada obsoleta); explored += 1 al cerrar un nodo; detenerse al cerrar goal;
    relajar vecinos; guardar prev. Medir time_ms con time.perf_counter() (solo el algoritmo).
    Si no hay ruta -> not_found(explored, time_ms).
    """
    raise NotImplementedError
