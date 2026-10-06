#!/usr/bin/env python3
"""Pruebas unitarias de los 5 algoritmos de ordenamiento (Python).

Ejecutar:  python -m unittest test_ordenamiento -v
"""
import random
import unittest
from array import array

from ordenamiento import ALGORITMOS


def reales_2_decimales(rng, n, lo=-50_000, hi=50_000):
    """Reales con 2 decimales (requisito de Counting Sort), incluye negativos."""
    return [rng.randrange(lo, hi) / 100 for _ in range(n)]


class PruebasOrdenamiento(unittest.TestCase):

    def verificar(self, datos):
        esperado = sorted(datos)
        for nombre, algoritmo in ALGORITMOS.items():
            with self.subTest(algoritmo=nombre, n=len(datos)):
                a = array("d", datos)
                algoritmo(a)
                self.assertEqual(list(a), esperado)

    def test_vacio(self):
        self.verificar([])

    def test_un_elemento(self):
        self.verificar([3.14])

    def test_dos_elementos(self):
        self.verificar([2.5, 1.25])

    def test_ya_ordenado(self):
        self.verificar([i / 100 for i in range(1000)])

    def test_orden_inverso(self):
        self.verificar([i / 100 for i in range(1000, 0, -1)])

    def test_todos_iguales(self):
        self.verificar([7.77] * 500)

    def test_con_duplicados(self):
        rng = random.Random(1)
        self.verificar([rng.randrange(20) / 100 for _ in range(2000)])

    def test_negativos(self):
        rng = random.Random(2)
        self.verificar(reales_2_decimales(rng, 1000, -100_000, 0))

    def test_aleatorio_5000(self):
        rng = random.Random(3)
        self.verificar(reales_2_decimales(rng, 5000))

    def test_rango_del_dataset(self):
        """Mismo rango que el benchmark: [0, 10 000) con 2 decimales."""
        rng = random.Random(4)
        self.verificar([rng.randrange(1_000_000) / 100 for _ in range(3000)])

    def test_reales_precision_completa(self):
        """Los algoritmos por comparación funcionan con cualquier real."""
        rng = random.Random(5)
        datos = [rng.uniform(-1e6, 1e6) for _ in range(3000)]
        esperado = sorted(datos)
        for nombre in ("bubble", "merge", "tree", "heap"):
            with self.subTest(algoritmo=nombre):
                a = array("d", datos)
                ALGORITMOS[nombre](a)
                self.assertEqual(list(a), esperado)


if __name__ == "__main__":
    unittest.main(verbosity=2)
