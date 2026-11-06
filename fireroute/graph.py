"""R2 – MAPA. Construye el grafo dirigido de Trujillo (zona de la B-26)."""
from __future__ import annotations

import random

from .common import Adj, Coords, haversine_m


def build_toy_graph(n: int = 5, seed: int = 7) -> tuple[Adj, Coords, float]:
    """Grafo de juguete n×n (YA IMPLEMENTADO) para que R4, R5, R6 y R7 prueben desde el día 1.

    Devuelve (adj, coords, vmax_ms). Tramos horizontales de doble sentido; algunos verticales
    de sentido único. Factor de congestión en [1, 2] => la heurística de A* es admisible.
    """
    rng = random.Random(seed)
    lat0, lon0, step, speed = -8.1116, -79.0288, 0.0009, 10.0  # ~100 m entre nodos
    coords: Coords = {r * n + c: (lat0 + r * step, lon0 + c * step) for r in range(n) for c in range(n)}
    adj: Adj = {u: [] for u in coords}

    def add(u: int, v: int) -> None:
        factor = rng.uniform(1.0, 2.0)
        adj[u].append((v, haversine_m(coords[u], coords[v]) / speed * factor))

    for r in range(n):
        for c in range(n):
            u = r * n + c
            if c + 1 < n:
                add(u, u + 1)
                add(u + 1, u)
            if r + 1 < n:
                add(u, u + n)
                if rng.random() < 0.8:
                    add(u + n, u)
    return adj, coords, speed


def build_trujillo_graph() -> tuple[Adj, Coords, float]:
    """TODO (R2): grafo real de la zona de la B-26 (OpenStreetMap con osmnx, o digitalizado a mano).

    Requisitos:
      - dirigido (respetar sentido de circulación: oneway)
      - nodos = ints consecutivos; coords[u] = (lat, lon)
      - costo base de cada tramo = longitud_m / velocidad_ms (segundos)
      - devolver también vmax_ms = MAYOR velocidad de todo el mapa
    """
    raise NotImplementedError


def save_graph(adj: Adj, coords: Coords, vmax_ms: float, path: str = "data/trujillo_b26.json") -> None:
    """TODO (R2): guardar el mapa en data/ para que TODOS usen el mismo."""
    raise NotImplementedError


def load_graph(path: str = "data/trujillo_b26.json") -> tuple[Adj, Coords, float]:
    """TODO (R2): cargar el mapa guardado (convertir claves str -> int si usas JSON)."""
    raise NotImplementedError
