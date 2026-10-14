# Actividad 3: Teorema Maestro y Divide y Vencerás

**Archivos de Código Fuente en C:**
* 📄 [Búsqueda en Árbol Binario Completo (`busqueda_arbol_completo.c`)](./busqueda_arbol_completo.c)
* 📄 [Par de Puntos más Cercanos (`closest 1.c`)](./closest%201.c)

---

## 1. Fundamentos Teóricos

### 1.1 El Paradigma Divide y Vencerás (*Divide and Conquer*)

El paradigma de diseño **Divide y Vencerás** resuelve un problema computacional complejo descomponiéndolo recursivamente en subproblemas más pequeños del mismo tipo, hasta alcanzar una dimensión trivial (*caso base*) que se resuelve directamente. Consta de tres fases fundamentales:

1. **Dividir ($D(n)$):** Descomponer la instancia del problema de tamaño $n$ en $a$ subproblemas disjuntos, cada uno de tamaño $n/b$.
2. **Conquistar / Vencer:** Resolver recursivamente cada uno de los $a$ subproblemas. Si el tamaño del subproblema es suficientemente pequeño ($n \le c$), se resuelve por fuerza bruta o de forma directa en tiempo constante $O(1)$.
3. **Combinar ($C(n)$):** Fusionar las soluciones parciales obtenidas de los subproblemas para construir la solución global de la instancia original.

El costo temporal no recursivo acumulado por nivel es:
$$f(n) = D(n) + C(n)$$

---

### 1.2 El Teorema Maestro (*Master Theorem*)

Aplica a ecuaciones de recurrencia con la forma canónica:

$$T(n) = a\,T\!\left(\frac{n}{b}\right) + f(n)$$

Donde:
* $a \ge 1$: Número de subproblemas recursivos generados en cada llamada (factor de ramificación).
* $b > 1$: Factor de reducción del tamaño de entrada en cada llamada.
* $f(n)$: Trabajo realizado fuera de las llamadas recursivas (división + combinación).

El comportamiento asintótico se rige por el **exponente crítico**:
$$c_{\text{crit}} = \log_b a$$

El cual determina el costo del nivel de las hojas: $L(n) = n^{\log_b a}$. La complejidad global depende de la comparación asintótica entre $f(n)$ y $n^{\log_b a}$:

| Caso | Condición | Dominio | Solución Asintótica |
| :---: | :--- | :--- | :---: |
| **Caso 1** | $f(n) = O(n^{\log_b a - \varepsilon})$ para algún $\varepsilon > 0$ | Las **hojas dominan** el costo total | $T(n) = \mathbf{\Theta(n^{\log_b a})}$ |
| **Caso 2** | $f(n) = \Theta(n^{\log_b a} \log^k n)$ con $k \ge 0$ | Costo **balanceado** en cada nivel | $T(n) = \mathbf{\Theta(n^{\log_b a} \log^{k+1} n)}$ |
| **Caso 3** | $f(n) = \Omega(n^{\log_b a + \varepsilon})$ con $\varepsilon > 0$ y condición de regularidad | La **raíz domina** el costo total | $T(n) = \mathbf{\Theta(f(n))}$ |

---

## 2. Programa 1: Búsqueda en un Árbol Binario Completo (No Ordenado)

* 📄 **Código fuente:** [`busqueda_arbol_completo.c`](./busqueda_arbol_completo.c)

### 2.1 Descripción del Algoritmo y Estructura de Datos

Un **árbol binario completo** de $n$ nodos se almacena secuencialmente en un arreglo unidimensional (representación clásica de montículo o *heap*):
* Raíz en el índice $i = 0$.
* Para cualquier nodo en la posición $i$:
  * **Hijo izquierdo:** $\text{izq}(i) = 2i + 1$.
  * **Hijo derecho:** $\text{der}(i) = 2i + 2$.
  * **Padre:** $\lfloor (i - 1) / 2 \rfloor$.

Al ser un árbol completo, no existen posiciones vacías ni huecos en el rango de índices $[0, n-1]$. Esto garantiza que, dado un subárbol con raíz en $i$, los subárboles izquierdo y derecho contienen aproximadamente la mitad de los nodos restantes ($\approx n/2$), garantizando que el factor de reducción sea **$b = 2$**.

> [!IMPORTANT]
> **Propiedad clave:** El árbol **NO es un Árbol Binario de Búsqueda (ABB)**. Sus valores están distribuidos de forma arbitraria (no ordenada). Por lo tanto, no existe ninguna propiedad de orden que permita descartar ramas a priori: para determinar si un elemento existe en el árbol en el peor caso, es estrictamente necesario explorar **ambos subárboles**.

```
                50 (i=0)
              /    \
       (i=1) 30     70 (i=2)
           /  \    /  \
         10   40  60   20
      (i=3) (i=4)(i=5) (i=6)

Arreglo: [50, 30, 70, 10, 40, 60, 20]  (n = 7)
```

---

### 2.2 Componentes de Divide y Vencerás en `buscar()`

Analizando la función recursiva en C:

```c
int buscar(int arbol[], int n, int i, int objetivo) {
    /* 1. CASO BASE */
    if (i >= n)
        return -1;

    /* 2. TRABAJO LOCAL */
    if (arbol[i] == objetivo)
        return i;

    /* 3 y 4. DIVIDIR Y CONQUISTAR */
    int izq = buscar(arbol, n, 2 * i + 1, objetivo);
    if (izq != -1)
        return izq;

    int der = buscar(arbol, n, 2 * i + 2, objetivo);
    return der;
}
```

1. **Caso Base:**
   * Condición: `i >= n`.
   * Si el índice cae fuera de los límites del arreglo, significa que el subárbol actual está vacío (se descendió más allá de un nodo hoja). Retorna inmediatamente `-1` en tiempo constante $O(1)$.
2. **Trabajo Local:**
   * Comparación `arbol[i] == objetivo`.
   * Si el elemento en la raíz del subárbol actual coincide con el objetivo, se retorna su índice $i$. Este trabajo cuesta una sola comparación: $O(1)$.
3. **Dividir ($D(n)$):**
   * Se calculan los índices de las raíces de los dos subárboles: $2i + 1$ y $2i + 2$.
   * Cada subárbol abarca aproximadamente la mitad del subárbol actual ($n/2$). El cálculo aritmético toma $O(1)$.
4. **Conquistar:**
   * Se realizan dos llamadas recursivas: una hacia el subárbol izquierdo (`buscar(..., 2*i + 1, ...)`) y, si no se encuentra allí, otra hacia el subárbol derecho (`buscar(..., 2*i + 2, ...)`).
   * En el peor caso (cuando el elemento no existe o se ubica en la última hoja evaluada), se ejecutan **ambas llamadas recursivas** $\implies \mathbf{a = 2}$.
5. **Combinar ($C(n)$):**
   * Se evalúa si la búsqueda izquierda tuvo éxito (`izq != -1`). Si fue así, se propaga el índice hacia arriba; de lo contrario, se propaga el resultado de la derecha (`der`).
   * Esta decisión condicional toma tiempo constante $O(1)$.

---

### 2.3 Prueba de Escritorio

Consideremos el árbol de prueba con $n = 7$:
`arbol = [50, 30, 70, 10, 40, 60, 20]`

#### Traza A: Búsqueda de `objetivo = 60`
1. `buscar(arbol, 7, 0, 60)`:
   * $i = 0 < 7$. `arbol[0] = 50 != 60`.
   * Llama a hijo izquierdo: `buscar(arbol, 7, 1, 60)`.
2. `buscar(arbol, 7, 1, 60)`:
   * $i = 1 < 7$. `arbol[1] = 30 != 60`.
   * Llama a hijo izquierdo: `buscar(arbol, 7, 3, 60)`.
3. `buscar(arbol, 7, 3, 60)`:
   * $i = 3 < 7$. `arbol[3] = 10 != 60`.
   * Llama a hijo izquierdo: `buscar(arbol, 7, 7, 60)`. Como $7 \ge 7 \implies -1$.
   * Llama a hijo derecho: `buscar(arbol, 7, 8, 60)`. Como $8 \ge 7 \implies -1$.
   * Retorna `-1` a su padre ($i=1$).
4. Regresa a `i = 1`:
   * Como `izq == -1`, llama a hijo derecho: `buscar(arbol, 7, 4, 60)`.
5. `buscar(arbol, 7, 4, 60)`:
   * $i = 4 < 7$. `arbol[4] = 40 != 60`.
   * Hijos izquierdo y derecho ($i=9$ e $i=10$) caen fuera $\implies$ retorna `-1`.
6. Regresa a `i = 1`:
   * Ambas ramas fallaron $\implies$ retorna `-1` a la raíz ($i=0$).
7. Regresa a `i = 0`:
   * Como `izq == -1`, llama a hijo derecho: `buscar(arbol, 7, 2, 60)`.
8. `buscar(arbol, 7, 2, 60)`:
   * $i = 2 < 7$. `arbol[2] = 70 != 60`.
   * Llama a hijo izquierdo: `buscar(arbol, 7, 5, 60)`.
9. `buscar(arbol, 7, 5, 60)`:
   * $i = 5 < 7$. `arbol[5] = 60 == 60` $\implies$ **¡Encontrado! Retorna índice `5`**.
10. Se propaga `5` hacia arriba: `i=2` recibe `5` y retorna `5`; la raíz `i=0` recibe `5` y retorna `5`.
* **Resultado:** `Valor 60 encontrado en el indice 5`.

#### Traza B: Búsqueda de `objetivo = 99` (Peor caso: elemento no existe)
* Se visitan secuencialmente los nodos $i = 0, 1, 3, 4, 2, 5, 6$, además de los casos base fuera de rango ($i = 7, 8, 9, 10, 11, 12, 13, 14$).
* Se inspeccionaron absolutamente todos los $n = 7$ elementos del árbol.
* **Resultado:** `Valor 99 no esta en el arbol` (retorna `-1`).

---

### 2.4 Análisis de Complejidad con el Teorema Maestro

1. **Planteamiento de la Recurrencia:**
   En el peor caso (elemento no encontrado), la función realiza una comparación local $O(1)$ y llama recursivamente a ambos subárboles de tamaño aproximado $n/2$:
   $$T(n) = 2\,T\!\left(\frac{n}{2}\right) + \Theta(1)$$

2. **Extracción de Parámetros:**
   * $a = 2$ (dos llamadas recursivas: subárbol izquierdo y derecho).
   * $b = 2$ (cada subárbol reduce la cantidad de nodos a la mitad).
   * $f(n) = \Theta(1) = \Theta(n^0)$ (comparación en raíz y retorno de índices).

3. **Cálculo del Exponente Crítico:**
   $$c_{\text{crit}} = \log_b a = \log_2 2 = 1$$
   La función de trabajo en las hojas es:
   $$L(n) = n^{\log_b a} = n^1 = n$$

4. **Comparación con $f(n)$:**
   Comparamos $f(n) = \Theta(1)$ con $n^{\log_b a} = n^1$:
   $$f(n) = O(n^{1 - \varepsilon}) \quad \text{para } \varepsilon = 1 > 0$$

5. **Aplicación del Teorema:**
   Corresponde al **Caso 1 del Teorema Maestro**, donde el costo en las hojas domina asintóticamente a la raíz:
   $$T(n) = \Theta(n^{\log_b a}) = \mathbf{\Theta(n)}$$

---

### 2.5 Respuestas a las Preguntas de la Actividad

#### 1. ¿Cuál es la complejidad de buscar si el árbol no está ordenado?
* **Peor caso ($O(n)$ o $\Theta(n)$):** Ocurre cuando el elemento no está en el árbol o se ubica en la última hoja explorada. Al no existir una relación de orden entre padres e hijos, no es posible descartar ninguna de las dos ramas, por lo que el algoritmo debe recorrer exhaustivamente los $n$ nodos.
* **Mejor caso ($\Omega(1)$):** Ocurre cuando el elemento buscado se encuentra en la raíz ($i = 0$). Solo se realiza una comparación.
* **Caso promedio ($\Theta(n)$):** Asumiendo que el elemento puede estar en cualquiera de los $n$ nodos con igual probabilidad, en promedio se visitan $n/2$ nodos, manteniendo un comportamiento lineal $\Theta(n)$.

#### 2. ¿Cómo se podría reducir la complejidad de este algoritmo?
Existen tres alternativas fundamentales para optimizar esta búsqueda:

1. **Convertir el árbol en un Árbol Binario de Búsqueda (ABB/BST):**
   Si se impone la propiedad de búsqueda:
   $$\forall x \in \text{subárbol izquierdo}: x < \text{raíz} \quad \text{y} \quad \forall y \in \text{subárbol derecho}: y > \text{raíz}$$
   En cada nodo solo se realiza **una llamada recursiva** ($a = 1$), descartando la mitad del árbol restante ($b = 2$):
   $$T(n) = 1\,T\!\left(\frac{n}{2}\right) + \Theta(1) \implies \mathbf{\Theta(\log n)} \quad \text{(Caso 2 del Teorema Maestro)}$$
   Para garantizar este rendimiento en el peor caso frente a datos degenerados, se utilizan árboles auto-balanceables como **AVL** o **Red-Black**.

2. **Ordenar el arreglo subyacente y aplicar Búsqueda Binaria directa:**
   Dado que los datos están contiguos en memoria, si se ordenan previamente en tiempo $O(n \log n)$, cualquier búsqueda posterior se realiza en **$O(\log n)$** mediante comparaciones de índices `inicio`, `medio` y `fin`.

3. **Utilizar una Tabla Hash:**
   Si el espacio no es una limitación estricta, almacenar los elementos en una tabla hash permite resolver las búsquedas en tiempo promedio **$O(1)$** con un costo espacial de $O(n)$.

---

## 3. Programa 2: Par de Puntos más Cercanos en 2D (*Closest Pair of Points*)

* 📄 **Código fuente:** [`closest 1.c`](./closest%201.c)

### 3.1 Descripción del Algoritmo

Dado un conjunto de $n$ puntos en el plano euclidiano 2D, $P = \{(x_1, y_1), (x_2, y_2), \dots, (x_n, y_n)\}$, el objetivo es encontrar el par de puntos $(p, q)$ cuya distancia euclidiana sea mínima:
$$\text{dist}(p, q) = \sqrt{(p.x - q.x)^2 + (p.y - q.y)^2}$$

* **Enfoque ingenuo (Fuerza Bruta):** Comparar todos los posibles pares $\binom{n}{2} = \frac{n(n-1)}{2}$, con una complejidad temporal de **$O(n^2)$**.
* **Enfoque Divide y Vencerás:** Divide el plano verticalmente mediante una recta $x = x_{\text{corte}}$, resuelve recursivamente en ambas mitades y combina eficientemente las soluciones, logrando una complejidad de **$O(n \log n)$**.

---

### 3.2 Componentes de Divide y Vencerás en `rec()`

Analizando la función central:

```c
static double rec(Punto P[], int ini, int fin, Punto aux[]) {
    int n = fin - ini + 1;

    /* 1. CASO BASE */
    if (n <= 3) {
        // Fuerza bruta en O(1) y ordenamiento por Y con Insertion Sort O(1)
        ...
        return best;
    }

    /* 2. DIVIDIR */
    int med = (ini + fin) / 2;
    double x_corte = P[med].x;

    /* 3. CONQUISTAR */
    double dL = rec(P, ini, med, aux);
    double dR = rec(P, med + 1, fin, aux);
    double delta = dL < dR ? dL : dR;

    /* 4. COMBINAR */
    // 4a. Fusión (merge) por coordenada Y: O(n)
    // 4b. Filtrado de puntos en franja vertical |x - x_corte| < delta: O(n)
    // 4c. Comparación de vecinos con Delta_y < delta (máximo 7 vecinos): O(n)
    ...
    return delta;
}
```

1. **Caso Base:**
   * Cuando el número de puntos es pequeño ($n \le 3$), no tiene sentido seguir dividiendo. Se calculan las distancias entre todos los pares del subconjunto (a lo sumo 3 comparaciones) en tiempo constante $O(1)$.
   * Se ordena este pequeño tramo por la coordenada $Y$ mediante *Insertion Sort* ($O(1)$).
2. **Dividir ($D(n)$):**
   * Como el arreglo $P$ se preordenó inicialmente por coordenada $X$, se calcula la mediana como $P[\text{med}]$.
   * La recta vertical imaginaria $x = x_{\text{corte}}$ divide el conjunto en dos mitades balanceadas: izquierda ($P[\text{ini}..\text{med}]$) y derecha ($P[\text{med}+1..\text{fin}]$), cada una de tamaño $n/2$. Cálculo en $O(1)$.
3. **Conquistar:**
   * Se resuelven recursivamente las dos mitades:
     * $d_L = \text{rec}(P, \text{ini}, \text{med}, \text{aux})$
     * $d_R = \text{rec}(P, \text{med}+1, \text{fin}, \text{aux})$
   * Se define $\delta = \min(d_L, d_R)$, que representa la distancia mínima encontrada hasta ahora sin cruzar la frontera de corte.
   * Se realizan exactamente **$a = 2$** llamadas recursivas con subproblemas de tamaño **$n/2$** ($b = 2$).
4. **Combinar ($C(n)$):**
   Esta es la fase ingenieril más brillante del algoritmo. Un par más cercano con distancia $< \delta$ solo puede existir si un punto está a la izquierda de la recta y el otro a la derecha. Por tanto, ambos puntos deben ubicarse dentro de una **franja vertical de ancho $2\delta$** centrada en $x_{\text{corte}}$ ($|p.x - x_{\text{corte}}| < \delta$).

   La combinación se realiza en 3 pasos lineales:
   * **Paso 4a — Mezcla (Merge) por $Y$ ($O(n)$):** Aprovechando que las dos mitades ya regresan ordenadas por $Y$ de sus respectivas llamadas recursivas, se fusionan de forma idéntica a Merge Sort utilizando el buffer `aux`. Esto evita tener que ordenar con `qsort` en cada nivel de recursión.
   * **Paso 4b — Filtrado de la Franja ($O(n)$):** Se recorre el arreglo ya ordenado por $Y$ y se seleccionan únicamente aquellos puntos cuya distancia horizontal a $x_{\text{corte}}$ sea menor que $\delta$.
   * **Paso 4c — Comparación Acotada de Candidatos ($O(n)$):**
     > [!TIP]
     > **Lema de empaquetamiento geométrico:**
     > En una región rectangular de dimensiones $2\delta \times \delta$, es geométricamente imposible ubicar más de **8 puntos** (4 a la izquierda y 4 a la derecha) tales que todos los puntos del mismo lado tengan una distancia mutua de al menos $\delta$.
     
     Como los puntos de la franja están rigurosamente ordenados por $Y$, para cada punto `aux[p]` **solo es necesario compararlo con los siguientes puntos `aux[q]` que cumplan $(aux[q].y - aux[p].y) < \delta$**, lo cual ocurre a lo sumo **7 veces**. Por ende, el bucle doble anidado realiza como máximo $7m = O(n)$ operaciones.

---

### 3.3 Prueba de Escritorio

Consideremos los 6 puntos evaluados en `main()`:
$$P = \{(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)\}$$

#### Paso 1: Preprocesamiento (Ordenamiento por $X$)
Tras la llamada a `qsort(P, 6, sizeof(Punto), cmp_x)`:
* $P_0 = (2.0, 3.0)$
* $P_1 = (3.0, 4.0)$
* $P_2 = (5.0, 1.0)$
* $P_3 = (12.0, 10.0)$
* $P_4 = (12.0, 30.0)$
* $P_5 = (40.0, 50.0)$

#### Paso 2: Llamada Principal `rec(P, 0, 5, aux)`
* $n = 6 > 3 \implies$ no es caso base.
* Mediana: $\text{med} = (0 + 5) / 2 = 2$.
* Punto de corte: $P_2 = (5.0, 1.0) \implies x_{\text{corte}} = 5.0$.

#### Paso 3: Recursión Izquierda `rec(P, 0, 2, aux)`
* Tramo: $\{P_0(2, 3), P_1(3, 4), P_2(5, 1)\}$.
* Tamaño $n = 3 \le 3 \implies$ **Caso Base**:
  * $\text{dist}(P_0, P_1) = \sqrt{(3-2)^2 + (4-3)^2} = \sqrt{1 + 1} = \sqrt{2} \approx \mathbf{1.4142}$.
  * $\text{dist}(P_0, P_2) = \sqrt{(5-2)^2 + (1-3)^2} = \sqrt{9 + 4} = \sqrt{13} \approx 3.6055$.
  * $\text{dist}(P_1, P_2) = \sqrt{(5-3)^2 + (1-4)^2} = \sqrt{4 + 9} = \sqrt{13} \approx 3.6055$.
  * Mínimo de la izquierda: $d_L = \mathbf{1.4142}$.
  * Tramo ordenado por $Y$: $[(5, 1), (2, 3), (3, 4)]$. Retorna $1.4142$.

#### Paso 4: Recursión Derecha `rec(P, 3, 5, aux)`
* Tramo: $\{P_3(12, 10), P_4(12, 30), P_5(40, 50)\}$.
* Tamaño $n = 3 \le 3 \implies$ **Caso Base**:
  * $\text{dist}(P_3, P_4) = \sqrt{(12-12)^2 + (30-10)^2} = 20.0$.
  * $\text{dist}(P_3, P_5) = \sqrt{(40-12)^2 + (50-10)^2} = \sqrt{28^2 + 40^2} = \sqrt{784 + 1600} \approx 48.826$.
  * $\text{dist}(P_4, P_5) = \sqrt{(40-12)^2 + (50-30)^2} = \sqrt{28^2 + 20^2} = \sqrt{784 + 400} \approx 34.409$.
  * Mínimo de la derecha: $d_R = \mathbf{20.0}$.
  * Tramo ordenado por $Y$: $[(12, 10), (12, 30), (40, 50)]$. Retorna $20.0$.

#### Paso 5: Combinación en el Nivel Superior
* Distancia mínima entre mitades: $\delta = \min(1.4142, 20.0) = \mathbf{1.4142}$.
* Se fusionan ambas mitades ordenadas por $Y$:
  `P` ordenado por $Y$: $[(5, 1), (2, 3), (3, 4), (12, 10), (12, 30), (40, 50)]$.
* Filtrado de la franja vertical $|x - 5.0| < 1.4142 \implies x \in (3.5858, 6.4142)$:
  * $(5, 1) \implies |5.0 - 5.0| = 0 < 1.4142$ $\implies$ **entra**.
  * $(2, 3) \implies |2.0 - 5.0| = 3.0 \ge 1.4142$ $\implies$ no entra.
  * $(3, 4) \implies |3.0 - 5.0| = 2.0 \ge 1.4142$ $\implies$ no entra.
  * $(12, 10), (12, 30), (40, 50)$ $\implies$ no entran (diferencia en $x \ge 7$).
* La franja solo contiene $m = 1$ punto. Al no haber parejas en la franja, no hay distancias menores.
* Retorna $\delta = \mathbf{1.4142}$.

---

### 3.4 Análisis de Complejidad con el Teorema Maestro

1. **Recurrencia de la Función `rec()`:**
   En cada nivel se resuelven 2 subproblemas de tamaño $n/2$, y la combinación (merge en $Y$, franja y verificación de vecinos) toma tiempo lineal $O(n)$:
   $$T(n) = 2\,T\!\left(\frac{n}{2}\right) + \Theta(n)$$

2. **Parámetros del Teorema:**
   * $a = 2$ (dos llamadas recursivas: mitad izquierda y derecha).
   * $b = 2$ (cada mitad tiene $n/2$ puntos).
   * $f(n) = \Theta(n)$ (costo de la mezcla, filtrado y comparaciones en la franja).

3. **Exponente Crítico:**
   $$c_{\text{crit}} = \log_b a = \log_2 2 = 1$$
   La función de trabajo en las hojas es:
   $$L(n) = n^{\log_b a} = n^1 = n$$

4. **Comparación con $f(n)$:**
   Comparamos $f(n) = \Theta(n)$ con $n^{\log_b a} = n^1$:
   $$f(n) = \Theta(n^{\log_b a}) = \Theta(n^1) \quad \text{con } k = 0$$

5. **Aplicación del Teorema:**
   Corresponde exactamente al **Caso 2 del Teorema Maestro** ($k = 0$):
   $$T(n) = \Theta(n^{\log_b a} \log^{k+1} n) = \mathbf{\Theta(n \log n)}$$

6. **Complejidad Total de `par_mas_cercano()`:**
   * Ordenamiento inicial por $X$ (`qsort`): $\Theta(n \log n)$.
   * Asignación y liberación de memoria: $O(1)$.
   * Recursión `rec()`: $\Theta(n \log n)$.
   
   $$T_{\text{total}}(n) = \Theta(n \log n) + \Theta(n \log n) = \mathbf{\Theta(n \log n)}$$

7. **Complejidad Espacial:**
   * Buffer auxiliar `aux`: Requiere un arreglo de $n$ elementos tipo `Punto` $\implies \Theta(n)$.
   * Pila de recursión: Como la división es balanceada ($b = 2$), la altura del árbol de recursión es $\lceil \log_2 n \rceil \implies O(\log n)$.
   * Espacio auxiliar total: **$O(n)$**.

---

## 4. Cuadro Comparativo de Ambos Algoritmos

| Criterio | Programa 1: Búsqueda en Árbol Completo | Programa 2: Par de Puntos más Cercanos |
| :--- | :---: | :---: |
| **Entrada** | Árbol binario completo de $n$ enteros en arreglo | $n$ coordenadas euclidianas $(x, y)$ |
| **¿Datos ordenados?** | **No** (sin propiedad de búsqueda) | Sí (ordenados por $X$ inicialmente y por $Y$ en merge) |
| **Recurrencia** | $T(n) = 2T(n/2) + \Theta(1)$ | $T(n) = 2T(n/2) + \Theta(n)$ |
| **Parámetros $a, b$** | $a = 2, \; b = 2$ | $a = 2, \; b = 2$ |
| **Exponente crítico ($\log_b a$)** | $\log_2 2 = 1$ | $\log_2 2 = 1$ |
| **Costo local $f(n)$** | $\Theta(1)$ | $\Theta(n)$ |
| **Caso Teorema Maestro** | **Caso 1** ($f(n) \ll n^{\log_b a}$) | **Caso 2** ($f(n) = \Theta(n^{\log_b a})$) |
| **Complejidad Temporal** | **$\Theta(n)$** | **$\Theta(n \log n)$** |
| **Complejidad Espacial** | $O(\log n)$ (pila de recursión) | $O(n)$ (buffer auxiliar) $+ O(\log n)$ (pila) |
| **Comparativa vs Fuerza Bruta** | Idéntica a búsqueda secuencial ($O(n)$) | **Drástica reducción:** $O(n \log n)$ vs $O(n^2)$ |

---

## 5. Conclusiones

1. **El Teorema Maestro formaliza el equilibrio entre ramas y trabajo local:**
   * Cuando el trabajo local $f(n)$ es despreciable respecto a la proliferación de ramas (como en la búsqueda no ordenada, donde $f(n) = O(1)$ pero $a = 2$), el costo se concentra en las hojas, resultando en complejidad lineal $\Theta(n)$.
   * Cuando el trabajo local se mantiene lineal $f(n) = \Theta(n)$ igualando el ritmo de ramificación de las hojas ($a = b = 2$), cada nivel del árbol de recursión realiza la misma cantidad de trabajo ($\Theta(n)$), acumulando un factor $\log n$ para un total de $\Theta(n \log n)$.

2. **La importancia de la combinación eficiente en Divide y Vencerás:**
   En el problema de los puntos más cercanos, si en cada llamada recursiva se hubiera ordenado la franja con `qsort` ($O(n \log n)$), la recurrencia habría sido $T(n) = 2T(n/2) + O(n \log n)$, resultando en $O(n \log^2 n)$. La técnica de arrastrar el ordenamiento por $Y$ mediante una mezcla tipo *Merge Sort* reduce el paso de combinación a $O(n)$ estricto, alcanzando la cota óptima $O(n \log n)$.

3. **Sin orden previo no hay ventaja en dividir:**
   La búsqueda en un árbol binario completo sin ordenar demuestra una lección fundamental del diseño de algoritmos: **dividir un problema en subproblemas no garantiza una mejora asintótica si se deben explorar todas las subdivisiones**. La verdadera ganancia asintótica en búsqueda (como la búsqueda binaria o los árboles de búsqueda) surge de la capacidad de **podar** ramas gracias a un invariante de orden.

