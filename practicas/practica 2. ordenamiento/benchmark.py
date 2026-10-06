#!/usr/bin/env python3
"""
Orquestador del benchmark de la Práctica 2.

Para cada lenguaje × algoritmo × n lanza UN subproceso (Python o Java) que
carga el dataset, ordena, verifica y reporta tiempo y memoria. Además:

  * Revisa la RAM antes de ejecutar (modelo teórico de memoria): si la corrida
    necesitaría más del 75 % de la RAM física se omite  -> estado 'omitido_ram'.
  * Predice el tiempo a partir del tamaño anterior medido (×f(n)/f(n_prev)):
    si supera el límite se omite                        -> estado 'omitido_tiempo'.
  * Si una corrida excede el límite (30 min) se mata    -> estado 'timeout'.
  * Mide el RSS máximo REAL del subproceso con os.wait4().
  * Repite 3 veces las corridas que tardan < 10 s y reporta la mediana.
  * Guarda cada resultado inmediatamente (se puede reanudar con --reanudar).
  * Al final estima (T = c·f(n)) las corridas no ejecutadas, marcadas 'estimado'.

Uso:
    python benchmark.py                 # benchmark completo
    python benchmark.py --reanudar      # continúa donde se quedó
    python benchmark.py --solo-estimar  # recalcula solo las estimaciones
"""
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

TAMANIOS = [100_000, 1_000_000, 10_000_000, 100_000_000, 1_000_000_000]
ALGORITMOS = ["bubble", "merge", "tree", "heap", "counting"]
LENGUAJES = ["java", "python"]

LIMITE_S = 30 * 60              # límite por corrida
REPETIR_SI_MENOR_A_S = 10       # corridas rápidas: 3 repeticiones (mediana)
REPETICIONES = 3
FRACCION_RAM = 0.75             # máximo de RAM física que puede pedir una corrida
K_CLAVES = 1_000_000            # rango de claves de Counting Sort (2 decimales en [0, 10 000))
JAVA = os.environ.get("JAVA_BIN", "/opt/homebrew/opt/openjdk@21/bin/java")
JAVA_XMX = "6g"
MB = 2 ** 20


# ---------------------------------------------------------------------
# Modelos teóricos
# ---------------------------------------------------------------------
def f_complejidad(alg, n):
    """Función de crecimiento teórica usada para predecir/estimar tiempos."""
    if alg == "bubble":
        return n * n
    if alg == "counting":
        return n + K_CLAVES
    return n * math.log2(n)


def memoria_extra_modelo(lenguaje, alg, n):
    """Bytes extra que pide el algoritmo además del arreglo de entrada."""
    if alg in ("bubble", "heap"):
        return 0
    if alg == "merge":
        return 8 * n                                   # buffer auxiliar
    if alg == "tree":                                  # nodos <= valores distintos <= k
        bytes_nodo = 24 if lenguaje == "python" else 20
        return 2 * min(n, K_CLAVES) * bytes_nodo       # x2 por crecimiento de arreglos
    if alg == "counting":
        return 8 * n + K_CLAVES * (8 if lenguaje == "python" else 4)
    raise ValueError(alg)


def memoria_total_modelo(lenguaje, alg, n):
    overhead = 40 * MB if lenguaje == "python" else 150 * MB
    return 8 * n + memoria_extra_modelo(lenguaje, alg, n) + overhead


def ram_fisica():
    return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")


# ---------------------------------------------------------------------
# Ejecución de una corrida
# ---------------------------------------------------------------------
def comando(lenguaje, alg, n):
    if lenguaje == "python":
        return [sys.executable, os.path.join(DIR, "ordenamiento.py"), "--algoritmo", alg, "--n", str(n)]
    return [JAVA, f"-Xmx{JAVA_XMX}", "-cp", DIR, "Ordenamiento", "--algoritmo", alg, "--n", str(n)]


def ejecutar_una(lenguaje, alg, n, rep, limite):
    """Lanza el subproceso, lo espera con os.wait4 (RSS máximo real) y aplica timeout."""
    os.makedirs(DIR_LOGS, exist_ok=True)
    ruta_log = os.path.join(DIR_LOGS, f"{lenguaje}_{alg}_{n}_r{rep}.log")
    with open(ruta_log, "w") as log:
        p = subprocess.Popen(comando(lenguaje, alg, n), stdout=log, stderr=subprocess.STDOUT, cwd=DIR)
        t0 = time.monotonic()
        espera = 0.01
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
            espera = min(espera * 1.5, 1.0)
        p.returncode = os.waitstatus_to_exitcode(status)   # evita un segundo wait
    pared_s = time.monotonic() - t0
    rss = uso.ru_maxrss if sys.platform == "darwin" else uso.ru_maxrss * 1024

    if timeout:
        return {"estado": "timeout", "pared_s": pared_s}
    resultado = None
    with open(ruta_log) as log:
        for linea in log:
            if linea.startswith("RESULTADO "):
                resultado = json.loads(linea[len("RESULTADO "):])
    if p.returncode != 0 or resultado is None:
        return {"estado": "error", "codigo": p.returncode, "log": os.path.relpath(ruta_log, DIR)}
    resultado.update(estado="ok", rss_pico_mb=rss / MB, pared_s=pared_s)
    return resultado


def ejecutar(lenguaje, alg, n, limite):
    r = ejecutar_una(lenguaje, alg, n, 1, limite)
    if r["estado"] != "ok":
        return r
    reps = [r]
    if r["tiempo_s"] < REPETIR_SI_MENOR_A_S:
        for i in range(2, REPETICIONES + 1):
            ri = ejecutar_una(lenguaje, alg, n, i, limite)
            if ri["estado"] == "ok":
                reps.append(ri)
    reps.sort(key=lambda x: x["tiempo_s"])
    mediana = dict(reps[len(reps) // 2])
    mediana["tiempos_s"] = [x["tiempo_s"] for x in reps]
    mediana["tiempo_s"] = statistics.median(mediana["tiempos_s"])
    mediana["verificado"] = all(x["verificado"] for x in reps)
    return mediana


# ---------------------------------------------------------------------
# Persistencia
# ---------------------------------------------------------------------
def version_java():
    try:
        out = subprocess.run([JAVA, "-version"], capture_output=True, text=True).stderr
        return out.splitlines()[0]
    except Exception:
        return "desconocida"


def cpu():
    try:
        return subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                              capture_output=True, text=True).stdout.strip()
    except Exception:
        return platform.processor()


def metadatos(limite):
    return {
        "fecha": datetime.datetime.now().isoformat(timespec="seconds"),
        "cpu": cpu(),
        "nucleos": os.cpu_count(),
        "ram_gb": round(ram_fisica() / 2**30, 1),
        "so": platform.platform(),
        "python": platform.python_version(),
        "java": version_java(),
        "java_flags": f"-Xmx{JAVA_XMX}",
        "limite_s": limite,
        "fraccion_ram": FRACCION_RAM,
    }


def cargar(ruta):
    if os.path.exists(ruta):
        with open(ruta) as f:
            return json.load(f)
    return None


def guardar(datos, ruta):
    tmp = ruta + ".tmp"
    with open(tmp, "w") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    os.replace(tmp, ruta)


def exportar_csv(datos, ruta):
    cols = ["lenguaje", "algoritmo", "n", "estado", "estimado", "tiempo_s", "rss_pico_mb",
            "mem_extra_mb", "verificado", "motivo"]
    with open(ruta, "w") as f:
        f.write(",".join(cols) + "\n")
        for c in sorted(datos["corridas"], key=lambda c: (c["lenguaje"], ALGORITMOS.index(c["algoritmo"]), c["n"])):
            fila = []
            for k in cols:
                v = c.get(k, "")
                if k == "tiempo_s" and c.get("estimado"):
                    v = c.get("tiempo_est_s", "")
                if k == "rss_pico_mb" and c.get("estimado"):
                    v = c.get("rss_est_mb", "")
                if k == "mem_extra_mb" and c.get("estimado"):
                    v = c.get("mem_extra_est_mb", "")
                fila.append(f'"{v}"' if isinstance(v, str) and "," in v else str(v))
            f.write(",".join(fila) + "\n")


# ---------------------------------------------------------------------
# Estimaciones
# ---------------------------------------------------------------------
def estimar(datos):
    """Para cada corrida no ejecutada, extrapola desde el n medido más grande."""
    ok = {}
    for c in datos["corridas"]:
        if c["estado"] == "ok":
            clave = (c["lenguaje"], c["algoritmo"])
            if clave not in ok or c["n"] > ok[clave]["n"]:
                ok[clave] = c
    for c in datos["corridas"]:
        if c["estado"] == "ok":
            c["estimado"] = False
            continue
        base = ok.get((c["lenguaje"], c["algoritmo"]))
        if base is None:
            c["estimado"] = False
            continue
        lang, alg, n, nb = c["lenguaje"], c["algoritmo"], c["n"], base["n"]
        c["estimado"] = True
        c["base_estimacion_n"] = nb
        c["tiempo_est_s"] = base["tiempo_s"] * f_complejidad(alg, n) / f_complejidad(alg, nb)
        c["rss_est_mb"] = base["rss_pico_mb"] + (memoria_total_modelo(lang, alg, n)
                                                 - memoria_total_modelo(lang, alg, nb)) / MB
        extra_b = memoria_extra_modelo(lang, alg, nb)
        c["mem_extra_est_mb"] = (base["mem_extra_mb"] * memoria_extra_modelo(lang, alg, n) / extra_b
                                 if extra_b > 0 else base["mem_extra_mb"])


# ---------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reanudar", action="store_true")
    ap.add_argument("--solo-estimar", action="store_true")
    ap.add_argument("--tamanios", type=int, nargs="+", default=TAMANIOS)
    ap.add_argument("--algoritmos", nargs="+", default=ALGORITMOS, choices=ALGORITMOS)
    ap.add_argument("--lenguajes", nargs="+", default=LENGUAJES, choices=LENGUAJES)
    ap.add_argument("--limite", type=float, default=LIMITE_S)
    ap.add_argument("--salida", default=os.path.join(DIR_RES, "resultados.json"))
    args = ap.parse_args()
    os.makedirs(DIR_RES, exist_ok=True)

    datos = cargar(args.salida) if (args.reanudar or args.solo_estimar) else None
    if datos is None:
        datos = {"meta": metadatos(args.limite), "corridas": []}

    if not args.solo_estimar:
        hechos = {(c["lenguaje"], c["algoritmo"], c["n"]) for c in datos["corridas"]}
        ram = ram_fisica()
        for n in sorted(args.tamanios):
            for lang in args.lenguajes:
                for alg in args.algoritmos:
                    clave = (lang, alg, n)
                    if clave in hechos:
                        continue
                    etiqueta = f"[{lang:6}] {alg:8} n={n:>13,}"
                    reg = {"lenguaje": lang, "algoritmo": alg, "n": n}

                    previos = [c for c in datos["corridas"]
                               if c["lenguaje"] == lang and c["algoritmo"] == alg and c["n"] < n]
                    previo = max(previos, key=lambda c: c["n"]) if previos else None
                    req = memoria_total_modelo(lang, alg, n)

                    if req > FRACCION_RAM * ram:
                        reg.update(estado="omitido_ram", memoria_requerida_mb=req / MB,
                                   motivo=f"requiere ~{req / 2**30:.1f} GB > {FRACCION_RAM:.0%} de {ram / 2**30:.0f} GB de RAM")
                    elif previo is not None and previo["estado"] != "ok":
                        reg.update(estado="omitido_tiempo",
                                   motivo=f"el tamaño anterior (n={previo['n']:,}) no se ejecutó/terminó")
                    elif previo is not None and (pred := previo["tiempo_s"] * f_complejidad(alg, n)
                                                 / f_complejidad(alg, previo["n"])) > args.limite:
                        reg.update(estado="omitido_tiempo", prediccion_s=pred,
                                   motivo=f"predicción {pred / 60:,.0f} min > límite {args.limite / 60:.0f} min")
                    else:
                        print(f"{etiqueta} ... ejecutando", flush=True)
                        reg.update(ejecutar(lang, alg, n, args.limite))
                        if reg["estado"] == "timeout":
                            reg["motivo"] = f"excedió el límite de {args.limite / 60:.0f} min"

                    if reg["estado"] == "ok":
                        print(f"{etiqueta}  {reg['tiempo_s']:12.4f} s  RSS {reg['rss_pico_mb']:9.1f} MB  "
                              f"extra {reg['mem_extra_mb']:9.1f} MB  verificado={reg['verificado']}", flush=True)
                    else:
                        print(f"{etiqueta}  {reg['estado'].upper()}: {reg.get('motivo', reg.get('log', ''))}", flush=True)

                    datos["corridas"].append(reg)
                    hechos.add(clave)
                    guardar(datos, args.salida)

    estimar(datos)
    guardar(datos, args.salida)
    exportar_csv(datos, os.path.splitext(args.salida)[0] + ".csv")
    print(f"\n✅ Resultados guardados en {args.salida}")


if __name__ == "__main__":
    main()
