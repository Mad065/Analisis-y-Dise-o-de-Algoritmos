#!/usr/bin/env python3
"""
Práctica 5 — Programación Dinámica
Escuela Superior de Cómputo (ESCOM - IPN)
Materia: Análisis y Diseño de Algoritmos

Suite de pruebas unitarias y verificación de optimalidad:
  1. Consistencia matemática: recursiva == memo == tabulacion
  2. Optimalidad y validez de las soluciones reconstruidas (restricciones satisfechas)
  3. Demostración formal y empírica del fracaso de la heurística voraz en cambio no canónico
  4. Casos borde y de estrés (cadenas vacías, montos imposibles, pesos cero, capacidades nulas)
"""
import json
import os
import unittest
from typing import List

from programacion_dinamica import (
    cambio_memo,
    cambio_recursivo,
    cambio_tabulacion,
    cambio_voraz,
    lcs_subcadena_memo,
    lcs_subcadena_recursiva,
    lcs_subcadena_tabulacion,
    lcsq_memo,
    lcsq_recursiva,
    lcsq_tabulacion,
    mochila_memo,
    mochila_recursiva,
    mochila_tabulacion,
)

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_DATOS = os.path.join(DIR_ACTUAL, "datos")


def es_subsecuencia(sub: str, original: str) -> bool:
    """Verifica si `sub` es subsecuencia de `original`."""
    it = iter(original)
    return all(c in it for c in sub)


class TestMochila(unittest.TestCase):
    """Pruebas unitarias para el Problema de la Mochila 0/1."""

    def test_caso_clasico_libro(self):
        pesos = [2, 3, 4, 5]
        valores = [3, 4, 5, 8]
        capacidad = 8
        rec = mochila_recursiva(pesos, valores, capacidad)
        mem = mochila_memo(pesos, valores, capacidad)
        tab = mochila_tabulacion(pesos, valores, capacidad)

        self.assertEqual(rec.valor_optimo, 12)
        self.assertEqual(mem.valor_optimo, 12)
        self.assertEqual(tab.valor_optimo, 12)

        # Verificar reconstrucción
        indices = tab.solucion_reconstruida
        peso_total = sum(pesos[i] for i in indices)
        val_total = sum(valores[i] for i in indices)
        self.assertLessEqual(peso_total, capacidad)
        self.assertEqual(val_total, 12)

    def test_consistencia_casos_pequenos(self):
        with open(os.path.join(DIR_DATOS, "mochila_casos.json"), "r", encoding="utf-8") as f:
            casos = json.load(f)["pequenos"]

        for caso in casos:
            with self.subTest(nombre=caso["nombre"]):
                p, v, w = caso["pesos"], caso["valores"], caso["capacidad"]
                rec = mochila_recursiva(p, v, w)
                mem = mochila_memo(p, v, w)
                tab = mochila_tabulacion(p, v, w)

                self.assertEqual(rec.valor_optimo, mem.valor_optimo)
                self.assertEqual(mem.valor_optimo, tab.valor_optimo)

                # Validar restricciones de reconstrucción
                indices = tab.solucion_reconstruida
                self.assertLessEqual(sum(p[i] for i in indices), w)
                self.assertEqual(sum(v[i] for i in indices), tab.valor_optimo)

    def test_casos_borde(self):
        # Capacidad cero
        tab = mochila_tabulacion([1, 2, 3], [10, 20, 30], 0)
        self.assertEqual(tab.valor_optimo, 0)
        self.assertEqual(tab.solucion_reconstruida, [])

        # Mochila vacía
        tab_vacia = mochila_tabulacion([], [], 10)
        self.assertEqual(tab_vacia.valor_optimo, 0)
        self.assertEqual(tab_vacia.solucion_reconstruida, [])

        # Objetos exceden capacidad
        tab_excede = mochila_tabulacion([100, 200], [50, 60], 50)
        self.assertEqual(tab_excede.valor_optimo, 0)
        self.assertEqual(tab_excede.solucion_reconstruida, [])


class TestCambioMonedas(unittest.TestCase):
    """Pruebas unitarias para el Problema del Cambio de Monedas."""

    def test_consistencia_casos_pequenos(self):
        with open(os.path.join(DIR_DATOS, "cambio_casos.json"), "r", encoding="utf-8") as f:
            casos = json.load(f)["pequenos"]

        for caso in casos:
            with self.subTest(nombre=caso["nombre"]):
                monedas = caso["monedas"]
                monto = caso["monto"]
                rec = cambio_recursivo(monedas, monto)
                mem = cambio_memo(monedas, monto)
                tab = cambio_tabulacion(monedas, monto)

                self.assertEqual(rec.valor_optimo, mem.valor_optimo)
                self.assertEqual(mem.valor_optimo, tab.valor_optimo)

                # Validar reconstrucción
                self.assertEqual(sum(tab.solucion_reconstruida), monto)
                self.assertEqual(len(tab.solucion_reconstruida), tab.valor_optimo)

    def test_demostracion_optimalidad_dp_vs_voraz(self):
        """Demuestra que el algoritmo voraz es subóptimo en monedas no canónicas."""
        with open(os.path.join(DIR_DATOS, "cambio_casos.json"), "r", encoding="utf-8") as f:
            casos = json.load(f)["no_canonicos_vs_voraz"]

        for caso in casos:
            with self.subTest(nombre=caso["nombre"]):
                monedas = caso["monedas"]
                monto = caso["monto"]
                dp_res = cambio_tabulacion(monedas, monto)
                voraz_res = cambio_voraz(monedas, monto)

                # DP debe hallar el óptimo matemático
                self.assertEqual(dp_res.valor_optimo, caso["optimo_esperado"])
                # Voraz produce una solución subóptima (más monedas)
                self.assertEqual(voraz_res.valor_optimo, caso["voraz_esperado"])
                self.assertLess(dp_res.valor_optimo, voraz_res.valor_optimo)

    def test_casos_borde_e_imposibles(self):
        # Monto 0
        tab_cero = cambio_tabulacion([1, 2, 5], 0)
        self.assertEqual(tab_cero.valor_optimo, 0)
        self.assertEqual(tab_cero.solucion_reconstruida, [])

        # Monto imposible: monedas pares para monto impar
        tab_imp = cambio_tabulacion([2, 4, 6], 15)
        self.assertEqual(tab_imp.valor_optimo, -1)
        self.assertEqual(tab_imp.solucion_reconstruida, [])


class TestLCSq(unittest.TestCase):
    """Pruebas unitarias para la Subsecuencia Común Más Larga (LCSq)."""

    def test_caso_clasico_clrs(self):
        s1 = "ABCBDAB"
        s2 = "BDCABA"
        rec = lcsq_recursiva(s1, s2)
        mem = lcsq_memo(s1, s2)
        tab = lcsq_tabulacion(s1, s2)

        self.assertEqual(rec.valor_optimo, 4)
        self.assertEqual(mem.valor_optimo, 4)
        self.assertEqual(tab.valor_optimo, 4)

        # Validar que la solución reconstruida sea una subsecuencia válida de ambas
        sub = tab.solucion_reconstruida
        self.assertEqual(len(sub), 4)
        self.assertTrue(es_subsecuencia(sub, s1))
        self.assertTrue(es_subsecuencia(sub, s2))

    def test_consistencia_casos_pequenos(self):
        with open(os.path.join(DIR_DATOS, "cadenas_casos.json"), "r", encoding="utf-8") as f:
            casos = json.load(f)["pequenos"]

        for caso in casos:
            with self.subTest(nombre=caso["nombre"]):
                s1, s2 = caso["s1"], caso["s2"]
                rec = lcsq_recursiva(s1, s2)
                mem = lcsq_memo(s1, s2)
                tab = lcsq_tabulacion(s1, s2)

                self.assertEqual(rec.valor_optimo, mem.valor_optimo)
                self.assertEqual(mem.valor_optimo, tab.valor_optimo)

                sub = tab.solucion_reconstruida
                self.assertEqual(len(sub), tab.valor_optimo)
                self.assertTrue(es_subsecuencia(sub, s1))
                self.assertTrue(es_subsecuencia(sub, s2))

    def test_casos_borde(self):
        # Cadenas idénticas
        tab_id = lcsq_tabulacion("ESCOM", "ESCOM")
        self.assertEqual(tab_id.valor_optimo, 5)
        self.assertEqual(tab_id.solucion_reconstruida, "ESCOM")

        # Cadenas disjuntas
        tab_disj = lcsq_tabulacion("AAAA", "BBBB")
        self.assertEqual(tab_disj.valor_optimo, 0)
        self.assertEqual(tab_disj.solucion_reconstruida, "")

        # Cadena vacía
        tab_vacia = lcsq_tabulacion("", "HOLA")
        self.assertEqual(tab_vacia.valor_optimo, 0)
        self.assertEqual(tab_vacia.solucion_reconstruida, "")


class TestLCSCadena(unittest.TestCase):
    """Pruebas unitarias para la Subcadena Común Más Larga (LCS)."""

    def test_caso_clasico(self):
        s1 = "ALGORITMOS_ESCOM"
        s2 = "AVANZADO_ALGORITMOS_IPN"
        mem = lcs_subcadena_memo(s1, s2)
        tab = lcs_subcadena_tabulacion(s1, s2)

        esperado = len("ALGORITMOS_")
        self.assertEqual(mem.valor_optimo, esperado)
        self.assertEqual(tab.valor_optimo, esperado)

        sub = tab.solucion_reconstruida
        self.assertEqual(sub, "ALGORITMOS_")
        self.assertIn(sub, s1)
        self.assertIn(sub, s2)

    def test_recursivo_pequeno(self):
        s1 = "HOLA"
        s2 = "SOLAR"
        rec = lcs_subcadena_recursiva(s1, s2)
        mem = lcs_subcadena_memo(s1, s2)
        tab = lcs_subcadena_tabulacion(s1, s2)

        self.assertEqual(rec.valor_optimo, 3)  # "OLA"
        self.assertEqual(mem.valor_optimo, 3)
        self.assertEqual(tab.valor_optimo, 3)

    def test_consistencia_casos_pequenos(self):
        with open(os.path.join(DIR_DATOS, "cadenas_casos.json"), "r", encoding="utf-8") as f:
            casos = json.load(f)["pequenos"]

        for caso in casos:
            with self.subTest(nombre=caso["nombre"]):
                s1, s2 = caso["s1"], caso["s2"]
                rec = lcs_subcadena_recursiva(s1, s2)
                mem = lcs_subcadena_memo(s1, s2)
                tab = lcs_subcadena_tabulacion(s1, s2)

                self.assertEqual(rec.valor_optimo, mem.valor_optimo)
                self.assertEqual(mem.valor_optimo, tab.valor_optimo)

                sub = tab.solucion_reconstruida
                self.assertEqual(len(sub), tab.valor_optimo)
                if tab.valor_optimo > 0:
                    self.assertIn(sub, s1)
                    self.assertIn(sub, s2)

    def test_casos_borde(self):
        # Cadenas idénticas
        tab_id = lcs_subcadena_tabulacion("ESCOM_IPN", "ESCOM_IPN")
        self.assertEqual(tab_id.valor_optimo, 9)
        self.assertEqual(tab_id.solucion_reconstruida, "ESCOM_IPN")

        # Cadenas disjuntas
        tab_disj = lcs_subcadena_tabulacion("12345", "67890")
        self.assertEqual(tab_disj.valor_optimo, 0)
        self.assertEqual(tab_disj.solucion_reconstruida, "")

        # Cadena vacía
        tab_vacia = lcs_subcadena_tabulacion("", "TEST")
        self.assertEqual(tab_vacia.valor_optimo, 0)
        self.assertEqual(tab_vacia.solucion_reconstruida, "")


if __name__ == "__main__":
    unittest.main()
