# Ejercicios

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

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* no hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:* en la línea 1 hay una asignación (operaciones = 1), en la línea 2 hay una suma y una asignación (operaciones = 3), en la línea 3 hay una multiplicación y una asignación (operaciones = 5), en la línea 4 hay una resta y una asignación (operaciones = 7) y en la línea 5 hay un retorno, siendo un total de 8 operaciones fijas sin importar el valor de `n`.

*Operaciones por iteración:* no hay iteración (no existen bucles ni estructuras repetitivas).

*Complejidad:* es constante dado que el número de operaciones no depende del parámetro de entrada `n`, por lo tanto es $O(1)$.

## Ejercicio 2

```c++
for (int i = 0; i < n; i += 2) {
    cout << i << endl;
}
```

*Operaciones por caso:* en el for tenemos una asignacion una comparacion y una suma con asignacion siendo 4 operaciones pero de las cuales solo la asignacion y comparacion se hacen al inicio siendo solo 2 operaciones

*Operaciones por iteracion:* en cada iteracion hay una comparacion una suma y asignacion y una impresion siendo 4 operaciones por iteracion

*Complejidad:* la complejidad es O(n) debido al for ya que las demas operaciones son constantes

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

* En la inicialización `int i = 0` hay 1 asignación (operaciones = 1).
* En la condición `i < n` se realizan comparaciones: se evalúa $\lceil \frac{n}{2} \rceil$ veces como verdadera y 1 vez como falsa al salir (operaciones de comparación = $\lceil \frac{n}{2} \rceil + 1$).
* En la actualización `i += 2` hay una suma y una asignación en cada paso que entra al bucle, es decir, 2 operaciones realizadas $\lceil \frac{n}{2} \rceil$ veces (operaciones de incremento = $2 \lceil \frac{n}{2} \rceil$).
* En el cuerpo `cout << i << endl;` hay 1 operación de impresión por cada iteración válida (operaciones de salida = $\lceil \frac{n}{2} \rceil$).
* Siendo un total de: $1 + (\lceil \frac{n}{2} \rceil + 1) + 2 \lceil \frac{n}{2} \rceil + \lceil \frac{n}{2} \rceil = 4 \lceil \frac{n}{2} \rceil + 2$ operaciones (o aproximadamente $2n + 2$ operaciones para $n \ge 0$ par). Si $n \le 0$, el bucle no entra y solo se hace la asignación inicial y 1 comparación fallida (total = 2 operaciones).

*Operaciones por iteración:* en cada vuelta del ciclo se ejecutan 4 operaciones (1 comparación verdadera `i < n`, 1 operación de salida en `cout`, y 1 suma más 1 asignación en `i += 2`).

*Complejidad:* es lineal respecto al valor de $n$, ya que el número de operaciones crece de forma directamente proporcional a $n$ dividida entre 2, por lo tanto es $O(n)$.

## Ejercicio 3

```c++
for (int i = 0; i < n; i++) {
    for (int j = 0; j < 5; j++) {
        cout << i << " " << j << endl;
    }
}
```

*Operaciones por caso:* en el for externo hay una asignacion y una comparacion en el interno otra asignacion otra comparacion y dentro una impresion dando 5 operaciones, las sumas y asignacion es en la iteracion

*Operaciones por iteracion:* en la iteracion en el for externo son una comparacion una suma y una asignacion siendo 3n operaciones por iteracion en el for interno es lo mismo cambiando la comparacion a que sea menor a 5 siendo 20 operaciones en total ya contando la impresion dentro de este siendo 5*4 operaciones

*Complejidad:* la complejidad total seria de 3n*20 = 60n siendo solo O(n) por reglas

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

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

*Complejidad:* es lineal respecto a $n$, ya que el bucle interno tiene un límite constante fijo (5 iteraciones) y no depende de $n$, por lo tanto es $O(n)$.

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

*Operaciones por caso:* en el bucle 1 esta su asignacion y comparacion seguido de la impresion, en el bloque 2 y 3 lo mismo siendo cada uno de 3 operaciones

*Operaciones por iteracion:* cada bucle tiene en su condicion que la variable sea menor a n teniendo como operaciones la comparacion la suma y asignacion y la impresion siendo 4 operaciones por iteracion de cada for

*Complejidad:* la cantidad de operaciones solo cambia por n en cada for y dado que estan separados solo se suman siendo n + n + n = 3n siendo por reglas simplemente O(n) 

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

* En el bucle 1: inicialización `int i = 0` (1 asignación), condición `i < n` ($n$ verdaderas + 1 falsa = $n + 1$ comparaciones), incremento `i++` (1 suma y 1 asignación ejecutadas $n$ veces = $2n$ operaciones) y cuerpo `cout << i << endl;` ($n$ operaciones de salida), sumando un subtotal de $4n + 2$ operaciones.
* En el bucle 2: inicialización `int j = 0` (1 asignación), condición `j < n` ($n + 1$ comparaciones), incremento `j++` ($2n$ operaciones) y cuerpo `cout << j << endl;` ($n$ operaciones de salida), sumando un subtotal de $4n + 2$ operaciones.
* En el bucle 3: inicialización `int k = 0` (1 asignación), condición `k < n` ($n + 1$ comparaciones), incremento `k++` ($2n$ operaciones) y cuerpo `cout << k << endl;` ($n$ operaciones de salida), sumando un subtotal de $4n + 2$ operaciones.
* Siendo un total general (para $n \ge 0$) de: $(4n + 2) + (4n + 2) + (4n + 2) = 12n + 6$ operaciones. Si $n \le 0$, cada bucle solo ejecuta su asignación y una comparación fallida, sumando un total de 6 operaciones.

*Operaciones por iteración:* en cada vuelta de cualquiera de los tres bucles se realizan 4 operaciones (1 comparación verdadera de la condición, 1 operación de impresión en el cuerpo y 2 operaciones por el incremento de la variable de control).

*Complejidad:* es lineal respecto a $n$, ya que los tres bucles se ejecutan de manera consecutiva (sumando sus complejidades individuales $O(n) + O(n) + O(n) = O(3n)$) y al descartar constantes el crecimiento es directamente proporcional a la entrada, por lo tanto es $O(n)$.

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

*Operaciones por caso:* cada for tiene su asignacion y comparacion y en el tercer for esta la impresion siendo 7 operaciones sin iteracion

*Operaciones por iteracion:* en los 2 primeros for son 3 operaciones por iteracion y en el tercero son 4 siendo 3n, 3n y 4n

*Complejidad:* dado que esta anidados se multiplican siendo (3n+1) (3n+1) (4n+2) dando O(n^3)

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

* Bucle externo `i`: 1 asignación inicial `int i = 0` (operaciones = 1), $n + 1$ comparaciones en `i < n` ($n$ verdaderas y 1 falsa), y $n$ incrementos `i++` con 1 suma y 1 asignación ($2n$ operaciones). Subtotal externo: $3n + 2$ operaciones.
* Bucle intermedio `j` (se repite $n$ veces): 1 asignación inicial por entrada `int j = 0` ($1 \times n = n$ operaciones), $n + 1$ comparaciones por entrada `j < n` ($(n + 1)n = n^2 + n$ comparaciones), y $n$ incrementos `j++` por entrada con 1 suma y 1 asignación ($2n \times n = 2n^2$ operaciones). Subtotal intermedio: $3n^2 + 2n$ operaciones.
* Bucle interno `k` (se repite $n^2$ veces): 1 asignación inicial por entrada `int k = 0` ($1 \times n^2 = n^2$ operaciones), $n + 1$ comparaciones por entrada `k < n` ($(n + 1)n^2 = n^3 + n^2$ comparaciones), $n$ incrementos `k++` por entrada con 1 suma y 1 asignación ($2n \times n^2 = 2n^3$ operaciones), y 1 operación de impresión en el cuerpo ejecutada $n^3$ veces ($n^3$ operaciones). Subtotal interno: $4n^3 + 2n^2$ operaciones.
* Siendo un total general (para $n \ge 0$) de: $(3n + 2) + (3n^2 + 2n) + (4n^3 + 2n^2) = 4n^3 + 5n^2 + 5n + 2$ operaciones. Si $n \le 0$, el bucle exterior no entra y solo realiza la inicialización y una comparación fallida (total = 2 operaciones).

*Operaciones por iteración:*

* Por cada iteración del bucle interno `k`: se ejecutan 4 operaciones (1 comparación verdadera `k < n`, 1 operación de impresión y 2 operaciones por el incremento `k++`).
* Por cada iteración del bucle intermedio `j`: se ejecutan $4n + 4$ operaciones (1 comparación verdadera `j < n`, 2 operaciones por el incremento `j++`, más la inicialización, comparaciones, incrementos e impresiones del bucle `k`).
* Por cada iteración del bucle externo `i`: se ejecutan $4n^2 + 5n + 4$ operaciones (1 comparación verdadera `i < n`, 2 operaciones por el incremento `i++`, más todo el bloque anidado de los bucles `j` y `k`).

*Complejidad:* es cúbica respecto al tamaño de entrada $n$, ya que son tres bucles anidados dependientes de $n$ que multiplican sus pasos ($n \times n \times n$), por lo tanto es $O(n^3)$.

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

*Operaciones por caso:* enpieza con una reserva de memoria y una asignacion (operaciones = 2) seguida de un for con una asignacion y una comparacion y dentro otra reserva de memoria y asignacion (operaciones = 6), en el segundo for tiene su asignacion su conparacion y dentro otro for con su asignacion y comparacion (operaciones = 10) por ultimo dentro del for anidado hay una suma asignacioN siendo un total de 12 operaciones sin iteracion

*Operaciones por iteracion:* con iteracion el primer for son 5 operaciones por comparacion suma y asignacion y reserva indexcion y asignacion, en el segundo for al ser anidados quedan 3 del externo y 5 del interno

*Complejidad:* la complejidad seria 2 + 5n + (3n*5n) = 2 +5n + 15n^2 y por reglas se vuelve O(n^2)

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

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



*Complejidad:* es cuadrática respecto al valor de $n$, ya que el término dominante corresponde al doble bucle anidado que llena la matriz de tamaño $n \times n$, por lo tanto es $O(n^2)$.

## Ejercicio 7

```c++
for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
        cout << i << " " << j << endl;
    }
}
```

*Operaciones por caso:* el for externo tiene asignacion y comparacion (operacion = 2) el for interno igual (operaciones = 4) y dentro el print siendo un total de 5 operaciones sin iteracion

*Operaciones por iteracion:* con iteracion tenemos 3 operaciones en el for externo y en el interno 4

*Complejidad:* la complejidad seria (2 + 3n) (3 + 4m) = 6 + 9n + 8m + 12nm y por reglas tendriamos solo O(nm)

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

* Bucle externo `i`: 1 asignación inicial `int i = 0` (operaciones = 1), $n + 1$ comparaciones en `i < n` ($n$ verdaderas y 1 falsa), y $n$ incrementos `i++` con 1 suma y 1 asignación ($2n$ operaciones). Subtotal externo: $3n + 2$ operaciones.
* Bucle interno `j` (se repite completo $n$ veces): 1 asignación inicial por entrada `int j = 0` ($1 \times n = n$ operaciones), $m + 1$ comparaciones por entrada `j < m` ($(m + 1)n = nm + n$ comparaciones), y $m$ incrementos `j++` por entrada con 1 suma y 1 asignación ($2m \times n = 2nm$ operaciones). Subtotal bucle interno: $3nm + 2n$ operaciones.
* Cuerpo del bucle `cout << i << " " << j << endl;`: se ejecuta $n \times m$ veces con 1 operación de impresión por ejecución ($nm$ operaciones).
* Siendo un total general (para $n, m \ge 0$) de: $(3n + 2) + (3nm + 2n) + nm = 4nm + 5n + 2$ operaciones. Si $n \le 0$, el bucle exterior no entra y solo se realiza la asignación inicial y 1 comparación fallida (total = 2 operaciones).

*Operaciones por iteración:*

* Por cada iteración del bucle interno `j`: se ejecutan 4 operaciones (1 comparación verdadera `j < m`, 1 operación de salida en `cout`, y 2 operaciones por el incremento `j++`).
* Por cada iteración del bucle externo `i`: se ejecutan $4m + 4$ operaciones (1 comparación verdadera `i < n`, 2 operaciones de incremento `i++`, más la inicialización de `j = 0`, las $m+1$ comparaciones de `j`, las $m$ impresiones y los $m$ incrementos de `j`).

*Complejidad:* depende de dos variables de entrada independientes ($n$ y $m$), ya que el bucle exterior corre $n$ veces y el bucle interior corre $m$ veces por cada vuelta, por lo tanto es $O(n \times m)$.

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

*Operaciones por caso:* en las declaraciones tenemos dos reservas de memoria (operaciones = 2) en el for externo tenemos una asignacion y una comparacion en el interno tenemos tambien una asignacion (operaciones = 6) y comparacion y dentro de este tenemos un if con una comparacion y si es verdades otra operacion break siendo siempre 7 operaciones y 8 si el if es verdadero

*Operaciones por iteracion:* en las iteraciones en el for externo tenemos 3 operaciones iterativas y en el interno 4

*Complejidad:* la complejidad seria 2 + 3n * 4n = 2 + 12n^2 que por reglas se vuelve O(n^2)

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

* En las declaraciones iniciales: `int arr[n];` y `int target;` representan reservas de espacio en memoria sin asignación explícita (operaciones = 0 directas de cómputo).
* En el bucle externo `i`: 1 asignación inicial `int i = 0` (operaciones = 1), $n + 1$ comparaciones en `i < n` ($n$ verdaderas y 1 falsa), y $n$ incrementos `i++` con 1 suma y 1 asignación ($2n$ operaciones). Subtotal externo fijo: $3n + 2$ operaciones.
* Para el bucle interno `j` (depende del contenido de `arr` y la posición de `target`):
* **Mejor caso** (`target` está en la primera posición `arr[0]`): en cada una de las $n$ iteraciones externas, `j` se inicializa (1 asignación), evalúa `j < n` (1 comparación verdadera), indexa y compara `arr[j] == target` (2 operaciones) y ejecuta `break;` (1 salto de control). Por tanto, el bucle interno hace $(1 + 1 + 2 + 1) \times n = 5n$ operaciones. Total mejor caso: $(3n + 2) + 5n = 8n + 2$ operaciones.
* **Peor caso** (`target` no está en el arreglo): el bucle interno corre completo las $n$ veces. Por cada vuelta externa hay: 1 inicialización `j = 0` ($n$ operaciones), $n + 1$ comparaciones `j < n` ($n^2 + n$ operaciones), $n$ incrementos `j++` ($2n^2$ operaciones), y $n$ evaluaciones de `arr[j] == target` con 1 indexación y 1 comparación ($2n^2$ operaciones). Total bucle interno peor caso: $5n^2 + 2n$ operaciones. Total peor caso: $(3n + 2) + (5n^2 + 2n) = 5n^2 + 5n + 2$ operaciones.



*Operaciones por iteración:*

* Por cada iteración del bucle interno `j`: se ejecutan 5 operaciones (1 comparación verdadera `j < n`, 2 operaciones en el `if` por indexar y comparar `arr[j] == target`, y 2 operaciones por el incremento `j++` si no se cumple la condición).
* Por cada iteración del bucle externo `i`: en el mejor caso realiza 8 operaciones (1 comparación `i < n`, 2 por `i++`, y 5 del bucle interno al romper en la primera vuelta); en el peor caso realiza $5n + 5$ operaciones (1 comparación `i < n`, 2 por `i++`, más la inicialización, comparaciones, incrementos y evaluaciones completas del ciclo de `j`).

*Complejidad:* en el mejor caso es lineal $\Omega(n)$ ya que el `break` se activa en la primera iteración de `j`; sin embargo, en el peor caso (y caso promedio) el ciclo interno recorre todo el arreglo sin encontrar el elemento, por lo tanto su cota superior es cuadrática $O(n^2)$.

## Ejercicio 9

```c++
int i = n;
while (i > 1) {
    cout << i << endl;
    i = i / 2;
}
```

*Operaciones por caso:* inicia con una asignacion y en el while una comparacion y dentro una impresion y una division y asignacion siendo 5 operaciones

*Operaciones por iteracion:* por iteraciones serian 4 operaciones por las operaciones de comparacion impresion division y asignacion dentro del while

*Complejidad:* su complejidad seria de 1 + 4n al dividir  constantemente n entre 2 esto se vuelve O(log_2(n))

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

* En la inicialización `int i = n;` hay 1 asignación (operaciones = 1).
* En el bucle `while (i > 1)` la variable $i$ se divide a la mitad en cada paso, por lo que el ciclo se ejecuta $k = \lfloor \log_2(n) \rfloor$ veces (para $n \ge 1$).
* En la condición `i > 1` se realizan $\lfloor \log_2(n) \rfloor$ comparaciones verdaderas y 1 falsa que rompe el ciclo (operaciones = $\lfloor \log_2(n) \rfloor + 1$).
* En el cuerpo `cout << i << endl;` hay 1 operación de salida ejecutada $\lfloor \log_2(n) \rfloor$ veces (operaciones = $\lfloor \log_2(n) \rfloor$).
* En la actualización `i = i / 2;` hay 1 división y 1 asignación ejecutadas $\lfloor \log_2(n) \rfloor$ veces (operaciones = $2 \lfloor \log_2(n) \rfloor$).


* Siendo un total general (para $n > 1$) de: $1 + (\lfloor \log_2(n) \rfloor + 1) + \lfloor \log_2(n) \rfloor + 2 \lfloor \log_2(n) \rfloor = 4 \lfloor \log_2(n) \rfloor + 2$ operaciones. Si $n \le 1$, el bucle no entra y solo se realiza la asignación inicial y 1 comparación fallida (total = 2 operaciones).

*Operaciones por iteración:* en cada vuelta del ciclo se realizan 4 operaciones (1 comparación verdadera `i > 1`, 1 operación de impresión en `cout`, y 1 división más 1 asignación en `i = i / 2`).

*Complejidad:* es logarítmica respecto a $n$, ya que en cada paso el valor de $i$ se divide entre 2, reduciendo el espacio del problema a la mitad de forma sucesiva, por lo tanto es $O(\log n)$.

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

*Operaciones por caso:* en el for tenemos una asignacion y comparacion (operaciones = 2) despues dentro tenemos otra asignacion y un while con una comparacion (operaciones = 4) dentro del while tenemos una impresion una multiplicacion y una asignacion siendo 7 operaciones

*Operaciones por iteracion:* en el for tenemos 4 operaciones iterativas contando la comparacion suma asignacion y la asignacion y en el while tenemos tambien 4 operaciones iterativas

*Complejidad:* al ser el for y while anidados se multiplican sus complejidades siendo 4n * 4(log_2(n)) el log base dos es por que j aumenta multiplicandose por 2 por reglas se vuelve O(n * log_2(n))

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

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

*Complejidad:* es linealítmica respecto a $n$, ya que el bucle exterior se ejecuta $n$ veces y por cada una de ellas el bucle interior crece de manera logarítmica ($\log_2 n$) al multiplicarse $j$ por 2 en cada paso, por lo tanto es $O(n \log n)$.

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

*Operaciones por caso:* 

*Operaciones por iteracion:* 

*Complejidad:* 

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

* En la inicialización `int i = 0` hay 1 asignación (operaciones = 1).
* En la condición `i < n` se realizan comparaciones: se evalúa $\lceil \frac{n}{2} \rceil$ veces como verdadera y 1 vez como falsa al salir (operaciones de comparación = $\lceil \frac{n}{2} \rceil + 1$).
* En la actualización `i += 2` hay una suma y una asignación en cada paso que entra al bucle, es decir, 2 operaciones realizadas $\lceil \frac{n}{2} \rceil$ veces (operaciones de incremento = $2 \lceil \frac{n}{2} \rceil$).
* En el cuerpo `cout << i << endl;` hay 1 operación de impresión por cada iteración válida (operaciones de salida = $\lceil \frac{n}{2} \rceil$).
* Siendo un total de: $1 + (\lceil \frac{n}{2} \rceil + 1) + 2 \lceil \frac{n}{2} \rceil + \lceil \frac{n}{2} \rceil = 4 \lceil \frac{n}{2} \rceil + 2$ operaciones (o aproximadamente $2n + 2$ operaciones para $n \ge 0$ par). Si $n \le 0$, el bucle no entra y solo se hace la asignación inicial y 1 comparación fallida (total = 2 operaciones).

*Operaciones por iteración:* en cada vuelta del ciclo se ejecutan 4 operaciones (1 comparación verdadera `i < n`, 1 operación de salida en `cout`, y 1 suma más 1 asignación en `i += 2`).

*Complejidad:* es lineal respecto al valor de $n$, ya que el número de operaciones crece de forma directamente proporcional a $n$ dividida entre 2, por lo tanto es $O(n)$.

## Ejercicio 12

```c++
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

*Operaciones por caso:* 

*Operaciones por iteracion:* 

*Complejidad:* 

### Respuesta de IA

*Prompt usado:*

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

*Operaciones por caso:*

* En la inicialización `int i = 0` hay 1 asignación (operaciones = 1).
* En la condición `i < n` se realizan comparaciones: se evalúa $\lceil \frac{n}{2} \rceil$ veces como verdadera y 1 vez como falsa al salir (operaciones de comparación = $\lceil \frac{n}{2} \rceil + 1$).
* En la actualización `i += 2` hay una suma y una asignación en cada paso que entra al bucle, es decir, 2 operaciones realizadas $\lceil \frac{n}{2} \rceil$ veces (operaciones de incremento = $2 \lceil \frac{n}{2} \rceil$).
* En el cuerpo `cout << i << endl;` hay 1 operación de impresión por cada iteración válida (operaciones de salida = $\lceil \frac{n}{2} \rceil$).
* Siendo un total de: $1 + (\lceil \frac{n}{2} \rceil + 1) + 2 \lceil \frac{n}{2} \rceil + \lceil \frac{n}{2} \rceil = 4 \lceil \frac{n}{2} \rceil + 2$ operaciones (o aproximadamente $2n + 2$ operaciones para $n \ge 0$ par). Si $n \le 0$, el bucle no entra y solo se hace la asignación inicial y 1 comparación fallida (total = 2 operaciones).

*Operaciones por iteración:* en cada vuelta del ciclo se ejecutan 4 operaciones (1 comparación verdadera `i < n`, 1 operación de salida en `cout`, y 1 suma más 1 asignación en `i += 2`).

*Complejidad:* es lineal respecto al valor de $n$, ya que el número de operaciones crece de forma directamente proporcional a $n$ dividida entre 2, por lo tanto es $O(n)$.