# Actividades: Prueba de Escritorio y Complejidad (Merge Sort)

* 📄 **Código fuente:** [`merge.c`](./merge.c)

---

## 1. Prueba de Escritorio

Este es el algoritmo de ordenamiento por mezcla (*merge*), donde se van agarrando bloques cada vez más grandes para ordenar los elementos de cada uno por separado y después juntarlos, obteniendo así la lista ordenada. Compara una mitad del bloque con la otra y así va ordenando la lista de menor a mayor. Para esto necesita `izq` que nos da el inicio de la primera mitad, `med` que nos da el inicio de la segunda mitad y `der` que nos da el final. Así compara los elementos del bloque de la izquierda con los de la derecha y los ordena. Después sigue con bloques más grandes hasta terminar.

Las líneas:
```c
if (med >= n - 1) continue;
if (der > n - 1) der = n - 1;
```
Son clave dado que estas ayudan a hacer que los arreglos no necesiten ser potencia de 2, y aseguran que solo se evalúe lo necesario, evitando bloques de mayor tamaño al del arreglo.

---

### Desarrollo de la Prueba de Escritorio

### Ciclo externo: `ancho = 1`

* **Ciclo interno: `izq = 0`**
  * Fusionando `A[0..0]` y `A[1..1]`
  * **Izq:** 0 | **Med:** 0 | **Der:** 1
  * **A:** `38, 27`
  * **temp:** `27, 38`
  * **A (después de fusionar):** `27, 38`

* **Ciclo interno: `izq = 2`**
  * Fusionando `A[2..2]` y `A[3..3]`
  * **Izq:** 2 | **Med:** 2 | **Der:** 3
  * **A:** `43, 3`
  * **temp:** `3, 43`
  * **A (después de fusionar):** `3, 43`

* **Ciclo interno: `izq = 4`**
  * Fusionando `A[4..4]` y `A[5..5]`
  * **Izq:** 4 | **Med:** 4 | **Der:** 5
  * **A:** `9, 82`
  * **temp:** `9, 82`
  * **A (después de fusionar):** `9, 82`

* **Ciclo interno: `izq = 6`**
  * *(Se omite la fusión por la condición del código `med >= n - 1`)*

### Ciclo externo: `ancho = 2`

* **Ciclo interno: `izq = 0`**
  * Fusionando `A[0..1]` y `A[2..3]`
  * **Izq:** 0 | **Med:** 1 | **Der:** 3
  * **A:** `27, 38, 3, 43`
  * **temp:** `3, 27, 38, 43`
  * **A (después de fusionar):** `3, 27, 38, 43`

* **Ciclo interno: `izq = 4`**
  * Fusionando `A[4..5]` y `A[6..6]`
  * **Izq:** 4 | **Med:** 5 | **Der:** 6
  * **A:** `9, 82, 10`
  * **temp:** `9, 10, 82`
  * **A (después de fusionar):** `9, 10, 82`

### Ciclo externo: `ancho = 4`

* **Ciclo interno: `izq = 0`**
  * Fusionando `A[0..3]` y `A[4..6]`
  * **Izq:** 0 | **Med:** 3 | **Der:** 6
  * **A:** `3, 27, 38, 43, 9, 10, 82`
  * **temp:** `3, 9, 10, 27, 38, 43, 82`
  * **A (después de fusionar):** `3, 9, 10, 27, 38, 43, 82`

**N:** 7
**Arreglo ordenado:** `3, 9, 10, 27, 38, 43, 82`

---

## 2. Cálculo de Complejidad (Propio)

En el cálculo de complejidad, la función `merge` tiene complejidad $O(n)$ dado que analiza todos los elementos del bloque dado, y la función `merge_sort_iterativo` es más interesante dado que en esta tenemos 2 `for` anidados que podrían ser simplemente $O(n^2)$, pero dado que los incrementos de la variable no son de 1 en 1 esto cambia, dado que el incremento es:

`ancho = 2 * ancho` donde `ancho` = $n$, entonces esto es $2^n$ y para que termine el ciclo se debe cumplir que $2^n \ge n$, entonces tenemos $n\sqrt{n}$.

En el segundo `for` tenemos algo similar:

`izq = izq + 2 * ancho` donde `izq` = $n$, entonces tenemos $n + 2n$. Como para detener el `for` necesitamos `izq > n`, entonces tenemos $2n \ge n$ obteniendo simplemente $n$. Tampoco deberíamos olvidar el hecho de que en este `for` se ejecuta el `merge`, pero como también es $n$, solo se suma y por reglas no cambia nada. Con eso ahora podemos decir que los `for` tienen complejidad $n\sqrt{n} \times n$.

---

## 3. Comparación con IA

### Prompt Proporcionado
> Por favor ayúdame con la siguiente actividad que me dejaron:
> Realiza la prueba de escritorio del programa adjunto; de igual forma, determina la complejidad de cada una de las funciones que lo componen. 
> Genera una respuesta propia, es válido que sea parcial, posteriormente compara tus resultados vs los generados por una IA.
> 
> Esta es mi respuesta y te adjunto el archivo con mis modificaciones para su análisis. Por favor, realiza la comparación entre mis resultados y lo que tú generes, siguiendo con la parte de comparación con IA en mi respuesta.
> Respuesta
> Prueba de escritorio
>
> Este es el algoritmo de ordenamiento por merge donde se van agarrando bloques cada vez mas grandes para ordenar los elemento de cada uno por separado y despues juntarlos asi obteniendo la lista ordenada, compara una mitad del bloque con la otra y y asi va ordenando la lista de menor a mayorpara esto necesita izq que nos da el inicio de la primera mitad med que nos da el inicio de la segunda mitad y der que nos da el final asi compara los elementos del bloque de la izquierda con los de la derceha y los ordena despues sigue con bloques mas grandes hasta terminar
>
> Las lineas
>
> if (med >= n - 1) continue;
> if (der > n - 1) der = n - 1;
>
> soin clave dado que estas ayudan a hacer que los arreglos no necesiten ser potencia de 2 y el otro hace que solo se evalue lo necesario evitando bloques de mayor tamaño al del arreglo
>
> Calculo de complejidad
>
> En el calculo de complejidad la funcion merge tiene complejidad n dado que analiza todos los elementos del bloque dado y la funcion merge_sort_iterativo es mas interesante dado que en esta tenemos 2 for anidados que podria ser simplemente n^2 pero dado que los incrementos de la variable no son de 1 en 1 esto cambia dado que el incremento es ancho = 2 * ancho donde ancho = n entonces esto es 2^n y para que termine el ciclo se debe cumplir que 2^n >= n entonces tenemos n√n en el segundo for tenemos algo similar izq = izq + 2 * ancho donde izq = n entonces tenemos n + 2n como para detener el for necesitamos izq > n entonces tenemos 2n >= n obteniendo simplemente n, tampoco deberiamos olvidar el >hecho de que en este for se ejecuta el merge pero como tambien es n solo se suma y por reglas no cambia nada y con eso ahora podemos decir que los for tienen complejidad n√n x n
>
> Comparacion con IA 



### Respuesta Generada por la IA

---

**Prueba de Escritorio (IA)**

La prueba de escritorio paso a paso con el arreglo inicial `A = {38, 27, 43, 3, 9, 82, 10}` de tamaño $n = 7$ se desarrolla de la siguiente manera:

**Estado inicial:** `[38, 27, 43, 3, 9, 82, 10]`

**Iteración 1 (ancho = 1):**
* **izq = 0:** `med = 0`, `der = 1`. Se fusionan `[38]` y `[27]`.
  * Resultado parcial: `[27, 38, 43, 3, 9, 82, 10]`
* **izq = 2:** `med = 2`, `der = 3`. Se fusionan `[43]` y `[3]`.
  * Resultado parcial: `[27, 38, 3, 43, 9, 82, 10]`
* **izq = 4:** `med = 4`, `der = 5`. Se fusionan `[9]` y `[82]`.
  * Resultado parcial: `[27, 38, 3, 43, 9, 82, 10]`
* **izq = 6:** `med = 6`. Se cumple `med >= n - 1` ($6 \ge 6$), por lo que se ejecuta `continue` y se omite la fusión.

**Iteración 2 (ancho = 2):**
* **izq = 0:** `med = 1`, `der = 3`. Se fusionan `[27, 38]` y `[3, 43]`.
  * Resultado parcial: `[3, 27, 38, 43, 9, 82, 10]`
* **izq = 4:** `med = 5`, `der = 7`. Se recorta `der` a 6 (`der > n - 1`). Se fusionan `[9, 82]` y `[10]`.
  * Resultado parcial: `[3, 27, 38, 43, 9, 10, 82]`

**Iteración 3 (ancho = 4):**
* **izq = 0:** `med = 3`, `der = 7`. Se recorta `der` a 6. Se fusionan `[3, 27, 38, 43]` y `[9, 10, 82]`.
  * Arreglo final: `[3, 9, 10, 27, 38, 43, 82]`

El ciclo externo se detiene porque el siguiente ancho (8) no es menor que $n$ (7).

---

**Análisis de Complejidad (IA)**

* **Función `merge`:** Su complejidad es $O(k)$, donde $k$ es el número de elementos a fusionar (`der - izq + 1`). En el peor de los casos, recorre todos los elementos del subarreglo una vez para ordenarlos y otra vez para copiarlos de vuelta al arreglo original.
* **Función `merge_sort_iterativo`:**
  * **Ciclo externo:** La variable `ancho` se multiplica por 2 en cada iteración (`ancho = 2 * ancho`). El número de pasos necesarios para que una variable que se duplica alcance el valor $n$ es logarítmico, específicamente $\log_2(n)$.
  * **Ciclo interno:** Aunque el salto de `izq` varía, en conjunto con la función `merge`, el ciclo interno procesa exactamente los $n$ elementos del arreglo en cada iteración del ciclo externo.
  * **Total:** Al multiplicar el trabajo del ciclo interno $O(n)$ por el número de iteraciones del ciclo externo $O(\log n)$, la complejidad temporal total es $O(n \log n)$.
* **Complejidad espacial:** Se requiere un arreglo auxiliar `tmp` del mismo tamaño que el original, por lo que la complejidad espacial es $O(n)$.

---

**Comparación con tus resultados**

Tienes una muy buena intuición sobre cómo funciona el algoritmo a nivel lógico. Detectaste perfectamente el propósito de las líneas `if (med >= n - 1) continue;` y `if (der > n - 1) der = n - 1;`, las cuales efectivamente evitan que el programa colapse al trabajar con arreglos cuyo tamaño no es potencia de 2. También acertaste en que la función `merge` tiene una complejidad lineal respecto al tamaño del bloque.

Donde hay un detalle matemático a ajustar es en el cálculo del ciclo externo. Mencionaste que el incremento `ancho = 2 * ancho` se traduce en $2^n$ y posteriormente en una raíz cuadrada $n\sqrt{n}$. En realidad, cuando una variable arranca en 1 y se multiplica por 2 repetidamente ($1, 2, 4, 8, 16 \dots$), el número de veces que puedes hacer esto antes de superar $n$ es el logaritmo base 2 de $n$ ($\log_2(n)$).

Por lo tanto, en lugar de que los `for` anidados den como resultado $n\sqrt{n} \times n$, el ciclo externo aporta $\log n$ y el trabajo combinado del ciclo interno más el `merge` aporta $n$. Esto nos da la complejidad matemática estándar de Merge Sort: $O(n \log n)$.

¿Te queda claro cómo la multiplicación sucesiva por 2 se transforma en un crecimiento logarítmico en lugar de uno exponencial o de raíz?

---

## 4. Conclusión

El análisis de complejidad del algoritmo *Merge Sort* iterativo demuestra cómo interactúan matemáticamente sus tres componentes principales: el ciclo externo, el ciclo interno y la función de fusión (`merge`).

### 1. Crecimiento Logarítmico del Ciclo Externo
Cuando una variable de control en un ciclo no se incrementa sumando una constante, sino multiplicándose repetidamente (`ancho = 2 * ancho`), la secuencia de valores generada ($1, 2, 4, 8, 16 \dots$) crece exponencialmente. Sin embargo, el **número de iteraciones** requeridas para que `ancho` alcance a $n$ es la función inversa: una escala **logarítmica**, denotada como $\log_2(n)$. Por lo tanto, el ciclo externo se ejecuta en $\Theta(\log_2 n)$ niveles o pasadas.

### 2. Cancelación Algebraica en el Ciclo Interno y `merge`
En cada pasada del ciclo externo se realiza el trabajo de fusión de subarreglos:
* **Número de iteraciones del ciclo interno:** El ciclo `for (izq = 0; izq < n; izq += 2 * ancho)` avanza en saltos de $2 \cdot \text{ancho}$, por lo que realiza $\frac{n}{2 \cdot \text{ancho}}$ iteraciones.
* **Costo de la función `merge`:** En cada iteración, la función de fusión procesa los elementos de dos bloques adyacentes de tamaño `ancho`, por lo que toma un tiempo lineal proporcional al tamaño combinado del bloque, es decir, $O(2 \cdot \text{ancho})$.

Al calcular el costo total de trabajo de cada nivel multiplicando el número de llamadas por el costo de la función `merge`:

$$\text{Trabajo por nivel} = \left( \frac{n}{2 \cdot \text{ancho}} \right) \times O(2 \cdot \text{ancho}) = O(n)$$

El factor $2 \cdot \text{ancho}$ presente en el denominador de las iteraciones se cancela algebraicamente con el $2 \cdot \text{ancho}$ del costo de la función `merge`. Esto demuestra que, sin importar el tamaño del bloque (`ancho = 1, 2, 4, \dots`), **el trabajo total acumulado en cada nivel de fusiones es siempre lineal, $O(n)$**.

### 3. Complejidad Global
Multiplicando los $\log_2(n)$ niveles del ciclo externo por el trabajo lineal $O(n)$ de cada pasada, obtenemos la complejidad temporal total del algoritmo:

$$\text{Complejidad Temporal Total} = O(n) \times \log_2(n) = O(n \log_2 n)$$

Este comportamiento es determinista y aplica para el peor, mejor y caso promedio ($\Theta(n \log n)$). Finalmente, el algoritmo requiere una **complejidad espacial de $O(n)$** debido a la asignación del arreglo auxiliar `tmp` indispensable para realizar la mezcla de elementos.