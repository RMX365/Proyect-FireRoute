# funcionalidades.py  (IGUAL en las dos versiones)
"""
Análisis empírico POR FUNCIONALIDAD (rúbrica, criterio IV): se corren los
MISMOS destinos activando y desactivando, una por una, cada restricción
(las demás quedan en su valor por defecto), y se interpreta el resultado.

Funcionalidades aisladas:
  1) Congestión            (factor de tráfico)
  2) Calles bloqueadas
  3) Sentido único
  4) Calles estrechas / bolardos (penalización)
  5) Ubicación imprecisa    (reporte por coordenadas aproximadas)
"""
from mapa import construir_grafo, coordenadas, nodo_mas_cercano, ESTACION, VEL_MAX
from algoritmo import buscar_ruta, NOMBRE_ALGORITMO

DESTINOS = ["H8", "E7", "A1"]      # mismos destinos para las 5 funcionalidades
ESCENARIO_BASE = "normal"          # escenario fijo: solo cambia la restricción probada


def _texto(ruta):
    return "-".join(ruta) if ruta else "sin ruta"


def interpretar_tiempo(min_on, min_off):
    if round(min_on, 4) == round(min_off, 4):
        return "no cambia el tiempo para este destino"
    diff = min_on - min_off
    signo = "más" if diff > 0 else "menos"
    return f"con la restricción activa se tarda {abs(diff):.2f} min {signo}"


def probar_funcionalidad(nombre, kwargs_on, kwargs_off, destinos=DESTINOS):
    print(f"\n=== {nombre} ===")
    for destino in destinos:
        grafo_on, coords = construir_grafo(ESCENARIO_BASE, **kwargs_on)
        grafo_off, _ = construir_grafo(ESCENARIO_BASE, **kwargs_off)
        ruta_on, min_on, exp_on = buscar_ruta(grafo_on, coords, ESTACION, destino, VEL_MAX)
        ruta_off, min_off, exp_off = buscar_ruta(grafo_off, coords, ESTACION, destino, VEL_MAX)
        print(f" Destino {destino}:")
        print(f"  [activada]    {min_on:>8.2f} min  {exp_on:>3} nodos   {_texto(ruta_on)}")
        print(f"  [desactivada] {min_off:>8.2f} min  {exp_off:>3} nodos   {_texto(ruta_off)}")
        if min_on == float("inf") or min_off == float("inf"):
            print("      -> acción: sin ruta en alguno de los dos casos, revisar el mapa")
        else:
            print(f"      -> acción: {interpretar_tiempo(min_on, min_off)}")


def congestion():
    probar_funcionalidad("1) Congestión (factor de tráfico)",
                          {"congestion": True}, {"congestion": False})


def bloqueos():
    probar_funcionalidad("2) Calles bloqueadas",
                          {"bloqueos": True}, {"bloqueos": False})


def sentido_unico():
    # Se agrega B2 (columna B, solo sentido norte->sur): es donde el efecto se
    # nota, porque desde D4 hay que rodear en vez de usar esa calle al revés.
    probar_funcionalidad("3) Sentido único",
                          {"sentido_unico": True}, {"sentido_unico": False},
                          destinos=DESTINOS + ["B2"])


def penalizacion():
    # Se agrega H4 (pasa por el tramo G4-H4, penalización de 4 min: el máximo
    # tramo penalizado del mapa después de E7-E8).
    probar_funcionalidad("4) Calles estrechas / bolardos (penalización)",
                          {"penalizacion": True}, {"penalizacion": False},
                          destinos=DESTINOS + ["H4"])


def ubicacion_imprecisa():
    print("\n=== 5) Ubicación imprecisa (reporte por coordenadas aproximadas) ===")
    coords = coordenadas()
    grafo, _ = construir_grafo(ESCENARIO_BASE)
    for destino in DESTINOS:
        x_real, y_real = coords[destino]
        # Simula un reporte con error de ubicación de poco más de media cuadra
        # (+0.25 km, -0.22 km; ESPACIO entre nodos = 0.4 km) para que el nodo
        # más cercano pueda cambiar y se note el efecto de la imprecisión
        x_aprox, y_aprox = x_real + 0.25, y_real - 0.22
        nodo_aproximado = nodo_mas_cercano(coords, x_aprox, y_aprox)
        ruta_exacta, min_exacta, _ = buscar_ruta(grafo, coords, ESTACION, destino, VEL_MAX)
        ruta_aprox, min_aprox, _ = buscar_ruta(grafo, coords, ESTACION, nodo_aproximado, VEL_MAX)
        print(f" Reporte cerca de {destino} ({x_aprox:.2f}, {y_aprox:.2f} km):")
        print(f"  [exacto]      nodo {destino:<5} {min_exacta:>8.2f} min  {_texto(ruta_exacta)}")
        print(f"  [aproximado]  nodo {nodo_aproximado:<5} {min_aprox:>8.2f} min  {_texto(ruta_aprox)}")
        if nodo_aproximado == destino:
            print("      -> acción: la imprecisión no cambió el nodo asignado")
        else:
            print(f"      -> acción: la imprecisión asignó el incidente a {nodo_aproximado} en vez de "
                  f"{destino} ({min_aprox - min_exacta:+.2f} min de diferencia)")


if __name__ == "__main__":
    print(f"Algoritmo: {NOMBRE_ALGORITMO}  (origen {ESTACION}, escenario base: {ESCENARIO_BASE})")
    congestion()
    bloqueos()
    sentido_unico()
    penalizacion()
    ubicacion_imprecisa()
