<!-- Generado automáticamente por generar_graficas.py -->

### 1. Quickselect (Selección de Hoare) — Tiempos de Ejecución

| Tamaño $n$ | Posición $k$ (Mediana) | Valor Encontrado | Python 32 bits | Python 64 bits | Java 32 bits | Java 64 bits | Speedup Java (32b / 64b) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 1,000 | 501 | 5,003,107 | 140.96 µs | 95.92 µs | 22.79 µs | 20.62 µs | **6.2×** / **4.7×** |
| 5,000 | 2,501 | 5,001,318 | 473.83 µs | 404.88 µs | 77.38 µs | 129.75 µs | **6.1×** / **3.1×** |
| 10,000 | 5,001 | 5,000,035 | 1.11 ms | 969.54 µs | 147.38 µs | 130.58 µs | **7.5×** / **7.4×** |
| 50,000 | 25,001 | 5,000,136 | 3.81 ms | 3.44 ms | 416.88 µs | 473.92 µs | **9.1×** / **7.3×** |
| 100,000 | 50,001 | 5,000,012 | 6.00 ms | 5.95 ms | 887.42 µs | 934.88 µs | **6.8×** / **6.4×** |
| 500,000 | 250,001 | 5,000,010 | 37.12 ms | 36.92 ms | 3.74 ms | 4.26 ms | **9.9×** / **8.7×** |
| 1,000,000 | 500,001 | 5,000,003 | 68.63 ms | 67.93 ms | 8.74 ms | 9.25 ms | **7.9×** / **7.3×** |
| 5,000,000 | 2,500,001 | 5,000,002 | 298.94 ms | 299.15 ms | 28.01 ms | 28.68 ms | **10.7×** / **10.4×** |
| 10,000,000 | 5,000,001 | 5,000,001 | 917.48 ms | 916.43 ms | 67.92 ms | 63.20 ms | **13.5×** / **14.5×** |

### 2. Quickselect — Consumo de Memoria (Arreglo de Datos vs RSS Pico del Proceso)

| Tamaño $n$ | Arreglo 32 bits (`4n`) | Arreglo 64 bits (`8n`) | RSS Pico Python (32b / 64b) | RSS Pico Java (32b / 64b) | Espacio Auxiliar |
| ---: | ---: | ---: | :---: | :---: | :---: |
| 1,000 | 3.9 KB | 7.8 KB | 20.47 MB / 20.48 MB | 76.36 MB / 76.36 MB | ≈ 0 MB ($O(1)$) |
| 5,000 | 19.6 KB | 39.1 KB | 20.48 MB / 20.48 MB | 76.28 MB / 76.34 MB | ≈ 0 MB ($O(1)$) |
| 10,000 | 39.1 KB | 78.1 KB | 20.50 MB / 20.50 MB | 76.28 MB / 76.34 MB | ≈ 0 MB ($O(1)$) |
| 50,000 | 195.4 KB | 390.7 KB | 20.62 MB / 20.81 MB | 76.58 MB / 76.95 MB | ≈ 0 MB ($O(1)$) |
| 100,000 | 390.7 KB | 781.3 KB | 20.81 MB / 21.22 MB | 77.16 MB / 77.22 MB | ≈ 0 MB ($O(1)$) |
| 500,000 | 1.91 MB | 3.81 MB | 22.34 MB / 24.34 MB | 79.08 MB / 82.83 MB | ≈ 0 MB ($O(1)$) |
| 1,000,000 | 3.81 MB | 7.63 MB | 24.36 MB / 28.16 MB | 82.72 MB / 86.89 MB | ≈ 0 MB ($O(1)$) |
| 5,000,000 | 19.07 MB | 38.15 MB | 39.58 MB / 58.69 MB | 96.95 MB / 120.09 MB | ≈ 0 MB ($O(1)$) |
| 10,000,000 | 38.15 MB | 76.29 MB | 58.72 MB / 96.84 MB | 120.09 MB / 158.39 MB | ≈ 0 MB ($O(1)$) |

### 3. Multiplicación de Matrices — Tiempo de Ejecución (Python)

| Variante | Representación | 16×16 | 32×32 | 64×64 | 128×128 | 256×256 | 512×512 |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tradicional 2D** | Bidimensional (2D) | 121.17 µs | 903.96 µs | 5.54 ms | 44.40 ms | 355.63 ms | 2.822 s |
| **Tradicional 1D Contiguo** | Unidimensional Contiguo (1D) | 212.12 µs | 1.59 ms | 12.96 ms | 106.63 ms | 857.69 ms | 6.900 s |
| **Strassen 2D** | Bidimensional (2D) | 1.14 ms | 7.86 ms | 57.43 ms | 404.73 ms | 2.873 s | 20.403 s |
| **Strassen 1D Contiguo** | Unidimensional Contiguo (1D) | 1.90 ms | 13.49 ms | 96.42 ms | 680.02 ms | 4.868 s | 33.798 s |

### 3. Multiplicación de Matrices — Tiempo de Ejecución (Java)

| Variante | Representación | 16×16 | 32×32 | 64×64 | 128×128 | 256×256 | 512×512 |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tradicional 2D** | Bidimensional (2D) | 58.71 µs | 415.62 µs | 1.15 ms | 5.74 ms | 12.21 ms | 56.37 ms |
| **Tradicional 1D Contiguo** | Unidimensional Contiguo (1D) | 62.79 µs | 464.12 µs | 1.33 ms | 5.54 ms | 9.72 ms | 36.03 ms |
| **Strassen 2D** | Bidimensional (2D) | 831.17 µs | 5.24 ms | 27.45 ms | 147.95 ms | 960.81 ms | 6.765 s |
| **Strassen 1D Contiguo** | Unidimensional Contiguo (1D) | 82.88 µs | 492.75 µs | 3.04 ms | 18.25 ms | 83.05 ms | 510.93 ms |

### 4. Multiplicación de Matrices — Memoria Auxiliar Viva y RSS Pico (Python)

| Variante | Métrica | 16×16 | 32×32 | 64×64 | 128×128 | 256×256 | 512×512 |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tradicional 2D** | Memoria Auxiliar Viva | 16.0 KB | 48.0 KB | 160.0 KB | 640.0 KB | 2.50 MB | 10.03 MB |
| **Tradicional 2D** | RSS Pico del Proceso | 20.53 MB | 20.56 MB | 20.88 MB | 21.95 MB | 26.80 MB | 46.25 MB |
| **Tradicional 1D Contiguo** | Memoria Auxiliar Viva | 1.1 KB | 4.1 KB | 16.1 KB | 64.1 KB | 256.1 KB | 1.00 MB |
| **Tradicional 1D Contiguo** | RSS Pico del Proceso | 20.50 MB | 20.56 MB | 20.55 MB | 20.59 MB | 21.45 MB | 24.47 MB |
| **Strassen 2D** | Memoria Auxiliar Viva | 80.5 KB | 279.4 KB | 1.01 MB | 3.90 MB | 15.29 MB | 60.57 MB |
| **Strassen 2D** | RSS Pico del Proceso | 20.61 MB | 20.72 MB | 21.25 MB | 23.52 MB | 32.70 MB | 71.83 MB |
| **Strassen 1D Contiguo** | Memoria Auxiliar Viva | 32.0 KB | 32.0 KB | 113.1 KB | 592.0 KB | 1.68 MB | 6.68 MB |
| **Strassen 1D Contiguo** | RSS Pico del Proceso | 20.50 MB | 20.55 MB | 20.62 MB | 21.16 MB | 23.06 MB | 30.25 MB |

### 4. Multiplicación de Matrices — Memoria Auxiliar Viva y RSS Pico (Java)

| Variante | Métrica | 16×16 | 32×32 | 64×64 | 128×128 | 256×256 | 512×512 |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Tradicional 2D** | Memoria Auxiliar Viva | 1.3 KB | 4.6 KB | 17.3 KB | 66.6 KB | 261.0 KB | 1.01 MB |
| **Tradicional 2D** | RSS Pico del Proceso | 68.03 MB | 68.08 MB | 68.70 MB | 68.83 MB | 70.64 MB | 78.70 MB |
| **Tradicional 1D Contiguo** | Memoria Auxiliar Viva | 1.0 KB | 4.0 KB | 16.0 KB | 64.0 KB | 256.0 KB | 1.00 MB |
| **Tradicional 1D Contiguo** | RSS Pico del Proceso | 68.03 MB | 68.02 MB | 64.77 MB | 68.53 MB | 69.64 MB | 74.61 MB |
| **Strassen 2D** | Memoria Auxiliar Viva | 13.1 KB | 3.63 MB | 4.31 MB | 116.47 MB | 117.28 MB | 127.35 MB |
| **Strassen 2D** | RSS Pico del Proceso | 71.44 MB | 73.17 MB | 82.22 MB | 190.86 MB | 195.14 MB | 216.88 MB |
| **Strassen 1D Contiguo** | Memoria Auxiliar Viva | 7.8 KB | 28.1 KB | 4.31 MB | 72.47 MB | 117.00 MB | 238.14 MB |
| **Strassen 1D Contiguo** | RSS Pico del Proceso | 70.69 MB | 72.25 MB | 73.89 MB | 147.67 MB | 225.69 MB | 396.22 MB |
