# Apuntes: Cálculo de Complejidad Algorítmica

El análisis de algoritmos es una parte fundamental de las Ciencias de la Computación. Nos permite predecir el comportamiento de un algoritmo cuando el tamaño de los datos de entrada (generalmente denotado como $n$) crece hacia el infinito.

Existen dos recursos principales que medimos al evaluar un algoritmo:
1. **Complejidad Temporal (Tiempo de Ejecución):** Cuánto tiempo tarda en completarse un algoritmo en función del tamaño de la entrada.
2. **Complejidad Espacial (Memoria):** Cuánta memoria adicional requiere el algoritmo para ejecutarse, sin contar el espacio que ocupan los datos de entrada en sí.

---

## 1. Notación Asintótica

Para expresar la complejidad de forma estandarizada y matemática, utilizamos la **Notación Asintótica**. Ignoramos factores dependientes del hardware (como la velocidad del procesador) y nos concentramos en la "tasa de crecimiento".

Las tres notaciones más utilizadas son:

* **Big O ($O$):** Representa el **límite superior** (el *peor caso*). Es la que más utilizamos porque nos garantiza que el algoritmo "no tardará más de X".
* **Omega ($\Omega$):** Representa el **límite inferior** (el *mejor caso*).
* **Theta ($\Theta$):** Representa un **límite ajustado** (cuando el mejor y el peor caso crecen a la misma tasa, el *caso promedio*).

---

## 2. Reglas Prácticas para Calcular Big O

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

## 3. Clases de Complejidad Comunes

Aquí presentamos los órdenes de complejidad ordenados desde el más eficiente hasta el menos eficiente:

| Notación | Nombre | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| **$O(1)$** | **Constante** | El tiempo no depende del tamaño de los datos. | Acceder a un elemento en un array o diccionario. |
| **$O(\log n)$**| **Logarítmica** | El tiempo crece muy lento. El problema se divide a la mitad en cada paso. | Búsqueda Binaria. |
| **$O(n)$** | **Lineal** | El tiempo crece proporcionalmente a la cantidad de datos. | Búsqueda Lineal, un ciclo `for`. |
| **$O(n \log n)$**| **Linealítmica**| Ligeramente peor que lineal. Común en buenos algoritmos de ordenamiento. | Merge Sort, Quick Sort, Tim Sort. |
| **$O(n^2)$** | **Cuadrática** | El tiempo crece exponencialmente rápido al doble. Ineficiente para grandes datos. | Bubble Sort, ciclos anidados dobles. |
| **$O(2^n)$** | **Exponencial** | El tiempo se duplica con cada elemento agregado. Muy ineficiente. | Fibonacci recursivo sin memoización. |
| **$O(n!)$** | **Factorial** | El peor de todos. Intenta todas las permutaciones posibles. | Problema del Agente Viajero (fuerza bruta). |

---

## 4. Ejemplos Prácticos en Python

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

