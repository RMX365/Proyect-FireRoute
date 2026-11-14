"""R9 – VISUALIZACIÓN. Dibuja el mapa y la ruta para capturas del informe y la exposición."""
from __future__ import annotations

import math

import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D

from .common import Adj, Coords, haversine_m


def _xy(coords: Coords, u: int) -> tuple[float, float]:
    return coords[u][1], coords[u][0]


def plot_route(adj: Adj, coords: Coords, path: list[int], title: str = "", out_path: str | None = None,
               vmax_ms: float | None = None, blocked: set[tuple[int, int]] | None = None) -> None:
    """Dibuja el mapa coloreado por congestión, los tramos bloqueados en rojo y la ruta.

    vmax_ms: si se indica, cada tramo se colorea por (costo real / costo a velocidad máxima).
    blocked: tramos (u, v) bloqueados que ya no están en adj. Los tramos con costo infinito también se dibujan.
    """
    blocked = set(blocked or ())
    factors: dict[tuple[int, int], float] = {}
    for u, edges in adj.items():
        for v, cost in edges:
            if math.isinf(cost):
                blocked.add((u, v))
                continue
            key = (min(u, v), max(u, v))
            factor = 1.0
            if vmax_ms:
                factor = cost / (haversine_m(coords[u], coords[v]) / vmax_ms)
            factors[key] = max(factors.get(key, 1.0), factor)

    fig, ax = plt.subplots(figsize=(8, 7))
    xs, ys = zip(*(_xy(coords, n) for n in coords))
    ax.scatter(xs, ys, s=10, color="gray", zorder=2)

    cmap = plt.get_cmap("YlGnBu")
    norm = Normalize(vmin=1.0, vmax=max(max(factors.values(), default=1.0), 1.01))
    segments = [[_xy(coords, u), _xy(coords, v)] for u, v in factors]
    colors = [cmap(norm(f)) if vmax_ms else "lightgray" for f in factors.values()]
    ax.add_collection(LineCollection(segments, colors=colors, linewidths=2, zorder=1))
    if vmax_ms:
        fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax, shrink=0.8,
                     label="Congestión (costo real / costo a velocidad máxima)")

    for u, v in blocked:
        (x0, y0), (x1, y1) = _xy(coords, u), _xy(coords, v)
        ax.plot([x0, x1], [y0, y1], color="red", linestyle="--", linewidth=3, zorder=3)
        ax.plot((x0 + x1) / 2, (y0 + y1) / 2, marker="x", color="red", markersize=9, markeredgewidth=2.5, zorder=3)

    handles = []
    if path:
        ax.plot([_xy(coords, n)[0] for n in path], [_xy(coords, n)[1] for n in path],
                color="darkorange", linewidth=3.5, zorder=4)
        ax.scatter(*_xy(coords, path[0]), c="green", marker="s", s=140, edgecolors="black", zorder=5)
        ax.scatter(*_xy(coords, path[-1]), c="red", marker="*", s=300, edgecolors="black", zorder=5)
        handles += [
            Line2D([], [], color="darkorange", linewidth=3.5, label="ruta"),
            Line2D([], [], color="green", marker="s", linestyle="", markersize=10, markeredgecolor="black", label="B-26 (origen)"),
            Line2D([], [], color="red", marker="*", linestyle="", markersize=15, markeredgecolor="black", label="incidente"),
        ]
    if blocked:
        handles.append(Line2D([], [], color="red", linestyle="--", linewidth=3, label="tramo bloqueado"))

    ax.autoscale_view()
    ax.set_title(title)
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_aspect("equal")
    ax.ticklabel_format(useOffset=False)
    ax.tick_params(axis="x", labelrotation=30)
    if handles:
        ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=len(handles), fontsize=8)
    if out_path:
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
    else:
        plt.show()
    plt.close(fig)

