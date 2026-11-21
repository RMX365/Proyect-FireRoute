# mapa.py
"""
Mapa urbano de FireRoute (modelo de la zona de la Compañía B-26, Trujillo).
OJO: es un MODELO (supuesto de modelado del informe), no un mapa oficial.

El mapa es un GRAFO DIRIGIDO:
  nodos   = intersecciones (A1, A2, ... H8)
  aristas = tramos de calle (cada una con su costo en MINUTOS)

grafo = { 'D4': [('E4', 0.35), ('D5', 0.41)], ... }   <- lista de adyacencia
"""
import math

ESPACIO = 0.4          # km entre intersecciones vecinas (cuadra urbana aprox.)
COLUMNAS = "ABCDEFGH"  # A..H  -> coordenada x
FILAS = range(1, 9)    # 1..8  -> coordenada y
ESTACION = "D4"        # Compañía de Bomberos B-26
VEL_MAX = 60           # km/h: velocidad máxima permitida (sirve para la heurística de A*)

# ---- Velocidad según tipo de vía (km/h) ----
VELOCIDAD = {"avenida": 50, "calle": 30, "estrecha": 20}

# ---- Factor de congestión por escenario (multiplica el tiempo del tramo) ----
FACTOR = {
    "normal":     {"avenida": 1.2, "calle": 1.1, "estrecha": 1.1},
    "hora_punta": {"avenida": 2.5, "calle": 1.6, "estrecha": 1.3},
    "bloqueo":    {"avenida": 1.2, "calle": 1.1, "estrecha": 1.1},
}

# ---- Avenidas: fila 4 y columna D (las demás son calles) ----
FILAS_AVENIDA = {4}
COLUMNAS_AVENIDA = {"D"}

# ---- Calles de sentido único (se guarda el SENTIDO permitido) ----
# fila 2: solo de oeste a este | fila 6: solo de este a oeste
# columna B: solo de norte a sur (fila 1 -> 8) | columna F: solo de sur a norte
FILAS_UNICO = {2: "E", 6: "O"}
COLUMNAS_UNICO = {"B": "S", "F": "N"}

# ---- Calles estrechas con bolardos/cadenas: penalización en minutos (ida y vuelta) ----
PENALIZACION = {
    ("C5", "D5"): 3,
    ("D5", "E5"): 3,
    ("G4", "H4"): 4,
    ("E7", "E8"): 5,   # máximo según Torres Tutiven (2025)
    ("B3", "C3"): 2,
}

# ---- Tramos bloqueados (obras / accidentes) en el escenario "bloqueo" ----
BLOQUEADOS = [("D4", "E5"), ("D5", "D6"), ("D3", "D2"), ("C4", "B4")]

ESCENARIOS = ["normal", "hora_punta", "bloqueo"]


def coordenadas():
    """Devuelve {nodo: (x_km, y_km)}"""
    coords = {}
    for i, letra in enumerate(COLUMNAS):
        for fila in FILAS:
            coords[f"{letra}{fila}"] = (i * ESPACIO, (fila - 1) * ESPACIO)
    return coords


def distancia_recta(coords, a, b):
    """Distancia en línea recta (km) entre dos nodos"""
    (x1, y1), (x2, y2) = coords[a], coords[b]
    return math.hypot(x1 - x2, y1 - y2)


def nodo_mas_cercano(coords, x, y):
    """Ubicación imprecisa: asigna el incidente al nodo más cercano del mapa"""
    mejor, mejor_d = None, float("inf")
    for nodo, (nx, ny) in coords.items():
        d = math.hypot(nx - x, ny - y)
        if d < mejor_d:
            mejor, mejor_d = nodo, d
    return mejor


def _tramos(coords):
    """Lista de tramos (origen, destino, tipo_via, sentido) antes de aplicar restricciones.
    sentido: 'doble' o 'uno' (solo origen -> destino)."""
    tramos = []
    letras = list(COLUMNAS)
    # Calles horizontales (de A a H en cada fila)
    for fila in FILAS:
        for i in range(len(letras) - 1):
            a, b = f"{letras[i]}{fila}", f"{letras[i+1]}{fila}"
            tipo = "avenida" if fila in FILAS_AVENIDA else "calle"
            if fila in FILAS_UNICO:
                if FILAS_UNICO[fila] == "E":
                    tramos.append((a, b, tipo, "uno"))
                else:
                    tramos.append((b, a, tipo, "uno"))
            else:
                tramos.append((a, b, tipo, "doble"))
    # Calles verticales (de la fila 1 a la 8 en cada columna)
    for letra in letras:
        for fila in range(1, 8):
            a, b = f"{letra}{fila}", f"{letra}{fila+1}"
            tipo = "avenida" if letra in COLUMNAS_AVENIDA else "calle"
            if letra in COLUMNAS_UNICO:
                if COLUMNAS_UNICO[letra] == "S":
                    tramos.append((a, b, tipo, "uno"))
                else:
                    tramos.append((b, a, tipo, "uno"))
            else:
                tramos.append((a, b, tipo, "doble"))
    # Avenida diagonal (doble sentido)
    for a, b in [("D4", "E5"), ("E5", "F6"), ("F6", "G7"), ("G7", "H8")]:
        tramos.append((a, b, "avenida", "doble"))
    return tramos


def construir_grafo(escenario, sentido_unico=True, penalizacion=True,
                     bloqueos=None, congestion=True, bloqueos_extra=None):
    """Construye el grafo dirigido con costos en MINUTOS.
    costo = (longitud / velocidad) * 60 * factor_congestion + penalizacion

    Los parámetros opcionales sirven para AISLAR cada restricción (criterio IV
    del informe: análisis empírico por funcionalidad), dejando las demás en su
    valor por defecto:
      sentido_unico  -> False: todas las calles pasan a doble sentido.
      penalizacion   -> False: no se suman minutos por bolardos/cadenas.
      bloqueos       -> None (por defecto): se activan solo si escenario ==
                        "bloqueo" (comportamiento original). True/False fuerza
                        el estado sin importar el escenario.
      congestion     -> False: factor de congestión = 1.0 (sin tráfico).
      bloqueos_extra -> lista adicional de tramos (origen, destino) a cortar,
                        para armar un escenario EXTREMO (varios cortes a la vez).
    Llamar solo con 'escenario' reproduce exactamente el comportamiento original.
    """
    coords = coordenadas()
    grafo = {nodo: [] for nodo in coords}

    aplicar_bloqueos = (escenario == "bloqueo") if bloqueos is None else bloqueos
    bloqueados = set()
    if aplicar_bloqueos:
        for a, b in BLOQUEADOS:
            bloqueados.add((a, b))
            bloqueados.add((b, a))
    if bloqueos_extra:
        for a, b in bloqueos_extra:
            bloqueados.add((a, b))
            bloqueados.add((b, a))

    for a, b, tipo, sentido in _tramos(coords):
        if not sentido_unico:
            sentido = "doble"
        # tramos estrechos: los que tienen penalización se tratan como vía estrecha
        pen = PENALIZACION.get((a, b), PENALIZACION.get((b, a), 0)) if penalizacion else 0
        tipo_real = "estrecha" if pen > 0 else tipo
        longitud = distancia_recta(coords, a, b)
        tiempo = longitud / VELOCIDAD[tipo_real] * 60
        factor = FACTOR[escenario][tipo_real] if congestion else 1.0
        costo = tiempo * factor + pen
        costo = round(costo, 4)

        sentidos = [(a, b)] if sentido == "uno" else [(a, b), (b, a)]
        for origen, destino in sentidos:
            if (origen, destino) in bloqueados:
                continue          # calle bloqueada: el tramo se elimina del mapa
            grafo[origen].append((destino, costo))
    return grafo, coords
