# main.py  (IGUAL en las dos versiones; solo cambia algoritmo.py)
import time
from mapa import (construir_grafo, ESTACION, VEL_MAX, ESCENARIOS,
                  distancia_recta, nodo_mas_cercano, COLUMNAS, FILAS)
from algoritmo import buscar_ruta, NOMBRE_ALGORITMO


def pedir_escenario():
    print("\nEscenarios:  1) normal   2) hora punta   3) calles bloqueadas")
    opcion = input("Elija escenario (1-3): ").strip()
    if opcion not in ("1", "2", "3"):
        print("Opción inválida, se usa 'normal'")
        opcion = "1"
    return ESCENARIOS[int(opcion) - 1]


def pedir_destino(coords):
    print("\nUbicación del incendio:  1) código de intersección (ej. G7)   2) coordenadas aproximadas (x,y en km)")
    opcion = input("Elija (1-2): ").strip()
    if opcion == "2":
        try:
            x, y = input("Ingrese x,y: ").split(",")
            nodo = nodo_mas_cercano(coords, float(x), float(y))
            print(f"Ubicación imprecisa -> nodo más cercano: {nodo}")
            return nodo
        except ValueError:
            print("Formato inválido")
            return None
    nodo = input("Código de intersección: ").strip().upper()
    if nodo not in coords:
        print(f"'{nodo}' no existe en el mapa (use {COLUMNAS[0]}1 ... {COLUMNAS[-1]}{max(FILAS)})")
        return None
    return nodo


def calcular_y_mostrar(escenario, destino, paso_a_paso=False):
    grafo, coords = construir_grafo(escenario)
    inicio = time.perf_counter()
    ruta, minutos, explorados = buscar_ruta(grafo, coords, ESTACION, destino, VEL_MAX, paso_a_paso)
    ms = (time.perf_counter() - inicio) * 1000

    print(f"\n===== RESULTADO ({NOMBRE_ALGORITMO}) =====")
    print(f"Escenario: {escenario} | Origen: {ESTACION} (B-26) | Destino: {destino}")
    if ruta is None:
        print("No existe ruta disponible (calles bloqueadas o sentidos de circulación).")
        print(f"Nodos explorados: {explorados}")
        return
    km = sum(distancia_recta(coords, ruta[i], ruta[i + 1]) for i in range(len(ruta) - 1))
    print("Ruta: " + " -> ".join(ruta))
    print(f"Tiempo estimado de llegada: {minutos:.2f} min")
    print(f"Distancia recorrida: {km:.2f} km")
    print(f"Nodos explorados: {explorados}")
    print(f"Tiempo de ejecución: {ms:.3f} ms")


def mostrar_mapa():
    grafo, coords = construir_grafo("normal")
    aristas = sum(len(v) for v in grafo.values())
    print(f"\nMapa: {len(grafo)} intersecciones, {aristas} tramos dirigidos. Estación B-26 en {ESTACION}.")
    print("Intersecciones: " + ", ".join(grafo))


def menu():
    print(f"=== FIREROUTE - Compañía de Bomberos B-26 | Algoritmo: {NOMBRE_ALGORITMO} ===")
    while True:
        print("\n1) Calcular ruta   2) Calcular ruta paso a paso   3) Ver mapa   4) Salir")
        opcion = input("Opción: ").strip()
        if opcion in ("1", "2"):
            escenario = pedir_escenario()
            _, coords = construir_grafo(escenario)
            destino = pedir_destino(coords)
            if destino is not None:
                calcular_y_mostrar(escenario, destino, paso_a_paso=(opcion == "2"))
        elif opcion == "3":
            mostrar_mapa()
        elif opcion == "4":
            print("Fin del programa")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    menu()
