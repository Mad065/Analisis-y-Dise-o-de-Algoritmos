# Apuntes: Divide y Vencerás (*Divide and Conquer*)

**Divide y Vencerás** (*Divide and Conquer*, abreviado frecuentemente como **D&C**) es uno de los paradigmas de diseño de algoritmos más importantes y poderosos de las Ciencias de la Computación. Su principio fundamental consiste en tomar un problema complejo de tamaño $n$, descomponerlo en subproblemas más pequeños **de la misma naturaleza**, resolverlos de manera recursiva y finalmente fusionar sus respuestas para obtener la solución global.

---

## 1. Filosofía y las Tres Fases del Paradigma

Todo algoritmo basado en Divide y Vencerás se estructura en tres etapas claramente diferenciadas en cada nivel de recursión:

1. **Dividir (*Divide*):** Particionar el problema original en uno o varios subproblemas menores que sean instancias más pequeñas del mismo problema.
2. **Vencer / Conquistar (*Conquer*):** Resolver los subproblemas de manera **recursiva**. Si el tamaño de un subproblema es lo suficientemente pequeño (alcanza el **caso base**), se resuelve directamente de forma trivial en tiempo constante $O(1)$.
3. **Combinar (*Combine*):** Unir o ensamblar las soluciones parciales obtenidas de los subproblemas para construir la solución al problema original.

```
                      [ Problema de tamaño n ]
                                 │
                   ┌─────────────┴─────────────┐          1. DIVIDIR
                   ▼                           ▼
         [ Subproblema n/2 ]         [ Subproblema n/2 ]
                   │                           │
              (Recursión)                 (Recursión)     2. VENCER
                   │                           │
                   ▼                           ▼
         [ Solución parcial ]        [ Solución parcial ]
                   └─────────────┬─────────────┘          3. COMBINAR
                                 ▼
                      [ Solución final de n ]
```

### Plantilla general en Python

```python
def divide_y_venceras(problema):
    # 1. CASO BASE (Vencer directamente cuando es pequeño)
    if es_caso_base(problema):
        return resolver_directamente(problema)
    
    # 2. DIVIDIR: Particionar en subproblemas independientes
    subproblemas = dividir(problema)
    
    # 3. VENCER: Resolver recursivamente cada subproblema
    soluciones_parciales = [divide_y_venceras(sub) for sub in subproblemas]
    
    # 4. COMBINAR: Unir respuestas parciales en la solución total
    return combinar(soluciones_parciales)
```

### Distribución del trabajo: ¿Dónde ocurre el esfuerzo?
Dependiendo del algoritmo, el peso computacional recae en fases distintas:
* **División fácil, Combinación costosa:** En **Merge Sort**, dividir toma $O(1)$ (calcular el punto medio), pero combinar las dos mitades ordenadas toma $O(n)$.
* **División costosa, Combinación trivial:** En **Quick Sort**, dividir toma $O(n)$ (reubicar elementos menores y mayores respecto al pivote), pero una vez que las mitades se ordenan recursivamente, ya están en su posición final y combinar toma $O(1)$.
* **Reduce y Vencerás (*Decrease and Conquer*):** Variante donde el problema se divide pero **solo se necesita explorar una de las partes** ($a = 1$), descartando el resto. Ejemplos: **Búsqueda Binaria**, **Quickselect** y **Algoritmo de Euclides**.

---

## 2. ¿Cuándo aplicar Divide y Vencerás?

Para que un problema sea candidato ideal para Divide y Vencerás, debe cumplir tres propiedades:

1. **Subproblemas independientes (Disjuntos):** Los subproblemas generados no deben compartir estado ni depender unos de otros.
   > **Nota crítica:** Si los subproblemas se **solapan** (es decir, se resuelven exactamente los mismos subproblemas repetidas veces, como en Fibonacci), usar Divide y Vencerás puro es ineficiente ($O(2^n)$) y debe emplearse **Programación Dinámica** o **Memoización**.
2. **Autorreferencia (Subestructura recursiva):** Cada subproblema debe ser exactamente el mismo tipo de problema que el original, únicamente con menos datos.
3. **Eficiencia en la división y combinación:** El tiempo invertido en partir el problema y unir las soluciones no debe superar el ahorro obtenido al reducir el tamaño de los datos.

### Comparativa de Paradigmas Algorítmicos

| Característica | Divide y Vencerás | Programación Dinámica | Algoritmos Voraces (*Greedy*) |
|----------------|-------------------|-----------------------|-------------------------------|
| **Relación entre subproblemas** | **Independientes** (no se solapan) | **Solapados** (se reutilizan soluciones) | Se elige solo **una** rama óptima local |
| **Dirección típica** | *Top-Down* (recursivo) | *Top-Down* (memoización) o *Bottom-Up* (tabulación) | Iterativo o recursivo lineal |
| **Objetivo común** | Ordenamiento, búsqueda, álgebra rápida | Optimización global, conteo de caminos | Optimización rápida bajo propiedad voraz |
| **Ejemplo clásico** | Merge Sort, Karatsuba | Mochila 0/1, Fibonacci, Floyd-Warshall | Dijkstra, Kruskal, Cambio de monedas |

---

## 3. Análisis Matemático y el Teorema Maestro

El tiempo de ejecución $T(n)$ de un algoritmo de Divide y Vencerás se modela mediante una **relación de recurrencia**:

$$T(n) = \begin{cases} \Theta(1) & \text{si } n \le n_0 \quad (\text{caso base}) \\ a\,T\!\left(\frac{n}{b}\right) + D(n) + C(n) & \text{si } n > n_0 \quad (\text{paso recursivo}) \end{cases}$$

Agrupando el costo de dividir $D(n)$ y el costo de combinar $C(n)$ en una sola función $f(n) = D(n) + C(n)$, obtenemos la forma estándar:

$$T(n) = a\,T\!\left(\frac{n}{b}\right) + f(n)$$

Donde:
* $a \ge 1$: **Número de subproblemas** que se resuelven recursivamente en cada paso.
* $b > 1$: **Factor de división** del tamaño de la entrada (cada subproblema tiene tamaño $n/b$).
* $f(n)$: **Costo no recursivo** (dividir el problema + combinar las soluciones) en el nivel actual.

### El Árbol de Recursión
Si expandimos la recurrencia en forma de árbol:
* La **altura del árbol** es $\log_b n$ (porque dividimos $n$ entre $b$ sucesivamente hasta llegar a $1$).
* En el nivel $i$ hay $a^i$ subproblemas, cada uno de tamaño $n / b^i$.
* El **número total de hojas** en la base del árbol es:
  $$a^{\log_b n} = n^{\log_b a}$$

### El Teorema Maestro (*Master Theorem*)
El Teorema Maestro resuelve la recurrencia comparando asintóticamente el trabajo realizado en las hojas, **$n^{\log_b a}$**, contra el trabajo de división/combinación en la raíz, **$f(n)$**:

1. **Caso 1 (Dominan las hojas / llamadas recursivas):**
   Si $f(n) = O(n^{\log_b a - \varepsilon})$ para alguna constante $\varepsilon > 0$ (es decir, $f(n)$ crece polinomialmente más lento que $n^{\log_b a}$):
   $$T(n) = \Theta(n^{\log_b a})$$
   *Intuición:* Hay tantos subproblemas que casi todo el trabajo ocurre en la base del árbol.
   *Ejemplo:* Algoritmo de Karatsuba ($a=3, b=2, f(n)=O(n) \implies \Theta(n^{\log_2 3})$).

2. **Caso 2 (Equilibrio entre hojas y niveles):**
   Si $f(n) = \Theta(n^{\log_b a} \log^k n)$ para algún $k \ge 0$ (usualmente $k=0$, por lo que $f(n) = \Theta(n^{\log_b a})$):
   $$T(n) = \Theta(n^{\log_b a} \log^{k+1} n)$$
   *Intuición:* Cada nivel del árbol cuesta exactamente lo mismo, así que el costo total es (costo por nivel) $\times$ (número de niveles $\log n$).
   *Ejemplo:* Merge Sort ($a=2, b=2, f(n)=O(n) \implies \Theta(n \log n)$).

3. **Caso 3 (Domina la raíz / fase de combinación):**
   Si $f(n) = \Omega(n^{\log_b a + \varepsilon})$ para algún $\varepsilon > 0$ (y se cumple la condición de regularidad $a\,f(n/b) \le c\,f(n)$ con $c < 1$):
   $$T(n) = \Theta(f(n))$$
   *Intuición:* El trabajo de dividir y combinar en la llamada inicial es tan grande que eclipsa el costo de todas las llamadas recursivas posteriores.

---

## 4. Algoritmos Clásicos con Implementación en Python

### 4.1 Búsqueda Binaria (*Binary Search*) — $\Theta(\log n)$
Localiza un valor objetivo dentro de un arreglo **previamente ordenado**.
* **Dividir:** Calcula el índice central `medio = (izq + der) // 2`.
* **Vencer:** Compara `arr[medio]` con el objetivo y descarta la mitad donde es imposible que se encuentre ($a = 1, b = 2$).
* **Combinar:** No requiere combinación; el índice hallado se retorna directamente ($f(n) = O(1)$).
* **Recurrencia:** $T(n) = 1 \cdot T(n/2) + O(1) \implies n^{\log_2 1} = n^0 = 1$. Caso 2 del Teorema Maestro $\implies \Theta(\log n)$.

```python
def busqueda_binaria(arr: list, objetivo) -> int:
    def _buscar(izq: int, der: int) -> int:
        # Caso base 1: el espacio de búsqueda se agotó
        if izq > der:
            return -1
        
        # 1. DIVIDIR: hallar punto medio
        medio = (izq + der) // 2
        
        # Caso base 2: elemento encontrado
        if arr[medio] == objetivo:
            return medio
        
        # 2. VENCER: explorar únicamente la mitad correspondiente
        if objetivo < arr[medio]:
            return _buscar(izq, medio - 1)
        else:
            return _buscar(medio + 1, der)

    return _buscar(0, len(arr) - 1)

datos = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print(busqueda_binaria(datos, 23))  # 5
```

---

### 4.2 Ordenamiento por Mezcla (*Merge Sort*) — $\Theta(n \log n)$
Ordena una lista dividiéndola en mitades iguales y fusionando ordenadamente los resultados.
* **Dividir:** Parte la lista de tamaño $n$ en dos sublistas de tamaño $n/2$ ($O(1)$ con índices).
* **Vencer:** Ordena recursivamente la mitad izquierda y la mitad derecha ($a = 2, b = 2$).
* **Combinar:** Mezcla (*merge*) las dos listas ya ordenadas usando dos punteros en tiempo lineal $O(n)$.
* **Recurrencia:** $T(n) = 2T(n/2) + \Theta(n) \implies \Theta(n \log n)$ en el **mejor, promedio y peor caso**.

```python
def merge_sort(arr: list) -> list:
    # Caso base: una lista de 0 o 1 elemento ya está ordenada
    if len(arr) <= 1:
        return arr
    
    # 1. DIVIDIR
    medio = len(arr) // 2
    mitad_izq = arr[:medio]
    mitad_der = arr[medio:]
    
    # 2. VENCER (Llamadas recursivas)
    izq_ordenada = merge_sort(mitad_izq)
    der_ordenada = merge_sort(mitad_der)
    
    # 3. COMBINAR (Fusión ordenada)
    return _merge(izq_ordenada, der_ordenada)

def _merge(izq: list, der: list) -> list:
    fusion = []
    i = j = 0
    
    # Comparar elementos frente a frente de ambas mitades
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            fusion.append(izq[i])
            i += 1
        else:
            fusion.append(der[j])
            j += 1
            
    # Agregar los elementos restantes de cualquiera de las dos mitades
    fusion.extend(izq[i:])
    fusion.extend(der[j:])
    return fusion

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))  # [3, 9, 10, 27, 38, 43, 82]
```

---

### 4.3 Ordenamiento Rápido (*Quick Sort*) — $\Theta(n \log n)$ promedio
A diferencia de Merge Sort, Quick Sort realiza el trabajo pesado durante la **división**.
* **Dividir (Partición):** Elige un elemento como **pivote** y reorganiza el arreglo de modo que todos los elementos menores al pivote queden a su izquierda y todos los mayores a su derecha ($O(n)$).Al finalizar la partición, el pivote ya ocupa su posición definitiva.
* **Vencer:** Ordena recursivamente los subarreglos izquierdo y derecho.
* **Combinar:** No hace nada ($O(1)$), ya que el ordenamiento ocurre en el lugar (*in-place*).
* **Complejidad:**
  * **Mejor caso y Caso promedio:** Particiones balanceadas $\implies T(n) = 2T(n/2) + O(n) \implies O(n \log n)$.
  * **Peor caso:** El pivote es siempre el mínimo o el máximo (ej. arreglo ya ordenado tomando el primer elemento como pivote) $\implies T(n) = T(n-1) + O(n) \implies O(n^2)$. Se mitiga eligiendo un **pivote aleatorio** o la *mediana de tres*.

#### Versión funcional (legible y concisa)

```python
def quicksort_funcional(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    
    pivote = arr[len(arr) // 2]
    menores = [x for x in arr if x < pivote]
    iguales = [x for x in arr if x == pivote]
    mayores = [x for x in arr if x > pivote]
    
    return quicksort_funcional(menores) + iguales + quicksort_funcional(mayores)
```

#### Versión *In-Place* (Esquema de partición de Lomuto con pivote aleatorio — $O(\log n)$ memoria)

```python
import random

def quicksort_inplace(arr: list) -> None:
    def _particionar(bajo: int, alto: int) -> int:
        # Elegir pivote aleatorio para evitar el peor caso O(n^2)
        idx_azar = random.randint(bajo, alto)
        arr[idx_azar], arr[alto] = arr[alto], arr[idx_azar]
        
        pivote = arr[alto]
        i = bajo - 1  # Frontera de elementos menores o iguales al pivote
        
        for j in range(bajo, alto):
            if arr[j] <= pivote:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                
        # Colocar el pivote en su posición final exacta
        arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
        return i + 1

    def _quicksort(bajo: int, alto: int) -> None:
        if bajo < alto:
            # 1. DIVIDIR: particionar y obtener índice del pivote
            indice_pivote = _particionar(bajo, alto)
            # 2. VENCER: ordenar subarreglos izquierdo y derecho
            _quicksort(bajo, indice_pivote - 1)
            _quicksort(indice_pivote + 1, alto)

    _quicksort(0, len(arr) - 1)

lista = [10, 7, 8, 9, 1, 5]
quicksort_inplace(lista)
print(lista)  # [1, 5, 7, 8, 9, 10]
```

---

### 4.4 Exponenciación Rápida (*Binary Exponentiation*) — $\Theta(\log n)$
Calcular $a^n$ multiplicando $a$ por sí mismo $n$ veces cuesta $O(n)$. Con Divide y Vencerás podemos lograrlo en $O(\log n)$ observando que:

$$a^n = \begin{cases} 1 & \text{si } n = 0 \\ \left(a^{n/2}\right)^2 & \text{si } n \text{ es par} \\ a \cdot \left(a^{(n-1)/2}\right)^2 & \text{si } n \text{ es impar} \end{cases}$$

* **Recurrencia:** $T(n) = T(n/2) + O(1) \implies \Theta(\log n)$.

```python
def potencia_rapida(base: float, exp: int) -> float:
    if exp < 0:
        return 1.0 / potencia_rapida(base, -exp)
    # Caso base
    if exp == 0:
        return 1.0
    
    # 1. DIVIDIR Y VENCER: calcular una sola vez la mitad
    mitad = potencia_rapida(base, exp // 2)
    
    # 2. COMBINAR: elevar al cuadrado el resultado parcial
    if exp % 2 == 0:
        return mitad * mitad
    else:
        return base * mitad * mitad

print(potencia_rapida(2, 30))  # 1073741824.0 (en solo 5 llamadas en vez de 30)
```

---

### 4.5 Problema del Subarreglo de Suma Máxima (*Maximum Subarray*) — $\Theta(n \log n)$
Dado un arreglo de números (positivos y negativos), encontrar el subarreglo contiguo cuyos elementos sumen el valor máximo posible.
* **Dividir:** Partir el arreglo a la mitad en `medio`.
* **Vencer:** El subarreglo óptimo debe encontrarse en uno de tres lugares posibles:
  1. Completamente en la **mitad izquierda** (resuelto recursivamente).
  2. Completamente en la **mitad derecha** (resuelto recursivamente).
  3. **Cruzando el punto medio** (se calcula en $O(n)$ extendiéndose desde el centro hacia la izquierda y hacia la derecha).
* **Combinar:** Devolver el máximo entre los tres valores anteriores.
* **Recurrencia:** $T(n) = 2T(n/2) + \Theta(n) \implies \Theta(n \log n)$ (mejora la fuerza bruta de $O(n^2)$).

```python
def suma_maxima_cruzada(arr: list, izq: int, medio: int, der: int) -> int:
    # Mejor suma extendiéndose desde el centro hacia la izquierda
    suma_izq = float('-inf')
    actual = 0
    for i in range(medio, izq - 1, -1):
        actual += arr[i]
        if actual > suma_izq:
            suma_izq = actual
            
    # Mejor suma extendiéndose desde el centro+1 hacia la derecha
    suma_der = float('-inf')
    actual = 0
    for j in range(medio + 1, der + 1):
        actual += arr[j]
        if actual > suma_der:
            suma_der = actual
            
    return suma_izq + suma_der

def max_subarreglo_dc(arr: list) -> int:
    if not arr:
        raise ValueError("El arreglo no puede estar vacío")

    def _resolver(izq: int, der: int) -> int:
        # Caso base: un único elemento
        if izq == der:
            return arr[izq]
        
        # 1. DIVIDIR
        medio = (izq + der) // 2
        
        # 2. VENCER (Izquierda y Derecha) + 3. COMBINAR (Cruzado)
        max_izq = _resolver(izq, medio)
        max_der = _resolver(medio + 1, der)
        max_cruz = suma_maxima_cruzada(arr, izq, medio, der)
        
        return max(max_izq, max_der, max_cruz)

    return _resolver(0, len(arr) - 1)

datos = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarreglo_dc(datos))  # 6 (correspondiente al subarreglo [4, -1, 2, 1])
```

---

### 4.6 Selección Rápida (*Quickselect*) — $\Theta(n)$ promedio
Encuentra el $k$-ésimo elemento más pequeño de un arreglo desordenado sin necesidad de ordenar todo el arreglo (lo cual costaría $O(n \log n)$).
* **Idea:** Usa la misma partición de Quick Sort. Una vez colocado el pivote en su índice `p`:
  * Si `k == p`, encontramos el elemento y terminamos.
  * Si `k < p`, buscamos recursivamente **solo en la izquierda**.
  * Si `k > p`, buscamos recursivamente **solo en la derecha**.
* **Recurrencia en caso promedio:** Como solo hacemos **una** llamada recursiva ($a=1, b=2$) con trabajo lineal $f(n)=O(n)$:
  $$T(n) = T(n/2) + c \cdot n = c n + c\frac{n}{2} + c\frac{n}{4} + \dots \le 2cn \implies \Theta(n)$$

```python
import random

def quickselect(arr: list, k: int):
    """Devuelve el elemento en la posición k (0-indexado) si el arreglo estuviera ordenado."""
    if not (0 <= k < len(arr)):
        raise IndexError("k está fuera de los límites del arreglo")

    def _seleccionar(lista: list, k_actual: int):
        if len(lista) == 1:
            return lista[0]
        
        pivote = random.choice(lista)
        menores = [x for x in lista if x < pivote]
        iguales = [x for x in lista if x == pivote]
        mayores = [x for x in lista if x > pivote]
        
        if k_actual < len(menores):
            return _seleccionar(menores, k_actual)
        elif k_actual < len(menores) + len(iguales):
            return pivote  # Caso base de éxito
        else:
            return _seleccionar(mayores, k_actual - len(menores) - len(iguales))

    return _seleccionar(arr, k)

print(quickselect([7, 10, 4, 3, 20, 15], 2))  # 7 (el 3er más pequeño: 3, 4, 7...)
```

---

### 4.7 Reducción Algebraica de Subproblemas: Karatsuba y Strassen
Una de las lecciones más profundas de Divide y Vencerás es que **disminuir el número de llamadas recursivas ($a$) a costa de hacer unas cuantas sumas más reduce el exponente de la complejidad**.

#### Multiplicación de Enteros de Karatsuba:
* **Divide y Vencerás ingenuo:** Divide dos números de $n$ dígitos en mitades y hace $4$ multiplicaciones recursivas de tamaño $n/2$:
  $$T(n) = 4T(n/2) + O(n) \implies \Theta(n^{\log_2 4}) = \Theta(n^2) \quad (\text{no mejora el método escolar})$$
* **Truco de Karatsuba:** Reemplaza una multiplicación por sumas algebraicas, dejando solo **$3$ llamadas recursivas** ($z_0, z_1, z_2$):
  $$T(n) = 3T(n/2) + O(n) \implies \Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$$
  *(Ver desarrollo completo y código en el apunte de `Algoritmos de multiplicacion.md`)*.

#### Multiplicación de Matrices de Strassen (1969):
* Multiplicar dos matrices de $n \times n$ por definición toma $O(n^3)$ (o $8$ subproblemas de tamaño $n/2 \times n/2$, donde $n^{\log_2 8} = n^3$).
* Volker Strassen descubrió una combinación algebraica para multiplicar bloques usando **7 productos recursivos** en lugar de 8:
  $$T(n) = 7T(n/2) + O(n^2) \implies \Theta(n^{\log_2 7}) \approx \Theta(n^{2.807})$$

---

### 4.8 Conteo de Inversiones en un Arreglo — $\Theta(n \log n)$
Una **inversión** en un arreglo es un par de índices $(i, j)$ tal que $i < j$ pero $\text{arr}[i] > \text{arr}[j]$ (mide qué tan "desordenado" está un arreglo).
* Fuerza bruta: comparar todos los pares toma $O(n^2)$.
* **Divide y Vencerás (basado en Merge Sort):** Contamos las inversiones en la mitad izquierda, en la mitad derecha y las **inversiones cruzadas** durante el paso de mezcla (`_merge`). Si al mezclar tomamos un elemento de la mitad derecha `der[j]` antes que `izq[i]`, sabemos instantáneamente que `der[j]` es menor que **todos los elementos restantes** en `izq` (desde `i` hasta el final de `izq`).

```python
def contar_inversiones(arr: list) -> tuple[list, int]:
    """Retorna una tupla (arreglo_ordenado, numero_de_inversiones)."""
    if len(arr) <= 1:
        return arr, 0
    
    medio = len(arr) // 2
    izq, inv_izq = contar_inversiones(arr[:medio])
    der, inv_der = contar_inversiones(arr[medio:])
    mezcla, inv_cruz = _merge_y_contar(izq, der)
    
    return mezcla, inv_izq + inv_der + inv_cruz

def _merge_y_contar(izq: list, der: list) -> tuple[list, int]:
    fusion = []
    i = j = inversiones = 0
    
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            fusion.append(izq[i])
            i += 1
        else:
            fusion.append(der[j])
            # Todos los elementos desde izq[i] hasta el final forman inversión con der[j]
            inversiones += len(izq) - i
            j += 1
            
    fusion.extend(izq[i:])
    fusion.extend(der[j:])
    return fusion, inversiones

_, total_inv = contar_inversiones([2, 4, 1, 3, 5])
print(total_inv)  # 3 inversiones: (2,1), (4,1), (4,3)
```

---

## 5. Tabla Resumen de Complejidades

| Algoritmo | Fuerza Bruta | Recurrencia D&C | Parámetros ($a, b, f(n)$) | Caso Maestro | Complejidad D&C |
|-----------|--------------|-----------------|---------------------------|--------------|-----------------|
| **Búsqueda Binaria** | $O(n)$ | $T(n) = T(n/2) + O(1)$ | $a=1, b=2, O(1)$ | Caso 2 | $\Theta(\log n)$ |
| **Exponenciación Rápida** | $O(n)$ | $T(n) = T(n/2) + O(1)$ | $a=1, b=2, O(1)$ | Caso 2 | $\Theta(\log n)$ |
| **Quickselect (Promedio)** | $O(n \log n)$ | $T(n) = T(n/2) + O(n)$ | $a=1, b=2, O(n)$ | Caso 3 | $\Theta(n)$ |
| **Merge Sort** | $O(n^2)$ | $T(n) = 2T(n/2) + O(n)$ | $a=2, b=2, O(n)$ | Caso 2 | $\Theta(n \log n)$ |
| **Quick Sort (Promedio)** | $O(n^2)$ | $T(n) = 2T(n/2) + O(n)$ | $a=2, b=2, O(n)$ | Caso 2 | $\Theta(n \log n)$ |
| **Subarreglo Suma Máxima** | $O(n^2)$ | $T(n) = 2T(n/2) + O(n)$ | $a=2, b=2, O(n)$ | Caso 2 | $\Theta(n \log n)$ |
| **Par de Puntos Más Cercanos** | $O(n^2)$ | $T(n) = 2T(n/2) + O(n)$ | $a=2, b=2, O(n)$ | Caso 2 | $\Theta(n \log n)$ |
| **Multiplicación Karatsuba** | $O(n^2)$ | $T(n) = 3T(n/2) + O(n)$ | $a=3, b=2, O(n)$ | Caso 1 | $\Theta(n^{1.585})$ |
| **Matrices de Strassen** | $O(n^3)$ | $T(n) = 7T(n/2) + O(n^2)$ | $a=7, b=2, O(n^2)$ | Caso 1 | $\Theta(n^{2.807})$ |

---

## 6. Ventajas, Desventajas y Optimizaciones en Producción

### Ventajas
1. **Salto asintótico radical:** Transforma problemas cuadráticos $O(n^2)$ en casi lineales $O(n \log n)$, o problemas lineales $O(n)$ en logarítmicos $O(\log n)$.
2. **Paralelismo natural:** Como los subproblemas son completamente independientes entre sí, pueden enviarse a distintos núcleos de CPU, hilos o nodos distribuidos (base del modelo *MapReduce*).
3. **Eficiencia en memoria caché (*Cache Locality*):** Al reducir los subproblemas recursivamente, llega un punto en que caben íntegros en la caché L1/L2 del procesador, acelerando drásticamente los accesos a memoria.

### Desventajas
1. **Sobrecarga (*overhead*) de recursión en entradas pequeñas:** Llamar miles de veces a la función para subproblemas diminutos (tamaño 1, 2 o 3) es más lento que un simple ciclo `for`.
2. **Consumo de pila y memoria auxiliar:** Algoritmos como Merge Sort requieren $O(n)$ de espacio adicional para mezclar, además del espacio en el *Call Stack*.

### Optimización Híbrida: Umbral de Corte (*Cut-off to Insertion Sort*)
En bibliotecas reales de producción (como `timsort` en Python o `std::sort` en C++), los algoritmos de Divide y Vencerás **no bajan hasta el caso base $n = 1$**. En su lugar, definen un umbral experimental (típicamente $k \in [16, 64]$): cuando el subproblema tiene tamaño $\le k$, se detiene la recursión y se resuelve directamente con **Insertion Sort** (que tiene constantes ocultas pequeñísimas y es sumamente veloz en arreglos casi ordenados o pequeños).

---

## 7. Ejercicios Propuestos

1. **Elemento Mayoritario (*Majority Element*):** Dado un arreglo de tamaño $n$, encontrar mediante Divide y Vencerás en $O(n \log n)$ el elemento que aparece más de $\lfloor n/2 \rfloor$ veces.
2. **Encontrar un Elemento Pico (*Peak Element*):** En un arreglo donde `arr[i] != arr[i+1]`, un elemento pico es aquel que es mayor que sus vecinos inmediatos. Diseña un algoritmo tipo Búsqueda Binaria que encuentre cualquier pico en tiempo $O(\log n)$.
3. **Búsqueda de Punto Fijo:** Dado un arreglo ordenado de enteros distintos (pueden ser negativos), diseñar un algoritmo $O(\log n)$ que determine si existe algún índice $i$ tal que $\text{arr}[i] == i$.
4. **Mínimo y Máximo Simultáneos:** Implementar una función Divide y Vencerás que encuentre tanto el mínimo como el máximo de un arreglo de tamaño $n$ usando como máximo $\frac{3n}{2} - 2$ comparaciones (mejor que las $2n - 2$ comparaciones del recorrido lineal tradicional).
5. **Búsqueda en Arreglo Ordenado y Rotado:** Dado un arreglo ordenado que fue rotado en algún pivote desconocido (ej. `[4, 5, 6, 7, 0, 1, 2]`), encontrar un elemento objetivo en tiempo $O(\log n)$.
