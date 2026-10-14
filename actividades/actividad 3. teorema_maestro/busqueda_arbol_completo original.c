/* ================================================================== *
 *  BÚSQUEDA EN UN ÁRBOL BINARIO COMPLETO  —  Divide y Vencerás        *
 *                                                                     *
 *  El arbol NO es de busqueda (no esta ordenado), asi que para        *
 *  hallar un valor hay que explorar AMBOS subarboles. Esto da el      *
 *  caso de divide y venceras con dos ramas.                           *
 *                                                                     *
 *                                                                     *
 *  El arbol se guarda en un ARREGLO (representacion de monticulo):    *
 *  para el nodo en el indice i,                                       *
 *      hijo izquierdo  = 2*i + 1                                      *
 *      hijo derecho    = 2*i + 2                                      *
 *  En un arbol COMPLETO de n nodos no hay huecos: indices 0..n-1.     *
 *  Esto garantiza que cada subarbol tiene ~n/2 nodos  => b = 2.       *
 * ================================================================== */

#include <stdio.h>
#include <stdbool.h>

/* ------------------------------------------------------------------ *
 *  buscar(): devuelve el indice donde aparece 'objetivo' dentro del   *
 *  subarbol con raiz en 'i', o -1 si no esta. Explora las DOS ramas.  *
 * ------------------------------------------------------------------ */
int buscar(int arbol[], int n, int i, int objetivo) {

    /* ---- CASO BASE: el indice cae fuera del arbol (subarbol vacio) */
    if (i >= n)
        return -1;

    /* ---- trabajo no recursivo: una comparacion  =>  f(n) = O(1) ---- */
    if (arbol[i] == objetivo)
        return i;


    int izq = buscar(arbol, n, 2 * i + 1, objetivo);
    if (izq != -1)
        return izq;

    int der = buscar(arbol, n, 2 * i + 2, objetivo);
    return der;
}



/* ---------------------------- prueba ---------------------------- */
int main(void) {
    /* Arbol binario completo de 7 nodos (no ordenado):
     *                 50
     *               /    \
     *             30      70
     *            /  \    /  \
     *          10   40  60   20
     * Indices:  0:50 1:30 2:70 3:10 4:40 5:60 6:20
     *    Instrucciones:
     *    ¿Cuál es la complejidad de buscar si el árbol no está ordenado?
     *    ¿Cómo se podría reducir la complejidad de este algoritmo?
     *    Ubica los componentes de divide y vencerás en la función buscar
     */
    int arbol[] = {50, 30, 70, 10, 40, 60, 20};
    int n = sizeof(arbol) / sizeof(arbol[0]);

    int objetivos[] = {60, 40, 99};
    for (int k = 0; k < 3; k++) {
        int pos = buscar(arbol, n, 0, objetivos[k]);
        if (pos != -1)
            printf("Valor %d encontrado en el indice %d\n", objetivos[k], pos);
        else
            printf("Valor %d no esta en el arbol\n", objetivos[k]);
    }
    return 0;
}
