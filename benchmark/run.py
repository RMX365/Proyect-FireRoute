"""R7 – Ejecuta todos los algoritmos en todos los escenarios y guarda results/benchmark.csv.

Uso:  python -m benchmark.run
"""
from __future__ import annotations

import csv
import statistics

from benchmark.scenarios import all_scenarios
from fireroute.astar import astar
from fireroute.bellman_ford import bellman_ford
from fireroute.dijkstra import dijkstra

REPEATS = 10  # repeticiones por medición; se promedia time_ms


def main() -> None:
    algos = {
        "dijkstra": lambda s, a, b: dijkstra(s.adj, a, b),
        "astar": lambda s, a, b: astar(s.adj, s.coords, a, b, s.vmax_ms),
        "bellman_ford": lambda s, a, b: bellman_ford(s.adj, a, b),
    }
    rows = []
    for sc in all_scenarios():
        for name, fn in algos.items():
            try:
                for a, b in sc.pairs:
                    runs = [fn(sc, a, b) for _ in range(REPEATS)]
                    r = runs[0]
                    rows.append({
                        "scenario": sc.name, "algo": name, "start": a, "goal": b,
                        "found": r.found, "cost_s": round(r.cost, 3), "explored": r.explored,
                        "time_ms": round(statistics.mean(x.time_ms for x in runs), 4),
                    })
            except NotImplementedError:
                print(f"[omitido] {name} aún no implementado")
    if rows:
        with open("results/benchmark.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
        print(f"OK: {len(rows)} filas en results/benchmark.csv")


if __name__ == "__main__":
    main()
