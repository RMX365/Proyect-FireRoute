"""Tests de corrección. Estarán en ROJO hasta que cada rol implemente su módulo (es lo esperado)."""
import math
import random

import pytest

from fireroute.astar import astar
from fireroute.bellman_ford import bellman_ford
from fireroute.dijkstra import dijkstra
from fireroute.graph import build_toy_graph

VMAX = 10.0


def tiny():
    adj = {0: [(1, 1.0), (2, 5.0)], 1: [(2, 1.0)], 2: [], 3: []}
    coords = {n: (0.0, 0.0) for n in adj}  # h = 0
    return adj, coords


ALGOS = {
    "dijkstra": lambda adj, co, a, b: dijkstra(adj, a, b),
    "astar": lambda adj, co, a, b: astar(adj, co, a, b, VMAX),
    "bellman_ford": lambda adj, co, a, b: bellman_ford(adj, a, b),
}


@pytest.mark.parametrize("name", ALGOS)
def test_ruta_simple(name):
    adj, co = tiny()
    r = ALGOS[name](adj, co, 0, 2)
    assert r.path == [0, 1, 2] and r.cost == pytest.approx(2.0)


@pytest.mark.parametrize("name", ALGOS)
def test_origen_igual_destino(name):
    adj, co = tiny()
    r = ALGOS[name](adj, co, 0, 0)
    assert r.path == [0] and r.cost == 0


@pytest.mark.parametrize("name", ALGOS)
def test_sin_ruta(name):
    adj, co = tiny()
    r = ALGOS[name](adj, co, 0, 3)
    assert r.path == [] and math.isinf(r.cost)


def test_los_tres_dan_el_mismo_costo_y_astar_explora_menos():
    adj, co, vmax = build_toy_graph()
    assert vmax == VMAX
    rng = random.Random(1)
    pares = [tuple(rng.sample(sorted(adj), 2)) for _ in range(25)]
    exp_d = exp_a = 0
    for a, b in pares:
        d = dijkstra(adj, a, b)
        s = astar(adj, co, a, b, vmax)
        f = bellman_ford(adj, a, b)
        assert d.cost == pytest.approx(s.cost) == pytest.approx(f.cost)
        exp_d += d.explored
        exp_a += s.explored
    assert exp_a <= exp_d
