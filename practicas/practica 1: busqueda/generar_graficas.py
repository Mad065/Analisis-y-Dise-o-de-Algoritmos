#!/usr/bin/env python3
"""
Generador de gráficas comparativas para los algoritmos de búsqueda.
Genera PNGs en la carpeta 'graficas/' con los resultados de Python y Java.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

# Directorio de salida
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graficas")
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# DATOS DE RESULTADOS (extraídos de la ejecución real)
# ============================================================

tamanios = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]
etiquetas = ["1K", "10K", "100K", "1M", "10M"]

# --- Python: Tiempos de búsqueda en microsegundos (µs) ---
py_secuencial = {
    "Mejor":  [1.04, 3.71, 2.79, 4.83, 8.17],
    "Peor":   [34.79, 357.88, 10050, 34060, 448380],
    "NoExiste": [34.92, 358.33, 7870, 31860, 442740],
    "Normal": [21.92, 254.46, 2460, 23420, 236640],
}
py_binaria = {
    "Mejor":  [2.08, 3.42, 4.92, 8.33, 54.88],
    "Peor":   [1.62, 2.83, 4.08, 6.33, 50.25],
    "NoExiste": [1.67, 2.79, 3.67, 5.58, 45.04],
    "Normal": [1.62, 2.50, 3.17, 4.96, 74.83],
}
py_interpolacion = {
    "Mejor":  [2.29, 5.17, 4.42, 4.21, 24.29],
    "Peor":   [0.708, 0.709, 0.542, 0.667, 0.625],
    "NoExiste": [0.333, 0.250, 0.292, 0.250, 0.250],
    "Normal": [1.42, 2.12, 1.46, 2.04, 7.96],
}
py_hash = {
    "Mejor":  [1.92, 3.50, 3.62, 3.67, 1020],
    "Peor":   [0.875, 0.750, 1.00, 1.42, 13.08],
    "NoExiste": [0.584, 0.708, 0.833, 1.04, 5.42],
    "Normal": [0.542, 0.709, 0.833, 0.792, 5.92],
}

# --- Java: Tiempos de búsqueda en microsegundos (µs) ---
java_secuencial = {
    "Mejor":  [1.21, 1.38, 1.50, 0.250, 0.042],
    "Peor":   [8.92, 90.33, 531.63, 393.46, 3100],
    "NoExiste": [9.21, 90.25, 226.13, 244.33, 2000],
    "Normal": [6.71, 42.29, 163.17, 839.96, 1400],
}
java_binaria = {
    "Mejor":  [1.13, 1.58, 2.25, 38.33, 12.38],
    "Peor":   [0.625, 0.334, 0.708, 2.00, 9.79],
    "NoExiste": [0.375, 0.667, 1.08, 7.29, 10.46],
    "Normal": [0.375, 0.708, 0.958, 0.625, 8.92],
}
java_interpolacion = {
    "Mejor":  [1.08, 0.750, 0.875, 1.25, 0.083],
    "Peor":   [0.167, 0.125, 0.125, 0.167, 0.042],
    "NoExiste": [0.084, 0.083, 0.084, 0.084, 0.042],
    "Normal": [0.334, 0.542, 0.458, 0.250, 0.167],
}
java_hash = {
    "Mejor":  [1.08, 1.08, 1.38, 4.54, 74.50],
    "Peor":   [0.792, 0.459, 3.96, 1.46, 29.75],
    "NoExiste": [0.208, 0.125, 0.208, 0.833, 28.54],
    "Normal": [0.416, 0.292, 0.500, 0.875, 23.88],
}

# --- Tiempos de preprocesamiento en milisegundos (ms) ---
py_sort_ms    = [0.095, 1.10, 20.63, 175.69, 2581.2]
py_hash_ms    = [1.19, 4.82, 64.88, 922.79, 16447.8]
java_sort_ms  = [3.91, 3.39, 10.69, 70.77, 702.65]
java_hash_ms  = [1.80, 1.68, 33.29, 212.63, 1960.3]

# ============================================================
# ESTILO COMÚN
# ============================================================
colores = {
    "Secuencial":    "#e74c3c",
    "Binaria":       "#3498db",
    "Interpolación": "#2ecc71",
    "Tabla Hash":    "#f39c12",
}
marcadores = {"Secuencial": "o", "Binaria": "s", "Interpolación": "^", "Tabla Hash": "D"}

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': '#fafafa',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'font.size': 11,
    'figure.dpi': 150,
})


def guardar(fig, nombre):
    ruta = os.path.join(OUT_DIR, nombre)
    fig.savefig(ruta, bbox_inches='tight', dpi=150)
    plt.close(fig)
    print(f"  ✓ Guardado: {ruta}")


# ============================================================
# 1. GRÁFICA: Comparación por caso (Python) – escala log
# ============================================================
def grafica_por_caso_python():
    casos = ["Mejor", "Peor", "NoExiste", "Normal"]
    titulos_caso = ["Mejor Caso", "Peor Caso", "No Existe", "Caso Normal"]
    datos = {
        "Secuencial": py_secuencial,
        "Binaria": py_binaria,
        "Interpolación": py_interpolacion,
        "Tabla Hash": py_hash,
    }

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Python — Tiempos de Búsqueda por Caso (escala log)", fontsize=16, fontweight='bold')

    for idx, (caso, titulo) in enumerate(zip(casos, titulos_caso)):
        ax = axes[idx // 2][idx % 2]
        for algo, vals in datos.items():
            ax.plot(etiquetas, vals[caso], marker=marcadores[algo],
                    color=colores[algo], linewidth=2, markersize=7, label=algo)
        ax.set_yscale('log')
        ax.set_title(titulo, fontsize=13, fontweight='bold')
        ax.set_xlabel("Tamaño del dataset")
        ax.set_ylabel("Tiempo (µs)")
        ax.legend(fontsize=9)

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    guardar(fig, "01_python_por_caso.png")


# ============================================================
# 2. GRÁFICA: Comparación por caso (Java) – escala log
# ============================================================
def grafica_por_caso_java():
    casos = ["Mejor", "Peor", "NoExiste", "Normal"]
    titulos_caso = ["Mejor Caso", "Peor Caso", "No Existe", "Caso Normal"]
    datos = {
        "Secuencial": java_secuencial,
        "Binaria": java_binaria,
        "Interpolación": java_interpolacion,
        "Tabla Hash": java_hash,
    }

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Java — Tiempos de Búsqueda por Caso (escala log)", fontsize=16, fontweight='bold')

    for idx, (caso, titulo) in enumerate(zip(casos, titulos_caso)):
        ax = axes[idx // 2][idx % 2]
        for algo, vals in datos.items():
            ax.plot(etiquetas, vals[caso], marker=marcadores[algo],
                    color=colores[algo], linewidth=2, markersize=7, label=algo)
        ax.set_yscale('log')
        ax.set_title(titulo, fontsize=13, fontweight='bold')
        ax.set_xlabel("Tamaño del dataset")
        ax.set_ylabel("Tiempo (µs)")
        ax.legend(fontsize=9)

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    guardar(fig, "02_java_por_caso.png")


# ============================================================
# 3. GRÁFICA: Peor caso comparativo – todos los algoritmos
# ============================================================
def grafica_peor_caso_comparativo():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle("Peor Caso — Comparación de Algoritmos", fontsize=16, fontweight='bold')

    # Python
    ax = axes[0]
    for algo, vals, c, m in [
        ("Secuencial", py_secuencial["Peor"], colores["Secuencial"], "o"),
        ("Binaria", py_binaria["Peor"], colores["Binaria"], "s"),
        ("Interpolación", py_interpolacion["Peor"], colores["Interpolación"], "^"),
        ("Tabla Hash", py_hash["Peor"], colores["Tabla Hash"], "D"),
    ]:
        ax.plot(etiquetas, vals, marker=m, color=c, linewidth=2.5, markersize=8, label=algo)
    ax.set_yscale('log')
    ax.set_title("Python", fontsize=14, fontweight='bold')
    ax.set_xlabel("Tamaño del dataset")
    ax.set_ylabel("Tiempo (µs)")
    ax.legend()

    # Java
    ax = axes[1]
    for algo, vals, c, m in [
        ("Secuencial", java_secuencial["Peor"], colores["Secuencial"], "o"),
        ("Binaria", java_binaria["Peor"], colores["Binaria"], "s"),
        ("Interpolación", java_interpolacion["Peor"], colores["Interpolación"], "^"),
        ("Tabla Hash", java_hash["Peor"], colores["Tabla Hash"], "D"),
    ]:
        ax.plot(etiquetas, vals, marker=m, color=c, linewidth=2.5, markersize=8, label=algo)
    ax.set_yscale('log')
    ax.set_title("Java", fontsize=14, fontweight='bold')
    ax.set_xlabel("Tamaño del dataset")
    ax.set_ylabel("Tiempo (µs)")
    ax.legend()

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    guardar(fig, "03_peor_caso_comparativo.png")


# ============================================================
# 4. GRÁFICA: Tiempos de preprocesamiento (ordenamiento + hash)
# ============================================================
def grafica_preprocesamiento():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle("Tiempos de Preprocesamiento", fontsize=16, fontweight='bold')

    x = np.arange(len(etiquetas))
    ancho = 0.35

    # Python
    ax = axes[0]
    b1 = ax.bar(x - ancho/2, py_sort_ms, ancho, label='Ordenamiento', color='#3498db', alpha=0.85)
    b2 = ax.bar(x + ancho/2, py_hash_ms, ancho, label='Constr. Tabla Hash', color='#f39c12', alpha=0.85)
    ax.set_title("Python", fontsize=14, fontweight='bold')
    ax.set_xlabel("Tamaño del dataset")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas)
    ax.set_yscale('log')
    ax.legend()

    # Java
    ax = axes[1]
    b1 = ax.bar(x - ancho/2, java_sort_ms, ancho, label='Ordenamiento', color='#3498db', alpha=0.85)
    b2 = ax.bar(x + ancho/2, java_hash_ms, ancho, label='Constr. Tabla Hash', color='#f39c12', alpha=0.85)
    ax.set_title("Java", fontsize=14, fontweight='bold')
    ax.set_xlabel("Tamaño del dataset")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas)
    ax.set_yscale('log')
    ax.legend()

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    guardar(fig, "04_preprocesamiento.png")


# ============================================================
# 5. GRÁFICA: Python vs Java (caso normal)
# ============================================================
def grafica_python_vs_java():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Python vs Java — Caso Normal por Algoritmo", fontsize=16, fontweight='bold')

    datos = [
        ("Secuencial", py_secuencial["Normal"], java_secuencial["Normal"]),
        ("Binaria", py_binaria["Normal"], java_binaria["Normal"]),
        ("Interpolación", py_interpolacion["Normal"], java_interpolacion["Normal"]),
        ("Tabla Hash", py_hash["Normal"], java_hash["Normal"]),
    ]

    for idx, (algo, py_vals, java_vals) in enumerate(datos):
        ax = axes[idx // 2][idx % 2]
        ax.plot(etiquetas, py_vals, marker='o', color='#e74c3c', linewidth=2.5,
                markersize=8, label='Python')
        ax.plot(etiquetas, java_vals, marker='s', color='#3498db', linewidth=2.5,
                markersize=8, label='Java')
        ax.set_yscale('log')
        ax.set_title(algo, fontsize=13, fontweight='bold', color=colores[algo])
        ax.set_xlabel("Tamaño del dataset")
        ax.set_ylabel("Tiempo (µs)")
        ax.legend(fontsize=10)

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    guardar(fig, "05_python_vs_java.png")


# ============================================================
# 6. GRÁFICA: Barras agrupadas por algoritmo – Dataset 10M
# ============================================================
def grafica_barras_10m():
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle("Tiempos de Búsqueda — Dataset 10,000,000 (todos los casos)", fontsize=16, fontweight='bold')

    algos = ["Secuencial", "Binaria", "Interpolación", "Tabla Hash"]
    casos = ["Mejor", "Peor", "NoExiste", "Normal"]
    colores_caso = ["#2ecc71", "#e74c3c", "#95a5a6", "#3498db"]

    x = np.arange(len(algos))
    ancho = 0.2

    # Python
    ax = axes[0]
    py_all = {
        "Secuencial": py_secuencial,
        "Binaria": py_binaria,
        "Interpolación": py_interpolacion,
        "Tabla Hash": py_hash,
    }
    for i, (caso, color) in enumerate(zip(casos, colores_caso)):
        vals = [py_all[a][caso][-1] for a in algos]  # índice -1 = 10M
        ax.bar(x + i * ancho, vals, ancho, label=caso.replace("NoExiste", "No Existe"),
               color=color, alpha=0.85)
    ax.set_title("Python", fontsize=14, fontweight='bold')
    ax.set_xlabel("Algoritmo")
    ax.set_ylabel("Tiempo (µs)")
    ax.set_xticks(x + 1.5 * ancho)
    ax.set_xticklabels(algos, rotation=15)
    ax.set_yscale('log')
    ax.legend(fontsize=9)

    # Java
    ax = axes[1]
    java_all = {
        "Secuencial": java_secuencial,
        "Binaria": java_binaria,
        "Interpolación": java_interpolacion,
        "Tabla Hash": java_hash,
    }
    for i, (caso, color) in enumerate(zip(casos, colores_caso)):
        vals = [java_all[a][caso][-1] for a in algos]
        ax.bar(x + i * ancho, vals, ancho, label=caso.replace("NoExiste", "No Existe"),
               color=color, alpha=0.85)
    ax.set_title("Java", fontsize=14, fontweight='bold')
    ax.set_xlabel("Algoritmo")
    ax.set_ylabel("Tiempo (µs)")
    ax.set_xticks(x + 1.5 * ancho)
    ax.set_xticklabels(algos, rotation=15)
    ax.set_yscale('log')
    ax.legend(fontsize=9)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    guardar(fig, "06_barras_10m.png")


# ============================================================
# 7. GRÁFICA: Escalabilidad – crecimiento con n (caso normal)
# ============================================================
def grafica_escalabilidad():
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.suptitle("Escalabilidad — Caso Normal (Python)", fontsize=16, fontweight='bold')

    # Líneas teóricas de referencia
    ns = np.array(tamanios, dtype=float)
    t_ref = ns / ns[0]  # normalizado para O(n)
    ax.plot(etiquetas, t_ref * py_secuencial["Normal"][0], '--', color='gray',
            alpha=0.4, linewidth=1, label='_nolegend_')

    for algo, vals, c, m in [
        ("Secuencial", py_secuencial["Normal"], colores["Secuencial"], "o"),
        ("Binaria", py_binaria["Normal"], colores["Binaria"], "s"),
        ("Interpolación", py_interpolacion["Normal"], colores["Interpolación"], "^"),
        ("Tabla Hash", py_hash["Normal"], colores["Tabla Hash"], "D"),
    ]:
        ax.plot(etiquetas, vals, marker=m, color=c, linewidth=2.5, markersize=9, label=algo)

    ax.set_yscale('log')
    ax.set_xlabel("Tamaño del dataset", fontsize=13)
    ax.set_ylabel("Tiempo (µs)", fontsize=13)
    ax.legend(fontsize=11)
    ax.annotate("O(n) — Secuencial crece linealmente",
                xy=(3, py_secuencial["Normal"][3]), fontsize=9, color=colores["Secuencial"],
                xytext=(2.5, py_secuencial["Normal"][3]*3),
                arrowprops=dict(arrowstyle='->', color=colores["Secuencial"]))
    ax.annotate("O(1) — Hash se mantiene constante",
                xy=(3, py_hash["Normal"][3]), fontsize=9, color=colores["Tabla Hash"],
                xytext=(1.5, py_hash["Normal"][3]*0.15),
                arrowprops=dict(arrowstyle='->', color=colores["Tabla Hash"]))

    fig.tight_layout(rect=[0, 0, 1, 0.95])
    guardar(fig, "07_escalabilidad.png")


# ============================================================
# EJECUTAR TODAS
# ============================================================
if __name__ == "__main__":
    print("Generando gráficas comparativas...\n")
    grafica_por_caso_python()
    grafica_por_caso_java()
    grafica_peor_caso_comparativo()
    grafica_preprocesamiento()
    grafica_python_vs_java()
    grafica_barras_10m()
    grafica_escalabilidad()
    print(f"\n✅ Todas las gráficas generadas en: {OUT_DIR}")
