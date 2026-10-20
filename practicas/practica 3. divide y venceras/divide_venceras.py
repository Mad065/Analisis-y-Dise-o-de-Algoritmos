#!/usr/bin/env python3
"""
Práctica 3 — Divide y Vencerás (Python).

Implementaciones en Python puro (sin numpy, sin funciones de ordenamiento/selección
nativas) de:

Parte 1 — Selección Rápida (Quickselect / Selección de Hoare):
    * quickselect_hoare(a, k)    O(n) promedio, O(n²) peor caso, espacio extra O(1)
      Evaluado sobre datasets de enteros de 32 bits (`array('i')`, 4 bytes/elem) y
      enteros de 64 bits (`array('q')`, 8 bytes/elem) en permutación pseudoaleatoria
      con valores en [1, 10^7].

Parte 2 — Multiplicación de Matrices Cuadradas (n x n):
    * multiplicar_tradicional_2d(A, B, n)   O(n³)       Arreglo 2D (`list[list[int]]`)
    * multiplicar_tradicional_1d(A, B, n)   O(n³)       Arreglo 1D contiguo (`array('i')`)
    * multiplicar_strassen_2d(A, B, n)      O(n^2.807)  Arreglo 2D (`list[list[int]]`)
    * multiplicar_strassen_1d(A, B, n)      O(n^2.807)  Arreglo 1D contiguo (`array('i')`)

Modo benchmark (invocado por benchmark.py):
    python divide_venceras.py --problema quickselect --bits 32 --n 1000000
    python divide_venceras.py --problema matrices --variante strassen_1d --n 256
Imprime una línea: RESULTADO {json}
"""
from __future__ import annotations

import argparse
import gc
import json
import math
import os
import resource
import sys
import time
from array import array

DIR_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")
RANGO_MAX_QS = 10_000_000


# =====================================================================
# PARTE 1: QUICKSELECT (SELECCIÓN DE HOARE)
# =====================================================================
def _particion_hoare(a, lo: int, hi: int):
    """Esquema de partición bidireccional de C. A. R. Hoare con pivote mediana de tres.

    Reordena a[lo..hi] in-place de modo que:
      - Todo elemento en a[lo..j] es <= pivote
      - Todo elemento en a[i..hi] es >= pivote
    Retorna los índices cruzados (i, j) con j < i.
    """
    mid = (lo + hi) >> 1
    # Ordenar a[lo], a[mid], a[hi] para elegir la mediana como pivote
    if a[mid] < a[lo]:
        a[lo], a[mid] = a[mid], a[lo]
    if a[hi] < a[lo]:
        a[lo], a[hi] = a[hi], a[lo]
    if a[hi] < a[mid]:
        a[mid], a[hi] = a[hi], a[mid]
    pivote = a[mid]

    i = lo
    j = hi
    while i <= j:
        while a[i] < pivote:
            i += 1
        while a[j] > pivote:
            j -= 1
        if i <= j:
            a[i], a[j] = a[j], a[i]
            i += 1
            j -= 1
    return i, j


def quickselect_hoare(a, k: int):
    """Encuentra el elemento que ocuparía la posición k (1 <= k <= n) si el
    arreglo A estuviera ordenado de forma creciente (Algoritmo FIND de Hoare).

    Opera in-place en tiempo promedio O(n) y espacio auxiliar estricto O(1).
    """
    n = len(a)
    if not (1 <= k <= n):
        raise ValueError(f"k={k} fuera del rango válido [1, {n}]")

    objetivo = k - 1  # Índice 0-based correspondiente a la posición k
    lo = 0
    hi = n - 1

    while lo < hi:
        i, j = _particion_hoare(a, lo, hi)
        if objetivo <= j:
            hi = j
        elif objetivo >= i:
            lo = i
        else:
            # j < objetivo < i: el elemento en a[objetivo] ya es el pivote exacto
            break

    return a[objetivo]


# =====================================================================
# PARTE 2: MULTIPLICACIÓN DE MATRICES (TRADICIONAL vs STRASSEN, 2D vs 1D)
# =====================================================================
def multiplicar_tradicional_2d(A: list, B: list, n: int) -> list:
    """Multiplicación clásica O(n³) usando arreglos bidimensionales (list[list[int]])."""
    C = [[0] * n for _ in range(n)]
    for i in range(n):
         fila_a = A[i]
         fila_c = C[i]
         for k in range(n):
             aik = fila_a[k]
             fila_b = B[k]
             for j in range(n):
                 fila_c[j] += aik * fila_b[j]
    return C


def multiplicar_tradicional_1d(A: array, B: array, n: int) -> array:
    """Multiplicación clásica O(n³) usando arreglos unidimensionales contiguos (array('i'))."""
    C = array("i", [0]) * (n * n)
    for i in range(n):
        in_ = i * n
        for k in range(n):
            aik = A[in_ + k]
            kn = k * n
            for j in range(n):
                C[in_ + j] += aik * B[kn + j]
    return C


def _sumar_2d(A: list, B: list, n: int) -> list:
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def _restar_2d(A: list, B: list, n: int) -> list:
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def multiplicar_strassen_2d(A: list, B: list, n: int) -> list:
    """Algoritmo de Strassen O(n^log2(7)) ≈ O(n^2.807) con arreglos bidimensionales."""
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    m = n >> 1
    A11 = [fila[:m] for fila in A[:m]]
    A12 = [fila[m:] for fila in A[:m]]
    A21 = [fila[:m] for fila in A[m:]]
    A22 = [fila[m:] for fila in A[m:]]

    B11 = [fila[:m] for fila in B[:m]]
    B12 = [fila[m:] for fila in B[:m]]
    B21 = [fila[:m] for fila in B[m:]]
    B22 = [fila[m:] for fila in B[m:]]

    # 7 productos recursivos de Strassen
    M1 = multiplicar_strassen_2d(_sumar_2d(A11, A22, m), _sumar_2d(B11, B22, m), m)
    M2 = multiplicar_strassen_2d(_sumar_2d(A21, A22, m), B11, m)
    M3 = multiplicar_strassen_2d(A11, _restar_2d(B12, B22, m), m)
    M4 = multiplicar_strassen_2d(A22, _restar_2d(B21, B11, m), m)
    M5 = multiplicar_strassen_2d(_sumar_2d(A11, A12, m), B22, m)
    M6 = multiplicar_strassen_2d(_restar_2d(A21, A11, m), _sumar_2d(B11, B12, m), m)
    M7 = multiplicar_strassen_2d(_restar_2d(A12, A22, m), _sumar_2d(B21, B22, m), m)

    # Ensamblar cuadrantes C11, C12, C21, C22
    C = [[0] * n for _ in range(n)]
    for i in range(m):
        c_sup = C[i]
        c_inf = C[i + m]
        m1_i, m2_i, m3_i, m4_i = M1[i], M2[i], M3[i], M4[i]
        m5_i, m6_i, m7_i = M5[i], M6[i], M7[i]
        for j in range(m):
            m1, m2, m3, m4 = m1_i[j], m2_i[j], m3_i[j], m4_i[j]
            m5, m6, m7 = m5_i[j], m6_i[j], m7_i[j]
            c_sup[j] = m1 + m4 - m5 + m7
            c_sup[j + m] = m3 + m5
            c_inf[j] = m2 + m4
            c_inf[j + m] = m1 - m2 + m3 + m6
    return C


def _sumar_1d(A: array, B: array, tam: int) -> array:
    return array("i", (A[k] + B[k] for k in range(tam)))


def _restar_1d(A: array, B: array, tam: int) -> array:
    return array("i", (A[k] - B[k] for k in range(tam)))


def multiplicar_strassen_1d(A: array, B: array, n: int) -> array:
    """Algoritmo de Strassen O(n^log2(7)) ≈ O(n^2.807) con arreglos 1D contiguos."""
    if n == 1:
        return array("i", (A[0] * B[0],))

    m = n >> 1
    mm = m * m
    A11, A12, A21, A22 = array("i"), array("i"), array("i"), array("i")
    B11, B12, B21, B22 = array("i"), array("i"), array("i"), array("i")

    # Extracción de cuadrantes por rebanadas contiguas de fila
    mitad_filas = m * n
    total_elem = n * n
    for base in range(0, mitad_filas, n):
        medio = base + m
        fin = base + n
        A11.extend(A[base:medio])
        A12.extend(A[medio:fin])
        B11.extend(B[base:medio])
        B12.extend(B[medio:fin])
    for base in range(mitad_filas, total_elem, n):
        medio = base + m
        fin = base + n
        A21.extend(A[base:medio])
        A22.extend(A[medio:fin])
        B21.extend(B[base:medio])
        B22.extend(B[medio:fin])

    # 7 productos recursivos de Strassen sobre bloques 1D contiguos
    M1 = multiplicar_strassen_1d(_sumar_1d(A11, A22, mm), _sumar_1d(B11, B22, mm), m)
    M2 = multiplicar_strassen_1d(_sumar_1d(A21, A22, mm), B11, m)
    M3 = multiplicar_strassen_1d(A11, _restar_1d(B12, B22, mm), m)
    M4 = multiplicar_strassen_1d(A22, _restar_1d(B21, B11, mm), m)
    M5 = multiplicar_strassen_1d(_sumar_1d(A11, A12, mm), B22, m)
    M6 = multiplicar_strassen_1d(_restar_1d(A21, A11, mm), _sumar_1d(B11, B12, mm), m)
    M7 = multiplicar_strassen_1d(_restar_1d(A12, A22, mm), _sumar_1d(B21, B22, mm), m)

    C = array("i", (0,)) * total_elem
    for i in range(m):
        im = i * m
        in1 = i * n
        in2 = (i + m) * n
        for j in range(m):
            k = im + j
            m1, m2, m3, m4 = M1[k], M2[k], M3[k], M4[k]
            m5, m6, m7 = M5[k], M6[k], M7[k]
            C[in1 + j] = m1 + m4 - m5 + m7
            C[in1 + m + j] = m3 + m5
            C[in2 + j] = m2 + m4
            C[in2 + m + j] = m1 - m2 + m3 + m6
    return C


VARIANTES_MATRICES = {
    "tradicional_2d": multiplicar_tradicional_2d,
    "tradicional_1d": multiplicar_tradicional_1d,
    "strassen_2d": multiplicar_strassen_2d,
    "strassen_1d": multiplicar_strassen_1d,
}


# =====================================================================
# UTILIDADES DE CARGA, VERIFICACIÓN Y MEDICIÓN DE MEMORIA
# =====================================================================
def rss_pico_bytes() -> int:
    """Pico de memoria residente del proceso (macOS: bytes; Linux: KB)."""
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def cargar_dataset_quickselect(bits: int, n: int) -> array:
    """Lee el archivo binario qs<bits>_n_<n>.bin directamente en un array contiguo."""
    ruta = os.path.join(DIR_DATOS, f"qs{bits}_n_{n}.bin")
    codigo = "i" if bits == 32 else "q"
    a = array(codigo, [0]) * n
    with open(ruta, "rb", buffering=0) as f:
        vista = memoryview(a).cast("B")
        leidos = 0
        while leidos < len(vista):
            m = f.readinto(vista[leidos:])
            if not m:
                raise IOError(f"Archivo incompleto: {ruta}")
            leidos += m
        vista.release()
    if sys.byteorder != "little":
        a.byteswap()
    return a


def cargar_dataset_matrices_1d(n: int) -> tuple[array, array]:
    """Lee mat_n_<n>.bin y devuelve (A, B) como dos arreglos 1D contiguos array('i')."""
    ruta = os.path.join(DIR_DATOS, f"mat_n_{n}.bin")
    nn = n * n
    buf = array("i", [0]) * (2 * nn)
    with open(ruta, "rb", buffering=0) as f:
        vista = memoryview(buf).cast("B")
        leidos = 0
        while leidos < len(vista):
            m = f.readinto(vista[leidos:])
            if not m:
                raise IOError(f"Archivo incompleto: {ruta}")
            leidos += m
        vista.release()
    if sys.byteorder != "little":
        buf.byteswap()
    return buf[:nn], buf[nn:]


def convertir_a_2d(arr1d: array, n: int) -> list:
    """Convierte un arreglo 1D contiguo de tamaño n*n en una matriz 2D list[list[int]]."""
    return [list(arr1d[i * n : (i + 1) * n]) for i in range(n)]


def bytes_matriz_py(es_2d: bool, n: int) -> int:
    """Calcula el tamaño exacto en bytes de una matriz n x n en CPython."""
    if not es_2d:
        # array('i') de n*n elementos: cabecera CPython (~64 B) + 4 * n^2 bytes
        return 64 + 4 * n * n
    # list[list[int]]: lista externa + n listas internas + n^2 objetos int (28 B c/u)
    tam_lista_ext = 56 + 8 * n
    tam_listas_filas = n * (56 + 8 * n)
    tam_enteros = n * n * 28
    return tam_lista_ext + tam_listas_filas + tam_enteros


def memoria_auxiliar_matrices_bytes(variante: str, n: int) -> tuple[int, int]:
    """Devuelve (memoria_pico_viva_bytes, memoria_acumulada_asignada_bytes) para matrices."""
    es_2d = variante.endswith("_2d")
    if variante.startswith("tradicional"):
        tam_c = bytes_matriz_py(es_2d, n)
        return tam_c, tam_c

    # En Strassen: en cada nivel de recursión d (con submatrices de lado m = n / 2^(d+1)),
    # el marco activo mantiene 8 cuadrantes (A11..B22), hasta 7 productos (M1..M7) y
    # 2 sumas/restas temporales = 17 submatrices de lado m vivas simultáneamente en la pila,
    # más la matriz de salida C de lado n.
    niveles = int(round(math.log2(n)))
    viva = bytes_matriz_py(es_2d, n)
    acumulada = 0
    for d in range(niveles):
        m = n >> (d + 1)
        tam_m = bytes_matriz_py(es_2d, m)
        tam_padre = bytes_matriz_py(es_2d, n >> d)
        viva += 17 * tam_m
        # Cada nodo en el nivel d (hay 7^d nodos) crea 8 cuadrantes + 10 sumas/restas + 1 matriz C
        acumulada += (7**d) * (18 * tam_m + tam_padre)
    # Caso base n=1 (7^niveles hojas)
    acumulada += (7**niveles) * bytes_matriz_py(es_2d, 1)
    return viva, acumulada


def verificar_quickselect(a: array, k: int, resultado: int, suma_antes: int) -> bool:
    """Verifica en O(n) que `resultado` sea exactamente el k-ésimo menor elemento."""
    n = len(a)
    idx = k - 1
    if a[idx] != resultado:
        return False
    # 1. Invariante de partición alrededor de idx
    for i in range(idx):
        if a[i] > resultado:
            return False
    for i in range(idx + 1, n):
        if a[i] < resultado:
            return False
    # 2. Invariante de permutación (suma exacta)
    if sum(a) != suma_antes:
        return False
    # 3. Verificación analítica del estrato [1, 10^7]
    paso = RANGO_MAX_QS // n
    if not ((k - 1) * paso + 1 <= resultado <= k * paso):
        return False
    return True


def verificar_matrices(A1d: array, B1d: array, C, es_2d: bool, n: int) -> bool:
    """Verifica C == A * B en O(n²) mediante la identidad asociativa A*(B*v) == C*v
    con dos vectores independientes v1 = (1..n) y v2 = alternante."""
    v1 = [j + 1 for j in range(n)]
    v2 = [((j * 31 + 7) % 97) - 48 for j in range(n)]

    # Calcular w1 = B * v1 y w2 = B * v2
    w1 = [0] * n
    w2 = [0] * n
    for k in range(n):
        kn = k * n
        s1 = 0
        s2 = 0
        for j in range(n):
            bkj = B1d[kn + j]
            s1 += bkj * v1[j]
            s2 += bkj * v2[j]
        w1[k] = s1
        w2[k] = s2

    # Comparar A * w con C * v fila por fila
    for i in range(n):
        in_ = i * n
        aw1 = 0
        aw2 = 0
        for k in range(n):
            aik = A1d[in_ + k]
            aw1 += aik * w1[k]
            aw2 += aik * w2[k]

        cv1 = 0
        cv2 = 0
        if es_2d:
            fila_c = C[i]
            for j in range(n):
                cij = fila_c[j]
                cv1 += cij * v1[j]
                cv2 += cij * v2[j]
        else:
            for j in range(n):
                cij = C[in_ + j]
                cv1 += cij * v1[j]
                cv2 += cij * v2[j]

        if aw1 != cv1 or aw2 != cv2:
            return False
    return True


# =====================================================================
# EJECUTORES DE BENCHMARK
# =====================================================================
def correr_quickselect(bits: int, n: int, k: int | None = None) -> dict:
    if k is None:
        k = (n // 2) + 1  # Mediana por defecto
    a = cargar_dataset_quickselect(bits, n)
    suma_antes = sum(a)
    mem_datos = sys.getsizeof(a)

    gc.collect()
    mem_base = rss_pico_bytes()

    gc.disable()
    t0 = time.perf_counter_ns()
    resultado = quickselect_hoare(a, k)
    t1 = time.perf_counter_ns()
    gc.enable()

    mem_pico = rss_pico_bytes()
    ok = verificar_quickselect(a, k, int(resultado), suma_antes)
    mb = 1024.0 * 1024.0
    return {
        "lenguaje": "python",
        "problema": "quickselect",
        "variante": f"{bits}bits",
        "bits": bits,
        "n": n,
        "k": k,
        "resultado": int(resultado),
        "tiempo_s": (t1 - t0) / 1e9,
        "mem_datos_mb": mem_datos / mb,
        "mem_base_mb": mem_base / mb,
        "mem_pico_mb": mem_pico / mb,
        "mem_extra_mb": max(0, mem_pico - mem_base) / mb,
        "verificado": ok,
    }


def correr_matrices(variante: str, n: int) -> dict:
    A1d, B1d = cargar_dataset_matrices_1d(n)
    es_2d = variante.endswith("_2d")
    if es_2d:
        A = convertir_a_2d(A1d, n)
        B = convertir_a_2d(B1d, n)
    else:
        A, B = A1d, B1d

    mem_datos = 2 * bytes_matriz_py(es_2d, n)
    mem_viva_teorica, mem_acumulada = memoria_auxiliar_matrices_bytes(variante, n)

    gc.collect()
    mem_base = rss_pico_bytes()

    gc.disable()
    t0 = time.perf_counter_ns()
    C = VARIANTES_MATRICES[variante](A, B, n)
    t1 = time.perf_counter_ns()
    gc.enable()

    mem_pico = rss_pico_bytes()
    delta_rss = max(0, mem_pico - mem_base)
    mem_extra = max(delta_rss, mem_viva_teorica)
    ok = verificar_matrices(A1d, B1d, C, es_2d, n)
    mb = 1024.0 * 1024.0
    return {
        "lenguaje": "python",
        "problema": "matrices",
        "variante": variante,
        "algoritmo": "strassen" if variante.startswith("strassen") else "tradicional",
        "representacion": "2d" if es_2d else "1d",
        "n": n,
        "tiempo_s": (t1 - t0) / 1e9,
        "mem_datos_mb": mem_datos / mb,
        "mem_base_mb": mem_base / mb,
        "mem_pico_mb": mem_pico / mb,
        "mem_extra_mb": mem_extra / mb,
        "mem_acumulada_mb": mem_acumulada / mb,
        "verificado": ok,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Benchmark individual — Práctica 3 (Divide y Vencerás)")
    p.add_argument("--problema", required=True, choices=["quickselect", "matrices"])
    p.add_argument("--bits", type=int, choices=[32, 64], default=32)
    p.add_argument("--variante", choices=list(VARIANTES_MATRICES), default="strassen_1d")
    p.add_argument("--n", required=True, type=int)
    p.add_argument("--k", type=int, default=None)
    args = p.parse_args()

    sys.setrecursionlimit(10_000)
    if args.problema == "quickselect":
        res = correr_quickselect(args.bits, args.n, args.k)
    else:
        res = correr_matrices(args.variante, args.n)

    print("RESULTADO " + json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
