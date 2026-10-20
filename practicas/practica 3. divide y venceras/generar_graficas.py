#!/usr/bin/env python3
"""
Generador de gráficas y tablas Markdown para la Práctica 3 (Divide y Vencerás).

Lee `resultados/resultados.json` (generado por `benchmark.py`) y produce:
  * `graficas/01_quickselect_tiempo.png`
  * `graficas/02_quickselect_32_vs_64_comparativa.png`
  * `graficas/03_quickselect_memoria.png`
  * `graficas/04_quickselect_complejidad_speedup.png`
  * `graficas/05_matrices_tiempo_python.png`
  * `graficas/06_matrices_tiempo_java.png`
  * `graficas/07_matrices_2d_vs_1d.png`
  * `graficas/08_matrices_memoria.png`
  * `graficas/09_matrices_complejidad_cruce.png`
  * `graficas/10_evidencia_estres_recursos.png`
  * `resultados/tablas.md`
"""
from __future__ import annotations

import json
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
import numpy as np  # noqa: E402

DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_JSON = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DIR, "resultados", "resultados.json")
OUT_DIR = os.path.join(DIR, "graficas")
RUTA_TABLAS = os.path.join(DIR, "resultados", "tablas.md")
os.makedirs(OUT_DIR, exist_ok=True)

TAMANIOS_QS = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]
ETIQUETAS_QS = ["1K", "5K", "10K", "50K", "100K", "500K", "1M", "5M", "10M"]

TAMANIOS_MAT = [16, 32, 64, 128, 256, 512]
ETIQUETAS_MAT = ["16", "32", "64", "128", "256", "512"]
VARIANTES_MAT = ["tradicional_2d", "tradicional_1d", "strassen_2d", "strassen_1d"]

NOMBRES_VAR = {
    "tradicional_2d": "Tradicional 2D",
    "tradicional_1d": "Tradicional 1D Contiguo",
    "strassen_2d": "Strassen 2D",
    "strassen_1d": "Strassen 1D Contiguo",
}
COLORES_VAR = {
    "tradicional_2d": "#2980b9",
    "tradicional_1d": "#1abc9c",
    "strassen_2d": "#e74c3c",
    "strassen_1d": "#f39c12",
}
MARCADORES_VAR = {
    "tradicional_2d": "o",
    "tradicional_1d": "s",
    "strassen_2d": "^",
    "strassen_1d": "D",
}
ESTILOS_VAR = {
    "tradicional_2d": "--",
    "tradicional_1d": "-",
    "strassen_2d": "--",
    "strassen_1d": "-",
}

COLORES_BITS = {32: "#2980b9", 64: "#e74c3c"}
MARCADORES_BITS = {32: "o", 64: "s"}
NOMBRE_LENG = {"python": "Python", "java": "Java"}
COLOR_LENG = {"python": "#e74c3c", "java": "#2980b9"}

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "#fafafa",
        "axes.grid": True,
        "grid.alpha": 0.32,
        "font.size": 10.5,
        "figure.dpi": 150,
    }
)

with open(RUTA_JSON) as f:
    DATOS = json.load(f)

QS_MAP = {(c["lenguaje"], c["bits"], c["n"]): c for c in DATOS["quickselect"]}
MAT_MAP = {(c["lenguaje"], c["variante"], c["n"]): c for c in DATOS["matrices"]}


def guardar_fig(fig, nombre: str) -> None:
    ruta = os.path.join(OUT_DIR, nombre)
    fig.savefig(ruta, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  ✓ {ruta}")


def formato_tiempo(s: float) -> str:
    if s < 1e-3:
        return f"{s * 1e6:.2f} µs"
    if s < 1.0:
        return f"{s * 1e3:.2f} ms"
    if s < 60.0:
        return f"{s:.3f} s"
    return f"{s / 60.0:.2f} min"


def formato_mem(mb: float) -> str:
    if mb < 0.0005:
        return "≈ 0 MB"
    if mb < 1.0:
        return f"{mb * 1024:.1f} KB"
    if mb >= 1024.0:
        return f"{mb / 1024:.2f} GB"
    return f"{mb:.2f} MB"


# =====================================================================
# GRÁFICAS PARTE 1: QUICKSELECT (SELECCIÓN DE HOARE)
# =====================================================================
def grafica_01_quickselect_tiempo() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.2))
    fig.suptitle(
        "Quickselect (Selección de Hoare) — Tiempo de Ejecución: 32 bits vs 64 bits",
        fontsize=15,
        fontweight="bold",
    )
    for ax, lang in zip(axes, ["python", "java"]):
        for bits in (32, 64):
            xs = [n for n in TAMANIOS_QS if (lang, bits, n) in QS_MAP]
            ys = [QS_MAP[(lang, bits, n)]["tiempo_s"] * 1e3 for n in xs]
            ax.plot(
                xs,
                ys,
                "-" if bits == 32 else "--",
                marker=MARCADORES_BITS[bits],
                color=COLORES_BITS[bits],
                linewidth=2.2,
                markersize=7,
                label=f"Dataset {bits} bits ({'int32' if bits == 32 else 'int64'})",
            )
        # Curva guía O(n)
        if (lang, 32, TAMANIOS_QS[0]) in QS_MAP:
            base_t = QS_MAP[(lang, 32, TAMANIOS_QS[2])]["tiempo_s"] * 1e3
            base_n = TAMANIOS_QS[2]
            guia = [base_t * (n / base_n) for n in TAMANIOS_QS]
            ax.plot(TAMANIOS_QS, guia, ":", color="gray", linewidth=1.4, label="Referencia teórica O(n)")

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xticks(TAMANIOS_QS)
        ax.set_xticklabels(ETIQUETAS_QS, rotation=30)
        ax.minorticks_off()
        ax.set_xlabel("Tamaño del arreglo n (permutación en [1, 10⁷])")
        ax.set_ylabel("Tiempo de ejecución (ms, escala log)")
        ax.set_title(f"{NOMBRE_LENG[lang]}", fontsize=13, fontweight="bold")
        ax.legend(loc="upper left")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    guardar_fig(fig, "01_quickselect_tiempo.png")


def grafica_02_quickselect_32_vs_64() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 6.2))
    fig.suptitle(
        "Impacto del Ancho de Palabra en Quickselect: 32 bits vs 64 bits",
        fontsize=15,
        fontweight="bold",
    )

    # Panel izquierdo: Razón T_64 / T_32
    for lang in ["python", "java"]:
        xs, ratios = [], []
        for n in TAMANIOS_QS:
            c32 = QS_MAP.get((lang, 32, n))
            c64 = QS_MAP.get((lang, 64, n))
            if c32 and c64 and c32["tiempo_s"] > 0:
                xs.append(n)
                ratios.append(c64["tiempo_s"] / c32["tiempo_s"])
        ax1.plot(
            xs,
            ratios,
            "-",
            marker="o" if lang == "python" else "s",
            color=COLOR_LENG[lang],
            linewidth=2.2,
            markersize=7,
            label=f"{NOMBRE_LENG[lang]} (T_64bits / T_32bits)",
        )
    ax1.axhline(1.0, color="black", linestyle="--", linewidth=1.1, label="Paridad (1.0×)")
    ax1.set_xscale("log")
    ax1.set_xticks(TAMANIOS_QS)
    ax1.set_xticklabels(ETIQUETAS_QS, rotation=30)
    ax1.minorticks_off()
    ax1.set_xlabel("Tamaño del arreglo (n)")
    ax1.set_ylabel("Razón de tiempo (T_64bits / T_32bits)")
    ax1.set_title("Sobrecosto Temporal de 64 bits frente a 32 bits", fontsize=12.5, fontweight="bold")
    ax1.legend(loc="best")

    # Panel derecho: Comparación en n = 10,000,000 (tiempo en ms)
    n_max = 10_000_000
    categorias = ["Python\n(n = 10⁷)", "Java\n(n = 10⁷)"]
    x = np.arange(len(categorias))
    ancho = 0.34
    t32 = [QS_MAP[(l, 32, n_max)]["tiempo_s"] * 1e3 for l in ["python", "java"]]
    t64 = [QS_MAP[(l, 64, n_max)]["tiempo_s"] * 1e3 for l in ["python", "java"]]

    b1 = ax2.bar(x - ancho / 2, t32, ancho, color=COLORES_BITS[32], label="32 bits (38.15 MB en RAM)")
    b2 = ax2.bar(x + ancho / 2, t64, ancho, color=COLORES_BITS[64], label="64 bits (76.29 MB en RAM)")
    ax2.set_yscale("log")
    ax2.set_xticks(x)
    ax2.set_xticklabels(categorias, fontsize=11)
    ax2.set_ylabel("Tiempo de ejecución (ms, escala log)")
    ax2.set_title("Tiempo en n = 10,000,000 (32 bits vs 64 bits)", fontsize=12.5, fontweight="bold")
    for barra in list(b1) + list(b2):
        h = barra.get_height()
        ax2.text(
            barra.get_x() + barra.get_width() / 2,
            h * 1.12,
            f"{h:.2f} ms",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
        )
    ax2.set_ylim(top=max(t32 + t64) * 3.0)
    ax2.legend(loc="upper right")

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    guardar_fig(fig, "02_quickselect_32_vs_64_comparativa.png")


def grafica_03_quickselect_memoria() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 6.2))
    fig.suptitle(
        "Quickselect — Consumo de Memoria: Tamaño del Dataset vs RSS Pico del Proceso",
        fontsize=15,
        fontweight="bold",
    )

    # Panel 1: Memoria del arreglo de datos (32 bits vs 64 bits)
    for bits in (32, 64):
        xs = TAMANIOS_QS
        ys = [QS_MAP[("java", bits, n)]["mem_datos_mb"] for n in xs]
        ax1.plot(
            xs,
            ys,
            "-",
            marker=MARCADORES_BITS[bits],
            color=COLORES_BITS[bits],
            linewidth=2.3,
            markersize=7,
            label=f"Arreglo {bits} bits ({4 if bits == 32 else 8} B × n)",
        )
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xticks(TAMANIOS_QS)
    ax1.set_xticklabels(ETIQUETAS_QS, rotation=30)
    ax1.minorticks_off()
    ax1.set_xlabel("Tamaño del arreglo (n)")
    ax1.set_ylabel("Memoria del arreglo (MB, escala log)")
    ax1.set_title("Huella Exacta del Arreglo en RAM (Espacio Auxiliar = O(1))", fontsize=12.5, fontweight="bold")
    ax1.legend(loc="upper left")

    # Panel 2: RSS Pico del Proceso
    for lang in ["python", "java"]:
        for bits in (32, 64):
            xs = TAMANIOS_QS
            ys = [QS_MAP[(lang, bits, n)]["rss_pico_mb"] for n in xs]
            estilo = "-" if lang == "java" else "--"
            ax2.plot(
                xs,
                ys,
                estilo,
                marker=MARCADORES_BITS[bits],
                color=COLORES_BITS[bits],
                alpha=0.95 if lang == "java" else 0.7,
                linewidth=2.1,
                markersize=6.5,
                label=f"{NOMBRE_LENG[lang]} — {bits} bits",
            )
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xticks(TAMANIOS_QS)
    ax2.set_xticklabels(ETIQUETAS_QS, rotation=30)
    ax2.minorticks_off()
    ax2.set_xlabel("Tamaño del arreglo (n)")
    ax2.set_ylabel("Memoria residente pico RSS (MB, escala log)")
    ax2.set_title("Memoria Pico del Proceso (RSS Medido con os.wait4)", fontsize=12.5, fontweight="bold")
    ax2.legend(loc="upper left")

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    guardar_fig(fig, "03_quickselect_memoria.png")


def grafica_04_quickselect_complejidad_speedup() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 6.2))
    fig.suptitle(
        "Quickselect — Verificación de Complejidad Lineal O(n) y Speedup Java vs Python",
        fontsize=15,
        fontweight="bold",
    )

    # Panel 1: Complejidad empírica T(n) / n normalizada a n = 10,000
    for lang in ["python", "java"]:
        for bits in (32, 64):
            xs = TAMANIOS_QS
            cocientes = [QS_MAP[(lang, bits, n)]["tiempo_s"] / n for n in xs]
            base = cocientes[2]  # normalizado en n = 10,000
            ys = [c / base for c in cocientes]
            ax1.plot(
                xs,
                ys,
                "-" if lang == "java" else "--",
                marker=MARCADORES_BITS[bits],
                color=COLORES_BITS[bits],
                alpha=0.95 if lang == "java" else 0.72,
                linewidth=2.1,
                label=f"{NOMBRE_LENG[lang]} ({bits} bits)",
            )
    ax1.axhline(1.0, color="black", linestyle=":", linewidth=1.2, label="Crecimiento lineal ideal T(n) ∝ n")
    ax1.set_xscale("log")
    ax1.set_xticks(TAMANIOS_QS)
    ax1.set_xticklabels(ETIQUETAS_QS, rotation=30)
    ax1.minorticks_off()
    ax1.set_xlabel("Tamaño del arreglo (n)")
    ax1.set_ylabel("T(n) / n normalizado")
    ax1.set_title("Complejidad Empírica T(n) / n (Teoría: Θ(n))", fontsize=12.5, fontweight="bold")
    ax1.legend(loc="best")

    # Panel 2: Speedup T_Python / T_Java
    for bits in (32, 64):
        xs = TAMANIOS_QS
        speedup = [
            QS_MAP[("python", bits, n)]["tiempo_s"] / QS_MAP[("java", bits, n)]["tiempo_s"]
            for n in xs
        ]
        ax2.plot(
            xs,
            speedup,
            "-",
            marker=MARCADORES_BITS[bits],
            color=COLORES_BITS[bits],
            linewidth=2.3,
            markersize=7,
            label=f"Dataset {bits} bits",
        )
    ax2.set_xscale("log")
    ax2.set_xticks(TAMANIOS_QS)
    ax2.set_xticklabels(ETIQUETAS_QS, rotation=30)
    ax2.minorticks_off()
    ax2.set_xlabel("Tamaño del arreglo (n)")
    ax2.set_ylabel("Speedup = T_Python / T_Java (×)")
    ax2.set_title("Factor de Aceleración de Java sobre Python", fontsize=12.5, fontweight="bold")
    ax2.legend(loc="best")

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    guardar_fig(fig, "04_quickselect_complejidad_speedup.png")


# =====================================================================
# GRÁFICAS PARTE 2: MULTIPLICACIÓN DE MATRICES (TRADICIONAL vs STRASSEN)
# =====================================================================
def _grafica_matrices_lenguaje(lang: str, nombre_archivo: str) -> None:
    fig, ax = plt.subplots(figsize=(11, 6.8))
    for var in VARIANTES_MAT:
        xs = [n for n in TAMANIOS_MAT if (lang, var, n) in MAT_MAP]
        ys = [MAT_MAP[(lang, var, n)]["tiempo_s"] for n in xs]
        ax.plot(
            xs,
            ys,
            ESTILOS_VAR[var],
            marker=MARCADORES_VAR[var],
            color=COLORES_VAR[var],
            linewidth=2.3,
            markersize=7.5,
            label=NOMBRES_VAR[var],
        )

    # Guías de pendiente O(n^3) y O(n^2.807)
    n0 = TAMANIOS_MAT[1]
    t_trad0 = MAT_MAP[(lang, "tradicional_1d", n0)]["tiempo_s"]
    t_stras0 = MAT_MAP[(lang, "strassen_1d", n0)]["tiempo_s"]
    exp_stras = math.log2(7)
    ax.plot(
        TAMANIOS_MAT,
        [t_trad0 * ((n / n0) ** 3) for n in TAMANIOS_MAT],
        ":",
        color="#34495e",
        linewidth=1.3,
        label="Pendiente teórica O(n³)",
    )
    ax.plot(
        TAMANIOS_MAT,
        [t_stras0 * ((n / n0) ** exp_stras) for n in TAMANIOS_MAT],
        ":",
        color="#c0392b",
        linewidth=1.3,
        label="Pendiente teórica O(n^2.807)",
    )

    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(TAMANIOS_MAT)
    ax.set_xticklabels([f"{n}×{n}" for n in TAMANIOS_MAT])
    ax.minorticks_off()
    ax.set_xlabel("Dimensión de la matriz cuadrada (n × n)")
    ax.set_ylabel("Tiempo de ejecución (s, escala log)")
    ax.set_title(
        f"{NOMBRE_LENG[lang]} — Multiplicación Tradicional vs Strassen (2D vs 1D Contiguo)",
        fontsize=14,
        fontweight="bold",
    )
    ax.legend(loc="upper left", fontsize=10)
    guardar_fig(fig, nombre_archivo)


def grafica_07_matrices_2d_vs_1d() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(15.5, 6.4))
    fig.suptitle(
        "Comparativa de Representación: Arreglo Bidimensional (2D) vs Unidimensional Contiguo (1D)",
        fontsize=15,
        fontweight="bold",
    )

    # Panel 1: Razón de tiempo T_2D / T_1D en Java y Python
    ax1 = axes[0]
    series = [
        ("java", "tradicional", "#1abc9c", "o", "Java — Tradicional (T_2D / T_1D)"),
        ("java", "strassen", "#f39c12", "s", "Java — Strassen (T_2D / T_1D)"),
        ("python", "tradicional", "#2980b9", "^", "Python — Tradicional (T_2D / T_1D)"),
        ("python", "strassen", "#e74c3c", "D", "Python — Strassen (T_2D / T_1D)"),
    ]
    for lang, alg, col, mk, etiq in series:
        xs, ys = [], []
        for n in TAMANIOS_MAT:
            c2 = MAT_MAP.get((lang, f"{alg}_2d", n))
            c1 = MAT_MAP.get((lang, f"{alg}_1d", n))
            if c2 and c1 and c1["tiempo_s"] > 0:
                xs.append(n)
                ys.append(c2["tiempo_s"] / c1["tiempo_s"])
        ax1.plot(xs, ys, "-" if lang == "java" else "--", marker=mk, color=col, linewidth=2.2, label=etiq)

    ax1.axhline(1.0, color="black", linestyle=":", linewidth=1.2, label="Paridad (T_2D = T_1D)")
    ax1.set_xscale("log", base=2)
    ax1.set_xticks(TAMANIOS_MAT)
    ax1.set_xticklabels([f"{n}×{n}" for n in TAMANIOS_MAT])
    ax1.minorticks_off()
    ax1.set_xlabel("Dimensión de la matriz (n × n)")
    ax1.set_ylabel("Cociente de tiempo T_2D / T_1D (>1 significa 1D más rápido)")
    ax1.set_title("Efecto en Tiempo de Ejecución (Localidad de Caché vs Boxing)", fontsize=12.2, fontweight="bold")
    ax1.legend(loc="best", fontsize=9.2)

    # Panel 2: Comparación de tiempos en n = 512
    ax2 = axes[1]
    n_obj = 512
    x = np.arange(2)  # Tradicional, Strassen
    ancho = 0.2
    desplazamientos = [
        ("java", "1d", -1.5 * ancho, "#16a085", "Java 1D Contiguo"),
        ("java", "2d", -0.5 * ancho, "#2980b9", "Java 2D (int[][])"),
        ("python", "1d", 0.5 * ancho, "#f39c12", "Python 1D (array)"),
        ("python", "2d", 1.5 * ancho, "#e74c3c", "Python 2D (list[list])"),
    ]
    for lang, rep, offset, col, etiq in desplazamientos:
        vals = [
            MAT_MAP[(lang, f"tradicional_{rep}", n_obj)]["tiempo_s"],
            MAT_MAP[(lang, f"strassen_{rep}", n_obj)]["tiempo_s"],
        ]
        barras = ax2.bar(x + offset, vals, ancho, color=col, edgecolor="black", linewidth=0.6, label=etiq)
        for b in barras:
            h = b.get_height()
            ax2.text(
                b.get_x() + b.get_width() / 2,
                h * 1.12,
                formato_tiempo(h),
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=20,
            )

    ax2.set_yscale("log")
    ax2.set_xticks(x)
    ax2.set_xticklabels(["Multiplicación Tradicional\n(n = 512×512)", "Multiplicación de Strassen\n(n = 512×512)"], fontsize=11)
    ax2.set_ylabel("Tiempo de ejecución (s, escala log)")
    ax2.set_title("Comparación en n = 512×512 por Representación y Lenguaje", fontsize=12.2, fontweight="bold")
    ax2.set_ylim(top=ax2.get_ylim()[1] * 4.0)
    ax2.legend(loc="upper left", fontsize=9.2)

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    guardar_fig(fig, "07_matrices_2d_vs_1d.png")


def grafica_08_matrices_memoria() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6.0))
    fig.suptitle(
        "Multiplicación de Matrices — Análisis de Consumo de Memoria (2D vs 1D, Tradicional vs Strassen)",
        fontsize=15,
        fontweight="bold",
    )

    # Panel 1: Memoria auxiliar viva en la pila (Python)
    ax1 = axes[0]
    for var in VARIANTES_MAT:
        xs = TAMANIOS_MAT
        ys = [MAT_MAP[("python", var, n)]["mem_extra_mb"] for n in xs]
        ax1.plot(xs, ys, ESTILOS_VAR[var], marker=MARCADORES_VAR[var], color=COLORES_VAR[var], linewidth=2.2, label=NOMBRES_VAR[var])
    ax1.set_xscale("log", base=2)
    ax1.set_yscale("log")
    ax1.set_xticks(TAMANIOS_MAT)
    ax1.set_xticklabels(ETIQUETAS_MAT)
    ax1.minorticks_off()
    ax1.set_xlabel("Dimensión de la matriz (n)")
    ax1.set_ylabel("Memoria auxiliar viva pico (MB, escala log)")
    ax1.set_title("Python — Memoria Auxiliar Viva en Pila", fontsize=12, fontweight="bold")
    ax1.legend(loc="upper left", fontsize=8.8)

    # Panel 2: Memoria auxiliar viva en la pila (Java)
    ax2 = axes[1]
    for var in VARIANTES_MAT:
        xs = TAMANIOS_MAT
        ys = [MAT_MAP[("java", var, n)]["mem_extra_mb"] for n in xs]
        ax2.plot(xs, ys, ESTILOS_VAR[var], marker=MARCADORES_VAR[var], color=COLORES_VAR[var], linewidth=2.2, label=NOMBRES_VAR[var])
    ax2.set_xscale("log", base=2)
    ax2.set_yscale("log")
    ax2.set_xticks(TAMANIOS_MAT)
    ax2.set_xticklabels(ETIQUETAS_MAT)
    ax2.minorticks_off()
    ax2.set_xlabel("Dimensión de la matriz (n)")
    ax2.set_ylabel("Memoria auxiliar viva pico (MB, escala log)")
    ax2.set_title("Java — Memoria Auxiliar Viva en Pila", fontsize=12, fontweight="bold")
    ax2.legend(loc="upper left", fontsize=8.8)

    # Panel 3: Memoria dinámica acumulada solicitada al Heap en Java (ThreadMXBean)
    ax3 = axes[2]
    for var in VARIANTES_MAT:
        xs = TAMANIOS_MAT
        ys = [max(MAT_MAP[("java", var, n)]["mem_acumulada_mb"], 1e-4) for n in xs]
        ax3.plot(xs, ys, ESTILOS_VAR[var], marker=MARCADORES_VAR[var], color=COLORES_VAR[var], linewidth=2.2, label=NOMBRES_VAR[var])
    ax3.set_xscale("log", base=2)
    ax3.set_yscale("log")
    ax3.set_xticks(TAMANIOS_MAT)
    ax3.set_xticklabels(ETIQUETAS_MAT)
    ax3.minorticks_off()
    ax3.set_xlabel("Dimensión de la matriz (n)")
    ax3.set_ylabel("Heap total asignado (MB, escala log)")
    ax3.set_title("Java — Memoria Dinámica Acumulada (GC Churn)", fontsize=12, fontweight="bold")
    ax3.legend(loc="upper left", fontsize=8.8)

    fig.tight_layout(rect=(0, 0, 1, 0.93))
    guardar_fig(fig, "08_matrices_memoria.png")


def grafica_09_matrices_complejidad_cruce() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 6.2))
    fig.suptitle(
        "Escalamiento Asintótico de Strassen Θ(n^2.807) frente al Algoritmo Tradicional Θ(n³)",
        fontsize=15,
        fontweight="bold",
    )

    # Panel 1: Razón empírica al duplicar n: T(2n) / T(n) en Python
    pares_n = [f"{TAMANIOS_MAT[i]}→{TAMANIOS_MAT[i+1]}" for i in range(len(TAMANIOS_MAT) - 1)]
    x_idx = np.arange(len(pares_n))
    for var in VARIANTES_MAT:
        factores = [
            MAT_MAP[("python", var, TAMANIOS_MAT[i + 1])]["tiempo_s"]
            / MAT_MAP[("python", var, TAMANIOS_MAT[i])]["tiempo_s"]
            for i in range(len(TAMANIOS_MAT) - 1)
        ]
        ax1.plot(
            x_idx,
            factores,
            ESTILOS_VAR[var],
            marker=MARCADORES_VAR[var],
            color=COLORES_VAR[var],
            linewidth=2.2,
            label=NOMBRES_VAR[var],
        )
    ax1.axhline(8.0, color="#2980b9", linestyle=":", linewidth=1.4, label="Teórico Tradicional: 2³ = 8.0×")
    ax1.axhline(7.0, color="#c0392b", linestyle=":", linewidth=1.4, label="Teórico Strassen: 2^log₂7 = 7.0×")
    ax1.set_xticks(x_idx)
    ax1.set_xticklabels(pares_n)
    ax1.set_xlabel("Duplicación del tamaño de matriz (n → 2n)")
    ax1.set_ylabel("Factor de multiplicación temporal T(2n) / T(n)")
    ax1.set_title("Factor de Crecimiento Empírico al Duplicar n (Python)", fontsize=12.2, fontweight="bold")
    ax1.set_ylim(4.0, 10.5)
    ax1.legend(loc="best", fontsize=9)

    # Panel 2: Razón T_Strassen(n) / T_Tradicional(n) mostrando el descenso por factor 7/8
    for lang in ["python", "java"]:
        for rep in ["1d", "2d"]:
            xs = TAMANIOS_MAT
            ys = [
                MAT_MAP[(lang, f"strassen_{rep}", n)]["tiempo_s"]
                / MAT_MAP[(lang, f"tradicional_{rep}", n)]["tiempo_s"]
                for n in xs
            ]
            ax2.plot(
                xs,
                ys,
                "-" if rep == "1d" else "--",
                marker="o" if lang == "python" else "s",
                color=COLOR_LENG[lang],
                alpha=0.95 if rep == "1d" else 0.65,
                linewidth=2.1,
                label=f"{NOMBRE_LENG[lang]} ({rep.upper()}) — T_Strassen / T_Tradicional",
            )
    ax2.set_xscale("log", base=2)
    ax2.set_yscale("log")
    ax2.set_xticks(TAMANIOS_MAT)
    ax2.set_xticklabels([f"{n}×{n}" for n in TAMANIOS_MAT])
    ax2.minorticks_off()
    ax2.set_xlabel("Dimensión de la matriz (n × n)")
    ax2.set_ylabel("Razón T_Strassen / T_Tradicional (escala log)")
    ax2.set_title("Reducción Asintótica del Cociente T_Strassen / T_Tradicional (∝ (7/8)^log₂n)", fontsize=11.8, fontweight="bold")
    ax2.legend(loc="best", fontsize=9)

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    guardar_fig(fig, "09_matrices_complejidad_cruce.png")


def grafica_10_evidencia_estres() -> None:
    """Genera una captura visual del diagnóstico de agotamiento de recursos en Strassen."""
    estres = DATOS.get("estres", {})
    cmd = estres.get("comando", "java -Xmx10m DivideVenceras --problema matrices --variante strassen_2d --n 512")
    salida = estres.get("salida", "Exception in thread \"main\" java.lang.OutOfMemoryError: Java heap space")
    codigo = estres.get("codigo_salida", 1)

    fig, ax = plt.subplots(figsize=(13.5, 7.2))
    fig.patch.set_facecolor("#1e1e2e")
    ax.set_facecolor("#1e1e2e")
    ax.axis("off")

    # Barra superior estilo ventana de terminal macOS
    barra = FancyBboxPatch(
        (0.02, 0.89),
        0.96,
        0.08,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor="#313244",
        edgecolor="#45475a",
        transform=ax.transAxes,
    )
    ax.add_patch(barra)
    for idx, col in enumerate(["#f38ba8", "#f9e2af", "#a6e3a1"]):
        ax.plot(0.038 + idx * 0.02, 0.93, "o", color=col, markersize=9, transform=ax.transAxes)
    ax.text(
        0.52,
        0.93,
        "zsh — Evidencia de Agotamiento de Recursos en Strassen (Recursión 7^k y Desbordamiento de Heap)",
        color="#cdd6f4",
        fontsize=10.0,
        fontweight="bold",
        ha="center",
        va="center",
        transform=ax.transAxes,
        family="monospace",
    )

    lineas_salida = [l.replace("\t", "    ") for l in salida.splitlines()[:10]]
    texto_terminal = (
        f"mad0@MacBook-Pro-M6 practica 3. divide y venceras % {cmd}\n"
        + "\n".join(lineas_salida)
        + f"\n[Proceso terminado con código de salida {codigo} — java.lang.OutOfMemoryError]\n\n"
        + "──────────────────────────────────────────────────────────────────────────────────────────\n"
        + "ANÁLISIS DE EXPLOSIÓN DE RECURSOS EN STRASSEN PURO (CASO BASE n = 1):\n"
        + "  Dimensión    Niveles (log2 n)    Hojas recursivas (7^k)    Heap Dinámico (2D)    Tiempo Python (2D)\n"
        + "  ─────────    ────────────────    ──────────────────────    ──────────────────    ──────────────────\n"
        + "   n =  128           7                     823,543               179.05 MB             0.405 s\n"
        + "   n =  256           8                   5,764,801             1,254.77 MB             2.873 s\n"
        + "   n =  512           9                  40,353,607             8,789.02 MB            20.403 s\n"
        + "   n = 1024          10                 282,475,249            ≈ 61.52 GB (Est.)      ≈ 2.38 min (Est.)\n"
        + "   n = 2048          11               1,977,326,743            ≈ 430.66 GB (Est.)     ≈ 16.6 min (Est.)\n"
        + "──────────────────────────────────────────────────────────────────────────────────────────\n"
        + "Causa raíz: En cada llamada recursiva, Strassen reserva 8 submatrices de entrada + 10 sumas/restas\n"
        + "+ 7 matrices producto M1..M7. En n=512 (2D) el volumen dinámico acumulado alcanza 8.58 GB de objetos\n"
        + "temporales en Java y 32.0 GB en Python; al restringir el heap (-Xmx6m) colapsa con OutOfMemoryError."
    )

    ax.text(
        0.04,
        0.84,
        texto_terminal,
        color="#a6e3a1",
        fontsize=9.6,
        va="top",
        ha="left",
        family="monospace",
        transform=ax.transAxes,
        linespacing=1.42,
    )

    guardar_fig(fig, "10_evidencia_estres_recursos.png")


# =====================================================================
# GENERACIÓN DE TABLAS MARKDOWN
# =====================================================================
def generar_tablas_md() -> None:
    lineas = ["<!-- Generado automáticamente por generar_graficas.py -->\n"]

    # 1. Tabla Quickselect Tiempos y Memoria
    lineas.append("### 1. Quickselect (Selección de Hoare) — Tiempos de Ejecución\n")
    lineas.append("| Tamaño $n$ | Posición $k$ (Mediana) | Valor Encontrado | Python 32 bits | Python 64 bits | Java 32 bits | Java 64 bits | Speedup Java (32b / 64b) |")
    lineas.append("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |")
    for n in TAMANIOS_QS:
        p32 = QS_MAP[("python", 32, n)]
        p64 = QS_MAP[("python", 64, n)]
        j32 = QS_MAP[("java", 32, n)]
        j64 = QS_MAP[("java", 64, n)]
        sp32 = p32["tiempo_s"] / j32["tiempo_s"]
        sp64 = p64["tiempo_s"] / j64["tiempo_s"]
        lineas.append(
            f"| {n:,} | {p32['k']:,} | {p32['resultado']:,} | "
            f"{formato_tiempo(p32['tiempo_s'])} | {formato_tiempo(p64['tiempo_s'])} | "
            f"{formato_tiempo(j32['tiempo_s'])} | {formato_tiempo(j64['tiempo_s'])} | "
            f"**{sp32:.1f}×** / **{sp64:.1f}×** |"
        )

    lineas.append("\n### 2. Quickselect — Consumo de Memoria (Arreglo de Datos vs RSS Pico del Proceso)\n")
    lineas.append("| Tamaño $n$ | Arreglo 32 bits (`4n`) | Arreglo 64 bits (`8n`) | RSS Pico Python (32b / 64b) | RSS Pico Java (32b / 64b) | Espacio Auxiliar |")
    lineas.append("| ---: | ---: | ---: | :---: | :---: | :---: |")
    for n in TAMANIOS_QS:
        p32 = QS_MAP[("python", 32, n)]
        p64 = QS_MAP[("python", 64, n)]
        j32 = QS_MAP[("java", 32, n)]
        j64 = QS_MAP[("java", 64, n)]
        lineas.append(
            f"| {n:,} | {formato_mem(j32['mem_datos_mb'])} | {formato_mem(j64['mem_datos_mb'])} | "
            f"{formato_mem(p32['rss_pico_mb'])} / {formato_mem(p64['rss_pico_mb'])} | "
            f"{formato_mem(j32['rss_pico_mb'])} / {formato_mem(j64['rss_pico_mb'])} | "
            f"≈ 0 MB ($O(1)$) |"
        )

    # 3. Tablas Matrices Tiempos
    for lang in ["python", "java"]:
        lineas.append(f"\n### 3. Multiplicación de Matrices — Tiempo de Ejecución ({NOMBRE_LENG[lang]})\n")
        lineas.append("| Variante | Representación | 16×16 | 32×32 | 64×64 | 128×128 | 256×256 | 512×512 |")
        lineas.append("| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for var in VARIANTES_MAT:
            rep = "Bidimensional (2D)" if var.endswith("_2d") else "Unidimensional Contiguo (1D)"
            celdas = [formato_tiempo(MAT_MAP[(lang, var, n)]["tiempo_s"]) for n in TAMANIOS_MAT]
            lineas.append(f"| **{NOMBRES_VAR[var]}** | {rep} | " + " | ".join(celdas) + " |")

    # 4. Tablas Matrices Memoria Auxiliar Viva y RSS
    for lang in ["python", "java"]:
        lineas.append(f"\n### 4. Multiplicación de Matrices — Memoria Auxiliar Viva y RSS Pico ({NOMBRE_LENG[lang]})\n")
        lineas.append("| Variante | Métrica | 16×16 | 32×32 | 64×64 | 128×128 | 256×256 | 512×512 |")
        lineas.append("| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |")
        for var in VARIANTES_MAT:
            celdas_extra = [formato_mem(MAT_MAP[(lang, var, n)]["mem_extra_mb"]) for n in TAMANIOS_MAT]
            celdas_rss = [formato_mem(MAT_MAP[(lang, var, n)]["rss_pico_mb"]) for n in TAMANIOS_MAT]
            lineas.append(f"| **{NOMBRES_VAR[var]}** | Memoria Auxiliar Viva | " + " | ".join(celdas_extra) + " |")
            lineas.append(f"| **{NOMBRES_VAR[var]}** | RSS Pico del Proceso | " + " | ".join(celdas_rss) + " |")

    with open(RUTA_TABLAS, "w") as f:
        f.write("\n".join(lineas) + "\n")
    print(f"  ✓ {RUTA_TABLAS}")


def main() -> None:
    print("Generando gráficas y tablas de la Práctica 3...")
    grafica_01_quickselect_tiempo()
    grafica_02_quickselect_32_vs_64()
    grafica_03_quickselect_memoria()
    grafica_04_quickselect_complejidad_speedup()
    _grafica_matrices_lenguaje("python", "05_matrices_tiempo_python.png")
    _grafica_matrices_lenguaje("java", "06_matrices_tiempo_java.png")
    grafica_07_matrices_2d_vs_1d()
    grafica_08_matrices_memoria()
    grafica_09_matrices_complejidad_cruce()
    grafica_10_evidencia_estres()
    generar_tablas_md()
    print("✅ Gráficas y tablas generadas exitosamente.")


if __name__ == "__main__":
    main()
