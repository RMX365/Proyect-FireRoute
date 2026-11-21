# FireRoute – Simulador de rutas para la Compañía de Bomberos B-26

Este repositorio contiene dos implementaciones independientes que comparten el mismo modelo de mapa:
- `FireRoute_Dijkstra/`: algoritmo de Dijkstra.
- `FireRoute_AStar/`: algoritmo A*.

El mapa es un **modelo esquemático** de 8×8 intersecciones; no representa cartografía oficial.

## Requisitos
Python 3.10 o superior. No se necesitan instalaciones adicionales: se utiliza únicamente la biblioteca estándar.

## Ejecución
Desde la carpeta raíz:
```bash
python comparar.py
```
Para ejecutar el menú interactivo, entra en la carpeta del algoritmo:
```bash
cd FireRoute_AStar
python main.py
```
También puedes entrar en `FireRoute_Dijkstra` y ejecutar `python main.py`.

## Pruebas
En cada carpeta de algoritmo:
```bash
python pruebas.py
python -m unittest -v
```

## Análisis por funcionalidad
En cada carpeta:
```bash
python funcionalidades.py
```
El comparador raíz también presenta un resumen comparativo de las restricciones activadas y desactivadas.

## Estructura
Cada proyecto contiene `mapa.py`, `algoritmo.py`, `main.py`, `funcionalidades.py`, `pruebas.py` y `test_fireroute.py`. El archivo `mapa.py` debe mantenerse idéntico en ambos proyectos para que la comparación sea justa.
