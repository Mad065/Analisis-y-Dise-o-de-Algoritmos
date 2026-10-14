/* ================================================================== *
 *  PAR DE PUNTOS MÁS CERCANOS  —  Divide y Vencerás                   *
 *                                                                     *
 *  Dado un conjunto de n puntos en el plano euclidiano 2D,            *
 *  encuentra el par cuya distancia euclidiana sea mínima.             *
 *                                                                     *
 *  Clave para que sea eficiente la combinación:                       *
 *  los puntos se mantienen ORDENADOS POR Y a través de la recursión   *
 *  mediante una fusión tipo merge (O(n)), en vez de reordenar en      *
 *  cada nivel con qsort (lo que elevaría el costo a O(n log^2 n)).    *
 *                                                                     *
 *  Recurrencia de rec(): T(n) = 2*T(n/2) + O(n) => O(n log n)         *
 *  (Caso 2 del Teorema Maestro).                                      *
 * ================================================================== */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>

typedef struct { double x, y; } Punto;

/* ---------- utilidades ---------- */

static double dist(Punto a, Punto b) {
    double dx = a.x - b.x, dy = a.y - b.y;
    return sqrt(dx * dx + dy * dy);
}

/* Comparador para el ordenamiento inicial por coordenada X (una sola vez) */
static int cmp_x(const void *a, const void *b) {
    double d = ((const Punto *)a)->x - ((const Punto *)b)->x;
    return (d > 0) - (d < 0);
}

/* ------------------------------------------------------------------ *
 *  rec(): resuelve el subproblema P[ini..fin] y DEJA ese tramo       *
 *  ordenado por Y al regresar (vía merge). Devuelve la distancia     *
 *  mínima del tramo. 'aux' es buffer de trabajo del tamaño de P.     *
 * ------------------------------------------------------------------ */
static double rec(Punto P[], int ini, int fin, Punto aux[]) {
    int n = fin - ini + 1;

    /* ---- 1. CASO BASE: <= 3 puntos, fuerza bruta O(1) ---- */
    if (n <= 3) {
        double best = DBL_MAX;
        for (int i = ini; i <= fin; i++)
            for (int j = i + 1; j <= fin; j++) {
                double d = dist(P[i], P[j]);
                if (d < best) best = d;
            }
        /* Ordenar por Y este tramo chico (insertion sort, O(1) aquí) */
        for (int i = ini + 1; i <= fin; i++) {
            Punto key = P[i];
            int k = i - 1;
            while (k >= ini && P[k].y > key.y) { P[k + 1] = P[k]; k--; }
            P[k + 1] = key;
        }
        return best;
    }

    /* ---- 2. DIVIDIR: calcular línea vertical de corte x = x_corte (O(1)) ---- */
    int med = (ini + fin) / 2;
    double x_corte = P[med].x;

    /* ---- 3. CONQUISTAR: 2 subproblemas de tamaño n/2 (a = 2, b = 2) ---- */
    double dL = rec(P, ini, med, aux);
    double dR = rec(P, med + 1, fin, aux);
    double delta = dL < dR ? dL : dR;

    /* ---- 4. COMBINAR: Trabajo no recursivo f(n) = O(n) ---- */
    
    /* 4a. Fusión (Merge) por coordenada Y en O(n):
     * Ambas mitades ya vienen ordenadas por Y de sus respectivas llamadas */
    int i = ini, j = med + 1, k = ini;
    while (i <= med && j <= fin)
        aux[k++] = (P[i].y <= P[j].y) ? P[i++] : P[j++];
    while (i <= med)  aux[k++] = P[i++];
    while (j <= fin)  aux[k++] = P[j++];
    for (k = ini; k <= fin; k++) P[k] = aux[k];

    /* 4b. Filtrar puntos en la franja vertical de ancho 2*delta:
     * Solo los puntos con |x - x_corte| < delta pueden formar un par mejor */
    int m = 0;
    for (k = ini; k <= fin; k++)
        if (fabs(P[k].x - x_corte) < delta)
            aux[m++] = P[k];

    /* 4c. Comparar candidatos en la franja:
     * Por geometría de empaquetamiento, para cada punto aux[p] basta comparar
     * con los puntos sucesores cuya diferencia en Y sea < delta (a lo sumo 7)
     * por lo que este bucle se ejecuta en tiempo O(m) <= O(n). */
    for (int p = 0; p < m; p++)
        for (int q = p + 1; q < m && (aux[q].y - aux[p].y) < delta; q++) {
            double d = dist(aux[p], aux[q]);
            if (d < delta) delta = d;
        }

    return delta;
}

/* ------------------------------------------------------------------ *
 *  par_mas_cercano(): lanza la recursión.                            *
 *  - Costo de qsort inicial: O(n log n)                              *
 *  - Costo de rec(P, 0, n-1, aux): T(n) = 2*T(n/2) + O(n)            *
 *                                => Theta(n log n)                   *
 *  - Costo total: O(n log n) + Theta(n log n) = Theta(n log n).      *
 *  - Espacio auxiliar: O(n) para el arreglo aux.                     *
 * ------------------------------------------------------------------ */
double par_mas_cercano(Punto P[], int n) {
    if (n < 2) return DBL_MAX;
    
    /* 1. Preprocesamiento: ordenar por X una sola vez => O(n log n) */
    qsort(P, n, sizeof(Punto), cmp_x);
    
    /* 2. Buffer auxiliar compartido para el merge por Y */
    Punto *aux = (Punto *) malloc(n * sizeof(Punto));
    if (!aux) return DBL_MAX;
    
    /* 3. Divide y vencerás => Theta(n log n) */
    double r = rec(P, 0, n - 1, aux);
    
    free(aux);
    return r;
}

/* ---------------------------- prueba ---------------------------- *
 *  RESPUESTAS A LAS INSTRUCCIONES:                                 *
 *                                                                  *
 *  1. Complejidad de la función rec:                               *
 *     - Recurrencia: T(n) = 2*T(n/2) + f(n)                         *
 *     - f(n) = O(n) por la fusión tipo merge y el barrido de franja *
 *     - Parámetros: a = 2, b = 2, c_crit = log_2(2) = 1             *
 *     - f(n) = Theta(n^1) = Theta(n^c_crit)                         *
 *     - Por Caso 2 del Teorema Maestro (k = 0):                     *
 *       T(n) = Theta(n^(log_b a) * log n) = Theta(n log n).         *
 *                                                                  *
 *  2. Componentes de Divide y Vencerás:                            *
 *     - Caso base:  n <= 3, fuerza bruta y ordenamiento en O(1).   *
 *     - Dividir:    recta vertical x = P[med].x en O(1).           *
 *     - Conquistar: 2 llamadas recursivas en mitades de n/2 puntos.*
 *     - Combinar:   merge por Y + franja 2*delta + vecinos (O(n)). *
 *                                                                  *
 *  3. Distancia mínima esperada en el main:                        *
 *     - Entre pts[0]=(2.0, 3.0) y pts[5]=(3.0, 4.0):              *
 *       dist = sqrt((3-2)^2 + (4-3)^2) = sqrt(2) ≈ 1.4142.         *
 * ------------------------------------------------------------------ */
int main(void) {
    Punto pts[] = {
        {2.0, 3.0}, {12.0, 30.0}, {40.0, 50.0}, {5.0, 1.0},
        {12.0, 10.0}, {3.0, 4.0}
    };
    int n = sizeof(pts) / sizeof(pts[0]);

    printf("=== Par de Puntos más Cercanos (Divide y Vencerás) ===\n");
    printf("Conjunto de puntos (n = %d):\n", n);
    for (int i = 0; i < n; i++) {
        printf("  P%d = (%.1f, %.1f)\n", i, pts[i].x, pts[i].y);
    }

    double d = par_mas_cercano(pts, n);
    printf("\nDistancia mínima calculada: %.4f\n", d);
    printf("Distancia mínima esperada:   1.4142 (entre (2.0, 3.0) y (3.0, 4.0), sqrt(2))\n");
    return 0;
}
