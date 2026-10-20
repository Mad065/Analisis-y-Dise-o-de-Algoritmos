#!/usr/bin/env python3
"""
Orquestador del benchmark de la Práctica 3 (Divide y Vencerás).

Ejecuta de manera aislada (un subproceso por corrida, midiendo RSS pico real
mediante `os.wait4`) los dos experimentos de la práctica en Python y Java:

1. Quickselect (Selección de Hoare):
   - n in {1000, 5000, 10000, 50000, 100000, 500000, 1000000, 5000000, 10000000}
   - Datasets de 32 bits (int32) y 64 bits (int64) en permutación pseudoaleatoria [1, 10^7].
   - Posición buscada: mediana k = floor(n/2) + 1.

2. Multiplicación de Matrices Cuadradas (Tradicional vs Strassen, 2D vs 1D Contiguo):
   - n in {16, 32, 64, 128, 256, 512}
   - Variantes: tradicional_2d, tradicional_1d, strassen_2d, strassen_1d.

3. Prueba de Estrés de Recursos (Evidencia de agotamiento de memoria/cómputo en Strassen):
   - Ejecuta Strassen con restricción de heap / extrapolación a n >= 1024 para
     capturar y documentar el desbordamiento de memoria (`OutOfMemoryError`) y
     la explosión combinatoria de $7^{\\log_2 n}$ llamadas recursivas.

Uso:
    python3 benchmark.py                # benchmark completo
    python3 benchmark.py --reanudar     # continúa donde se quedó
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import os
import platform
import statistics
import subprocess
import sys
import time

DIR = os.path.dirname(os.path.abspath(__file__))
DIR_RES = os.path.join(DIR, "resultados")
DIR_LOGS = os.path.join(DIR_RES, "logs")

TAMANIOS_QS = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]
BITS_QS = [32, 64]

TAMANIOS_MAT = [16, 32, 64, 128, 256, 512]
VARIANTES_MAT = ["tradicional_2d", "tradicional_1d", "strassen_2d", "strassen_1d"]

LENGUAJES = ["java", "python"]

LIMITE_S = 15 * 60
REPETIR_SI_MENOR_A_S = 2.0
REPETICIONES = 3
FRACCION_RAM = 0.75
def _resolver_java() -> str:
    candidatos = [
        os.environ.get("JAVA_BIN", ""),
        "/Users/mad0/Applications/IntelliJ IDEA.app/Contents/jbr/Contents/Home/bin/java",
        "/Applications/DBeaver.app/Contents/Eclipse/jre/Contents/Home/bin/java",
        "/opt/homebrew/opt/openjdk@21/bin/java",
        "java",
    ]
    for c in candidatos:
        if c and os.path.exists(c):
            return c
    return "java"


JAVA = _resolver_java()
JAVA_XMX = "6g"
MB = 2**20


def ram_fisica() -> int:
    return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")


def version_java() -> str:
    try:
        out = subprocess.run([JAVA, "-version"], capture_output=True, text=True).stderr
        return out.splitlines()[0]
    except Exception:
        return "desconocida"


def cpu_brand() -> str:
    try:
        return subprocess.run(
            ["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True
        ).stdout.strip()
    except Exception:
        return platform.processor()


def metadatos(limite: float) -> dict:
    return {
        "fecha": datetime.datetime.now().isoformat(timespec="seconds"),
        "cpu": cpu_brand(),
        "nucleos": os.cpu_count(),
        "ram_gb": round(ram_fisica() / 2**30, 1),
        "so": platform.platform(),
        "python": platform.python_version(),
        "java": version_java(),
        "java_flags": f"-Xmx{JAVA_XMX}",
        "limite_s": limite,
    }


def comando_qs(lenguaje: str, bits: int, n: int) -> list[str]:
    if lenguaje == "python":
        return [
            sys.executable,
            os.path.join(DIR, "divide_venceras.py"),
            "--problema",
            "quickselect",
            "--bits",
            str(bits),
            "--n",
            str(n),
        ]
    return [
        JAVA,
        f"-Xmx{JAVA_XMX}",
        "-cp",
        DIR,
        "DivideVenceras",
        "--problema",
        "quickselect",
        "--bits",
        str(bits),
        "--n",
        str(n),
    ]


def comando_mat(lenguaje: str, variante: str, n: int) -> list[str]:
    if lenguaje == "python":
        return [
            sys.executable,
            os.path.join(DIR, "divide_venceras.py"),
            "--problema",
            "matrices",
            "--variante",
            variante,
            "--n",
            str(n),
        ]
    return [
        JAVA,
        f"-Xmx{JAVA_XMX}",
        "-cp",
        DIR,
        "DivideVenceras",
        "--problema",
        "matrices",
        "--variante",
        variante,
        "--n",
        str(n),
    ]


def ejecutar_subproceso(cmd: list[str], nombre_log: str, limite: float) -> dict:
    os.makedirs(DIR_LOGS, exist_ok=True)
    ruta_log = os.path.join(DIR_LOGS, nombre_log)
    with open(ruta_log, "w") as log:
        p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=DIR)
        t0 = time.monotonic()
        espera = 0.005
        timeout = False
        while True:
            pid, status, uso = os.wait4(p.pid, os.WNOHANG)
            if pid != 0:
                break
            if time.monotonic() - t0 > limite:
                p.kill()
                pid, status, uso = os.wait4(p.pid, 0)
                timeout = True
                break
            time.sleep(espera)
            espera = min(espera * 1.5, 0.25)
        p.returncode = os.waitstatus_to_exitcode(status)
    pared_s = time.monotonic() - t0
    rss = uso.ru_maxrss if sys.platform == "darwin" else uso.ru_maxrss * 1024

    if timeout:
        return {"estado": "timeout", "pared_s": pared_s, "rss_pico_mb": rss / MB}

    resultado = None
    with open(ruta_log) as log:
        for linea in log:
            if linea.startswith("RESULTADO "):
                resultado = json.loads(linea[len("RESULTADO ") :])
    if p.returncode != 0 or resultado is None:
        return {
            "estado": "error",
            "codigo": p.returncode,
            "rss_pico_mb": rss / MB,
            "log": os.path.relpath(ruta_log, DIR),
        }
    resultado.update(estado="ok", rss_pico_mb=rss / MB, pared_s=pared_s, estimado=False)
    return resultado


def ejecutar_con_repeticiones(cmd_fn, prefijo_log: str, limite: float) -> dict:
    r1 = ejecutar_subproceso(cmd_fn(), f"{prefijo_log}_r1.log", limite)
    if r1["estado"] != "ok":
        return r1
    reps = [r1]
    if r1["tiempo_s"] < REPETIR_SI_MENOR_A_S:
        for i in range(2, REPETICIONES + 1):
            ri = ejecutar_subproceso(cmd_fn(), f"{prefijo_log}_r{i}.log", limite)
            if ri["estado"] == "ok":
                reps.append(ri)
    reps.sort(key=lambda x: x["tiempo_s"])
    mediana = dict(reps[len(reps) // 2])
    mediana["tiempos_s"] = [x["tiempo_s"] for x in reps]
    mediana["tiempo_s"] = statistics.median(mediana["tiempos_s"])
    mediana["rss_pico_mb"] = statistics.median(x["rss_pico_mb"] for x in reps)
    mediana["verificado"] = all(x["verificado"] for x in reps)
    return mediana


def ejecutar_prueba_estres() -> dict:
    """Ejecuta una prueba controlada de agotamiento de recursos en Strassen
    para documentar el comportamiento cuando el árbol recursivo 7^k agota el heap
    o el presupuesto de cómputo."""
    os.makedirs(DIR_LOGS, exist_ok=True)
    ruta_log = os.path.join(DIR_LOGS, "estres_strassen_oom.log")
    cmd = [
        JAVA,
        "-Xmx6m",
        "-XX:+UseSerialGC",
        "-cp",
        DIR,
        "DivideVenceras",
        "--problema",
        "matrices",
        "--variante",
        "strassen_2d",
        "--n",
        "512",
    ]
    t0 = time.monotonic()
    proc = subprocess.run(cmd, cwd=DIR, capture_output=True, text=True, timeout=30)
    dt = time.monotonic() - t0
    salida = (proc.stdout + "\n" + proc.stderr).strip()
    with open(ruta_log, "w") as f:
        f.write(f"$ {' '.join(cmd)}\n")
        f.write(salida + "\n")
    return {
        "comando": "java -Xmx6m -XX:+UseSerialGC DivideVenceras --problema matrices --variante strassen_2d --n 512",
        "codigo_salida": proc.returncode,
        "tiempo_s": round(dt, 4),
        "salida": salida,
        "log": os.path.relpath(ruta_log, DIR),
    }


def guardar(datos: dict, ruta: str) -> None:
    tmp = ruta + ".tmp"
    with open(tmp, "w") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    os.replace(tmp, ruta)


def exportar_csv(datos: dict, ruta_qs: str, ruta_mat: str) -> None:
    cols_qs = [
        "lenguaje",
        "bits",
        "n",
        "k",
        "resultado",
        "estado",
        "tiempo_s",
        "mem_datos_mb",
        "rss_pico_mb",
        "mem_extra_mb",
        "verificado",
    ]
    with open(ruta_qs, "w") as f:
        f.write(",".join(cols_qs) + "\n")
        for c in sorted(
            datos["quickselect"], key=lambda x: (x["lenguaje"], x["bits"], x["n"])
        ):
            f.write(",".join(str(c.get(col, "")) for col in cols_qs) + "\n")

    cols_mat = [
        "lenguaje",
        "variante",
        "algoritmo",
        "representacion",
        "n",
        "estado",
        "tiempo_s",
        "mem_datos_mb",
        "rss_pico_mb",
        "mem_extra_mb",
        "mem_acumulada_mb",
        "verificado",
    ]
    with open(ruta_mat, "w") as f:
        f.write(",".join(cols_mat) + "\n")
        for c in sorted(
            datos["matrices"],
            key=lambda x: (x["lenguaje"], VARIANTES_MAT.index(x["variante"]), x["n"]),
        ):
            f.write(",".join(str(c.get(col, "")) for col in cols_mat) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reanudar", action="store_true")
    ap.add_argument("--limite", type=float, default=LIMITE_S)
    ap.add_argument("--salida", default=os.path.join(DIR_RES, "resultados.json"))
    args = ap.parse_args()
    os.makedirs(DIR_RES, exist_ok=True)

    datos = None
    if args.reanudar and os.path.exists(args.salida):
        with open(args.salida) as f:
            datos = json.load(f)
    if datos is None:
        datos = {
            "meta": metadatos(args.limite),
            "quickselect": [],
            "matrices": [],
            "estres": {},
        }

    hechos_qs = {(c["lenguaje"], c["bits"], c["n"]) for c in datos["quickselect"]}
    hechos_mat = {(c["lenguaje"], c["variante"], c["n"]) for c in datos["matrices"]}

    print("=" * 78)
    print("PARTE 1: BENCHMARK QUICKSELECT (SELECCIÓN DE HOARE) — 32 BITS vs 64 BITS")
    print("=" * 78)
    for n in TAMANIOS_QS:
        for lang in LENGUAJES:
            for bits in BITS_QS:
                clave = (lang, bits, n)
                if clave in hechos_qs:
                    continue
                etiqueta = f"[{lang:6}] Quickselect {bits}-bit  n={n:>10,}"
                print(f"{etiqueta} ... ejecutando", flush=True)
                reg = ejecutar_con_repeticiones(
                    lambda l=lang, b=bits, tam=n: comando_qs(l, b, tam),
                    f"qs_{lang}_{bits}b_{n}",
                    args.limite,
                )
                if reg["estado"] == "ok":
                    print(
                        f"{etiqueta}  {reg['tiempo_s']*1e3:9.3f} ms  "
                        f"Datos {reg['mem_datos_mb']:6.2f} MB  "
                        f"RSS {reg['rss_pico_mb']:7.2f} MB  "
                        f"k={reg['k']:,} -> {reg['resultado']:,}  "
                        f"ok={reg['verificado']}",
                        flush=True,
                    )
                else:
                    print(f"{etiqueta}  {reg['estado'].upper()}", flush=True)
                datos["quickselect"].append(reg)
                hechos_qs.add(clave)
                guardar(datos, args.salida)

    print("\n" + "=" * 78)
    print("PARTE 2: BENCHMARK MULTIPLICACIÓN DE MATRICES (TRADICIONAL vs STRASSEN, 2D vs 1D)")
    print("=" * 78)
    for n in TAMANIOS_MAT:
        for lang in LENGUAJES:
            for var in VARIANTES_MAT:
                clave = (lang, var, n)
                if clave in hechos_mat:
                    continue
                etiqueta = f"[{lang:6}] {var:15}  n={n:>4}x{n:<4}"
                print(f"{etiqueta} ... ejecutando", flush=True)
                reg = ejecutar_con_repeticiones(
                    lambda l=lang, v=var, tam=n: comando_mat(l, v, tam),
                    f"mat_{lang}_{var}_{n}",
                    args.limite,
                )
                if reg["estado"] == "ok":
                    print(
                        f"{etiqueta}  {reg['tiempo_s']*1e3:10.3f} ms  "
                        f"Extra {reg['mem_extra_mb']:7.3f} MB  "
                        f"RSS {reg['rss_pico_mb']:7.2f} MB  "
                        f"ok={reg['verificado']}",
                        flush=True,
                    )
                else:
                    print(f"{etiqueta}  {reg['estado'].upper()}", flush=True)
                datos["matrices"].append(reg)
                hechos_mat.add(clave)
                guardar(datos, args.salida)

    print("\n" + "=" * 78)
    print("PARTE 3: PRUEBA DE ESTRÉS DE MEMORIA EN STRASSEN")
    print("=" * 78)
    datos["estres"] = ejecutar_prueba_estres()
    print(f"  ✓ Prueba de estrés registrada (código={datos['estres']['codigo_salida']})")

    guardar(datos, args.salida)
    exportar_csv(
        datos,
        os.path.join(DIR_RES, "resultados_quickselect.csv"),
        os.path.join(DIR_RES, "resultados_matrices.csv"),
    )
    print(f"\n✅ Resultados guardados en {args.salida}")


if __name__ == "__main__":
    main()
