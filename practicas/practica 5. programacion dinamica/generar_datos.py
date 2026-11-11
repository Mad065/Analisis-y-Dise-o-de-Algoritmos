#!/usr/bin/env python3
"""
Práctica 5 — Programación Dinámica
Escuela Superior de Cómputo (ESCOM - IPN)
Materia: Análisis y Diseño de Algoritmos

Generador de datasets y casos de prueba reproducibles para:
  1. Problema de la Mochila 0/1 (pequeños, medianos, grandes, correlaciones)
  2. Problema del Cambio de Monedas (canónicos, no canónicos y patológicos para Greedy)
  3. Subsecuencia Común Más Larga LCSq y Subcadena Común LCS (ADN y sintéticos)
"""
from __future__ import annotations

import json
import os
import random

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_DATOS = os.path.join(DIR_ACTUAL, "datos")


def generar_casos_mochila() -> dict:
    random.seed(42)
    casos = {
        "pequenos": [],
        "medianos": [],
        "grandes": [],
        "especiales": []
    }

    # Casos pequeños (aptos para recursión ingenua)
    for n in [4, 8, 12, 16, 20]:
        pesos = [random.randint(1, 15) for _ in range(n)]
        valores = [random.randint(5, 50) for _ in range(n)]
        capacidad = sum(pesos) // 2
        casos["pequenos"].append({
            "nombre": f"mochila_n{n}_w{capacidad}",
            "n": n,
            "pesos": pesos,
            "valores": valores,
            "capacidad": capacidad
        })

    # Casos medianos (para memoización y tabulación)
    for n in [50, 100, 200]:
        pesos = [random.randint(1, 30) for _ in range(n)]
        valores = [random.randint(10, 100) for _ in range(n)]
        capacidad = sum(pesos) // 3
        casos["medianos"].append({
            "nombre": f"mochila_med_n{n}",
            "n": n,
            "pesos": pesos,
            "valores": valores,
            "capacidad": capacidad
        })

    # Casos grandes (estrés de memoria y escalabilidad)
    for n, cap in [(500, 1000), (1000, 2000)]:
        pesos = [random.randint(1, 50) for _ in range(n)]
        valores = [random.randint(10, 200) for _ in range(n)]
        casos["grandes"].append({
            "nombre": f"mochila_gran_n{n}_cap{cap}",
            "n": n,
            "pesos": pesos,
            "valores": valores,
            "capacidad": cap
        })

    # Casos especiales
    # 1. Correlación inversa (ítems ligeros muy valiosos)
    pesos_inv = [2, 3, 5, 20, 30]
    valores_inv = [50, 45, 60, 10, 5]
    casos["especiales"].append({
        "nombre": "correlacion_inversa",
        "pesos": pesos_inv,
        "valores": valores_inv,
        "capacidad": 15
    })

    # 2. Ítems exceden capacidad
    casos["especiales"].append({
        "nombre": "excede_capacidad",
        "pesos": [50, 60, 70],
        "valores": [100, 200, 300],
        "capacidad": 30
    })

    return casos


def generar_casos_cambio() -> dict:
    casos = {
        "pequenos": [],
        "medianos": [],
        "grandes": [],
        "no_canonicos_vs_voraz": [],
        "imposibles": []
    }

    # Sistemas monetarios
    sistema_mxn = [1, 2, 5, 10, 20]
    sistema_usd = [1, 5, 10, 25]

    # Pequeños (recursión ingenua: denominaciones [1, 2, 5] para evidenciar curva exponencial controlada)
    sistema_peq = [1, 2, 5]
    for monto in [6, 9, 12, 15, 18]:
        casos["pequenos"].append({
            "nombre": f"cambio_peq_m{monto}",
            "monedas": sistema_peq,
            "monto": monto
        })

    # Medianos
    for monto in [100, 250, 500, 1000]:
        casos["medianos"].append({
            "nombre": f"cambio_med_m{monto}",
            "monedas": sistema_mxn,
            "monto": monto
        })

    # Grandes
    for monto in [2500, 5000, 10000]:
        casos["grandes"].append({
            "nombre": f"cambio_gran_m{monto}",
            "monedas": sistema_mxn,
            "monto": monto
        })

    # Sistemas no canónicos (falla de voraz vs DP)
    casos["no_canonicos_vs_voraz"] = [
        {
            "nombre": "no_canonico_1_3_4_m6",
            "descripcion": "Monedas [1, 3, 4], monto 6. Voraz elige 4+1+1 (3 monedas). DP elige 3+3 (2 monedas).",
            "monedas": [1, 3, 4],
            "monto": 6,
            "optimo_esperado": 2,
            "voraz_esperado": 3
        },
        {
            "nombre": "no_canonico_1_15_25_m30",
            "descripcion": "Monedas [1, 15, 25], monto 30. Voraz elige 25+1*5 (6 monedas). DP elige 15+15 (2 monedas).",
            "monedas": [1, 15, 25],
            "monto": 30,
            "optimo_esperado": 2,
            "voraz_esperado": 6
        },
        {
            "nombre": "no_canonico_1_6_10_m12",
            "descripcion": "Monedas [1, 6, 10], monto 12. Voraz elige 10+1+1 (3 monedas). DP elige 6+6 (2 monedas).",
            "monedas": [1, 6, 10],
            "monto": 12,
            "optimo_esperado": 2,
            "voraz_esperado": 3
        }
    ]

    # Casos imposibles
    casos["imposibles"].append({
        "nombre": "imposible_pares_monto_impar",
        "monedas": [2, 4, 6],
        "monto": 15,
        "optimo_esperado": -1
    })

    return casos


def generar_casos_cadenas() -> dict:
    random.seed(1337)
    casos = {
        "pequenos": [],
        "medianos": [],
        "grandes": [],
        "especiales": []
    }

    # Pequeños (recursión ingenua: longitud moderada para evitar explosión 3^(2l))
    letras = "ABCD"
    for l in [3, 4, 5, 6, 7]:
        s1 = "".join(random.choices(letras, k=l))
        s2 = "".join(random.choices(letras, k=l))
        casos["pequenos"].append({
            "nombre": f"cadenas_peq_len{l}",
            "s1": s1,
            "s2": s2
        })

    # Medianos
    bases = "ACGT"
    for l in [50, 100, 250, 500]:
        s1 = "".join(random.choices(bases, k=l))
        s2 = "".join(random.choices(bases, k=l))
        casos["medianos"].append({
            "nombre": f"cadenas_med_adn_len{l}",
            "s1": s1,
            "s2": s2
        })

    # Grandes
    for l in [1000, 2000]:
        s1 = "".join(random.choices(bases, k=l))
        s2 = "".join(random.choices(bases, k=l))
        casos["grandes"].append({
            "nombre": f"cadenas_gran_adn_len{l}",
            "s1": s1,
            "s2": s2
        })

    # Casos especiales
    casos["especiales"] = [
        {
            "nombre": "identicas",
            "s1": "ALGORITMOS_ESCOM_IPN",
            "s2": "ALGORITMOS_ESCOM_IPN",
            "lcsq_esperado": 20,
            "subcadena_esperada": 20
        },
        {
            "nombre": "completamente_disjuntas",
            "s1": "AAAAAAA",
            "s2": "BBBBBBB",
            "lcsq_esperado": 0,
            "subcadena_esperada": 0
        },
        {
            "nombre": "subcadena_insertada",
            "s1": "PRE_PROGRAMACION_DINAMICA_SUF",
            "s2": "OTRO_PROGRAMACION_DINAMICA_FIN",
            "subcadena_esperada": len("PROGRAMACION_DINAMICA")
        }
    ]

    return casos


def main() -> None:
    os.makedirs(DIR_DATOS, exist_ok=True)

    mochila = generar_casos_mochila()
    with open(os.path.join(DIR_DATOS, "mochila_casos.json"), "w", encoding="utf-8") as f:
        json.dump(mochila, f, indent=2)

    cambio = generar_casos_cambio()
    with open(os.path.join(DIR_DATOS, "cambio_casos.json"), "w", encoding="utf-8") as f:
        json.dump(cambio, f, indent=2)

    cadenas = generar_casos_cadenas()
    with open(os.path.join(DIR_DATOS, "cadenas_casos.json"), "w", encoding="utf-8") as f:
        json.dump(cadenas, f, indent=2)

    print(f"Datasets generados con éxito en: {DIR_DATOS}")
    print(f" - mochila_casos.json: {len(mochila['pequenos'])} pequeños, {len(mochila['medianos'])} medianos, {len(mochila['grandes'])} grandes")
    print(f" - cambio_casos.json: {len(cambio['pequenos'])} pequeños, {len(cambio['medianos'])} medianos, {len(cambio['no_canonicos_vs_voraz'])} no canónicos")
    print(f" - cadenas_casos.json: {len(cadenas['pequenos'])} pequeños, {len(cadenas['medianos'])} medianos, {len(cadenas['grandes'])} grandes")


if __name__ == "__main__":
    main()
