#Ejecutar con: python -m unittest test_split_paddle.py
import unittest
from split_paddle import calcular_pagos


class TestCalcularPagos(unittest.TestCase):
    def test_un_jugador_todo_el_tiempo(self):
        jugadores = [{"nombre": "A", "llegada": 18, "salida": 20}]
        total = 1000
        inicio = 18
        fin = 20
        pagos = calcular_pagos(jugadores, total, inicio, fin)
        self.assertEqual(len(pagos), 1)
        self.assertEqual(pagos[0]["pago"], 1000)
        self.assertAlmostEqual(pagos[0]["tiempo"], 2.0)

    def test_dos_jugadores_mismo_tiempo(self):
        jugadores = [
            {"nombre": "A", "llegada": 18, "salida": 20},
            {"nombre": "B", "llegada": 18, "salida": 20},
        ]
        total = 1000
        inicio = 18
        fin = 20
        pagos = calcular_pagos(jugadores, total, inicio, fin)
        self.assertEqual(pagos[0]["pago"] + pagos[1]["pago"], 1000)
        self.assertEqual(pagos[0]["pago"], 500)
        self.assertEqual(pagos[1]["pago"], 500)

    def test_jugador_parte_del_tiempo(self):
        jugadores = [
            {"nombre": "A", "llegada": 18, "salida": 20},
            {"nombre": "B", "llegada": 19, "salida": 20},
        ]
        total = 900
        inicio = 18
        fin = 20
        pagos = calcular_pagos(jugadores, total, inicio, fin)
        # A juega 2h, B juega 1h. Total 3h. A paga 2/3, B paga 1/3.
        self.assertEqual(pagos[0]["pago"] + pagos[1]["pago"], 900)
        self.assertEqual(pagos[0]["pago"], 600)
        self.assertEqual(pagos[1]["pago"], 300)

    def test_jugador_fuera_de_rango(self):
        jugadores = [
            {"nombre": "A", "llegada": 17, "salida": 18},
            {"nombre": "B", "llegada": 18, "salida": 20},
        ]
        total = 1000
        inicio = 18
        fin = 20
        pagos = calcular_pagos(jugadores, total, inicio, fin)
        # A no juega nada, B juega todo
        self.assertEqual(pagos[0]["pago"], 0)
        self.assertEqual(pagos[1]["pago"], 1000)


if __name__ == "__main__":
    unittest.main()
