# FireRoute – Dijkstra

Simulador académico de rutas para la Compañía de Bomberos B-26. El mapa es un **modelo esquemático** de 8×8 intersecciones, no un mapa vial oficial.

## Requisitos
- Python 3.10 o superior (no requiere paquetes externos).
- Solo se utiliza la biblioteca estándar de Python.

## Ejecutar
Abre esta carpeta en VS Code y ejecuta:

```bash
python main.py
```

## Ejecutar el análisis empírico y las pruebas
```bash
python pruebas.py
```

`pruebas.py` presenta la tabla de casos del análisis y verifica escenarios normales, extremos y entradas erróneas.

Para ejecutar las pruebas con el framework estándar `unittest`:

```bash
python -m unittest -v
```

## Archivos
- `mapa.py`: nodos, calles, sentidos, costos y restricciones.
- `algoritmo.py`: implementación de Dijkstra.
- `funcionalidades.py`: comparación con restricciones activadas/desactivadas individualmente.
- `main.py`: menú interactivo y modo paso a paso.
- `pruebas.py`: análisis empírico y verificaciones de escenarios.

Desde la carpeta raíz del ZIP:
```bash
python comparar.py
```
Esto compara Dijkstra y A* con el mismo mapa y los mismos escenarios.
