#!/usr/bin/env python3
"""
Práctica 5 — Generador de Gráficas Estadísticas y Comparativas
Materia: Análisis y Diseño de Algoritmos (ESCOM - IPN)

Genera visualizaciones de alto impacto con matplotlib:
  1. 01_mochila_tiempo_comparativa.png: Curva semilogarítmica Recursivo vs Memo vs Tabulación.
  2. 02_cambio_tiempo_comparativa.png: Explosión exponencial en Cambio de Monedas.
  3. 03_cadenas_tiempo_comparativa.png: Comparativa en LCSq y Subcadena LCS.
  4. 04_escalabilidad_memo_vs_tabulacion.png: Rendimiento a gran escala (Memo vs Tabulación).
  5. 05_consumo_memoria_comparativa.png: Huella de memoria (Hash Map vs Matriz DP).
  6. 06_cambio_optimalidad_dp_vs_voraz.png: Demostración cuantitativa DP vs Voraz.
"""
from __future__ import annotations

import json
import os
import matplotlib.pyplot as plt
import numpy as np

DIR_ACTUAL = os.path.dirname(os.path.abspath(__file__))
DIR_RESULTADOS = os.path.join(DIR_ACTUAL, "resultados")
DIR_GRAFICAS = os.path.join(DIR_ACTUAL, "graficas")


def configurar_estilo() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
        "axes.grid": True,
        "grid.alpha": 0.35,
        "grid.linestyle": "--",
        "figure.autolayout": True
    })


def graficar_mochila_pequena(data: list) -> None:
    n_vals = [d["n"] for d in data]
    t_rec = [d["recursivo"]["tiempo_ms"] for d in data]
    t_mem = [d["memo"]["tiempo_ms"] for d in data]
    t_tab = [d["tabulacion"]["tiempo_ms"] for d in data]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(n_vals, t_rec, marker="o", color="#d62728", linewidth=2.2, label="Recursiva Ingenua $O(2^n)$")
    ax.plot(n_vals, t_mem, marker="s", color="#ff7f0e", linewidth=2.0, label="Memoización (Top-down) $O(n W)$")
    ax.plot(n_vals, t_tab, marker="^", color="#2ca02c", linewidth=2.0, label="Tabulación (Bottom-up) $O(n W)$")

    ax.set_yscale("log")
    ax.set_xlabel("Número de elementos ($n$)")
    ax.set_ylabel("Tiempo de ejecución (ms) — Escala Logarítmica")
    ax.set_title("Mochila 0/1: Explosión Exponencial vs. Programación Dinámica")
    ax.legend()

    # Anotación del speedup en n=20
    sp = round(t_rec[-1] / t_tab[-1], 1)
    ax.annotate(
        f"Speedup Tabulación:\n{sp}x más rápida",
        xy=(n_vals[-1], t_tab[-1]),
        xytext=(n_vals[-1] - 4, t_tab[-1] * 25),
        arrowprops=dict(facecolor="#2ca02c", shrink=0.08, width=1.5, headwidth=7),
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#e8f5e9", edgecolor="#2ca02c")
    )

    salida = os.path.join(DIR_GRAFICAS, "01_mochila_tiempo_comparativa.png")
    fig.savefig(salida)
    plt.close(fig)
    print(f" -> Guardada: {salida}")


def graficar_cambio_pequeno(data: list) -> None:
    montos = [d["monto"] for d in data]
    t_rec = [d["recursivo"]["tiempo_ms"] for d in data]
    t_mem = [d["memo"]["tiempo_ms"] for d in data]
    t_tab = [d["tabulacion"]["tiempo_ms"] for d in data]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    ax.plot(montos, t_rec, marker="o", color="#d62728", linewidth=2.2, label="Recursiva Ingenua $O(k^V)$")
    ax.plot(montos, t_mem, marker="s", color="#1f77b4", linewidth=2.0, label="Memoización $O(k V)$")
    ax.plot(montos, t_tab, marker="^", color="#2ca02c", linewidth=2.0, label="Tabulación $O(k V)$")

    ax.set_yscale("log")
    ax.set_xlabel("Monto objetivo ($V$)")
    ax.set_ylabel("Tiempo de ejecución (ms) — Escala Logarítmica")
    ax.set_title("Cambio de Monedas: Crecimiento Exponencial vs. Polinomial")
    ax.legend()

    salida = os.path.join(DIR_GRAFICAS, "02_cambio_tiempo_comparativa.png")
    fig.savefig(salida)
    plt.close(fig)
    print(f" -> Guardada: {salida}")


def graficar_cadenas_pequenas(data_lcsq: list, data_sub: list) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    # Subplot 1: LCSq
    l_lcsq = [d["longitud"] for d in data_lcsq]
    t_rec1 = [d["recursivo"]["tiempo_ms"] for d in data_lcsq]
    t_mem1 = [d["memo"]["tiempo_ms"] for d in data_lcsq]
    t_tab1 = [d["tabulacion"]["tiempo_ms"] for d in data_lcsq]

    ax1.plot(l_lcsq, t_rec1, marker="o", color="#d62728", label="Recursiva $O(2^{2L})$")
    ax1.plot(l_lcsq, t_mem1, marker="s", color="#ff7f0e", label="Memoización $O(L^2)$")
    ax1.plot(l_lcsq, t_tab1, marker="^", color="#2ca02c", label="Tabulación $O(L^2)$")
    ax1.set_yscale("log")
    ax1.set_xlabel("Longitud de cadenas ($L$)")
    ax1.set_ylabel("Tiempo (ms) — Escala Log")
    ax1.set_title("LCSq (Subsecuencia Común)")
    ax1.legend()

    # Subplot 2: Subcadena LCS
    l_sub = [d["longitud"] for d in data_sub]
    t_rec2 = [d["recursivo"]["tiempo_ms"] for d in data_sub]
    t_mem2 = [d["memo"]["tiempo_ms"] for d in data_sub]
    t_tab2 = [d["tabulacion"]["tiempo_ms"] for d in data_sub]

    ax2.plot(l_sub, t_rec2, marker="o", color="#d62728", label="Recursiva $O(3^{2L})$")
    ax2.plot(l_sub, t_mem2, marker="s", color="#ff7f0e", label="Memoización $O(L^2)$")
    ax2.plot(l_sub, t_tab2, marker="^", color="#2ca02c", label="Tabulación $O(L^2)$")
    ax2.set_yscale("log")
    ax2.set_xlabel("Longitud de cadenas ($L$)")
    ax2.set_ylabel("Tiempo (ms) — Escala Log")
    ax2.set_title("LCS (Subcadena Común)")
    ax2.legend()

    fig.suptitle("Procesamiento de Cadenas: Costo Exponencial vs. Programación Dinámica", fontsize=14)
    salida = os.path.join(DIR_GRAFICAS, "03_cadenas_tiempo_comparativa.png")
    fig.savefig(salida)
    plt.close(fig)
    print(f" -> Guardada: {salida}")


def graficar_escalabilidad(data_mochila: list, data_cambio: list) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    # Subplot 1: Mochila Escalabilidad
    n_vals = [d["n"] for d in data_mochila]
    t_mem1 = [d["memo"]["tiempo_ms"] for d in data_mochila]
    t_tab1 = [d["tabulacion"]["tiempo_ms"] for d in data_mochila]

    ax1.plot(n_vals, t_mem1, marker="s", color="#ff7f0e", linewidth=2.0, label="Memoización (Top-down)")
    ax1.plot(n_vals, t_tab1, marker="^", color="#2ca02c", linewidth=2.0, label="Tabulación (Bottom-up)")
    ax1.set_xlabel("Número de elementos ($n$)")
    ax1.set_ylabel("Tiempo de ejecución (ms)")
    ax1.set_title("Mochila 0/1: Escalabilidad a Gran Escala")
    ax1.legend()

    # Subplot 2: Cambio Escalabilidad
    m_vals = [d["monto"] for d in data_cambio]
    t_mem2 = [d["memo"]["tiempo_ms"] for d in data_cambio]
    t_tab2 = [d["tabulacion"]["tiempo_ms"] for d in data_cambio]

    ax2.plot(m_vals, t_mem2, marker="s", color="#1f77b4", linewidth=2.0, label="Memoización (Top-down)")
    ax2.plot(m_vals, t_tab2, marker="^", color="#2ca02c", linewidth=2.0, label="Tabulación (Bottom-up)")
    ax2.set_xlabel("Monto objetivo ($V$)")
    ax2.set_ylabel("Tiempo de ejecución (ms)")
    ax2.set_title("Cambio de Monedas: Escalabilidad a Gran Escala")
    ax2.legend()

    fig.suptitle("Comparativa de Eficiencia: Memoización vs. Tabulación", fontsize=14)
    salida = os.path.join(DIR_GRAFICAS, "04_escalabilidad_memo_vs_tabulacion.png")
    fig.savefig(salida)
    plt.close(fig)
    print(f" -> Guardada: {salida}")


def graficar_memoria(data_mochila: list) -> None:
    n_vals = [d["n"] for d in data_mochila]
    mem_mem = [d["memo"]["memoria_kib"] / 1024.0 for d in data_mochila]  # MiB
    mem_tab = [d["tabulacion"]["memoria_kib"] / 1024.0 for d in data_mochila]  # MiB

    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    x = np.arange(len(n_vals))
    width = 0.35

    rects1 = ax.bar(x - width/2, mem_mem, width, label="Memoización (Hash Map en Heap)", color="#ff7f0e", alpha=0.85)
    rects2 = ax.bar(x + width/2, mem_tab, width, label="Tabulación (Matriz Densa)", color="#2ca02c", alpha=0.85)

    ax.set_xlabel("Número de elementos ($n$)")
    ax.set_ylabel("Memoria Pico (MiB)")
    ax.set_title("Mochila 0/1: Huella de Memoria (Memoización vs. Tabulación)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"n={n}" for n in n_vals])
    ax.legend()

    # Etiquetas de valor sobre barras
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}", xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"{h:.1f}", xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=8)

    salida = os.path.join(DIR_GRAFICAS, "05_consumo_memoria_comparativa.png")
    fig.savefig(salida)
    plt.close(fig)
    print(f" -> Guardada: {salida}")


def graficar_optimalidad_voraz(data_opt: list) -> None:
    nombres = [d["nombre"].replace("no_canonico_", "") for d in data_opt]
    dp_vals = [d["dp_optimo"] for d in data_opt]
    vor_vals = [d["voraz_monedas_total"] for d in data_opt]

    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
    x = np.arange(len(nombres))
    width = 0.32

    r1 = ax.bar(x - width/2, dp_vals, width, label="Programación Dinámica (Óptimo Global)", color="#2ca02c", alpha=0.9)
    r2 = ax.bar(x + width/2, vor_vals, width, label="Heurística Voraz (Subóptimo)", color="#d62728", alpha=0.9)

    ax.set_ylabel("Número de monedas requeridas")
    ax.set_title("Demostración Cuantitativa: Suboptimalidad Voraz vs. Optimalidad DP")
    ax.set_xticks(x)
    ax.set_xticklabels(nombres)
    ax.legend()

    for i, d in enumerate(data_opt):
        # Anotar detalle de monedas
        ax.text(i - width/2, dp_vals[i] + 0.15, f"{dp_vals[i]} m.\n{d['dp_monedas']}", ha="center", va="bottom", fontsize=8, color="#1b5e20", fontweight="bold")
        ax.text(i + width/2, vor_vals[i] + 0.15, f"{vor_vals[i]} m.\n{d['voraz_monedas'][:3]}...", ha="center", va="bottom", fontsize=8, color="#b71c1c", fontweight="bold")

    ax.set_ylim(0, max(vor_vals) + 2)
    salida = os.path.join(DIR_GRAFICAS, "06_cambio_optimalidad_dp_vs_voraz.png")
    fig.savefig(salida)
    plt.close(fig)
    print(f" -> Guardada: {salida}")


def main() -> None:
    os.makedirs(DIR_GRAFICAS, exist_ok=True)
    configurar_estilo()

    ruta_json = os.path.join(DIR_RESULTADOS, "resultados.json")
    with open(ruta_json, "r", encoding="utf-8") as f:
        res = json.load(f)

    print("Generando gráficas comparativas...")
    graficar_mochila_pequena(res["mochila_pequena"])
    graficar_cambio_pequeno(res["cambio_pequeno"])
    graficar_cadenas_pequenas(res["lcsq_pequeno"], res["subcadena_pequena"])
    graficar_escalabilidad(res["mochila_escalabilidad"], res["cambio_escalabilidad"])
    graficar_memoria(res["mochila_escalabilidad"])
    graficar_optimalidad_voraz(res["cambio_optimalidad"])
    print(f"[OK] 6 gráficas generadas exitosamente en: {DIR_GRAFICAS}")


if __name__ == "__main__":
    main()
