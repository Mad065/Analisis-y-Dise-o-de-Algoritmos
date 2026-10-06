#!/usr/bin/env python3
"""
Generador de gráficas y tablas para la Práctica 2 (Algoritmos de Ordenamiento).

Lee `resultados/resultados.json` (producido por benchmark.py) y genera:
  * graficas/*.png         — 8 gráficas comparativas
  * resultados/tablas.md   — tablas Markdown listas para el reporte

Convención visual: valores MEDIDOS = línea sólida + marcador relleno;
valores ESTIMADOS = línea punteada + marcador hueco.
"""
import json
import math
import os
import sys

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
import numpy as np  # noqa: E402

DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_JSON = sys.argv[1] if len(sys.argv) > 1 else os.path.join(DIR, "resultados", "resultados.json")
OUT_DIR = os.path.join(DIR, "graficas")
RUTA_TABLAS = os.path.join(DIR, "resultados", "tablas.md")
os.makedirs(OUT_DIR, exist_ok=True)

TAMANIOS = [100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000]
ETIQUETAS_N = ["10⁵", "10⁶", "10⁷", "10⁸", "10⁹"]
ETIQUETAS_N_TABLA = ["100,000", "1,000,000", "10,000,000", "100,000,000", "1,000,000,000"]
ALGORITMOS = ["bubble", "merge", "tree", "heap", "counting"]
LENGUAJES = ["python", "java"]
K_CLAVES = 1_000_000

NOMBRES = {"bubble": "Bubble Sort", "merge": "Merge Sort", "tree": "Tree Sort",
           "heap": "Heap Sort", "counting": "Counting Sort"}
NOMBRE_LENG = {"python": "Python", "java": "Java"}
COLORES = {"bubble": "#e74c3c", "merge": "#3498db", "tree": "#2ecc71",
           "heap": "#9b59b6", "counting": "#f39c12"}
MARCADORES = {"bubble": "o", "merge": "s", "tree": "^", "heap": "D", "counting": "P"}
COLOR_LENG = {"python": "#e74c3c", "java": "#3498db"}
MARCA_LENG = {"python": "o", "java": "s"}
SUPER_ESTADO = {"timeout": "T", "omitido_tiempo": "P", "omitido_ram": "R"}

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#fafafa",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "font.size": 11,
    "figure.dpi": 150,
})

with open(RUTA_JSON) as f:
    DATOS = json.load(f)
CORRIDAS = {(c["lenguaje"], c["algoritmo"], c["n"]): c for c in DATOS["corridas"]}


# ---------------------------------------------------------------------
# Acceso a datos
# ---------------------------------------------------------------------
def valor(lang, alg, n, metrica):
    """Devuelve (valor, estimado, estado). metrica: 'tiempo' | 'rss' | 'extra'."""
    c = CORRIDAS.get((lang, alg, n))
    if c is None:
        return None, False, None
    if c["estado"] == "ok":
        v = {"tiempo": c["tiempo_s"], "rss": c["rss_pico_mb"], "extra": c["mem_extra_mb"]}[metrica]
        return v, False, "ok"
    if c.get("estimado"):
        v = {"tiempo": c["tiempo_est_s"], "rss": c["rss_est_mb"], "extra": c["mem_extra_est_mb"]}[metrica]
        return v, True, c["estado"]
    return None, False, c["estado"]


def serie(lang, alg, metrica):
    xs, ys, est = [], [], []
    for n in TAMANIOS:
        v, e, _ = valor(lang, alg, n, metrica)
        if v is not None:
            xs.append(n)
            ys.append(max(v, 1e-9))
            est.append(e)
    return xs, ys, est


def f_complejidad(alg, n):
    if alg == "bubble":
        return n * n
    if alg == "counting":
        return n + K_CLAVES
    return n * math.log2(n)


# ---------------------------------------------------------------------
# Dibujo
# ---------------------------------------------------------------------
def dibujar(ax, xs, ys, est, color, marcador, etiqueta, lw=2.2, ms=7):
    for i in range(len(xs) - 1):
        estilo = "-" if not (est[i] or est[i + 1]) else "--"
        ax.plot(xs[i:i + 2], ys[i:i + 2], estilo, color=color, linewidth=lw,
                alpha=1.0 if estilo == "-" else 0.6)
    for x, y, e in zip(xs, ys, est):
        ax.plot([x], [y], marcador, color=color, markersize=ms,
                markerfacecolor="white" if e else color, markeredgewidth=1.8)
    ax.plot([], [], "-", marker=marcador, color=color, label=etiqueta)


def configurar_eje_n(ax):
    ax.set_xscale("log")
    ax.set_xticks(TAMANIOS)
    ax.set_xticklabels(ETIQUETAS_N)
    ax.minorticks_off()
    ax.set_xlabel("Tamaño del arreglo (n)")


def leyenda_estimado(ax, loc="lower right"):
    extra = [Line2D([], [], color="gray", marker="o", linestyle="-", label="Medido"),
             Line2D([], [], color="gray", marker="o", linestyle="--", markerfacecolor="white",
                    label="Estimado")]
    leg = ax.legend(handles=extra, loc=loc, fontsize=8, framealpha=0.9)
    ax.add_artist(leg)


def eje_tiempo(ax):
    if ax.has_data():
        ax.set_yscale("log")
    ax.set_ylabel("Tiempo (s, escala log)")
    referencias = [(1, "1 s"), (60, "1 min"), (3600, "1 h"), (86400, "1 día"), (86400 * 365, "1 año")]
    y0, y1 = ax.get_ylim()
    for v, txt in referencias:
        if y0 < v < y1:
            ax.axhline(v, color="gray", linestyle=":", linewidth=0.8, alpha=0.6)
            ax.text(ax.get_xlim()[0] * 1.05, v * 1.15, txt, fontsize=7, color="gray")


def guardar(fig, nombre):
    ruta = os.path.join(OUT_DIR, nombre)
    fig.savefig(ruta, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  ✓ {ruta}")


# ---------------------------------------------------------------------
# Gráficas
# ---------------------------------------------------------------------
def grafica_tiempo_lenguaje(lang, nombre):
    fig, ax = plt.subplots(figsize=(11, 7))
    for alg in ALGORITMOS:
        xs, ys, est = serie(lang, alg, "tiempo")
        dibujar(ax, xs, ys, est, COLORES[alg], MARCADORES[alg], NOMBRES[alg])
    configurar_eje_n(ax)
    eje_tiempo(ax)
    ax.set_title(f"{NOMBRE_LENG[lang]} — Tiempo de ejecución vs n (log-log)", fontsize=15, fontweight="bold")
    leyenda_estimado(ax)
    ax.legend(loc="upper left", fontsize=10)
    guardar(fig, nombre)


def grafica_python_vs_java():
    fig, axes = plt.subplots(2, 3, figsize=(17, 10))
    fig.suptitle("Python vs Java — Tiempo de ejecución por algoritmo", fontsize=16, fontweight="bold")
    for idx, alg in enumerate(ALGORITMOS):
        ax = axes[idx // 3][idx % 3]
        for lang in LENGUAJES:
            xs, ys, est = serie(lang, alg, "tiempo")
            dibujar(ax, xs, ys, est, COLOR_LENG[lang], MARCA_LENG[lang], NOMBRE_LENG[lang])
        configurar_eje_n(ax)
        eje_tiempo(ax)
        ax.set_title(NOMBRES[alg], fontsize=13, fontweight="bold", color=COLORES[alg])
        ax.legend(loc="upper left", fontsize=9)
    ax = axes[1][2]
    ax.axis("off")
    ax.text(0.05, 0.6,
            "Línea sólida / marcador relleno: medido\n"
            "Línea punteada / marcador hueco: estimado\n\n"
            "Estimación: T(n) = T(n₀) · f(n) / f(n₀)\n"
            "  Bubble:   f(n) = n²\n"
            "  Merge, Tree, Heap: f(n) = n log n\n"
            "  Counting: f(n) = n + k",
            fontsize=11, va="center", family="monospace")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    guardar(fig, "03_python_vs_java.png")


def grafica_memoria(metrica, nombre, titulo, ylabel):
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))
    fig.suptitle(titulo, fontsize=16, fontweight="bold")
    for ax, lang in zip(axes, LENGUAJES):
        for alg in ALGORITMOS:
            xs, ys, est = serie(lang, alg, metrica)
            if metrica == "extra":
                ys = [max(y, 0.05) for y in ys]     # escala log: 0 MB se dibuja en el piso
            dibujar(ax, xs, ys, est, COLORES[alg], MARCADORES[alg], NOMBRES[alg])
        configurar_eje_n(ax)
        if ax.has_data():
            ax.set_yscale("log")
        ax.set_ylabel(ylabel)
        ax.set_title(NOMBRE_LENG[lang], fontsize=14, fontweight="bold")
        if metrica == "rss":
            ram_mb = DATOS["meta"]["ram_gb"] * 1024
            ax.axhline(ram_mb, color="black", linestyle="-.", linewidth=1.2)
            ax.text(TAMANIOS[0], ram_mb * 1.12, f"RAM física ({DATOS['meta']['ram_gb']:.0f} GB)", fontsize=8)
        leyenda_estimado(ax)
        ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    guardar(fig, nombre)


def grafica_barras(n_obj=10_000_000):
    fig, ax = plt.subplots(figsize=(12, 6.5))
    x = np.arange(len(ALGORITMOS))
    ancho = 0.38
    for i, lang in enumerate(LENGUAJES):
        for j, alg in enumerate(ALGORITMOS):
            v, e, _ = valor(lang, alg, n_obj, "tiempo")
            if v is None:
                continue
            ax.bar(x[j] + (i - 0.5) * ancho, v, ancho, color=COLOR_LENG[lang], alpha=0.45 if e else 0.9,
                   hatch="//" if e else None, edgecolor="black", linewidth=0.6)
            ax.text(x[j] + (i - 0.5) * ancho, v * 1.15, formato_tiempo(v, e), ha="center", fontsize=8,
                    rotation=0)
    if ax.has_data():
        ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([NOMBRES[a] for a in ALGORITMOS])
    ax.set_ylabel("Tiempo (s, escala log)")
    ax.set_title(f"Tiempo de ejecución con n = {n_obj:,}", fontsize=15, fontweight="bold")
    handles = [Rectangle((0, 0), 1, 1, color=COLOR_LENG[l], alpha=0.9) for l in LENGUAJES]
    handles.append(Rectangle((0, 0), 1, 1, facecolor="white", hatch="//", edgecolor="black"))
    ax.legend(handles, ["Python", "Java", "Estimado"], fontsize=10)
    guardar(fig, "06_barras_10M.png")


def grafica_speedup():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    for alg in ALGORITMOS:
        xs, ys, est = [], [], []
        for n in TAMANIOS:
            vp, ep, _ = valor("python", alg, n, "tiempo")
            vj, ej, _ = valor("java", alg, n, "tiempo")
            if vp is not None and vj is not None and vj > 0:
                xs.append(n)
                ys.append(vp / vj)
                est.append(ep or ej)
        dibujar(ax, xs, ys, est, COLORES[alg], MARCADORES[alg], NOMBRES[alg])
    configurar_eje_n(ax)
    if ax.has_data():
        ax.set_yscale("log")
    ax.set_ylabel("Speedup = T_Python / T_Java (escala log)")
    ax.axhline(1, color="black", linewidth=0.8)
    ax.set_title("¿Cuántas veces es más rápido Java que Python?", fontsize=15, fontweight="bold")
    leyenda_estimado(ax)
    ax.legend(loc="upper left", fontsize=10)
    guardar(fig, "07_speedup_java.png")


def grafica_complejidad_empirica():
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))
    fig.suptitle("Complejidad empírica: T(n) / f(n), normalizado al primer n medido",
                 fontsize=16, fontweight="bold")
    for ax, lang in zip(axes, LENGUAJES):
        for alg in ALGORITMOS:
            xs, ys = [], []
            for n in TAMANIOS:
                v, e, _ = valor(lang, alg, n, "tiempo")
                if v is not None and not e:
                    xs.append(n)
                    ys.append(v / f_complejidad(alg, n))
            if not ys:
                continue
            ys = [y / ys[0] for y in ys]
            ax.plot(xs, ys, "-", marker=MARCADORES[alg], color=COLORES[alg], linewidth=2.2, markersize=7,
                    label=f"{NOMBRES[alg]}  (f = {'n²' if alg == 'bubble' else 'n+k' if alg == 'counting' else 'n log n'})")
        configurar_eje_n(ax)
        ax.axhline(1, color="black", linestyle="--", linewidth=1)
        ax.set_ylabel("T(n)/f(n) relativo  (1 = coincide con la teoría)")
        ax.set_title(NOMBRE_LENG[lang], fontsize=14, fontweight="bold")
        ax.legend(fontsize=9, loc="upper left")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    guardar(fig, "08_complejidad_empirica.png")


# ---------------------------------------------------------------------
# Tablas Markdown
# ---------------------------------------------------------------------
def formato_tiempo(s, estimado=False):
    if s < 1e-3:
        t = f"{s * 1e6:.1f} µs"
    elif s < 1:
        t = f"{s * 1e3:.2f} ms"
    elif s < 120:
        t = f"{s:.2f} s"
    elif s < 7200:
        t = f"{s / 60:.1f} min"
    elif s < 172800:
        t = f"{s / 3600:.1f} h"
    elif s < 86400 * 365:
        t = f"{s / 86400:.1f} días"
    else:
        t = f"{s / (86400 * 365):,.1f} años"
    return ("≈" + t) if estimado else t


def formato_mem(mb, estimado=False):
    t = f"{mb / 1024:.2f} GB" if mb >= 1024 else f"{mb:.1f} MB"
    return ("≈" + t) if estimado else t


def celda(lang, alg, n, metrica):
    v, e, estado = valor(lang, alg, n, metrica)
    if v is None:
        return "—"
    fmt = formato_tiempo if metrica == "tiempo" else formato_mem
    if metrica == "extra" and v < 0.05 and not e:
        return "≈ 0 MB"
    txt = fmt(v, e)
    if e:
        txt = f"*{txt}*<sup>{SUPER_ESTADO.get(str(estado), '?')}</sup>"
    return txt


def tabla(lang, metrica):
    filas = ["| Algoritmo | " + " | ".join(ETIQUETAS_N_TABLA) + " |",
             "| --- | " + " | ".join(["---:"] * len(TAMANIOS)) + " |"]
    for alg in ALGORITMOS:
        filas.append(f"| {NOMBRES[alg]} | " + " | ".join(celda(lang, alg, n, metrica) for n in TAMANIOS) + " |")
    return "\n".join(filas)


def tabla_speedup():
    filas = ["| Algoritmo | " + " | ".join(ETIQUETAS_N_TABLA) + " |",
             "| --- | " + " | ".join(["---:"] * len(TAMANIOS)) + " |"]
    for alg in ALGORITMOS:
        celdas = []
        for n in TAMANIOS:
            vp, ep, _ = valor("python", alg, n, "tiempo")
            vj, ej, _ = valor("java", alg, n, "tiempo")
            if vp is None or vj is None or vj <= 0:
                celdas.append("—")
            elif ep or ej:
                celdas.append(f"*≈{vp / vj:,.0f}×*")
            else:
                celdas.append(f"{vp / vj:,.0f}×")
        filas.append(f"| {NOMBRES[alg]} | " + " | ".join(celdas) + " |")
    return "\n".join(filas)


def tabla_estados():
    filas = ["| Lenguaje | Algoritmo | n | Estado | Motivo | Estimado desde |",
             "| --- | --- | ---: | --- | --- | ---: |"]
    for c in sorted(DATOS["corridas"], key=lambda c: (LENGUAJES.index(c["lenguaje"]),
                                                       ALGORITMOS.index(c["algoritmo"]), c["n"])):
        if c["estado"] == "ok":
            continue
        base = f"{c['base_estimacion_n']:,}" if c.get("base_estimacion_n") else "—"
        filas.append(f"| {NOMBRE_LENG[c['lenguaje']]} | {NOMBRES[c['algoritmo']]} | {c['n']:,} | "
                     f"`{c['estado']}`<sup>{SUPER_ESTADO.get(c['estado'], '')}</sup> | {c.get('motivo', '')} | {base} |")
    return "\n".join(filas)


def tabla_verificacion():
    ok = [c for c in DATOS["corridas"] if c["estado"] == "ok"]
    verif = sum(1 for c in ok if c.get("verificado"))
    return f"Corridas ejecutadas: **{len(ok)}** — verificadas correctamente: **{verif}/{len(ok)}**"


def escribir_tablas():
    partes = ["<!-- Generado automáticamente por generar_graficas.py -->"]
    for lang in LENGUAJES:
        partes += [f"\n#### Tiempo de ejecución — {NOMBRE_LENG[lang]}\n", tabla(lang, "tiempo")]
    for lang in LENGUAJES:
        partes += [f"\n#### Memoria pico del proceso (RSS) — {NOMBRE_LENG[lang]}\n", tabla(lang, "rss")]
    for lang in LENGUAJES:
        partes += [f"\n#### Memoria extra del algoritmo — {NOMBRE_LENG[lang]}\n", tabla(lang, "extra")]
    partes += ["\n#### Speedup de Java sobre Python (T_Python / T_Java)\n", tabla_speedup()]
    partes += ["\n#### Corridas no ejecutadas\n", tabla_estados()]
    partes += ["\n" + tabla_verificacion() + "\n"]
    with open(RUTA_TABLAS, "w") as f:
        f.write("\n".join(partes))
    print(f"  ✓ {RUTA_TABLAS}")


if __name__ == "__main__":
    print("Generando gráficas y tablas...")
    grafica_tiempo_lenguaje("python", "01_tiempo_python.png")
    grafica_tiempo_lenguaje("java", "02_tiempo_java.png")
    grafica_python_vs_java()
    grafica_memoria("rss", "04_memoria_pico_rss.png", "Memoria pico del proceso (RSS) vs n", "RSS pico (MB, escala log)")
    grafica_memoria("extra", "05_memoria_extra.png", "Memoria extra consumida por el algoritmo vs n",
                    "Memoria extra (MB, escala log)")
    grafica_barras()
    grafica_speedup()
    grafica_complejidad_empirica()
    escribir_tablas()
    print("✅ Listo")
