# Apuntes: Algoritmos Voraces (*Greedy Algorithms*)

Los **algoritmos voraces** (también conocidos en inglés como *greedy algorithms* o algoritmos glotones/ávidos) constituyen uno de los paradigmas de diseño de algoritmos más intuitivos, directos y eficientes en Ciencias de la Computación. Se aplican fundamentalmente a **problemas de optimización**, donde el objetivo es encontrar la mejor solución posible (maximizando ganancias o minimizando costos) entre un conjunto de configuraciones válidas.

La filosofía central del paradigma voraz se resume en una regla de oro:
> **"En cada paso, toma la decisión que parezca mejor en ese preciso momento, de forma miope y localmente óptima, sin reconsiderar nunca las decisiones pasadas (*sin backtracking*)."**

---

## 1. Filosofía y Dinámica del Paradigma

A diferencia de técnicas exhaustivas como la **Fuerza Bruta**, o sistemáticas como la **Programación Dinámica**, un algoritmo voraz no evalúa todas las alternativas futuras ni calcula de antemano el impacto a largo plazo de su elección. Avanza de forma implacable construyendo la solución paso a paso.

```
                   [ Estado Inicial ]
                           │
                           ▼
                 ¿Cuál es la mejor opción
                   disponible AHORA?
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
        [ Opción A (Costo 2) ]  [ Opción B (Costo 7) ]
                │
         (Elegir A y descartar
          B definitivamente)
                │
                ▼
        [ Nueva decisión local... ]
                │
                ▼
        [ Solución Final ]
```

### El dilema: Óptimo Local vs. Óptimo Global
La gran fortaleza de los algoritmos voraces es su **velocidad y bajo consumo de memoria**: rara vez exploran múltiples ramas y casi siempre operan en tiempos lineales $O(n)$ o cuasilineales $O(n \log n)$. 

Sin embargo, su mayor peligro es la **miopía**:
* **Problema bien estructurado:** La secuencia de elecciones localmente óptimas conduce infaliblemente a la solución **óptima global** (ej. Algoritmo de Dijkstra, Árbol de Expansión Mínima).
* **Problema sin estructura voraz:** La elección miope inicial cierra el paso a mejores opciones globales futuras, atrapando al algoritmo en un pésimo subóptimo (ej. Problema del Viajante de Comercio o la Mochila 0/1).

---

## 2. Anatomía y Componentes Formales

Formalmente, todo algoritmo voraz opera sobre una estructura bien definida compuesta por **seis elementos esenciales**:

1. **Conjunto de candidatos ($C$):** La colección de todos los elementos a partir de los cuales se construye una solución (aristas de un grafo, actividades por agendar, denominaciones de monedas, etc.).
2. **Conjunto de seleccionados ($S$):** La solución parcial construida hasta el momento con los candidatos que ya han sido aceptados.
3. **Función de selección:** Métrica heurística que determina, en cada paso, cuál de los candidatos disponibles en $C$ es el más prometedor (el de menor peso, mayor valor, menor duración, etc.).
4. **Función de factibilidad (*Feasibility function*):** Verifica si añadir el candidato seleccionado al conjunto $S$ produce un estado válido que cumpla todas las restricciones del problema (por ejemplo, que no forme ciclos en un árbol o que no exceda la capacidad de una mochila).
5. **Función objetivo:** Criterio numérico que se busca optimizar (maximizar beneficio o minimizar costo).
6. **Función de solución:** Evalúa si el conjunto actual $S$ ya constituye una solución completa y válida al problema original, deteniendo el algoritmo.

### Plantilla genérica en Python

```python
from typing import Any, Callable

def algoritmo_voraz_generico(
    candidatos: list[Any],
    es_solucion: Callable[[list[Any]], bool],
    es_factible: Callable[[list[Any], Any], bool],
    seleccionar_mejor: Callable[[list[Any]], Any]
) -> list[Any] | None:
    """
    Plantilla abstracta del paradigma voraz.
    """
    solucion = []
    candidatos_restantes = candidatos.copy()
    
    while candidatos_restantes and not es_solucion(solucion):
        # 1. Elección voraz local
        mejor_candidato = seleccionar_mejor(candidatos_restantes)
        candidatos_restantes.remove(mejor_candidato)
        
        # 2. Prueba de factibilidad
        if es_factible(solucion, mejor_candidato):
            solucion.append(mejor_candidato)
            
    if es_solucion(solucion):
        return solucion
    return None  # No se pudo construir una solución factible completa
```

---

## 3. Condiciones de Optimalidad: ¿Cuándo funciona Greedy?

Un algoritmo voraz no se puede aplicar a ciegas. Para asegurar matemáticamente que la solución encontrada sea el **óptimo global**, el problema debe satisfacer dos propiedades teóricas fundamentales demostradas por Thomas H. Cormen et al. (CLRS):

### 3.1 Propiedad de la Elección Voraz (*Greedy-Choice Property*)
Una solución globalmente óptima puede alcanzarse tomando decisiones localmente óptimas (voraces) en cada paso.
* A diferencia de la **Programación Dinámica**, donde la decisión en el estado actual depende de haber resuelto previamente todos los subproblemas derivados, en el paradigma voraz **primero se hace la elección** y luego se resuelve el único subproblema resultante.
* Las decisiones son **irrevocables**: nunca se hace *backtracking* para corregir una elección anterior.

### 3.2 Subestructura Óptima (*Optimal Substructure*)
Una solución óptima al problema general contiene dentro de sí soluciones óptimas a los subproblemas derivados.
* Si $S$ es la solución óptima a una instancia $P$, y realizamos la primera elección voraz $x$, el conjunto restante $S \setminus \{x\}$ debe ser la solución óptima al subproblema residual $P'$.

```
[ Solución Óptima Global: S ] = { Elección Voraz x } U { Solución Óptima del Subproblema P' }
```

---

## 4. Técnicas de Demostración de Correctitud

Probar que un algoritmo voraz es correcto suele ser **mucho más difícil que diseñarlo o programarlo**. La intuición suele engañar. Las dos técnicas formales más utilizadas en el análisis matemático de algoritmos son:

### 4.1 Argumento de Intercambio (*Exchange Argument*)
Es la técnica más poderosa y extendida:
1. Supongamos que existe una solución óptima arbitraria $O$ que difiere de nuestra solución voraz $G$.
2. Identificamos el **primer punto de divergencia** donde $O$ y $G$ toman decisiones distintas.
3. Demostramos que podemos intercambiar el elemento elegido por $O$ por el elemento elegido por $G$ sin violar la factibilidad y sin empeorar el valor de la función objetivo.
4. Repitiendo este proceso de intercambio de forma inductiva, transformamos gradualmente $O$ en $G$ demostrando que el costo de $G$ es menor o igual al de $O$. Como $O$ era óptima, **$G$ también debe ser óptima**.

### 4.2 El Voraz se Mantiene a la Vanguardia (*Greedy Stays Ahead*)
Se utiliza midiendo el progreso de la solución en cada paso $k$:
1. Se define una métrica de progreso cuantitativa $M$.
2. Se demuestra por inducción matemática que para todo paso $k \in \{1, 2, \dots, m\}$:
   $$M(G_k) \ge M(O_k) \quad \text{(para maximización)}$$
3. Al llegar al paso final, la solución voraz habrá alcanzado al menos el mismo rendimiento que cualquier otra solución factible óptima.

### 4.3 Teoría de Matroides (Breve fundamento algebraico)
Un **matroide** es una estructura combinatoria abstracta $(S, \mathcal{I})$ que generaliza la noción de independencia lineal del álgebra lineal.
* Si los subconjuntos factibles de un problema de optimización forman un matroide con pesos, el **Teorema de Rado-Edmonds** garantiza que el algoritmo voraz clásico siempre devolverá la solución óptima absoluta (este es el fundamento formal detrás del Algoritmo de Kruskal).

---

## 5. Comparativa: Voraz vs. Programación Dinámica vs. Divide y Vencerás

| Característica | Algoritmos Voraces (*Greedy*) | Programación Dinámica (*DP*) | Divide y Vencerás (*D&C*) |
| :--- | :--- | :--- | :--- |
| **Toma de decisiones** | **Miope e irrevocable:** Toma la mejor opción local en cada paso sin explorar ramas. | **Exhaustiva e informada:** Evalúa todas las elecciones posibles y guarda resultados. | **División estructural:** Divide el problema en mitades o partes fijas independientes. |
| **Subproblemas** | Genera **un solo** subproblema tras cada decisión voraz. | Subproblemas **solapados** que se repiten con alta frecuencia. | Subproblemas **independientes y disjuntos** (no se solapan). |
| **Dirección** | *Top-down* lineal (iterativo o recursión directa). | *Top-down* con Memoización o *Bottom-up* con Tabulación. | *Top-down* recursivo con fase de combinación. |
| **Complejidad típica** | Muy eficiente: $O(n)$ o $O(n \log n)$. | Polinomial moderada: $O(n^2)$, $O(n \cdot W)$, $O(n^3)$. | Logarítmica o cuasilineal: $O(\log n)$, $O(n \log n)$. |
| **Uso de memoria** | Mínimo: comúnmente $O(1)$ o $O(n)$. | Elevado: tablas de memoización $O(n)$ o $O(n \times W)$. | Moderado: pila de llamadas recursivas $O(\log n)$. |
| **Garantía de éxito** | **No universal:** Requiere que se cumpla la propiedad de elección voraz. | **Garantizada:** Siempre encuentra el óptimo si la subestructura es óptima. | **Garantizada:** Siempre une las soluciones parciales de manera exacta. |

---

## 6. Dos Estudios de Caso Clásicos: Cuándo Funciona y Cuándo Falla

### Caso 1: El Problema de la Mochila (*Knapsack Problem*)

Imagina que dispones de una mochila con capacidad máxima de peso $W = 50\text{ kg}$ y tres artículos disponibles:

| Objeto | Peso ($w_i$) | Valor ($v_i$) | Densidad de valor ($\rho_i = v_i / w_i$) |
| :---: | :---: | :---: | :---: |
| **A** | $10\text{ kg}$ | $\$60$ | $\$6/\text{kg}$ |
| **B** | $20\text{ kg}$ | $\$100$ | $\$5/\text{kg}$ |
| **C** | $30\text{ kg}$ | $\$120$ | $\$4/\text{kg}$ |

#### Variante Fraccionaria (*Fractional Knapsack*): ¡Greedy es ÓPTIMO!
Podemos fraccionar los objetos (llevar polvos, líquidos o telas).
* **Estrategia voraz:** Ordenar y tomar según la mayor densidad de valor $\rho_i$.
* **Paso 1:** Tomamos todo el objeto **A** ($10\text{ kg}$, valor $\$60$). Capacidad restante: $40\text{ kg}$.
* **Paso 2:** Tomamos todo el objeto **B** ($20\text{ kg}$, valor $\$100$). Capacidad restante: $20\text{ kg}$.
* **Paso 3:** Del objeto **C** solo caben $20\text{ kg}$ de sus $30\text{ kg}$. Tomamos la fracción $\frac{20}{30} = \frac{2}{3}$ de **C** (valor $\frac{2}{3} \times \$120 = \$80$).
* **Ganancia total:** $\$60 + \$100 + \$80 = \mathbf{\$240}$ (Óptimo absoluto en tiempo $O(n \log n)$).

#### Variante 0/1 (Objetos indivisibles): ¡Greedy FRACASA!
Los objetos deben tomarse enteros o dejarse.
* Si aplicamos la misma estrategia voraz (mayor densidad):
  * Tomamos **A** ($10\text{ kg}$, $\$60$). Capacidad restante: $40\text{ kg}$.
  * Tomamos **B** ($20\text{ kg}$, $\$100$). Capacidad restante: $20\text{ kg}$.
  * El objeto **C** pesa $30\text{ kg}$ y no cabe. Se descarta.
  * **Ganancia voraz:** $\$60 + \$100 = \mathbf{\$160}$ (peso total: $30\text{ kg}$, desperdiciando $20\text{ kg}$).
* **Solución óptima global real:**
  * Ignoramos **A** y tomamos **B** ($20\text{ kg}$) + **C** ($30\text{ kg}$).
  * Peso total: $50\text{ kg}$ (llena la mochila).
  * **Ganancia óptima:** $\$100 + \$120 = \mathbf{\$220}$.
* **Conclusión:** La mochila 0/1 no tiene la propiedad de elección voraz; requiere **Programación Dinámica** con tiempo pseudo-polinomial $O(n \cdot W)$.

---

### Caso 2: El Problema del Cambio de Monedas (*Coin Change Problem*)

Queremos dar un cambio exacto de $V$ utilizando la **menor cantidad posible de monedas**.

#### Sistema Canónico (Monedas de curso legal estándar)
Denominaciones: $\{1, 2, 5, 10\}$. Queremos dar cambio de $\$18$.
* Estrategia voraz: Elegir siempre la moneda de mayor valor menor o igual al resto.
  * $\$18 - 10 = \$8$ (1 moneda de 10)
  * $\$8 - 5 = \$3$ (1 moneda de 5)
  * $\$3 - 2 = \$1$ (1 moneda de 2)
  * $\$1 - 1 = \$0$ (1 moneda de 1)
* **Total:** 4 monedas ($10 + 5 + 2 + 1$). Es el óptimo global garantizado.

#### Sistema No Canónico (Donde Greedy fracasa rotundamente)
Denominaciones arbitrarias: $\{1, 3, 4\}$. Queremos dar cambio de **$\$6$**.
* **Elección voraz:**
  * Toma la moneda mayor: $4$. Restante: $\$2$.
  * No caben de $4$ ni de $3$; toma dos monedas de $1$.
  * **Resultado voraz:** $4 + 1 + 1 \implies \mathbf{3\text{ monedas}}$.
* **Solución óptima:**
  * $3 + 3 = 6 \implies \mathbf{2\text{ monedas}}$.
* **Conclusión:** El algoritmo voraz devuelve una solución subóptima si el sistema monetario no es canónico.

---

## 7. Algoritmos Clásicos: Teoría, Complejidad e Implementación en Python

---

### 7.1 Selección de Actividades (*Activity Selection Problem*)

#### Planteamiento
Dado un conjunto de $n$ actividades con tiempos de inicio $s_i$ y terminación $f_i$, determinar el **subconjunto compatible de tamaño máximo** (ninguna actividad debe solaparse con otra en el tiempo).

```
Actividad A: [====]             (fina: 4)
Actividad B:    [========]      (fina: 9)
Actividad C:       [====]       (fina: 7)
Actividad D:             [===]  (fina: 11)
```

#### ¿Cuál es la heurística voraz correcta?
* **¿Menor duración ($f_i - s_i$)?** Falla: una actividad corta en medio puede bloquear dos actividades largas en los extremos.
* **¿Menor tiempo de inicio ($s_i$)?** Falla: una actividad que empieza muy temprano y dura todo el día bloquea a todas las demás.
* **¿Menor tiempo de terminación ($f_i$)?** **¡Correcto!** Terminar lo más temprano posible deja el mayor tiempo disponible libre para acomodar las actividades restantes.

#### Análisis de Complejidad
* **Temporal:** $O(n \log n)$ para ordenar las actividades por tiempo de fin + $O(n)$ para recorrerlas linealmente $\implies \mathbf{\Theta(n \log n)}$.
* **Espacial:** $\mathbf{O(n)}$ para almacenar el subconjunto solución.

#### Implementación en Python

```python
from typing import NamedTuple

class Actividad(NamedTuple):
    nombre: str
    inicio: int
    fin: int

def seleccion_actividades(actividades: list[Actividad]) -> list[Actividad]:
    """
    Selecciona el número máximo de actividades compatibles mutuamente.
    Complejidad: O(n log n) en tiempo, O(n) en espacio.
    """
    if not actividades:
        return []

    # 1. ORDENAR vorazmente por tiempo de fin ascendente (f_i)
    ordenadas = sorted(actividades, key=lambda a: a.fin)

    seleccionadas = [ordenadas[0]]
    ultimo_fin = ordenadas[0].fin

    # 2. SELECCIÓN LINEAL: escoger la siguiente actividad compatible
    for act in ordenadas[1:]:
        if act.inicio >= ultimo_fin:  # No hay solapamiento
            seleccionadas.append(act)
            ultimo_fin = act.fin

    return seleccionadas

# Caso de prueba
if __name__ == "__main__":
    lista_actividades = [
        Actividad("A1", 1, 4),
        Actividad("A2", 3, 5),
        Actividad("A3", 0, 6),
        Actividad("A4", 5, 7),
        Actividad("A5", 3, 9),
        Actividad("A6", 5, 9),
        Actividad("A7", 6, 10),
        Actividad("A8", 8, 11),
        Actividad("A9", 8, 12),
        Actividad("A10", 2, 14),
        Actividad("A11", 12, 16)
    ]
    res = seleccion_actividades(lista_actividades)
    print("Actividades seleccionadas:", [a.nombre for a in res])
    # Resultado esperado: ['A1', 'A4', 'A8', 'A11'] (4 actividades)
```

---

### 7.2 Problema de la Mochila Fraccionaria (*Fractional Knapsack*)

#### Planteamiento
Dada una capacidad $W$ y $n$ artículos, cada uno con valor $v_i$ y peso $w_i$, podemos tomar cualquier fracción $x_i \in [0, 1]$ de cada artículo. Buscamos maximizar el valor total recolectado sin exceder $W$.

#### Estrategia Voraz
Calcular la **densidad de valor** $\rho_i = v_i / w_i$ para cada artículo. Ordenar en orden descendente y llenar la mochila con los artículos de mayor densidad. Si el último artículo no cabe por completo, tomar exactamente la fracción que llena el espacio restante.

#### Análisis de Complejidad
* **Temporal:** $O(n \log n)$ debido al ordenamiento de densidades. (Se puede optimizar a $O(n)$ usando selección lineal rápida / Quickselect de medianas).
* **Espacial:** $O(n)$ o $O(1)$ auxiliar si se ordena *in-place*.

#### Implementación en Python

```python
class Articulo:
    def __init__(self, nombre: str, valor: float, peso: float):
        self.nombre = nombre
        self.valor = valor
        self.peso = peso
        self.densidad = valor / peso

def mochila_fraccionaria(capacidad: float, articulos: list[Articulo]) -> tuple[float, list[tuple[str, float]]]:
    """
    Resuelve la mochila fraccionaria con estrategia voraz por densidad de valor.
    Devuelve (valor_total_obtenido, lista_de_porciones_tomadas).
    """
    # 1. Ordenar por densidad de valor descendente
    articulos_ordenados = sorted(articulos, key=lambda a: a.densidad, reverse=True)

    valor_total = 0.0
    capacidad_restante = capacidad
    detalle = []

    for item in articulos_ordenados:
        if capacidad_restante <= 0:
            break

        if item.peso <= capacidad_restante:
            # Cabe completo
            valor_total += item.valor
            capacidad_restante -= item.peso
            detalle.append((item.nombre, 1.0))
        else:
            # Solo cabe una fracción
            fraccion = capacidad_restante / item.peso
            valor_total += item.valor * fraccion
            detalle.append((item.nombre, fraccion))
            capacidad_restante = 0.0

    return valor_total, detalle

# Caso de prueba
if __name__ == "__main__":
    items = [
        Articulo("Oro en polvo", 60, 10),
        Articulo("Plata en grano", 100, 20),
        Articulo("Cobre en viruta", 120, 30)
    ]
    val_max, fracciones = mochila_fraccionaria(50.0, items)
    print(f"Valor máximo: ${val_max:.2f}")  # 240.00
    print("Detalle:", fracciones)  # Oro: 1.0, Plata: 1.0, Cobre: 0.6667
```

---

### 7.3 Codificación de Huffman (*Huffman Coding*)

#### Planteamiento
Es un algoritmo fundamental de **compresión de datos sin pérdida**. Los sistemas estándar asignan un número fijo de bits a cada carácter (ej. ASCII usa 8 bits por letra). Huffman utiliza **códigos de longitud variable libres de prefijo** (*prefix codes*):
* Los caracteres que aparecen con **mayor frecuencia** reciben códigos binarios **muy cortos** (1 o 2 bits).
* Los caracteres que aparecen raramente reciben códigos más largos.
* **Condición de libre prefijo:** Ningún código asignado puede ser prefijo de otro, permitiendo decodificar de izquierda a derecha sin ambigüedad.

#### Estrategia Voraz
1. Contar la frecuencia de cada carácter.
2. Cada carácter se convierte en un nodo hoja con su peso respectivo.
3. Se insertan todos los nodos en una **cola de prioridad de mínimos (Min-Heap)**.
4. **Bucle voraz:** En cada paso, extraer los dos nodos con menores frecuencias ($n_1$ y $n_2$). Fusionarlos creando un nodo padre cuya frecuencia sea la suma de ambas, y reinsertarlo en el heap.
5. Repetir hasta que quede un único nodo raíz: el **Árbol de Huffman**.
6. Recorrer el árbol asignando `'0'` a la rama izquierda y `'1'` a la rama derecha.

```
                  (Total: 100)
                  /          \
                '0'          '1'
             (Freq: 45)     (Freq: 55)
               [ 'a' ]       /      \
                           '0'      '1'
                       (Freq: 25)  [ 'b': 30 ]
                         /    \
                       '0'    '1'
                   [ 'c': 12 ][ 'd': 13 ]
```

#### Análisis de Complejidad
* **Temporal:** $O(k \log k)$ donde $k$ es el número de caracteres únicos (alfabeto), ya que realizamos $k-1$ extracciones e inserciones en el heap de tamaño $k$.
* **Espacial:** $O(k)$ para almacenar los nodos del árbol y la tabla de códigos.

#### Implementación en Python

```python
import heapq
from collections import Counter
from typing import Optional

class NodoHuffman:
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.izq: Optional['NodoHuffman'] = None
        self.der: Optional['NodoHuffman'] = None

    # Comparador para el Min-Heap
    def __lt__(self, otro: 'NodoHuffman') -> bool:
        return self.freq < otro.freq

def construir_arbol_huffman(texto: str) -> Optional[NodoHuffman]:
    if not texto:
        return None

    # Contar frecuencias de caracteres
    frecuencias = Counter(texto)

    # Min-Heap voraz
    heap: list[NodoHuffman] = [NodoHuffman(c, f) for c, f in frecuencias.items()]
    heapq.heapify(heap)

    # Caso especial: solo un carácter único
    if len(heap) == 1:
        raiz = NodoHuffman(None, heap[0].freq)
        raiz.izq = heapq.heappop(heap)
        return raiz

    # Fusión voraz de los dos nodos de menor frecuencia
    while len(heap) > 1:
        nodo1 = heapq.heappop(heap)
        nodo2 = heapq.heappop(heap)

        padre = NodoHuffman(None, nodo1.freq + nodo2.freq)
        padre.izq = nodo1
        padre.der = nodo2

        heapq.heappush(heap, padre)

    return heap[0]

def generar_codigos(raiz: Optional[NodoHuffman]) -> dict[str, str]:
    codigos = {}

    def _dfs(nodo: Optional[NodoHuffman], prefijo: str):
        if nodo is None:
            return
        if nodo.char is not None:
            codigos[nodo.char] = prefijo if prefijo else "0"
            return
        _dfs(nodo.izq, prefijo + "0")
        _dfs(nodo.der, prefijo + "1")

    _dfs(raiz, "")
    return codigos

def codificar_huffman(texto: str) -> tuple[str, dict[str, str]]:
    raiz = construir_arbol_huffman(texto)
    codigos = generar_codigos(raiz)
    texto_codificado = "".join(codigos[c] for c in texto)
    return texto_codificado, codigos

# Caso de prueba
if __name__ == "__main__":
    mensaje = "ABRACADABRA"
    codificado, tabla = codificar_huffman(mensaje)
    print("Tabla de códigos:", tabla)
    print("Texto codificado en bits:", codificado)
    print(f"Longitud original (8 bits/char): {len(mensaje) * 8} bits")
    print(f"Longitud comprimida: {len(codificado)} bits")
```

---

### 7.4 Árbol de Expansión Mínima (MST): Algoritmo de Kruskal

#### Planteamiento
Dado un grafo no dirigido conexo y ponderado $G = (V, E)$, un **Árbol de Expansión Mínima** (*Minimum Spanning Tree*) es un subgrafo que conecta todos los vértices sin formar ciclos (un árbol) y cuya suma total de pesos en las aristas es la mínima posible.

#### Estrategia Voraz de Kruskal
1. Tomar todas las aristas $E$ y ordenarlas de menor a mayor peso.
2. Inicializar cada vértice en su propio conjunto disjunto.
3. Recorrer las aristas ordenadas e incorporar vorazmente la arista $(u, v)$ a la solución **siempre y cuando sus extremos no pertenezcan ya al mismo componente conexo** (para evitar ciclos).
4. Para realizar estas comprobaciones en tiempo casi constante, se utiliza la estructura de datos **Disjoint Set Union (DSU) / Union-Find** con compresión de caminos y unión por rango.

#### Análisis de Complejidad
* **Temporal:** $O(E \log E)$ por el ordenamiento inicial de aristas. Como $E \le V^2$, $\log(E) \le 2\log(V)$, por lo que la complejidad se escribe equivalentemente como $\mathbf{O(E \log V)}$. Las operaciones sobre el DSU toman tiempo casi lineal $O(E \cdot \alpha(V))$ donde $\alpha$ es la función inversa de Ackermann ($\alpha(V) \le 4$ en el universo observable).
* **Espacial:** $\mathbf{O(V + E)}$ para almacenar el grafo y las estructuras del DSU.

#### Implementación en Python

```python
class DisjointSetUnion:
    """Estructura DSU con Unión por Rango y Compresión de Caminos."""
    def __init__(self, n: int):
        self.padre = list(range(n))
        self.rango = [0] * n

    def find(self, x: int) -> int:
        if self.padre[x] != x:
            # Compresión de caminos
            self.padre[x] = self.find(self.padre[x])
        return self.padre[x]

    def union(self, x: int, y: int) -> bool:
        raiz_x = self.find(x)
        raiz_y = self.find(y)

        if raiz_x == raiz_y:
            return False  # Ya están en el mismo conjunto (formaría ciclo)

        # Unión por rango
        if self.rango[raiz_x] < self.rango[raiz_y]:
            self.padre[raiz_x] = raiz_y
        elif self.rango[raiz_x] > self.rango[raiz_y]:
            self.padre[raiz_y] = raiz_x
        else:
            self.padre[raiz_y] = raiz_x
            self.rango[raiz_x] += 1
            
        return True

def kruskal(num_vertices: int, aristas: list[tuple[int, int, float]]) -> tuple[float, list[tuple[int, int, float]]]:
    """
    Algoritmo de Kruskal para el Árbol de Expansión Mínima (MST).
    aristas: lista de tuplas (origen, destino, peso).
    """
    # 1. ORDENAR aristas vorazmente por peso ascendente
    aristas_ordenadas = sorted(aristas, key=lambda a: a[2])
    
    dsu = DisjointSetUnion(num_vertices)
    mst = []
    costo_total = 0.0

    for u, v, peso in aristas_ordenadas:
        # 2. SELECCIÓN: si no forman ciclo, unir conjuntos
        if dsu.union(u, v):
            mst.append((u, v, peso))
            costo_total += peso
            if len(mst) == num_vertices - 1:
                break  # El MST está completo

    return costo_total, mst

# Caso de prueba
if __name__ == "__main__":
    # Grafo con 4 vértices (0, 1, 2, 3)
    grafo_aristas = [
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4)
    ]
    costo, arbol = kruskal(4, grafo_aristas)
    print(f"Costo total del MST (Kruskal): {costo}")  # 19 (aristas: (2,3,4), (0,3,5), (0,1,10))
    print("Aristas del MST:", arbol)
```

---

### 7.5 Árbol de Expansión Mínima (MST): Algoritmo de Prim

#### Planteamiento
Al igual que Kruskal, Prim encuentra el MST de un grafo no dirigido conexo y ponderado. Sin embargo, su enfoque de construcción es diferente:
* Kruskal hace crecer un "bosque" de árboles independientes que se van uniendo.
* **Prim hace crecer un único árbol central desde un nodo raíz arbitrario**, incorporando en cada iteración la arista de menor peso que comunique un nodo ya integrado al árbol con un nodo exterior aún no visitado.

#### Estrategia Voraz de Prim
1. Iniciar con un vértice inicial cualquiera $s$ marcado como visitado.
2. Colocar todas las aristas incidentes de $s$ en una cola de prioridad de mínimos (Min-Heap).
3. **Bucle voraz:** Extraer del heap la arista con menor peso $(u, v)$. Si el extremo $v$ ya está en el árbol, se descarta. Si no está, se incorpora la arista al MST, se marca $v$ como visitado y se añaden todas sus aristas hacia nodos no visitados al heap.
4. Repetir hasta haber visitado todos los vértices.

#### Kruskal vs. Prim: ¿Cuál usar?
* **Grafo disperso ($E \ll V^2$):** **Kruskal** suele ser más rápido y simple de implementar.
* **Grafo denso ($E \approx V^2$):** **Prim** es superior, especialmente con matriz de adyacencia ($O(V^2)$) o con montículos de Fibonacci ($O(E + V \log V)$).

#### Implementación en Python

```python
import heapq

def prim(num_vertices: int, adyacencias: dict[int, list[tuple[int, float]]]) -> tuple[float, list[tuple[int, int, float]]]:
    """
    Algoritmo de Prim para MST usando Min-Heap.
    adyacencias[u] = [(v, peso), ...]
    Complejidad: O(E log V) en tiempo, O(V + E) en espacio.
    """
    visitados = [False] * num_vertices
    mst = []
    costo_total = 0.0

    # Heap almacena tuplas: (peso, u, v)
    # Comenzamos arbitrariamente desde el vértice 0
    heap: list[tuple[float, int, int]] = []
    visitados[0] = True
    for v, peso in adyacencias.get(0, []):
        heapq.heappush(heap, (peso, 0, v))

    while heap and len(mst) < num_vertices - 1:
        peso, u, v = heapq.heappop(heap)

        if visitados[v]:
            continue

        # Elección voraz: incluir el vértice v al árbol
        visitados[v] = True
        mst.append((u, v, peso))
        costo_total += peso

        for vecino, peso_vecino in adyacencias.get(v, []):
            if not visitados[vecino]:
                heapq.heappush(heap, (peso_vecino, v, vecino))

    return costo_total, mst

# Caso de prueba
if __name__ == "__main__":
    ady: dict[int, list[tuple[int, float]]] = {
        0: [(1, 10), (2, 6), (3, 5)],
        1: [(0, 10), (3, 15)],
        2: [(0, 6), (3, 4)],
        3: [(0, 5), (1, 15), (2, 4)]
    }
    costo, arbol = prim(4, ady)
    print(f"Costo total del MST (Prim): {costo}")  # 19
    print("Aristas del MST:", arbol)
```

---

### 7.6 Caminos Mínimos desde Origen Único: Algoritmo de Dijkstra

#### Planteamiento
Dado un grafo dirigido o no dirigido ponderado con **pesos no negativos** ($w(e) \ge 0$) y un vértice origen $s$, hallar la distancia mínima desde $s$ hacia todos los demás vértices del grafo.

#### ¿Por qué Dijkstra es un Algoritmo Voraz?
En cada paso, Dijkstra selecciona el vértice no visitado $u$ que tenga la **menor distancia tentativa acumulada** $d[u]$ desde el origen. En el instante en que $u$ es extraído del heap, el algoritmo decreta esa distancia como **definitiva e inmutable** (propiedad voraz), relajando a partir de él las distancias hacia sus vecinos:
$$d[v] = \min(d[v], d[u] + w(u, v))$$

#### La gran trampa: ¿Por qué falla con pesos negativos?
Si existen aristas con pesos negativos, una distancia que el algoritmo declaró como "óptima e inmutable" podría abaratarse posteriormente a través de un camino más largo que contenga una arista intensamente negativa. Dijkstra es incapaz de retroceder para corregir esto. Para grafos con pesos negativos debe usarse **Bellman-Ford** (Programación Dinámica, $O(V \cdot E)$).

#### Análisis de Complejidad
* **Temporal con Min-Heap binario:** $\mathbf{O((V + E) \log V)}$.
* **Espacial:** $\mathbf{O(V + E)}$ para almacenar listas de adyacencia y arreglos de distancias.

#### Implementación en Python

```python
import heapq

def dijkstra(num_vertices: int, adyacencias: dict[int, list[tuple[int, float]]], origen: int) -> tuple[list[float], list[int]]:
    """
    Calcula distancias mínimas desde el vértice origen.
    Retorna (distancias, predecesores).
    """
    distancias = [float('inf')] * num_vertices
    predecesores = [-1] * num_vertices
    distancias[origen] = 0.0

    # Heap contiene pares: (distancia_acumulada, vertice)
    heap: list[tuple[float, int]] = [(0.0, origen)]

    while heap:
        dist_actual, u = heapq.heappop(heap)

        # Si encontramos una distancia desactualizada en el heap, la ignoramos
        if dist_actual > distancias[u]:
            continue

        # Relajación voraz de aristas
        for v, peso in adyacencias.get(u, []):
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias[v]:
                distancias[v] = nueva_dist
                predecesores[v] = u
                heapq.heappush(heap, (nueva_dist, v))

    return distancias, predecesores

# Caso de prueba
if __name__ == "__main__":
    grafo = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }
    dist, pred = dijkstra(4, grafo, 0)
    print("Distancias desde el origen 0:", dist)  # [0.0, 3.0, 1.0, 4.0]
```

---

## 8. Algoritmos Voraces como Heurísticas y Aproximaciones

Existen problemas sumamente complejos clasificados como **NP-Difíciles (NP-Hard)** donde no existe ningún algoritmo que encuentre la solución exacta en tiempo polinomial (a menos que $P = NP$).

En estos escenarios, los algoritmos voraces se utilizan como **heurísticas de aproximación**: renuncian a garantizar el óptimo absoluto a cambio de entregar una **solución razonablemente buena en tiempo casi instantáneo**.

### 8.1 Problema del Viajante de Comercio (TSP) - Heurística del Vecino más Cercano
* **Estrategia voraz:** Comenzar en una ciudad y viajar sucesivamente a la ciudad no visitada más cercana, cerrando el ciclo al volver al origen.
* **Costo computacional:** Muy veloz, $O(n^2)$.
* **Calidad:** En el peor de los casos, la ruta voraz puede ser arbitrariamente mala (el factor de aproximación no está acotado si no se cumple la desigualdad triangular).

### 8.2 Cobertura de Conjuntos (*Set Cover Problem*)
* **Problema:** Dado un universo $U$ y una familia de subconjuntos $\mathcal{S}$, seleccionar la menor cantidad de subconjuntos cuya unión cubra todo $U$.
* **Estrategia voraz:** En cada paso, elegir el subconjunto que cubra la mayor cantidad de elementos **aún no cubiertos**.
* **Garantía teórica:** Johnson y Chvátal demostraron que esta regla voraz tiene un factor de aproximación de:
  $$\alpha = H(n) = \sum_{i=1}^n \frac{1}{i} \approx \ln(n) + 1$$
  Es decir, la solución voraz nunca superará al óptimo por más de un factor logarítmico.

---

## 9. Ficha Técnica y Tabla Comparativa de Complejidades

| Problema | Algoritmo | Criterio de Selección Voraz | Estructura de Datos Clave | Complejidad Temporal | Complejidad Espacial | ¿Garantiza Óptimo Global? |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **Selección de Actividades** | Interval Scheduling | Menor tiempo de fin ($f_i$) | Arreglo ordenado | $\Theta(n \log n)$ | $O(n)$ | **Sí** |
| **Mochila Fraccionaria** | Voraz por Densidad | Mayor densidad ($v_i / w_i$) | Arreglo ordenado / Heap | $O(n \log n)$ | $O(1)$ aux | **Sí** |
| **Mochila 0/1** | Heurística Voraz | Mayor densidad ($v_i / w_i$) | Arreglo ordenado | $O(n \log n)$ | $O(1)$ aux | **NO** (Subóptimo) |
| **Cambio de Monedas** | Voraz Canónico | Mayor denominación $\le$ resto | Arreglo descendente | $O(n)$ | $O(1)$ | **Condicional** (solo canónicos) |
| **Codificación de Datos** | Algoritmo de Huffman | Menor frecuencia de caracteres | Min-Heap binario | $O(k \log k)$ | $O(k)$ | **Sí** |
| **Árbol de Expansión (MST)** | Kruskal | Menor peso de arista global | DSU (*Union-Find*) | $O(E \log V)$ | $O(V + E)$ | **Sí** |
| **Árbol de Expansión (MST)** | Prim | Menor peso de arista frontera | Min-Heap binario | $O(E \log V)$ | $O(V + E)$ | **Sí** |
| **Caminos Mínimos** | Dijkstra | Menor distancia acumulada | Min-Heap binario | $O((V + E) \log V)$ | $O(V + E)$ | **Sí** (pesos $\ge 0$) |
| **Viajante de Comercio (TSP)** | Vecino más cercano | Menor distancia a nodo libre | Matriz de distancias | $O(V^2)$ | $O(V)$ | **NO** (Aproximación) |

---

## 10. Errores Frecuentes, Trampas y Buenas Prácticas

1. **La falacia del "Suena lógico":** Asumir que porque una regla parece óptima a nivel intuitivo, el algoritmo devolverá la respuesta correcta. En algoritmos voraces, **siempre se debe exigir una demostración formal** (o buscar activamente un contraejemplo numérico simple).
2. **Olvidar el costo de ordenamiento inicial:** La fase de selección iterativa suele ser $O(n)$, pero requiere ordenar los candidatos previamente ($O(n \log n)$). Omitir esto en exámenes conduce a un cálculo erróneo de la complejidad.
3. **No usar la estructura de datos adecuada:**
   * Implementar Kruskal buscando ciclos con BFS/DFS tradicional eleva el costo a $O(V \cdot E)$. Debe usarse siempre **DSU con compresión de caminos**.
   * Buscar el mínimo linealmente en Dijkstra eleva el tiempo a $O(V^2)$. Con **Min-Heap** baja a $O(E \log V)$.
4. **Ignorar las precondiciones del grafo:** Aplicar Dijkstra con aristas negativas conduce a bucles silenciosos o respuestas erróneas. Comprobar siempre que todos los pesos sean no negativos ($w \ge 0$).

---

## 11. Ejercicios Propuestos y Problemas de Examen

1. **Secuenciación de Tareas con Deadlines (*Job Sequencing with Deadlines*):**
   * Dado un conjunto de $n$ tareas, donde cada tarea tiene un tiempo límite (*deadline*) y un beneficio si se completa antes o en el deadline (cada tarea toma exactamente 1 unidad de tiempo). Diseña un algoritmo voraz en $O(n \log n)$ o $O(n^2)$ que maximice la ganancia total.
2. **Salas de Reuniones Mínimas (*Meeting Rooms II*):**
   * Dada una serie de intervalos de tiempo para conferencias $[s_i, e_i]$, determinar el número mínimo de salas de conferencias requeridas para que ninguna reunión se solape. Demuestra cómo resolverlo vorazmente en $O(n \log n)$ usando ordenamiento de puntos temporales o un Min-Heap.
3. **Reventar Globos con Flechas Mínimas (*Minimum Arrows to Burst Balloons*):**
   * Hay varios globos esféricos alineados en un plano $2D$, dados como intervalos $[x_{\text{inicio}}, x_{\text{fin}}]$. Una flecha disparada en $x$ revienta todos los globos cuya proyección cubra $x$. Determina la menor cantidad de flechas necesarias modelándolo como una variante de selección de intervalos.
4. **El Problema de las Gasolineras (*Gas Station / Circular Tour*):**
   * En una ruta circular hay $n$ gasolineras. En cada estación $i$ hay una cantidad de combustible `gas[i]` y cuesta `cost[i]` viajar a la siguiente estación. Demuestra que si la suma total de combustible supera o iguala al costo total, existe un único punto de inicio garantizado que se puede encontrar en un solo recorrido voraz $O(n)$.
5. **Partición de Etiquetas (*Partition Labels*):**
   * Dada una cadena de caracteres (ej. `"ababcbacadefegdehijhklij"`), partirla en el mayor número posible de partes de modo que cada letra aparezca a lo sumo en una sola parte. Diseña un algoritmo voraz $O(n)$ rastreando el último índice de aparición de cada carácter.
