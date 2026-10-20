#!/usr/bin/env python3
"""
Pruebas unitarias automatizadas para la Práctica 3 (Divide y Vencerás).

Ejecutar:
    python3 -m unittest test_divide_venceras -v
"""
from __future__ import annotations

import os
import random
import sys
import unittest
from array import array

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from divide_venceras import (
    convertir_a_2d,
    multiplicar_strassen_1d,
    multiplicar_strassen_2d,
    multiplicar_tradicional_1d,
    multiplicar_tradicional_2d,
    quickselect_hoare,
)


class PruebasQuickselect(unittest.TestCase):
    """Pruebas unitarias para Quickselect (Selección de Hoare) en 32 y 64 bits."""

    def verificar_arreglo(self, datos: list[int]):
        esperado = sorted(datos)
        n = len(datos)
        posiciones = sorted({1, max(1, n // 4), (n // 2) + 1, max(1, (3 * n) // 4), n})
        for bits, codigo in ((32, "i"), (64, "q")):
            for k in posiciones:
                with self.subTest(bits=bits, n=n, k=k):
                    arr = array(codigo, datos)
                    res = quickselect_hoare(arr, k)
                    self.assertEqual(res, esperado[k - 1])
                    # Verificar invariante de partición de Hoare alrededor de k-1
                    self.assertTrue(all(x <= res for x in arr[: k - 1]))
                    self.assertTrue(all(x >= res for x in arr[k:]))

    def test_un_elemento(self):
        self.verificar_arreglo([42])

    def test_dos_elementos(self):
        self.verificar_arreglo([99, 12])
        self.verificar_arreglo([12, 99])

    def test_ya_ordenado(self):
        self.verificar_arreglo(list(range(1, 501)))

    def test_orden_inverso(self):
        self.verificar_arreglo(list(range(500, 0, -1)))

    def test_todos_iguales(self):
        self.verificar_arreglo([777] * 200)

    def test_con_duplicados(self):
        rng = random.Random(10)
        self.verificar_arreglo([rng.randint(1, 15) for _ in range(800)])

    def test_permutacion_rango_10M(self):
        rng = random.Random(20)
        datos = rng.sample(range(1, 10_000_001), 2000)
        self.verificar_arreglo(datos)

    def test_todas_las_k_en_arreglo_pequeno(self):
        rng = random.Random(30)
        datos = rng.sample(range(1, 1000), 45)
        esperado = sorted(datos)
        for k in range(1, len(datos) + 1):
            a32 = array("i", datos)
            a64 = array("q", datos)
            self.assertEqual(quickselect_hoare(a32, k), esperado[k - 1])
            self.assertEqual(quickselect_hoare(a64, k), esperado[k - 1])

    def test_k_fuera_de_rango(self):
        a = array("i", [3, 1, 2])
        with self.assertRaises(ValueError):
            quickselect_hoare(a, 0)
        with self.assertRaises(ValueError):
            quickselect_hoare(a, 4)


class PruebasMatrices(unittest.TestCase):
    """Pruebas unitarias para Multiplicación Tradicional y Strassen (2D y 1D)."""

    def verificar_multiplicacion(self, A1d: array, B1d: array, n: int):
        A2d = convertir_a_2d(A1d, n)
        B2d = convertir_a_2d(B1d, n)

        C_trad_2d = multiplicar_tradicional_2d(A2d, B2d, n)
        C_trad_1d = multiplicar_tradicional_1d(A1d, B1d, n)
        C_stras_2d = multiplicar_strassen_2d(A2d, B2d, n)
        C_stras_1d = multiplicar_strassen_1d(A1d, B1d, n)

        # Verificar que las 4 variantes produzcan exactamente la misma matriz
        self.assertEqual(C_trad_2d, C_stras_2d)
        self.assertEqual(list(C_trad_1d), list(C_stras_1d))
        self.assertEqual(convertir_a_2d(C_trad_1d, n), C_trad_2d)

    def test_caso_base_1x1(self):
        A = array("i", [7])
        B = array("i", [-9])
        self.verificar_multiplicacion(A, B, 1)

    def test_matriz_2x2(self):
        A = array("i", [1, 2, 3, 4])
        B = array("i", [5, 6, 7, 8])
        self.verificar_multiplicacion(A, B, 2)
        C = multiplicar_strassen_1d(A, B, 2)
        self.assertEqual(list(C), [19, 22, 43, 50])

    def test_matriz_identidad(self):
        n = 16
        rng = random.Random(50)
        A = array("i", (rng.randint(-100, 100) for _ in range(n * n)))
        I = array("i", (1 if i == j else 0 for i in range(n) for j in range(n)))
        self.assertEqual(list(multiplicar_strassen_1d(A, I, n)), list(A))
        self.assertEqual(list(multiplicar_strassen_1d(I, A, n)), list(A))

    def test_matriz_ceros(self):
        n = 16
        Z = array("i", [0]) * (n * n)
        A = array("i", range(n * n))
        self.assertEqual(list(multiplicar_strassen_1d(A, Z, n)), [0] * (n * n))

    def test_tamanios_potencia_de_dos(self):
        rng = random.Random(77)
        for n in (4, 8, 16, 32, 64):
            with self.subTest(n=n):
                A = array("i", (rng.randint(-100, 100) for _ in range(n * n)))
                B = array("i", (rng.randint(-100, 100) for _ in range(n * n)))
                self.verificar_multiplicacion(A, B, n)


if __name__ == "__main__":
    unittest.main(verbosity=2)
