import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryPoolMXBean;
import java.lang.management.MemoryType;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.Arrays;
import java.util.Locale;
import java.util.Random;

/**
 * Práctica 2 — Algoritmos de Ordenamiento (Java).
 *
 * <pre>
 *   1. Bubble Sort      O(n²)          espacio extra O(1)
 *   2. Merge Sort       O(n log n)     espacio extra O(n)
 *   3. Tree Sort        O(n log n)*    espacio extra O(nodos)
 *   4. Heap Sort        O(n log n)     espacio extra O(1)
 *   5. Counting Sort    O(n + k)       espacio extra O(n + k)
 * </pre>
 *
 * Todos los algoritmos ordenan IN-PLACE un {@code double[]} (tipos primitivos,
 * sin boxing).
 *
 * Uso:
 * <pre>
 *   java -Xmx6g Ordenamiento --algoritmo merge --n 1000000   (corrida de benchmark)
 *   java Ordenamiento --test                                 (autoprueba)
 * </pre>
 */
public class Ordenamiento {

    /** Counting Sort sobre reales: precisión fija de 2 decimales. */
    static final int ESCALA_COUNTING = 100;

    // =====================================================================
    // 1. BUBBLE SORT
    // =====================================================================
    /**
     * Bubble Sort optimizado: tras cada pasada el límite se reduce a la
     * posición del último intercambio; si no hubo intercambios, termina.
     */
    static void bubbleSort(double[] a) {
        int limite = a.length - 1;
        while (limite > 0) {
            int ultimo = 0;
            for (int j = 0; j < limite; j++) {
                if (a[j] > a[j + 1]) {
                    double t = a[j];
                    a[j] = a[j + 1];
                    a[j + 1] = t;
                    ultimo = j;
                }
            }
            limite = ultimo;
        }
    }

    // =====================================================================
    // 2. MERGE SORT
    // =====================================================================
    /** Merge Sort top-down con un único buffer auxiliar preasignado. */
    static void mergeSort(double[] a) {
        if (a.length < 2) return;
        double[] aux = new double[a.length];
        mergeSort(a, aux, 0, a.length);
    }

    /** Ordena a[lo, hi) (intervalo semiabierto). */
    private static void mergeSort(double[] a, double[] aux, int lo, int hi) {
        if (hi - lo < 2) return;
        int mid = (lo + hi) >>> 1;
        mergeSort(a, aux, lo, mid);
        mergeSort(a, aux, mid, hi);
        System.arraycopy(a, lo, aux, lo, hi - lo);
        int i = lo, j = mid, k = lo;
        while (i < mid && j < hi) {
            if (aux[j] < aux[i]) a[k++] = aux[j++];   // '<' estricto => estable
            else a[k++] = aux[i++];
        }
        if (i < mid) System.arraycopy(aux, i, a, k, mid - i);
        // el resto de la mitad derecha ya está en su lugar
    }

    // =====================================================================
    // 3. TREE SORT
    // =====================================================================
    /**
     * Tree Sort con un Árbol Binario de Búsqueda. Los nodos se guardan en
     * arreglos paralelos (clave, izq, der, cuenta); los repetidos incrementan
     * el contador del nodo. Inserción y recorrido in-order iterativos.
     */
    static void treeSort(double[] a) {
        int n = a.length;
        if (n < 2) return;
        int cap = Math.min(n, 1024);
        double[] clave = new double[cap];
        int[] izq = new int[cap], der = new int[cap], cuenta = new int[cap];
        clave[0] = a[0]; izq[0] = -1; der[0] = -1; cuenta[0] = 1;
        int total = 1;

        // --- Construcción del BST ---
        for (int idx = 1; idx < n; idx++) {
            double x = a[idx];
            int nodo = 0;
            while (true) {
                double c = clave[nodo];
                if (x < c) {
                    if (izq[nodo] < 0) { izq[nodo] = total; break; }
                    nodo = izq[nodo];
                } else if (x > c) {
                    if (der[nodo] < 0) { der[nodo] = total; break; }
                    nodo = der[nodo];
                } else {                      // valor repetido
                    cuenta[nodo]++;
                    nodo = -1;
                    break;
                }
            }
            if (nodo >= 0) {                  // se crea un nodo nuevo
                if (total == clave.length) {  // crecimiento x2 (amortizado O(1))
                    int nc = (int) Math.min((long) clave.length * 2, n);
                    clave = Arrays.copyOf(clave, nc);
                    izq = Arrays.copyOf(izq, nc);
                    der = Arrays.copyOf(der, nc);
                    cuenta = Arrays.copyOf(cuenta, nc);
                }
                clave[total] = x; izq[total] = -1; der[total] = -1; cuenta[total] = 1;
                total++;
            }
        }

        // --- Recorrido in-order con pila explícita ---
        int[] pila = new int[64];
        int tope = 0, nodo = 0, k = 0;
        while (tope > 0 || nodo >= 0) {
            while (nodo >= 0) {
                if (tope == pila.length) pila = Arrays.copyOf(pila, pila.length * 2);
                pila[tope++] = nodo;
                nodo = izq[nodo];
            }
            nodo = pila[--tope];
            double c = clave[nodo];
            for (int r = cuenta[nodo]; r > 0; r--) a[k++] = c;
            nodo = der[nodo];
        }
    }

    // =====================================================================
    // 4. HEAP SORT
    // =====================================================================
    /** Hunde a[i] dentro del max-heap a[0, n). */
    private static void siftDown(double[] a, int i, int n) {
        double x = a[i];
        while (true) {
            int hijo = 2 * i + 1;
            if (hijo >= n) break;
            if (hijo + 1 < n && a[hijo + 1] > a[hijo]) hijo++;
            if (a[hijo] <= x) break;
            a[i] = a[hijo];
            i = hijo;
        }
        a[i] = x;
    }

    /** Heap Sort in-place: construcción bottom-up del max-heap + extracciones. */
    static void heapSort(double[] a) {
        int n = a.length;
        for (int i = n / 2 - 1; i >= 0; i--) siftDown(a, i, n);
        for (int fin = n - 1; fin > 0; fin--) {
            double t = a[0]; a[0] = a[fin]; a[fin] = t;
            siftDown(a, 0, fin);
        }
    }

    // =====================================================================
    // 5. COUNTING SORT
    // =====================================================================
    /**
     * Counting Sort estable (CLRS) para reales con precisión fija: clave =
     * round(x * 100) - claveMin. Espacio extra O(n + k).
     */
    static void countingSort(double[] a) {
        int n = a.length;
        if (n < 2) return;
        double mn = a[0], mx = a[0];
        for (double x : a) { if (x < mn) mn = x; if (x > mx) mx = x; }
        long kmin = Math.round(mn * ESCALA_COUNTING);
        int k = (int) (Math.round(mx * ESCALA_COUNTING) - kmin + 1);
        int[] cuenta = new int[k];

        // 1) Contar ocurrencias
        for (double x : a) cuenta[(int) (Math.round(x * ESCALA_COUNTING) - kmin)]++;

        // 2) Sumas prefijas -> posición inicial de cada clave
        int total = 0;
        for (int i = 0; i < k; i++) { int c = cuenta[i]; cuenta[i] = total; total += c; }

        // 3) Colocar cada elemento (recorrido hacia adelante => estable)
        double[] salida = new double[n];
        for (double x : a) salida[cuenta[(int) (Math.round(x * ESCALA_COUNTING) - kmin)]++] = x;

        // 4) Copiar de regreso
        System.arraycopy(salida, 0, a, 0, n);
    }

    // =====================================================================
    // Despachador
    // =====================================================================
    static void ordenar(String algoritmo, double[] a) {
        switch (algoritmo) {
            case "bubble":   bubbleSort(a);   break;
            case "merge":    mergeSort(a);    break;
            case "tree":     treeSort(a);     break;
            case "heap":     heapSort(a);     break;
            case "counting": countingSort(a); break;
            default: throw new IllegalArgumentException("Algoritmo desconocido: " + algoritmo);
        }
    }

    static final String[] ALGORITMOS = {"bubble", "merge", "tree", "heap", "counting"};

    // =====================================================================
    // Utilidades de benchmark
    // =====================================================================
    static double[] cargarDataset(int n) throws IOException {
        Path ruta = Paths.get("datos", "n_" + n + ".bin");
        double[] a = new double[n];
        try (FileChannel ch = FileChannel.open(ruta, StandardOpenOption.READ)) {
            ByteBuffer buf = ByteBuffer.allocateDirect(8 << 20).order(ByteOrder.LITTLE_ENDIAN);
            int pos = 0;
            while (pos < n) {
                buf.clear();
                int bytes = (int) Math.min(buf.capacity(), (long) (n - pos) * 8);
                buf.limit(bytes);
                while (buf.hasRemaining()) {
                    if (ch.read(buf) < 0) throw new IOException("Archivo incompleto: " + ruta);
                }
                buf.flip();
                int m = bytes / 8;
                buf.asDoubleBuffer().get(a, pos, m);
                pos += m;
            }
        }
        return a;
    }

    static long sumaClaves(double[] a) {
        long s = 0;
        for (double x : a) s += Math.round(x * ESCALA_COUNTING);
        return s;
    }

    static boolean estaOrdenado(double[] a) {
        for (int i = 1; i < a.length; i++) if (a[i - 1] > a[i]) return false;
        return true;
    }

    static double[] aleatorio2Decimales(Random rng, int n, int lo, int hi) {
        double[] a = new double[n];
        for (int i = 0; i < n; i++) a[i] = (lo + rng.nextInt(hi - lo)) / 100.0;
        return a;
    }

    static long heapUsado() {
        long s = 0;
        for (MemoryPoolMXBean p : ManagementFactory.getMemoryPoolMXBeans())
            if (p.getType() == MemoryType.HEAP) s += p.getUsage().getUsed();
        return s;
    }

    static long heapPico() {
        long s = 0;
        for (MemoryPoolMXBean p : ManagementFactory.getMemoryPoolMXBeans())
            if (p.getType() == MemoryType.HEAP) s += p.getPeakUsage().getUsed();
        return s;
    }

    static void reiniciarPicos() {
        for (MemoryPoolMXBean p : ManagementFactory.getMemoryPoolMXBeans())
            if (p.getType() == MemoryType.HEAP) p.resetPeakUsage();
    }

    static void gcCompleto() {
        for (int i = 0; i < 3; i++) {
            System.gc();
            try { Thread.sleep(50); } catch (InterruptedException ignored) { }
        }
    }

    /** Calienta el JIT ejecutando el algoritmo sobre arreglos pequeños. */
    static void calentar(String algoritmo) {
        Random rng = new Random(7);
        int m = algoritmo.equals("bubble") ? 2_000 : 20_000;
        for (int r = 0; r < 10; r++) ordenar(algoritmo, aleatorio2Decimales(rng, m, 0, 1_000_000));
    }

    /** Bytes asignados en el heap por el hilo actual (contador exacto de la JVM). */
    static long bytesAsignadosHilo() {
        return ((com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean())
            .getThreadAllocatedBytes(Thread.currentThread().threadId());
    }

    static void correr(String algoritmo, int n) throws IOException {
        double[] a = cargarDataset(n);
        long sumaAntes = sumaClaves(a);
        calentar(algoritmo);
        gcCompleto();
        long base = heapUsado();
        reiniciarPicos();
        long asignadosAntes = bytesAsignadosHilo();

        long t0 = System.nanoTime();
        ordenar(algoritmo, a);
        long t1 = System.nanoTime();

        long asignados = bytesAsignadosHilo() - asignadosAntes;
        long pico = heapPico();
        boolean ok = a.length == n && estaOrdenado(a) && sumaClaves(a) == sumaAntes;
        double mb = 1024.0 * 1024.0;
        // mem_extra_mb: memoria que el algoritmo pidió al heap durante el ordenamiento.
        // heap_pico_delta_mb: crecimiento del pico del heap (resolución = tamaño de región G1).
        System.out.println(String.format(Locale.ROOT,
            "RESULTADO {\"lenguaje\": \"java\", \"algoritmo\": \"%s\", \"n\": %d, \"tiempo_s\": %.9f, "
                + "\"mem_base_mb\": %.3f, \"mem_pico_mb\": %.3f, \"mem_extra_mb\": %.3f, "
                + "\"heap_pico_delta_mb\": %.3f, \"verificado\": %s}",
            algoritmo, n, (t1 - t0) / 1e9, base / mb, pico / mb, asignados / mb,
            Math.max(0, pico - base) / mb, ok));
    }

    // =====================================================================
    // Autoprueba
    // =====================================================================
    static int fallos = 0;

    static void probar(String caso, double[] datos, String... algoritmos) {
        double[] esperado = datos.clone();
        Arrays.sort(esperado);
        for (String alg : algoritmos) {
            double[] a = datos.clone();
            ordenar(alg, a);
            boolean ok = Arrays.equals(a, esperado);
            if (!ok) fallos++;
            System.out.printf("  %-6s %-10s %-32s n=%d%n", ok ? "OK" : "FALLO", alg, caso, datos.length);
        }
    }

    static void autoprueba() {
        Random rng = new Random(1);
        double[] orden = new double[1000], inverso = new double[1000], iguales = new double[500];
        for (int i = 0; i < 1000; i++) { orden[i] = i / 100.0; inverso[i] = (1000 - i) / 100.0; }
        Arrays.fill(iguales, 7.77);
        double[] dup = new double[2000];
        for (int i = 0; i < dup.length; i++) dup[i] = rng.nextInt(20) / 100.0;
        double[] reales = new double[3000];
        for (int i = 0; i < reales.length; i++) reales[i] = (rng.nextDouble() * 2 - 1) * 1e6;

        probar("vacio", new double[0], ALGORITMOS);
        probar("un elemento", new double[]{3.14}, ALGORITMOS);
        probar("dos elementos", new double[]{2.5, 1.25}, ALGORITMOS);
        probar("ya ordenado", orden, ALGORITMOS);
        probar("orden inverso", inverso, ALGORITMOS);
        probar("todos iguales", iguales, ALGORITMOS);
        probar("con duplicados", dup, ALGORITMOS);
        probar("negativos", aleatorio2Decimales(rng, 1000, -100_000, 0), ALGORITMOS);
        probar("aleatorio 5000", aleatorio2Decimales(rng, 5000, -50_000, 50_000), ALGORITMOS);
        probar("rango dataset [0,10000)", aleatorio2Decimales(rng, 3000, 0, 1_000_000), ALGORITMOS);
        probar("reales precision completa", reales, "bubble", "merge", "tree", "heap");

        System.out.println(fallos == 0 ? "\nTODAS LAS PRUEBAS PASARON" : "\n" + fallos + " PRUEBAS FALLARON");
        if (fallos > 0) System.exit(1);
    }

    public static void main(String[] args) throws IOException {
        String algoritmo = null;
        int n = -1;
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--test": autoprueba(); return;
                case "--algoritmo": algoritmo = args[++i]; break;
                case "--n": n = Integer.parseInt(args[++i]); break;
                default: throw new IllegalArgumentException("Argumento desconocido: " + args[i]);
            }
        }
        if (algoritmo == null || n < 0) {
            System.err.println("Uso: java Ordenamiento --algoritmo <bubble|merge|tree|heap|counting> --n <N> | --test");
            System.exit(2);
        }
        correr(algoritmo, n);
    }
}
