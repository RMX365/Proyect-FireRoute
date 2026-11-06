from fireroute.common import haversine_m, reconstruct_path
from fireroute.graph import build_toy_graph


def test_haversine_cero():
    assert haversine_m((0, 0), (0, 0)) == 0


def test_reconstruct_path():
    assert reconstruct_path({1: 0, 2: 1}, 0, 2) == [0, 1, 2]
    assert reconstruct_path({}, 0, 5) == []


def test_toy_graph_fuertemente_conexo():
    adj, _, _ = build_toy_graph()
    rev = {u: [] for u in adj}
    for u, es in adj.items():
        for v, _ in es:
            rev[v].append(u)

    def alcanza(g):
        seen, stack = {0}, [0]
        while stack:
            for x in g[stack.pop()]:
                x = x[0] if isinstance(x, tuple) else x
                if x not in seen:
                    seen.add(x)
                    stack.append(x)
        return len(seen)

    assert alcanza(adj) == len(adj) and alcanza(rev) == len(adj)
