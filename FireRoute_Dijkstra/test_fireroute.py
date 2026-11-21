"""Pruebas automáticas de contrato para el algoritmo de FireRoute."""
import unittest
from mapa import construir_grafo, coordenadas, ESTACION, VEL_MAX
from algoritmo import buscar_ruta

class FireRouteTests(unittest.TestCase):
    def test_ruta_normal(self):
        grafo, coords = construir_grafo("normal")
        ruta, minutos, explorados = buscar_ruta(grafo, coords, ESTACION, "H8", VEL_MAX)
        self.assertIsNotNone(ruta)
        self.assertEqual(ruta[0], ESTACION)
        self.assertEqual(ruta[-1], "H8")
        self.assertGreater(minutos, 0)
        self.assertGreater(explorados, 0)

    def test_destino_inexistente(self):
        grafo, coords = construir_grafo("normal")
        ruta, minutos, _ = buscar_ruta(grafo, coords, ESTACION, "ZZ", VEL_MAX)
        self.assertIsNone(ruta)
        self.assertEqual(minutos, float("inf"))

    def test_origen_inexistente(self):
        grafo, coords = construir_grafo("normal")
        ruta, minutos, _ = buscar_ruta(grafo, coords, "ZZ", "H8", VEL_MAX)
        self.assertIsNone(ruta)
        self.assertEqual(minutos, float("inf"))

    def test_destino_aislado(self):
        grafo, coords = construir_grafo("normal")
        grafo["ISLA"] = []
        coords["ISLA"] = (99.0, 99.0)
        ruta, minutos, _ = buscar_ruta(grafo, coords, ESTACION, "ISLA", VEL_MAX)
        self.assertIsNone(ruta)
        self.assertEqual(minutos, float("inf"))

    def test_estacion_aislada_por_bloqueos(self):
        cortes = [("D4", "D3"), ("D4", "C4"), ("D4", "D5"),
                  ("D4", "E5"), ("D4", "E4")]
        grafo, coords = construir_grafo("normal", bloqueos_extra=cortes)
        ruta, minutos, _ = buscar_ruta(grafo, coords, ESTACION, "H8", VEL_MAX)
        self.assertIsNone(ruta)
        self.assertEqual(minutos, float("inf"))

    def test_costo_no_negativo(self):
        for escenario in ("normal", "hora_punta", "bloqueo"):
            grafo, _ = construir_grafo(escenario)
            for aristas in grafo.values():
                for _, costo in aristas:
                    self.assertGreaterEqual(costo, 0)

if __name__ == "__main__":
    unittest.main()
