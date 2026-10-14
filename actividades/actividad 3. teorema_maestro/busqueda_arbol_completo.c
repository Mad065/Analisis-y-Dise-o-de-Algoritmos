/* ================================================================== *
 *  BÚSQUEDA EN UN ÁRBOL BINARIO COMPLETO  —  Divide y Vencerás        *
 *                                                                     *
 *  El árbol NO es de búsqueda (no está ordenado), así que para        *
 *  hallar un valor hay que explorar AMBOS subárboles. Esto da el      *
 *  caso de divide y vencerás con dos ramas:                           *
 *      T(n) = 2*T(n/2) + O(1)  =>  O(n) por Teorema Maestro (Caso 1)  *
 *                                                                     *
 *  El árbol se guarda en un ARREGLO (representación de montículo):    *
 *  para el nodo en el índice i,                                       *
 *      hijo izquierdo  = 2*i + 1                                      *
 *      hijo derecho    = 2*i + 2                                      *
 *  En un árbol COMPLETO de n nodos no hay huecos: índices 0..n-1.     *
 *  Esto garantiza que cada subárbol tiene ~n/2 nodos  => b = 2.       *
 * ================================================================== */

#include <stdio.h>
#include <stdbool.h>

/* ------------------------------------------------------------------ *
 *  buscar(): devuelve el índice donde aparece 'objetivo' dentro del   *
 *  subárbol con raíz en 'i', o -1 si no está.                         *
 *                                                                     *
 *  COMPONENTES DE DIVIDE Y VENCERÁS:                                  *
 *   1. Caso Base:     i >= n (nodo inexistente, retorna -1)          *
 *   2. Trabajo local: arbol[i] == objetivo  => f(n) = O(1)            *
 *   3. Dividir:       subproblemas en 2*i+1 y 2*i+2 (tamaño n/2)      *
 *   4. Conquistar:    llamadas recursivas en izq y der (a = 2)        *
 *   5. Combinar:      si izq != -1 retorna izq, si no der => O(1)     *
 * ------------------------------------------------------------------ */
int buscar(int arbol[], int n, int i, int objetivo) {

    /* ---- 1. CASO BASE: el índice cae fuera del árbol (subárbol vacío) */
    if (i >= n)
        return -1;

    /* ---- 2. TRABAJO LOCAL (no recursivo): comparación en raíz => f(n) = O(1) */
    if (arbol[i] == objetivo)
        return i;

    /* ---- 3 y 4. DIVIDIR Y CONQUISTAR: exploramos ambas ramas (a = 2, b = 2) */
    /* Subárbol izquierdo (tamaño n/2) */
    int izq = buscar(arbol, n, 2 * i + 1, objetivo);
    
    /* ---- 5. COMBINAR: si se encontró en la izquierda, propagamos el índice */
    if (izq != -1)
        return izq;

    /* Si no estuvo en la izquierda, exploramos subárbol derecho (tamaño n/2) */
    int der = buscar(arbol, n, 2 * i + 2, objetivo);
    return der;
}

/* ---------------------------- prueba ---------------------------- *
 *  RESPUESTAS A LAS INSTRUCCIONES:                                 *
 *                                                                  *
 *  1. ¿Cuál es la complejidad de buscar si el árbol no está ordenado?*
 *     - Recurrencia: T(n) = 2*T(n/2) + O(1)                         *
 *     - a = 2, b = 2, f(n) = O(1) = O(n^0)                         *
 *     - c_crit = log_b(a) = log_2(2) = 1                            *
 *     - Como f(n) = O(n^(1 - eps)) con eps = 1, aplica Caso 1 del   *
 *       Teorema Maestro: T(n) = Theta(n^(log_b a)) = Theta(n).       *
 *     - En el peor caso (elemento ausente o en la última hoja), se  *
 *       visitan los n nodos => Complejidad O(n).                     *
 *                                                                  *
 *  2. ¿Cómo se podría reducir la complejidad de este algoritmo?     *
 *     - Ordenar el árbol como Árbol Binario de Búsqueda (ABB/BST):   *
 *       izq < raiz < der permite descartar una rama completa en     *
 *       cada paso (a = 1, b = 2, f(n) = O(1)), dando O(log n).     *
 *     - Búsqueda binaria directa sobre el arreglo ordenado: O(log n)*
 *     - Tabla Hash: O(1) promedio de búsqueda con O(n) de espacio.  *
 *                                                                  *
 *  3. Componentes de Divide y Vencerás en buscar():                 *
 *     - Dividir:   hijo_izq = 2*i + 1, hijo_der = 2*i + 2 (O(1)).    *
 *     - Conquistar: 2 llamadas recursivas buscar(..., 2*i+1) y      *
 *                  buscar(..., 2*i+2) con subproblemas n/2.         *
 *     - Combinar:  retornar el índice si izq != -1, si no der (O(1))*
 * ------------------------------------------------------------------ */
int main(void) {
    /* Árbol binario completo de 7 nodos (no ordenado):
     *                 50 (i=0)
     *               /    \
     *        (i=1) 30     70 (i=2)
     *            /  \    /  \
     *          10   40  60   20
     *       (i=3) (i=4)(i=5) (i=6)
     *
     * Arreglo: [50, 30, 70, 10, 40, 60, 20]
     */
    int arbol[] = {50, 30, 70, 10, 40, 60, 20};
    int n = sizeof(arbol) / sizeof(arbol[0]);

    printf("=== Búsqueda en Árbol Binario Completo (No Ordenado) ===\n");
    printf("Estructura en arreglo (n = %d):\n", n);
    for (int i = 0; i < n; i++) {
        printf("  Índice %d -> Valor %d\n", i, arbol[i]);
    }
    printf("\nBúsquedas de prueba:\n");

    int objetivos[] = {60, 40, 99};
    for (int k = 0; k < 3; k++) {
        int pos = buscar(arbol, n, 0, objetivos[k]);
        if (pos != -1)
            printf("  ✓ Valor %d ENCONTRADO en el índice %d\n", objetivos[k], pos);
        else
            printf("  ✗ Valor %d NO ESTÁ en el árbol (resultado: -1)\n", objetivos[k]);
    }
    return 0;
}
