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
 * Práctica 3 — Divide y Vencerás (Java).
 *
 * <pre>
 * Parte 1 — Selección Rápida (Quickselect / Selección de Hoare):
 *   * quickselect32(int[] a, int k)    O(n) promedio, espacio extra O(1), enteros 32 bits
 *   * quickselect64(long[] a, int k)   O(n) promedio, espacio extra O(1), enteros 64 bits
 *
 * Parte 2 — Multiplicación de Matrices Cuadradas (n x n):
 *   * tradicional2D(int[][] A, int[][] B, int n)   O(n³)       Arreglo 2D (int[][])
 *   * tradicional1D(int[] A, int[] B, int n)       O(n³)       Arreglo 1D contiguo (int[])
 *   * strassen2D(int[][] A, int[][] B, int n)      O(n^2.807)  Arreglo 2D (int[][])
 *   * strassen1D(int[] A, int[] B, int n)          O(n^2.807)  Arreglo 1D contiguo (int[])
 * </pre>
 *
 * Uso:
 * <pre>
 *   java -Xmx6g DivideVenceras --problema quickselect --bits 32 --n 1000000
 *   java -Xmx6g DivideVenceras --problema matrices --variante strassen_1d --n 256
 *   java DivideVenceras --test
 * </pre>
 */
public class DivideVenceras {

    static final int RANGO_MAX_QS = 10_000_000;

    // =====================================================================
    // PARTE 1: QUICKSELECT (SELECCIÓN DE HOARE) — 32 BITS Y 64 BITS
    // =====================================================================

    /**
     * Quickselect (Selección de Hoare) sobre un arreglo de enteros de 32 bits.
     * Encuentra el elemento que ocuparía la posición k (1 <= k <= n) si el
     * arreglo estuviera ordenado de forma creciente.
     */
    static int quickselect32(int[] a, int k) {
        int n = a.length;
        if (k < 1 || k > n) {
            throw new IllegalArgumentException("k fuera de rango [1, " + n + "]: " + k);
        }
        int objetivo = k - 1;
        int lo = 0;
        int hi = n - 1;

        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            // Mediana de tres entre a[lo], a[mid], a[hi]
            if (a[mid] < a[lo]) { int t = a[lo]; a[lo] = a[mid]; a[mid] = t; }
            if (a[hi] < a[lo])  { int t = a[lo]; a[lo] = a[hi];  a[hi] = t;  }
            if (a[hi] < a[mid]) { int t = a[mid]; a[mid] = a[hi]; a[hi] = t; }
            int pivote = a[mid];

            int i = lo;
            int j = hi;
            while (i <= j) {
                while (a[i] < pivote) i++;
                while (a[j] > pivote) j--;
                if (i <= j) {
                    int t = a[i];
                    a[i] = a[j];
                    a[j] = t;
                    i++;
                    j--;
                }
            }

            if (objetivo <= j) {
                hi = j;
            } else if (objetivo >= i) {
                lo = i;
            } else {
                break;
            }
        }
        return a[objetivo];
    }

    /**
     * Quickselect (Selección de Hoare) sobre un arreglo de enteros de 64 bits.
     * Encuentra el elemento que ocuparía la posición k (1 <= k <= n) si el
     * arreglo estuviera ordenado de forma creciente.
     */
    static long quickselect64(long[] a, int k) {
        int n = a.length;
        if (k < 1 || k > n) {
            throw new IllegalArgumentException("k fuera de rango [1, " + n + "]: " + k);
        }
        int objetivo = k - 1;
        int lo = 0;
        int hi = n - 1;

        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            // Mediana de tres entre a[lo], a[mid], a[hi]
            if (a[mid] < a[lo]) { long t = a[lo]; a[lo] = a[mid]; a[mid] = t; }
            if (a[hi] < a[lo])  { long t = a[lo]; a[lo] = a[hi];  a[hi] = t;  }
            if (a[hi] < a[mid]) { long t = a[mid]; a[mid] = a[hi]; a[hi] = t; }
            long pivote = a[mid];

            int i = lo;
            int j = hi;
            while (i <= j) {
                while (a[i] < pivote) i++;
                while (a[j] > pivote) j--;
                if (i <= j) {
                    long t = a[i];
                    a[i] = a[j];
                    a[j] = t;
                    i++;
                    j--;
                }
            }

            if (objetivo <= j) {
                hi = j;
            } else if (objetivo >= i) {
                lo = i;
            } else {
                break;
            }
        }
        return a[objetivo];
    }

    // =====================================================================
    // PARTE 2: MULTIPLICACIÓN DE MATRICES (TRADICIONAL vs STRASSEN, 2D vs 1D)
    // =====================================================================

    /** Multiplicación clásica O(n³) usando arreglos bidimensionales (int[][]). */
    static int[][] tradicional2D(int[][] A, int[][] B, int n) {
        int[][] C = new int[n][n];
        for (int i = 0; i < n; i++) {
            int[] filaA = A[i];
            int[] filaC = C[i];
            for (int k = 0; k < n; k++) {
                int aik = filaA[k];
                int[] filaB = B[k];
                for (int j = 0; j < n; j++) {
                    filaC[j] += aik * filaB[j];
                }
            }
        }
        return C;
    }

    /** Multiplicación clásica O(n³) usando arreglos unidimensionales contiguos (int[]). */
    static int[] tradicional1D(int[] A, int[] B, int n) {
        int[] C = new int[n * n];
        for (int i = 0; i < n; i++) {
            int in = i * n;
            for (int k = 0; k < n; k++) {
                int aik = A[in + k];
                int kn = k * n;
                for (int j = 0; j < n; j++) {
                    C[in + j] += aik * B[kn + j];
                }
            }
        }
        return C;
    }

    private static int[][] sumar2D(int[][] A, int[][] B, int n) {
        int[][] R = new int[n][n];
        for (int i = 0; i < n; i++) {
            int[] ai = A[i], bi = B[i], ri = R[i];
            for (int j = 0; j < n; j++) {
                ri[j] = ai[j] + bi[j];
            }
        }
        return R;
    }

    private static int[][] restar2D(int[][] A, int[][] B, int n) {
        int[][] R = new int[n][n];
        for (int i = 0; i < n; i++) {
            int[] ai = A[i], bi = B[i], ri = R[i];
            for (int j = 0; j < n; j++) {
                ri[j] = ai[j] - bi[j];
            }
        }
        return R;
    }

    /** Algoritmo de Strassen O(n^log2(7)) ≈ O(n^2.807) con arreglos bidimensionales (int[][]). */
    static int[][] strassen2D(int[][] A, int[][] B, int n) {
        if (n == 1) {
            return new int[][]{{A[0][0] * B[0][0]}};
        }
        int m = n >>> 1;
        int[][] A11 = new int[m][m], A12 = new int[m][m], A21 = new int[m][m], A22 = new int[m][m];
        int[][] B11 = new int[m][m], B12 = new int[m][m], B21 = new int[m][m], B22 = new int[m][m];

        for (int i = 0; i < m; i++) {
            System.arraycopy(A[i], 0, A11[i], 0, m);
            System.arraycopy(A[i], m, A12[i], 0, m);
            System.arraycopy(A[i + m], 0, A21[i], 0, m);
            System.arraycopy(A[i + m], m, A22[i], 0, m);

            System.arraycopy(B[i], 0, B11[i], 0, m);
            System.arraycopy(B[i], m, B12[i], 0, m);
            System.arraycopy(B[i + m], 0, B21[i], 0, m);
            System.arraycopy(B[i + m], m, B22[i], 0, m);
        }

        int[][] M1 = strassen2D(sumar2D(A11, A22, m), sumar2D(B11, B22, m), m);
        int[][] M2 = strassen2D(sumar2D(A21, A22, m), B11, m);
        int[][] M3 = strassen2D(A11, restar2D(B12, B22, m), m);
        int[][] M4 = strassen2D(A22, restar2D(B21, B11, m), m);
        int[][] M5 = strassen2D(sumar2D(A11, A12, m), B22, m);
        int[][] M6 = strassen2D(restar2D(A21, A11, m), sumar2D(B11, B12, m), m);
        int[][] M7 = strassen2D(restar2D(A12, A22, m), sumar2D(B21, B22, m), m);

        int[][] C = new int[n][n];
        for (int i = 0; i < m; i++) {
            int[] cSup = C[i], cInf = C[i + m];
            int[] m1i = M1[i], m2i = M2[i], m3i = M3[i], m4i = M4[i];
            int[] m5i = M5[i], m6i = M6[i], m7i = M7[i];
            for (int j = 0; j < m; j++) {
                int v1 = m1i[j], v2 = m2i[j], v3 = m3i[j], v4 = m4i[j];
                int v5 = m5i[j], v6 = m6i[j], v7 = m7i[j];
                cSup[j]     = v1 + v4 - v5 + v7;
                cSup[j + m] = v3 + v5;
                cInf[j]     = v2 + v4;
                cInf[j + m] = v1 - v2 + v3 + v6;
            }
        }
        return C;
    }

    private static int[] sumar1D(int[] A, int[] B, int tam) {
        int[] R = new int[tam];
        for (int k = 0; k < tam; k++) {
            R[k] = A[k] + B[k];
        }
        return R;
    }

    private static int[] restar1D(int[] A, int[] B, int tam) {
        int[] R = new int[tam];
        for (int k = 0; k < tam; k++) {
            R[k] = A[k] - B[k];
        }
        return R;
    }

    /** Algoritmo de Strassen O(n^log2(7)) ≈ O(n^2.807) con arreglos 1D contiguos (int[]). */
    static int[] strassen1D(int[] A, int[] B, int n) {
        if (n == 1) {
            return new int[]{A[0] * B[0]};
        }
        int m = n >>> 1;
        int mm = m * m;
        int[] A11 = new int[mm], A12 = new int[mm], A21 = new int[mm], A22 = new int[mm];
        int[] B11 = new int[mm], B12 = new int[mm], B21 = new int[mm], B22 = new int[mm];

        for (int i = 0; i < m; i++) {
            int im = i * m;
            int in1 = i * n;
            int in2 = (i + m) * n;
            System.arraycopy(A, in1, A11, im, m);
            System.arraycopy(A, in1 + m, A12, im, m);
            System.arraycopy(A, in2, A21, im, m);
            System.arraycopy(A, in2 + m, A22, im, m);

            System.arraycopy(B, in1, B11, im, m);
            System.arraycopy(B, in1 + m, B12, im, m);
            System.arraycopy(B, in2, B21, im, m);
            System.arraycopy(B, in2 + m, B22, im, m);
        }

        int[] M1 = strassen1D(sumar1D(A11, A22, mm), sumar1D(B11, B22, mm), m);
        int[] M2 = strassen1D(sumar1D(A21, A22, mm), B11, m);
        int[] M3 = strassen1D(A11, restar1D(B12, B22, mm), m);
        int[] M4 = strassen1D(A22, restar1D(B21, B11, mm), m);
        int[] M5 = strassen1D(sumar1D(A11, A12, mm), B22, m);
        int[] M6 = strassen1D(restar1D(A21, A11, mm), sumar1D(B11, B12, mm), m);
        int[] M7 = strassen1D(restar1D(A12, A22, mm), sumar1D(B21, B22, mm), m);

        int[] C = new int[n * n];
        for (int i = 0; i < m; i++) {
            int im = i * m;
            int in1 = i * n;
            int in2 = (i + m) * n;
            for (int j = 0; j < m; j++) {
                int k = im + j;
                int v1 = M1[k], v2 = M2[k], v3 = M3[k], v4 = M4[k];
                int v5 = M5[k], v6 = M6[k], v7 = M7[k];
                C[in1 + j]     = v1 + v4 - v5 + v7;
                C[in1 + m + j] = v3 + v5;
                C[in2 + j]     = v2 + v4;
                C[in2 + m + j] = v1 - v2 + v3 + v6;
            }
        }
        return C;
    }

    // =====================================================================
    // CARGA DE DATASETS Y VERIFICACIÓN
    // =====================================================================
    static int[] cargarQuickselect32(int n) throws IOException {
        Path ruta = Paths.get("datos", "qs32_n_" + n + ".bin");
        int[] a = new int[n];
        try (FileChannel ch = FileChannel.open(ruta, StandardOpenOption.READ)) {
            ByteBuffer buf = ByteBuffer.allocateDirect(8 << 20).order(ByteOrder.LITTLE_ENDIAN);
            int pos = 0;
            while (pos < n) {
                buf.clear();
                int bytes = (int) Math.min(buf.capacity(), (long) (n - pos) * 4);
                buf.limit(bytes);
                while (buf.hasRemaining()) {
                    if (ch.read(buf) < 0) throw new IOException("Archivo incompleto: " + ruta);
                }
                buf.flip();
                int m = bytes / 4;
                buf.asIntBuffer().get(a, pos, m);
                pos += m;
            }
        }
        return a;
    }

    static long[] cargarQuickselect64(int n) throws IOException {
        Path ruta = Paths.get("datos", "qs64_n_" + n + ".bin");
        long[] a = new long[n];
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
                buf.asLongBuffer().get(a, pos, m);
                pos += m;
            }
        }
        return a;
    }

    static int[][] cargarMatrices1D(int n) throws IOException {
        Path ruta = Paths.get("datos", "mat_n_" + n + ".bin");
        int nn = n * n;
        int[] A = new int[nn];
        int[] B = new int[nn];
        try (FileChannel ch = FileChannel.open(ruta, StandardOpenOption.READ)) {
            ByteBuffer buf = ByteBuffer.allocateDirect(2 * nn * 4).order(ByteOrder.LITTLE_ENDIAN);
            while (buf.hasRemaining()) {
                if (ch.read(buf) < 0) throw new IOException("Archivo incompleto: " + ruta);
            }
            buf.flip();
            buf.asIntBuffer().get(A, 0, nn).get(B, 0, nn);
        }
        return new int[][]{A, B};
    }

    static int[][] a2D(int[] a1d, int n) {
        int[][] m = new int[n][n];
        for (int i = 0; i < n; i++) {
            System.arraycopy(a1d, i * n, m[i], 0, n);
        }
        return m;
    }

    static long suma32(int[] a) {
        long s = 0;
        for (int x : a) s += x;
        return s;
    }

    static long suma64(long[] a) {
        long s = 0;
        for (long x : a) s += x;
        return s;
    }

    static boolean verificarQuickselect32(int[] a, int k, int resultado, long sumaAntes) {
        int n = a.length;
        int idx = k - 1;
        if (a[idx] != resultado) return false;
        for (int i = 0; i < idx; i++) if (a[i] > resultado) return false;
        for (int i = idx + 1; i < n; i++) if (a[i] < resultado) return false;
        if (suma32(a) != sumaAntes) return false;
        int paso = RANGO_MAX_QS / n;
        return resultado >= (k - 1) * paso + 1 && resultado <= k * paso;
    }

    static boolean verificarQuickselect64(long[] a, int k, long resultado, long sumaAntes) {
        int n = a.length;
        int idx = k - 1;
        if (a[idx] != resultado) return false;
        for (int i = 0; i < idx; i++) if (a[i] > resultado) return false;
        for (int i = idx + 1; i < n; i++) if (a[i] < resultado) return false;
        if (suma64(a) != sumaAntes) return false;
        long paso = RANGO_MAX_QS / n;
        return resultado >= (k - 1) * paso + 1 && resultado <= k * paso;
    }

    static boolean verificarMatrices(int[] A1d, int[] B1d, int[] C1d, int[][] C2d, int n) {
        long[] v1 = new long[n], v2 = new long[n];
        for (int j = 0; j < n; j++) {
            v1[j] = j + 1;
            v2[j] = ((j * 31 + 7) % 97) - 48;
        }
        long[] w1 = new long[n], w2 = new long[n];
        for (int k = 0; k < n; k++) {
            int kn = k * n;
            long s1 = 0, s2 = 0;
            for (int j = 0; j < n; j++) {
                long bkj = B1d[kn + j];
                s1 += bkj * v1[j];
                s2 += bkj * v2[j];
            }
            w1[k] = s1;
            w2[k] = s2;
        }
        for (int i = 0; i < n; i++) {
            int in = i * n;
            long aw1 = 0, aw2 = 0;
            for (int k = 0; k < n; k++) {
                long aik = A1d[in + k];
                aw1 += aik * w1[k];
                aw2 += aik * w2[k];
            }
            long cv1 = 0, cv2 = 0;
            if (C2d != null) {
                int[] fila = C2d[i];
                for (int j = 0; j < n; j++) {
                    long cij = fila[j];
                    cv1 += cij * v1[j];
                    cv2 += cij * v2[j];
                }
            } else {
                for (int j = 0; j < n; j++) {
                    long cij = C1d[in + j];
                    cv1 += cij * v1[j];
                    cv2 += cij * v2[j];
                }
            }
            if (aw1 != cv1 || aw2 != cv2) return false;
        }
        return true;
    }

    // =====================================================================
    // MEDICIÓN DE MEMORIA Y PRECALENTAMIENTO JIT
    // =====================================================================
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
            try { Thread.sleep(40); } catch (InterruptedException ignored) { }
        }
    }

    static long bytesAsignadosHilo() {
        return ((com.sun.management.ThreadMXBean) ManagementFactory.getThreadMXBean())
            .getThreadAllocatedBytes(Thread.currentThread().threadId());
    }

    /** Bytes exactos de una matriz n x n en el heap de HotSpot JVM (64-bit con CompressedOops). */
    static long bytesMatrizJava(boolean es2d, int n) {
        if (!es2d) {
            // 1 arreglo int[n*n]: cabecera 16B + alineación a múltiplos de 8B
            long raw = 16L + 4L * n * n;
            return (raw + 7L) & ~7L;
        }
        // int[n][n]: arreglo externo (16 + 4*n alineado a 8) + n filas de (16 + 4*n alineado a 8)
        long ext = (16L + 4L * n + 7L) & ~7L;
        long fila = (16L + 4L * n + 7L) & ~7L;
        return ext + (long) n * fila;
    }

    /** Memoria auxiliar simultáneamente viva en la pila de recursión para matrices. */
    static long memoriaVivaMatricesBytes(String variante, int n) {
        boolean es2d = variante.endsWith("_2d");
        if (variante.startsWith("tradicional")) {
            return bytesMatrizJava(es2d, n);
        }
        int niveles = Integer.numberOfTrailingZeros(n);
        long viva = bytesMatrizJava(es2d, n);
        for (int d = 0; d < niveles; d++) {
            int m = n >>> (d + 1);
            viva += 17L * bytesMatrizJava(es2d, m);
        }
        return viva;
    }

    static void calentarQuickselect(int bits) {
        Random rng = new Random(17);
        int m = 20_000;
        if (bits == 32) {
            for (int r = 0; r < 10; r++) {
                int[] a = new int[m];
                for (int i = 0; i < m; i++) a[i] = rng.nextInt(RANGO_MAX_QS) + 1;
                quickselect32(a, m / 2 + 1);
            }
        } else {
            for (int r = 0; r < 10; r++) {
                long[] a = new long[m];
                for (int i = 0; i < m; i++) a[i] = rng.nextInt(RANGO_MAX_QS) + 1L;
                quickselect64(a, m / 2 + 1);
            }
        }
    }

    static void calentarMatrices(String variante) {
        Random rng = new Random(23);
        int m = 16;
        for (int r = 0; r < 8; r++) {
            if (variante.endsWith("_2d")) {
                int[][] A = new int[m][m], B = new int[m][m];
                for (int i = 0; i < m; i++) {
                    for (int j = 0; j < m; j++) {
                        A[i][j] = rng.nextInt(41) - 20;
                        B[i][j] = rng.nextInt(41) - 20;
                    }
                }
                if (variante.equals("tradicional_2d")) tradicional2D(A, B, m);
                else strassen2D(A, B, m);
            } else {
                int[] A = new int[m * m], B = new int[m * m];
                for (int i = 0; i < m * m; i++) {
                    A[i] = rng.nextInt(41) - 20;
                    B[i] = rng.nextInt(41) - 20;
                }
                if (variante.equals("tradicional_1d")) tradicional1D(A, B, m);
                else strassen1D(A, B, m);
            }
        }
    }

    // =====================================================================
    // CORRIDAS DE BENCHMARK
    // =====================================================================
    static void correrQuickselect(int bits, int n, int k) throws IOException {
        if (k <= 0) k = (n / 2) + 1;
        calentarQuickselect(bits);
        double mb = 1024.0 * 1024.0;

        if (bits == 32) {
            int[] a = cargarQuickselect32(n);
            long sumaAntes = suma32(a);
            long memDatos = 16L + 4L * n;
            gcCompleto();
            long base = heapUsado();
            reiniciarPicos();
            long asigAntes = bytesAsignadosHilo();

            long t0 = System.nanoTime();
            int res = quickselect32(a, k);
            long t1 = System.nanoTime();

            long asignados = Math.max(0L, bytesAsignadosHilo() - asigAntes);
            long pico = heapPico();
            boolean ok = verificarQuickselect32(a, k, res, sumaAntes);
            System.out.println(String.format(Locale.ROOT,
                "RESULTADO {\"lenguaje\": \"java\", \"problema\": \"quickselect\", \"variante\": \"32bits\", "
                    + "\"bits\": 32, \"n\": %d, \"k\": %d, \"resultado\": %d, \"tiempo_s\": %.9f, "
                    + "\"mem_datos_mb\": %.4f, \"mem_base_mb\": %.3f, \"mem_pico_mb\": %.3f, "
                    + "\"mem_extra_mb\": %.4f, \"verificado\": %s}",
                n, k, res, (t1 - t0) / 1e9, memDatos / mb, base / mb, pico / mb, asignados / mb, ok));
        } else {
            long[] a = cargarQuickselect64(n);
            long sumaAntes = suma64(a);
            long memDatos = 16L + 8L * n;
            gcCompleto();
            long base = heapUsado();
            reiniciarPicos();
            long asigAntes = bytesAsignadosHilo();

            long t0 = System.nanoTime();
            long res = quickselect64(a, k);
            long t1 = System.nanoTime();

            long asignados = Math.max(0L, bytesAsignadosHilo() - asigAntes);
            long pico = heapPico();
            boolean ok = verificarQuickselect64(a, k, res, sumaAntes);
            System.out.println(String.format(Locale.ROOT,
                "RESULTADO {\"lenguaje\": \"java\", \"problema\": \"quickselect\", \"variante\": \"64bits\", "
                    + "\"bits\": 64, \"n\": %d, \"k\": %d, \"resultado\": %d, \"tiempo_s\": %.9f, "
                    + "\"mem_datos_mb\": %.4f, \"mem_base_mb\": %.3f, \"mem_pico_mb\": %.3f, "
                    + "\"mem_extra_mb\": %.4f, \"verificado\": %s}",
                n, k, res, (t1 - t0) / 1e9, memDatos / mb, base / mb, pico / mb, asignados / mb, ok));
        }
    }

    static void correrMatrices(String variante, int n) throws IOException {
        int[][] ab = cargarMatrices1D(n);
        int[] A1d = ab[0], B1d = ab[1];
        boolean es2d = variante.endsWith("_2d");
        int[][] A2d = es2d ? a2D(A1d, n) : null;
        int[][] B2d = es2d ? a2D(B1d, n) : null;

        calentarMatrices(variante);
        gcCompleto();
        long base = heapUsado();
        reiniciarPicos();
        long asigAntes = bytesAsignadosHilo();

        int[] C1d = null;
        int[][] C2d = null;
        long t0 = System.nanoTime();
        switch (variante) {
            case "tradicional_2d": C2d = tradicional2D(A2d, B2d, n); break;
            case "tradicional_1d": C1d = tradicional1D(A1d, B1d, n); break;
            case "strassen_2d":    C2d = strassen2D(A2d, B2d, n);    break;
            case "strassen_1d":    C1d = strassen1D(A1d, B1d, n);    break;
            default: throw new IllegalArgumentException("Variante desconocida: " + variante);
        }
        long t1 = System.nanoTime();

        long asignados = Math.max(0L, bytesAsignadosHilo() - asigAntes);
        long pico = heapPico();
        long memDatos = 2L * bytesMatrizJava(es2d, n);
        long memViva = memoriaVivaMatricesBytes(variante, n);
        long memExtra = Math.max(memViva, Math.min(asignados, Math.max(0L, pico - base)));
        boolean ok = verificarMatrices(A1d, B1d, C1d, C2d, n);
        double mb = 1024.0 * 1024.0;
        String alg = variante.startsWith("strassen") ? "strassen" : "tradicional";
        String rep = es2d ? "2d" : "1d";

        System.out.println(String.format(Locale.ROOT,
            "RESULTADO {\"lenguaje\": \"java\", \"problema\": \"matrices\", \"variante\": \"%s\", "
                + "\"algoritmo\": \"%s\", \"representacion\": \"%s\", \"n\": %d, \"tiempo_s\": %.9f, "
                + "\"mem_datos_mb\": %.4f, \"mem_base_mb\": %.3f, \"mem_pico_mb\": %.3f, "
                + "\"mem_extra_mb\": %.4f, \"mem_acumulada_mb\": %.4f, \"verificado\": %s}",
            variante, alg, rep, n, (t1 - t0) / 1e9, memDatos / mb, base / mb, pico / mb,
            memExtra / mb, asignados / mb, ok));
    }

    // =====================================================================
    // AUTOPRUEBA (--test)
    // =====================================================================
    static int fallos = 0;

    static void probarQuickselectCaso(String nombre, int[] datos) {
        int[] ord = datos.clone();
        Arrays.sort(ord);
        int n = datos.length;
        int[] ks = {1, Math.max(1, n / 4), (n / 2) + 1, Math.max(1, (3 * n) / 4), n};
        boolean ok32 = true, ok64 = true;
        for (int k : ks) {
            int[] copia32 = datos.clone();
            int r32 = quickselect32(copia32, k);
            if (r32 != ord[k - 1]) ok32 = false;

            long[] copia64 = new long[n];
            for (int i = 0; i < n; i++) copia64[i] = datos[i];
            long r64 = quickselect64(copia64, k);
            if (r64 != ord[k - 1]) ok64 = false;
        }
        if (!ok32 || !ok64) fallos++;
        System.out.printf("  %-6s Quickselect (32/64 bits) %-30s n=%d%n",
            (ok32 && ok64) ? "OK" : "FALLO", nombre, n);
    }

    static void probarMatricesCaso(String nombre, int n, int minVal, int maxVal) {
        Random rng = new Random(100 + n);
        int[] A1 = new int[n * n], B1 = new int[n * n];
        for (int i = 0; i < n * n; i++) {
            A1[i] = minVal + rng.nextInt(maxVal - minVal + 1);
            B1[i] = minVal + rng.nextInt(maxVal - minVal + 1);
        }
        int[][] A2 = a2D(A1, n), B2 = a2D(B1, n);

        int[][] ct2 = tradicional2D(A2, B2, n);
        int[] ct1 = tradicional1D(A1, B1, n);
        int[][] cs2 = strassen2D(A2, B2, n);
        int[] cs1 = strassen1D(A1, B1, n);

        boolean ok = Arrays.equals(ct1, cs1);
        for (int i = 0; i < n && ok; i++) {
            for (int j = 0; j < n; j++) {
                int esp = ct1[i * n + j];
                if (ct2[i][j] != esp || cs2[i][j] != esp) {
                    ok = false;
                    break;
                }
            }
        }
        if (!ok) fallos++;
        System.out.printf("  %-6s Matrices (Trad/Strassen 2D/1D) %-24s n=%dx%d%n",
            ok ? "OK" : "FALLO", nombre, n, n);
    }

    static void autoprueba() {
        System.out.println("=== Autoprueba Práctica 3: Divide y Vencerás (Java) ===");
        Random rng = new Random(42);
        probarQuickselectCaso("un elemento", new int[]{99});
        probarQuickselectCaso("dos elementos", new int[]{25, 10});

        int[] yaOrd = new int[1000], inv = new int[1000], dup = new int[1500], aleat = new int[5000];
        for (int i = 0; i < 1000; i++) { yaOrd[i] = i + 1; inv[i] = 1000 - i; }
        for (int i = 0; i < 1500; i++) dup[i] = rng.nextInt(15) + 1;
        for (int i = 0; i < 5000; i++) aleat[i] = rng.nextInt(RANGO_MAX_QS) + 1;

        probarQuickselectCaso("ya ordenado", yaOrd);
        probarQuickselectCaso("orden inverso", inv);
        probarQuickselectCaso("con duplicados", dup);
        probarQuickselectCaso("permutacion [1, 10^7]", aleat);

        probarMatricesCaso("caso base 1x1", 1, -50, 50);
        probarMatricesCaso("matriz 2x2", 2, -50, 50);
        probarMatricesCaso("matriz 4x4", 4, -50, 50);
        probarMatricesCaso("matriz 16x16", 16, -100, 100);
        probarMatricesCaso("matriz 32x32", 32, -100, 100);
        probarMatricesCaso("matriz 64x64", 64, -100, 100);

        System.out.println(fallos == 0 ? "\nTODAS LAS PRUEBAS PASARON" : "\n" + fallos + " PRUEBAS FALLARON");
        if (fallos > 0) System.exit(1);
    }

    public static void main(String[] args) throws IOException {
        String problema = null;
        String variante = "strassen_1d";
        int bits = 32;
        int n = -1;
        int k = -1;

        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--test": autoprueba(); return;
                case "--problema": problema = args[++i]; break;
                case "--variante": variante = args[++i]; break;
                case "--bits": bits = Integer.parseInt(args[++i]); break;
                case "--n": n = Integer.parseInt(args[++i]); break;
                case "--k": k = Integer.parseInt(args[++i]); break;
                default: throw new IllegalArgumentException("Argumento desconocido: " + args[i]);
            }
        }
        if (problema == null || n <= 0) {
            System.err.println("Uso: java DivideVenceras --problema <quickselect|matrices> [--bits 32|64] "
                + "[--variante <tradicional_2d|tradicional_1d|strassen_2d|strassen_1d>] --n <N> | --test");
            System.exit(2);
        }
        if (problema.equals("quickselect")) {
            correrQuickselect(bits, n, k);
        } else if (problema.equals("matrices")) {
            correrMatrices(variante, n);
        } else {
            throw new IllegalArgumentException("Problema desconocido: " + problema);
        }
    }
}
