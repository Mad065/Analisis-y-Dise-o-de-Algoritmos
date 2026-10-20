#!/usr/bin/env python3
"""
Generador de datasets compartidos para la Práctica 3 (Divide y Vencerás).

Genera archivos binarios little-endian en `datos/` para que tanto Python como
Java operen exactamente sobre los mismos datos de entrada:

1. Quickselect (Selección de Hoare):
   - Tamaños: n in {1000, 5000, 10000, 50000, 100000, 500000, 1000000, 5000000, 10000000}
   - Valores: enteros en el rango [1, 10^7] distribuidos en permutación
     pseudoaleatoria uniforme (muestreo estratificado sin reemplazo en [1, 10^7]
     seguido de barajado de Fisher-Yates con semilla determinista).
   - `datos/qs32_n_<N>.bin`: codificado en 32 bits con signo (int32, 4 bytes/elem).
   - `datos/qs64_n_<N>.bin`: codificado en 64 bits con signo (int64, 8 bytes/elem),
     conteniendo exactamente la misma permutación numérica que el archivo de 32 bits.

2. Multiplicación de Matrices (Tradicional vs Strassen, 2D vs 1D):
   - Tamaños: matrices cuadradas n x n con n in {16, 32, 64, 128, 256, 512}
   - Valores: enteros pseudoaleatorios en [-100, 100] (evita desbordamiento en int32
     incluso tras sumas/productos de tamaño 512).
   - `datos/mat_n_<N>.bin`: 2 * N * N enteros de 32 bits (int32 little-endian),
     donde los primeros N^2 elementos corresponden a la matriz A y los siguientes
     N^2 elementos a la matriz B en orden por filas (row-major).
"""
import os
import random
import sys
import time
from array import array

SEMILLA_BASE = 2026
RANGO_MAX_QS = 10_000_000
TAMANIOS_QS = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]
TAMANIOS_MAT = [16, 32, 64, 128, 256, 512]
MIN_VAL_MAT = -100
MAX_VAL_MAT = 100

DIR_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


def ruta_qs(bits: int, n: int) -> str:
    return os.path.join(DIR_DATOS, f"qs{bits}_n_{n}.bin")


def ruta_mat(n: int) -> str:
    return os.path.join(DIR_DATOS, f"mat_n_{n}.bin")


def generar_quickselect(n: int) -> None:
    r32 = ruta_qs(32, n)
    r64 = ruta_qs(64, n)
    if (
        os.path.exists(r32)
        and os.path.getsize(r32) == 4 * n
        and os.path.exists(r64)
        and os.path.getsize(r64) == 8 * n
    ):
        print(f"  ✓ qs32/qs64 n={n:>10,} ya existen, se omiten")
        return

    if sys.byteorder != "little":
        raise RuntimeError("Se requiere arquitectura little-endian")

    t0 = time.perf_counter()
    rng = random.Random(SEMILLA_BASE + n)

    # Generación de n enteros distintos en [1, 10^7] cubriendo todo el rango
    # mediante partición estratificada exacta (todos los n dividen a 10^7)
    # seguida de una permutación pseudoaleatoria de Fisher-Yates.
    if n == RANGO_MAX_QS:
        valores = list(range(1, RANGO_MAX_QS + 1))
    else:
        paso = RANGO_MAX_QS // n
        valores = [i * paso + rng.randrange(1, paso + 1) for i in range(n)]

    rng.shuffle(valores)

    arr32 = array("i", valores)
    arr64 = array("q", valores)
    assert arr32.itemsize == 4, "array('i') debe ser de 4 bytes (32 bits)"
    assert arr64.itemsize == 8, "array('q') debe ser de 8 bytes (64 bits)"

    with open(r32, "wb") as f32:
        arr32.tofile(f32)
    with open(r64, "wb") as f64:
        arr64.tofile(f64)

    dt = time.perf_counter() - t0
    mb32 = (4 * n) / (1024 * 1024)
    mb64 = (8 * n) / (1024 * 1024)
    print(f"  ✓ qs32 ({mb32:5.2f} MB) y qs64 ({mb64:5.2f} MB) para n={n:>10,} en {dt:.2f} s")


def generar_matrices(n: int) -> None:
    ruta = ruta_mat(n)
    total_enteros = 2 * n * n
    if os.path.exists(ruta) and os.path.getsize(ruta) == 4 * total_enteros:
        print(f"  ✓ mat_n_{n}.bin ya existe, se omite")
        return

    if sys.byteorder != "little":
        raise RuntimeError("Se requiere arquitectura little-endian")

    t0 = time.perf_counter()
    rng = random.Random(SEMILLA_BASE + 1000 + n)
    datos = array("i", (rng.randint(MIN_VAL_MAT, MAX_VAL_MAT) for _ in range(total_enteros)))
    with open(ruta, "wb") as f:
        datos.tofile(f)

    dt = time.perf_counter() - t0
    kb = (4 * total_enteros) / 1024
    print(f"  ✓ mat_n_{n}.bin ({n}x{n}, {kb:7.1f} KB) en {dt:.3f} s")


def main() -> None:
    os.makedirs(DIR_DATOS, exist_ok=True)
    print("Generando datasets de Quickselect (32 bits y 64 bits)...")
    for n in TAMANIOS_QS:
        generar_quickselect(n)

    print("\nGenerando datasets de Matrices Cuadradas (A y B)...")
    for n in TAMANIOS_MAT:
        generar_matrices(n)

    print("\n✅ Todos los datasets fueron generados correctamente.")


if __name__ == "__main__":
    main()
