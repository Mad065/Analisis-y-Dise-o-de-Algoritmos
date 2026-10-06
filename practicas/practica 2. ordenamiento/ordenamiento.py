#!/usr/bin/env python3
"""
Práctica 2 — Algoritmos de Ordenamiento (Python).

Implementaciones en Python puro (sin sorted(), sin numpy) de:
    1. Bubble Sort      O(n²)          espacio extra O(1)
    2. Merge Sort       O(n log n)     espacio extra O(n)
    3. Tree Sort        O(n log n)*    espacio extra O(nodos)
    4. Heap Sort        O(n log n)     espacio extra O(1)
    5. Counting Sort    O(n + k)       espacio extra O(n + k)

Todas las funciones ordenan IN-PLACE una secuencia mutable de floats
(se usa `array('d')`: 8 bytes por elemento, frente a ~32 bytes en un `list`,
lo que permite trabajar con 10^8 elementos en un equipo de 8 GB).

Modo benchmark (una sola corrida, la usa benchmark.py):
    python ordenamiento.py --algoritmo merge --n 1000000
Imprime una línea:  RESULTADO {json}
"""
import argparse
import gc
import json
import os
import resource
import sys
import time
from array import array
from itertools import islice
from operator import le

# Counting Sort sobre reales: precisión fija de 2 decimales => clave = round(x * 100)
ESCALA_COUNTING = 100


# =====================================================================
# 1. BUBBLE SORT
# =====================================================================
def bubble_sort(a):
    """Bubble Sort optimizado.

    Tras cada pasada, todo lo que está después del último intercambio ya está
    en su posición final, así que el límite se reduce a esa posición. Si en
    una pasada no hay intercambios (ultimo = 0) el arreglo ya está ordenado.
    """
    limite = len(a) - 1
    while limite > 0:
        ultimo = 0
        for j in range(limite):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                ultimo = j
        limite = ultimo


# =====================================================================
# 2. MERGE SORT
# =====================================================================
def merge_sort(a):
    """Merge Sort top-down con un único buffer auxiliar preasignado.

    Se reserva UNA sola vez un arreglo auxiliar de tamaño n (espacio O(n)) y
    las copias se hacen con memoryview para no crear arreglos temporales.
    """
    n = len(a)
    if n < 2:
        return
    aux = array("d", [0.0]) * n
    ma, maux = memoryview(a), memoryview(aux)
    try:
        _merge_sort(a, aux, ma, maux, 0, n)
    finally:
        ma.release()
        maux.release()


def _merge_sort(a, aux, ma, maux, lo, hi):
    """Ordena a[lo:hi] (intervalo semiabierto)."""
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    _merge_sort(a, aux, ma, maux, lo, mid)
    _merge_sort(a, aux, ma, maux, mid, hi)
    # Mezcla: copiar el bloque a aux y fusionar de regreso en a
    maux[lo:hi] = ma[lo:hi]
    i, j, k = lo, mid, lo
    while i < mid and j < hi:
        if aux[j] < aux[i]:          # '<' estricto => estable
            a[k] = aux[j]
            j += 1
        else:
            a[k] = aux[i]
            i += 1
        k += 1
    if i < mid:                      # resto de la mitad izquierda
        ma[k:hi] = maux[i:mid]
    # el resto de la mitad derecha ya está en su lugar


# =====================================================================
# 3. TREE SORT
# =====================================================================
def tree_sort(a):
    """Tree Sort con un Árbol Binario de Búsqueda (BST).

    Los nodos se guardan en arreglos paralelos (clave, izq, der, cuenta) en
    lugar de objetos, para reducir drásticamente la memoria. Los valores
    repetidos incrementan el contador del nodo en lugar de crear nodos nuevos.
    Inserción iterativa y recorrido in-order iterativo (pila explícita) para
    no depender del límite de recursión.
    """
    n = len(a)
    if n < 2:
        return
    clave = array("d", [a[0]])
    izq = array("i", [-1])
    der = array("i", [-1])
    cuenta = array("q", [1])
    total_nodos = 1

    # --- Construcción del BST ---
    for idx in range(1, n):
        x = a[idx]
        nodo = 0
        while True:
            c = clave[nodo]
            if x < c:
                sig = izq[nodo]
                if sig < 0:
                    izq[nodo] = total_nodos
                    break
                nodo = sig
            elif x > c:
                sig = der[nodo]
                if sig < 0:
                    der[nodo] = total_nodos
                    break
                nodo = sig
            else:                     # valor repetido
                cuenta[nodo] += 1
                x = None
                break
        if x is not None:             # se creó un nodo nuevo
            clave.append(x)
            izq.append(-1)
            der.append(-1)
            cuenta.append(1)
            total_nodos += 1

    # --- Recorrido in-order: escribe los valores ordenados en a ---
    pila = []
    nodo = 0
    k = 0
    while pila or nodo >= 0:
        while nodo >= 0:
            pila.append(nodo)
            nodo = izq[nodo]
        nodo = pila.pop()
        c = clave[nodo]
        for _ in range(cuenta[nodo]):
            a[k] = c
            k += 1
        nodo = der[nodo]


# =====================================================================
# 4. HEAP SORT
# =====================================================================
def _sift_down(a, i, n):
    """Hunde a[i] dentro del max-heap a[0:n]."""
    x = a[i]
    while True:
        hijo = 2 * i + 1
        if hijo >= n:
            break
        if hijo + 1 < n and a[hijo + 1] > a[hijo]:
            hijo += 1
        if a[hijo] <= x:
            break
        a[i] = a[hijo]
        i = hijo
    a[i] = x


def heap_sort(a):
    """Heap Sort in-place: construcción bottom-up del max-heap + extracciones."""
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(a, i, n)
    for fin in range(n - 1, 0, -1):
        a[0], a[fin] = a[fin], a[0]
        _sift_down(a, 0, fin)


# =====================================================================
# 5. COUNTING SORT
# =====================================================================
def counting_sort(a, escala=ESCALA_COUNTING):
    """Counting Sort estable (CLRS) para reales con precisión fija.

    Cada real x se mapea a la clave entera round(x * escala) - clave_min.
    Requiere que los datos tengan a lo más log10(escala) decimales (2 aquí).
    k = rango de claves. Espacio extra: arreglo de conteo O(k) + salida O(n).
    """
    n = len(a)
    if n < 2:
        return
    kmin = round(min(a) * escala)
    k = round(max(a) * escala) - kmin + 1
    cuenta = array("q", [0]) * k

    # 1) Contar ocurrencias de cada clave
    for x in a:
        cuenta[round(x * escala) - kmin] += 1

    # 2) Sumas prefijas -> posición inicial de cada clave en la salida
    total = 0
    for i in range(k):
        c = cuenta[i]
        cuenta[i] = total
        total += c

    # 3) Colocar cada elemento en su posición (recorrido hacia adelante => estable)
    salida = array("d", [0.0]) * n
    for x in a:
        clave = round(x * escala) - kmin
        salida[cuenta[clave]] = x
        cuenta[clave] += 1

    # 4) Copiar la salida de regreso al arreglo original
    memoryview(a)[:] = memoryview(salida)


ALGORITMOS = {
    "bubble": bubble_sort,
    "merge": merge_sort,
    "tree": tree_sort,
    "heap": heap_sort,
    "counting": counting_sort,
}


# =====================================================================
# MODO BENCHMARK (una corrida por proceso)
# =====================================================================
DIR_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


def cargar_dataset(n):
    """Lee el dataset directamente en un array preasignado (readinto), sin
    buffers temporales: así el pico de RSS base no queda inflado y la memoria
    extra del algoritmo se mide correctamente."""
    ruta = os.path.join(DIR_DATOS, f"n_{n}.bin")
    a = array("d", [0.0]) * n
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


def suma_claves(a):
    """Suma entera exacta de round(x*100). No depende del orden: sirve para
    comprobar que el resultado es una permutación de la entrada."""
    return sum(round(x * ESCALA_COUNTING) for x in a)


def esta_ordenado(a):
    return all(map(le, a, islice(a, 1, None)))


def rss_pico_bytes():
    """Pico de memoria residente del proceso (macOS: bytes; Linux: KB)."""
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def correr(algoritmo, n):
    a = cargar_dataset(n)
    suma_antes = suma_claves(a)
    gc.collect()
    mem_base = rss_pico_bytes()

    gc.disable()                      # igual que timeit: evita pausas del GC
    t0 = time.perf_counter_ns()
    ALGORITMOS[algoritmo](a)
    t1 = time.perf_counter_ns()
    gc.enable()

    mem_pico = rss_pico_bytes()
    verificado = len(a) == n and esta_ordenado(a) and suma_claves(a) == suma_antes
    return {
        "lenguaje": "python",
        "algoritmo": algoritmo,
        "n": n,
        "tiempo_s": (t1 - t0) / 1e9,
        "mem_base_mb": mem_base / 2**20,
        "mem_pico_mb": mem_pico / 2**20,
        "mem_extra_mb": (mem_pico - mem_base) / 2**20,
        "verificado": verificado,
    }


def main():
    p = argparse.ArgumentParser(description="Corrida individual de un algoritmo de ordenamiento")
    p.add_argument("--algoritmo", required=True, choices=list(ALGORITMOS))
    p.add_argument("--n", required=True, type=int)
    args = p.parse_args()
    sys.setrecursionlimit(10_000)
    res = correr(args.algoritmo, args.n)
    print("RESULTADO " + json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
