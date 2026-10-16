# Apuntes: Algoritmos de Búsqueda

La búsqueda es una de las operaciones más fundamentales y frecuentes en las ciencias de la computación. Consiste en encontrar la posición (o la existencia) de un elemento específico, llamado **objetivo** (o *target*), dentro de una colección de datos (como un arreglo, una lista o un árbol). 

La elección del algoritmo de búsqueda adecuado depende enteramente de la estructura de nuestros datos y de si estos se encuentran ordenados o no.

---

## 1. Búsqueda Lineal (Secuencial)

Es el algoritmo de búsqueda más básico e intuitivo. Consiste en recorrer la estructura de datos elemento por elemento desde el principio hasta el final, comparando cada uno con el elemento que estamos buscando.

* **Requisito:** Ninguno. Funciona tanto en colecciones desordenadas como ordenadas.
* **Complejidad Temporal:** $O(n)$ en el peor de los casos (cuando el elemento no existe o está al final). $O(1)$ en el mejor de los casos (si el elemento está en la primera posición).
* **Uso ideal:** Listas pequeñas o datos desordenados donde ordenar primero costaría más que la búsqueda en sí.

### Implementación en Python

```python
def busqueda_lineal(arreglo, objetivo):
    """
    Realiza una búsqueda lineal en un arreglo.
    Devuelve el índice del objetivo si se encuentra, de lo contrario -1.
    """
    for i in range(len(arreglo)):
        if arreglo[i] == objetivo:
            return i  # Elemento encontrado
    return -1  # Elemento no encontrado

# Prueba rápida
datos = [4, 2, 8, 5, 1, 9]
print(busqueda_lineal(datos, 5))  # Salida: 3
```

---

## 2. Búsqueda Binaria (Binary Search)

La búsqueda binaria es un algoritmo altamente eficiente que utiliza el paradigma de **"Divide y Vencerás"**. En lugar de buscar uno por uno, compara el elemento central del arreglo con el objetivo; si no coinciden, descarta la mitad del arreglo donde sabe que el elemento no puede estar y repite el proceso en la mitad restante.

* **Requisito fundamental:** La colección de datos **DEBE estar ordenada** previamente.
* **Complejidad Temporal:** $O(\log n)$. En cada paso el espacio de búsqueda se reduce a la mitad.
* **Uso ideal:** Grandes volúmenes de datos donde las consultas son frecuentes y la colección se mantiene ordenada.

### Implementación Iterativa en Python

```python
def busqueda_binaria(arreglo, objetivo):
    """
    Realiza una búsqueda binaria en un arreglo ORDENADO.
    Devuelve el índice del objetivo si se encuentra, de lo contrario -1.
    """
    izquierda = 0
    derecha = len(arreglo) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        
        if arreglo[medio] == objetivo:
            return medio
        elif arreglo[medio] < objetivo:
            izquierda = medio + 1  # Descartamos la mitad izquierda
        else:
            derecha = medio - 1    # Descartamos la mitad derecha
            
    return -1

# Prueba rápida
datos_ordenados = [1, 3, 5, 7, 9, 11, 15, 18]
print(busqueda_binaria(datos_ordenados, 7))  # Salida: 3
```

> 💡 **Analogía:** Si buscas una palabra en un diccionario, no lees página por página (búsqueda lineal). Abres el diccionario por la mitad; si la palabra que buscas está alfabéticamente antes, ignoras la segunda mitad y repites el proceso. ¡Eso es búsqueda binaria!

### 2.1 Uso en el Mundo Real: Búsqueda de Rangos y `bisect` (`lower_bound`)

En la industria, rara vez se programa la búsqueda binaria desde cero o solo para saber si un valor existe. Lo más común es buscar **puntos de inserción**, **el primer elemento mayor o igual a $X$** (*lower bound*) o **todos los elementos dentro de un rango** (por ejemplo, filtrar transacciones entre dos fechas). En Python, esto se hace con el módulo nativo `bisect` (implementado en C):

```python
import bisect

precios = [100, 200, 200, 200, 350, 500, 800]

# Primer índice donde aparece >= 200 (lower_bound)
izq = bisect.bisect_left(precios, 200)   # Salida: 1

# Índice justo después del último 200 (upper_bound)
der = bisect.bisect_right(precios, 200)  # Salida: 4

print(f"El 200 aparece {der - izq} veces (índices {izq} a {der - 1})")
```

---

## 3. Búsqueda de Salto (Jump Search)

Es un punto intermedio entre la búsqueda lineal y la binaria. Al igual que la búsqueda binaria, requiere que el arreglo esté **ordenado**. Funciona saltando bloques de un tamaño fijo $m$ hasta encontrar un bloque donde el elemento objetivo podría estar. Luego, realiza una búsqueda lineal solo en ese bloque.

* **Requisito:** Datos ordenados.
* **Complejidad Temporal:** $O(\sqrt{n})$, asumiendo que el tamaño de salto óptimo es $m = \sqrt{n}$.
* **Uso ideal:** Sistemas donde retroceder en la memoria es costoso (por ejemplo, en ciertos tipos de hardware), ya que la búsqueda binaria salta de ida y vuelta de manera impredecible, mientras que Jump Search avanza sistemáticamente.

### Implementación en Python

```python
import math

def busqueda_salto(arreglo, objetivo):
    n = len(arreglo)
    salto = int(math.sqrt(n))
    previo = 0
    
    # Encontrar el bloque donde el elemento podría estar
    while arreglo[min(salto, n) - 1] < objetivo:
        previo = salto
        salto += int(math.sqrt(n))
        if previo >= n:
            return -1
            
    # Búsqueda lineal en el bloque identificado
    while arreglo[previo] < objetivo:
        previo += 1
        if previo == min(salto, n):
            return -1
            
    # Verificar si lo encontramos
    if arreglo[previo] == objetivo:
        return previo
        
    return -1

datos_ordenados = [1, 3, 5, 7, 9, 11, 15, 18, 21, 24]
print(busqueda_salto(datos_ordenados, 15))  # Salida: 6
```

---

## 4. Búsqueda Exponencial (Exponential Search)

Este algoritmo se utiliza en arreglos ordenados y es especialmente útil para buscar en listas de tamaño infinito o no delimitado. Consiste en encontrar un rango donde el elemento puede estar (doblando el índice en cada iteración: 1, 2, 4, 8...) y luego realizar una búsqueda binaria en ese sub-rango.

* **Requisito:** Datos ordenados.
* **Complejidad Temporal:** $O(\log i)$, donde $i$ es la posición del elemento buscado (en el peor caso $O(\log n)$).
* **Uso ideal:** Casos en los que el objetivo está cerca del principio del arreglo o en flujos/estructuras cuyo tamaño total se desconoce.

### Implementación en Python

```python
def busqueda_exponencial(arreglo, objetivo):
    n = len(arreglo)
    if n == 0:
        return -1
    # Si el elemento está en la primera posición
    if arreglo[0] == objetivo:
        return 0
        
    # Encontrar el rango para la búsqueda binaria
    i = 1
    while i < n and arreglo[i] <= objetivo:
        i *= 2
        
    # Realizar búsqueda binaria en el rango encontrado [i/2, min(i, n - 1)]
    izquierda = i // 2
    derecha = min(i, n - 1)
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if arreglo[medio] == objetivo:
            return medio
        elif arreglo[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
            
    return -1

datos_ordenados = [1, 3, 5, 7, 9, 11, 15, 18, 21, 24, 30, 35, 40]
print(busqueda_exponencial(datos_ordenados, 15))  # Salida: 6
```

---

## 5. Búsqueda por Interpolación (Interpolation Search)

La búsqueda por interpolación es una mejora de la búsqueda binaria para casos en los que los datos del arreglo ordenado están **distribuidos de manera uniforme**. En lugar de siempre ir al punto medio, calcula una estimación (interpolación) de la posición basada en el valor que estamos buscando.

* **Requisito:** Datos ordenados y uniformemente distribuidos.
* **Complejidad Temporal:** $O(\log(\log n))$ en promedio, $O(n)$ en el peor caso (cuando la distribución es exponencial o muy desigual).
* **Uso ideal:** Arreglos donde se conoce que la separación numérica entre los elementos es relativamente constante (por ejemplo, índices numéricos consecutivos o directorios).

> 💡 **Analogía:** Si vas a buscar el nombre "Zapata" en un directorio, no abres el libro a la mitad, sino que lo abres directamente hacia el final. La búsqueda por interpolación intenta hacer exactamente esta predicción matemática.

### Implementación en Python

```python
def busqueda_interpolacion(arreglo, objetivo):
    bajo = 0
    alto = len(arreglo) - 1
    
    while bajo <= alto and objetivo >= arreglo[bajo] and objetivo <= arreglo[alto]:
        # Si hay un solo elemento o los extremos son iguales
        if bajo == alto or arreglo[alto] == arreglo[bajo]:
            if arreglo[bajo] == objetivo:
                return bajo
            return -1
            
        # Fórmula de interpolación lineal para estimar la posición
        pos = bajo + int(((float(alto - bajo) / (arreglo[alto] - arreglo[bajo])) * (objetivo - arreglo[bajo])))
        
        if arreglo[pos] == objetivo:
            return pos
        if arreglo[pos] < objetivo:
            bajo = pos + 1
        else:
            alto = pos - 1
            
    return -1

datos_distribuidos = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print(busqueda_interpolacion(datos_distribuidos, 70))  # Salida: 6
```

---

## 6. Tablas Hash (Búsqueda por Hashing)

En la vida real, cuando necesitamos buscar por clave exacta en memoria RAM, **las Tablas Hash son el estándar absoluto**. Utilizan una **función hash** para convertir la clave de búsqueda (un texto, un ID, una tupla) en un índice numérico directo dentro de un arreglo en memoria.

* **Complejidad Temporal:** $O(1)$ en promedio. En el peor de los casos (muchas colisiones), puede degradarse a $O(n)$, pero los motores modernos mitigan esto con funciones hash criptográficas o redimensionamiento dinámico.
* **Uso ideal:** Bases de datos en memoria (Redis), cachés, compiladores y estructuras nativas como `dict` y `set` en Python, `HashMap` en Java o `unordered_map` en C++.

> 📝 **Nota:** Si vas a realizar muchas búsquedas sobre una lista desordenada en Python, convertirla primero en un conjunto (`conjunto = set(lista)`) cuesta $O(n)$, pero reduce todas las búsquedas posteriores de $O(n)$ a **$O(1)$ instantáneo**.

---

## Parte II: Los Algoritmos de Búsqueda Más Usados en el Mundo Real

Más allá de buscar un número dentro de un arreglo estático, el software moderno necesita buscar en **bases de datos con millones de registros que cambian cada segundo**, **archivos de texto**, **redes de autocompletado**, **grafos** y **mapas GPS**. A continuación se presentan los algoritmos que realmente mueven la industria.

---

## 7. Árboles B y B+ (El Motor de las Bases de Datos y Sistemas de Archivos)

La Búsqueda Binaria sobre un arreglo tiene un defecto grave en la vida real: **insertar o eliminar un dato cuesta $O(n)$** porque obliga a recorrer y desplazar millones de elementos en memoria. Para solucionar esto manteniendo búsquedas logarítmicas y lecturas rápidas en disco (SSD/NVMe), la industria utiliza **Árboles B+** (*B+ Trees*).

A diferencia de un árbol binario (donde cada nodo tiene a lo más $2$ hijos), un nodo de un **Árbol B+** almacena **cientos de claves ordenadas** (ajustadas exactamente al tamaño de una página de disco de $4\text{ KB}$ o $16\text{ KB}$).
* En un **Árbol B+**, todos los datos reales viven en las **hojas**, y las hojas están conectadas entre sí mediante una lista doblemente enlazada, lo que hace que las consultas por rango (`WHERE edad BETWEEN 20 AND 30`) sean instantáneas.

* **Complejidad Temporal:** $O(\log_B n)$ para búsqueda, inserción y eliminación (donde $B$ es el factor de ramificación, típicamente $B \approx 100\text{–}500$; con solo $3$ o $4$ saltos se busca entre **mil millones** de registros).
* **Dónde se usa realmente:** Índices de **PostgreSQL, MySQL (InnoDB), SQLite, Oracle, SQL Server** y sistemas de archivos como **NTFS (Windows), APFS (macOS) y ext4 (Linux)**. *(En memoria RAM pura se suelen usar **Árboles Rojo-Negro**, como en `std::map` de C++ o `TreeMap` de Java).*

---

## 8. Búsqueda de Subcadenas en Texto: KMP y Boyer-Moore (`Ctrl+F` y `grep`)

Cuando presionas `Ctrl+F` en un editor de código, ejecutas `grep` en la terminal o buscas una secuencia de ADN en un genoma, no buscas un elemento en un arreglo, sino un **patrón** de longitud $m$ dentro de un **texto** de longitud $n$.
La búsqueda ingenua compara carácter por carácter desde cada posición y tarda $O(n \cdot m)$. En la realidad se usan dos algoritmos fundamentales:

1. **Algoritmo KMP (Knuth-Morris-Pratt):** Precalcula una tabla de prefijos-sufijos llamada **LPS** (*Longest Proper Prefix which is also Suffix*) en tiempo $O(m)$. Cuando ocurre una discrepancia, KMP sabe exactamente cuántos caracteres ya coincidieron y **jamás retrocede el puntero del texto principal**, logrando tiempo lineal garantizado $O(n + m)$.
2. **Algoritmo de Boyer-Moore (y su variante Horspool):** Es el estándar en herramientas como **GNU `grep`** y editores de texto. Compara el patrón de **derecha a izquierda**; si el último carácter del patrón ni siquiera existe en la palabra actual del texto, **salta $m$ caracteres de golpe**, logrando una complejidad **sub-lineal $O(n / m)$** en el caso promedio.

* **Complejidad Temporal:** $O(n + m)$ garantizado en KMP; $O(n / m)$ en promedio en Boyer-Moore.
* **Uso ideal:** Editores de texto, motores de expresiones regulares, buscadores de código, bioinformática y sistemas de detección de intrusiones en red.

### Implementación de KMP en Python

```python
def buscar_kmp(texto, patron):
    """
    Busca todas las apariciones de 'patron' dentro de 'texto' en tiempo O(n + m)
    usando el algoritmo Knuth-Morris-Pratt (KMP).
    """
    n, m = len(texto), len(patron)
    if m == 0:
        return [0]
        
    # 1. Construir arreglo LPS (mayor prefijo propio que también es sufijo)
    lps = [0] * m
    longitud = 0
    i = 1
    while i < m:
        if patron[i] == patron[longitud]:
            longitud += 1
            lps[i] = longitud
            i += 1
        elif longitud != 0:
            longitud = lps[longitud - 1]
        else:
            lps[i] = 0
            i += 1
            
    # 2. Recorrer el texto sin retroceder nunca el índice 'i'
    posiciones = []
    i = j = 0  # i para texto, j para patrón
    while i < n:
        if texto[i] == patron[j]:
            i += 1
            j += 1
            if j == m:
                posiciones.append(i - j)  # Coincidencia encontrada
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]  # Saltar inteligentemente usando LPS
            else:
                i += 1
                
    return posiciones

# Prueba rápida
texto = "ABABDABACDABABCABAB"
patron = "ABABCABAB"
print(buscar_kmp(texto, patron))  # Salida: [10]
```

---

## 9. Búsqueda por Prefijos: Trie / Árbol de Prefijos (Autocompletado)

Cuando escribes `"alg"` en la barra de búsqueda de Google o en el teclado de tu teléfono y al instante te sugiere `"algoritmo"`, `"álgebra"`, `"alguien"`, se está utilizando un **Trie** (del inglés *re**trie**val*).

Un Trie es un árbol donde cada nodo representa un carácter y cada camino desde la raíz hasta un nodo marcado representa una palabra. Su propiedad mágica es que el tiempo de búsqueda **no depende de cuántas millones de palabras haya en el diccionario ($n$)**, sino únicamente de la **longitud de la palabra buscada ($L$)**.

* **Complejidad Temporal:** $O(L)$ para buscar una palabra o verificar un prefijo, donde $L$ es el número de letras de la consulta.
* **Uso ideal:** Sistemas de autocompletado en tiempo real, correctores ortográficos, enrutamiento de direcciones IP en routers (*Longest Prefix Matching*) y diccionarios predictivos.

### Implementación en Python

```python
class NodoTrie:
    def __init__(self):
        self.hijos = {}
        self.es_fin_de_palabra = False

class Trie:
    def __init__(self):
        self.raiz = NodoTrie()
        
    def insertar(self, palabra):
        nodo = self.raiz
        for char in palabra:
            if char not in nodo.hijos:
                nodo.hijos[char] = NodoTrie()
            nodo = nodo.hijos[char]
        nodo.es_fin_de_palabra = True
        
    def autocompletar(self, prefijo):
        """Devuelve todas las palabras almacenadas que comienzan con 'prefijo'."""
        nodo = self.raiz
        for char in prefijo:
            if char not in nodo.hijos:
                return []  # El prefijo no existe
            nodo = nodo.hijos[char]
            
        resultados = []
        def _recolectar(nodo_actual, camino):
            if nodo_actual.es_fin_de_palabra:
                resultados.append(camino)
            for char, siguiente in nodo_actual.hijos.items():
                _recolectar(siguiente, camino + char)
                
        _recolectar(nodo, prefijo)
        return resultados

# Prueba rápida
buscador = Trie()
for p in ["algoritmo", "algebra", "alguien", "arbol", "arreglo"]:
    buscador.insertar(p)
print(buscador.autocompletar("alg"))  # Salida: ['algoritmo', 'algebra', 'alguien']
```

---

## 10. Búsqueda en Grafos y Árboles: BFS y DFS

Cuando los datos están conectados en forma de red (redes sociales, páginas web con hipervínculos, redes eléctricas o árboles del DOM en HTML), usamos los dos algoritmos de búsqueda en grafos más importantes de la computación:

1. **Búsqueda en Anchura (BFS - *Breadth-First Search*):**
   * Explora el grafo **por niveles** (primero todos los vecinos a distancia $1$, luego todos los de distancia $2$, etc.) utilizando una **Cola FIFO** (`collections.deque`).
   * **Propiedad clave:** Garantiza encontrar siempre el **camino más corto** (en número de saltos/aristas) en grafos no ponderados.
2. **Búsqueda en Profundidad (DFS - *Depth-First Search*):**
   * Explora avanzando lo más profundo posible por una rama antes de retroceder (*backtracking*), utilizando una **Pila LIFO** o recursión.
   * **Propiedad clave:** Consume mucha menos memoria en árboles muy anchos y es la base para detectar ciclos, resolver laberintos, ordenamiento topológico de dependencias (como `npm` o `pip`) y recolectores de basura (*Mark-and-Sweep*).

* **Complejidad Temporal:** $O(V + E)$ para ambos, donde $V$ es el número de vértices (nodos) y $E$ es el número de aristas (conexiones).

### Implementación de BFS (Camino más corto en red) en Python

```python
from collections import deque

def bfs_camino_mas_corto(grafo, inicio, objetivo):
    """
    Encuentra la ruta con menor número de saltos entre 'inicio' y 'objetivo'
    usando Búsqueda en Anchura (BFS).
    """
    visitados = {inicio}
    cola = deque([(inicio, [inicio])])
    
    while cola:
        nodo, camino = cola.popleft()
        if nodo == objetivo:
            return camino
            
        for vecino in grafo.get(nodo, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append((vecino, camino + [vecino]))
                
    return None  # No existe conexión

# Prueba rápida: Red de conexiones
red = {
    "Ana": ["Beto", "Carla"],
    "Beto": ["Ana", "Daniel"],
    "Carla": ["Ana", "Elena"],
    "Daniel": ["Beto", "Fernando"],
    "Elena": ["Carla", "Fernando"],
    "Fernando": ["Daniel", "Elena"]
}
print(bfs_camino_mas_corto(red, "Ana", "Fernando"))  # Salida: ['Ana', 'Beto', 'Daniel', 'Fernando']
```

---

## 11. Búsqueda de Rutas Óptimas con Pesos: Dijkstra y A* (GPS y Videojuegos)

Si las conexiones entre nodos tienen **costos o distancias distintas** (kilómetros en una carretera, tráfico en tiempo real o latencia en milisegundos de fibra óptica), BFS ya no sirve porque menos saltos no significa menor distancia. Aquí reinan **Dijkstra** y **A\*** (*A-Star*):

* **Algoritmo de Dijkstra:** Usa una **Cola de Prioridad (Min-Heap)** para expandir siempre el nodo no visitado con la menor distancia acumulada $g(n)$ desde el origen.
* **Algoritmo A\* (A-Star):** Es la evolución de Dijkstra usada en **Google Maps, Waze y motores de videojuegos (Unity, Unreal Engine)**. En lugar de explorar en todas direcciones como un círculo, suma una **heurística estimada** $h(n)$ (como la distancia en línea recta o euclidiana hacia la meta) y prioriza según:
  $$f(n) = g(n) + h(n)$$
  Esto dirige la búsqueda directamente hacia el destino sin perder la garantía de encontrar la ruta óptima (siempre que $h(n)$ nunca sobreestime el costo real).

* **Complejidad Temporal:** $O((V + E) \log V)$ usando un Min-Heap (`heapq`).

### Implementación de A* / Dijkstra en Python

```python
import heapq

def busqueda_a_estrella(grafo, inicio, meta, heuristica):
    """
    Encuentra el camino de costo mínimo entre 'inicio' y 'meta' usando A*.
    Si heuristica(n) == 0 para todo nodo, funciona exactamente como Dijkstra.
    """
    # Cola de prioridad: (f_score, costo_acumulado_g, nodo_actual, camino)
    frontera = [(heuristica(inicio), 0, inicio, [inicio])]
    mejor_g = {inicio: 0}
    
    while frontera:
        f, g, actual, camino = heapq.heappop(frontera)
        
        if actual == meta:
            return camino, g
            
        if g > mejor_g.get(actual, float("inf")):
            continue
            
        for vecino, peso in grafo.get(actual, []):
            nuevo_g = g + peso
            if nuevo_g < mejor_g.get(vecino, float("inf")):
                mejor_g[vecino] = nuevo_g
                prioridad_f = nuevo_g + heuristica(vecino)
                heapq.heappush(frontera, (prioridad_f, nuevo_g, vecino, camino + [vecino]))
                
    return None, float("inf")

# Prueba rápida
mapa = {
    "A": [("B", 4), ("C", 2)],
    "B": [("C", 1), ("D", 5)],
    "C": [("B", 1), ("D", 8), ("E", 10)],
    "D": [("E", 2)],
    "E": []
}
# Con heurística 0 equivale a Dijkstra puro
ruta, distancia = busqueda_a_estrella(mapa, "A", "E", heuristica=lambda _: 0)
print(f"Ruta óptima: {ruta} (Costo: {distancia})")  # Salida: ['A', 'C', 'B', 'D', 'E'] (Costo: 10)
```

---

## 12. Búsqueda a Escala de Internet: Índices Invertidos y Filtros de Bloom

Para cerrar el panorama industrial, existen dos técnicas que permiten a buscadores web y bases de datos distribuidas responder consultas en milisegundos sobre terabytes de información:

1. **Índice Invertido (*Inverted Index*):**
   * **Dónde se usa:** **Google Search, Elasticsearch, Apache Lucene, motores de búsqueda de comercio electrónico**.
   * **Cómo funciona:** En lugar de buscar una palabra recorriendo millones de documentos, construye un diccionario que mapea cada palabra única hacia la lista ordenada de IDs de documentos donde aparece (`"algoritmo" -> [Doc_2, Doc_15, Doc_89]`). Buscar dos palabras consiste simplemente en **intersectar dos listas ordenadas**.
2. **Filtro de Bloom (*Bloom Filter*):**
   * **Dónde se usa:** **Cassandra, RocksDB, Bigtable, navegadores como Chrome** (para verificar URLs maliciosas) y redes **Blockchain**.
   * **Cómo funciona:** Es una estructura probabilística ultracompacta de bits con múltiples funciones hash que responde en $O(1)$ si un elemento **"definitivamente NO está"** o **"probablemente SÍ está"**. Evita hacer lecturas innecesarias a disco cuando se busca una clave que no existe.

---

## 13. Comparativa General de Complejidad y Uso en la Industria

A continuación se muestra el resumen completo comparando los algoritmos clásicos en arreglos y los algoritmos de búsqueda más utilizados en sistemas reales:

| Algoritmo / Estructura | Mejor Caso | Caso Promedio | Peor Caso | Requisito / Estructura | Uso Principal en la Realidad |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Lineal (Secuencial)** | $O(1)$ | $O(n)$ | $O(n)$ | Ninguno | Listas pequeñas ($n < 50$) o búsqueda única sin índice |
| **Binaria (`bisect`)** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | Arreglo ordenado | Arreglos estáticos en RAM, búsqueda de rangos |
| **Salto (Jump)**| $O(1)$ | $O(\sqrt{n})$ | $O(\sqrt{n})$ | Arreglo ordenado | Estructuras donde retroceder es costoso |
| **Exponencial**| $O(1)$ | $O(\log i)$ | $O(\log n)$ | Arreglo ordenado | Flujos no acotados o cuando el objetivo está al inicio |
| **Interpolación**| $O(1)$ | $O(\log(\log n))$| $O(n)$ | Ordenado y uniforme | Datos numéricos con distribución uniforme conocida |
| **Tabla Hash (`dict`/`set`)** | $O(1)$ | $O(1)$ | $O(n)$* | Memoria adicional | **Estándar en RAM** para búsqueda exacta por clave |
| **Árbol B+ (*B+ Tree*)** | $O(\log_B n)$ | $O(\log_B n)$ | $O(\log_B n)$ | Bloques ordenados | **Estándar en Bases de Datos SQL** y sistemas de archivos |
| **KMP / Boyer-Moore** | $O(n/m)$ | $O(n + m)$ | $O(n + m)$ | Tabla precalculada ($O(m)$) | **Estándar en texto**: `Ctrl+F`, `grep`, ADN |
| **Trie (Árbol Prefijos)** | $O(L)$ | $O(L)$ | $O(L)$ | Árbol de caracteres | **Autocompletado**, correctores, ruteo de IPs |
| **BFS / DFS** | $O(1)$ | $O(V + E)$ | $O(V + E)$ | Grafo o Árbol | Redes sociales, compiladores, web crawlers |
| **Dijkstra / A\*** | $O(E)$ | $O((V+E)\log V)$ | $O((V+E)\log V)$ | Grafo ponderado | **GPS (Google Maps, Waze)**, rutas de red y videojuegos |

*\* El peor caso en Hashing se da cuando todos los elementos colisionan en el mismo índice, lo cual se evita con funciones hash modernas.*

