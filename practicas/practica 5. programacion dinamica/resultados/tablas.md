# Tablas Comparativas de Rendimiento y Optimalidad — Práctica 5

## 1. Mochila 0/1: Comparativa de 3 Variantes (Tiempos y Llamadas)
| $n$ | Capacidad | Tiempo Rec (ms) | Tiempo Memo (ms) | Tiempo Tab (ms) | Llamadas Rec | Subproblemas Memo | Speedup Tab/Rec |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 4 | 13 | 0.0036 | 0.00437 | 0.00747 | 20 | 11 | **0.5x** |
| 8 | 36 | 0.03077 | 0.02734 | 0.02787 | 305 | 107 | **1.1x** |
| 12 | 46 | 0.43733 | 0.08137 | 0.05694 | 4575 | 304 | **7.7x** |
| 16 | 60 | 6.55875 | 0.1485 | 0.08913 | 71458 | 589 | **73.6x** |
| 20 | 81 | 109.31356 | 0.28143 | 0.14916 | 1170310 | 1061 | **732.9x** |


## 2. Mochila 0/1: Escalabilidad a Gran Escala (Memoización vs Tabulación)
| $n$ | Capacidad | Tiempo Memo (ms) | Tiempo Tab (ms) | Memoria Memo (KiB) | Memoria Tab (KiB) | Relación Tiempo (Memo/Tab) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 50 | 250 | 2.81308 | 1.15738 | 1012.316 | 293.992 | 2.43x |
| 100 | 500 | 13.04842 | 4.96092 | 4720.641 | 1125.738 | 2.63x |
| 150 | 750 | 29.67346 | 11.22533 | 15330.562 | 2483.891 | 2.64x |
| 200 | 1000 | 54.53604 | 20.21367 | 20021.547 | 4555.098 | 2.7x |
| 300 | 1500 | 128.11596 | 46.80933 | 63566.57 | 10441.195 | 2.74x |


## 3. Cambio de Monedas: Comparativa de 3 Variantes
| Monto $V$ | Tiempo Rec (ms) | Tiempo Memo (ms) | Tiempo Tab (ms) | Llamadas Rec | Subproblemas Memo | Speedup Tab/Rec |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 6 | 0.00925 | 0.00403 | 0.00276 | 64 | 6 | **3.4x** |
| 9 | 0.0375 | 0.00528 | 0.00309 | 319 | 9 | **12.1x** |
| 12 | 0.17123 | 0.00663 | 0.00352 | 1582 | 12 | **48.6x** |
| 15 | 0.84669 | 0.0085 | 0.00439 | 7843 | 15 | **192.9x** |
| 18 | 4.21313 | 0.00932 | 0.00486 | 38869 | 18 | **866.9x** |


## 4. Demostración Cuantitativa de Optimalidad: DP vs Voraz (Sistemas No Canónicos)
| Instancia | Monedas $C$ | Monto $V$ | Monedas Óptimas (DP) | Solución DP | Monedas Voraz | Solución Voraz | ¿Voraz Subóptimo? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `no_canonico_1_3_4_m6` | [1, 3, 4] | 6 | **2** | `[3, 3]` | 3 | `[4, 1, 1]` | ✅ SÍ (Demostrado) |
| `no_canonico_1_15_25_m30` | [1, 15, 25] | 30 | **2** | `[15, 15]` | 6 | `[25, 1, 1, 1, 1, 1]` | ✅ SÍ (Demostrado) |
| `no_canonico_1_6_10_m12` | [1, 6, 10] | 12 | **2** | `[6, 6]` | 3 | `[10, 1, 1]` | ✅ SÍ (Demostrado) |


## 5. LCSq: Comparativa de 3 Variantes
| Longitud $L$ | Tiempo Rec (ms) | Tiempo Memo (ms) | Tiempo Tab (ms) | Llamadas Rec | Subproblemas Memo | Speedup Tab/Rec |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 3 | 0.00433 | 0.00365 | 0.00397 | 27 | 9 | **1.1x** |
| 4 | 0.00704 | 0.00479 | 0.00477 | 63 | 14 | **1.5x** |
| 5 | 0.00579 | 0.00468 | 0.00582 | 49 | 15 | **1.0x** |
| 6 | 0.036 | 0.00847 | 0.00795 | 382 | 30 | **4.5x** |
| 7 | 0.1069 | 0.01213 | 0.00872 | 1233 | 48 | **12.3x** |


## 6. Subcadena LCS: Comparativa de 3 Variantes
| Longitud $L$ | Tiempo Rec (ms) | Tiempo Memo (ms) | Tiempo Tab (ms) | Llamadas Rec | Subproblemas Memo | Speedup Tab/Rec |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 3 | 0.00658 | 0.00318 | 0.00266 | 48 | 9 | **2.5x** |
| 4 | 0.01833 | 0.00417 | 0.00288 | 180 | 16 | **6.4x** |
| 5 | 0.07794 | 0.00544 | 0.00354 | 826 | 25 | **22.0x** |
| 6 | 0.27823 | 0.00724 | 0.00441 | 2978 | 36 | **63.1x** |
| 7 | 1.39015 | 0.0094 | 0.0052 | 15355 | 49 | **267.3x** |

