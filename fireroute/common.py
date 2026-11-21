"""Contrato compartido. NO cambiar firmas sin avisar a R1 (todos dependen de esto).

Unidades: distancias en metros, velocidades en m/s, costos y tiempos de llegada en SEGUNDOS.
Grafo dirigido:  adj[u] = [(v, costo_seg), ...]     coords[u] = (lat, lon)
"""
from __future__ import annotations

import math
from dataclasses import dataclass

Adj = dict[int, list[tuple[int, float]]]
Coords = dict[int, tuple[float, float]]

DEFAULT_VMAX_MS = 16.7  # ~60 km/h; velocidad máxima de TODO el mapa (heurística de A*)


@dataclass
class Result:
    path: list[int]    # nodos de origen a destino ([] si no hay ruta)
    cost: float        # tiempo de llegada en segundos (inf si no hay ruta)
    explored: int      # nodos cerrados/extraídos de la cola (sin contar entradas obsoletas)
    time_ms: float     # tiempo de ejecución del algoritmo en milisegundos

    @property
    def found(self) -> bool:
        return bool(self.path)


def not_found(explored: int, time_ms: float) -> Result:
    return Result(path=[], cost=math.inf, explored=explored, time_ms=time_ms)


def haversine_m(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Distancia en línea recta (metros) entre dos puntos (lat, lon)."""
    r = 6_371_000.0
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    h = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * r * math.asin(math.sqrt(h))


def reconstruct_path(prev: dict[int, int], start: int, goal: int) -> list[int]:
    """Reconstruye start -> goal desde el diccionario de predecesores. [] si no hay ruta."""
    if goal != start and goal not in prev:
        return []
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return path[::-1]
