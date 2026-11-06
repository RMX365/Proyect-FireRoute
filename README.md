# FireRoute

Simulador de ruta óptima de unidades de la Compañía de Bomberos Salvadora Trujillo N.º 26 (B-26):
**Dijkstra (estrategia voraz) vs A\***. Curso: Análisis de Algoritmos y Estrategias de Programación (UPN, 2026-2).

## Puesta en marcha (VS Code)
```bash
git clone <URL-del-repo> && cd <repo>
git checkout develop
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
pytest                         # en rojo hasta implementar cada módulo (normal)
python -m benchmark.run        # genera results/benchmark.csv
```
En VS Code: `Ctrl+Shift+P` → *Python: Select Interpreter* → elegir `.venv`.

## Flujo de Git (ramas `main` y `develop`)
1. Siempre partir de `develop` actualizado: `git checkout develop && git pull`
2. Crear tu rama: `git checkout -b feature/r4-dijkstra` (rol + módulo)
3. Commits pequeños y claros: `feat(dijkstra): implementa cola de prioridad`
4. `git push -u origin feature/r4-dijkstra` y abrir **Pull Request hacia `develop`** con 1 revisor
5. **Nadie hace push directo a `develop` ni a `main`.** Solo R1 pasa `develop` → `main` al congelar el código.

## Contrato (no cambiar sin avisar a R1)
Ver `fireroute/common.py`: unidades en **segundos/metros/m·s⁻¹**, grafo `adj[u] = [(v, costo_seg)]`,
`Result(path, cost, explored, time_ms)`. Reglas: congestión ≥ 1, `vmax` = mayor velocidad del mapa.

## Roles
Ver `docs/roles.md`. Busca `TODO (Rx)` en el código para encontrar lo que te toca.

## Uso de IA
Se declara el uso de herramientas de IA como apoyo (revisión, depuración); todo resultado se verifica con tests propios.
