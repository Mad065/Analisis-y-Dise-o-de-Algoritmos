import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;

public class algoritmosBusquedaPropio {

    // Búsqueda secuencial
    public static <T> Integer busquedaSecuencial(List<T> arr, T objetivo) {
        for (int i = 0; i < arr.size(); i++) {
            if (arr.get(i).equals(objetivo)) {
                return i;
            }
        }
        return null;
    }

    // Búsqueda binaria
    public static Integer busquedaBinaria(List<Integer> arr, int objetivo) {
        int inicio = 0;
        int fin = arr.size() - 1;

        while (inicio <= fin) {
            int medio = inicio + (fin - inicio) / 2;
            if (arr.get(medio) == objetivo) {
                return medio;
            } else if (arr.get(medio) < objetivo) {
                inicio = medio + 1;
            } else {
                fin = medio - 1;
            }
        }
        return null;
    }

    // Búsqueda por interpolación
    public static Integer busquedaInterpolacion(List<Integer> arr, int objetivo) {
        int inicio = 0;
        int fin = arr.size() - 1;

        // Asegura que el objetivo esté dentro del rango de valores evaluados
        while (inicio <= fin && objetivo >= arr.get(inicio) && objetivo <= arr.get(fin)) {
            if (inicio == fin) {
                if (arr.get(inicio) == objetivo) {
                    return inicio;
                }
                return null;
            }

            int pos = inicio + (int) (((float) (fin - inicio) / (arr.get(fin) - arr.get(inicio))) 
                              * (objetivo - arr.get(inicio)));

            if (arr.get(pos) == objetivo) {
                return pos;
            } else if (arr.get(pos) < objetivo) {
                inicio = pos + 1;
            } else {
                fin = pos - 1;
            }
        }
        return null;
    }

    // Clase auxiliar tabla hash
    static class Par<K, V> {
        K clave;
        V valor;

        Par(K clave, V valor) {
            this.clave = clave;
            this.valor = valor;
        }
    }

    // Búsqueda por tabla hash
    static class TablaHash<K, V> {
        private int tamano;
        private List<List<Par<K, V>>> tabla;

        public TablaHash(int tamano) {
            this.tamano = tamano;
            this.tabla = new ArrayList<>(tamano);
            for (int i = 0; i < tamano; i++) {
                this.tabla.add(new LinkedList<>());
            }
        }

        private int hash(K clave) {
            // Math.abs es necesario porque hashCode() en Java puede ser negativo
            return Math.abs(clave.hashCode()) % this.tamano;
        }

        public void insertar(K clave, V valor) {
            int indice = this.hash(clave);
            List<Par<K, V>> bucket = this.tabla.get(indice);

            // Actualizar valor si la clave ya existe en el bucket
            for (Par<K, V> par : bucket) {
                if (par.clave.equals(clave)) {
                    par.valor = valor;
                    return;
                }
            }

            // Si no existe, agregar nuevo par (clave, valor)
            bucket.add(new Par<>(clave, valor));
        }

        public V buscar(K clave) {
            int indice = this.hash(clave);
            List<Par<K, V>> bucket = this.tabla.get(indice);

            for (Par<K, V> par : bucket) {
                if (par.clave.equals(clave)) {
                    return par.valor;
                }
            }
            return null;
        }
    }

    // Test
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        System.out.print("Ingrese de que tamaño desea la lista de prueba: ");
        int tamano = scanner.nextInt();

        List<Integer> datos = new ArrayList<>();
        for (int i = 0; i < tamano; i++) {
            datos.add(random.nextInt(tamano * 10) + 1);
        }

        Collections.sort(datos);

        System.out.println("Lista de prueba: " + datos);


        System.out.print("Ingrese el elemento a buscar: ");
        int objetivo = scanner.nextInt();

        System.out.println("Elemento a buscar: " + objetivo + "\n");

        // 1. Secuencial
        Integer idxSeq = busquedaSecuencial(datos, objetivo);
        System.out.println("Secuencial: encontrado en índice " + idxSeq);

        // 2. Binaria
        Integer idxBin = busquedaBinaria(datos, objetivo);
        System.out.println("Binaria: encontrado en índice " + idxBin);

        // 3. Interpolación
        Integer idxInterp = busquedaInterpolacion(datos, objetivo);
        System.out.println("Interpolación: encontrado en índice " + idxInterp);

        // 4. Tabla Hash
        System.out.println("\nTabla Hash");
        TablaHash<String, Map<String, Object>> tabla = new TablaHash<>(5);

        Map<String, Object> usr1 = new HashMap<>();
        usr1.put("nombre", "Ana");
        usr1.put("edad", 28);
        tabla.insertar("usuario_1", usr1);

        Map<String, Object> usr2 = new HashMap<>();
        usr2.put("nombre", "Carlos");
        usr2.put("edad", 34);
        tabla.insertar("usuario_2", usr2);

        Map<String, Object> usr3 = new HashMap<>();
        usr3.put("nombre", "Elena");
        usr3.put("edad", 22);
        tabla.insertar("usuario_3", usr3);

        String claveBusqueda = "usuario_2";
        Map<String, Object> resultadoHash = tabla.buscar(claveBusqueda);
        System.out.println("Búsqueda por clave '" + claveBusqueda + "': " + resultadoHash);

        scanner.close();
    }
}