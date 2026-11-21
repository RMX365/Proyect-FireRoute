# comparar.py
# Carga los DOS proyectos (Dijkstra y A*) y genera:
#   - Tabla 4.1: resumen por escenario (todos los destinos)
#   - Tabla 4.2: comparación de doble entrada (algoritmo elegido vs el otro)
#
# Se ejecuta desde la carpeta que contiene FireRoute_Dijkstra/ y FireRoute_AStar/:
#   python comparar.py
#
# mapa.py y algoritmo.py se llaman IGUAL en los dos proyectos, así que se cargan
# con importlib bajo un nombre único por carpeta para que no choquen entre sí.
import importlib.util
import os

CARPETAS = {"Dijkstra": "FireRoute_Dijkstra", "A*": "FireRoute_AStar"}
ALGORITMO_ELEGIDO = "A*"   # el que se sustenta como elección final (informe, sección 4.2)


def cargar(carpeta, modulo):
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), carpeta, f"{modulo}.py")
    spec = importlib.util.spec_from_file_location(f"{carpeta}.{modulo}", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mods = {nombre: {"mapa": cargar(carpeta, "mapa"), "algoritmo": cargar(carpeta, "algoritmo")}
        for nombre, carpeta in CARPETAS.items()}

mapa_ref = mods["Dijkstra"]["mapa"]          # mapa.py es idéntico en los dos proyectos
ESTACION, VEL_MAX, ESCENARIOS = mapa_ref.ESTACION, mapa_ref.VEL_MAX, mapa_ref.ESCENARIOS
DESTINOS = sorted(n for n in mapa_ref.coordenadas() if n != ESTACION)   # 63 destinos


def correr_todo():
    """resultados[escenario][destino][nombre_algoritmo] = (ruta, minutos, explorados)"""
    resultados = {}
    for escenario in ESCENARIOS:
        resultados[escenario] = {}
        for nombre, mod in mods.items():
            grafo, coords = mod["mapa"].construir_grafo(escenario)
            for destino in DESTINOS:
                ruta, minutos, explorados = mod["algoritmo"].buscar_ruta(
                    grafo, coords, ESTACION, destino, VEL_MAX)
                resultados[escenario].setdefault(destino, {})[nombre] = (ruta, minutos, explorados)
    return resultados


def tabla_4_1(resultados):
    total_destinos = len(DESTINOS)
    print(f"=== Tabla 4.1: resumen por escenario ({total_destinos} destinos x {len(ESCENARIOS)} escenarios) ===")
    print(f"{'Escenario':<12}{'Mismo tiempo':>14}{'Expl. Dijkstra':>16}{'Expl. A*':>10}{'Reducción A*':>14}")
    for escenario in ESCENARIOS:
        destinos = resultados[escenario]
        mismos_tiempo = suma_d = suma_a = 0
        for datos in destinos.values():
            _, min_d, exp_d = datos["Dijkstra"]
            _, min_a, exp_a = datos["A*"]
            if round(min_d, 4) == round(min_a, 4):
                mismos_tiempo += 1
            suma_d += exp_d
            suma_a += exp_a
        prom_d, prom_a = suma_d / total_destinos, suma_a / total_destinos
        reduccion = (1 - prom_a / prom_d) * 100 if prom_d else 0
        print(f"{escenario:<12}{mismos_tiempo:>14}{prom_d:>16.1f}{prom_a:>10.1f}{reduccion:>13.1f}%")


def tabla_4_2(resultados):
    otro = next(n for n in mods if n != ALGORITMO_ELEGIDO)
    print(f"\n=== Tabla 4.2: {ALGORITMO_ELEGIDO} (elegido) vs {otro} ===")
    print(f"{'Escenario':<12}{'Mismo tiempo':>14}{'Misma ruta':>12}"
          f"{'Ruta distinta':>15}{f'{ALGORITMO_ELEGIDO} explora menos':>22}")
    for escenario in ESCENARIOS:
        destinos = resultados[escenario]
        mismo_tiempo = misma_ruta = ruta_distinta = explora_menos = 0
        for datos in destinos.values():
            ruta_e, min_e, exp_e = datos[ALGORITMO_ELEGIDO]
            ruta_o, min_o, exp_o = datos[otro]
            if round(min_e, 4) == round(min_o, 4):
                mismo_tiempo += 1
                if ruta_e == ruta_o:
                    misma_ruta += 1
                else:
                    ruta_distinta += 1
            if exp_e < exp_o:
                explora_menos += 1
        print(f"{escenario:<12}{mismo_tiempo:>14}{misma_ruta:>12}{ruta_distinta:>15}{explora_menos:>22}")
    print(f"\n(\"Ruta distinta\" = mismo tiempo pero camino diferente: hay rutas empatadas, no es un error.)")


def tabla_funcionalidades():
    """Aísla cada restricción y compara ambos algoritmos con los mismos destinos."""
    print("\n=== Análisis por funcionalidad (restricción activada vs desactivada) ===")
    casos = [
        ("Congestión", {"congestion": True}, {"congestion": False}, ["H8", "E7", "A1"]),
        ("Bloqueos", {"bloqueos": True}, {"bloqueos": False}, ["H8", "E7", "A1"]),
        ("Sentido único", {"sentido_unico": True}, {"sentido_unico": False}, ["H8", "E7", "A1", "B2"]),
        ("Calles estrechas / penalización", {"penalizacion": True}, {"penalizacion": False}, ["H8", "E7", "A1", "H4"]),
    ]
    for etiqueta, on, off, destinos in casos:
        print(f"\n{etiqueta} | destinos: {', '.join(destinos)}")
        print(f"{'Algoritmo':<12}{'Activada (min)':>17}{'Desactivada (min)':>20}{'Diferencia':>14}")
        for nombre, mod in mods.items():
            suma_on = suma_off = 0.0
            n = 0
            for destino in destinos:
                g_on, c_on = mapa_ref.construir_grafo("normal", **on)
                g_off, c_off = mapa_ref.construir_grafo("normal", **off)
                _, t_on, _ = mod["algoritmo"].buscar_ruta(g_on, c_on, ESTACION, destino, VEL_MAX)
                _, t_off, _ = mod["algoritmo"].buscar_ruta(g_off, c_off, ESTACION, destino, VEL_MAX)
                if t_on != float("inf") and t_off != float("inf"):
                    suma_on += t_on
                    suma_off += t_off
                    n += 1
            if n:
                prom_on, prom_off = suma_on/n, suma_off/n
                print(f"{nombre:<12}{prom_on:>17.2f}{prom_off:>20.2f}{prom_on-prom_off:>+14.2f}")
            else:
                print(f"{nombre:<12}{'sin ruta':>17}{'sin ruta':>20}{'--':>14}")

    # La ubicación imprecisa no modifica el grafo: modifica el nodo destino asignado.
    print("\nUbicación imprecisa | reporte por coordenadas aproximadas")
    print(f"{'Algoritmo':<12}{'Destino exacto':>18}{'Nodo asignado':>18}{'Tiempo exacto':>16}{'Tiempo aprox.':>16}")
    for nombre, mod in mods.items():
        grafo, coords = mapa_ref.construir_grafo("normal")
        for destino in ("H8", "E7", "A1"):
            x, y = coords[destino]
            aproximado = mapa_ref.nodo_mas_cercano(coords, x + 0.25, y - 0.22)
            _, exacto, _ = mod["algoritmo"].buscar_ruta(grafo, coords, ESTACION, destino, VEL_MAX)
            _, aprox, _ = mod["algoritmo"].buscar_ruta(grafo, coords, ESTACION, aproximado, VEL_MAX)
            print(f"{nombre:<12}{destino:>18}{aproximado:>18}{exacto:>16.2f}{aprox:>16.2f}")



if __name__ == "__main__":
    resultados = correr_todo()
    tabla_4_1(resultados)
    tabla_4_2(resultados)
    tabla_funcionalidades()
