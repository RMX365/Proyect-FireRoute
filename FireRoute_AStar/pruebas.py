# pruebas.py  (IGUAL en las dos versiones)
# 1) Tabla del análisis empírico (informe, sección 4.1)
# 2) Pruebas automáticas normal / extremo / error (rúbrica, criterio III)
import time
from mapa import construir_grafo, ESTACION, VEL_MAX
from algoritmo import buscar_ruta, NOMBRE_ALGORITMO

# ---------------------------------------------------------------------------
# 1) TABLA EMPÍRICA (igual que antes, para el informe 4.1)
# ---------------------------------------------------------------------------
CASOS = [
    ("normal", "H8"), ("normal", "A8"), ("normal", "A1"), ("normal", "H1"),
    ("hora_punta", "H8"), ("hora_punta", "A1"),
    ("bloqueo", "H8"), ("bloqueo", "E5"), ("bloqueo", "D6"),
]
REPETICIONES = 300   # se promedia el tiempo para que sea estable


def tabla_empirica():
    print(f"Algoritmo: {NOMBRE_ALGORITMO}  (origen {ESTACION})")
    print(f"{'Escenario':<11}{'Destino':<9}{'Minutos':>9}{'Explorados':>12}{'Tiempo(ms)':>12}  Ruta")
    for escenario, destino in CASOS:
        grafo, coords = construir_grafo(escenario)
        inicio = time.perf_counter()
        for _ in range(REPETICIONES):
            ruta, minutos, explorados = buscar_ruta(grafo, coords, ESTACION, destino, VEL_MAX)
        ms = (time.perf_counter() - inicio) * 1000 / REPETICIONES
        texto = "-".join(ruta) if ruta else "sin ruta"
        print(f"{escenario:<11}{destino:<9}{minutos:>9.2f}{explorados:>12}{ms:>12.3f}  {texto}")


# ---------------------------------------------------------------------------
# 2) PRUEBAS AUTOMÁTICAS (criterio III: normal, extremo, error)
# ---------------------------------------------------------------------------
fallos = []


def verificar(nombre, condicion, detalle=""):
    estado = "OK" if condicion else "FALLÓ"
    sufijo = f" -> {detalle}" if detalle else ""
    print(f"  [{estado}] {nombre}{sufijo}")
    if not condicion:
        fallos.append(nombre)


def pruebas_normales():
    print("\n--- Casos NORMALES (ruta directa esperada) ---")
    for escenario, destino in [("normal", "H8"), ("normal", "A1"), ("hora_punta", "G7")]:
        grafo, coords = construir_grafo(escenario)
        ruta, minutos, explorados = buscar_ruta(grafo, coords, ESTACION, destino, VEL_MAX)
        verificar(f"{escenario}/{destino}: existe ruta", ruta is not None)
        if ruta:
            verificar(f"{escenario}/{destino}: ruta empieza en {ESTACION}", ruta[0] == ESTACION)
            verificar(f"{escenario}/{destino}: ruta termina en {destino}", ruta[-1] == destino)
            verificar(f"{escenario}/{destino}: tiempo positivo", minutos > 0)
            verificar(f"{escenario}/{destino}: explora al menos 1 nodo", explorados >= 1)


def pruebas_extremas():
    print("\n--- Casos EXTREMOS (esquina a esquina / varias calles cortadas a la vez) ---")

    # 1) Esquina a esquina en hora punta: la combinación más lenta del mapa
    grafo, coords = construir_grafo("hora_punta")
    ruta, minutos, explorados = buscar_ruta(grafo, coords, "A1", "H8", VEL_MAX)
    verificar("A1 -> H8 en hora_punta: existe ruta", ruta is not None)
    if ruta:
        verificar("A1 -> H8 en hora_punta: es de los casos más lentos (> 12 min)", minutos > 12,
                   f"{minutos:.2f} min")

    # 2) Bloqueo extremo: a los cortes del escenario "bloqueo" se SUMAN 2 más,
    #    dejando a la estación con solo 2 de sus 5 salidas habituales
    extra = [("D4", "D3"), ("D4", "C4")]
    grafo, coords = construir_grafo("bloqueo", bloqueos_extra=extra)
    ruta, minutos, explorados = buscar_ruta(grafo, coords, ESTACION, "H8", VEL_MAX)
    verificar("Bloqueo extremo (4 calles cortadas cerca de la estación): sigue habiendo ruta",
              ruta is not None)
    if ruta:
        grafo_normal, coords_normal = construir_grafo("normal")
        _, minutos_normal, _ = buscar_ruta(grafo_normal, coords_normal, ESTACION, "H8", VEL_MAX)
        verificar("Bloqueo extremo: tarda igual o más que en escenario normal",
                  minutos >= minutos_normal, f"{minutos:.2f} min vs {minutos_normal:.2f} min")

    # 3) Bloqueo total: se cortan las 5 salidas de la estación -> no puede salir ningún camión
    aislar_estacion = [("D4", "D3"), ("D4", "C4"), ("D4", "D5"), ("D4", "E5"), ("D4", "E4")]
    grafo, coords = construir_grafo("normal", bloqueos_extra=aislar_estacion)
    ruta, minutos, explorados = buscar_ruta(grafo, coords, ESTACION, "H8", VEL_MAX)
    verificar("Estación totalmente aislada (5 salidas cortadas): no existe ruta", ruta is None)
    verificar("Estación totalmente aislada: tiempo devuelto es infinito", minutos == float("inf"))


def pruebas_de_error():
    print("\n--- Casos de ERROR (entradas inválidas) ---")
    grafo, coords = construir_grafo("normal")

    # 1) Destino que no existe en el mapa
    ruta, minutos, explorados = buscar_ruta(grafo, coords, ESTACION, "ZZ", VEL_MAX)
    verificar("Destino inexistente ('ZZ'): no lanza excepción y responde 'sin ruta'", ruta is None)

    # 2) Origen que no existe en el mapa
    ruta, minutos, explorados = buscar_ruta(grafo, coords, "ZZ", "H8", VEL_MAX)
    verificar("Origen inexistente ('ZZ'): no lanza excepción y responde 'sin ruta'", ruta is None)

    # 3) Destino aislado: nodo sintético sin ninguna conexión al resto del mapa
    grafo_sintetico = {n: list(v) for n, v in grafo.items()}
    grafo_sintetico["ISLA"] = []               # nodo sin salidas ni entradas
    coords_sintetico = dict(coords)
    coords_sintetico["ISLA"] = (99.0, 99.0)    # coordenada ficticia (la usa la heurística de A*)
    ruta, minutos, explorados = buscar_ruta(grafo_sintetico, coords_sintetico, ESTACION, "ISLA", VEL_MAX)
    verificar("Destino aislado ('ISLA', sin conexiones): no existe ruta", ruta is None)


if __name__ == "__main__":
    tabla_empirica()
    print(f"\n=== PRUEBAS AUTOMÁTICAS ({NOMBRE_ALGORITMO}) ===")
    pruebas_normales()
    pruebas_extremas()
    pruebas_de_error()
    if fallos:
        print(f"\nResultado: {len(fallos)} prueba(s) fallaron -> {fallos}")
        raise SystemExit(1)
    print("\nResultado: todas las pruebas automáticas pasaron")
