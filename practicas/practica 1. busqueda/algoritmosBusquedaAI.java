/**
 * ============================================================================
 * PRÁCTICA 1: ALGORITMOS DE BÚSQUEDA
 * Análisis y Diseño de Algoritmos - ESCOM IPN
 * ============================================================================
 *
 * Este programa implementa y compara cuatro algoritmos de búsqueda:
 *   1. Búsqueda Secuencial (Sequential Search / Linear Search)
 *   2. Búsqueda Binaria (Binary Search)
 *   3. Búsqueda por Interpolación (Interpolation Search)
 *   4. Búsqueda con Tabla Hash (Hash Table Search)
 *
 * Se generan datasets aleatorios de tamaños: 1K, 10K, 100K, 1M, 10M
 * Se evalúan cuatro escenarios para cada algoritmo:
 *   - Caso ideal (mejor caso específico para cada algoritmo)
 *   - Peor caso (peor caso específico para cada algoritmo)
 *   - Elemento no existente (el objetivo no está en el dataset)
 *   - Caso normal (búsqueda de un elemento en posición aleatoria)
 *
 * Se mide por separado:
 *   - El tiempo de ordenamiento (requerido por búsqueda binaria e interpolación)
 *   - El tiempo de construcción de la tabla hash
 *   - El tiempo de búsqueda para cada algoritmo en cada caso
 *
 * COMPILACIÓN Y EJECUCIÓN:
 *   javac algoritmosBusquedaAI.java
 *   java -Xmx4g algoritmosBusquedaAI
 *   (se recomienda -Xmx4g para datasets de 10M elementos)
 * ============================================================================
 */

import java.util.Arrays;   // Para Arrays.sort() (Dual-Pivot Quicksort)
import java.util.Random;    // Para generar números aleatorios
import java.util.ArrayList; // Para las cadenas de la tabla hash
import java.util.List;      // Interfaz List para la tabla hash

public class algoritmosBusquedaAI {

    // ========================================================================
    // CONSTANTES Y CONFIGURACIÓN
    // ========================================================================

    /** Tamaños de los datasets a evaluar */
    static final int[] TAMANIOS_DATASET = {1_000, 10_000, 100_000, 1_000_000, 10_000_000};

    /** Semilla para reproducibilidad de resultados */
    static final long SEMILLA_RANDOM = 42L;


    // ========================================================================
    // 1. BÚSQUEDA SECUENCIAL (Sequential Search / Linear Search)
    // ========================================================================
    // Complejidad temporal:
    //   - Mejor caso: O(1) — el elemento está en la primera posición
    //   - Peor caso:  O(n) — el elemento está al final o no existe
    //   - Caso promedio: O(n/2) ≈ O(n)
    // Complejidad espacial: O(1) — no requiere espacio adicional
    //
    // Funcionamiento:
    //   Recorre el arreglo de izquierda a derecha, comparando cada
    //   elemento con el objetivo hasta encontrarlo o llegar al final.
    //
    // Ventajas:
    //   - No requiere que los datos estén ordenados
    //   - Implementación muy simple
    //   - Sin costo de preprocesamiento
    //
    // Desventajas:
    //   - Ineficiente para grandes volúmenes de datos
    //   - Tiempo lineal O(n) en el peor caso
    // ========================================================================

    /**
     * Realiza una búsqueda secuencial (lineal) en el arreglo.
     *
     * Recorre el arreglo elemento por elemento desde el inicio hasta
     * encontrar el objetivo o llegar al final.
     *
     * @param arreglo  Arreglo de enteros donde buscar
     * @param objetivo Elemento a buscar
     * @return Índice del elemento si se encuentra, -1 si no existe
     */
    static int busquedaSecuencial(int[] arreglo, int objetivo) {
        // Recorremos cada posición del arreglo de izquierda a derecha
        for (int i = 0; i < arreglo.length; i++) {
            // Comparamos el elemento actual con el objetivo
            if (arreglo[i] == objetivo) {
                // ¡Encontrado! Retornamos el índice
                return i;
            }
        }
        // Si llegamos aquí, recorrimos TODO el arreglo sin encontrar el objetivo
        return -1;
    }


    // ========================================================================
    // 2. BÚSQUEDA BINARIA (Binary Search)
    // ========================================================================
    // PREREQUISITO: El arreglo DEBE estar ORDENADO de menor a mayor.
    //
    // Complejidad temporal:
    //   - Mejor caso: O(1) — el elemento está justo en el punto medio
    //   - Peor caso:  O(log₂ n) — elemento en un extremo o no existe
    //   - Caso promedio: O(log₂ n)
    // Complejidad espacial: O(1) — versión iterativa
    //
    // Funcionamiento:
    //   1. Se define un rango de búsqueda [izquierda, derecha]
    //   2. Se calcula el punto medio: medio = (izquierda + derecha) / 2
    //   3. Si arr[medio] == objetivo → encontrado
    //   4. Si arr[medio] > objetivo → buscar en mitad izquierda
    //   5. Si arr[medio] < objetivo → buscar en mitad derecha
    //   6. Repetir hasta encontrar o agotar el rango
    //
    // Ejemplo de eficiencia:
    //   n = 10,000,000 → log₂(10,000,000) ≈ 23 comparaciones
    //   ¡Solo 23 pasos para buscar entre 10 millones de elementos!
    //
    // Ventajas:
    //   - Extremadamente eficiente: O(log n)
    //   - Comportamiento predecible
    //
    // Desventajas:
    //   - REQUIERE datos ordenados (costo de ordenamiento: O(n log n))
    //   - No eficiente para datos que cambian frecuentemente
    // ========================================================================

    /**
     * Realiza una búsqueda binaria en un arreglo ORDENADO.
     *
     * Divide repetidamente el rango de búsqueda a la mitad,
     * comparando el elemento medio con el objetivo.
     *
     * @param arregloOrdenado Arreglo de enteros ORDENADO de menor a mayor
     * @param objetivo        Elemento a buscar
     * @return Índice del elemento si se encuentra, -1 si no existe
     */
    static int busquedaBinaria(int[] arregloOrdenado, int objetivo) {
        // Establecemos los límites iniciales del rango de búsqueda
        int izquierda = 0;                            // Límite inferior
        int derecha = arregloOrdenado.length - 1;     // Límite superior

        // Mientras el rango de búsqueda sea válido (no se haya agotado)
        while (izquierda <= derecha) {
            // Paso 1: Calcular el punto medio
            // Nota: Usamos esta fórmula en lugar de (izq + der) / 2
            // para evitar desbordamiento de enteros (integer overflow)
            // cuando izquierda + derecha > Integer.MAX_VALUE
            int medio = izquierda + (derecha - izquierda) / 2;

            // Paso 2: Comparar el elemento del medio con el objetivo

            // Caso A: ¡El elemento del medio ES el objetivo!
            if (arregloOrdenado[medio] == objetivo) {
                return medio;  // Retornamos su índice
            }

            // Caso B: El objetivo es MENOR → buscar en la MITAD IZQUIERDA
            if (arregloOrdenado[medio] > objetivo) {
                derecha = medio - 1;  // Descartamos la mitad derecha
            }
            // Caso C: El objetivo es MAYOR → buscar en la MITAD DERECHA
            else {
                izquierda = medio + 1;  // Descartamos la mitad izquierda
            }
        }

        // Si izquierda > derecha, el rango se agotó → no existe
        return -1;
    }


    // ========================================================================
    // 3. BÚSQUEDA POR INTERPOLACIÓN (Interpolation Search)
    // ========================================================================
    // PREREQUISITO: El arreglo DEBE estar ORDENADO. Funciona mejor con
    //               datos distribuidos de forma aproximadamente uniforme.
    //
    // Complejidad temporal:
    //   - Mejor caso: O(1) — la interpolación acierta directamente
    //   - Caso promedio: O(log log n) — con distribución uniforme
    //   - Peor caso: O(n) — con distribución muy desigual
    // Complejidad espacial: O(1)
    //
    // Fórmula de interpolación:
    //   pos = izq + ((objetivo - arr[izq]) × (der - izq)) / (arr[der] - arr[izq])
    //
    // Analogía:
    //   Cuando buscamos "zapato" en el diccionario, abrimos cerca del final.
    //   Si buscamos "avión", abrimos cerca del inicio. La búsqueda por
    //   interpolación estima DÓNDE debería estar el elemento basándose
    //   en su valor relativo dentro del rango.
    //
    // Comparación con búsqueda binaria:
    //   n = 10^7 → log₂(10^7) ≈ 23,  log₂(log₂(10^7)) ≈ 5
    //   ¡Interpolación puede ser ~5x más rápida con datos uniformes!
    //
    // Ventajas:
    //   - Más rápida que binaria con datos uniformemente distribuidos
    //   - O(log log n) << O(log n) para n grandes
    //
    // Desventajas:
    //   - Puede degradarse a O(n) con datos no uniformes
    //   - Requiere aritmética adicional por iteración
    //   - Requiere datos numéricos y ordenados
    // ========================================================================

    /**
     * Realiza una búsqueda por interpolación en un arreglo ORDENADO.
     *
     * Utiliza la distribución de los valores para estimar la posición
     * más probable del objetivo, como buscar una palabra en el diccionario.
     *
     * @param arregloOrdenado Arreglo de enteros ORDENADO
     * @param objetivo        Número a buscar
     * @return Índice del elemento si se encuentra, -1 si no existe
     */
    static int busquedaInterpolacion(int[] arregloOrdenado, int objetivo) {
        // Definimos los límites iniciales
        int izquierda = 0;
        int derecha = arregloOrdenado.length - 1;

        // Condiciones del bucle (más restrictivas que búsqueda binaria):
        // 1. izquierda <= derecha: rango válido
        // 2. objetivo >= arr[izquierda]: no menor que el mínimo del rango
        // 3. objetivo <= arr[derecha]: no mayor que el máximo del rango
        while (izquierda <= derecha &&
               objetivo >= arregloOrdenado[izquierda] &&
               objetivo <= arregloOrdenado[derecha]) {

            // Caso especial: si solo queda un elemento en el rango
            if (izquierda == derecha) {
                if (arregloOrdenado[izquierda] == objetivo) {
                    return izquierda;  // ¡Es el que buscamos!
                }
                return -1;  // No es el que buscamos
            }

            // ============================================================
            // Fórmula de interpolación lineal:
            //
            //                  (objetivo - arr[izq]) × (der - izq)
            // pos = izq + ─────────────────────────────────────────────
            //                      arr[der] - arr[izq]
            //
            // Desglose:
            // - (objetivo - arr[izq]) / (arr[der] - arr[izq]) =
            //   fracción proporcional de la distancia al objetivo
            // - Esa fracción × (der - izq) = desplazamiento estimado
            // - izq + desplazamiento = posición estimada
            //
            // NOTA: Usamos long para evitar desbordamiento en la
            // multiplicación de valores grandes
            // ============================================================
            long numerador = (long)(objetivo - arregloOrdenado[izquierda])
                           * (long)(derecha - izquierda);
            int denominador = arregloOrdenado[derecha] - arregloOrdenado[izquierda];
            int posicion = izquierda + (int)(numerador / denominador);

            // Verificamos si la posición estimada contiene el objetivo
            if (arregloOrdenado[posicion] == objetivo) {
                return posicion;  // ¡Encontrado en la posición interpolada!
            }

            // Si el valor es MENOR → buscar MÁS A LA DERECHA
            if (arregloOrdenado[posicion] < objetivo) {
                izquierda = posicion + 1;
            }
            // Si el valor es MAYOR → buscar MÁS A LA IZQUIERDA
            else {
                derecha = posicion - 1;
            }
        }

        // El objetivo está fuera del rango de valores → no existe
        return -1;
    }


    // ========================================================================
    // 4. TABLA HASH CON ENCADENAMIENTO SEPARADO
    // ========================================================================
    // Complejidad temporal:
    //   - Inserción: O(1) amortizado
    //   - Búsqueda mejor caso: O(1) — acceso directo, sin colisiones
    //   - Búsqueda caso promedio: O(1 + α) donde α = n/m (factor de carga)
    //   - Búsqueda peor caso: O(n) — todos los elementos en una cubeta
    // Complejidad espacial: O(n + m) donde m = tamaño de la tabla
    //
    // Funcionamiento:
    //   1. Aplicar función hash: h(clave) → índice de cubeta
    //   2. Almacenar/buscar en la lista de esa cubeta
    //   3. Colisiones se resuelven con encadenamiento (listas enlazadas)
    //
    // Ejemplo con tabla de tamaño 5 y hash(x) = x % 5:
    //   Insertar: 10, 15, 22, 7, 20
    //
    //   [0] → [10, 15, 20]  (10%5=0, 15%5=0, 20%5=0)
    //   [1] → []
    //   [2] → [22, 7]       (22%5=2, 7%5=2)
    //   [3] → []
    //   [4] → []
    //
    // Factor de carga (α = n/m):
    //   - α < 1: pocas colisiones, buen rendimiento
    //   - α ≈ 1: rendimiento aceptable
    //   - α > 1: muchas colisiones, rendimiento se degrada
    // ========================================================================

    /**
     * Implementación de una Tabla Hash con Encadenamiento Separado.
     *
     * Cada posición (cubeta/bucket) de la tabla almacena una lista de
     * elementos. Las colisiones se resuelven agregando elementos a la
     * lista de la cubeta correspondiente.
     */
    static class TablaHash {

        /** La tabla: arreglo de listas (cadenas para colisiones) */
        private List<List<Integer>> tabla;

        /** Tamaño de la tabla (número de cubetas) */
        private int tamanio;

        /** Número total de elementos almacenados */
        private int numElementos;

        /**
         * Constructor: inicializa la tabla hash.
         *
         * El tamaño se elige como el siguiente número primo mayor a
         * 1.3 veces la capacidad esperada para:
         * - Mantener un factor de carga α ≈ 0.77
         * - Reducir colisiones (tamaño primo mejora distribución)
         *
         * @param capacidadEsperada Número estimado de elementos a almacenar
         */
        TablaHash(int capacidadEsperada) {
            // Calculamos el tamaño como siguiente primo > 1.3 × capacidad
            this.tamanio = siguientePrimo((int)(capacidadEsperada * 1.3));

            // Creamos la tabla: lista de listas vacías
            this.tabla = new ArrayList<>(this.tamanio);
            for (int i = 0; i < this.tamanio; i++) {
                this.tabla.add(new ArrayList<>());
            }

            this.numElementos = 0;
        }

        /**
         * Verifica si un número es primo.
         * Optimizado: verifica solo hasta √n, usando 6k ± 1.
         */
        private static boolean esPrimo(int n) {
            if (n < 2) return false;
            if (n == 2 || n == 3) return true;
            if (n % 2 == 0 || n % 3 == 0) return false;
            // Todo primo > 3 tiene la forma 6k ± 1
            for (int i = 5; i * i <= n; i += 6) {
                if (n % i == 0 || n % (i + 2) == 0) return false;
            }
            return true;
        }

        /**
         * Encuentra el menor número primo mayor o igual a n.
         */
        private static int siguientePrimo(int n) {
            if (n <= 2) return 2;
            if (n % 2 == 0) n++;  // Si es par, empezar con impar
            while (!esPrimo(n)) {
                n += 2;  // Solo verificar impares
            }
            return n;
        }

        /**
         * Función hash: calcula el índice de cubeta para una clave.
         * Usa el método de módulo: hash(clave) = clave mod tamaño.
         *
         * @param clave Clave numérica
         * @return Índice de cubeta (0 ≤ índice < tamaño)
         */
        private int funcionHash(int clave) {
            // Math.abs para manejar posibles valores negativos
            return Math.abs(clave % this.tamanio);
        }

        /**
         * Inserta una clave en la tabla hash.
         * Calcula hash → agrega a la cadena de esa cubeta.
         *
         * @param clave Valor a insertar
         */
        void insertar(int clave) {
            int indice = funcionHash(clave);
            this.tabla.get(indice).add(clave);
            this.numElementos++;
        }

        /**
         * Busca una clave en la tabla hash.
         * Calcula hash → busca secuencialmente en la cadena.
         *
         * @param clave Valor a buscar
         * @return Índice de la cubeta si se encuentra, -1 si no existe
         */
        int buscar(int clave) {
            int indice = funcionHash(clave);
            List<Integer> cadena = this.tabla.get(indice);
            // Búsqueda secuencial en la cadena (generalmente muy corta)
            for (int i = 0; i < cadena.size(); i++) {
                if (cadena.get(i) == clave) {
                    return indice;  // ¡Encontrado en esta cubeta!
                }
            }
            return -1;  // No encontrado
        }

        /** @return Tamaño de la tabla (número de cubetas) */
        int getTamanio() { return tamanio; }

        /** @return Número de elementos almacenados */
        int getNumElementos() { return numElementos; }

        /** @return Factor de carga α = n/m */
        double getFactorCarga() { return (double) numElementos / tamanio; }

        /** @return Longitud de la cadena más larga (máximas colisiones) */
        int getLongitudMaxCadena() {
            int max = 0;
            for (List<Integer> cadena : tabla) {
                if (cadena.size() > max) {
                    max = cadena.size();
                }
            }
            return max;
        }

        /** @return Número de cubetas que contienen al menos un elemento */
        int getCubetasOcupadas() {
            int count = 0;
            for (List<Integer> cadena : tabla) {
                if (!cadena.isEmpty()) {
                    count++;
                }
            }
            return count;
        }

        /**
         * Encuentra el elemento al final de la cadena más larga.
         * Útil para simular el peor caso de búsqueda.
         */
        int getElementoPeorCaso() {
            int maxLen = 0;
            int indiceCubetaMax = 0;
            for (int i = 0; i < tabla.size(); i++) {
                if (tabla.get(i).size() > maxLen) {
                    maxLen = tabla.get(i).size();
                    indiceCubetaMax = i;
                }
            }
            List<Integer> cubetaMax = tabla.get(indiceCubetaMax);
            // El último elemento de la cadena más larga = peor caso
            return cubetaMax.get(cubetaMax.size() - 1);
        }
    }


    // ========================================================================
    // FUNCIONES AUXILIARES
    // ========================================================================

    /**
     * Genera un dataset de números enteros aleatorios ÚNICOS.
     *
     * Usa un enfoque de "gaps aleatorios" que garantiza unicidad:
     * partiendo desde 0, suma incrementos aleatorios entre 1 y 9.
     * Luego mezcla el arreglo con Fisher-Yates shuffle.
     *
     * @param tamanio Cantidad de elementos a generar
     * @param semilla Semilla para reproducibilidad
     * @return Arreglo de enteros únicos sin ordenar
     */
    static int[] generarDataset(int tamanio, long semilla) {
        Random random = new Random(semilla);
        int[] dataset = new int[tamanio];

        // Generamos valores únicos con incrementos aleatorios
        // Cada valor es estrictamente mayor que el anterior
        // Los gaps aleatorios (1-9) dan distribución aproximadamente uniforme
        int valorActual = 0;
        for (int i = 0; i < tamanio; i++) {
            valorActual += random.nextInt(9) + 1;  // Incremento de 1 a 9
            dataset[i] = valorActual;
        }

        // Mezclamos el arreglo con el algoritmo de Fisher-Yates (Knuth shuffle)
        // Esto garantiza una permutación uniformemente aleatoria
        for (int i = tamanio - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);   // Índice aleatorio en [0, i]
            // Intercambiar dataset[i] y dataset[j]
            int temp = dataset[i];
            dataset[i] = dataset[j];
            dataset[j] = temp;
        }

        return dataset;
    }

    /**
     * Formatea un tiempo en nanosegundos a la unidad más legible.
     *
     * Escala automáticamente:
     * - < 1,000 ns → nanosegundos (ns)
     * - < 1,000,000 ns → microsegundos (us)
     * - < 1,000,000,000 ns → milisegundos (ms)
     * - ≥ 1,000,000,000 ns → segundos (s)
     *
     * @param nanosegundos Tiempo en nanosegundos
     * @return Tiempo formateado como String
     */
    static String formatearTiempo(long nanosegundos) {
        if (nanosegundos < 1_000L) {
            return String.format("%d ns", nanosegundos);
        } else if (nanosegundos < 1_000_000L) {
            return String.format("%.2f us", nanosegundos / 1_000.0);
        } else if (nanosegundos < 1_000_000_000L) {
            return String.format("%.2f ms", nanosegundos / 1_000_000.0);
        } else {
            return String.format("%.4f s", nanosegundos / 1_000_000_000.0);
        }
    }

    /**
     * Formatea un número con separador de miles para legibilidad.
     *
     * @param n Número a formatear
     * @return String con formato de miles (ej: "1,000,000")
     */
    static String formatearNumero(int n) {
        return String.format("%,d", n);
    }


    // ========================================================================
    // FUNCIÓN PRINCIPAL: EJECUCIÓN DE BENCHMARKS
    // ========================================================================

    public static void main(String[] args) {

        // ==================================================================
        // Encabezado del programa
        // ==================================================================
        System.out.println("=".repeat(100));
        System.out.println("  PRACTICA 1: COMPARACION DE ALGORITMOS DE BUSQUEDA");
        System.out.println("  Analisis y Diseno de Algoritmos - ESCOM IPN");
        System.out.println("=".repeat(100));
        System.out.println();
        System.out.println("  Algoritmos implementados:");
        System.out.println("    1. Busqueda Secuencial       - O(n)");
        System.out.println("    2. Busqueda Binaria          - O(log n) [requiere ordenamiento previo]");
        System.out.println("    3. Busqueda por Interpolacion - O(log log n) promedio [requiere orden.]");
        System.out.println("    4. Tabla Hash                - O(1) promedio [requiere construccion]");
        System.out.println();

        // Construimos la cadena de tamaños para mostrar
        StringBuilder tamStr = new StringBuilder();
        for (int i = 0; i < TAMANIOS_DATASET.length; i++) {
            if (i > 0) tamStr.append(", ");
            tamStr.append(formatearNumero(TAMANIOS_DATASET[i]));
        }
        System.out.println("  Tamanios de dataset: " + tamStr);
        System.out.println("  Semilla aleatoria:  " + SEMILLA_RANDOM);
        System.out.println("  Java:               " + System.getProperty("java.version"));
        System.out.println();

        // Nombres para las tablas de resultados
        String[] nombresAlgoritmos = {"Secuencial", "Binaria", "Interpolacion", "Tabla Hash"};
        String[] nombresCasos = {"Mejor caso", "Peor caso", "No existe", "Caso normal"};

        // ==================================================================
        // Iteramos sobre cada tamaño de dataset
        // ==================================================================
        for (int tamanio : TAMANIOS_DATASET) {

            System.out.println();
            System.out.println("#".repeat(100));
            System.out.printf("#  DATASET: %,12d elementos%n", tamanio);
            System.out.println("#".repeat(100));

            // ==============================================================
            // PASO 1: Generar el dataset aleatorio
            // ==============================================================
            System.out.printf("%n  [1/4] Generando %,d numeros aleatorios unicos...%n", tamanio);
            long inicioGen = System.nanoTime();
            int[] dataset = generarDataset(tamanio, SEMILLA_RANDOM);
            long tiempoGeneracion = System.nanoTime() - inicioGen;
            System.out.println("        Completado en " + formatearTiempo(tiempoGeneracion));

            // ==============================================================
            // PASO 2: Ordenar una copia del dataset
            // (requerido para búsqueda binaria y por interpolación)
            // ==============================================================
            System.out.println();
            System.out.println("  [2/4] Ordenando dataset (necesario para busqueda binaria e interpolacion)...");

            // IMPORTANTE: Creamos una COPIA para no modificar el original
            // El dataset original (desordenado) se usa para búsqueda secuencial
            int[] datasetOrdenado = Arrays.copyOf(dataset, dataset.length);

            // Medimos el tiempo de ordenamiento
            // Java usa Dual-Pivot Quicksort para tipos primitivos: O(n log n)
            long inicioSort = System.nanoTime();
            Arrays.sort(datasetOrdenado);
            long tiempoOrdenamiento = System.nanoTime() - inicioSort;

            System.out.println("        Algoritmo: Dual-Pivot Quicksort (Java built-in)");
            System.out.println("        Complejidad: O(n log n) promedio");
            System.out.println("        >>> Tiempo de ordenamiento: " + formatearTiempo(tiempoOrdenamiento));

            // ==============================================================
            // PASO 3: Construir la tabla hash
            // ==============================================================
            System.out.println();
            System.out.println("  [3/4] Construyendo tabla hash con encadenamiento separado...");

            long inicioHashBuild = System.nanoTime();
            TablaHash tablaHash = new TablaHash(tamanio);
            for (int elemento : dataset) {
                tablaHash.insertar(elemento);
            }
            long tiempoConstruccionHash = System.nanoTime() - inicioHashBuild;

            // Estadísticas de la tabla hash
            double factorCarga = tablaHash.getFactorCarga();
            int cubetasOcupadas = tablaHash.getCubetasOcupadas();
            int longMaxCadena = tablaHash.getLongitudMaxCadena();
            double longPromedio = (cubetasOcupadas > 0) ?
                (double) tablaHash.getNumElementos() / cubetasOcupadas : 0;

            System.out.printf("        Tamanio de la tabla:       %,12d%n", tablaHash.getTamanio());
            System.out.printf("        Elementos insertados:      %,12d%n", tablaHash.getNumElementos());
            System.out.printf("        Factor de carga (n/m):     %12.4f%n", factorCarga);
            System.out.printf("        Cubetas ocupadas:          %,12d%n", cubetasOcupadas);
            System.out.printf("        Long. maxima de cadena:    %12d%n", longMaxCadena);
            System.out.printf("        Long. promedio de cadena:  %12.2f%n", longPromedio);
            System.out.println("        >>> Tiempo de construccion: " + formatearTiempo(tiempoConstruccionHash));

            // ==============================================================
            // PASO 4: Ejecutar búsquedas en los 4 casos de prueba
            // ==============================================================
            System.out.println();
            System.out.println("  [4/4] Ejecutando busquedas...");

            int n = dataset.length;

            // ---- Definir objetivos de búsqueda ----

            // CASO "NO EXISTE" (compartido):
            // Valor mayor al máximo, garantizado que no existe
            int maxValor = Integer.MIN_VALUE;
            for (int v : dataset) {
                if (v > maxValor) maxValor = v;
            }
            int objetivoNoExiste = maxValor + 100;

            // CASO "NORMAL" (compartido):
            // Elemento aleatorio del dataset
            Random rndNormal = new Random(tamanio);
            int indiceAleatorio = n / 4 + rndNormal.nextInt(n / 2);
            int objetivoNormal = dataset[indiceAleatorio];

            // MEJOR CASO por algoritmo:
            int objetivoMejorSeq = dataset[0];                        // Primer elem → 1 comparación
            int objetivoMejorBin = datasetOrdenado[n / 2];            // Elemento medio → 1 comparación
            int objetivoMejorInterp = datasetOrdenado[n / 2];         // Buena interpolación en datos uniformes
            int objetivoMejorHash = dataset[0];                       // Generalmente O(1)

            // PEOR CASO por algoritmo:
            int objetivoPeorSeq = dataset[n - 1];                     // Último elem → n comparaciones
            int objetivoPeorBin = datasetOrdenado[0];                 // Extremo → log₂(n) comparaciones
            int objetivoPeorInterp = datasetOrdenado[0];              // Extremo → muchos ajustes
            int objetivoPeorHash = tablaHash.getElementoPeorCaso();   // Cubeta más larga

            // ---- Ejecutar búsquedas y medir tiempos ----
            // Almacenamos los tiempos en una matriz:
            // tiempos[algoritmo][caso] = nanosegundos
            long[][] tiempos = new long[4][4];
            long inicio, fin;

            // --- BÚSQUEDA SECUENCIAL (opera sobre arreglo desordenado) ---

            // Mejor caso: primer elemento
            inicio = System.nanoTime();
            busquedaSecuencial(dataset, objetivoMejorSeq);
            fin = System.nanoTime();
            tiempos[0][0] = fin - inicio;

            // Peor caso: último elemento
            inicio = System.nanoTime();
            busquedaSecuencial(dataset, objetivoPeorSeq);
            fin = System.nanoTime();
            tiempos[0][1] = fin - inicio;

            // No existe
            inicio = System.nanoTime();
            busquedaSecuencial(dataset, objetivoNoExiste);
            fin = System.nanoTime();
            tiempos[0][2] = fin - inicio;

            // Caso normal
            inicio = System.nanoTime();
            busquedaSecuencial(dataset, objetivoNormal);
            fin = System.nanoTime();
            tiempos[0][3] = fin - inicio;

            // --- BÚSQUEDA BINARIA (opera sobre arreglo ordenado) ---

            // Mejor caso: elemento medio
            inicio = System.nanoTime();
            busquedaBinaria(datasetOrdenado, objetivoMejorBin);
            fin = System.nanoTime();
            tiempos[1][0] = fin - inicio;

            // Peor caso: primer elemento del ordenado
            inicio = System.nanoTime();
            busquedaBinaria(datasetOrdenado, objetivoPeorBin);
            fin = System.nanoTime();
            tiempos[1][1] = fin - inicio;

            // No existe
            inicio = System.nanoTime();
            busquedaBinaria(datasetOrdenado, objetivoNoExiste);
            fin = System.nanoTime();
            tiempos[1][2] = fin - inicio;

            // Caso normal
            inicio = System.nanoTime();
            busquedaBinaria(datasetOrdenado, objetivoNormal);
            fin = System.nanoTime();
            tiempos[1][3] = fin - inicio;

            // --- BÚSQUEDA POR INTERPOLACIÓN (opera sobre arreglo ordenado) ---

            // Mejor caso: elemento medio
            inicio = System.nanoTime();
            busquedaInterpolacion(datasetOrdenado, objetivoMejorInterp);
            fin = System.nanoTime();
            tiempos[2][0] = fin - inicio;

            // Peor caso: primer elemento del ordenado
            inicio = System.nanoTime();
            busquedaInterpolacion(datasetOrdenado, objetivoPeorInterp);
            fin = System.nanoTime();
            tiempos[2][1] = fin - inicio;

            // No existe
            inicio = System.nanoTime();
            busquedaInterpolacion(datasetOrdenado, objetivoNoExiste);
            fin = System.nanoTime();
            tiempos[2][2] = fin - inicio;

            // Caso normal
            inicio = System.nanoTime();
            busquedaInterpolacion(datasetOrdenado, objetivoNormal);
            fin = System.nanoTime();
            tiempos[2][3] = fin - inicio;

            // --- TABLA HASH ---

            // Mejor caso
            inicio = System.nanoTime();
            tablaHash.buscar(objetivoMejorHash);
            fin = System.nanoTime();
            tiempos[3][0] = fin - inicio;

            // Peor caso
            inicio = System.nanoTime();
            tablaHash.buscar(objetivoPeorHash);
            fin = System.nanoTime();
            tiempos[3][1] = fin - inicio;

            // No existe
            inicio = System.nanoTime();
            tablaHash.buscar(objetivoNoExiste);
            fin = System.nanoTime();
            tiempos[3][2] = fin - inicio;

            // Caso normal
            inicio = System.nanoTime();
            tablaHash.buscar(objetivoNormal);
            fin = System.nanoTime();
            tiempos[3][3] = fin - inicio;

            // ==============================================================
            // IMPRIMIR TABLA DE RESULTADOS DE BÚSQUEDA
            // ==============================================================
            int anchoAlgo = 18;
            int anchoCaso = 18;

            System.out.println();
            System.out.println("  +-- RESULTADOS DE BUSQUEDA (tiempos de busqueda solamente)");
            System.out.println("  |");

            // Separador de la tabla
            StringBuilder separador = new StringBuilder("  +");
            separador.append("-".repeat(anchoAlgo + 2));
            for (int c = 0; c < nombresCasos.length; c++) {
                separador.append("+");
                separador.append("-".repeat(anchoCaso + 2));
            }
            separador.append("+");
            System.out.println(separador);

            // Encabezado
            System.out.printf("  | %-" + anchoAlgo + "s ", "Algoritmo");
            for (String caso : nombresCasos) {
                System.out.printf("| %" + anchoCaso + "s ", caso);
            }
            System.out.println("|");
            System.out.println(separador);

            // Filas de datos
            for (int a = 0; a < nombresAlgoritmos.length; a++) {
                System.out.printf("  | %-" + anchoAlgo + "s ", nombresAlgoritmos[a]);
                for (int c = 0; c < nombresCasos.length; c++) {
                    System.out.printf("| %" + anchoCaso + "s ", formatearTiempo(tiempos[a][c]));
                }
                System.out.println("|");
            }
            System.out.println(separador);

            // ==============================================================
            // TABLA DE TIEMPOS DE PREPROCESAMIENTO
            // ==============================================================
            System.out.println();
            System.out.println("  +-- TIEMPOS DE PREPROCESAMIENTO");
            System.out.println("  |");
            String sep2 = "  +" + "-".repeat(40) + "+" + "-".repeat(22) + "+";
            System.out.println(sep2);
            System.out.printf("  | %-38s | %20s |%n", "Operacion", "Tiempo");
            System.out.println(sep2);
            System.out.printf("  | %-38s | %20s |%n", "Generacion del dataset",
                    formatearTiempo(tiempoGeneracion));
            System.out.printf("  | %-38s | %20s |%n", "Ordenamiento (Dual-Pivot Quicksort)",
                    formatearTiempo(tiempoOrdenamiento));
            System.out.printf("  | %-38s | %20s |%n", "Construccion tabla hash",
                    formatearTiempo(tiempoConstruccionHash));
            System.out.println(sep2);

            // ==============================================================
            // TABLA DE OBJETIVOS UTILIZADOS
            // ==============================================================
            System.out.println();
            System.out.println("  +-- OBJETIVOS DE BUSQUEDA UTILIZADOS POR CASO");
            System.out.println("  |");
            String sep3 = "  +" + "-".repeat(17) + "+" + "-".repeat(14) + "+"
                         + "-".repeat(14) + "+" + "-".repeat(16) + "+" + "-".repeat(14) + "+";
            System.out.println(sep3);
            System.out.printf("  | %-15s | %12s | %12s | %14s | %12s |%n",
                    "Caso", "Secuencial", "Binaria", "Interpolacion", "Tabla Hash");
            System.out.println(sep3);
            System.out.printf("  | %-15s | %,12d | %,12d | %,14d | %,12d |%n",
                    "Mejor caso", objetivoMejorSeq, objetivoMejorBin,
                    objetivoMejorInterp, objetivoMejorHash);
            System.out.printf("  | %-15s | %,12d | %,12d | %,14d | %,12d |%n",
                    "Peor caso", objetivoPeorSeq, objetivoPeorBin,
                    objetivoPeorInterp, objetivoPeorHash);
            System.out.printf("  | %-15s | %,12d | %,12d | %,14d | %,12d |%n",
                    "No existe", objetivoNoExiste, objetivoNoExiste,
                    objetivoNoExiste, objetivoNoExiste);
            System.out.printf("  | %-15s | %,12d | %,12d | %,14d | %,12d |%n",
                    "Caso normal", objetivoNormal, objetivoNormal,
                    objetivoNormal, objetivoNormal);
            System.out.println(sep3);
        }

        // ==================================================================
        // RESUMEN TEÓRICO DE COMPLEJIDADES
        // ==================================================================
        System.out.println();
        System.out.println();
        System.out.println("=".repeat(100));
        System.out.println("  RESUMEN TEORICO DE COMPLEJIDADES");
        System.out.println("=".repeat(100));
        System.out.println();
        String sepFinal = "  " + "-".repeat(94);
        System.out.printf("  %-20s | %14s | %14s | %14s | %12s | %10s%n",
                "Algoritmo", "Mejor", "Promedio", "Peor", "Espacio", "Ordenado?");
        System.out.println(sepFinal);
        System.out.printf("  %-20s | %14s | %14s | %14s | %12s | %10s%n",
                "Secuencial", "O(1)", "O(n)", "O(n)", "O(1)", "No");
        System.out.printf("  %-20s | %14s | %14s | %14s | %12s | %10s%n",
                "Binaria", "O(1)", "O(log n)", "O(log n)", "O(1)", "Si");
        System.out.printf("  %-20s | %14s | %14s | %14s | %12s | %10s%n",
                "Interpolacion", "O(1)", "O(log log n)", "O(n)", "O(1)", "Si");
        System.out.printf("  %-20s | %14s | %14s | %14s | %12s | %10s%n",
                "Tabla Hash", "O(1)", "O(1)", "O(n)", "O(n+m)", "No");
        System.out.println(sepFinal);
        System.out.println();
        System.out.println("  Notas importantes:");
        System.out.println("  * El costo de ordenamiento O(n log n) debe sumarse al tiempo de busqueda");
        System.out.println("    binaria e interpolacion si los datos NO estan previamente ordenados.");
        System.out.println("  * La tabla hash requiere O(n) de construccion antes de buscar.");
        System.out.println("  * Para UNA sola busqueda en datos no ordenados, la busqueda secuencial");
        System.out.println("    puede ser mas eficiente que binaria (se evita el costo de ordenar).");
        System.out.println("  * Para MULTIPLES busquedas, la tabla hash o la busqueda binaria son");
        System.out.println("    significativamente superiores a la busqueda secuencial.");
        System.out.println("  * La busqueda por interpolacion supera a la binaria solo cuando los datos");
        System.out.println("    estan distribuidos de forma aproximadamente uniforme.");
    }
}
