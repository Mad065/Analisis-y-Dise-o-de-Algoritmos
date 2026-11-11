#!/usr/bin/env python3
"""
Práctica 5 — Programación Dinámica
Escuela Superior de Cómputo (ESCOM - IPN)
Materia: Análisis y Diseño de Algoritmos

Orquestador de benchmarking y evaluación empírica de alto rendimiento:
  - Tiempo de CPU de alta resolución (time.perf_counter_ns)
  - Memoria pico en heap con tracemalloc
  - Conteo de llamadas recursivas y tamaño del espacio de estados evaluado
  - Escalabilidad de Memoización vs Tabulación
  - Demostración cuantitativa de optimalidad: DP vs Heurística Voraz
"""
from __future__ import annotations

import gc
import json
import os
import random
import sys
import time
import tracemalloc
from typing import Any, Callable, Dict, List, Tuple

# Aumentar límite de recursión para soportar instancias medianas/grandes en Memoización
sys.setrecursionlimit(100000)

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
DIR_RESULTADOS = os.path.join(DIR_ACTUAL, "resultados")


def medir_ejecucion(
    func: Callable[..., Any],
    *args: Any,
    repeticiones: int = 3
) -> Dict[str, Any]:
    """Mide tiempo de CPU (promedio en ms), memoria pico (KiB) y métricas de ResultadoDP."""
    gc.collect()
    gc.disable()

    # Medición de memoria pico con tracemalloc
    tracemalloc.start()
    try:
        resultado_obj = func(*args)
        _, peak_mem_bytes = tracemalloc.get_traced_memory()
    except RecursionError:
        tracemalloc.stop()
        gc.enable()
        return {
            "error": "RecursionError",
            "tiempo_ms": None,
            "memoria_kib": None,
            "valor_optimo": None,
            "llamadas": None
        }
    finally:
        tracemalloc.stop()

    gc.enable()

    # Medición de tiempo con repeticiones
    tiempos = []
    for _ in range(repeticiones):
        gc.collect()
        t0 = time.perf_counter_ns()
        func(*args)
        t1 = time.perf_counter_ns()
        tiempos.append((t1 - t0) / 1_000_000.0)  # ms

    tiempo_prom_ms = sum(tiempos) / len(tiempos)

    return {
        "tiempo_ms": round(tiempo_prom_ms, 5),
        "memoria_kib": round(peak_mem_bytes / 1024.0, 3),
        "valor_optimo": resultado_obj.valor_optimo,
        "llamadas": resultado_obj.llamadas_recursivas,
        "subproblemas": resultado_obj.subproblemas_evaluados,
        "tamanio_tabla": resultado_obj.tamanio_tabla
    }


def benchmark_mochila_pequena(casos: List[dict]) -> List[dict]:
    print("-> Ejecutando benchmark Mochila (instancias pequeñas: 3 variantes)...")
    res = []
    for c in casos:
        p, v, w = c["pesos"], c["valores"], c["capacidad"]
        n = c["n"]

        m_rec = medir_ejecucion(mochila_recursiva, p, v, w, repeticiones=2)
        m_mem = medir_ejecucion(mochila_memo, p, v, w, repeticiones=5)
        m_tab = medir_ejecucion(mochila_tabulacion, p, v, w, repeticiones=5)

        res.append({
            "n": n,
            "capacidad": w,
            "recursivo": m_rec,
            "memo": m_mem,
            "tabulacion": m_tab
        })
    return res


def benchmark_mochila_escalabilidad() -> List[dict]:
    print("-> Ejecutando benchmark Mochila (escalabilidad: Memo vs Tabulación)...")
    res = []
    random.seed(123)
    tamanos = [50, 100, 150, 200, 300]
    for n in tamanos:
        pesos = [random.randint(1, 30) for _ in range(n)]
        valores = [random.randint(10, 100) for _ in range(n)]
        cap = n * 5

        m_mem = medir_ejecucion(mochila_memo, pesos, valores, cap, repeticiones=1)
        m_tab = medir_ejecucion(mochila_tabulacion, pesos, valores, cap, repeticiones=1)

        res.append({
            "n": n,
            "capacidad": cap,
            "memo": m_mem,
            "tabulacion": m_tab
        })
    return res


def benchmark_cambio_pequeno(casos: List[dict]) -> List[dict]:
    print("-> Ejecutando benchmark Cambio (instancias pequeñas: 3 variantes)...")
    res = []
    for c in casos:
        monedas = c["monedas"]
        monto = c["monto"]

        m_rec = medir_ejecucion(cambio_recursivo, monedas, monto, repeticiones=2)
        m_mem = medir_ejecucion(cambio_memo, monedas, monto, repeticiones=5)
        m_tab = medir_ejecucion(cambio_tabulacion, monedas, monto, repeticiones=5)

        res.append({
            "monto": monto,
            "monedas": monedas,
            "recursivo": m_rec,
            "memo": m_mem,
            "tabulacion": m_tab
        })
    return res


def benchmark_cambio_escalabilidad() -> List[dict]:
    print("-> Ejecutando benchmark Cambio (escalabilidad: Memo vs Tabulación)...")
    res = []
    monedas = [1, 2, 5, 10, 20, 50, 100]
    montos = [100, 500, 1000, 2500, 5000]

    for monto in montos:
        m_mem = medir_ejecucion(cambio_memo, monedas, monto, repeticiones=1)
        m_tab = medir_ejecucion(cambio_tabulacion, monedas, monto, repeticiones=1)

        res.append({
            "monto": monto,
            "memo": m_mem,
            "tabulacion": m_tab
        })
    return res


def benchmark_cambio_optimalidad_voraz(casos: List[dict]) -> List[dict]:
    print("-> Evaluando optimalidad matemática: DP vs Voraz en sistemas no canónicos...")
    res = []
    for c in casos:
        monedas = c["monedas"]
        monto = c["monto"]
        dp_res = cambio_tabulacion(monedas, monto)
        voraz_res = cambio_voraz(monedas, monto)

        res.append({
            "nombre": c["nombre"],
            "monedas": monedas,
            "monto": monto,
            "dp_optimo": dp_res.valor_optimo,
            "dp_monedas": dp_res.solucion_reconstruida,
            "voraz_monedas_total": voraz_res.valor_optimo,
            "voraz_monedas": voraz_res.solucion_reconstruida,
            "es_suboptimo_voraz": voraz_res.valor_optimo > dp_res.valor_optimo
        })
    return res


def benchmark_lcsq_pequeno(casos: List[dict]) -> List[dict]:
    print("-> Ejecutando benchmark LCSq (instancias pequeñas: 3 variantes)...")
    res = []
    for c in casos:
        s1, s2 = c["s1"], c["s2"]
        l = len(s1)

        m_rec = medir_ejecucion(lcsq_recursiva, s1, s2, repeticiones=2)
        m_mem = medir_ejecucion(lcsq_memo, s1, s2, repeticiones=5)
        m_tab = medir_ejecucion(lcsq_tabulacion, s1, s2, repeticiones=5)

        res.append({
            "longitud": l,
            "recursivo": m_rec,
            "memo": m_mem,
            "tabulacion": m_tab
        })
    return res


def benchmark_lcsq_escalabilidad() -> List[dict]:
    print("-> Ejecutando benchmark LCSq (escalabilidad: Memo vs Tabulación)...")
    res = []
    random.seed(999)
    bases = "ACGT"
    longitudes = [50, 100, 200, 350, 500]

    for l in longitudes:
        s1 = "".join(random.choices(bases, k=l))
        s2 = "".join(random.choices(bases, k=l))

        m_mem = medir_ejecucion(lcsq_memo, s1, s2, repeticiones=1)
        m_tab = medir_ejecucion(lcsq_tabulacion, s1, s2, repeticiones=1)

        res.append({
            "longitud": l,
            "memo": m_mem,
            "tabulacion": m_tab
        })
    return res


def benchmark_subcadena_pequena(casos: List[dict]) -> List[dict]:
    print("-> Ejecutando benchmark Subcadena LCS (instancias pequeñas: 3 variantes)...")
    res = []
    for c in casos:
        s1, s2 = c["s1"], c["s2"]
        l = len(s1)

        m_rec = medir_ejecucion(lcs_subcadena_recursiva, s1, s2, repeticiones=2)
        m_mem = medir_ejecucion(lcs_subcadena_memo, s1, s2, repeticiones=5)
        m_tab = medir_ejecucion(lcs_subcadena_tabulacion, s1, s2, repeticiones=5)

        res.append({
            "longitud": l,
            "recursivo": m_rec,
            "memo": m_mem,
            "tabulacion": m_tab
        })
    return res


def benchmark_subcadena_escalabilidad() -> List[dict]:
    print("-> Ejecutando benchmark Subcadena LCS (escalabilidad: Memo vs Tabulación)...")
    res = []
    random.seed(888)
    bases = "ACGT"
    longitudes = [50, 100, 200, 350, 500]

    for l in longitudes:
        s1 = "".join(random.choices(bases, k=l))
        s2 = "".join(random.choices(bases, k=l))

        m_mem = medir_ejecucion(lcs_subcadena_memo, s1, s2, repeticiones=1)
        m_tab = medir_ejecucion(lcs_subcadena_tabulacion, s1, s2, repeticiones=1)

        res.append({
            "longitud": l,
            "memo": m_mem,
            "tabulacion": m_tab
        })
    return res


def generar_tablas_markdown(resultados: dict) -> str:
    md = []
    md.append("# Tablas Comparativas de Rendimiento y Optimalidad — Práctica 5\n")

    # Tabla 1: Mochila pequeña
    md.append("## 1. Mochila 0/1: Comparativa de 3 Variantes (Tiempos y Llamadas)")
    md.append("| $n$ | Capacidad | Tiempo Rec (ms) | Tiempo Memo (ms) | Tiempo Tab (ms) | Llamadas Rec | Subproblemas Memo | Speedup Tab/Rec |")
    md.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for r in resultados["mochila_pequena"]:
        n = r["n"]
        cap = r["capacidad"]
        trec = r["recursivo"]["tiempo_ms"]
        tmem = r["memo"]["tiempo_ms"]
        ttab = r["tabulacion"]["tiempo_ms"]
        calls = r["recursivo"]["llamadas"]
        subp = r["memo"]["subproblemas"]
        sp = round(trec / ttab, 1) if ttab > 0 else "N/A"
        md.append(f"| {n} | {cap} | {trec} | {tmem} | {ttab} | {calls} | {subp} | **{sp}x** |")
    md.append("\n")

    # Tabla 2: Mochila escalabilidad
    md.append("## 2. Mochila 0/1: Escalabilidad a Gran Escala (Memoización vs Tabulación)")
    md.append("| $n$ | Capacidad | Tiempo Memo (ms) | Tiempo Tab (ms) | Memoria Memo (KiB) | Memoria Tab (KiB) | Relación Tiempo (Memo/Tab) |")
    md.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for r in resultados["mochila_escalabilidad"]:
        n = r["n"]
        cap = r["capacidad"]
        tmem = r["memo"]["tiempo_ms"]
        ttab = r["tabulacion"]["tiempo_ms"]
        mmem = r["memo"]["memoria_kib"]
        mtab = r["tabulacion"]["memoria_kib"]
        rel = round(tmem / ttab, 2) if ttab > 0 else "N/A"
        md.append(f"| {n} | {cap} | {tmem} | {ttab} | {mmem} | {mtab} | {rel}x |")
    md.append("\n")

    # Tabla 3: Cambio pequeñas
    md.append("## 3. Cambio de Monedas: Comparativa de 3 Variantes")
    md.append("| Monto $V$ | Tiempo Rec (ms) | Tiempo Memo (ms) | Tiempo Tab (ms) | Llamadas Rec | Subproblemas Memo | Speedup Tab/Rec |")
    md.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for r in resultados["cambio_pequeno"]:
        v = r["monto"]
        trec = r["recursivo"]["tiempo_ms"]
        tmem = r["memo"]["tiempo_ms"]
        ttab = r["tabulacion"]["tiempo_ms"]
        calls = r["recursivo"]["llamadas"]
        subp = r["memo"]["subproblemas"]
        sp = round(trec / ttab, 1) if ttab > 0 else "N/A"
        md.append(f"| {v} | {trec} | {tmem} | {ttab} | {calls} | {subp} | **{sp}x** |")
    md.append("\n")

    # Tabla 4: Demostración de Optimalidad DP vs Voraz
    md.append("## 4. Demostración Cuantitativa de Optimalidad: DP vs Voraz (Sistemas No Canónicos)")
    md.append("| Instancia | Monedas $C$ | Monto $V$ | Monedas Óptimas (DP) | Solución DP | Monedas Voraz | Solución Voraz | ¿Voraz Subóptimo? |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for r in resultados["cambio_optimalidad"]:
        nom = r["nombre"]
        coins = str(r["monedas"])
        v = r["monto"]
        opt = r["dp_optimo"]
        sol_dp = str(r["dp_monedas"])
        vor = r["voraz_monedas_total"]
        sol_vor = str(r["voraz_monedas"])
        subopt = "✅ SÍ (Demostrado)" if r["es_suboptimo_voraz"] else "No"
        md.append(f"| `{nom}` | {coins} | {v} | **{opt}** | `{sol_dp}` | {vor} | `{sol_vor}` | {subopt} |")
    md.append("\n")

    # Tabla 5: LCSq pequeñas
    md.append("## 5. LCSq: Comparativa de 3 Variantes")
    md.append("| Longitud $L$ | Tiempo Rec (ms) | Tiempo Memo (ms) | Tiempo Tab (ms) | Llamadas Rec | Subproblemas Memo | Speedup Tab/Rec |")
    md.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for r in resultados["lcsq_pequeno"]:
        l = r["longitud"]
        trec = r["recursivo"]["tiempo_ms"]
        tmem = r["memo"]["tiempo_ms"]
        ttab = r["tabulacion"]["tiempo_ms"]
        calls = r["recursivo"]["llamadas"]
        subp = r["memo"]["subproblemas"]
        sp = round(trec / ttab, 1) if ttab > 0 else "N/A"
        md.append(f"| {l} | {trec} | {tmem} | {ttab} | {calls} | {subp} | **{sp}x** |")
    md.append("\n")

    # Tabla 6: Subcadena pequeñas
    md.append("## 6. Subcadena LCS: Comparativa de 3 Variantes")
    md.append("| Longitud $L$ | Tiempo Rec (ms) | Tiempo Memo (ms) | Tiempo Tab (ms) | Llamadas Rec | Subproblemas Memo | Speedup Tab/Rec |")
    md.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    for r in resultados["subcadena_pequena"]:
        l = r["longitud"]
        trec = r["recursivo"]["tiempo_ms"]
        tmem = r["memo"]["tiempo_ms"]
        ttab = r["tabulacion"]["tiempo_ms"]
        calls = r["recursivo"]["llamadas"]
        subp = r["memo"]["subproblemas"]
        sp = round(trec / ttab, 1) if ttab > 0 else "N/A"
        md.append(f"| {l} | {trec} | {tmem} | {ttab} | {calls} | {subp} | **{sp}x** |")
    md.append("\n")

    return "\n".join(md)


def main() -> None:
    os.makedirs(DIR_RESULTADOS, exist_ok=True)

    with open(os.path.join(DIR_DATOS, "mochila_casos.json"), "r", encoding="utf-8") as f:
        mochila_casos = json.load(f)
    with open(os.path.join(DIR_DATOS, "cambio_casos.json"), "r", encoding="utf-8") as f:
        cambio_casos = json.load(f)
    with open(os.path.join(DIR_DATOS, "cadenas_casos.json"), "r", encoding="utf-8") as f:
        cadenas_casos = json.load(f)

    resultados = {
        "mochila_pequena": benchmark_mochila_pequena(mochila_casos["pequenos"]),
        "mochila_escalabilidad": benchmark_mochila_escalabilidad(),
        "cambio_pequeno": benchmark_cambio_pequeno(cambio_casos["pequenos"]),
        "cambio_escalabilidad": benchmark_cambio_escalabilidad(),
        "cambio_optimalidad": benchmark_cambio_optimalidad_voraz(cambio_casos["no_canonicos_vs_voraz"]),
        "lcsq_pequeno": benchmark_lcsq_pequeno(cadenas_casos["pequenos"]),
        "lcsq_escalabilidad": benchmark_lcsq_escalabilidad(),
        "subcadena_pequena": benchmark_subcadena_pequena(cadenas_casos["pequenos"]),
        "subcadena_escalabilidad": benchmark_subcadena_escalabilidad(),
    }

    # Guardar JSON
    ruta_json = os.path.join(DIR_RESULTADOS, "resultados.json")
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2)

    # Generar tablas Markdown
    md_content = generar_tablas_markdown(resultados)
    ruta_tablas = os.path.join(DIR_RESULTADOS, "tablas.md")
    with open(ruta_tablas, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n[OK] Benchmarking finalizado exitosamente:")
    print(f"  - Métricas guardadas en: {ruta_json}")
    print(f"  - Tablas generadas en: {ruta_tablas}")


if __name__ == "__main__":
    main()
