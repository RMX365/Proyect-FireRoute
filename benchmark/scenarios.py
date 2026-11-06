"""R7 – ESCENARIOS. Cada escenario = un mapa (con restricciones aplicadas) + pares origen-destino."""
from __future__ import annotations

import random
from dataclasses import dataclass

from fireroute.common import Adj, Coords
from fireroute.graph import build_toy_graph


@dataclass
class Scenario:
    name: str
    adj: Adj
    coords: Coords
    vmax_ms: float
    pairs: list[tuple[int, int]]  # (origen B-26, incidente)


def toy_scenarios() -> list[Scenario]:
    """Escenario de ejemplo para probar el pipeline. R7: reemplazar/ampliar con el mapa real."""
    adj, coords, vmax = build_toy_graph()
    rng = random.Random(42)
    nodes = sorted(adj)
    pairs = [tuple(rng.sample(nodes, 2)) for _ in range(20)]
    return [Scenario("toy_base", adj, coords, vmax, pairs)]


def all_scenarios() -> list[Scenario]:
    """TODO (R7): trafico_normal, trafico_alto, calle_bloqueada, sentido_unico, obstaculos, zona_incierta.
    Usar fireroute.costs.apply_scenario (R3) sobre el mapa real (R2). Semilla fija, 20-30 pares."""
    return toy_scenarios()
