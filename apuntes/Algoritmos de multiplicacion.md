# Apuntes: Algoritmos de multiplicacion

La multiplicación de números es una de las operaciones más fundamentales en la computación. Aunque las computadoras modernas tienen hardware dedicado para multiplicar números pequeños rápidamente, cuando trabajamos con números muy grandes (por ejemplo, en criptografía, con cientos o miles de dígitos), el algoritmo que elijamos define si la operación tomará milisegundos o siglos.

---

## 1. El Enfoque Tradicional (Método Escolar)

El método que aprendemos en la escuela primaria consiste en multiplicar cada dígito del primer número por cada dígito del segundo, sumar los acarreos y al final sumar todas las filas. 

* **Complejidad:** Si ambos números tienen $n$ dígitos, este algoritmo requiere $n^2$ operaciones de multiplicación.
* **Notación Big-O:** Se clasifica como un algoritmo $O(n^2)$. Para números pequeños es excelente, pero si $n$ se duplica, el tiempo de ejecución se cuadruplica.

---

## 2. El Algoritmo de Karatsuba

Descubierto por Anatoly Karatsuba en 1960, este fue el primer algoritmo que demostró que la multiplicación podía realizarse en un tiempo menor a $O(n^2)$. 

Utiliza la estrategia de **"Divide y Vencerás"** (Divide and Conquer). La brillantez de Karatsuba radica en reducir la cantidad de sub-multiplicaciones necesarias de cuatro a solo tres.

### ¿Cómo funciona la reducción?

Supongamos que queremos multiplicar dos números $x$ e $y$ de $n$ dígitos. 
1. Dividimos ambos números a la mitad ($m = n/2$).
2. Expresamos $x$ e $y$ en términos de sus mitades superior e inferior:
   $$x = x_1 \cdot 10^m + x_0$$
   $$y = y_1 \cdot 10^m + y_0$$

La multiplicación tradicional requeriría calcular 4 productos parciales:
$$x \cdot y = (x_1 \cdot y_1) \cdot 10^{2m} + (x_1 \cdot y_0 + x_0 \cdot y_1) \cdot 10^m + (x_0 \cdot y_0)$$

Karatsuba optimizó el término medio $(x_1 \cdot y_0 + x_0 \cdot y_1)$ realizando solo **tres multiplicaciones** en total:

1. **Calcula:** $z_2 = x_1 \cdot y_1$
2. **Calcula:** $z_0 = x_0 \cdot y_0$
3. **Calcula:** $z_1 = (x_1 + x_0) \cdot (y_1 + y_0) - z_2 - z_0$

El resultado final se ensambla así:
$$Resultado = z_2 \cdot 10^{2m} + z_1 \cdot 10^m + z_0$$

---

## 3. Ejemplo Paso a Paso

Multipliquemos $1234 \times 5678$ usando Karatsuba.

* **Paso 1: Dividir los números ($m = 2$)**
  * $x = 1234 \rightarrow x_1 = 12, x_0 = 34$
  * $y = 5678 \rightarrow y_1 = 56, y_0 = 78$

* **Paso 2: Calcular $z_2$ y $z_0$**
  * $z_2 = 12 \times 56 = 672$
  * $z_0 = 34 \times 78 = 2652$

* **Paso 3: Calcular el término medio ($z_1$) usando la fórmula mágica**
  * $z_1 = (12 + 34) \times (56 + 78) - 672 - 2652$
  * $z_1 = (46 \times 134) - 672 - 2652$
  * $z_1 = 6164 - 672 - 2652 = 2840$

* **Paso 4: Ensamblar el resultado final**
  * $Resultado = 672 \cdot 10^4 + 2840 \cdot 10^2 + 2652$
  * $Resultado = 6720000 + 284000 + 2652 = \mathbf{7006652}$

*(Puedes comprobar en una calculadora que $1234 \times 5678 = 7006652$)*.

---

## 4. Comparativa de Complejidad

| Algoritmo | Complejidad Temporal | Notas |
| :--- | :--- | :--- |
| **Tradicional** | $O(n^2)$ | Mejor para números pequeños (menos de 100 dígitos). |
| **Karatsuba** | $O(n^{\log_2 3}) \approx O(n^{1.585})$ | Mucho más rápido para números grandes. Reduce significativamente las llamadas recursivas. |

> 💡 **Analogía:** Si incrementamos el tamaño de los números 10 veces, el método escolar tardará 100 veces más. Karatsuba tardará aproximadamente 38 veces más. A gran escala, esta diferencia es abismal.

---

## 5. Implementación en Python

Dado que Python maneja números enteros grandes de forma nativa, podemos implementar Karatsuba fácilmente con recursividad:

```python
def karatsuba(x, y):
    # Caso base: si los números son de 1 dígito, multiplicamos normal
    if x < 10 or y < 10:
        return x * y
    
    # Calculamos el tamaño del número para dividirlo a la mitad (m)
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    
    # Dividimos los números en mitades
    x1 = x // (10**m)
    x0 = x % (10**m)
    y1 = y // (10**m)
    y0 = y % (10**m)
    
    # Tres llamadas recursivas de Karatsuba
    z2 = karatsuba(x1, y1)
    z0 = karatsuba(x0, y0)
    z1 = karatsuba((x1 + x0), (y1 + y0)) - z2 - z0
    
    # Ensamblamos el resultado
    return z2 * (10**(2*m)) + z1 * (10**m) + z0

# Prueba rápida
print(karatsuba(1234, 5678))  # Salida: 7006652
```

> 📝 **Nota:** En la práctica, lenguajes como Python utilizan el algoritmo de Karatsuba internamente (o variantes más avanzadas como Toom-Cook o la Transformada Rápida de Fourier) cuando detectan que estás multiplicando enteros extremadamente grandes.