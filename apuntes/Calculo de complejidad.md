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