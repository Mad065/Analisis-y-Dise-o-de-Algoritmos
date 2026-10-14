#include <stdio.h>
#include <stdlib.h>

/* ------------------------------------------------------------------ */
/*  merge(): fusiona dos subarreglos adyacentes ya ordenados          */
/*    A[izq .. med]      (izquierdo)                                   */
/*    A[med+1 .. der]    (derecho)                                     */
/*  usando un arreglo auxiliar 'tmp'.                                  */
/* ------------------------------------------------------------------ */
void merge(int A[], int tmp[], int izq, int med, int der) {
    int i = izq;        /* recorre el subarreglo izquierdo  */
    int j = med + 1;    /* recorre el subarreglo derecho    */
    int k = izq;        /* recorre el arreglo de salida     */

    printf("Fusionando A[%d..%d] y A[%d..%d]\n", izq, med, med + 1, der);
    printf("Izq: %d\n", izq);
    printf("Med: %d\n", med);
    printf("Der: %d\n", der);

    /* (1) mezcla comparando cabeza contra cabeza */
    while (i <= med && j <= der) {          /* <-- ciclo principal */
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


    printf("A: ");
    for (int x = izq; x <= der; x++)
        printf("%d ", A[x]);
    printf("\n");
    
    printf("temp: ");
    for (int x = izq; x <= der; x++)
        printf("%d ", tmp[x]);
    printf("\n");

    /* (4) vuelca el segmento fusionado de tmp de regreso a A */
    for (k = izq; k <= der; k++)
        A[k] = tmp[k];

    printf("A (despues de fusionar): ");
    for (int x = izq; x <= der; x++)
        printf("%d ", A[x]);
    printf("\n\n");
}

/* ------------------------------------------------------------------ */
/*  merge_sort_iterativo(): version NO recursiva (bottom-up).         */
/*  En lugar de dividir con recursion, va fusionando bloques de       */
/*  tamano 'ancho' que se duplica en cada pasada: 1, 2, 4, 8, ...     */
/* ------------------------------------------------------------------ */
void merge_sort_iterativo(int A[], int n) {
    int *tmp = (int *) malloc(n * sizeof(int));
    if (tmp == NULL) return;

    int ancho, izq;

    /* CICLO EXTERNO: ancho de los bloques a fusionar */
    for (ancho = 1; ancho < n; ancho = 2 * ancho) {
        printf("-----------------------------------Ciclo externo: ancho = %d\n", ancho);

        /* CICLO INTERNO: recorre el arreglo por pares de bloques */
        for (izq = 0; izq < n; izq = izq + 2 * ancho) {
            printf("------------------------Ciclo interno: izq = %d\n", izq);
            int med = izq + ancho - 1;
            int der = izq + 2 * ancho - 1;

            if (med >= n - 1) continue;      /* no hay bloque derecho */
            if (der > n - 1) der = n - 1;     /* recorta el ultimo bloque */

            merge(A, tmp, izq, med, der);
        }
    }

    free(tmp);
}

int main(void) {
    int A[] = {38, 27, 43, 3, 9, 82, 10};
    int n = sizeof(A) / sizeof(A[0]);

    merge_sort_iterativo(A, n);

    printf("N: %d\n", n);

    printf("\nArreglo ordenado: \n");
    for (int i = 0; i < n; i++)
        printf("%d ", A[i]);
    printf("\n");
    return 0;
}