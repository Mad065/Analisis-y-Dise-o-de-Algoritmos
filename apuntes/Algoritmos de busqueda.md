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
* **Complejidad Temporal:** $O(\log n)$.
* **Uso ideal:** Casos en los que el objetivo está cerca del principio del arreglo o en estructuras cuyo tamaño se desconoce.

### Implementación en Python

```python
def busqueda_exponencial(arreglo, objetivo):
    n = len(arreglo)
    # Si el elemento está en la primera posición
    if arreglo[0] == objetivo:
        return 0
        
    # Encontrar el rango para la búsqueda binaria
    i = 1
    while i < n and arreglo[i] <= objetivo:
        i *= 2
        
    # Realizar búsqueda binaria en el rango encontrado [i/2, min(i, n)]
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
* **Uso ideal:** Arreglos donde se conoce que la separación numérica entre los elementos es relativamente constante (por ejemplo, buscar un nombre en una guía telefónica).

> 💡 **Analogía:** Si vas a buscar el nombre "Zapata" en un directorio, no abres el libro a la mitad, sino que lo abres directamente hacia el final. La búsqueda por interpolación intenta hacer exactamente esta predicción matemática.

### Implementación en Python

```python
def busqueda_interpolacion(arreglo, objetivo):
    bajo = 0
    alto = len(arreglo) - 1
    
    while bajo <= alto and objetivo >= arreglo[bajo] and objetivo <= arreglo[alto]:
        # Si hay un solo elemento o son iguales
        if bajo == alto:
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

Aunque técnicamente es una estructura de datos, el Hashing nos brinda un algoritmo de búsqueda que desafía los límites del tiempo. Utiliza una **función hash** para convertir la clave de búsqueda en un índice directo de memoria.

* **Complejidad Temporal:** $O(1)$ en promedio. En el peor de los casos (muchas colisiones), puede degradarse a $O(n)$, pero con una buena función hash es casi instantáneo.
* **Uso ideal:** Bases de datos, diccionarios de Python (`dict`), memorias caché (Redis), donde la velocidad es crítica y el consumo de memoria extra no es un problema.

> 📝 **Nota:** En Python, los diccionarios (`dict`) y los conjuntos (`set`) están implementados internamente con tablas hash. Buscar si un elemento existe en un `set` o acceder a una llave en un `dict` es de complejidad $O(1)$.

---

## 7. Comparativa de Complejidad

A continuación se muestra un resumen comparando el rendimiento temporal y los requisitos de cada algoritmo de búsqueda visto:

| Algoritmo | Mejor Caso | Caso Promedio | Peor Caso | Requisito Previo |
| :--- | :---: | :---: | :---: | :--- |
| **Lineal** | $O(1)$ | $O(n)$ | $O(n)$ | Ninguno |
| **Salto (Jump)**| $O(1)$ | $O(\sqrt{n})$ | $O(\sqrt{n})$ | Arreglo ordenado |
| **Binaria** | $O(1)$ | $O(\log n)$ | $O(\log n)$ | Arreglo ordenado |
| **Exponencial**| $O(1)$ | $O(\log n)$ | $O(\log n)$ | Arreglo ordenado |
| **Interpolación**| $O(1)$ | $O(\log(\log n))$| $O(n)$ | Ordenado y uniforme |
| **Hash** | $O(1)$ | $O(1)$ | $O(n)$* | Memoria adicional |

*\* El peor caso en Hashing se da cuando todos los elementos colisionan en el mismo índice, lo cual es evitable con una buena distribución.*
