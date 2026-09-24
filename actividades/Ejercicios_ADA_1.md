# Ejercicios

## Ejercicio 1

```c
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

```c
for (int i = 0; i < n; i += 2) {
    cout << i << endl;
}
```

*Operaciones por caso:* En el for tenemos

*Operaciones por iteracion:* No hay iteracion

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
> Operaciones por iteracion: No hay iteracion
> 
> Complejidad: es constante dado que no cambia la cantidad de operaciones O(1)

*Operaciones por caso:* en la línea 1 hay una asignación (operaciones = 1), en la línea 2 hay una suma y una asignación (operaciones = 3), en la línea 3 hay una multiplicación y una asignación (operaciones = 5), en la línea 4 hay una resta y una asignación (operaciones = 7) y en la línea 5 hay un retorno, siendo un total de 8 operaciones fijas sin importar el valor de `n`.

*Operaciones por iteración:* No hay iteración (no existen bucles ni estructuras repetitivas).

*Complejidad:* es constante dado que el número de operaciones no depende del parámetro de entrada `n`, por lo tanto es $O(1)$.

## Ejercicio 3

```c
for (int i = 0; i < n; i++) {
    for (int j = 0; j < 5; j++) {
        cout << i << " " << j << endl;
    }
}
```

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

## Ejercicio 4

```c
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

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

## Ejercicio 5

```c
for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
        for (int k = 0; k < n; k++) {
            cout << i << " " << j << " " << k << endl;
        }
    }
}
```

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

## Ejercicio 6

```c
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

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

## Ejercicio 7

```c
for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
        cout << i << " " << j << endl;
    }
}
```

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

## Ejercicio 8

```c
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

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

## Ejercicio 9

```c
int i = n;
while (i > 1) {
    cout << i << endl;
    i = i / 2;
}
```

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

## Ejercicio 10

```c
for (int i = 0; i < n; i++) {
    int j = 1;
    while (j < n) {
        cout << i << " " << j << endl;
        j = j * 2;
    }
}
```

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

## Ejercicio 11

```c
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

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)

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

*Operaciones por caso:* en la linea 1 hay una asignacion (operaciones = 1) en la linea 2 hay una suma y una asignacion (operaciones = 3) en la linea 3 hay una multiplicacion y una asignacion (operaciones = 5) en la linea 4 hay una resta y una asignacion (operaciones = 7) y en la linea 5 hay un retorno siendo un total de 8 operaciones

*Operaciones por iteracion:* No hay iteracion

*Complejidad:* es constante dado que no cambia la cantidad de operaciones O(1)