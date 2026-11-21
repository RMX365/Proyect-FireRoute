"""R9 – VISUALIZACIÓN. Dibuja el mapa y la ruta para capturas del informe y la exposición."""
from __future__ import annotations

import matplotlib.pyplot as plt

from .common import Adj, Coords


def plot_route(adj: Adj, coords: Coords, path: list[int], title: str = "", out_path: str | None = None) -> None:
    """Versión básica (mejorarla: colores por congestión, bloqueos en rojo, marcar B-26 e incidente,
    leyenda, o usar folium/osmnx sobre el mapa real)."""
    fig, ax = plt.subplots(figsize=(7, 7))
    for u, edges in adj.items():
        for v, _ in edges:
            ax.plot([coords[u][1], coords[v][1]], [coords[u][0], coords[v][0]], color="lightgray", lw=0.8)
    if path:
        ax.plot([coords[n][1] for n in path], [coords[n][0] for n in path], color="crimson", lw=2.5, label="ruta")
        ax.scatter(*coords[path[0]][::-1], c="green", s=80, label="B-26 (origen)", zorder=3)
        ax.scatter(*coords[path[-1]][::-1], c="red", s=80, label="incidente", zorder=3)
    ax.set_title(title)
    ax.legend()
    ax.set_aspect("equal")
    if out_path:
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
    else:
        plt.show()
    plt.close(fig)
