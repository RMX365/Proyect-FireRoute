"""R3 – RESTRICCIONES. Costo de cada tramo según tráfico, bloqueos y obstáculos (informe, sec. 1.2)."""
from __future__ import annotations

import math

from .common import Adj


def edge_cost(length_m: float, speed_ms: float, congestion: float = 1.0,
              penalty_s: float = 0.0, blocked: bool = False) -> float:
    """TODO (R3): tiempo del tramo en segundos.

    costo = (longitud / velocidad) * congestion + penalty_s      ; bloqueado -> math.inf
    OJO: congestion >= 1 (si fuera < 1 la heurística de A* deja de ser admisible). Validar con assert.
    """
    raise NotImplementedError


def apply_scenario(adj: Adj, congestion: dict[tuple[int, int], float] | None = None,
                   blocked: set[tuple[int, int]] | None = None,
                   penalties: dict[tuple[int, int], float] | None = None) -> Adj:
    """TODO (R3): devuelve una COPIA de adj con el escenario aplicado (no modificar el original).

    - congestion[(u, v)]: factor >= 1 que multiplica el costo del tramo
    - blocked: tramos eliminados del grafo (o costo math.inf)
    - penalties[(u, v)]: segundos extra (bolardos, calles angostas; hasta ~300 s según Torres Tutiven, 2025)
    """
    raise NotImplementedError
