#!/usr/bin/env python3
"""
Generador de datasets para la Práctica 2 (Algoritmos de Ordenamiento).

Cada dataset es un archivo binario `datos/n_<N>.bin` con N números reales
codificados como float64 little-endian. Python y Java leen EXACTAMENTE el mismo
archivo, por lo que ambos lenguajes ordenan los mismos datos.

Los valores son reales con 2 decimales fijos en el rango [0, 10 000):
    x = randrange(0, 1_000_000) / 100
Esto permite aplicar Counting Sort sobre reales mediante la clave entera
round(x * 100), con un arreglo de conteo de k = 1 000 000 casillas.

Uso:
    python generar_datos.py                 # genera 10^5 .. 10^8
    python generar_datos.py 100000 1000000  # genera solo los tamaños indicados
"""
import os
import random
import sys
import time
from array import array

SEMILLA = 42
RANGO_CLAVES = 1_000_000          # claves enteras en [0, 1 000 000)
ESCALA = 100                      # 2 decimales
BLOQUE = 1_000_000                # elementos escritos por bloque
TAMANIOS = [100_000, 1_000_000, 10_000_000, 100_000_000]
# 10^9 NO se genera: 8 GB en disco y no cabe en la RAM (8 GB) del equipo.

DIR_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


def ruta_dataset(n: int) -> str:
    return os.path.join(DIR_DATOS, f"n_{n}.bin")


def generar(n: int) -> None:
    ruta = ruta_dataset(n)
    if os.path.exists(ruta) and os.path.getsize(ruta) == 8 * n:
        print(f"  ✓ {os.path.basename(ruta)} ya existe, se omite")
        return
    rng = random.Random(SEMILLA + n)   # semilla distinta (pero fija) por tamaño
    t0 = time.perf_counter()
    if sys.byteorder != "little":
        raise RuntimeError("Se esperaba una arquitectura little-endian")
    with open(ruta, "wb") as f:
        restantes = n
        while restantes > 0:
            m = min(BLOQUE, restantes)
            bloque = array("d", (rng.randrange(RANGO_CLAVES) / ESCALA for _ in range(m)))
            bloque.tofile(f)
            restantes -= m
    print(f"  ✓ {os.path.basename(ruta)} ({8 * n / 2**20:,.1f} MB) en {time.perf_counter() - t0:.1f} s")


def main() -> None:
    os.makedirs(DIR_DATOS, exist_ok=True)
    tamanios = [int(a) for a in sys.argv[1:]] or TAMANIOS
    print("Generando datasets...")
    for n in tamanios:
        generar(n)


if __name__ == "__main__":
    main()
