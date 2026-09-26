# Apuntes: Cálculo de Complejidad Algorítmica

El análisis de algoritmos es una parte fundamental de las Ciencias de la Computación. Nos permite predecir el comportamiento de un algoritmo cuando el tamaño de los datos de entrada (generalmente denotado como $n$) crece hacia el infinito.

Existen dos recursos principales que medimos al evaluar un algoritmo:
1. **Complejidad Temporal (Tiempo de Ejecución):** Cuánto tiempo tarda en completarse un algoritmo en función del tamaño de la entrada.
2. **Complejidad Espacial (Memoria):** Cuánta memoria adicional requiere el algoritmo para ejecutarse, sin contar el espacio que ocupan los datos de entrada en sí.

---

## 1. ¿Por qué medir la complejidad?

Medir la complejidad tiene implicaciones directas en el desarrollo de software:
* **Escalabilidad:** Un algoritmo ineficiente puede funcionar bien con $10$ elementos, pero colapsar un sistema con $1,000,000$ de elementos. El mejor hardware del mundo no puede compensar un mal algoritmo.
* **Independencia del entorno:** Permite comparar dos soluciones matemáticas de forma objetiva, sin importar si una se ejecuta en una supercomputadora y otra en un dispositivo antiguo.
* **Viabilidad:** Nos ayuda a saber si una solución es viable para producción y si cumplirá con los tiempos de respuesta requeridos antes de escribir el código final.

---

## 2. Notación Asintótica

Para expresar la complejidad de forma estandarizada y matemática, utilizamos la **Notación Asintótica**. Ignoramos factores dependientes del hardware (como la velocidad del procesador) y nos concentramos en la "tasa de crecimiento".

Las tres notaciones más utilizadas son:

* **Big O ($O$):** Representa el **límite superior** (el *peor caso*). Es la que más utilizamos porque nos garantiza que el algoritmo "no tardará más de X".
* **Omega ($\Omega$):** Representa el **límite inferior** (el *mejor caso*).
* **Theta ($\Theta$):** Representa un **límite ajustado** (cuando el mejor y el peor caso crecen a la misma tasa, el *caso promedio*).

---

## 3. Definición Formal de Big-O ($O$)

Matemáticamente, decimos que una función de tiempo $f(n)$ pertenece a $O(g(n))$ si existen dos constantes positivas $c$ y $n_0$ tales que:

$$f(n) \le c \cdot g(n) \quad \text{para todo} \quad n \ge n_0$$

**¿Qué significa esto en la práctica?**
Significa que, a partir de un cierto tamaño de entrada crítico ($n_0$), el tiempo de ejecución de nuestro algoritmo $f(n)$ nunca sobrepasará a la función $g(n)$ multiplicada por una constante $c$. Es decir, $g(n)$ actúa como un "techo" garantizado para el peor de los escenarios.

---

## 4. Reglas Prácticas para Calcular Big O

Calcular la complejidad $O()$ a partir de código requiere seguir ciertas reglas matemáticas para simplificar la expresión:

### Regla 1: Descartar las Constantes
El análisis asintótico ignora las constantes porque, para un $n$ muy grande, no cambian la forma general de la curva de crecimiento.
* $O(2n) \rightarrow O(n)$
* $O(500) \rightarrow O(1)$
* $O(\frac{n}{2}) \rightarrow O(n)$

### Regla 2: Descartar Términos No Dominantes
Si un algoritmo consta de varias partes, solo nos importa la parte que crece más rápido. El término dominante eclipsará a los demás cuando $n$ sea gigante.
* $O(n^2 + n + 1000) \rightarrow O(n^2)$
* $O(n + \log n) \rightarrow O(n)$
* $O(2^n + n^{100}) \rightarrow O(2^n)$

### Regla 3: Sumar Secuencias (Instrucciones Consecutivas)
Si tienes dos bloques de código ejecutándose uno tras otro, sus complejidades se suman.
```python
for i in range(n):  # Toma O(n)
    print(i)

for j in range(n):  # Toma O(n)
    print(j)

```

*Total:* $O(n) + O(n) = O(2n) \rightarrow O(n)$

### Regla 4: Multiplicar Ciclos Anidados

Si tienes ciclos dentro de otros ciclos, sus complejidades se multiplican.

```python
for i in range(n):        # Repite 'n' veces
    for j in range(n):    # Cada iteración toma 'n' veces
        print(i, j)

```

*Total:* $O(n) \times O(n) = O(n^2)$

---

## 5. Jerarquía de Crecimiento

Al analizar algoritmos, la jerarquía de crecimiento nos muestra cómo se comparan las clases de complejidad desde la más rápida y eficiente hasta la más lenta:

$$O(1) < O(\log n) < O(n) < O(n \log n) < O(n^2) < O(2^n) < O(n!)$$

---

## 6. Clases de Complejidad Comunes

Aquí presentamos los órdenes de complejidad ordenados desde el más eficiente hasta el menos eficiente:

| Notación | Nombre | Descripción | Ejemplo |
| --- | --- | --- | --- |
| **$O(1)$** | **Constante** | El tiempo no depende del tamaño de los datos. | Acceder a un elemento en un array o diccionario. |
| **$O(\log n)$** | **Logarítmica** | El tiempo crece muy lento. El problema se divide a la mitad en cada paso. | Búsqueda Binaria. |
| **$O(n)$** | **Lineal** | El tiempo crece proporcionalmente a la cantidad de datos. | Búsqueda Lineal, un ciclo `for`. |
| **$O(n \log n)$** | **Linealítmica** | Ligeramente peor que lineal. Común en buenos algoritmos de ordenamiento. | Merge Sort, Quick Sort, Tim Sort. |
| **$O(n^2)$** | **Cuadrática** | El tiempo crece exponencialmente rápido al doble. Ineficiente para grandes datos. | Bubble Sort, ciclos anidados dobles. |
| **$O(2^n)$** | **Exponencial** | El tiempo se duplica con cada elemento agregado. Muy ineficiente. | Fibonacci recursivo sin memoización. |
| **$O(n!)$** | **Factorial** | El peor de todos. Intenta todas las permutaciones posibles. | Problema del Agente Viajero (fuerza bruta). |

---

## 7. Ejemplos Prácticos en Python

### Ejemplo 1: Complejidad Constante $O(1)$

```python
def obtener_primer_elemento(arreglo):
    # No importa si el arreglo tiene 10 o 10 millones de elementos,
    # acceder al índice 0 siempre toma la misma cantidad de tiempo.
    return arreglo[0]

```

### Ejemplo 2: Complejidad Lineal $O(n)$

```python
def imprimir_elementos(arreglo):
    # Toma n pasos, uno por cada elemento del arreglo.
    for elemento in arreglo:
        print(elemento)

```

### Ejemplo 3: Complejidad Cuadrática $O(n^2)$

```python
def imprimir_pares(arreglo):
    # Por cada elemento, volvemos a recorrer todo el arreglo.
    # Si n = 10, esto imprimirá 100 veces.
    for i in arreglo:
        for j in arreglo:
            print(i, j)

```

> 💡 **Nota Importante:** Es crucial considerar también el tamaño de los argumentos. Si tienes un algoritmo con dos ciclos anidados iterando sobre dos arreglos **distintos** de tamaños $A$ y $B$, la complejidad es $O(A \times B)$, **no** $O(n^2)$.


---

## 8. Traducción de Código a Complejidad Matemática

Para calcular la complejidad de un código real, debes saber cómo "traducir" cada estructura de control a una expresión matemática. Aquí tienes una tabla rápida de traducción:

| Estructura de Código | Traducción Matemática | Complejidad Resultante |
| :--- | :--- | :--- |
| Operaciones básicas (+, -, *, /), asignaciones, `if`/`else`, `return` | $c$ (Constante) | **$O(1)$** |
| Bucle `for` o `while` lineal (ej. `i += 1`, `i -= 1`) | $\sum_{i=1}^{n} c$ | **$O(n)$** |
| Bucle donde el contador se divide o multiplica (ej. `i *= 2`, `i /= 2`) | $\sum_{i=1}^{\log_2 n} c$ | **$O(\log n)$** |
| Bucle donde el contador se eleva al cuadrado (ej. `i = i * i`, con $i \ge 2$) | $\sum_{k=1}^{\log_2(\log_2 n)} c$ | **$O(\log \log n)$** |
| Bucles anidados independientes | $O(n) \times O(n)$ | **$O(n^2)$** |
| Dos bucles secuenciales (uno después de otro) | $O(n) + O(n)$ | **$O(n)$** |
| Recursión simple dividiendo en mitades (ej. Búsqueda Binaria) | $T(n) = T(n/2) + O(1)$ | **$O(\log n)$** |
| Recursión dividiendo y procesando todo (ej. Merge Sort) | $T(n) = 2T(n/2) + O(n)$| **$O(n \log n)$** |
| Recursión múltiple (ej. Fibonacci ingenuo) | $T(n) = T(n-1) + T(n-2)$ | **$O(2^n)$** |

---

## 9. Casos Extraños (Edge Cases) y Trampas Comunes

A veces, el código engaña a simple vista. Estos son los casos "extraños" que suelen confundir al calcular la complejidad:

### 1. Bucles anidados dependientes (La Sumatoria de Gauss)
No todos los bucles anidados son $O(n \times m)$. Si el ciclo interno depende del externo, el cálculo cambia:
```python
for i in range(n):
    for j in range(i):  # j depende de i; llega hasta i, no hasta n
        print(i, j)
```
*Análisis:* El ciclo interno se ejecuta $1 + 2 + 3 + ... + (n-1)$ veces. Por la fórmula de Gauss, esto es $\frac{n(n-1)}{2} = \frac{n^2 - n}{2}$. Descartando constantes y términos no dominantes, la complejidad sigue siendo **$O(n^2)$**, pero el número de operaciones reales es exactamente la mitad que en un bucle anidado normal.

### 2. Concatenación de Strings (El peligro de la inmutabilidad)
```python
resultado = ""
for char in arreglo:
    resultado += char  # ¡Oculta un O(n) interno!
```
*Análisis:* En lenguajes como Python o Java, los strings son **inmutables**. La operación `+=` crea un string completamente nuevo copiando el anterior. Un bucle $O(n)$ que hace una copia de tamaño $O(n)$ resulta en una complejidad catastrófica de **$O(n^2)$**. *(Solución: usar `"".join()` en Python o `StringBuilder` en Java para que sea O(n)).*

### 3. Complejidad Amortizada (Arreglos Dinámicos)
```python
arreglo = []
for i in range(n):
    arreglo.append(i)
```
*Análisis:* La operación `append()` (o `add()` en Java) usualmente toma $O(1)$. Sin embargo, cuando la memoria subyacente del arreglo se llena, el sistema debe solicitar más memoria y copiar todo ($O(n)$). ¿Por qué decimos que todo el ciclo es **$O(n)$** y no $O(n^2)$? Porque ese costo pesado ocurre tan raramente (se duplica la capacidad) que, al "repartir" o *amortizar* el costo entre todas las inserciones, en promedio cada `append()` toma $O(1)$.

### 4. Bucles con múltiples punteros (Técnica "Two Pointers")
```python
left = 0
right = len(arr) - 1
while left < right:
    if arr[left] + arr[right] == target:
        break
    elif arr[left] + arr[right] < target:
        left += 1
    else:
        right -= 1
```
*Análisis:* Aunque parece que hay condiciones complejas, si observas los punteros `left` y `right`, solo se mueven hacia el centro. En conjunto, recorrerán el arreglo un máximo de una sola vez. Complejidad: **$O(n)$**.

### 5. Crecimiento Exponencial del Índice (`i = i * i`)
```python
i = 2
while i < n:
    i = i * i  # O también i = i ** 2
```
*Análisis:* Supongamos que $i$ empieza en $2$.
- Iteración 0: $i = 2 = 2^{2^0}$
- Iteración 1: $i = 2^2 = 4 = 2^{2^1}$
- Iteración 2: $i = 4^2 = 16 = 2^{2^2}$
- Iteración $k$: $i = 2^{2^k}$

El bucle termina cuando $i \ge n$, es decir $2^{2^k} \ge n$.
Aplicando logaritmo base 2 en ambos lados: $\log_2(2^{2^k}) \ge \log_2(n) \implies 2^k \ge \log_2(n)$.
Aplicando logaritmo nuevamente: $k \ge \log_2(\log_2 n)$.

Por lo tanto, la complejidad del ciclo es **$O(\log \log n)$** (doble logarítmica), que crece ridículamente lento (incluso para $n = 10^{80}$ —el número de átomos en el universo observable— solo toma unas 8 iteraciones).

---

## 10. Trucos de Oro para un Buen Cálculo

1. **Vigila los métodos nativos (Built-ins):** ¡No asumas que las funciones del lenguaje son $O(1)$!
   * `lista.pop(0)` o `lista.insert(0, x)` son **$O(n)$** porque deben desplazar todos los elementos restantes a la izquierda o derecha.
   * `x in lista` es **$O(n)$** (búsqueda secuencial), pero `x in set` o `x in dict` es **$O(1)$** (tabla hash).
   * `lista.sort()` es **$O(n \log n)$** (Timsort/Dual-Pivot Quicksort).
   * `sum(lista)` o `max(lista)` es **$O(n)$**.

2. **Diferencia bien tus variables de tamaño ($n$ vs $m$):**
   * Si iteras una matriz de filas $A$ y columnas $B$, la complejidad es **$O(A \cdot B)$**. ¡Nunca escribas $O(n^2)$ a menos que el problema especifique que es una matriz cuadrada ($n \times n$)!
   * Si buscas un patrón de longitud $p$ en un texto de longitud $t$, el análisis (por fuerza bruta) es **$O(p \cdot t)$**. Es importante darle un nombre distinto a cada variable de entrada independiente.

3. **Cuidado con las ramas en las recursiones:**
   * La fórmula rápida es $O(R^P)$ donde $R$ son las ramas por llamada y $P$ la profundidad del árbol.
   * Si un método recursivo se llama a sí mismo 2 veces por iteración (ej. Fibonacci ingenuo), $R=2$, profundidad $n$, entonces es **$O(2^n)$**. 

4. **El truco de la reducción rápida ($O(\log n)$):**
   Si notas que el espacio de búsqueda se reduce multiplicando o dividiendo por una fracción (se divide a la mitad, al tercio, se corta un trozo del 90%), inmediatamente debes pensar en un logaritmo **$O(\log n)$**.

5. **La regla del "Peor de los Casos" (con sentido común):**
   Si un algoritmo hace un paso inicial de ordenamiento y luego una búsqueda, evalúa ambas partes y quédate con el mayor. Por ejemplo: Ordenar $O(n \log n)$ + Búsqueda Binaria $O(\log n)$. La suma es $O(n \log n + \log n)$. Por la regla de descartar términos no dominantes, el algoritmo completo es **$O(n \log n)$**.