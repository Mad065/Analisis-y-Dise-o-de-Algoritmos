#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
 PRÁCTICA 1: ALGORITMOS DE BÚSQUEDA
 Análisis y Diseño de Algoritmos - ESCOM IPN
============================================================================

 Este programa implementa y compara cuatro algoritmos de búsqueda:
   1. Búsqueda Secuencial (Sequential Search / Linear Search)
   2. Búsqueda Binaria (Binary Search)
   3. Búsqueda por Interpolación (Interpolation Search)
   4. Búsqueda con Tabla Hash (Hash Table Search)

 Se generan datasets aleatorios de tamaños: 1K, 10K, 100K, 1M, 10M
 Se evalúan cuatro escenarios para cada algoritmo:
   - Caso ideal (mejor caso específico para cada algoritmo)
   - Peor caso (peor caso específico para cada algoritmo)
   - Elemento no existente (el objetivo no está en el dataset)
   - Caso normal (búsqueda de un elemento en posición aleatoria)

 Se mide por separado:
   - El tiempo de ordenamiento (requerido por búsqueda binaria e interpolación)
   - El tiempo de construcción de la tabla hash
   - El tiempo de búsqueda para cada algoritmo en cada caso
============================================================================
"""

import random    # Para generar números aleatorios
import time      # Para medir tiempos de ejecución con precisión
import sys       # Para información del sistema


# ============================================================================
# CONSTANTES Y CONFIGURACIÓN
# ============================================================================

# Tamaños de los datasets que se van a evaluar
TAMANIOS_DATASET = [1_000, 10_000, 100_000, 1_000_000, 10_000_000]

# Semilla para el generador de números aleatorios
# Esto permite que los resultados sean reproducibles: cada ejecución
# generará exactamente los mismos datasets y objetivos de búsqueda
SEMILLA_RANDOM = 42


# ============================================================================
# 1. BÚSQUEDA SECUENCIAL (Sequential Search / Linear Search)
# ============================================================================
# La búsqueda secuencial es el algoritmo de búsqueda más simple.
# Recorre el arreglo elemento por elemento, desde el inicio hasta el final,
# comparando cada elemento con el objetivo.
#
# Complejidad temporal:
#   - Mejor caso: O(1) — el elemento está en la primera posición
#   - Peor caso:  O(n) — el elemento está en la última posición o no existe
#   - Caso promedio: O(n/2) ≈ O(n)
#
# Complejidad espacial: O(1) — no usa espacio adicional
#
# Ventajas:
#   - No requiere que los datos estén ordenados
#   - Implementación extremadamente simple
#   - Funciona con cualquier tipo de datos comparables
#   - Sin costo de preprocesamiento
#
# Desventajas:
#   - Ineficiente para grandes volúmenes de datos
#   - Tiempo lineal O(n) en el peor caso y caso promedio
# ============================================================================
def busqueda_secuencial(arreglo, objetivo):
    """
    Realiza una búsqueda secuencial (lineal) en el arreglo.

    Recorre el arreglo elemento por elemento desde el inicio hasta
    encontrar el objetivo o llegar al final.

    Parámetros:
        arreglo (list): Lista de elementos donde buscar
        objetivo: Elemento a buscar

    Retorna:
        int: Índice del elemento si se encuentra, -1 si no existe
    """
    # Recorremos el arreglo de izquierda a derecha, posición por posición
    for i in range(len(arreglo)):
        # Comparamos el elemento en la posición actual con el objetivo
        if arreglo[i] == objetivo:
            # ¡Encontrado! Retornamos el índice donde se encontró
            return i

    # Si llegamos aquí, recorrimos TODO el arreglo sin encontrar el objetivo
    return -1


# ============================================================================
# 2. BÚSQUEDA BINARIA (Binary Search)
# ============================================================================
# PREREQUISITO: El arreglo DEBE estar ORDENADO de menor a mayor.
#
# La búsqueda binaria funciona dividiendo repetidamente el espacio de
# búsqueda a la mitad. En cada paso, compara el elemento del medio con
# el objetivo y descarta la mitad que no puede contener el objetivo.
#
# Complejidad temporal:
#   - Mejor caso: O(1) — el elemento está justo en el punto medio
#   - Peor caso:  O(log₂ n) — el elemento está en un extremo o no existe
#   - Caso promedio: O(log₂ n)
#
# Complejidad espacial: O(1) — versión iterativa (sin recursión)
#
# Ejemplo de por qué O(log n) es tan eficiente:
#   n = 10,000,000 → log₂(10,000,000) ≈ 23 comparaciones
#   ¡Solo 23 pasos para buscar entre 10 millones de elementos!
#
# Analogía:
#   Es como el juego de "adivina el número". Si alguien piensa un número
#   entre 1 y 100, siempre preguntamos "¿es mayor o menor que 50?", luego
#   "¿mayor o menor que 25 (o 75)?", etc. En máximo 7 intentos lo encontramos.
#
# Ventajas:
#   - Extremadamente eficiente: O(log n)
#   - Predecible: siempre O(log n) sin importar la distribución de datos
#
# Desventajas:
#   - REQUIERE que los datos estén ordenados
#   - El ordenamiento tiene costo O(n log n) que debe considerarse
#   - No es eficiente si los datos cambian frecuentemente
# ============================================================================
def busqueda_binaria(arreglo_ordenado, objetivo):
    """
    Realiza una búsqueda binaria en un arreglo ORDENADO.

    Divide repetidamente el rango de búsqueda a la mitad,
    comparando el elemento medio con el objetivo.

    Parámetros:
        arreglo_ordenado (list): Lista ORDENADA de menor a mayor
        objetivo: Elemento a buscar

    Retorna:
        int: Índice del elemento si se encuentra, -1 si no existe
    """
    # Establecemos los límites iniciales del rango de búsqueda
    izquierda = 0                            # Límite inferior (inicio del arreglo)
    derecha = len(arreglo_ordenado) - 1      # Límite superior (final del arreglo)

    # Mientras el rango de búsqueda sea válido (no se haya agotado)
    while izquierda <= derecha:
        # Paso 1: Calculamos el punto medio del rango actual
        # Usamos // (división entera) para obtener un índice entero
        # Fórmula: medio = (izquierda + derecha) // 2
        medio = (izquierda + derecha) // 2

        # Paso 2: Comparamos el elemento del medio con el objetivo

        # Caso A: ¡El elemento del medio ES el objetivo!
        if arreglo_ordenado[medio] == objetivo:
            return medio  # Retornamos su índice

        # Caso B: El objetivo es MENOR que el elemento del medio
        # → El objetivo solo puede estar en la MITAD IZQUIERDA
        #   (entre izquierda y medio-1)
        elif arreglo_ordenado[medio] > objetivo:
            derecha = medio - 1  # Descartamos la mitad derecha

        # Caso C: El objetivo es MAYOR que el elemento del medio
        # → El objetivo solo puede estar en la MITAD DERECHA
        #   (entre medio+1 y derecha)
        else:
            izquierda = medio + 1  # Descartamos la mitad izquierda

    # Si izquierda > derecha, el rango se agotó → el elemento NO existe
    return -1


# ============================================================================
# 3. BÚSQUEDA POR INTERPOLACIÓN (Interpolation Search)
# ============================================================================
# PREREQUISITO: El arreglo DEBE estar ORDENADO y, idealmente, los valores
#               deben estar distribuidos de manera aproximadamente uniforme.
#
# La búsqueda por interpolación es una mejora de la búsqueda binaria.
# En lugar de siempre ir al punto medio, ESTIMA la posición probable
# del objetivo usando interpolación lineal basada en los valores.
#
# Fórmula de interpolación:
#   pos = izq + ((objetivo - arr[izq]) × (der - izq)) / (arr[der] - arr[izq])
#
# Analogía:
#   Cuando buscamos una palabra en el diccionario, no abrimos siempre
#   por la mitad. Si buscamos "zapato", abrimos cerca del final.
#   Si buscamos "avión", abrimos cerca del inicio. La búsqueda por
#   interpolación hace exactamente esto: estima DÓNDE debería estar
#   el elemento basándose en su valor relativo.
#
# Complejidad temporal:
#   - Mejor caso: O(1) — la interpolación acierta en el primer intento
#   - Caso promedio: O(log log n) — con distribución uniforme
#   - Peor caso: O(n) — con distribución muy desigual (ej: exponencial)
#
# Complejidad espacial: O(1)
#
# Ventajas:
#   - Más rápida que binaria con datos uniformemente distribuidos
#   - O(log log n) es significativamente mejor que O(log n) para n grandes
#     Ejemplo: n=10^7 → log(10^7)≈23, log(log(10^7))≈5
#
# Desventajas:
#   - Puede degradarse a O(n) con datos mal distribuidos
#   - Requiere operaciones aritméticas adicionales por iteración
#   - Requiere datos numéricos (necesita aritmética sobre los valores)
#   - Requiere datos ordenados
# ============================================================================
def busqueda_interpolacion(arreglo_ordenado, objetivo):
    """
    Realiza una búsqueda por interpolación en un arreglo ORDENADO.

    Utiliza la distribución de los valores para estimar la posición
    más probable del objetivo, similar a cómo buscamos en un diccionario.

    Parámetros:
        arreglo_ordenado (list): Lista ORDENADA de elementos numéricos
        objetivo (int/float): Número a buscar

    Retorna:
        int: Índice del elemento si se encuentra, -1 si no existe
    """
    # Definimos los límites iniciales del rango de búsqueda
    izquierda = 0
    derecha = len(arreglo_ordenado) - 1

    # Condiciones del bucle (más restrictivas que búsqueda binaria):
    # 1. izquierda <= derecha: el rango debe ser válido
    # 2. objetivo >= arreglo[izquierda]: el objetivo no puede ser menor que el mínimo
    # 3. objetivo <= arreglo[derecha]: el objetivo no puede ser mayor que el máximo
    # Las condiciones 2 y 3 son necesarias para que la fórmula de interpolación
    # tenga sentido y produzca un índice dentro del rango
    while (izquierda <= derecha and
           objetivo >= arreglo_ordenado[izquierda] and
           objetivo <= arreglo_ordenado[derecha]):

        # Caso especial: si solo queda un elemento en el rango
        if izquierda == derecha:
            if arreglo_ordenado[izquierda] == objetivo:
                return izquierda  # Es el que buscamos
            return -1  # No es el que buscamos

        # ================================================================
        # Fórmula de interpolación lineal:
        #
        #                    (objetivo - arr[izq]) × (der - izq)
        # pos = izq + ─────────────────────────────────────────────
        #                        arr[der] - arr[izq]
        #
        # Desglose de la fórmula:
        # ─────────────────────────────────────────────────────────
        # (objetivo - arr[izq])    → Distancia del objetivo al valor mínimo
        # (arr[der] - arr[izq])    → Rango total de valores
        # La división da la       → Fracción proporcional (entre 0.0 y 1.0)
        # (der - izq)             → Rango de índices disponibles
        # Multiplicar fracción    → Desplazamiento estimado desde izquierda
        # Sumar izquierda         → Posición estimada absoluta
        #
        # Ejemplo numérico:
        #   arr = [10, 20, 30, 40, 50], buscamos 35
        #   izq=0, der=4, arr[izq]=10, arr[der]=50
        #   pos = 0 + ((35-10) × (4-0)) / (50-10) = (25 × 4) / 40 = 2.5 → 2
        #   Verificamos arr[2]=30 → 35 > 30, así que izq = 3
        #   Siguiente iteración encontrará 40, etc.
        # ================================================================
        posicion = izquierda + int(
            ((objetivo - arreglo_ordenado[izquierda]) *
             (derecha - izquierda)) /
            (arreglo_ordenado[derecha] - arreglo_ordenado[izquierda])
        )

        # Verificamos si la posición estimada contiene el objetivo
        if arreglo_ordenado[posicion] == objetivo:
            return posicion  # ¡Encontrado en la posición interpolada!

        # Si el valor en la posición es MENOR que el objetivo,
        # el objetivo debe estar MÁS A LA DERECHA
        if arreglo_ordenado[posicion] < objetivo:
            izquierda = posicion + 1

        # Si el valor en la posición es MAYOR que el objetivo,
        # el objetivo debe estar MÁS A LA IZQUIERDA
        else:
            derecha = posicion - 1

    # El objetivo está fuera del rango de valores del arreglo → no existe
    return -1


# ============================================================================
# 4. TABLA HASH CON ENCADENAMIENTO SEPARADO (Separate Chaining Hash Table)
# ============================================================================
# Una tabla hash es una estructura de datos que permite búsquedas en
# tiempo promedio O(1) al usar una FUNCIÓN HASH para calcular directamente
# la posición donde almacenar y buscar cada elemento.
#
# Complejidad temporal:
#   - Inserción: O(1) amortizado
#   - Búsqueda (mejor caso): O(1) — sin colisiones, acceso directo
#   - Búsqueda (caso promedio): O(1 + α) donde α = n/m (factor de carga)
#   - Búsqueda (peor caso): O(n) — todos los elementos en la misma cubeta
#
# Complejidad espacial: O(n + m)
#   donde n = número de elementos, m = tamaño de la tabla
#
# Funcionamiento:
#   1. Se aplica una función hash a la clave: h(clave) → índice
#   2. Se almacena el elemento en tabla[índice]
#   3. Si hay COLISIÓN (dos claves con el mismo hash), se resuelve
#      mediante encadenamiento separado
#
# Resolución de colisiones — Encadenamiento Separado:
#   Cada celda de la tabla contiene una LISTA (cadena). Cuando hay
#   colisión, simplemente se agrega el nuevo elemento a la lista.
#
#   Ejemplo con tabla de tamaño 5 y hash(x) = x % 5:
#   Insertar: 10, 15, 22, 7, 20
#
#   Índice  Cadena
#   [0] → [10] → [15] → [20]    (10%5=0, 15%5=0, 20%5=0)
#   [1] → []                      (vacía)
#   [2] → [22] → [7]             (22%5=2, 7%5=2)
#   [3] → []                      (vacía)
#   [4] → []                      (vacía)
#
#   Para buscar 7: hash(7)=2, recorremos cadena en [2]: 22→7 ¡encontrado!
#
# Factor de carga (α = n/m):
#   - α < 1: pocas colisiones, buen rendimiento
#   - α ≈ 1: rendimiento aceptable
#   - α > 1: muchas colisiones, rendimiento se degrada
#
# Ventajas:
#   - Tiempo promedio O(1) para búsqueda e inserción
#   - No requiere datos ordenados
#   - Flexible: se adapta a datos dinámicos
#
# Desventajas:
#   - Requiere espacio O(n + m) para la tabla y las cadenas
#   - El rendimiento depende de la calidad de la función hash
#   - Requiere tiempo O(n) de construcción antes de poder buscar
#   - No mantiene los datos ordenados (no sirve para rango queries)
# ============================================================================
class TablaHash:
    """
    Implementación de una Tabla Hash con Encadenamiento Separado.

    Cada posición (cubeta/bucket) de la tabla almacena una lista de
    elementos. Las colisiones se resuelven agregando elementos a la
    lista de la cubeta correspondiente.
    """

    def __init__(self, capacidad_esperada):
        """
        Inicializa la tabla hash.

        El tamaño se elige como el siguiente número primo mayor a
        1.3 veces la capacidad esperada. Usar un número primo reduce
        los patrones en la función hash modular, distribuyendo mejor
        los elementos.

        Un factor 1.3x significa un factor de carga α ≈ 0.77, lo cual
        ofrece un buen balance entre uso de memoria y pocas colisiones.

        Parámetros:
            capacidad_esperada (int): Número estimado de elementos
        """
        # Calculamos el tamaño de la tabla como el siguiente primo > 1.3n
        # ¿Por qué primo? Porque reduce colisiones con hash modular.
        # ¿Por qué 1.3x? Para tener un factor de carga α ≈ 0.77 (< 1)
        self.tamanio = self._siguiente_primo(int(capacidad_esperada * 1.3))

        # Creamos la tabla: un arreglo de listas vacías (cubetas/buckets)
        # Cada lista almacenará los elementos que caigan en esa cubeta
        self.tabla = [[] for _ in range(self.tamanio)]

        # Contador de elementos almacenados en la tabla
        self.num_elementos = 0

    def _es_primo(self, n):
        """
        Verifica si un número es primo usando prueba de divisibilidad.

        Un número primo solo es divisible entre 1 y sí mismo.
        Optimizamos verificando solo hasta √n y solo números 6k±1.

        Parámetros:
            n (int): Número a verificar

        Retorna:
            bool: True si n es primo
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        # Si es divisible por 2 o 3, no es primo
        if n % 2 == 0 or n % 3 == 0:
            return False
        # Todo primo mayor a 3 tiene la forma 6k ± 1
        # Solo necesitamos verificar hasta √n
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def _siguiente_primo(self, n):
        """
        Encuentra el menor número primo mayor o igual a n.

        Parámetros:
            n (int): Número base

        Retorna:
            int: Siguiente primo >= n
        """
        if n <= 2:
            return 2
        # Si n es par, empezamos con n+1 (los primos > 2 son impares)
        if n % 2 == 0:
            n += 1
        # Verificamos impares sucesivos hasta encontrar un primo
        while not self._es_primo(n):
            n += 2
        return n

    def _funcion_hash(self, clave):
        """
        Calcula el índice hash para una clave numérica.

        Utiliza el método de MÓDULO (division method):
            hash(clave) = clave mod tamaño_tabla

        Este método es simple pero efectivo cuando el tamaño de la tabla
        es un número primo, ya que distribuye las claves uniformemente.

        Parámetros:
            clave (int): Clave numérica a hashear

        Retorna:
            int: Índice en la tabla (0 ≤ índice < tamaño_tabla)
        """
        return clave % self.tamanio

    def insertar(self, clave):
        """
        Inserta una clave en la tabla hash.

        Proceso:
        1. Calcula hash(clave) para obtener el índice de la cubeta
        2. Agrega la clave al final de la lista en esa cubeta

        Parámetros:
            clave (int): Valor a insertar

        Complejidad: O(1) amortizado
        """
        # Paso 1: Calcular el índice de la cubeta
        indice = self._funcion_hash(clave)

        # Paso 2: Agregar la clave a la cadena (lista) de esa cubeta
        self.tabla[indice].append(clave)

        # Paso 3: Incrementar el contador de elementos
        self.num_elementos += 1

    def buscar(self, clave):
        """
        Busca una clave en la tabla hash.

        Proceso:
        1. Calcula hash(clave) para obtener el índice de la cubeta
        2. Recorre la lista de esa cubeta buscando la clave

        Parámetros:
            clave (int): Valor a buscar

        Retorna:
            tuple: (índice_cubeta, posición_en_cadena) si se encuentra
                   (-1, -1) si no se encuentra

        Complejidad: O(1) promedio, O(k) donde k es la longitud de la cadena
        """
        # Paso 1: Calcular el índice de la cubeta
        indice = self._funcion_hash(clave)

        # Paso 2: Obtener la lista (cadena) almacenada en esa cubeta
        cadena = self.tabla[indice]

        # Paso 3: Búsqueda secuencial dentro de la cadena
        # En una tabla hash bien dimensionada, esta cadena es muy corta (1-2 elementos)
        for i, elemento in enumerate(cadena):
            if elemento == clave:
                # ¡Encontrado! Retornamos la cubeta y posición en la cadena
                return indice, i

        # La clave no está en la tabla
        return -1, -1


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def generar_dataset(tamanio, semilla=SEMILLA_RANDOM):
    """
    Genera un dataset de números enteros aleatorios ÚNICOS.

    Los números se generan en el rango [1, tamaño × 10] para asegurar:
    - Suficiente espacio entre valores para una distribución uniforme
    - No hay valores repetidos (importante para las búsquedas)
    - Los valores son positivos (simplifica el caso "no existe" usando -1)

    Parámetros:
        tamanio (int): Cantidad de elementos a generar
        semilla (int): Semilla para reproducibilidad

    Retorna:
        list: Lista de 'tamaño' números aleatorios únicos sin ordenar
    """
    # Fijamos la semilla para que los resultados sean reproducibles
    # Esto significa que cada ejecución genera exactamente los mismos datos
    random.seed(semilla)

    # random.sample() selecciona 'tamanio' elementos SIN repetición
    # del rango [1, tamaño × 10]
    # Usar un rango 10× mayor asegura que siempre hay suficientes números
    rango_valores = tamanio * 10
    dataset = random.sample(range(1, rango_valores + 1), tamanio)

    return dataset


def formatear_tiempo(nanosegundos):
    """
    Formatea un tiempo en nanosegundos a la unidad más legible.

    Escala automáticamente:
    - < 1,000 ns → nanosegundos (ns)
    - < 1,000,000 ns → microsegundos (μs)
    - < 1,000,000,000 ns → milisegundos (ms)
    - ≥ 1,000,000,000 ns → segundos (s)

    Parámetros:
        nanosegundos (int/float): Tiempo en nanosegundos

    Retorna:
        str: Tiempo formateado con unidad apropiada
    """
    if nanosegundos < 1_000:
        return f"{nanosegundos:.0f} ns"
    elif nanosegundos < 1_000_000:
        return f"{nanosegundos / 1_000:.2f} us"
    elif nanosegundos < 1_000_000_000:
        return f"{nanosegundos / 1_000_000:.2f} ms"
    else:
        return f"{nanosegundos / 1_000_000_000:.4f} s"


def medir_tiempo_busqueda(funcion_busqueda, *argumentos):
    """
    Mide el tiempo de ejecución de una función de búsqueda con
    la máxima precisión disponible.

    Usa time.perf_counter_ns() que retorna nanosegundos (10⁻⁹ s)
    con la mayor resolución que ofrece el sistema operativo.

    Parámetros:
        funcion_busqueda: Función de búsqueda a cronometrar
        *argumentos: Argumentos a pasar a la función

    Retorna:
        tuple: (resultado_de_la_busqueda, tiempo_en_nanosegundos)
    """
    # Registramos el instante inicial (en nanosegundos)
    inicio = time.perf_counter_ns()

    # Ejecutamos la función de búsqueda con sus argumentos
    resultado = funcion_busqueda(*argumentos)

    # Registramos el instante final
    fin = time.perf_counter_ns()

    # El tiempo transcurrido es la diferencia
    tiempo_ns = fin - inicio

    return resultado, tiempo_ns


# ============================================================================
# FUNCIÓN PRINCIPAL: EJECUCIÓN DE BENCHMARKS
# ============================================================================

def ejecutar_benchmarks():
    """
    Ejecuta todos los benchmarks de búsqueda para cada tamaño de dataset.

    Para cada tamaño de dataset:
      1. Genera el dataset de números aleatorios únicos
      2. Ordena una copia del dataset (midiendo el tiempo)
      3. Construye la tabla hash (midiendo el tiempo)
      4. Define los objetivos de búsqueda para 4 casos:
         - Mejor caso (específico por algoritmo)
         - Peor caso (específico por algoritmo)
         - Elemento no encontrado (compartido)
         - Caso normal (compartido)
      5. Ejecuta cada algoritmo en cada caso midiendo tiempos
      6. Muestra tablas comparativas con los resultados
    """

    # ==================================================================
    # Encabezado del programa
    # ==================================================================
    print("=" * 100)
    print("  PRACTICA 1: COMPARACION DE ALGORITMOS DE BUSQUEDA")
    print("  Analisis y Diseno de Algoritmos - ESCOM IPN")
    print("=" * 100)
    print()
    print("  Algoritmos implementados:")
    print("    1. Busqueda Secuencial       - O(n)")
    print("    2. Busqueda Binaria          - O(log n) [requiere ordenamiento previo]")
    print("    3. Busqueda por Interpolacion - O(log log n) promedio [requiere orden.]")
    print("    4. Tabla Hash                - O(1) promedio [requiere construccion]")
    print()
    print(f"  Tamanios de dataset: {', '.join(f'{t:,}' for t in TAMANIOS_DATASET)}")
    print(f"  Semilla aleatoria:  {SEMILLA_RANDOM}")
    print(f"  Python:             {sys.version.split()[0]}")
    print()

    # Nombres para las filas y columnas de las tablas de resultados
    nombres_algoritmos = ["Secuencial", "Binaria", "Interpolacion", "Tabla Hash"]
    nombres_casos = ["Mejor caso", "Peor caso", "No existe", "Caso normal"]

    # ==================================================================
    # Iteramos sobre cada tamaño de dataset
    # ==================================================================
    for tamanio in TAMANIOS_DATASET:

        print(f"\n{'#' * 100}")
        print(f"#  DATASET: {tamanio:>12,} elementos")
        print(f"{'#' * 100}")

        # ==============================================================
        # PASO 1: Generar el dataset aleatorio
        # ==============================================================
        print(f"\n  [1/4] Generando {tamanio:,} numeros aleatorios unicos...")
        inicio_gen = time.perf_counter_ns()
        dataset = generar_dataset(tamanio)
        tiempo_generacion = time.perf_counter_ns() - inicio_gen
        print(f"        Completado en {formatear_tiempo(tiempo_generacion)}")

        # ==============================================================
        # PASO 2: Ordenar una copia del dataset
        # (requerido para busqueda binaria y por interpolacion)
        # ==============================================================
        print(f"\n  [2/4] Ordenando dataset (necesario para busqueda binaria e interpolacion)...")

        # IMPORTANTE: Creamos una COPIA para no modificar el original.
        # El dataset original (desordenado) se usa para busqueda secuencial.
        dataset_ordenado = dataset.copy()

        # Medimos el tiempo de ordenamiento por separado
        # Python usa Timsort: un algoritmo híbrido basado en merge sort e insertion sort
        # Complejidad: O(n log n) en el peor caso, O(n) en el mejor caso
        inicio_sort = time.perf_counter_ns()
        dataset_ordenado.sort()
        fin_sort = time.perf_counter_ns()
        tiempo_ordenamiento = fin_sort - inicio_sort

        print(f"        Algoritmo: Timsort (Python built-in)")
        print(f"        Complejidad: O(n log n) peor caso")
        print(f"        >>> Tiempo de ordenamiento: {formatear_tiempo(tiempo_ordenamiento)}")

        # ==============================================================
        # PASO 3: Construir la tabla hash
        # ==============================================================
        print(f"\n  [3/4] Construyendo tabla hash con encadenamiento separado...")

        # Medimos el tiempo de construcción de la tabla hash
        # Esto incluye crear la tabla y todos los n insertados
        inicio_hash_build = time.perf_counter_ns()
        tabla_hash = TablaHash(tamanio)
        for elemento in dataset:
            tabla_hash.insertar(elemento)
        fin_hash_build = time.perf_counter_ns()
        tiempo_construccion_hash = fin_hash_build - inicio_hash_build

        # Estadísticas de la tabla hash para evaluar su calidad
        factor_carga = tabla_hash.num_elementos / tabla_hash.tamanio
        cadenas_no_vacias = sum(1 for c in tabla_hash.tabla if c)
        long_max_cadena = max(len(c) for c in tabla_hash.tabla) if tabla_hash.tabla else 0
        # Longitud promedio de cadenas NO vacías
        long_prom = tabla_hash.num_elementos / cadenas_no_vacias if cadenas_no_vacias else 0

        print(f"        Tamanio de la tabla:       {tabla_hash.tamanio:>12,}")
        print(f"        Elementos insertados:      {tabla_hash.num_elementos:>12,}")
        print(f"        Factor de carga (n/m):     {factor_carga:>12.4f}")
        print(f"        Cubetas ocupadas:          {cadenas_no_vacias:>12,}")
        print(f"        Long. maxima de cadena:    {long_max_cadena:>12}")
        print(f"        Long. promedio de cadena:  {long_prom:>12.2f}")
        print(f"        >>> Tiempo de construccion: {formatear_tiempo(tiempo_construccion_hash)}")

        # ==============================================================
        # PASO 4: Ejecutar búsquedas en los 4 casos de prueba
        # ==============================================================
        print(f"\n  [4/4] Ejecutando busquedas...")
        n = len(dataset)

        # ---- Definición de OBJETIVOS DE BÚSQUEDA por caso ----
        #
        # Cada algoritmo tiene diferentes "mejores" y "peores" casos.
        # Definimos objetivos ESPECÍFICOS para maximizar/minimizar
        # el rendimiento de cada algoritmo.

        # CASO "NO EXISTE" (compartido por todos los algoritmos):
        # Un valor que SABEMOS que no está en el dataset
        # Como todos los valores son positivos (≥1), usamos un valor
        # mayor al máximo para garantizar que no existe
        objetivo_no_existe = max(dataset) + 100

        # CASO "NORMAL" (compartido por todos los algoritmos):
        # Un elemento aleatorio del dataset, en una posición "intermedia"
        random.seed(tamanio)  # Semilla basada en tamaño para reproducibilidad
        indice_aleatorio = random.randint(n // 4, 3 * n // 4)
        objetivo_normal = dataset[indice_aleatorio]

        # MEJOR CASO por algoritmo:
        # - Secuencial: primer elemento → se encuentra en la 1ª comparación
        # - Binaria: elemento medio del arreglo ordenado → se encuentra
        #            en la 1ª comparación (justo donde mira primero)
        # - Interpolación: elemento medio en datos uniformes → interpolación
        #                  acierta casi exactamente en el 1er intento
        # - Hash: cualquier elemento → generalmente O(1) sin colisión
        objetivo_mejor_seq = dataset[0]
        objetivo_mejor_bin = dataset_ordenado[n // 2]
        objetivo_mejor_interp = dataset_ordenado[n // 2]
        objetivo_mejor_hash = dataset[0]

        # PEOR CASO por algoritmo:
        # - Secuencial: último elemento → debe recorrer TODO el arreglo
        # - Binaria: primer elemento del ordenado → está en el extremo,
        #            requiere log₂(n) divisiones para llegar
        # - Interpolación: primer elemento del ordenado → en el extremo,
        #                  la interpolación debe ajustarse repetidamente
        # - Hash: elemento en la cubeta más larga → máxima búsqueda
        #         secuencial dentro de la cadena
        objetivo_peor_seq = dataset[-1]
        objetivo_peor_bin = dataset_ordenado[0]
        objetivo_peor_interp = dataset_ordenado[0]
        # Para hash: encontramos la cubeta con más colisiones
        indice_cubeta_max = max(range(len(tabla_hash.tabla)),
                                key=lambda idx: len(tabla_hash.tabla[idx]))
        cubeta_larga = tabla_hash.tabla[indice_cubeta_max]
        # El peor caso es buscar el ÚLTIMO elemento de la cadena más larga
        objetivo_peor_hash = cubeta_larga[-1] if cubeta_larga else dataset[-1]

        # ---- Ejecutar todas las búsquedas y registrar tiempos ----
        # Estructura: resultados[algoritmo][caso] = tiempo_en_nanosegundos
        resultados = {}

        # --- BÚSQUEDA SECUENCIAL ---
        # Opera sobre el arreglo ORIGINAL (desordenado)
        resultados["Secuencial"] = {}
        _, t = medir_tiempo_busqueda(busqueda_secuencial, dataset, objetivo_mejor_seq)
        resultados["Secuencial"]["Mejor caso"] = t
        _, t = medir_tiempo_busqueda(busqueda_secuencial, dataset, objetivo_peor_seq)
        resultados["Secuencial"]["Peor caso"] = t
        _, t = medir_tiempo_busqueda(busqueda_secuencial, dataset, objetivo_no_existe)
        resultados["Secuencial"]["No existe"] = t
        _, t = medir_tiempo_busqueda(busqueda_secuencial, dataset, objetivo_normal)
        resultados["Secuencial"]["Caso normal"] = t

        # --- BÚSQUEDA BINARIA ---
        # Opera sobre el arreglo ORDENADO
        resultados["Binaria"] = {}
        _, t = medir_tiempo_busqueda(busqueda_binaria, dataset_ordenado, objetivo_mejor_bin)
        resultados["Binaria"]["Mejor caso"] = t
        _, t = medir_tiempo_busqueda(busqueda_binaria, dataset_ordenado, objetivo_peor_bin)
        resultados["Binaria"]["Peor caso"] = t
        _, t = medir_tiempo_busqueda(busqueda_binaria, dataset_ordenado, objetivo_no_existe)
        resultados["Binaria"]["No existe"] = t
        _, t = medir_tiempo_busqueda(busqueda_binaria, dataset_ordenado, objetivo_normal)
        resultados["Binaria"]["Caso normal"] = t

        # --- BÚSQUEDA POR INTERPOLACIÓN ---
        # Opera sobre el arreglo ORDENADO
        resultados["Interpolacion"] = {}
        _, t = medir_tiempo_busqueda(busqueda_interpolacion, dataset_ordenado, objetivo_mejor_interp)
        resultados["Interpolacion"]["Mejor caso"] = t
        _, t = medir_tiempo_busqueda(busqueda_interpolacion, dataset_ordenado, objetivo_peor_interp)
        resultados["Interpolacion"]["Peor caso"] = t
        _, t = medir_tiempo_busqueda(busqueda_interpolacion, dataset_ordenado, objetivo_no_existe)
        resultados["Interpolacion"]["No existe"] = t
        _, t = medir_tiempo_busqueda(busqueda_interpolacion, dataset_ordenado, objetivo_normal)
        resultados["Interpolacion"]["Caso normal"] = t

        # --- TABLA HASH ---
        # Opera sobre la tabla hash construida previamente
        resultados["Tabla Hash"] = {}
        _, t = medir_tiempo_busqueda(tabla_hash.buscar, objetivo_mejor_hash)
        resultados["Tabla Hash"]["Mejor caso"] = t
        _, t = medir_tiempo_busqueda(tabla_hash.buscar, objetivo_peor_hash)
        resultados["Tabla Hash"]["Peor caso"] = t
        _, t = medir_tiempo_busqueda(tabla_hash.buscar, objetivo_no_existe)
        resultados["Tabla Hash"]["No existe"] = t
        _, t = medir_tiempo_busqueda(tabla_hash.buscar, objetivo_normal)
        resultados["Tabla Hash"]["Caso normal"] = t

        # ==============================================================
        # IMPRIMIR TABLA DE RESULTADOS DE BÚSQUEDA
        # ==============================================================
        ancho_algo = 18   # Ancho de la columna de algoritmo
        ancho_caso = 18   # Ancho de cada columna de caso

        print()
        print("  ┌─ RESULTADOS DE BUSQUEDA (tiempos de busqueda solamente)")
        print("  │")

        # Línea superior de la tabla
        linea = "  ├─" + "─" * ancho_algo + "─┬─"
        linea += "─┬─".join("─" * ancho_caso for _ in nombres_casos)
        linea += "─┐"
        # Usamos una versión simplificada:
        separador = "  +" + "-" * (ancho_algo + 2)
        for _ in nombres_casos:
            separador += "+" + "-" * (ancho_caso + 2)
        separador += "+"
        print(separador)

        # Encabezado
        enc = f"  | {'Algoritmo':<{ancho_algo}} "
        for caso in nombres_casos:
            enc += f"| {caso:>{ancho_caso}} "
        enc += "|"
        print(enc)
        print(separador)

        # Filas de datos
        for algo in nombres_algoritmos:
            fila = f"  | {algo:<{ancho_algo}} "
            for caso in nombres_casos:
                tiempo = resultados[algo][caso]
                fila += f"| {formatear_tiempo(tiempo):>{ancho_caso}} "
            fila += "|"
            print(fila)

        print(separador)

        # ==============================================================
        # TABLA DE TIEMPOS DE PREPROCESAMIENTO
        # ==============================================================
        print()
        print("  ┌─ TIEMPOS DE PREPROCESAMIENTO")
        print("  │")
        sep2 = "  +" + "-" * 40 + "+" + "-" * 22 + "+"
        print(sep2)
        print(f"  | {'Operacion':<38} | {'Tiempo':>20} |")
        print(sep2)
        print(f"  | {'Generacion del dataset':<38} | {formatear_tiempo(tiempo_generacion):>20} |")
        print(f"  | {'Ordenamiento (Timsort)':<38} | {formatear_tiempo(tiempo_ordenamiento):>20} |")
        print(f"  | {'Construccion tabla hash':<38} | {formatear_tiempo(tiempo_construccion_hash):>20} |")
        print(sep2)

        # ==============================================================
        # TABLA DE OBJETIVOS UTILIZADOS
        # ==============================================================
        print()
        print("  ┌─ OBJETIVOS DE BUSQUEDA UTILIZADOS POR CASO")
        print("  │")
        sep3 = "  +" + "-" * 17 + "+" + "-" * 14 + "+" + "-" * 14 + "+" + "-" * 16 + "+" + "-" * 14 + "+"
        print(sep3)
        print(f"  | {'Caso':<15} | {'Secuencial':>12} | {'Binaria':>12} | {'Interpolacion':>14} | {'Tabla Hash':>12} |")
        print(sep3)
        print(f"  | {'Mejor caso':<15} | {objetivo_mejor_seq:>12,} | {objetivo_mejor_bin:>12,} | {objetivo_mejor_interp:>14,} | {objetivo_mejor_hash:>12,} |")
        print(f"  | {'Peor caso':<15} | {objetivo_peor_seq:>12,} | {objetivo_peor_bin:>12,} | {objetivo_peor_interp:>14,} | {objetivo_peor_hash:>12,} |")
        print(f"  | {'No existe':<15} | {objetivo_no_existe:>12,} | {objetivo_no_existe:>12,} | {objetivo_no_existe:>14,} | {objetivo_no_existe:>12,} |")
        print(f"  | {'Caso normal':<15} | {objetivo_normal:>12,} | {objetivo_normal:>12,} | {objetivo_normal:>14,} | {objetivo_normal:>12,} |")
        print(sep3)

    # ==================================================================
    # RESUMEN TEÓRICO DE COMPLEJIDADES
    # ==================================================================
    print(f"\n\n{'=' * 100}")
    print("  RESUMEN TEORICO DE COMPLEJIDADES")
    print(f"{'=' * 100}")
    print()
    sep_final = "  " + "-" * 94
    print(f"  {'Algoritmo':<20} | {'Mejor':>14} | {'Promedio':>14} | {'Peor':>14} | {'Espacio':>12} | {'Ordenado?':>10}")
    print(sep_final)
    print(f"  {'Secuencial':<20} | {'O(1)':>14} | {'O(n)':>14} | {'O(n)':>14} | {'O(1)':>12} | {'No':>10}")
    print(f"  {'Binaria':<20} | {'O(1)':>14} | {'O(log n)':>14} | {'O(log n)':>14} | {'O(1)':>12} | {'Si':>10}")
    print(f"  {'Interpolacion':<20} | {'O(1)':>14} | {'O(log log n)':>14} | {'O(n)':>14} | {'O(1)':>12} | {'Si':>10}")
    print(f"  {'Tabla Hash':<20} | {'O(1)':>14} | {'O(1)':>14} | {'O(n)':>14} | {'O(n+m)':>12} | {'No':>10}")
    print(sep_final)
    print()
    print("  Notas importantes:")
    print("  * El costo de ordenamiento O(n log n) debe sumarse al tiempo de busqueda")
    print("    binaria e interpolacion si los datos NO estan previamente ordenados.")
    print("  * La tabla hash requiere O(n) de construccion antes de buscar.")
    print("  * Para UNA sola busqueda en datos no ordenados, la busqueda secuencial")
    print("    puede ser mas eficiente que binaria (se evita el costo de ordenar).")
    print("  * Para MULTIPLES busquedas, la tabla hash o la busqueda binaria son")
    print("    significativamente superiores a la busqueda secuencial.")
    print("  * La busqueda por interpolacion supera a la binaria solo cuando los datos")
    print("    estan distribuidos de forma aproximadamente uniforme.")


# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================
# En Python, esta condición verifica si el archivo se está ejecutando
# directamente (no importado como módulo). Solo en ese caso ejecutamos
# los benchmarks.
# ============================================================================
if __name__ == "__main__":
    ejecutar_benchmarks()
