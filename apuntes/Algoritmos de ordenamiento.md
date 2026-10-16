# Apuntes: Algoritmos de Ordenamiento

El **ordenamiento** (*sorting*) es uno de los problemas más estudiados y fundamentales en las Ciencias de la Computación. Consiste en tomar una colección de elementos $\langle a_1, a_2, \dots, a_n \rangle$ y reorganizarlos en una permutación $\langle a'_1, a'_2, \dots, a'_n \rangle$ que cumpla una relación de orden total (generalmente no decreciente: $a'_1 \le a'_2 \le \dots \le a'_n$).

Contar con datos ordenados es el requisito indispensable para habilitar algoritmos de búsqueda ultrarrápidos (como la **Búsqueda Binaria**, **Jump Search** o **Interpolation Search**), detectar duplicados en tiempo lineal, construir índices en bases de datos y optimizar el procesamiento de grandes volúmenes de información.

---

## Conceptos Clave para Clasificar Algoritmos de Ordenamiento

Antes de analizar cada algoritmo, es importante conocer los cuatro criterios técnicos con los que se evalúan:

1. **Complejidad Temporal:** Cantidad de operaciones que realiza en el **mejor caso** (datos ya ordenados), **caso promedio** (datos aleatorios) y **peor caso** (datos en orden inverso o configuraciones patológicas).
2. **Complejidad Espacial (Memoria Auxiliar):**
   * **In-place ($O(1)$ o $O(\log n)$):** Ordena los elementos directamente sobre el arreglo original utilizando una cantidad constante (o logarítmica por la pila de recursión) de memoria adicional.
   * **Out-of-place ($O(n)$ o $O(n + k)$):** Requiere reservar arreglos o estructuras auxiliares proporcionales al tamaño de la entrada.
3. **Estabilidad:** Un algoritmo es **estable** si preserva el orden relativo original de los elementos que tienen claves iguales.
   > 💡 **Ejemplo de estabilidad:** Si tienes una lista de alumnos ordenada alfabéticamente por nombre y luego la ordenas por calificación usando un algoritmo **estable**, los alumnos que empaten con `10` seguirán apareciendo en orden alfabético entre sí.
4. **Mecanismo de Ordenamiento:**
   * **Basados en comparaciones:** Deciden el orden comparando pares de elementos ($a_i < a_j$). Teóricamente, ningún algoritmo basado en comparaciones puede tener un peor caso mejor que $\Omega(n \log n)$.
   * **No basados en comparaciones:** Aprovechan propiedades internas de las claves (valor numérico, dígitos o distribución) para alcanzar tiempos lineales $O(n)$.

---

## Parte I: Algoritmos Elementales o Cuadráticos — $O(n^2)$

Son algoritmos sencillos de implementar e intuitivos, ideales para comprender las bases o para ordenar arreglos muy pequeños, pero inviables cuando el volumen de datos crece a cientos de miles o millones de elementos.

---

### 1. Ordenamiento Burbuja (Bubble Sort)

Es el algoritmo de ordenamiento más básico. Funciona recorriendo repetidamente el arreglo y comparando pares de elementos **adyacentes**; si están en el orden incorrecto, los intercambia. En cada pasada completa, el elemento más grande "burbujea" (flota) hacia su posición final al extremo derecho del arreglo.

* **Paradigma:** Iterativo por intercambios adyacentes (Fuerza Bruta).
* **Complejidad Temporal:** $O(n^2)$ en el caso promedio y peor caso. $O(n)$ en el mejor caso (si se aplica la optimización de parada temprana).
* **Espacio Auxiliar:** $O(1)$ (*in-place*).
* **Estabilidad:** Sí (solo intercambia si $a[j] > a[j+1]$ de forma estricta).
* **Uso ideal:** Fines educativos o verificar rápidamente si una lista ya está ordenada.

#### Optimización Clave (vista en Práctica 2)
En lugar de reducir el límite en $1$ por cada pasada o usar solo una bandera booleana, podemos guardar el **índice del último intercambio realizado**. Todo lo que esté a la derecha de ese índice ya quedó ordenado y no necesita volver a compararse. Si en una pasada no ocurre ningún intercambio (`ultimo == 0`), el algoritmo termina de inmediato.

```
Pasada 1 sobre [5, 1, 4, 2, 8]:
(5, 1) -> [1, 5, 4, 2, 8]  (intercambio en j=0)
(5, 4) -> [1, 4, 5, 2, 8]  (intercambio en j=1)
(5, 2) -> [1, 4, 2, 5, 8]  (intercambio en j=2)
(5, 8) -> [1, 4, 2, 5, 8]  (no hay intercambio; el 5 y el 8 ya están en su lugar)
```

#### Implementación en Python

```python
def bubble_sort(arreglo):
    """
    Ordena un arreglo in-place usando Bubble Sort optimizado.
    Rastrea la posición del último intercambio para acortar las pasadas.
    """
    limite = len(arreglo) - 1
    while limite > 0:
        ultimo_intercambio = 0
        for j in range(limite):
            if arreglo[j] > arreglo[j + 1]:
                arreglo[j], arreglo[j + 1] = arreglo[j + 1], arreglo[j]
                ultimo_intercambio = j
        limite = ultimo_intercambio
    return arreglo

# Prueba rápida
datos = [64, 34, 25, 12, 22, 11, 90]
print(bubble_sort(datos))  # Salida: [11, 12, 22, 25, 34, 64, 90]
```

---

### 2. Ordenamiento por Selección (Selection Sort)

Divide conceptualmente el arreglo en dos partes: una sublista izquierda ya ordenada y una sublista derecha por ordenar. En cada iteración, busca el **elemento mínimo** de la parte desordenada y lo intercambia con el primer elemento de dicha parte.

* **Paradigma:** Selección iterativa exhaustiva.
* **Complejidad Temporal:** $O(n^2)$ en **todos los casos** (mejor, promedio y peor), ya que siempre recorre el resto del arreglo para confirmar cuál es el mínimo.
* **Espacio Auxiliar:** $O(1)$ (*in-place*).
* **Estabilidad:** No (los intercambios a larga distancia pueden alterar el orden de elementos iguales).
* **Uso ideal:** Situaciones donde **escribir en memoria es extremadamente costoso** (como memorias EEPROM o Flash antiguas), pues realiza a lo sumo $O(n)$ intercambios en total, a diferencia de los $O(n^2)$ intercambios de Bubble Sort.

#### Implementación en Python

```python
def selection_sort(arreglo):
    """
    Ordena un arreglo buscando sucesivamente el elemento mínimo
    y colocándolo en su posición final.
    """
    n = len(arreglo)
    for i in range(n - 1):
        indice_min = i
        # Buscar el mínimo en el subarreglo desordenado [i+1 .. n-1]
        for j in range(i + 1, n):
            if arreglo[j] < arreglo[indice_min]:
                indice_min = j
        
        # Intercambiar solo si encontramos un elemento menor
        if indice_min != i:
            arreglo[i], arreglo[indice_min] = arreglo[indice_min], arreglo[i]
            
    return arreglo

# Prueba rápida
datos = [29, 10, 14, 37, 13]
print(selection_sort(datos))  # Salida: [10, 13, 14, 29, 37]
```

---

### 3. Ordenamiento por Inserción (Insertion Sort)

Construye el arreglo ordenado final tomando un elemento a la vez e insertándolo en la posición correcta dentro de la parte izquierda ya ordenada, desplazando hacia la derecha los elementos mayores.

* **Paradigma:** Incremental (*Decrease and Conquer*).
* **Complejidad Temporal:** $O(n^2)$ en el caso promedio y peor caso. $O(n)$ en el mejor caso (cuando el arreglo está ordenado o casi ordenado).
* **Espacio Auxiliar:** $O(1)$ (*in-place*).
* **Estabilidad:** Sí.
* **Uso ideal:** Arreglos pequeños ($n \le 32$), flujos de datos en tiempo real (*online algorithms*, donde los datos van llegando uno por uno) y colecciones **casi ordenadas**.

> 💡 **Analogía:** Es exactamente la forma en que la mayoría de las personas ordenan una mano de cartas en un juego de mesa: tomas una carta nueva con la mano derecha y la deslizas entre las cartas de tu mano izquierda hasta dejarla en su lugar correcto.

#### Implementación en Python

```python
def insertion_sort(arreglo):
    """
    Ordena un arreglo insertando cada elemento en su posición correcta
    dentro del subarreglo izquierdo previamente ordenado.
    """
    for i in range(1, len(arreglo)):
        clave = arreglo[i]
        j = i - 1
        
        # Desplazar elementos de arreglo[0..i-1] que sean mayores que la clave
        while j >= 0 and arreglo[j] > clave:
            arreglo[j + 1] = arreglo[j]
            j -= 1
            
        arreglo[j + 1] = clave
    return arreglo

# Prueba rápida
datos = [12, 11, 13, 5, 6]
print(insertion_sort(datos))  # Salida: [5, 6, 11, 12, 13]
```

---

### 4. Ordenamiento Shell (Shell Sort)

Propuesto por Donald Shell en 1959, es una generalización e ingeniosa optimización de **Insertion Sort**. El problema de Insertion Sort es que solo mueve elementos una posición a la vez; si el número más pequeño está al final del arreglo, requiere $n$ desplazamientos para llegar al inicio. Shell Sort soluciona esto comparando e intercambiando elementos separados por una **brecha** (*gap*) grande que se va reduciendo progresivamente hasta llegar a `gap = 1` (donde ejecuta un Insertion Sort final sobre un arreglo que ya está casi ordenado).

* **Paradigma:** Inserción por incrementos decrecientes.
* **Complejidad Temporal:** Depende de la secuencia de brechas elegida: $O(n^2)$ con la secuencia original ($n/2, n/4, \dots, 1$), pero baja a $O(n^{3/2})$ con la secuencia de Knuth o hasta $O(n \log^2 n)$ con secuencias avanzadas (Sedgewick / Ciura).
* **Espacio Auxiliar:** $O(1)$ (*in-place*).
* **Estabilidad:** No.
* **Uso ideal:** Sistemas embebidos o de recursos limitados donde se requiere un código muy corto, sin recursión, sin memoria extra $O(1)$ y mucho más rápido que $O(n^2)$.

#### Implementación en Python

```python
def shell_sort(arreglo):
    """
    Ordena un arreglo utilizando Shell Sort con reducción de brecha (gap).
    """
    n = len(arreglo)
    gap = n // 2  # Brecha inicial
    
    while gap > 0:
        # Realizar un Insertion Sort con salto 'gap'
        for i in range(gap, n):
            temp = arreglo[i]
            j = i
            while j >= gap and arreglo[j - gap] > temp:
                arreglo[j] = arreglo[j - gap]
                j -= gap
            arreglo[j] = temp
        gap //= 2  # Reducir la brecha a la mitad
        
    return arreglo

# Prueba rápida
datos = [23, 29, 15, 19, 31, 7, 9, 5, 2]
print(shell_sort(datos))  # Salida: [2, 5, 7, 9, 15, 19, 23, 29, 31]
```

---

## Parte II: Algoritmos Eficientes de Comparación — $O(n \log n)$

Mediante el uso de **Divide y Vencerás** o **Estructuras de Datos jerárquicas** (árboles y montículos), estos algoritmos logran romper la barrera cuadrática y escalan a decenas o cientos de millones de datos en cuestión de segundos.

---

### 5. Ordenamiento por Mezcla (Merge Sort)

Diseñado por John von Neumann en 1945, es el ejemplo canónico del paradigma **Divide y Vencerás**. Divide el arreglo por la mitad en dos subarreglos, ordena cada mitad recursivamente y luego **fusiona** (*merge*) ambas mitades ordenadas en un solo arreglo ordenado.

* **Paradigma:** Divide y Vencerás (*Divide and Conquer*).
* **Relación de Recurrencia:** $T(n) = 2T(n/2) + \Theta(n) \implies \Theta(n \log n)$ por el Caso 2 del Teorema Maestro.
* **Complejidad Temporal:** $O(n \log n)$ garantizado en el **mejor, promedio y peor caso**.
* **Espacio Auxiliar:** $O(n)$ (necesita un buffer auxiliar para realizar la mezcla).
* **Estabilidad:** Sí (cuando ante empate se toma primero el elemento de la mitad izquierda).
* **Uso ideal:** Ordenamiento de listas enlazadas, ordenamiento externo (archivos gigantes en disco que no caben en RAM) y casos donde se exige **estabilidad** y tiempo $O(n \log n)$ sin excepciones.

```
                  [38, 27, 43, 3]
                   /           \
            [38, 27]           [43, 3]         <-- Fase DIVIDIR
             /    \             /    \
          [38]    [27]       [43]    [3]
             \    /             \    /
            [27, 38]           [3, 43]         <-- Fase COMBINAR (Merge)
                   \           /
                  [3, 27, 38, 43]
```

> 📝 **Optimización de Memoria (Práctica 2):** Crear nuevos arreglos temporales en cada llamada recursiva satura al recolector de basura (*Garbage Collector*). En implementaciones de alto rendimiento, se reserva **un único arreglo auxiliar de tamaño $n$** al inicio y se reutiliza en todas las llamadas recursivas pasando índices `lo`, `mid` y `hi`.

#### Implementación en Python

```python
def merge_sort(arreglo):
    """
    Ordena un arreglo utilizando el algoritmo Merge Sort.
    Reserva un único buffer auxiliar O(n) para optimizar el uso de memoria.
    """
    n = len(arreglo)
    if n < 2:
        return arreglo
        
    aux = [None] * n
    
    def _sort(lo, hi):
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        _sort(lo, mid)
        _sort(mid, hi)
        
        # Copiar el rango actual al buffer auxiliar
        aux[lo:hi] = arreglo[lo:hi]
        
        # Fusionar las dos mitades ordenadas de regreso en 'arreglo'
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            if aux[j] < aux[i]:  # '<' estricto preserva la estabilidad
                arreglo[k] = aux[j]
                j += 1
            else:
                arreglo[k] = aux[i]
                i += 1
            k += 1
            
        # Copiar los elementos restantes de la mitad izquierda (si quedan)
        while i < mid:
            arreglo[k] = aux[i]
            i += 1
            k += 1
        # (Los restantes de la mitad derecha ya están en su posición final)

    _sort(0, n)
    return arreglo

# Prueba rápida
datos = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort(datos))  # Salida: [3, 9, 10, 27, 38, 43, 82]
```

---

### 6. Ordenamiento Rápido (Quick Sort)

Desarrollado por Tony Hoare en 1959, es uno de los algoritmos más rápidos y utilizados en la práctica. También emplea **Divide y Vencerás**, pero invierte la carga de trabajo respecto a Merge Sort: elige un elemento llamado **pivote** y **particiona** el arreglo in-place de modo que todos los elementos menores que el pivote queden a su izquierda y los mayores a su derecha. Al finalizar la partición, el pivote ya está en su posición definitiva y solo resta ordenar recursivamente ambos lados.

* **Paradigma:** Divide y Vencerás (con trabajo pesado en la fase de división).
* **Complejidad Temporal:** $O(n \log n)$ en el mejor caso y caso promedio. **$O(n^2)$ en el peor caso** (ocurre si el pivote elegido es siempre el mínimo o el máximo, p. ej., al elegir el primer/último elemento en un arreglo ya ordenado).
* **Espacio Auxiliar:** $O(\log n)$ para la pila de llamadas recursivas (ordena los datos *in-place*).
* **Estabilidad:** No (en su versión *in-place* estándar).
* **Uso ideal:** Ordenamiento de propósito general en memoria RAM cuando no se requiere estabilidad; posee excelente localidad de caché y bajas constantes ocultas.

> 💡 **¿Cómo evitar el peor caso $O(n^2)$?** Nunca elijas ciegamente el primer o último elemento como pivote. Usa un **pivote aleatorio** o la **mediana de tres** (la mediana entre el primer, el central y el último elemento del subarreglo).

#### Implementación en Python (Partición de Lomuto con Mediana de Tres)

```python
def quick_sort(arreglo):
    """
    Ordena un arreglo in-place usando Quick Sort.
    Utiliza selección de pivote por 'mediana de tres' para evitar el peor caso O(n^2).
    """
    def _particionar(bajo, alto):
        # Elegir mediana entre bajo, medio y alto como pivote
        medio = (bajo + alto) // 2
        if arreglo[medio] < arreglo[bajo]:
            arreglo[bajo], arreglo[medio] = arreglo[medio], arreglo[bajo]
        if arreglo[alto] < arreglo[bajo]:
            arreglo[bajo], arreglo[alto] = arreglo[alto], arreglo[bajo]
        if arreglo[medio] < arreglo[alto]:
            arreglo[medio], arreglo[alto] = arreglo[alto], arreglo[medio]
            
        pivote = arreglo[alto]
        i = bajo - 1  # Índice del último elemento menor o igual al pivote
        
        for j in range(bajo, alto):
            if arreglo[j] <= pivote:
                i += 1
                arreglo[i], arreglo[j] = arreglo[j], arreglo[i]
                
        # Colocar el pivote en su posición final definitiva
        arreglo[i + 1], arreglo[alto] = arreglo[alto], arreglo[i + 1]
        return i + 1

    def _quick_sort(bajo, alto):
        if bajo < alto:
            indice_pivote = _particionar(bajo, alto)
            _quick_sort(bajo, indice_pivote - 1)
            _quick_sort(indice_pivote + 1, alto)

    _quick_sort(0, len(arreglo) - 1)
    return arreglo

# Prueba rápida
datos = [10, 7, 8, 9, 1, 5]
print(quick_sort(datos))  # Salida: [1, 5, 7, 8, 9, 10]
```

---

### 7. Ordenamiento por Montículos (Heap Sort)

Propuesto por J. W. J. Williams en 1964, es una versión mejorada de Selection Sort que utiliza una estructura de datos llamada **Montículo Binario Máximo** (*Max-Heap*) para encontrar el elemento máximo en tiempo $O(\log n)$ en lugar de $O(n)$.

Un *Max-Heap* es un árbol binario casi completo donde todo nodo padre es mayor o igual que sus hijos, y se representa directamente sobre el mismo arreglo sin usar punteros: para un nodo en el índice $i$, su hijo izquierdo está en $2i + 1$ y su hijo derecho en $2i + 2$.

El algoritmo consta de dos fases:
1. **Construcción del Max-Heap (*Heapify bottom-up*):** Convierte el arreglo desordenado en un Max-Heap en tiempo lineal $O(n)$ hundiendo (`sift_down`) los nodos internos desde $\lfloor n/2 \rfloor - 1$ hasta $0$.
2. **Extracción sucesiva:** Como el elemento más grande siempre está en la raíz (`arreglo[0]`), se intercambia con el último elemento del montículo activo, se reduce el tamaño del montículo en $1$ y se restaura la propiedad del Max-Heap aplicando `sift_down` a la nueva raíz en $O(\log n)$.

* **Paradigma:** Selección asistida por estructura de datos (*Max-Heap*).
* **Complejidad Temporal:** $O(n \log n)$ garantizado en el **mejor, promedio y peor caso**.
* **Espacio Auxiliar:** $O(1)$ estricto (*in-place*).
* **Estabilidad:** No.
* **Uso ideal:** Sistemas con **restricción estricta de memoria RAM** o sistemas de tiempo real donde se necesita garantía absoluta de $O(n \log n)$ en el peor caso con $0\text{ MB}$ de memoria extra.

> 📝 **Observación Práctica (Práctica 2):** Aunque tanto Merge Sort como Heap Sort son $O(n \log n)$, en la práctica Merge Sort suele ser entre $2\times$ y $3\times$ más rápido en arreglos gigantes ($n = 10^8$). Esto se debe a la **localidad de caché**: Merge Sort recorre memoria contigua, mientras que Heap Sort salta constantemente entre índices $i$ y $2i+1$, provocando fallos de caché (*cache misses*). A cambio, Heap Sort no gasta memoria adicional.

#### Implementación en Python

```python
def _sift_down(arreglo, i, n):
    """Hunde el elemento arreglo[i] dentro del Max-Heap arreglo[0:n]."""
    x = arreglo[i]
    while True:
        hijo = 2 * i + 1  # Hijo izquierdo
        if hijo >= n:
            break
        # Si existe el hijo derecho y es mayor que el izquierdo, elegir el derecho
        if hijo + 1 < n and arreglo[hijo + 1] > arreglo[hijo]:
            hijo += 1
        # Si el mayor de los hijos no supera a x, ya está en su lugar
        if arreglo[hijo] <= x:
            break
        arreglo[i] = arreglo[hijo]
        i = hijo
    arreglo[i] = x

def heap_sort(arreglo):
    """
    Ordena un arreglo in-place en tiempo O(n log n) y espacio auxiliar O(1).
    """
    n = len(arreglo)
    # 1. Construir el Max-Heap (bottom-up en tiempo O(n))
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arreglo, i, n)
        
    # 2. Extraer uno por uno el máximo (raíz) hacia el final del arreglo
    for fin in range(n - 1, 0, -1):
        arreglo[0], arreglo[fin] = arreglo[fin], arreglo[0]
        _sift_down(arreglo, 0, fin)
        
    return arreglo

# Prueba rápida
datos = [12, 11, 13, 5, 6, 7]
print(heap_sort(datos))  # Salida: [5, 6, 7, 11, 12, 13]
```

---

### 8. Ordenamiento con Árbol Binario (Tree Sort)

Consiste en insertar uno por uno los elementos del arreglo en un **Árbol Binario de Búsqueda** (*Binary Search Tree* o **BST**), donde para cada nodo todos los valores del subárbol izquierdo son menores y todos los del subárbol derecho son mayores. Una vez construido el árbol, se realiza un recorrido **In-Order** (Izquierda $\to$ Raíz $\to$ Derecha) para recuperar todos los elementos ordenados de menor a mayor.

* **Paradigma:** Inserción en estructura arbórea + recorrido en profundidad.
* **Complejidad Temporal:**
  * **Caso Promedio:** $O(n \log n)$ (o bien $O(n \log k)$ si hay $k$ elementos únicos y se agrupan duplicados por conteo).
  * **Peor Caso:** $O(n^2)$ si se emplea un BST simple y el arreglo de entrada ya está ordenado (el árbol degenera en una lista enlazada de altura $n$). Si se usa un árbol autobalanceado (AVL o Rojo-Negro), el peor caso se mantiene en $O(n \log n)$.
* **Espacio Auxiliar:** $O(n)$ nodos (o $O(k)$ nodos si los duplicados incrementan un contador de frecuencia `cuenta` en cada nodo, como se implementó en la Práctica 2).
* **Estabilidad:** Puede ser estable si los duplicados se insertan sistemáticamente en el subárbol derecho (o si se guardan en una lista dentro del nodo).
* **Uso ideal:** Cuando los datos además de ordenarse necesitarán búsquedas, inserciones dinámicas posteriores o cuando existen millones de elementos repetidos de un conjunto acotado de $k$ claves únicas.

```
Entrada: [5, 3, 7, 2, 4, 8]

        (5)
       /   \
     (3)   (7)     --->  Recorrido In-Order (Izq -> Raíz -> Der):
     / \     \           2 -> 3 -> 4 -> 5 -> 7 -> 8
   (2) (4)   (8)
```

#### Implementación en Python (Iterativa con Conteo de Frecuencias)

```python
class NodoBST:
    __slots__ = ("clave", "izq", "der", "cuenta")
    def __init__(self, clave):
        self.clave = clave
        self.izq = None
        self.der = None
        self.cuenta = 1

def tree_sort(arreglo):
    """
    Ordena un arreglo insertando sus elementos en un BST con contador de
    repeticiones y realizando un recorrido in-order iterativo.
    """
    if len(arreglo) < 2:
        return arreglo
        
    raiz = NodoBST(arreglo[0])
    
    # 1. Insertar cada elemento iterativamente en el BST
    for x in arreglo[1:]:
        actual = raiz
        while True:
            if x < actual.clave:
                if actual.izq is None:
                    actual.izq = NodoBST(x)
                    break
                actual = actual.izq
            elif x > actual.clave:
                if actual.der is None:
                    actual.der = NodoBST(x)
                    break
                actual = actual.der
            else:
                # Elemento repetido: incrementar contador sin crear nodo extra
                actual.cuenta += 1
                break
                
    # 2. Recorrido In-Order iterativo usando pila explícita
    pila = []
    actual = raiz
    k = 0
    while pila or actual is not None:
        while actual is not None:
            pila.append(actual)
            actual = actual.izq
        actual = pila.pop()
        for _ in range(actual.cuenta):
            arreglo[k] = actual.clave
            k += 1
        actual = actual.der
        
    return arreglo

# Prueba rápida
datos = [5, 3, 7, 2, 4, 3, 8, 5]
print(tree_sort(datos))  # Salida: [2, 3, 3, 4, 5, 5, 7, 8]
```

---

## Parte III: Algoritmos No Basados en Comparaciones — $O(n)$

### ¿Por qué los algoritmos de comparación no pueden bajar de $\Omega(n \log n)$?
Cualquier algoritmo que ordene únicamente comparando pares ($a_i \le a_j$) puede representarse como un **árbol de decisión binario** donde cada hoja es una de las $n!$ permutaciones posibles de la entrada. Para alcanzar las $n!$ hojas, la altura mínima $h$ del árbol debe cumplir $2^h \ge n!$, y por la aproximación de Stirling:

$$h \ge \log_2(n!) = \Omega(n \log n)$$

Sin embargo, si dejamos de comparar elementos entre sí y **explotamos la representación numérica de las claves**, podemos ordenar en **tiempo lineal**.

---

### 9. Ordenamiento por Cuentas (Counting Sort)

Es un algoritmo ultrarrápido diseñado para ordenar elementos cuyas claves son **números enteros dentro de un rango acotado** de tamaño $k = \text{máx} - \text{mín} + 1$ (o números reales con precisión decimal fija que puedan escalarse a enteros, como se demostró en la Práctica 2 multiplicando por $100$).

Funciona en tres pasos lineales sin hacer ni una sola comparación entre elementos:
1. **Conteo de frecuencias:** Cuenta cuántas veces aparece cada valor en un arreglo auxiliar `cuenta` de tamaño $k$.
2. **Sumas prefijas (acumuladas):** Acumula las frecuencias en `cuenta` para determinar exactamente en qué índice del arreglo final debe empezar a colocarse cada clave.
3. **Construcción estable de la salida:** Recorre el arreglo original y coloca cada elemento directamente en su posición final dentro del arreglo `salida`.

* **Paradigma:** Distribución y direccionamiento directo por conteo de frecuencias.
* **Complejidad Temporal:** $O(n + k)$, donde $n$ es el número de elementos y $k$ es el rango de valores $(\text{máx} - \text{mín} + 1)$. Si $k = O(n)$, el tiempo es estrictamente lineal **$O(n)$**.
* **Espacio Auxiliar:** $O(n + k)$ (arreglo de conteo de tamaño $k$ + arreglo de salida de tamaño $n$).
* **Estabilidad:** Sí (fundamental para que pueda usarse como subrutina dentro de **Radix Sort**).
* **Uso ideal:** Grandes volúmenes de datos con un rango de claves moderado (calificaciones, edades, códigos postales o números decimales de precisión fija). En la Práctica 2 fue el algoritmo más veloz de todos, ordenando $100,000,000$ de números en solo $12.2\text{ s}$ en Java y $43.2\text{ s}$ en Python.

#### Implementación en Python

```python
def counting_sort(arreglo):
    """
    Ordena un arreglo de enteros de manera estable en tiempo O(n + k).
    """
    n = len(arreglo)
    if n < 2:
        return arreglo
        
    k_min = min(arreglo)
    k_max = max(arreglo)
    k = k_max - k_min + 1
    
    # 1. Contar apariciones de cada clave desplazada por k_min
    cuenta = [0] * k
    for x in arreglo:
        cuenta[x - k_min] += 1
        
    # 2. Calcular sumas prefijas para obtener el índice inicial de cada clave
    acumulado = 0
    for i in range(k):
        frecuencia = cuenta[i]
        cuenta[i] = acumulado
        acumulado += frecuencia
        
    # 3. Colocar cada elemento en su posición final (recorrido hacia adelante = estable)
    salida = [0] * n
    for x in arreglo:
        clave = x - k_min
        salida[cuenta[clave]] = x
        cuenta[clave] += 1
        
    arreglo[:] = salida
    return arreglo

# Prueba rápida
datos = [4, 2, 2, 8, 3, 3, 1]
print(counting_sort(datos))  # Salida: [1, 2, 2, 3, 3, 4, 8]
```

> 💡 **Adaptación a números reales con decimales fijos:** Si los datos tienen a lo más $d$ decimales (por ejemplo, precios o mediciones con 2 decimales como `14.25`), basta con transformar cada número en la clave entera `round(x * 10**d) - k_min` al indexar el arreglo `cuenta`.

---

### 10. Ordenamiento por Residuos / Dígitos (Radix Sort)

¿Qué ocurre si queremos ordenar números enteros muy grandes (por ejemplo, de $0$ a $10^9$) donde el rango $k$ de Counting Sort consumiría gigabytes de memoria? **Radix Sort** resuelve este problema ordenando los números **dígito por dígito**, comenzando desde el dígito menos significativo (unidades) hasta el más significativo (**LSD Radix Sort**), utilizando **Counting Sort** con base $b$ (usualmente $b = 10$ o $b = 256$) como subrutina estable en cada posición.

* **Paradigma:** Distribución posicional por dígitos.
* **Complejidad Temporal:** $O(d \cdot (n + b))$, donde $d$ es la cantidad de dígitos del número máximo y $b$ es la base numérica.
* **Espacio Auxiliar:** $O(n + b)$.
* **Estabilidad:** Sí (y depende obligatoriamente de que el algoritmo interno por dígito sea **estable**).
* **Uso ideal:** Enteros de 32 o 64 bits, matrículas, números telefónicos o cadenas de longitud fija.

```
Ordenando [170, 45, 75, 90, 802, 24, 2, 66] dígito a dígito:
1) Por unidades (10^0): [170, 90, 802, 2, 24, 45, 75, 66]
2) Por decenas  (10^1): [802, 2, 24, 45, 66, 170, 75, 90]
3) Por centenas (10^2): [2, 24, 45, 66, 75, 90, 170, 802]  <-- ¡Ordenado!
```

#### Implementación en Python

```python
def _counting_sort_por_digito(arreglo, exp):
    """Subrutina estable que ordena según el dígito en la posición 'exp'."""
    n = len(arreglo)
    salida = [0] * n
    cuenta = [0] * 10  # Base decimal (dígitos 0 a 9)
    
    for x in arreglo:
        digito = (x // exp) % 10
        cuenta[digito] += 1
        
    # Sumas prefijas acumuladas
    for i in range(1, 10):
        cuenta[i] += cuenta[i - 1]
        
    # Construir la salida recorriendo en reversa para mantener estabilidad
    for i in range(n - 1, -1, -1):
        digito = (arreglo[i] // exp) % 10
        salida[cuenta[digito] - 1] = arreglo[i]
        cuenta[digito] -= 1
        
    arreglo[:] = salida

def radix_sort(arreglo):
    """
    Ordena enteros no negativos en tiempo O(d * (n + b)) usando LSD Radix Sort.
    """
    if len(arreglo) < 2:
        return arreglo
        
    maximo = max(arreglo)
    exp = 1  # 10^0 (unidades), 10^1 (decenas), 10^2 (centenas)...
    while maximo // exp > 0:
        _counting_sort_por_digito(arreglo, exp)
        exp *= 10
        
    return arreglo

# Prueba rápida
datos = [170, 45, 75, 90, 802, 24, 2, 66]
print(radix_sort(datos))  # Salida: [2, 24, 45, 66, 75, 90, 170, 802]
```

---

### 11. Ordenamiento por Cubetas (Bucket Sort)

Divide el intervalo de valores posibles en $n$ subintervalos de igual tamaño llamados **cubetas** (*buckets*). Distribuye cada elemento en su cubeta correspondiente mediante una fórmula matemática proporcional, ordena individualmente cada cubeta (usualmente con **Insertion Sort**, ya que cada cubeta tendrá muy pocos elementos) y finalmente concatena todas las cubetas en orden.

* **Paradigma:** Distribución probabilística + Divide y Vencerás.
* **Complejidad Temporal:** $O(n)$ en el mejor caso y caso promedio (cuando los datos están **uniformemente distribuidos**). $O(n^2)$ en el peor caso (si todos los elementos caen en la misma cubeta y se usa Insertion Sort).
* **Espacio Auxiliar:** $O(n)$ para almacenar las cubetas.
* **Estabilidad:** Sí (si el ordenamiento interno de cada cubeta es estable).
* **Uso ideal:** Números en punto flotante distribuidos de forma uniforme (por ejemplo, números generados aleatoriamente en el rango $[0.0, 1.0)$).

#### Implementación en Python

```python
def bucket_sort(arreglo):
    """
    Ordena un arreglo de números flotantes distribuidos uniformemente.
    """
    n = len(arreglo)
    if n < 2:
        return arreglo
        
    val_min, val_max = min(arreglo), max(arreglo)
    if val_min == val_max:
        return arreglo
        
    # 1. Crear n cubetas vacías
    cubetas = [[] for _ in range(n)]
    rango = val_max - val_min
    
    # 2. Distribuir cada elemento en su cubeta correspondiente
    for x in arreglo:
        indice = int((x - val_min) / rango * (n - 1))
        cubetas[indice].append(x)
        
    # 3. Ordenar cada cubeta con Insertion Sort y concatenar resultados
    k = 0
    for cubeta in cubetas:
        insertion_sort(cubeta)  # Reutilizamos Insertion Sort para listas pequeñas
        for x in cubeta:
            arreglo[k] = x
            k += 1
            
    return arreglo

# Prueba rápida
datos = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
print(bucket_sort(datos))  # Salida: [0.12, 0.17, 0.21, 0.23, 0.26, 0.39, 0.68, 0.72, 0.78, 0.94]
```

---

## Parte IV: Los Algoritmos Más Usados en el Mundo Real (Híbridos y Producción)

En la industria y en las bibliotecas estándar de los lenguajes de programación modernos **casi nunca se utiliza un algoritmo clásico "puro"**. En su lugar, se emplean **algoritmos híbridos** que combinan lo mejor de varios métodos para adaptarse a los datos reales, evitar peores casos patológicos y aprovechar la caché del procesador.

---

### 12. Timsort (El motor de Python, Java, JavaScript V8 y Android)

Diseñado por **Tim Peters** en 2002 para Python (`list.sort()` y `sorted()`), demostró ser tan superior en datos del mundo real que hoy es el algoritmo estándar en **Python, Java (`Arrays.sort` para objetos), el motor V8 de Chrome/Node.js (`Array.prototype.sort`), Swift y Android**.

**¿Por qué es tan rápido en la realidad?**
Los datos del mundo real rara vez son números 100% aleatorios; casi siempre contienen **subsecuencias que ya están ordenadas** de forma ascendente o descendente (llamadas **rachas** o *runs*). Timsort combina **Insertion Sort** + **Merge Sort**:
1. Divide el arreglo en bloques pequeños llamados `minrun` (de tamaño entre $32$ y $64$).
2. Ordena cada bloque pequeño usando **Insertion Sort** (que es imbatible en arreglos pequeños y en rachas casi ordenadas).
3. Fusiona los bloques ordenados usando la lógica de **Merge Sort** (con optimizaciones como el *modo galope* cuando un bloque gana repetidamente).

* **Complejidad Temporal:** $O(n)$ en el mejor caso (datos ya ordenados o en orden inverso), $O(n \log n)$ en caso promedio y peor caso.
* **Espacio Auxiliar:** $O(n)$.
* **Estabilidad:** Sí.

#### Implementación Didáctica de Timsort en Python

```python
def _insertion_sort_rango(arreglo, izq, der):
    """Ordena el subarreglo arreglo[izq..der] in-place con Insertion Sort."""
    for i in range(izq + 1, der + 1):
        clave = arreglo[i]
        j = i - 1
        while j >= izq and arreglo[j] > clave:
            arreglo[j + 1] = arreglo[j]
            j -= 1
        arreglo[j + 1] = clave

def _merge_rango(arreglo, izq, medio, der):
    """Fusiona dos subarreglos ordenados arreglo[izq..medio] y arreglo[medio+1..der]."""
    mitad_izq = arreglo[izq : medio + 1]
    mitad_der = arreglo[medio + 1 : der + 1]
    i = j = 0
    k = izq
    while i < len(mitad_izq) and j < len(mitad_der):
        if mitad_izq[i] <= mitad_der[j]:
            arreglo[k] = mitad_izq[i]
            i += 1
        else:
            arreglo[k] = mitad_der[j]
            j += 1
        k += 1
    while i < len(mitad_izq):
        arreglo[k] = mitad_izq[i]
        i += 1
        k += 1
    while j < len(mitad_der):
        arreglo[k] = mitad_der[j]
        j += 1
        k += 1

def timsort(arreglo):
    """
    Implementación de Timsort: combina Insertion Sort en bloques (MIN_RUN = 32)
    con fusiones sucesivas de Merge Sort.
    """
    n = len(arreglo)
    MIN_RUN = 32
    
    # 1. Ordenar cada subarreglo de tamaño MIN_RUN con Insertion Sort
    for inicio in range(0, n, MIN_RUN):
        fin = min(inicio + MIN_RUN - 1, n - 1)
        _insertion_sort_rango(arreglo, inicio, fin)
        
    # 2. Fusionar las rachas doblando el tamaño en cada pasada (32, 64, 128...)
    tamano = MIN_RUN
    while tamano < n:
        for izq in range(0, n, 2 * tamano):
            medio = min(n - 1, izq + tamano - 1)
            der = min((izq + 2 * tamano - 1), (n - 1))
            if medio < der:
                _merge_rango(arreglo, izq, medio, der)
        tamano *= 2
        
    return arreglo

# Prueba rápida
datos = [5, 21, 7, 23, 19, 10, 1, 4, 8, 12, 2, 99, 15]
print(timsort(datos))  # Salida: [1, 2, 4, 5, 7, 8, 10, 12, 15, 19, 21, 23, 99]
```

> 📝 **Nota:** En Python, a partir de la versión 3.11, Timsort evolucionó a **Powersort**, una variante que mejora aún más el orden en que se fusionan las rachas usando casi la misma estructura base.

---

### 13. Introsort y pdqsort (El motor de C++, .NET, Rust y Go)

En lenguajes de sistemas como **C++ (`std::sort`)** o **C# / .NET (`Array.Sort`)**, no se puede usar Timsort como algoritmo por defecto porque requiere $O(n)$ de memoria extra. Tampoco se puede usar Quick Sort puro porque un atacante podría enviar datos diseñados para provocar su peor caso $O(n^2)$ y congelar el servidor (*ataque de denegación de servicio*).

La solución fue creada por David Musser en 1997: **Introsort (*Introspective Sort*)**, un híbrido de **3 algoritmos**:
1. Comienza ejecutando **Quick Sort** por su altísima velocidad y localidad de caché.
2. Si el tamaño de una partición baja de $16$ elementos, cambia a **Insertion Sort**.
3. Vigila la profundidad de la recursión: si supera el límite de $2 \lfloor \log_2 n \rfloor$ (señal de que Quick Sort está degenerando hacia $O(n^2)$), **cambia automáticamente a Heap Sort** en esa rama para garantizar $O(n \log n)$ en el peor de los casos.

* **Complejidad Temporal:** $O(n \log n)$ garantizado en el peor caso y caso promedio.
* **Espacio Auxiliar:** $O(\log n)$ (*in-place*).
* **Estabilidad:** No.
* **Evolución moderna (`pdqsort`):** **Rust (`sort_unstable`)** y **Go (`slices.Sort`)** utilizan **Pattern-Defeating Quicksort (`pdqsort`)**, una mejora moderna de Introsort que además detecta patrones repetidos y rachas ordenadas para lograr $O(n)$ en entradas estructuradas.

#### Implementación de Introsort en Python

```python
import math

def introsort(arreglo):
    """
    Ordena un arreglo in-place combinando Quick Sort, Heap Sort e Insertion Sort.
    Garantiza O(n log n) en el peor caso sin usar memoria extra O(n).
    """
    n = len(arreglo)
    if n < 2:
        return arreglo
    profundidad_max = 2 * int(math.log2(n))

    def _heapsort_rango(lo, hi):
        # Ordena arreglo[lo..hi] usando un sub-arreglo con heap_sort
        sub = arreglo[lo : hi + 1]
        heap_sort(sub)
        arreglo[lo : hi + 1] = sub

    def _introsort(lo, hi, limite_prof):
        tamano = hi - lo + 1
        # 1. Para arreglos pequeños, usar Insertion Sort
        if tamano <= 16:
            _insertion_sort_rango(arreglo, lo, hi)
            return
            
        # 2. Si se agotó el límite de recursión, rescate con Heap Sort O(n log n)
        if limite_prof == 0:
            _heapsort_rango(lo, hi)
            return
            
        # 3. Caso normal: particionar con Quick Sort (pivote central)
        pivote = arreglo[(lo + hi) // 2]
        i, j = lo, hi
        while i <= j:
            while arreglo[i] < pivote:
                i += 1
            while arreglo[j] > pivote:
                j -= 1
            if i <= j:
                arreglo[i], arreglo[j] = arreglo[j], arreglo[i]
                i += 1
                j -= 1
        if lo < j:
            _introsort(lo, j, limite_prof - 1)
        if i < hi:
            _introsort(i, hi, limite_prof - 1)

    _introsort(0, n - 1, profundidad_max)
    return arreglo

# Prueba rápida
datos = [10, 7, 8, 9, 1, 5, 3, 2, 6, 4]
print(introsort(datos))  # Salida: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

---

### 14. Quick Sort de 3 Vías y Dual-Pivot Quick Sort (Datos con Duplicados y Java)

En bases de datos reales es sumamente común ordenar tablas por columnas con **muchos valores repetidos** (por ejemplo, ordenar millones de clientes por `"país"`, `"edad"` o `"estado civil"`). El Quick Sort tradicional de 2 vías se vuelve lento cuando hay muchos elementos iguales al pivote.

Para resolverlo en la vida real se emplean dos variantes:
1. **Quick Sort de 3 Vías (*Dutch National Flag* de Dijkstra):** Particiona el arreglo en **tres zonas** en una sola pasada:
   * Elementos **estrictamente menores** que el pivote ($< P$).
   * Elementos **iguales** al pivote ($== P$), ¡que quedan todos juntos en su posición final y no vuelven a tocarse!
   * Elementos **estrictamente mayores** que el pivote ($> P$).
   Si hay $k$ valores únicos y muchos duplicados, reduce la complejidad hasta **$O(n)$**.
2. **Dual-Pivot Quick Sort (Vladimir Yaroslavskiy, 2009):** Es el algoritmo que usa **Java (`Arrays.sort`) para todos los arreglos de tipos primitivos** (`int[]`, `double[]`, `float[]`). Utiliza **dos pivotes** ($P_1 \le P_2$) para dividir el arreglo en tres partes ($< P_1$, entre $P_1$ y $P_2$, y $> P_2$), reduciendo el tráfico entre la caché del CPU y la memoria RAM.

#### Implementación de Quick Sort de 3 Vías en Python

```python
def quick_sort_3_vias(arreglo):
    """
    Quick Sort con partición de 3 vías (Bandera Nacional Holandesa de Dijkstra).
    Ideal para arreglos con gran cantidad de elementos duplicados.
    """
    def _sort(lo, hi):
        if lo >= hi:
            return
        lt = lo      # arreglo[lo .. lt-1] < pivote
        gt = hi      # arreglo[gt+1 .. hi] > pivote
        i = lo + 1   # arreglo[lt .. i-1] == pivote
        pivote = arreglo[lo]
        
        while i <= gt:
            if arreglo[i] < pivote:
                arreglo[lt], arreglo[i] = arreglo[i], arreglo[lt]
                lt += 1
                i += 1
            elif arreglo[i] > pivote:
                arreglo[i], arreglo[gt] = arreglo[gt], arreglo[i]
                gt -= 1
            else:
                i += 1
                
        # Ahora arreglo[lt..gt] son todos iguales al pivote y ya están listos
        _sort(lo, lt - 1)
        _sort(gt + 1, hi)

    _sort(0, len(arreglo) - 1)
    return arreglo

# Prueba rápida con muchos elementos repetidos
datos = [4, 2, 4, 1, 4, 2, 1, 4, 3, 2, 4]
print(quick_sort_3_vias(datos))  # Salida: [1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 4]
```

---

### 15. Ordenamiento Externo (*External K-Way Merge Sort* — Bases de Datos y Big Data)

Como comprobamos en la [Práctica 2](../practicas/practica%202.%20ordenamiento/REPORTE.md), al intentar ordenar $n = 1,000,000,000$ ($10^9$) números de punto flotante (`7.6 GB` de datos puros) en una computadora con `8 GB` de RAM, los algoritmos en memoria principal se vuelven inviables por falta de RAM (`omitido_ram`).

¿Cómo ordenan entonces **PostgreSQL, MySQL, Apache Spark o MapReduce** tablas de $500\text{ GB}$ si el servidor solo tiene $8\text{ GB}$ de RAM? Usan **External $K$-Way Merge Sort**:
1. **Fase de División (Creación de *Runs*):** Lee del disco bloques que sí quepan en la memoria RAM (por ejemplo, bloques de $500\text{ MB}$), los ordena en RAM con Quick Sort o Timsort, y escribe cada bloque ordenado en un archivo temporal en disco.
2. **Fase de Fusión de $K$ Vías (*K-Way Merge* con Min-Heap):** Abre todos los $K$ archivos temporales al mismo tiempo, lee únicamente el primer elemento de cada archivo y los mete en un **Montículo Mínimo (*Min-Heap*)** de tamaño $K$. En cada paso extrae el mínimo del Heap en $O(\log K)$, lo escribe al archivo final ordenado y lee el siguiente número del archivo de donde provino ese mínimo.

* **Complejidad Temporal:** $O(n \log n)$ con lecturas/escrituras secuenciales óptimas en disco.
* **Espacio en RAM:** $O(K)$ (puede ordenar terabytes de datos usando apenas unos pocos megabytes de RAM).

#### Implementación de Fusión de $K$ Vías con Min-Heap en Python

```python
import heapq

def k_way_merge(bloques_ordenados):
    """
    Fusiona K listas o flujos ya ordenados en tiempo O(n log K) y memoria O(K)
    utilizando un Min-Heap. Es el corazón del Ordenamiento Externo en Bases de Datos.
    *(Nota: en Python estándar también existe 'heapq.merge(*bloques_ordenados)').*
    """
    min_heap = []
    
    # 1. Insertar el primer elemento de cada uno de los K bloques en el Min-Heap
    # Tupla: (valor, indice_de_bloque, indice_dentro_del_bloque)
    for id_bloque, bloque in enumerate(bloques_ordenados):
        if bloque:
            heapq.heappush(min_heap, (bloque[0], id_bloque, 0))
            
    resultado = []
    # 2. Extraer siempre el menor global y avanzar en ese bloque
    while min_heap:
        valor, id_bloque, idx_elem = heapq.heappop(min_heap)
        resultado.append(valor)
        
        siguiente_idx = idx_elem + 1
        if siguiente_idx < len(bloques_ordenados[id_bloque]):
            siguiente_val = bloques_ordenados[id_bloque][siguiente_idx]
            heapq.heappush(min_heap, (siguiente_val, id_bloque, siguiente_idx))
            
    return resultado

# Prueba rápida: 4 bloques ordenados independientemente en disco
bloques = [
    [1, 10, 20],
    [2, 5, 30],
    [0, 15, 25],
    [3, 8, 12]
]
print(k_way_merge(bloques))  # Salida: [0, 1, 2, 3, 5, 8, 10, 12, 15, 20, 25, 30]
```

---

## ¿Qué Algoritmo Usa Cada Lenguaje en la Vida Real?

| Lenguaje / Sistema | Función Nativa | Algoritmo Real que Ejecuta por Debajo | ¿Estable? |
| :--- | :--- | :--- | :---: |
| **Python** | `list.sort()` / `sorted()` | **Timsort / Powersort** (Merge Sort + Insertion Sort) | Sí |
| **Java (Primitivos)** | `Arrays.sort(int[])` | **Dual-Pivot Quick Sort** + Insertion Sort | No |
| **Java (Objetos)** | `Arrays.sort(Object[])` | **Timsort** | Sí |
| **C++** | `std::sort` | **Introsort** (Quick Sort + Heap Sort + Insertion Sort) | No |
| **C++ (Estable)** | `std::stable_sort` | **Merge Sort** adaptativo | Sí |
| **JavaScript (V8)** | `Array.prototype.sort()` | **Timsort** | Sí |
| **Rust / Go** | `sort_unstable` / `slices.Sort` | **pdqsort** (*Pattern-Defeating Quicksort*) | No |
| **PostgreSQL / Spark** | `ORDER BY` (datos gigantes) | **External K-Way Merge Sort** (con Min-Heap) | Sí |

---

## Resumen y Comparativa General de Complejidad

A continuación se presenta la tabla maestra comparativa de todos los algoritmos de ordenamiento estudiados:

| Algoritmo | Mejor Caso | Caso Promedio | Peor Caso | Espacio Auxiliar | ¿Estable? | ¿Comparativo? | Paradigma / Base |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Bubble Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Sí | Sí | Intercambios adyacentes |
| **Selection Sort** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | No | Sí | Selección del mínimo |
| **Insertion Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Sí | Sí | Inserción incremental |
| **Shell Sort** | $O(n \log n)$ | $O(n^{1.5})$* | $O(n^{1.5})$* | $O(1)$ | No | Sí | Inserción por brechas (*gaps*) |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Sí | Sí | Divide y Vencerás |
| **Quick Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | No | Sí | Divide y Vencerás (Pivote) |
| **Quick Sort 3 Vías** | $O(n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | No | Sí | Partición tripartita (duplicados) |
| **Heap Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ | No | Sí | Selección con *Max-Heap* |
| **Tree Sort (BST)** | $O(n \log k)$ | $O(n \log k)$ | $O(n^2)$** | $O(k)$ | Depende | Sí | Árbol Binario de Búsqueda |
| **Counting Sort** | $O(n + k)$ | $O(n + k)$ | $O(n + k)$ | $O(n + k)$ | Sí | No | Conteo de frecuencias |
| **Radix Sort** | $O(d(n + b))$ | $O(d(n + b))$ | $O(d(n + b))$ | $O(n + b)$ | Sí | No | Distribución por dígitos |
| **Bucket Sort** | $O(n)$ | $O(n)$ | $O(n^2)$ | $O(n)$ | Sí | No | Distribución en cubetas |
| **Timsort** | $O(n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Sí | Sí | Híbrido (Merge + Insertion) |
| **Introsort / pdqsort**| $O(n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(\log n)$ | No | Sí | Híbrido (Quick + Heap + Insertion)|

*\* En Shell Sort la complejidad exacta depende de la secuencia de brechas elegida.*  
*\*\* En Tree Sort el peor caso baja a $O(n \log n)$ si se emplea un árbol autobalanceado (AVL / Rojo-Negro).*

---

## Conclusiones Prácticas y Guía de Selección (Resultados de la Práctica 2)

A partir de la experimentación con hasta $10^8$ elementos reales en la [Práctica 2: Algoritmos de Ordenamiento](../practicas/practica%202.%20ordenamiento/REPORTE.md), podemos resumir las siguientes reglas de decisión para elegir el algoritmo ideal:

1. **¿Tus datos son enteros o reales con precisión fija en un rango acotado $k$?**
   $\to$ Usa **Counting Sort** (o **Radix Sort** si el rango es grande). Romper la barrera $\Omega(n \log n)$ le permitió ordenar $100$ millones de datos en $12.24\text{ s}$ en Java, superando a todos los demás.
2. **¿Necesitas ordenamiento general en producción con estabilidad o datos parcialmente ordenados?**
   $\to$ Usa **Timsort** (nativo en Python `sorted()`) o **Merge Sort**. Gracias a su acceso secuencial a memoria (alta localidad espacial de caché), Merge Sort superó por más de $3\times$ a Heap Sort a pesar de tener la misma complejidad teórica.
3. **¿Buscas máxima velocidad in-place sin riesgo de caer en $O(n^2)$?**
   $\to$ Usa **Introsort / pdqsort** (o **Quick Sort de 3 vías** si hay muchas claves repetidas).
4. **¿La memoria RAM es crítica y no puedes permitirte un buffer auxiliar $O(n)$?**
   $\to$ Usa **Heap Sort**. Garantiza $O(n \log n)$ en el peor caso utilizando exactamente $O(1)$ de memoria extra ($0\text{ MB}$ adicionales).
5. **¿Los datos son tan masivos ($n = 10^9$ o terabytes) que no caben en la memoria RAM?**
   $\to$ Usa **Ordenamiento Externo (*External K-Way Merge Sort*)** apoyado en un Min-Heap.
6. **¿Cuándo evitar $O(n^2)$ como Bubble Sort?**
   $\to$ Siempre que $n$ sea grande: al multiplicar $n$ por $10$, el tiempo de un algoritmo $O(n^2)$ se multiplica por $100$ (pasar de $n = 10^5$ a $n = 10^8$ en Bubble Sort incrementa el tiempo de segundos a meses o décadas).

