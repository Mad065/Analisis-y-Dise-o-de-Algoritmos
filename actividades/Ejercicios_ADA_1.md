# Actividades: Ejercicios ADA 1

## Ejercicio 1

```c++
int funcion(int n) {
    int x = 5;                    // Línea 1
    int y = x + 3;                // Línea 2
    int z = x * y;                // Línea 3
    int resultado = z - 10;       // Línea 4
    return resultado;             // Línea 5
}
```

**Operaciones por caso:** En la línea 1 hay una asignación (operaciones = 1); en la línea 2 hay una suma y una asignación (operaciones = 3); en la línea 3 hay una multiplicación y una asignación (operaciones = 5); en la línea 4 hay una resta y una asignación (operaciones = 7); y en la línea 5 hay un retorno, siendo un total de 8 operaciones.

**Operaciones por iteración:** No hay iteración.

**Complejidad:** Es constante dado que no cambia la cantidad de operaciones, $O(1)$.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> int funcion(int n) {
> int x = 5; // Línea 1
> int y = x + 3; // Línea 2
> int z = x * y; // Línea 3
> int resultado = z - 10; // Línea 4
> return resultado; // Línea 5
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: no hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:** en la línea 1 hay una asignación (operaciones = 1), en la línea 2 hay una suma y una asignación (operaciones = 3), en la línea 3 hay una multiplicación y una asignación (operaciones = 5), en la línea 4 hay una resta y una asignación (operaciones = 7) y en la línea 5 hay un retorno, siendo un total de 8 operaciones fijas sin importar el valor de `n`.

*Operaciones por iteración:* no hay iteración (no existen bucles ni estructuras repetitivas).

**Complejidad:** es constante dado que el número de operaciones no depende del parámetro de entrada `n`, por lo tanto es $O(1)$.

## Ejercicio 2

```c++
for (int i = 0; i < n; i += 2) {
    cout << i << endl;
}
```

**Operaciones por caso:** En el `for` tenemos una asignación, una comparación y una suma con asignación siendo 4 operaciones, pero de las cuales solo la asignación y comparación se hacen al inicio, siendo solo 2 operaciones.

**Operaciones por iteración:** En cada iteración hay una comparación, una suma y asignación, y una impresión, siendo 4 operaciones por iteración.

**Complejidad:** La complejidad es $O(n)$ debido al `for`, ya que las demás operaciones son constantes.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> for (int i = 0; i < n; i += 2) {
>    cout << i << endl;
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* En la inicialización `int i = 0` hay 1 asignación (operaciones = 1).
* En la condición `i < n` se realizan comparaciones: se evalúa $\lceil \frac{n}{2} \rceil$ veces como verdadera y 1 vez como falsa al salir (operaciones de comparación = $\lceil \frac{n}{2} \rceil + 1$).
* En la actualización `i += 2` hay una suma y una asignación en cada paso que entra al bucle, es decir, 2 operaciones realizadas $\lceil \frac{n}{2} \rceil$ veces (operaciones de incremento = $2 \lceil \frac{n}{2} \rceil$).
* En el cuerpo `cout << i << endl;` hay 1 operación de impresión por cada iteración válida (operaciones de salida = $\lceil \frac{n}{2} \rceil$).
* Siendo un total de: $1 + (\lceil \frac{n}{2} \rceil + 1) + 2 \lceil \frac{n}{2} \rceil + \lceil \frac{n}{2} \rceil = 4 \lceil \frac{n}{2} \rceil + 2$ operaciones (o aproximadamente $2n + 2$ operaciones para $n \ge 0$ par). Si $n \le 0$, el bucle no entra y solo se hace la asignación inicial y 1 comparación fallida (total = 2 operaciones).

*Operaciones por iteración:* en cada vuelta del ciclo se ejecutan 4 operaciones (1 comparación verdadera `i < n`, 1 operación de salida en `cout`, y 1 suma más 1 asignación en `i += 2`).

**Complejidad:** es lineal respecto al valor de $n$, ya que el número de operaciones crece de forma directamente proporcional a $n$ dividida entre 2, por lo tanto es $O(n)$.

## Ejercicio 3

```c++
for (int i = 0; i < n; i++) {
    for (int j = 0; j < 5; j++) {
        cout << i << " " << j << endl;
    }
}
```

**Operaciones por caso:** En el `for` externo hay una asignación y una comparación; en el interno otra asignación, otra comparación y dentro una impresión, dando 5 operaciones. Las sumas y asignación son en la iteración.

**Operaciones por iteración:** En la iteración, en el `for` externo son una comparación, una suma y una asignación, siendo $3n$ operaciones por iteración. En el `for` interno es lo mismo cambiando la comparación a que sea menor a 5, siendo 20 operaciones en total (ya contando la impresión dentro de este, siendo $5 \times 4$ operaciones).

**Complejidad:** La complejidad total sería de $3n \times 20 = 60n$, siendo solo $O(n)$ por reglas.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> for (int i = 0; i < n; i++) {
>    for (int j = 0; j < 5; j++) {
>        cout << i << " " << j << endl;
>    }
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* Bucle externo:
* Inicialización `int i = 0`: 1 asignación (operaciones = 1).
* Condición `i < n`: se evalúa $n$ veces como verdadera y 1 vez como falsa al terminar ($n + 1$ comparaciones).
* Incremento `i++`: 1 suma y 1 asignación ejecutadas $n$ veces ($2n$ operaciones).


* Bucle interno (se ejecuta completo por cada una de las $n$ iteraciones del bucle externo):
* Inicialización `int j = 0`: 1 asignación por cada iteración externa ($1 \times n = n$ operaciones).
* Condición `j < 5`: 5 evaluaciones verdaderas y 1 falsa por cada iteración externa ($6 \times n = 6n$ operaciones).
* Incremento `j++`: 1 suma y 1 asignación por iteración interna ($2 \times 5 \times n = 10n$ operaciones).
* Cuerpo `cout << i << " " << j << endl;`: 1 operación de salida por cada iteración interna ($5 \times n = 5n$ operaciones).


* Total general (para $n \ge 0$): $1 + (n + 1) + 2n + n + 6n + 10n + 5n = 25n + 2$ operaciones. Si $n \le 0$, el bucle externo no entra y solo se realiza la asignación inicial y 1 comparación falsa (total = 2 operaciones).

*Operaciones por iteración:*

* Por cada iteración del bucle interno: 4 operaciones (1 comparación verdadera `j < 5`, 1 operación de impresión y 2 operaciones por el incremento `j++`).
* Por cada iteración del bucle externo: 24 operaciones (1 comparación verdadera `i < n`, 2 operaciones de incremento `i++`, y todo el ciclo interno que suma 21 operaciones entre su inicialización, 6 comparaciones, 5 salidas y 10 operaciones de incremento de `j`).

**Complejidad:** es lineal respecto a $n$, ya que el bucle interno tiene un límite constante fijo (5 iteraciones) y no depende de $n$, por lo tanto es $O(n)$.

## Ejercicio 4

```c++
// Bucle 1
for (int i = 0; i < n; i++) {
    cout << i << endl;
}
// Bucle 2
for (int j = 0; j < n; j++) {
    cout << j << endl;
}
// Bucle 3
for (int k = 0; k < n; k++) {
    cout << k << endl;
}
```

**Operaciones por caso:** En el bucle 1 está su asignación y comparación seguido de la impresión; en el bloque 2 y 3 lo mismo, siendo cada uno de 3 operaciones.

**Operaciones por iteración:** Cada bucle tiene en su condición que la variable sea menor a $n$, teniendo como operaciones la comparación, la suma y asignación, y la impresión, siendo 4 operaciones por iteración de cada `for`.

**Complejidad:** La cantidad de operaciones solo cambia por $n$ en cada `for`, y dado que están separados solo se suman, siendo $n + n + n = 3n$, siendo por reglas simplemente $O(n)$. 

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> // Bucle 1
> for (int i = 0; i < n; i++) {
>     cout << i << endl;
> }
> // Bucle 2
> for (int j = 0; j < n; j++) {
>     cout << j << endl;
> }
> // Bucle 3
> for (int k = 0; k < n; k++) {
>     cout << k << endl;
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* En el bucle 1: inicialización `int i = 0` (1 asignación), condición `i < n` ($n$ verdaderas + 1 falsa = $n + 1$ comparaciones), incremento `i++` (1 suma y 1 asignación ejecutadas $n$ veces = $2n$ operaciones) y cuerpo `cout << i << endl;` ($n$ operaciones de salida), sumando un subtotal de $4n + 2$ operaciones.
* En el bucle 2: inicialización `int j = 0` (1 asignación), condición `j < n` ($n + 1$ comparaciones), incremento `j++` ($2n$ operaciones) y cuerpo `cout << j << endl;` ($n$ operaciones de salida), sumando un subtotal de $4n + 2$ operaciones.
* En el bucle 3: inicialización `int k = 0` (1 asignación), condición `k < n` ($n + 1$ comparaciones), incremento `k++` ($2n$ operaciones) y cuerpo `cout << k << endl;` ($n$ operaciones de salida), sumando un subtotal de $4n + 2$ operaciones.
* Siendo un total general (para $n \ge 0$) de: $(4n + 2) + (4n + 2) + (4n + 2) = 12n + 6$ operaciones. Si $n \le 0$, cada bucle solo ejecuta su asignación y una comparación fallida, sumando un total de 6 operaciones.

*Operaciones por iteración:* en cada vuelta de cualquiera de los tres bucles se realizan 4 operaciones (1 comparación verdadera de la condición, 1 operación de impresión en el cuerpo y 2 operaciones por el incremento de la variable de control).

**Complejidad:** es lineal respecto a $n$, ya que los tres bucles se ejecutan de manera consecutiva (sumando sus complejidades individuales $O(n) + O(n) + O(n) = O(3n)$) y al descartar constantes el crecimiento es directamente proporcional a la entrada, por lo tanto es $O(n)$.

## Ejercicio 5

```c++
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        for (int k = 0; k < n; k++) {
            cout << i << " " << j << " " << k << endl;
        }
    }
}
```

**Operaciones por caso:** Cada `for` tiene su asignación y comparación, y en el tercer `for` está la impresión, siendo 7 operaciones sin iteración.

**Operaciones por iteración:** En los 2 primeros `for` son 3 operaciones por iteración y en el tercero son 4, siendo $3n$, $3n$ y $4n$.

**Complejidad:** Dado que están anidados se multiplican, siendo $(3n+1)(3n+1)(4n+2)$ dando $O(n^3)$.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> for (int i = 0; i < n; i++) {
>     for (int j = 0; j < n; j++) {
>         for (int k = 0; k < n; k++) {
>             cout << i << " " << j << " " << k << endl;
>         }
>     }
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* Bucle externo `i`: 1 asignación inicial `int i = 0` (operaciones = 1), $n + 1$ comparaciones en `i < n` ($n$ verdaderas y 1 falsa), y $n$ incrementos `i++` con 1 suma y 1 asignación ($2n$ operaciones). Subtotal externo: $3n + 2$ operaciones.
* Bucle intermedio `j` (se repite $n$ veces): 1 asignación inicial por entrada `int j = 0` ($1 \times n = n$ operaciones), $n + 1$ comparaciones por entrada `j < n` ($(n + 1)n = n^2 + n$ comparaciones), y $n$ incrementos `j++` por entrada con 1 suma y 1 asignación ($2n \times n = 2n^2$ operaciones). Subtotal intermedio: $3n^2 + 2n$ operaciones.
* Bucle interno `k` (se repite $n^2$ veces): 1 asignación inicial por entrada `int k = 0` ($1 \times n^2 = n^2$ operaciones), $n + 1$ comparaciones por entrada `k < n` ($(n + 1)n^2 = n^3 + n^2$ comparaciones), $n$ incrementos `k++` por entrada con 1 suma y 1 asignación ($2n \times n^2 = 2n^3$ operaciones), y 1 operación de impresión en el cuerpo ejecutada $n^3$ veces ($n^3$ operaciones). Subtotal interno: $4n^3 + 2n^2$ operaciones.
* Siendo un total general (para $n \ge 0$) de: $(3n + 2) + (3n^2 + 2n) + (4n^3 + 2n^2) = 4n^3 + 5n^2 + 5n + 2$ operaciones. Si $n \le 0$, el bucle exterior no entra y solo realiza la inicialización y una comparación fallida (total = 2 operaciones).

*Operaciones por iteración:*

* Por cada iteración del bucle interno `k`: se ejecutan 4 operaciones (1 comparación verdadera `k < n`, 1 operación de impresión y 2 operaciones por el incremento `k++`).
* Por cada iteración del bucle intermedio `j`: se ejecutan $4n + 4$ operaciones (1 comparación verdadera `j < n`, 2 operaciones por el incremento `j++`, más la inicialización, comparaciones, incrementos e impresiones del bucle `k`).
* Por cada iteración del bucle externo `i`: se ejecutan $4n^2 + 5n + 4$ operaciones (1 comparación verdadera `i < n`, 2 operaciones por el incremento `i++`, más todo el bloque anidado de los bucles `j` y `k`).

**Complejidad:** es cúbica respecto al tamaño de entrada $n$, ya que son tres bucles anidados dependientes de $n$ que multiplican sus pasos ($n \times n \times n$), por lo tanto es $O(n^3)$.

## Ejercicio 6

```c++
int** matriz = new int*[n];
for (int i = 0; i < n; i++) {
    matriz[i] = new int[n];
}
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        matriz[i][j] = i + j;
    }
}
```

**Operaciones por caso:** Empieza con una reserva de memoria y una asignación (operaciones = 2), seguida de un `for` con una asignación y una comparación, y dentro otra reserva de memoria y asignación (operaciones = 6). En el segundo `for` tiene su asignación, su comparación, y dentro otro `for` con su asignación y comparación (operaciones = 10). Por último, dentro del `for` anidado hay una suma y asignación, siendo un total de 12 operaciones sin iteración.

**Operaciones por iteración:** Con iteración, el primer `for` son 5 operaciones por comparación, suma y asignación, y reserva, indexación y asignación. En el segundo `for`, al ser anidados, quedan 3 del externo y 5 del interno.

**Complejidad:** La complejidad sería $2 + 5n + (3n \times 5n) = 2 + 5n + 15n^2$ y por reglas se vuelve $O(n^2)$.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> int** matriz = new int*[n];
> for (int i = 0; i < n; i++) {
>     matriz[i] = new int[n];
> }
> for (int i = 0; i < n; i++) {
>     for (int j = 0; j < n; j++) {
>         matriz[i][j] = i + j;
>     }
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* En la asignación de memoria principal `int** matriz = new int*[n];`: hay 1 reserva de memoria y 1 asignación (operaciones = 2).
* En el primer bucle (reserva de filas):
* Inicialización `int i = 0`: 1 asignación (operaciones = 1).
* Condición `i < n`: $n$ evaluaciones verdaderas y 1 falsa ($n + 1$ comparaciones).
* Incremento `i++`: 1 suma y 1 asignación ejecutadas $n$ veces ($2n$ operaciones).
* Cuerpo `matriz[i] = new int[n];`: 1 reserva de memoria, 1 indexación y 1 asignación por iteración ($3n$ operaciones).
* Subtotal primer bucle: $1 + (n + 1) + 2n + 3n = 6n + 2$ operaciones.


* En el segundo bloque (bucles anidados para asignación de valores):
* Bucle exterior `i`: 1 asignación inicial `int i = 0` (operaciones = 1), $n + 1$ comparaciones en `i < n` ($n$ verdaderas y 1 falsa), y $n$ incrementos `i++` con 1 suma y 1 asignación ($2n$ operaciones). Subtotal: $3n + 2$ operaciones.
* Bucle interior `j` (se repite $n$ veces): 1 asignación inicial por entrada `int j = 0` ($1 \times n = n$ operaciones), $n + 1$ comparaciones por entrada `j < n` ($(n + 1)n = n^2 + n$ comparaciones), y $n$ incrementos `j++` por entrada con 1 suma y 1 asignación ($2n \times n = 2n^2$ operaciones). Subtotal: $3n^2 + 2n$ operaciones.
* Cuerpo `matriz[i][j] = i + j;` (se ejecuta $n^2$ veces): 1 suma (`i + j`), 2 indexaciones de puntero (`[i]` y `[j]`) y 1 asignación, sumando 4 operaciones por ejecución ($4 \times n^2 = 4n^2$ operaciones).
* Subtotal segundo bloque: $(3n + 2) + (3n^2 + 2n) + 4n^2 = 7n^2 + 5n + 2$ operaciones.


* Siendo un total general (para $n \ge 0$) de: $2 + (6n + 2) + (7n^2 + 5n + 2) = 7n^2 + 11n + 6$ operaciones. Si $n \le 0$, no entran los bucles y solo se ejecutan las asignaciones/reservas iniciales y las comparaciones fallidas (total = 6 operaciones).

*Operaciones por iteración:*

* En el primer bucle: se ejecutan 6 operaciones por iteración (1 comparación verdadera `i < n`, 2 operaciones de incremento `i++`, y 3 operaciones en el cuerpo por indexación, reserva y asignación).
* En el segundo bloque:
* Por cada iteración del bucle interno `j`: se ejecutan 7 operaciones (1 comparación verdadera `j < n`, 2 operaciones de incremento `j++`, y 4 operaciones en la asignación con suma e indexación doble).
* Por cada iteración del bucle externo `i`: se ejecutan $7n + 4$ operaciones (1 comparación verdadera `i < n`, 2 operaciones de incremento `i++`, más todo el ciclo interno de `j` con su inicialización, comparaciones, incrementos y cuerpo).



**Complejidad:** es cuadrática respecto al valor de $n$, ya que el término dominante corresponde al doble bucle anidado que llena la matriz de tamaño $n \times n$, por lo tanto es $O(n^2)$.

## Ejercicio 7

```c++
for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
        cout << i << " " << j << endl;
    }
}
```

**Operaciones por caso:** El `for` externo tiene asignación y comparación (operaciones = 2); el `for` interno igual (operaciones = 4), y dentro el `print`, siendo un total de 5 operaciones sin iteración.

**Operaciones por iteración:** Con iteración tenemos 3 operaciones en el `for` externo y en el interno 4.

**Complejidad:** La complejidad sería $(2 + 3n)(3 + 4m) = 6 + 9n + 8m + 12nm$, y por reglas tendríamos solo $O(nm)$.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> for (int i = 0; i < n; i++) {
>     for (int j = 0; j < m; j++) {
>         cout << i << " " << j << endl;
>     }
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* Bucle externo `i`: 1 asignación inicial `int i = 0` (operaciones = 1), $n + 1$ comparaciones en `i < n` ($n$ verdaderas y 1 falsa), y $n$ incrementos `i++` con 1 suma y 1 asignación ($2n$ operaciones). Subtotal externo: $3n + 2$ operaciones.
* Bucle interno `j` (se repite completo $n$ veces): 1 asignación inicial por entrada `int j = 0` ($1 \times n = n$ operaciones), $m + 1$ comparaciones por entrada `j < m` ($(m + 1)n = nm + n$ comparaciones), y $m$ incrementos `j++` por entrada con 1 suma y 1 asignación ($2m \times n = 2nm$ operaciones). Subtotal bucle interno: $3nm + 2n$ operaciones.
* Cuerpo del bucle `cout << i << " " << j << endl;`: se ejecuta $n \times m$ veces con 1 operación de impresión por ejecución ($nm$ operaciones).
* Siendo un total general (para $n, m \ge 0$) de: $(3n + 2) + (3nm + 2n) + nm = 4nm + 5n + 2$ operaciones. Si $n \le 0$, el bucle exterior no entra y solo se realiza la asignación inicial y 1 comparación fallida (total = 2 operaciones).

*Operaciones por iteración:*

* Por cada iteración del bucle interno `j`: se ejecutan 4 operaciones (1 comparación verdadera `j < m`, 1 operación de salida en `cout`, y 2 operaciones por el incremento `j++`).
* Por cada iteración del bucle externo `i`: se ejecutan $4m + 4$ operaciones (1 comparación verdadera `i < n`, 2 operaciones de incremento `i++`, más la inicialización de `j = 0`, las $m+1$ comparaciones de `j`, las $m$ impresiones y los $m$ incrementos de `j`).

**Complejidad:** depende de dos variables de entrada independientes ($n$ y $m$), ya que el bucle exterior corre $n$ veces y el bucle interior corre $m$ veces por cada vuelta, por lo tanto es $O(n \times m)$.

## Ejercicio 8

```c++
int arr[n];
int target;

for (int i = 0; i < n; i++) {
    //
    for (int j = 0; j < n; j++) {
        if (arr[j] == target) {
            break;
        }
    }
}
```

**Operaciones por caso:** En las declaraciones tenemos dos reservas de memoria (operaciones = 2). En el `for` externo tenemos una asignación y una comparación; en el interno tenemos también una asignación y comparación (operaciones = 6), y dentro de este tenemos un `if` con una comparación y si es verdadero otra operación `break`, siendo siempre 7 operaciones y 8 si el `if` es verdadero.

**Operaciones por iteración:** En las iteraciones, en el `for` externo tenemos 3 operaciones iterativas y en el interno 4.

**Complejidad:** La complejidad sería $2 + 3n \times 4n = 2 + 12n^2$, que por reglas se vuelve $O(n^2)$.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> int arr[n];
> int target;
>
> for (int i = 0; i < n; i++) {
>     //
>     for (int j = 0; j < n; j++) {
>         if (arr[j] == target) {
>             break;
>         }
>     }
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* En las declaraciones iniciales: `int arr[n];` y `int target;` representan reservas de espacio en memoria sin asignación explícita (operaciones = 0 directas de cómputo).
* En el bucle externo `i`: 1 asignación inicial `int i = 0` (operaciones = 1), $n + 1$ comparaciones en `i < n` ($n$ verdaderas y 1 falsa), y $n$ incrementos `i++` con 1 suma y 1 asignación ($2n$ operaciones). Subtotal externo fijo: $3n + 2$ operaciones.
* Para el bucle interno `j` (depende del contenido de `arr` y la posición de `target`):
* **Mejor caso** (`target` está en la primera posición `arr[0]`): en cada una de las $n$ iteraciones externas, `j` se inicializa (1 asignación), evalúa `j < n` (1 comparación verdadera), indexa y compara `arr[j] == target` (2 operaciones) y ejecuta `break;` (1 salto de control). Por tanto, el bucle interno hace $(1 + 1 + 2 + 1) \times n = 5n$ operaciones. Total mejor caso: $(3n + 2) + 5n = 8n + 2$ operaciones.
* **Peor caso** (`target` no está en el arreglo): el bucle interno corre completo las $n$ veces. Por cada vuelta externa hay: 1 inicialización `j = 0` ($n$ operaciones), $n + 1$ comparaciones `j < n` ($n^2 + n$ operaciones), $n$ incrementos `j++` ($2n^2$ operaciones), y $n$ evaluaciones de `arr[j] == target` con 1 indexación y 1 comparación ($2n^2$ operaciones). Total bucle interno peor caso: $5n^2 + 2n$ operaciones. Total peor caso: $(3n + 2) + (5n^2 + 2n) = 5n^2 + 5n + 2$ operaciones.



*Operaciones por iteración:*

* Por cada iteración del bucle interno `j`: se ejecutan 5 operaciones (1 comparación verdadera `j < n`, 2 operaciones en el `if` por indexar y comparar `arr[j] == target`, y 2 operaciones por el incremento `j++` si no se cumple la condición).
* Por cada iteración del bucle externo `i`: en el mejor caso realiza 8 operaciones (1 comparación `i < n`, 2 por `i++`, y 5 del bucle interno al romper en la primera vuelta); en el peor caso realiza $5n + 5$ operaciones (1 comparación `i < n`, 2 por `i++`, más la inicialización, comparaciones, incrementos y evaluaciones completas del ciclo de `j`).

**Complejidad:** en el mejor caso es lineal $\Omega(n)$ ya que el `break` se activa en la primera iteración de `j`; sin embargo, en el peor caso (y caso promedio) el ciclo interno recorre todo el arreglo sin encontrar el elemento, por lo tanto su cota superior es cuadrática $O(n^2)$.

## Ejercicio 9

```c++
int i = n;
while (i > 1) {
    cout << i << endl;
    i = i / 2;
}
```

**Operaciones por caso:** Inicia con una asignación y en el `while` una comparación, y dentro una impresión y una división y asignación, siendo 5 operaciones.

**Operaciones por iteración:** Por iteraciones serían 4 operaciones (comparación, impresión, división y asignación) dentro del `while`.

**Complejidad:** Su complejidad sería de $1 + 4k$. Al dividir constantemente $n$ entre 2, esto se vuelve $O(\log_2(n))$.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> int i = n;
> while (i > 1) {
>    cout << i << endl;
>     i = i / 2;
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* En la inicialización `int i = n;` hay 1 asignación (operaciones = 1).
* En el bucle `while (i > 1)` la variable $i$ se divide a la mitad en cada paso, por lo que el ciclo se ejecuta $k = \lfloor \log_2(n) \rfloor$ veces (para $n \ge 1$).
* En la condición `i > 1` se realizan $\lfloor \log_2(n) \rfloor$ comparaciones verdaderas y 1 falsa que rompe el ciclo (operaciones = $\lfloor \log_2(n) \rfloor + 1$).
* En el cuerpo `cout << i << endl;` hay 1 operación de salida ejecutada $\lfloor \log_2(n) \rfloor$ veces (operaciones = $\lfloor \log_2(n) \rfloor$).
* En la actualización `i = i / 2;` hay 1 división y 1 asignación ejecutadas $\lfloor \log_2(n) \rfloor$ veces (operaciones = $2 \lfloor \log_2(n) \rfloor$).


* Siendo un total general (para $n > 1$) de: $1 + (\lfloor \log_2(n) \rfloor + 1) + \lfloor \log_2(n) \rfloor + 2 \lfloor \log_2(n) \rfloor = 4 \lfloor \log_2(n) \rfloor + 2$ operaciones. Si $n \le 1$, el bucle no entra y solo se realiza la asignación inicial y 1 comparación fallida (total = 2 operaciones).

*Operaciones por iteración:* en cada vuelta del ciclo se realizan 4 operaciones (1 comparación verdadera `i > 1`, 1 operación de impresión en `cout`, y 1 división más 1 asignación en `i = i / 2`).

**Complejidad:** es logarítmica respecto a $n$, ya que en cada paso el valor de $i$ se divide entre 2, reduciendo el espacio del problema a la mitad de forma sucesiva, por lo tanto es $O(\log n)$.

## Ejercicio 10

```c++
for (int i = 0; i < n; i++) {
    int j = 1;
    while (j < n) {
        cout << i << " " << j << endl;
        j = j * 2;
    }
}
```

**Operaciones por caso:** En el `for` tenemos una asignación y comparación (operaciones = 2); después, dentro tenemos otra asignación y un `while` con una comparación (operaciones = 4). Dentro del `while` tenemos una impresión, una multiplicación y una asignación, siendo 7 operaciones.

**Operaciones por iteración:** En el `for` tenemos 4 operaciones iterativas contando la comparación, suma, asignación y la asignación interior. En el `while` tenemos también 4 operaciones iterativas.

**Complejidad:** Al ser el `for` y `while` anidados, se multiplican sus complejidades siendo $4n \times 4(\log_2(n))$. El logaritmo base dos es porque `j` aumenta multiplicándose por 2; por reglas se vuelve $O(n \log_2(n))$.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> for (int i = 0; i < n; i++) {
>     int j = 1;
>     while (j < n) {
>         cout << i << " " << j << endl;
>         j = j * 2;
>     }
> }
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* En el bucle externo `i`:
* Inicialización `int i = 0`: 1 asignación (operaciones = 1).
* Condición `i < n`: $n$ evaluaciones verdaderas y 1 falsa ($n + 1$ comparaciones).
* Incremento `i++`: 1 suma y 1 asignación ejecutadas $n$ veces ($2n$ operaciones).
* Subtotal del bucle externo: $3n + 2$ operaciones.


* En el bucle interno `while` (la variable $j$ se duplica en cada paso empezando en 1, por lo que itera $k = \lceil \log_2(n) \rceil$ veces para $n > 1$ por cada vuelta externa):
* Inicialización `int j = 1`: 1 asignación por cada iteración externa ($1 \times n = n$ operaciones).
* Condición `j < n`: $\lceil \log_2(n) \rceil$ evaluaciones verdaderas y 1 falsa por cada vuelta externa ($(\lceil \log_2(n) \rceil + 1) \times n = n \lceil \log_2(n) \rceil + n$ comparaciones).
* Cuerpo `cout << i << " " << j << endl;`: 1 operación de impresión por iteración del while ($n \lceil \log_2(n) \rceil$ operaciones).
* Actualización `j = j * 2;`: 1 multiplicación y 1 asignación por iteración del while ($2 \times n \lceil \log_2(n) \rceil = 2n \lceil \log_2(n) \rceil$ operaciones).
* Subtotal del bucle interno: $n + (n \lceil \log_2(n) \rceil + n) + n \lceil \log_2(n) \rceil + 2n \lceil \log_2(n) \rceil = 4n \lceil \log_2(n) \rceil + 2n$ operaciones.


* Siendo un total general (para $n > 1$) de: $(3n + 2) + (4n \lceil \log_2(n) \rceil + 2n) = 4n \lceil \log_2(n) \rceil + 5n + 2$ operaciones. Si $n \le 0$, el bucle exterior no entra y solo hace la inicialización y una comparación fallida (total = 2 operaciones). Si $n = 1$, el bucle externo entra 1 vez y el `while` evalúa la condición como falsa directamente (total = 9 operaciones).

*Operaciones por iteración:*

* Por cada iteración del bucle interno `while`: se ejecutan 4 operaciones (1 comparación verdadera `j < n`, 1 operación de salida en `cout`, y 1 multiplicación más 1 asignación en `j = j * 2`).
* Por cada iteración del bucle externo `i`: se ejecutan $4 \lceil \log_2(n) \rceil + 5$ operaciones (1 comparación verdadera `i < n`, 2 operaciones por el incremento `i++`, 1 asignación en `int j = 1`, más las comparaciones, impresiones y multiplicaciones del bucle `while`).

**Complejidad:** es linealítmica respecto a $n$, ya que el bucle exterior se ejecuta $n$ veces y por cada una de ellas el bucle interior crece de manera logarítmica ($\log_2 n$) al multiplicarse $j$ por 2 en cada paso, por lo tanto es $O(n \log n)$.

## Ejercicio 11

```c++
int search(int arr[], int n, int target) {
    /*
    Búsqueda
    */
    int salto = (int)sqrt(n);
    
    //
    int prev = 0;
    while (arr[min(salto, n) - 1] < target) {
        prev = salto;
        salto += (int)sqrt(n);
        
        // Si llegamos al final sin encontrar
        if (prev >= n) {
            return -1;
        }
    }
    
    // Búsqueda en el bloque
    while (arr[prev] < target) {
        prev++;
    
        // Si llegamos al siguiente bloque o al final
        if (prev == min(salto, n)) {
            return -1;
        }
    }
    
    // Verificar si encontramos el elemento
    if (arr[prev] == target) {
        return prev;
    }

    return -1;
}
```

**Operaciones por caso:** Hay una asignación con un `cast` y una función (operaciones = 3); después otra inicialización (operaciones = 4). En el primer `while` hay 4 operaciones (la función `min`, la resta, la indexación del arreglo y la comparación, totalizando 8), y dentro de este hay una asignación, una suma con asignación, `cast` y función (operaciones = 13), y después una comparación en el `if` y otra si es verdadera (operaciones = 14). En el siguiente `while` hay una comparación con extracción de valor y dentro una suma y asignación, y otra comparación con una función (operaciones = 20). Al último `if` hay otra comparación con indexación, y termina con un `return` (operaciones = 23).

**Operaciones por iteración:** Las iteraciones solo están en los `while`, siendo en el primero 10 operaciones y en el segundo solo 6.

**Complejidad:** La complejidad terminaría siendo $4 + 10\sqrt{n} + 6\sqrt{n} + 3 = 7 + 16\sqrt{n}$, que por reglas termina siendo simplemente $O(\sqrt{n})$, donde $\sqrt{n}$ viene de `int salto = (int)sqrt(n);`.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo.
> 
> int search(int arr[], int n, int target) {
>    /*
>    Búsqueda
>    */
>    int salto = (int)sqrt(n);
>    
>    int prev = 0;
>    while (arr[min(salto, n) - 1] < target) {
>        prev = salto;
>        salto += (int)sqrt(n);
>        if (prev >= n) {
>            return -1;
>        }
>    }
>    
>    while (arr[prev] < target) {
>        prev++;
>        if (prev == min(salto, n)) {
>            return -1;
>        }
>    }
>    
>    if (arr[prev] == target) {
>        return prev;
>    }
>
>    return -1;
>}
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* En la inicialización:
* `int salto = (int)sqrt(n);`: 1 función matemática `sqrt`, 1 conversión de tipo y 1 asignación (operaciones = 3).
* `int prev = 0;`: 1 asignación (operaciones = 1).
* Subtotal de inicialización: 4 operaciones.


* **Mejor caso** (`target` está en el primer elemento `arr[0]` o el primer bloque ya lo supera en su inicio sin iterar los bucles):
* Primer `while`: evalúa `min(salto, n) - 1` (1 mínimo y 1 resta), indexa `arr[...]` y compara `< target` (2 operaciones). Como `target` ya es menor o igual, la condición es falsa de inmediato (4 operaciones).
* Segundo `while`: evalúa indexación `arr[prev]` y comparación `< target` (2 operaciones). Como `arr[0] == target`, es falsa de inmediato (2 operaciones).
* Verificación final: evalúa `arr[prev] == target` (1 indexación y 1 comparación = 2 operaciones) y ejecuta `return prev;` (1 operación).
* Total mejor caso: $4 + 4 + 2 + 2 + 1 = 13$ operaciones.


* **Peor caso** (`target` es mayor que todos los elementos o está al final del último bloque de tamaño $m \approx \sqrt{n}$):
* El primer `while` (búsqueda por bloques) da aproximadamente $\lceil \frac{n}{m} \rceil \approx \sqrt{n}$ saltos. En cada salto evalúa condición (4 operaciones), asigna `prev = salto` (1 op), calcula `(int)sqrt(n)` y suma a `salto` (3 ops), y evalúa `if (prev >= n)` (1 comparación), totalizando 9 operaciones por vuelta, más 4 operaciones de la última evaluación que resulta falsa.
* El segundo `while` (búsqueda lineal dentro del bloque) itera hasta $m \approx \sqrt{n}$ veces. En cada paso evalúa condición (2 operaciones), incrementa `prev++` (2 ops), y evalúa `if (prev == min(salto, n))` (1 mínimo y 1 comparación = 2 ops), totalizando 6 operaciones por vuelta, más 2 operaciones de la condición falsa de salida.
* Verificación final: evalúa `arr[prev] == target` (2 operaciones) y hace un `return` (1 operación).
* Total peor caso: aproximadamente $15\sqrt{n} + 13$ operaciones (o del orden de $c \cdot \sqrt{n}$).



*Operaciones por iteración:*

* Por cada iteración del primer `while` (fase de saltos): se realizan 9 operaciones (1 evaluación de condición compuesta con `min`, resta, indexación y comparación; 1 asignación en `prev = salto`; 1 cálculo de `sqrt`, 1 suma y 1 asignación en `salto += ...`; y 1 comparación en el `if`).
* Por cada iteración del segundo `while` (fase lineal): se realizan 6 operaciones (1 evaluación con indexación y comparación `arr[prev] < target`; 2 operaciones por el incremento `prev++`; y 2 operaciones por el `if` evaluando la función `min` y la igualdad).

**Complejidad:** este algoritmo corresponde a **Jump Search** (búsqueda por saltos con paso óptimo $m = \sqrt{n}$). En el mejor caso realiza operaciones constantes $\Omega(1)$ si el objetivo está al principio; en el peor caso recorre a lo más $\frac{n}{m}$ bloques y luego $m$ elementos dentro del bloque ($\sqrt{n} + \sqrt{n}$), por lo tanto su complejidad es $O(\sqrt{n})$.

## Ejercicio 12

```c
#include <stdio.h>
#include <stdlib.h>
/* ------------------------------------------------------------------ */
/* merge(): fusiona dos subarreglos adyacentes ya ordenados           */
/* A[izq .. med] (izquierdo)                                          */
/* A[med+1 .. der] (derecho)                                          */
/* usando un arreglo auxiliar 'tmp'.                                  */
/* ------------------------------------------------------------------ */
void merge(int A[], int tmp[], int izq, int med, int der) {
    int i = izq; /* recorre el subarreglo izquierdo */
    int j = med + 1; /* recorre el subarreglo derecho */
    int k = izq; /* recorre el arreglo de salida */
    
    /* (1) mezcla comparando cabeza contra cabeza */
    while (i <= med && j <= der) { /* <-- ciclo principal */
        if (A[i] <= A[j])
            tmp[k++] = A[i++];
        else
    
            tmp[k++] = A[j++];
    }

    /* (2) copia el remanente del lado izquierdo (si quedó) */
    while (i <= med)
        tmp[k++] = A[i++];
    
    /* (3) copia el remanente del lado derecho (si quedó) */
    while (j <= der)
        tmp[k++] = A[j++];
    
    /* (4) vuelca el segmento fusionado de tmp de regreso a A */
    for (k = izq; k <= der; k++)
        A[k] = tmp[k];
}

/* ------------------------------------------------------------------ */
/* merge_sort_iterativo(): version NO recursiva (bottom-up).          */
/* En lugar de dividir con recursion, va fusionando bloques de        */
/* tamano 'ancho' que se duplica en cada pasada: 1, 2, 4, 8, ...      */
/* ------------------------------------------------------------------ */
void merge_sort_iterativo(int A[], int n) {
    int *tmp = (int *) malloc(n * sizeof(int));
    if (tmp == NULL) return;

    int ancho, izq;
    
    /* CICLO EXTERNO: ancho de los bloques a fusionar */
    for (ancho = 1; ancho < n; ancho = 2 * ancho) {
    
        /* CICLO INTERNO: recorre el arreglo por pares de bloques */
        for (izq = 0; izq < n; izq = izq + 2 * ancho) {
            int med = izq + ancho - 1;
            int der = izq + 2 * ancho - 1;

            if (med >= n - 1) continue; /* no hay bloque derecho */
            if (der > n - 1) der = n - 1; /* recorta el ultimo bloque */

            merge(A, tmp, izq, med, der);
        }
    }

    free(tmp);
}

int main(void) {
    int A[] = {38, 27, 43, 3, 9, 82, 10};
    int n = sizeof(A) / sizeof(A[0]);

    merge_sort_iterativo(A, n);

    for (int i = 0; i < n; i++)
        printf("%d ", A[i]);
    printf("\n");
    return 0;
}
```

**Operaciones por caso:** En la función `merge` tenemos una asignación, una suma y asignación, y otra asignación (operaciones = 4). En el `while` tenemos 2 comparaciones y un `and`, y dentro tenemos un `if/else` con una comparación y 2 indexaciones, y si es verdadero o falso, una asignación y 2 indexaciones con dos sumas y asignaciones (operaciones = 17). Los siguientes 2 `while` no siempre se ejecutan, pero son 2 comparaciones (operaciones = 19). El `for` tiene 5 operaciones: una asignación, una comparación, 2 indexaciones y otra asignación (operaciones = 24). En el `merge_sort` tenemos 5 operaciones para el `tmp`, siendo la asignación, el `cast`, la reserva de memoria, la función y la multiplicación; después, una comparación y 2 reservas de memoria (operaciones = 32). En el primer `for` tenemos su asignación y comparación (operaciones = 36), y en el segundo `for` tenemos también su asignación y comparación, y dentro de este tenemos una suma, resta y asignación, una suma, resta, asignación y multiplicación (operaciones = 40). Después, 2 comparaciones y una llamada a la función `merge` y la liberación de memoria (operaciones = 47). Por último, en el `main` tenemos la creación del arreglo, la división y asignación de `n` con 2 funciones e indexación (operaciones = 53). Después, la función `merge_sort` (operaciones = 54), y al final un `for` con asignación, comparación y un `print` con indexación (operaciones = 58), terminando con otro `print` y `return`, siendo 60 operaciones en total.

**Operaciones por iteración:** En las iteraciones, en `merge` en el `while` tenemos 13 operaciones, en el `for` tenemos 5. En el `merge_sort` tenemos 2 `for`, siendo el primero de 3 operaciones y el segundo de 16. En el `main` hay un solo `for` que es de 5 operaciones.

**Complejidad:** La complejidad completa la obtenemos multiplicando la complejidad de `merge` por `merge_sort` dado que están anidados. `merge` es de $18n$ y `merge_sort` de $\log_2(n)$ debido a cómo incrementa $n$. Dado que están anidados se multiplican, y por reglas queda $O(n \log_2(n))$.

---

### Respuesta de IA

**Prompt usado:**

> Por favor ayudame con lo siguiente
> Determina cuántas operaciones se realizarán en cada caso. 
> 
> Determina cuántas operaciones se realizarán por iteración.
> 
> Determina la complejidad del algoritmo adjunto
> 
> puedes basarte en el siguiente formato de markdown para generar tu propia respuesta
> 
> Operaciones por caso: en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma > y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones > = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno > siendo un total de 8 operaciones
> 
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

**Operaciones por caso:**

* En la reserva de memoria y control inicial: `int *tmp = (int *) malloc(n * sizeof(int));` y la validación `if (tmp == NULL)` toman 1 multiplicación, 1 llamada a `malloc`, 1 asignación y 1 comparación (operaciones = 4).
* Nivel de fusiones completas (cada nivel fusiona segmentos que cubren los $n$ elementos):
* La función `merge()` procesa un segmento de tamaño $L = (\text{der} - \text{izq} + 1)$. Inicializa 3 variables (`i`, `j`, `k`) con 3 asignaciones y 1 suma (operaciones = 4).
* En la mezcla principal y remanentes: cada uno de los $L$ elementos se compara y se copia en `tmp[k++]` con 2 indexaciones, 1 asignación y 2 incrementos postfijos ($2 + 1 + 2 = 5$ operaciones elementales por elemento copiado, más 2 comparaciones en la condición del bucle), sumando aproximadamente entre $8L$ y $9L$ operaciones por todo el segmento.
* En el volcado de regreso: el bucle `for (k = izq; k <= der; k++) A[k] = tmp[k];` realiza 1 inicialización, $L + 1$ comparaciones, $2L$ operaciones de incremento (`k++`) y $3L$ operaciones por copiar `A[k] = tmp[k]` (2 indexaciones y 1 asignación), sumando $6L + 2$ operaciones.
* Por tanto, para un nivel completo donde la suma de todas las longitudes de subsegmentos es $\sum L = n$, la función `merge()` consume en total aproximadamente $15n$ operaciones por pasada.


* Bucle externo `ancho` y bucle interno `izq`:
* El bucle externo duplica el `ancho` iniciando en 1 hasta alcanzar $n$, ejecutándose exactamente $\lceil \log_2(n) \rceil$ veces.
* El bucle interno divide el arreglo en pasos de $2 \times \text{ancho}$, calculando `med` y `der` (sumas, restas y asignaciones $\approx 6$ operaciones por bloque) y llamando a `merge()`.
* La suma del trabajo de todos los bloques en una misma pasada externa es de orden lineal ($\approx c_1 n$ operaciones por pasada).


* Al finalizar los bucles: se ejecuta `free(tmp);` (1 liberación de memoria).
* Siendo un total general: tanto en el **mejor caso** (arreglo ya ordenado), **caso promedio** y **peor caso** (arreglo en orden inverso), Merge Sort siempre realiza el proceso completo de división y fusión en todos sus niveles, realizando aproximadamente $c \cdot n \lceil \log_2(n) \rceil + k \cdot n$ operaciones totales (donde $c \approx 15 \text{ a } 18$).

*Operaciones por iteración:*

* Por cada elemento fusionado en `merge()` (iteración del `while` principal): se ejecutan entre 8 y 9 operaciones (2 comparaciones de límites `i <= med && j <= der`, 1 comparación de elementos `A[i] <= A[j]`, 2 indexaciones, 1 asignación y 2 incrementos).
* Por cada iteración del volcado de `tmp` a `A`: se ejecutan 6 operaciones (1 comparación `k <= der`, 2 indexaciones, 1 asignación y 2 operaciones por el incremento `k++`).
* Por cada iteración del bucle interno `izq`: se ejecutan aproximadamente $15L + 10$ operaciones (cálculo de límites `med` y `der`, dos comparaciones `if`, y la fusión completa de los subarreglos de tamaño $L$).
* Por cada iteración del bucle externo `ancho`: se ejecuta una pasada completa sobre todo el arreglo de tamaño $n$, sumando aproximadamente $15n + 5$ operaciones (1 comparación de condición, 2 operaciones para duplicar `ancho = 2 * ancho`, más todas las fusiones del nivel).

**Complejidad:** es linealítmica en todos los casos (mejor, promedio y peor caso), ya que el bucle externo realiza $\log_2(n)$ iteraciones y en cada una de ellas se procesan linealmente los $n$ elementos del arreglo mediante fusiones sucesivas, por lo tanto su complejidad es $\Theta(n \log n)$ y su cota superior es $O(n \log n)$. Con una complejidad espacial adicional de $O(n)$ debido al arreglo auxiliar `tmp`.