# Apuntes: Recursividad

La **recursividad** es una técnica de diseño de algoritmos en la que una función se define y se resuelve en términos de sí misma. Un problema general se descompone en uno o más subproblemas **del mismo tipo pero de menor tamaño**, repitiendo este proceso hasta llegar a instancias tan simples y directas que pueden resolverse de manera inmediata sin requerir más llamadas recursivas.

---

## 1. Anatomía de una función recursiva

Toda función recursiva bien estructurada consta fundamentalmente de dos componentes esenciales:

1. **Caso base (o condición de parada):** Es el escenario elemental que detiene la recursión. Devuelve un resultado directo sin realizar nuevas llamadas recursivas. Sin un caso base alcanzable, el algoritmo entraría en recursión infinita.
2. **Caso recursivo (o paso recursivo):** Es la sección donde el problema se reformula en una o varias llamadas a la misma función, pasando argumentos que representan una versión reducida del problema original.

```python
def factorial(n):
    # 1. Caso base
    if n == 0:
        return 1
    # 2. Caso recursivo (se reduce el tamaño con n - 1)
    return n * factorial(n - 1)
```

> **Regla de oro de la recursividad:** Cada llamada recursiva debe garantizar un avance estricto hacia el caso base (*progreso hacia la terminación*).

---

## 2. Metodología: Cómo construir una función recursiva paso a paso

Diseñar un algoritmo recursivo suele ser contra intuitivo al inicio porque requiere pensar de manera **inductiva** en lugar de secuencial. La metodología estándar para construir cualquier función recursiva consta de cuatro etapas:

### Paso 1: Definir la firma y el contrato de la función
Antes de escribir una sola línea de código, define con precisión:
* ¿Qué recibe la función como entrada?
* ¿Qué tipo de dato devuelve?
* ¿Qué representa conceptualmente el valor de retorno para una entrada dada?

### Paso 2: Identificar el subproblema y realizar el "Salto de Fe" (*Leap of Faith*)
Este es el principio fundamental del pensamiento recursivo:
* **No intentes rastrear mentalmente todo el árbol de llamadas** hasta el final; eso sobrecarga la mente humana.
* Supón con certeza que tu función **ya funciona correctamente** para cualquier entrada más pequeña que la actual (esta es la *hipótesis inductiva* de las matemáticas).
* Pregúntate: *Si ya tuviera resuelto el problema para el tamaño $n-1$ (o para la mitad de los elementos, o para el resto de la lista), ¿cómo uso esa respuesta para resolver el problema para el tamaño $n$?*

### Paso 3: Combinar el resultado del subproblema con el estado actual
Escribe la expresión matemática o lógica que une la llamada recursiva con el elemento actual:
* En factorial: `n * factorial(n - 1)`
* En suma de lista: `lista[0] + suma(lista[1:])`
* En invertir cadena: `invertir(cadena[1:]) + cadena[0]`

### Paso 4: Identificar y programar los casos base
Pregúntate: *¿Cuál es la entrada más pequeña y elemental posible para la cual la respuesta es obvia y no requiere descomposición?*

### Plantilla estándar de una función recursiva

```python
def resolver_recursivo(problema):
    # 1. CASO(S) BASE: ¿Es la entrada elemental o indivisible?
    if condicion_de_parada(problema):
        return resultado_trivial
    
    # 2. DESCOMPOSICIÓN: Reducir a un subproblema menor
    subproblema = reducir(problema)
    
    # 3. LLAMADA RECURSIVA: "Salto de fe" (asumir que funciona)
    solucion_subproblema = resolver_recursivo(subproblema)
    
    # 4. COMBINACIÓN: Unir la solución del subproblema con el elemento actual
    return combinar(problema, solucion_subproblema)
```

---

## 3. Cómo identificar y definir casos base

El caso base es el cimiento de la recursión. Si está mal formulado, el programa caerá en un desbordamiento de pila o producirá resultados erróneos.

### 3.1 Criterio de la "Entrada Mínima Indivisible"
Para identificar el caso base, pregúntate qué ocurre en el límite inferior de la estructura de datos:

| Tipo de dato / Problema | Casos base típicos | Valor de retorno trivial |
|-------------------------|--------------------|--------------------------|
| **Enteros / Conteo** ($n$) | $n = 0$ o $n \le 1$ | $0$, $1$, o valor neutro |
| **Cadenas de texto** (`str`) | Longitud 0 (`""`) o 1 | `""` o el mismo carácter |
| **Listas / Arreglos** (`list`) | Lista vacía (`[]`) o de 1 elemento | `0`, `[]`, o `lista[0]` |
| **Árboles binarios / Nodos** | Nodo nulo (`nodo is None`) | `None`, `0`, o valor neutro |
| **Búsquedas con punteros** | Cruce de límites (`izq > der`) | `-1` o `False` (no encontrado) |
| **Tableros / Matrices** | Casilla meta alcanzada o fuera de límites | `True` / `False` |

### 3.2 ¿Cuántos casos base se necesitan?
El número de casos base depende directamente de **cuántos pasos hacia atrás da la llamada recursiva**:

* **Un solo caso base:** Cuando cada llamada reduce el tamaño en 1 ($n - 1$) o a la mitad ($n / 2$).
  * Ejemplo: `factorial(n)` solo consulta `n - 1`. Basta con $n = 0$.
* **Múltiples casos base:** Cuando una llamada consulta múltiples estados previos ($n - 1$ y $n - 2$).
  * Ejemplo: En Fibonacci, $F(n) = F(n-1) + F(n-2)$. Si $n = 2$, requiere $F(1)$ y $F(0)$. Por tanto, son **estrictamente obligatorios dos casos base**: para $n = 0$ y para $n = 1$. Sin ambos, la llamada $F(1)$ intentaría evaluar $F(-1)$, provocando un ciclo infinito.
* **Casos base alternativos (éxito vs. fallo):** En algoritmos de búsqueda o validación, suele haber al menos dos casos base:
  1. *Caso base de éxito:* Se encontró el objetivo (`if elemento == objetivo: return True`).
  2. *Caso base de fallo:* Se agotó el espacio de búsqueda (`if inicio > fin: return False`).

### 3.3 Regla defensiva: Usar desigualdades en lugar de igualdades estrictas
Un error clásico es comparar con igualdad exacta (`if n == 0:`). Si por algún motivo la función recibe un número negativo o decrementa de 2 en 2 con un número impar, **se saltará el caso base**.

```python
# ❌ PELIGROSO: Si n es negativo o si el decremento salta el 0, ciclo infinito
if n == 0:
    return 1

# ✅ DEFENSIVO: Cubre tanto el valor límite como cualquier desbordamiento
if n <= 0:
    return 1
```

---

## 4. Manejo de excepciones, validaciones y el patrón Wrapper

Uno de los errores más comunes al aprender recursividad es mezclar la **validación de errores** con el **caso base**.

### 4.1 Caso Base vs. Excepción / Validación

| Concepto | Propósito | ¿Cuándo ocurre? | Acción |
|----------|-----------|-----------------|--------|
| **Validación de entrada** | Verificar que los datos iniciales cumplen las precondiciones del dominio (tipos válidos, rango permitido). | Al inicio de la ejecución con los argumentos del usuario. | Lanzar excepción (`TypeError`, `ValueError`). |
| **Caso Base** | Detener el algoritmo cuando la reducción recursiva llega a su estado natural más simple. | Al final de la cadena recursiva legítima. | Devolver un valor de retorno normal. |

Por ejemplo, en la función factorial:
* Que $n = 0$ devuelva $1$ es un **caso base**.
* Que alguien ingrese $n = -4$ o $n = 3.14$ es un **error de entrada** que debe lanzar `ValueError` o `TypeError`.

### 4.2 El problema de validar dentro de la función recursiva
Si colocas validaciones de tipo o de dominio dentro de la función recursiva, se evaluarán repetidamente en **cada una** de las $n$ llamadas:

```python
# Ineficiente: valida el tipo y rango en cada llamada recursiva
def factorial_ineficiente(n):
    if not isinstance(n, int):
        raise TypeError("n debe ser un entero")
    if n < 0:
        raise ValueError("n no puede ser negativo")
    if n == 0:
        return 1
    return n * factorial_ineficiente(n - 1)
```

### 4.3 El patrón Función Conductora / Auxiliar (*Wrapper / Helper Pattern*)
La mejor práctica en diseño de software para algoritmos recursivos es desacoplar la validación de la lógica recursiva mediante dos funciones:
1. **Función pública (Wrapper/Conductora):** Valida argumentos una sola vez, prepara estructuras o acumuladores y maneja excepciones.
2. **Función auxiliar recursiva (`_helper`):** Asume datos limpios y se enfoca pura y exclusivamente en el paso recursivo y el caso base.

#### Ejemplo: Factorial robusto con Wrapper

```python
def factorial(n: int) -> int:
    """Función pública (Wrapper): valida precondiciones una sola vez."""
    if not isinstance(n, int):
        raise TypeError(f"El argumento debe ser un número entero, recibido: {type(n).__name__}")
    if n < 0:
        raise ValueError("El factorial no está definido para números enteros negativos.")
    
    # Invoca la función auxiliar interna
    return _factorial_helper(n)

def _factorial_helper(n: int) -> int:
    """Función recursiva auxiliar: sin sobrecarga de validaciones."""
    if n <= 1:
        return 1
    return n * _factorial_helper(n - 1)
```

#### Ejemplo: Búsqueda binaria con interfaz limpia
El patrón Wrapper también evita exponer al usuario parámetros de control interno (como índices o acumuladores):

```python
def busqueda_binaria(datos: list, objetivo) -> int:
    """El usuario solo proporciona la lista y el objetivo.
    El Wrapper valida y configura los punteros iniciales."""
    if not isinstance(datos, list):
        raise TypeError("El argumento 'datos' debe ser una lista.")
    
    # Función auxiliar interna recursiva
    def _buscar(izq: int, der: int) -> int:
        if izq > der:
            return -1  # Caso base 1: elemento no presente
        
        medio = (izq + der) // 2
        if datos[medio] == objetivo:
            return medio  # Caso base 2: elemento encontrado
        elif datos[medio] < objetivo:
            return _buscar(medio + 1, der)
        else:
            return _buscar(izq, medio - 1)

    return _buscar(0, len(datos) - 1)
```

### 4.4 Manejo y captura de `RecursionError`
Python incluye un mecanismo de protección para evitar que el desbordamiento de pila sature la memoria del sistema operativo:

```python
import sys

def ejecucion_segura_recursiva(func, *args, **kwargs):
    """Ejecuta una función recursiva capturando de forma segura el límite de pila."""
    try:
        return func(*args, **kwargs)
    except RecursionError:
        limite = sys.getrecursionlimit()
        print(f"Error: Se excedió la profundidad máxima de recursión permitida ({limite} marcos).")
        print("Recomendación: Transformar el algoritmo a una versión iterativa o incrementar el límite.")
        return None
```

---

## 5. La pila de llamadas (Call Stack)

Cada llamada a cualquier función en Python reserva un bloque en la memoria denominado **marco de pila** (*stack frame*). Este marco contiene:
* Los parámetros recibidos por la función.
* Las variables locales calculadas durante esa invocación.
* La **dirección de retorno**: la instrucción del código a la que se debe volver una vez finalizada la llamada.

En un algoritmo recursivo, cada nueva llamada apila un marco sobre el anterior. La pila no empieza a desahogarse hasta que se alcanza el **caso base**.

Traza de ejecución de `factorial(4)`:

```
[Llamadas descendentes / Apilado]
factorial(4)
 └─ espera: 4 * factorial(3)
                 └─ espera: 3 * factorial(2)
                                 └─ espera: 2 * factorial(1)
                                                 └─ espera: 1 * factorial(0)
                                                                 └─ retorna 1 (CASO BASE)

[Retornos ascendentes / Desapilado]
                                                 └─ calcula: 1 * 1  = 1
                                 └─ calcula: 2 * 1  = 2
                 └─ calcula: 3 * 2  = 6
 └─ calcula: 4 * 6  = 24
Resultado final: 24
```

### Límites de memoria y configuración de la pila
* **Complejidad espacial intrínseca:** Si una función realiza una cadena de $n$ llamadas anidadas, requiere $O(n)$ de memoria adicional únicamente para alojar los marcos de pila.
* Por defecto, el límite en CPython suele ser de $1000$ marcos de pila:

```python
import sys
print(sys.getrecursionlimit())   # Típicamente 1000

# Se puede modificar (usar con precaución para evitar segmentation fault del SO):
sys.setrecursionlimit(3000)
```

---

## 6. Tipos de recursividad

| Tipo | Descripción | Ejemplo típico |
|------|-------------|----------------|
| **Directa** | La función se invoca explícitamente a sí misma dentro de su propio cuerpo. | `factorial(n)` |
| **Indirecta (mutua)** | La función $A$ invoca a la función $B$, y la función $B$ invoca a la función $A$. | `es_par(n)` / `es_impar(n)` |
| **Lineal** | Cada invocación genera como máximo **una** llamada recursiva. | Búsqueda binaria, factorial |
| **Múltiple (arborescente)** | Cada invocación genera **dos o más** llamadas recursivas, creando un árbol de ejecución. | Fibonacci, Torres de Hanoi |
| **De cola (*tail recursion*)** | La llamada recursiva es la **última instrucción** computable antes de retornar; no deja operaciones pendientes. | Factorial con acumulador |
| **Anidada** | Una llamada recursiva recibe como argumento otra llamada a la misma función. | Función de Ackermann |

---

## 7. Ejemplos de código en Python

### 7.1 Suma de los primeros $n$ números naturales
* **Caso base:** $n = 0 \implies 0$
* **Paso recursivo:** $n + \text{suma}(n - 1)$

```python
def suma_naturales(n: int) -> int:
    if n < 0:
        raise ValueError("n debe ser un número entero no negativo")
    if n == 0:
        return 0
    return n + suma_naturales(n - 1)

print(suma_naturales(5))  # 15
```

### 7.2 Potencia: lineal vs. exponenciación binaria

Versión lineal clásica — $O(n)$ en tiempo y espacio de pila:

```python
def potencia(base: float, exp: int) -> float:
    if exp < 0:
        return 1.0 / potencia(base, -exp)
    if exp == 0:
        return 1.0
    return base * potencia(base, exp - 1)
```

Versión optimizada (Divide y Vencerás) — $O(\log n)$ en tiempo y espacio:

```python
def potencia_rapida(base: float, exp: int) -> float:
    if exp < 0:
        return 1.0 / potencia_rapida(base, -exp)
    if exp == 0:
        return 1.0
    
    mitad = potencia_rapida(base, exp // 2)
    if exp % 2 == 0:
        return mitad * mitad
    return base * mitad * mitad

print(potencia_rapida(2, 10))  # 1024.0
```

### 7.3 Sucesión de Fibonacci: Ingenua vs. Memoización

Definición matemática:
$$F(n) = F(n-1) + F(n-2), \quad F(0)=0,\; F(1)=1$$

#### Versión ingenua ($O(2^n)$ tiempo — Ineficiente):
Recalcula repetidamente los mismos subproblemas en un árbol exponencial:

```python
def fib_ingenuo(n: int) -> int:
    if n < 0:
        raise ValueError("n no puede ser negativo")
    if n <= 1:
        return n
    return fib_ingenuo(n - 1) + fib_ingenuo(n - 2)
```

#### Versión con Memoización ($O(n)$ tiempo y $O(n)$ espacio):
Almacena resultados intermedios en un diccionario para reutilizarlos:

```python
def fib_memo(n: int, memo: dict = None) -> int:
    if n < 0:
        raise ValueError("n no puede ser negativo")
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

print(fib_memo(50))  # 12586269025
```

Uso mediante biblioteca estándar:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_lru(n: int) -> int:
    if n <= 1:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)
```

### 7.4 Algoritmo de Euclides (Máximo Común Divisor)
* **Caso base:** Cuando el divisor es $0$, el MCD es el dividendo.
* Complejidad temporal: $O(\log(\min(a, b)))$.

```python
def mcd(a: int, b: int) -> int:
    if b == 0:
        return abs(a)
    return mcd(b, a % b)

print(mcd(48, 18))  # 6
```

### 7.5 Manipulación de cadenas: Invertir y Palíndromos

```python
def invertir_cadena(s: str) -> str:
    # Caso base: cadena vacía o de 1 caracter
    if len(s) <= 1:
        return s
    # Caso recursivo: invertir el resto y añadir el primer caracter al final
    return invertir_cadena(s[1:]) + s[0]

def es_palindromo(s: str) -> bool:
    # Limpieza previa de caracteres no alfanuméricos y minúsculas
    def _verificar(texto: str) -> bool:
        if len(texto) <= 1:
            return True  # Caso base: 0 o 1 letra siempre es palíndromo
        if texto[0] != texto[-1]:
            return False # Caso base de discrepancia
        return _verificar(texto[1:-1])

    s_limpia = "".join(c.lower() for c in s if c.isalnum())
    return _verificar(s_limpia)

print(invertir_cadena("algoritmo"))  # omtirogla
print(es_palindromo("Anita lava la tina"))  # True
```

### 7.6 Torres de Hanoi — Complejidad $O(2^n)$
Problema clásico de recursividad múltiple. Requiere exactamente $2^n - 1$ movimientos mínimos para desplazar $n$ discos.

```python
def hanoi(n: int, origen: str, destino: str, auxiliar: str) -> None:
    if n <= 0:
        return
    if n == 1:
        print(f"Mover disco 1 de {origen} a {destino}")
        return
    
    # 1. Mover n-1 discos del origen al auxiliar usando destino de apoyo
    hanoi(n - 1, origen, auxiliar, destino)
    # 2. Mover el disco mayor directamente al destino
    print(f"Mover disco {n} de {origen} a {destino}")
    # 3. Mover los n-1 discos del auxiliar al destino usando origen de apoyo
    hanoi(n - 1, auxiliar, destino, origen)

hanoi(3, "A", "C", "B")
```

### 7.7 Generación de permutaciones (Backtracking)

```python
def permutaciones(elementos: list) -> list:
    if len(elementos) <= 1:
        return [elementos]
    
    resultado = []
    for i, actual in enumerate(elementos):
        resto = elementos[:i] + elementos[i+1:]
        for sub_perm in permutaciones(resto):
            resultado.append([actual] + sub_perm)
    return resultado

print(permutaciones([1, 2, 3]))
# [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
```

### 7.8 Ordenamiento por Mezcla (Merge Sort) — $O(n \log n)$

```python
def merge_sort(lista: list) -> list:
    if len(lista) <= 1:
        return lista
    
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])
    
    return _mezclar(izquierda, derecha)

def _mezclar(izq: list, der: list) -> list:
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))  # [3, 9, 10, 27, 38, 43, 82]
```

### 7.9 Recorrido de estructuras anidadas y árboles (Aplanar listas)

```python
def aplanar(estructura: list) -> list:
    resultado = []
    for elemento in estructura:
        if isinstance(elemento, list):
            resultado.extend(aplanar(elemento))
        else:
            resultado.append(elemento)
    return resultado

print(aplanar([1, [2, [3, 4], 5], [[6]], 7]))  # [1, 2, 3, 4, 5, 6, 7]
```

---

## 8. Recursividad de cola (Tail Recursion)

Una función presenta **recursividad de cola** cuando la llamada recursiva es la **última acción** a ejecutar antes de que la función retorne su resultado. En este esquema, no queda ninguna operación pendiente (como sumas o multiplicaciones) al regresar.

Para lograr esto, se suele utilizar un parámetro adicional llamado **acumulador** que transporta el estado parcial del cálculo hacia adelante:

```python
# Versión recursiva de cola
def factorial_cola(n: int, acumulador: int = 1) -> int:
    if n <= 1:
        return acumulador
    # La llamada recursiva es pura; no hay multiplicación esperando el retorno
    return factorial_cola(n - 1, n * acumulador)
```

### Optimización de Llamada de Cola (TCO)
En lenguajes funcionales y compilados (Haskell, Scheme, Scala, Kotlin, ES6 en ciertos motores), el compilador detecta la recursividad de cola y reutiliza el mismo marco de pila actual, reduciendo el consumo espacial a **$O(1)$** (equivalente a un bucle `while`).

> **Importante en Python:** CPython **NO implementa TCO**. Guido van Rossum decidió intencionalmente no implementarlo para preservar trazas de pila completas y legibles durante la depuración. Por lo tanto, en Python, incluso una función recursiva de cola consume $O(n)$ marcos de pila y puede lanzar `RecursionError`.

---

## 9. Análisis de complejidad de algoritmos recursivos

El coste computacional de una función recursiva se modela formalmente mediante una **relación de recurrencia**, donde $T(n)$ representa el tiempo necesario para resolver un problema de tamaño $n$.

| Algoritmo | Ecuación de recurrencia | Complejidad Temporal | Complejidad Espacial (pila) |
|-----------|-------------------------|----------------------|-----------------------------|
| Factorial / Suma simple | $T(n) = T(n-1) + O(1)$ | $O(n)$ | $O(n)$ |
| Búsqueda binaria | $T(n) = T(n/2) + O(1)$ | $O(\log n)$ | $O(\log n)$ |
| Merge Sort | $T(n) = 2T(n/2) + O(n)$ | $O(n \log n)$ | $O(n)$ (pila + copias) |
| Fibonacci ingenuo | $T(n) = T(n-1) + T(n-2) + O(1)$ | $O(2^n)$ | $O(n)$ |
| Torres de Hanoi | $T(n) = 2T(n-1) + O(1)$ | $O(2^n)$ | $O(n)$ |

### 9.1 Método de Sustitución hacia atrás (Expansión)
Consiste en expandir sucesivamente la relación hasta detectar el patrón general:

Para $T(n) = T(n-1) + c$ con $T(1) = d$:
$$T(n) = T(n-2) + c + c = T(n-2) + 2c$$
$$T(n) = T(n-3) + 3c$$
$$\dots$$
$$T(n) = T(1) + (n-1)c = d + (n-1)c \implies O(n)$$

### 9.2 Árbol de Recursión
Se desglosa visualmente cada llamada en los nodos de un árbol:
1. Se determina el número de niveles del árbol (profundidad).
2. Se calcula el costo de procesamiento por nivel.
3. Se suma el costo de todos los niveles.

En **Merge Sort**, la profundidad es $\log_2 n$ niveles. En cada nivel se realiza un trabajo de mezcla acumulado de $c \cdot n$. Por lo tanto:
$$\text{Total} = \sum_{i=0}^{\log_2 n} c \cdot n = c \cdot n \log_2 n \implies O(n \log n)$$

### 9.3 El Teorema Maestro
Aplica a recurrencias de la forma "divide y vencerás":

$$T(n) = a\,T\!\left(\frac{n}{b}\right) + f(n), \quad \text{donde } a \ge 1, \; b > 1$$

Donde:
* $a$ es el número de subproblemas generados en cada llamada.
* $b$ es el factor por el cual se divide el tamaño de la entrada.
* $f(n)$ es el trabajo realizado fuera de las llamadas recursivas (dividir y combinar).

Se compara $f(n)$ con la función crítica del número de hojas: $n^{\log_b a}$:

1. **Caso 1:** Si $f(n) = O(n^{\log_b a - \varepsilon})$ para algún $\varepsilon > 0$, entonces:
   $$T(n) = \Theta(n^{\log_b a})$$
2. **Caso 2:** Si $f(n) = \Theta(n^{\log_b a} \log^k n)$ con $k \ge 0$, entonces:
   $$T(n) = \Theta(n^{\log_b a} \log^{k+1} n)$$
3. **Caso 3:** Si $f(n) = \Omega(n^{\log_b a + \varepsilon})$ para algún $\varepsilon > 0$ y se cumple la condición de regularidad $a f(n/b) \le c f(n)$ para $c < 1$:
   $$T(n) = \Theta(f(n))$$

---

## 10. Recursividad vs. Iteración

Todo algoritmo recursivo tiene un equivalente iterativo y viceversa (Teorema de Böhm-Jacopini / Equivalencia de Turing).

| Criterio | Recursividad | Iteración |
|----------|--------------|-----------|
| **Legibilidad y elegancia** | Altísima en estructuras jerárquicas (árboles, grafos, fractales, divide y vencerás). | Más intuitiva en recorridos secuenciales simples. |
| **Consumo de memoria** | $O(\text{profundidad})$ por el almacenamiento de marcos en la pila. | $O(1)$ en la gran mayoría de casos (solo variables de control). |
| **Tiempo de ejecución** | Mayor sobrecarga (*overhead*) debido a la creación/destrucción constante de marcos. | Mayor velocidad bruta de ejecución. |
| **Peligro principal** | Desbordamiento de pila (`RecursionError`). | Bucles infinitos que congelan la CPU sin desbordar memoria. |

### Transformación de recursivo a iterativo

```python
# Versión iterativa de Factorial - O(1) memoria
def factorial_iterativo(n: int) -> int:
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

# Versión iterativa de Fibonacci - O(1) memoria
def fib_iterativo(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

---

## 11. Estrategias algorítmicas basadas en recursividad

1. **Divide y Vencerás (*Divide and Conquer*):**
   * Divide el problema en subproblemas disjuntos del mismo tipo.
   * Conquista resolviendo recursivamente cada subproblema.
   * Combina las soluciones para formular la respuesta global (*Merge Sort, Quick Sort, Búsqueda Binaria*).
2. **Programación Dinámica / Memoización:**
   * Se utiliza cuando los subproblemas se **solapan** (se calculan una y otra vez las mismas ramas).
   * Almacena las respuestas calculadas para responder en $O(1)$ ante futuras consultas idénticas.
3. **Vuelta Atrás (*Backtracking*):**
   * Explora exhaustivamente un espacio de búsqueda mediante un árbol de decisiones.
   * Si en una rama se violan las restricciones, la recursión **retrocede** desarmando el paso para explorar caminos alternativos (*N-Reinas, Sudoku, laberintos*).

---

## 12. Errores comunes y lista de comprobación de diseño

### Errores más frecuentes:
* **Caso base faltante o inalcanzable:** Provoca un ciclo infinito que culmina en `RecursionError`.
* **Argumentos que no convergen:** Llamar a `f(n)` en lugar de `f(n - 1)`, o realizar operaciones donde la entrada crece en lugar de disminuir.
* **Uso ineficiente de memoria con rebanado (*slicing*):** Pasar `lista[1:]` crea una copia física completa de la lista en cada llamada, elevando el costo espacial a $O(n^2)$. Se debe preferir el paso de índices (`inicio`, `fin`).
* **Comparaciones frágiles de parada:** Usar `if n == 0:` en lugar de `if n <= 0:`.
* **Olvido del retorno:** Omitir `return` delante de la llamada recursiva (`f(n-1)` en lugar de `return f(n-1)`), lo que provoca que la función devuelva `None`.

### Lista de comprobación (*Checklist*) para diseñar tu función recursiva:
1. **[ ] ¿Definí el caso base correcto?** ¿Cubre el caso más pequeño posible?
2. **[ ] ¿Utilicé desigualdades defensivas?** (ej. `<= 0` en lugar de `== 0`).
3. **[ ] ¿Las llamadas recursivas reducen el problema?** ¿Está garantizado que convergerán al caso base?
4. **[ ] ¿Validé precondiciones en una función Wrapper?** ¿Están aisladas las excepciones de los casos base?
5. **[ ] ¿Hay subproblemas solapados?** Si es así, ¿implementé memoización?
6. **[ ] ¿Todas las rutas del caso recursivo devuelven un valor con `return`?**

---

## 13. Ejercicios propuestos

1. **Conteo de dígitos:** Implementar una función recursiva que cuente la cantidad de dígitos de un entero positivo sin convertirlo a `str`.
2. **Suma de dígitos:** Dado un número entero positivo $n$, calcular la suma de sus dígitos recursivamente.
3. **Conversión decimal a binario:** Diseñar una función recursiva que retorne la representación binaria en forma de cadena de un número decimal dado.
4. **Coeficiente Binomial:** Calcular el coeficiente binomial $\binom{n}{k}$ utilizando la identidad recursiva del Triángulo de Pascal:
   $$\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}, \quad \text{con } \binom{n}{0} = \binom{n}{n} = 1$$
5. **Conjunto potencia (*Power Set*):** Generar recursivamente todos los subconjuntos posibles de una lista dada de elementos únicos.
6. **Quick Sort:** Implementar el algoritmo de ordenamiento rápido utilizando particionado recursivo.
7. **Resolución de laberintos (Backtracking):** Implementar una función recursiva que determine si existe un camino para salir de una matriz binaria desde $(0,0)$ hasta $(N-1, M-1)$.
