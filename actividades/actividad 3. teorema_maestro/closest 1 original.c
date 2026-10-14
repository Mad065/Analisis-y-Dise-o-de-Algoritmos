/* ================================================================== *
 *  PAR DE PUNTOS MÁS CERCANOS  —  Divide y Vencerás                   *
 *                                                                     *
 *                                                                     *
 *  Clave para que sea eficiente la combinación                        *
 *  los puntos se mantienen ORDENADOS POR Y a través de la recursión   *
 *  mediante una fusion tipo merge, en vez de reordenar en cada nivel. *
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

/* comparador para el ordenamiento inicial por X (una sola vez) */
static int cmp_x(const void *a, const void *b) {
    double d = ((const Punto *)a)->x - ((const Punto *)b)->x;
    return (d > 0) - (d < 0);
}

/* ------------------------------------------------------------------ *
 *  rec(): resuelve el subproblema P[ini..fin] y DEJA ese tramo       *
 *  ordenado por Y al regresar (via merge). Devuelve la distancia     *
 *  mínima del tramo. 'aux' es buffer de trabajo del tamaño de P.     *
 * ------------------------------------------------------------------ */
static double rec(Punto P[], int ini, int fin, Punto aux[]) {
    int n = fin - ini + 1;

    /* ---- CASO BASE: <= 3 puntos, fuerza bruta O(1) ---- */
    if (n <= 3) {
        double best = DBL_MAX;
        for (int i = ini; i <= fin; i++)
            for (int j = i + 1; j <= fin; j++) {
                double d = dist(P[i], P[j]);
                if (d < best) best = d;
            }
        /* ordenar por Y este tramo chico (insertion sort, O(1) aquí) */
        for (int i = ini + 1; i <= fin; i++) {
            Punto key = P[i];
            int k = i - 1;
            while (k >= ini && P[k].y > key.y) { P[k + 1] = P[k]; k--; }
            P[k + 1] = key;
        }
        return best;
    }

    /* ----
     *
     *
     */
    int med = (ini + fin) / 2;
    double x_corte = P[med].x;


    double dL = rec(P, ini, med, aux);
    double dR = rec(P, med + 1, fin, aux);
    double delta = dL < dR ? dL : dR;


    int i = ini, j = med + 1, k = ini;
    while (i <= med && j <= fin)
        aux[k++] = (P[i].y <= P[j].y) ? P[i++] : P[j++];
    while (i <= med)  aux[k++] = P[i++];
    while (j <= fin)  aux[k++] = P[j++];
    for (k = ini; k <= fin; k++) P[k] = aux[k];


    int m = 0;
    for (k = ini; k <= fin; k++)
        if (fabs(P[k].x - x_corte) < delta)
            aux[m++] = P[k];


    for (int p = 0; p < m; p++)
        for (int q = p + 1; q < m && (aux[q].y - aux[p].y) < delta; q++) {
            double d = dist(aux[p], aux[q]);
            if (d < delta) delta = d;
        }

    return delta;
}

/* ------------------------------------------------------------------ *
 *  par_mas_cercano():                                                *
 *  lanza la recursion. El costo total ?                               *
 * ------------------------------------------------------------------ */
double par_mas_cercano(Punto P[], int n) {
    if (n < 2) return DBL_MAX;
    qsort(P, n, sizeof(Punto), cmp_x);         /* Costo? */
    Punto *aux = (Punto *) malloc(n * sizeof(Punto));
    if (!aux) return DBL_MAX;
    double r = rec(P, 0, n - 1, aux);          /* Complejidad?  */
    free(aux);
    return r;
}

/* ---------------------------- prueba ----------------------------
 *
 * Instrucciones:
 * Determina la complejidad de la función rec
 * Determina los componentes de divide y vencerás.
 *
 */
int main(void) {
    Punto pts[] = {
        {2.0, 3.0}, {12.0, 30.0}, {40.0, 50.0}, {5.0, 1.0},
        {12.0, 10.0}, {3.0, 4.0}
    };
    int n = sizeof(pts) / sizeof(pts[0]);

    double d = par_mas_cercano(pts, n);
    printf("Distancia minima: %.4f\n", d);   /* esperado: ? */
    return 0;
}
