#!/usr/bin/env python3
"""
Práctica 5 — Programación Dinámica
Escuela Superior de Cómputo (ESCOM - IPN)
Materia: Análisis y Diseño de Algoritmos

Implementación canónica en Python puro de cuatro problemas fundamentales:
  1. Problema de la Mochila 0/1 (0/1 Knapsack)
  2. Problema del Cambio de Monedas (Coin Change - Mínimas Monedas)
  3. Subsecuencia Común Más Larga (LCSq - Longest Common Subsequence)
  4. Subcadena Común Más Larga (LCS - Longest Common Substring)

Para cada problema se implementan tres versiones:
  a) Recursividad ingenua (Naive Recursion)
  b) Memoización (Top-down DP)
  c) Tabulación (Bottom-up DP con reconstrucción de solución óptima)

Adicionalmente, se incluye la heurística voraz para el problema del cambio
con el fin de contrastar experimental y formalmente la optimalidad de DP.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# =====================================================================
# ESTRUCTURAS DE RETORNO Y MÉTRICAS
# =====================================================================
@dataclass
class ResultadoDP:
    """Contenedor de resultados algorítmicos con métricas de ejecución."""
    problema: str
    variante: str
    valor_optimo: int
    solucion_reconstruida: Any = None
    llamadas_recursivas: int = 0
    subproblemas_evaluados: int = 0
    tamanio_tabla: int = 0


# =====================================================================
# PROBLEMA 1: MOCHILA 0/1 (0/1 KNAPSACK)
# =====================================================================

def mochila_recursiva(
    pesos: List[int],
    valores: List[int],
    capacidad: int
) -> ResultadoDP:
    """
    Resuelve la Mochila 0/1 mediante recursividad ingenua.
    Complejidad temporal: O(2^n)
    Complejidad espacial: O(n) en pila de llamadas.
    """
    n = len(pesos)
    llamadas = 0

    def _rec(i: int, cap_restante: int) -> int:
        nonlocal llamadas
        llamadas += 1
        if i == 0 or cap_restante <= 0:
            return 0
        
        peso_actual = pesos[i - 1]
        val_actual = valores[i - 1]

        if peso_actual > cap_restante:
            return _rec(i - 1, cap_restante)
        else:
            excluir = _rec(i - 1, cap_restante)
            incluir = val_actual + _rec(i - 1, cap_restante - peso_actual)
            return max(excluir, incluir)

    val_max = _rec(n, capacidad)
    return ResultadoDP(
        problema="Mochila 0/1",
        variante="Recursiva Ingenua",
        valor_optimo=val_max,
        llamadas_recursivas=llamadas,
        subproblemas_evaluados=llamadas
    )


def mochila_memo(
    pesos: List[int],
    valores: List[int],
    capacidad: int
) -> ResultadoDP:
    """
    Resuelve la Mochila 0/1 mediante Memoización (Top-down).
    Complejidad temporal: O(n * W)
    Complejidad espacial: O(n * W) en memoria + O(n) en pila.
    """
    n = len(pesos)
    memo: Dict[Tuple[int, int], int] = {}
    llamadas = 0

    def _rec(i: int, cap_restante: int) -> int:
        nonlocal llamadas
        llamadas += 1
        if i == 0 or cap_restante <= 0:
            return 0

        estado = (i, cap_restante)
        if estado in memo:
            return memo[estado]

        peso_actual = pesos[i - 1]
        val_actual = valores[i - 1]

        if peso_actual > cap_restante:
            res = _rec(i - 1, cap_restante)
        else:
            excluir = _rec(i - 1, cap_restante)
            incluir = val_actual + _rec(i - 1, cap_restante - peso_actual)
            res = max(excluir, incluir)

        memo[estado] = res
        return res

    val_max = _rec(n, capacidad)
    return ResultadoDP(
        problema="Mochila 0/1",
        variante="Memoización",
        valor_optimo=val_max,
        llamadas_recursivas=llamadas,
        subproblemas_evaluados=len(memo),
        tamanio_tabla=len(memo)
    )


def mochila_tabulacion(
    pesos: List[int],
    valores: List[int],
    capacidad: int
) -> ResultadoDP:
    """
    Resuelve la Mochila 0/1 mediante Tabulación (Bottom-up).
    Incluye reconstrucción del conjunto óptimo de elementos seleccionados.
    Complejidad temporal: O(n * W)
    Complejidad espacial: O(n * W)
    """
    n = len(pesos)
    # dp[i][c] = valor máximo considerando los primeros i elementos y capacidad c
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        peso_actual = pesos[i - 1]
        val_actual = valores[i - 1]
        for c in range(capacidad + 1):
            if peso_actual > c:
                dp[i][c] = dp[i - 1][c]
            else:
                dp[i][c] = max(dp[i - 1][c], val_actual + dp[i - 1][c - peso_actual])

    val_max = dp[n][capacidad]

    # Reconstrucción de la solución óptima
    items_seleccionados: List[int] = []
    c_actual = capacidad
    for i in range(n, 0, -1):
        if dp[i][c_actual] != dp[i - 1][c_actual]:
            idx_item = i - 1
            items_seleccionados.append(idx_item)
            c_actual -= pesos[idx_item]
    items_seleccionados.reverse()

    return ResultadoDP(
        problema="Mochila 0/1",
        variante="Tabulación",
        valor_optimo=val_max,
        solucion_reconstruida=items_seleccionados,
        subproblemas_evaluados=(n + 1) * (capacidad + 1),
        tamanio_tabla=(n + 1) * (capacidad + 1)
    )


# =====================================================================
# PROBLEMA 2: CAMBIO DE MONEDAS (COIN CHANGE - MÍNIMAS MONEDAS)
# =====================================================================

def cambio_recursivo(
    monedas: List[int],
    monto: int
) -> ResultadoDP:
    """
    Halla el mínimo número de monedas para alcanzar el monto mediante recursividad ingenua.
    Retorna math.inf (o -1 en representación entera) si el monto es inalcanzable.
    Complejidad temporal: O(k^monto)
    Complejidad espacial: O(monto) en pila de llamadas.
    """
    llamadas = 0

    def _rec(m: int) -> float:
        nonlocal llamadas
        llamadas += 1
        if m == 0:
            return 0
        if m < 0:
            return math.inf

        min_monedas = math.inf
        for c in monedas:
            res = _rec(m - c)
            if res != math.inf:
                min_monedas = min(min_monedas, 1 + res)
        return min_monedas

    res = _rec(monto)
    val_optimo = int(res) if res != math.inf else -1

    return ResultadoDP(
        problema="Cambio de Monedas",
        variante="Recursiva Ingenua",
        valor_optimo=val_optimo,
        llamadas_recursivas=llamadas,
        subproblemas_evaluados=llamadas
    )


def cambio_memo(
    monedas: List[int],
    monto: int
) -> ResultadoDP:
    """
    Halla el mínimo número de monedas mediante Memoización (Top-down).
    Complejidad temporal: O(k * monto)
    Complejidad espacial: O(monto) en memoria + O(monto) en pila.
    """
    memo: Dict[int, float] = {}
    llamadas = 0

    def _rec(m: int) -> float:
        nonlocal llamadas
        llamadas += 1
        if m == 0:
            return 0
        if m < 0:
            return math.inf

        if m in memo:
            return memo[m]

        min_monedas = math.inf
        for c in monedas:
            res = _rec(m - c)
            if res != math.inf:
                min_monedas = min(min_monedas, 1 + res)

        memo[m] = min_monedas
        return min_monedas

    res = _rec(monto)
    val_optimo = int(res) if res != math.inf else -1

    return ResultadoDP(
        problema="Cambio de Monedas",
        variante="Memoización",
        valor_optimo=val_optimo,
        llamadas_recursivas=llamadas,
        subproblemas_evaluados=len(memo),
        tamanio_tabla=len(memo)
    )


def cambio_tabulacion(
    monedas: List[int],
    monto: int
) -> ResultadoDP:
    """
    Halla el mínimo número de monedas mediante Tabulación (Bottom-up).
    Incluye reconstrucción del conjunto exacto de monedas utilizadas.
    Complejidad temporal: O(k * monto)
    Complejidad espacial: O(monto)
    """
    # dp[v] = cantidad mínima de monedas para sumar v
    dp = [float("inf")] * (monto + 1)
    dp[0] = 0.0

    # padre[v] = última moneda utilizada para formar el monto v
    padre = [-1] * (monto + 1)

    for v in range(1, monto + 1):
        for c in monedas:
            if v >= c and dp[v - c] + 1 < dp[v]:
                dp[v] = dp[v - c] + 1
                padre[v] = c

    if dp[monto] == float("inf"):
        val_optimo = -1
        monedas_usadas: List[int] = []
    else:
        val_optimo = int(dp[monto])
        monedas_usadas = []
        curr = monto
        while curr > 0:
            coin = padre[curr]
            monedas_usadas.append(coin)
            curr -= coin

    return ResultadoDP(
        problema="Cambio de Monedas",
        variante="Tabulación",
        valor_optimo=val_optimo,
        solucion_reconstruida=monedas_usadas,
        subproblemas_evaluados=monto + 1,
        tamanio_tabla=monto + 1
    )


def cambio_voraz(
    monedas: List[int],
    monto: int
) -> ResultadoDP:
    """
    Aproximación voraz (Greedy) para cambio de monedas:
    Selecciona repetidamente la moneda de mayor denominación disponible.
    Sirve para contrastar casos donde la estrategia voraz falla (no canónica).
    """
    ordenadas = sorted(monedas, reverse=True)
    curr = monto
    monedas_usadas: List[int] = []

    for c in ordenadas:
        while curr >= c:
            monedas_usadas.append(c)
            curr -= c

    val_optimo = len(monedas_usadas) if curr == 0 else -1

    return ResultadoDP(
        problema="Cambio de Monedas",
        variante="Voraz (Greedy)",
        valor_optimo=val_optimo,
        solucion_reconstruida=monedas_usadas,
        subproblemas_evaluados=len(ordenadas)
    )


# =====================================================================
# PROBLEMA 3: SUBSECUENCIA COMÚN MÁS LARGA (LCSq)
# =====================================================================

def lcsq_recursiva(s1: str, s2: str) -> ResultadoDP:
    """
    Calcula la longitud de la subsecuencia común más larga mediante recursividad ingenua.
    Complejidad temporal: O(2^(m + n))
    Complejidad espacial: O(m + n) en pila de llamadas.
    """
    m, n = len(s1), len(s2)
    llamadas = 0

    def _rec(i: int, j: int) -> int:
        nonlocal llamadas
        llamadas += 1
        if i == 0 or j == 0:
            return 0

        if s1[i - 1] == s2[j - 1]:
            return 1 + _rec(i - 1, j - 1)
        else:
            return max(_rec(i - 1, j), _rec(i, j - 1))

    val_max = _rec(m, n)
    return ResultadoDP(
        problema="Subsecuencia Común Más Larga (LCSq)",
        variante="Recursiva Ingenua",
        valor_optimo=val_max,
        llamadas_recursivas=llamadas,
        subproblemas_evaluados=llamadas
    )


def lcsq_memo(s1: str, s2: str) -> ResultadoDP:
    """
    Calcula la longitud de la subsecuencia común más larga mediante Memoización (Top-down).
    Complejidad temporal: O(m * n)
    Complejidad espacial: O(m * n) en memoria + O(m + n) en pila.
    """
    m, n = len(s1), len(s2)
    memo: Dict[Tuple[int, int], int] = {}
    llamadas = 0

    def _rec(i: int, j: int) -> int:
        nonlocal llamadas
        llamadas += 1
        if i == 0 or j == 0:
            return 0

        estado = (i, j)
        if estado in memo:
            return memo[estado]

        if s1[i - 1] == s2[j - 1]:
            res = 1 + _rec(i - 1, j - 1)
        else:
            res = max(_rec(i - 1, j), _rec(i, j - 1))

        memo[estado] = res
        return res

    val_max = _rec(m, n)
    return ResultadoDP(
        problema="Subsecuencia Común Más Larga (LCSq)",
        variante="Memoización",
        valor_optimo=val_max,
        llamadas_recursivas=llamadas,
        subproblemas_evaluados=len(memo),
        tamanio_tabla=len(memo)
    )


def lcsq_tabulacion(s1: str, s2: str) -> ResultadoDP:
    """
    Calcula la LCSq mediante Tabulación (Bottom-up).
    Incluye reconstrucción de la cadena subsecuencia óptima.
    Complejidad temporal: O(m * n)
    Complejidad espacial: O(m * n)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    val_max = dp[m][n]

    # Reconstrucción de la subsecuencia
    caracteres: List[str] = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            caracteres.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    caracteres.reverse()
    subsecuencia = "".join(caracteres)

    return ResultadoDP(
        problema="Subsecuencia Común Más Larga (LCSq)",
        variante="Tabulación",
        valor_optimo=val_max,
        solucion_reconstruida=subsecuencia,
        subproblemas_evaluados=(m + 1) * (n + 1),
        tamanio_tabla=(m + 1) * (n + 1)
    )


# =====================================================================
# PROBLEMA 4: SUBCADENA COMÚN MÁS LARGA (LCS - LONGEST COMMON SUBSTRING)
# =====================================================================

def lcs_subcadena_recursiva(s1: str, s2: str) -> ResultadoDP:
    """
    Calcula la longitud de la subcadena común más larga mediante recursión ingenua.
    Explora ramificaciones recursivas evaluando sufijos comunes y reinicios.
    Complejidad temporal: O(3^(m + n))
    Complejidad espacial: O(m + n) en pila de llamadas.
    """
    m, n = len(s1), len(s2)
    llamadas = 0

    def _rec(i: int, j: int, longitud_actual: int) -> int:
        nonlocal llamadas
        llamadas += 1
        if i == 0 or j == 0:
            return longitud_actual

        c1 = longitud_actual
        if s1[i - 1] == s2[j - 1]:
            c1 = _rec(i - 1, j - 1, longitud_actual + 1)

        c2 = _rec(i - 1, j, 0)
        c3 = _rec(i, j - 1, 0)

        return max(longitud_actual, c1, c2, c3)

    val_max = _rec(m, n, 0) if (m > 0 and n > 0) else 0

    return ResultadoDP(
        problema="Subcadena Común Más Larga (LCS)",
        variante="Recursiva Ingenua",
        valor_optimo=val_max,
        llamadas_recursivas=llamadas,
        subproblemas_evaluados=llamadas
    )


def lcs_subcadena_memo(s1: str, s2: str) -> ResultadoDP:
    """
    Calcula la longitud de la subcadena común más larga mediante Memoización (Top-down).
    Memoiza la longitud del sufijo común más largo que finaliza exactamente en (i, j),
    maximizando sobre todos los pares (i, j).
    Complejidad temporal: O(m * n)
    Complejidad espacial: O(m * n) en memoria + O(min(m, n)) en pila.
    """
    m, n = len(s1), len(s2)
    memo: Dict[Tuple[int, int], int] = {}
    llamadas = 0

    def _sufijo_comun(i: int, j: int) -> int:
        nonlocal llamadas
        llamadas += 1
        if i == 0 or j == 0:
            return 0

        estado = (i, j)
        if estado in memo:
            return memo[estado]

        if s1[i - 1] == s2[j - 1]:
            res = 1 + _sufijo_comun(i - 1, j - 1)
        else:
            res = 0

        memo[estado] = res
        return res

    max_global = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            val = _sufijo_comun(i, j)
            if val > max_global:
                max_global = val

    return ResultadoDP(
        problema="Subcadena Común Más Larga (LCS)",
        variante="Memoización",
        valor_optimo=max_global,
        llamadas_recursivas=llamadas,
        subproblemas_evaluados=len(memo),
        tamanio_tabla=len(memo)
    )


def lcs_subcadena_tabulacion(s1: str, s2: str) -> ResultadoDP:
    """
    Calcula la subcadena común más larga mediante Tabulación (Bottom-up).
    Incluye reconstrucción de la subcadena contigua óptima.
    Complejidad temporal: O(m * n)
    Complejidad espacial: O(m * n)
    """
    m, n = len(s1), len(s2)
    # dp[i][j] = longitud del sufijo común más largo de s1[0..i-1] y s2[0..j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    max_len = 0
    fin_s1 = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    fin_s1 = i
            else:
                dp[i][j] = 0

    subcadena = s1[fin_s1 - max_len : fin_s1] if max_len > 0 else ""

    return ResultadoDP(
        problema="Subcadena Común Más Larga (LCS)",
        variante="Tabulación",
        valor_optimo=max_len,
        solucion_reconstruida=subcadena,
        subproblemas_evaluados=(m + 1) * (n + 1),
        tamanio_tabla=(m + 1) * (n + 1)
    )


# =====================================================================
# INTERFAZ DE LÍNEA DE COMANDOS (CLI)
# =====================================================================
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Práctica 5: Programación Dinámica (Mochila, Cambio, LCSq, LCS)"
    )
    parser.add_argument(
        "--problema",
        choices=["mochila", "cambio", "lcsq", "subcadena"],
        required=True,
        help="Problema a resolver"
    )
    parser.add_argument(
        "--variante",
        choices=["recursiva", "memo", "tabulacion", "voraz"],
        default="tabulacion",
        help="Estrategia algorítmica"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprime el resultado en formato JSON"
    )
    parser.add_argument("--pesos", type=int, nargs="+", help="Pesos para la mochila")
    parser.add_argument("--valores", type=int, nargs="+", help="Valores para la mochila")
    parser.add_argument("--capacidad", type=int, help="Capacidad máxima de la mochila")
    parser.add_argument("--monedas", type=int, nargs="+", help="Denominaciones de monedas")
    parser.add_argument("--monto", type=int, help="Monto objetivo para el cambio")
    parser.add_argument("--s1", type=str, help="Primera cadena para LCSq/Subcadena")
    parser.add_argument("--s2", type=str, help="Segunda cadena para LCSq/Subcadena")

    args = parser.parse_args()

    res: Optional[ResultadoDP] = None

    if args.problema == "mochila":
        pesos = args.pesos or [2, 3, 4, 5]
        valores = args.valores or [3, 4, 5, 8]
        capacidad = args.capacidad if args.capacidad is not None else 8
        if args.variante == "recursiva":
            res = mochila_recursiva(pesos, valores, capacidad)
        elif args.variante == "memo":
            res = mochila_memo(pesos, valores, capacidad)
        else:
            res = mochila_tabulacion(pesos, valores, capacidad)

    elif args.problema == "cambio":
        monedas = args.monedas or [1, 3, 4]
        monto = args.monto if args.monto is not None else 6
        if args.variante == "recursiva":
            res = cambio_recursivo(monedas, monto)
        elif args.variante == "memo":
            res = cambio_memo(monedas, monto)
        elif args.variante == "voraz":
            res = cambio_voraz(monedas, monto)
        else:
            res = cambio_tabulacion(monedas, monto)

    elif args.problema == "lcsq":
        s1 = args.s1 or "ABCBDAB"
        s2 = args.s2 or "BDCABA"
        if args.variante == "recursiva":
            res = lcsq_recursiva(s1, s2)
        elif args.variante == "memo":
            res = lcsq_memo(s1, s2)
        else:
            res = lcsq_tabulacion(s1, s2)

    elif args.problema == "subcadena":
        s1 = args.s1 or "ESCOM_ALGORITMOS"
        s2 = args.s2 or "AVANZADO_ALGORITMOS_ESCOM"
        if args.variante == "recursiva":
            res = lcs_subcadena_recursiva(s1, s2)
        elif args.variante == "memo":
            res = lcs_subcadena_memo(s1, s2)
        else:
            res = lcs_subcadena_tabulacion(s1, s2)

    if res:
        if args.json:
            print(json.dumps({
                "problema": res.problema,
                "variante": res.variante,
                "valor_optimo": res.valor_optimo,
                "solucion": res.solucion_reconstruida,
                "llamadas": res.llamadas_recursivas,
                "subproblemas": res.subproblemas_evaluados,
                "tamanio_tabla": res.tamanio_tabla
            }, indent=2))
        else:
            print(f"[{res.problema}] Variante: {res.variante}")
            print(f"  Valor óptimo: {res.valor_optimo}")
            if res.solucion_reconstruida is not None:
                print(f"  Solución reconstruida: {res.solucion_reconstruida}")
            print(f"  Llamadas recursivas: {res.llamadas_recursivas}")
            print(f"  Subproblemas evaluados: {res.subproblemas_evaluados}")


if __name__ == "__main__":
    main()
