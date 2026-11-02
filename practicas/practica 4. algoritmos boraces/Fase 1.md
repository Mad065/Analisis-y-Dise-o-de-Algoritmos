# Práctica 4: Algoritmos Voraces y Codificación Huffman
## Fase 1: Teoría sin ayuda de la IA

---

### 1. Análisis del Mensaje y Codificación Huffman

Se analiza la cadena de entrada de longitud $N = 36$ caracteres:

$$\mathcal{M} = \text{"ABRACADABRA\_ALGORITMO\_AVANZADO\_ESCOM"}$$

---

#### A. Tabla de Frecuencias Absolutas y Relativas

Contabilizando la ocurrencia de cada carácter en $\mathcal{M}$, se obtiene un alfabeto de $k = 17$ símbolos distintos. La frecuencia relativa se define como:

$$p_i = \frac{f_i}{N} = \frac{f_i}{36}$$

| Carácter ($c_i$) | Representación / Significado | Frecuencia ($f_i$) | Probabilidad ($p_i$) | $p_i$ (decimal) |   Porcentaje   |
| :--------------: | :--------------------------: | :----------------: | :------------------: | :-------------: | :------------: |
|      **A**       |          Letra 'A'           |         9          |     $9/36 = 1/4$     |    $0.250000$   |   $25.00\%$    |
|      **O**       |          Letra 'O'           |         4          |     $4/36 = 1/9$     |    $0.111111$   |   $11.11\%$    |
|      **R**       |          Letra 'R'           |         3          |    $3/36 = 1/12$     |    $0.083333$   |    $8.33\%$    |
|      **\_**      |     Guion bajo / Espacio     |         3          |    $3/36 = 1/12$     |    $0.083333$   |    $8.33\%$    |
|      **B**       |          Letra 'B'           |         2          |    $2/36 = 1/18$     |    $0.055556$   |    $5.56\%$    |
|      **C**       |          Letra 'C'           |         2          |    $2/36 = 1/18$     |    $0.055556$   |    $5.56\%$    |
|      **D**       |          Letra 'D'           |         2          |    $2/36 = 1/18$     |    $0.055556$   |    $5.56\%$    |
|      **M**       |          Letra 'M'           |         2          |    $2/36 = 1/18$     |    $0.055556$   |    $5.56\%$    |
|      **E**       |          Letra 'E'           |         1          |        $1/36$        |    $0.027778$   |    $2.78\%$    |
|      **G**       |          Letra 'G'           |         1          |        $1/36$        |    $0.027778$   |    $2.78\%$    |
|      **I**       |          Letra 'I'           |         1          |        $1/36$        |    $0.027778$   |    $2.78\%$    |
|      **L**       |          Letra 'L'           |         1          |        $1/36$        |    $0.027778$   |    $2.78\%$    |
|      **N**       |          Letra 'N'           |         1          |        $1/36$        |    $0.027778$   |    $2.78\%$    |
|      **S**       |          Letra 'S'           |         1          |        $1/36$        |    $0.027778$   |    $2.78\%$    |
|      **T**       |          Letra 'T'           |         1          |        $1/36$        |    $0.027778$   |    $2.78\%$    |
|      **V**       |          Letra 'V'           |         1          |        $1/36$        |    $0.027778$   |    $2.78\%$    |
|      **Z**       |          Letra 'Z'           |         1          |        $1/36$        |    $0.027778$   |    $2.78\%$    |
|    **Total**     |    **17 símbolos únicos**    |       **36**       |   **$36/36 = 1$**    |  **$1.000000$** | **$100.00\%$** |

---

#### B. Entropía Empírica de Shannon

La entropía de Shannon $H(X)$ establece el límite teórico inferior e infranqueable para la compresión de datos sin pérdida (promedio de bits mínimos por carácter):

$$H(X) = -\sum_{i=1}^{k} p_i \log_2(p_i) = \sum_{i=1}^{k} p_i \log_2\left(\frac{1}{p_i}\right)$$

Agrupando los cálculos por clases de frecuencia idéntica para exactitud analítica:

1. **Símbolos con $f_i = 9$ (1 símbolo: `A`):**
   $$1 \times \left[ \frac{9}{36} \log_2\left(\frac{36}{9}\right) \right] = \frac{1}{4} \log_2(4) = 0.25 \times 2 = \mathbf{0.500000\text{ bits}}$$

2. **Símbolos con $f_i = 4$ (1 símbolo: `O`):**
   $$1 \times \left[ \frac{4}{36} \log_2\left(\frac{36}{4}\right) \right] = \frac{1}{9} \log_2(9) \approx 0.111111 \times 3.169925 = \mathbf{0.352214\text{ bits}}$$

3. **Símbolos con $f_i = 3$ (2 símbolos: `R`, `_`):**
   $$2 \times \left[ \frac{3}{36} \log_2\left(\frac{36}{3}\right) \right] = \frac{6}{36} \log_2(12) = \frac{1}{6} \times 3.584963 = \mathbf{0.597494\text{ bits}}$$

4. **Símbolos con $f_i = 2$ (4 símbolos: `B`, `C`, `D`, `M`):**
   $$4 \times \left[ \frac{2}{36} \log_2\left(\frac{36}{2}\right) \right] = \frac{8}{36} \log_2(18) = \frac{2}{9} \times 4.169925 = \mathbf{0.926650\text{ bits}}$$

5. **Símbolos con $f_i = 1$ (9 símbolos: `E`, `G`, `I`, `L`, `N`, `S`, `T`, `V`, `Z`):**
   $$9 \times \left[ \frac{1}{36} \log_2\left(\frac{36}{1}\right) \right] = \frac{9}{36} \log_2(36) = \frac{1}{4} \times 5.169925 = \mathbf{1.292481\text{ bits}}$$

**Suma total de la entropía empírica:**
$$H(X) = 0.500000 + 0.352214 + 0.597494 + 0.926650 + 1.292481 = \mathbf{3.668839\text{ bits/símbolo}}$$

---

#### C. Construcción Paso a Paso del Árbol de Huffman

El algoritmo voraz (*greedy*) de Huffman mantiene un bosque de nodos ordenados en una cola de prioridad de mínimos (*min-heap*), combinando repetidamente las dos raíces de menor peso hasta consolidar un único árbol con raíz de peso total $N = 36$.

##### 1. Bosque Inicial (17 nodos hoja)
* Peso 1: `[E:1, G:1, I:1, L:1, N:1, S:1, T:1, V:1, Z:1]`
* Peso 2: `[B:2, C:2, D:2, M:2]`
* Peso 3: `[R:3, _:3]`
* Peso 4: `[O:4]`
* Peso 9: `[A:9]`

---

##### 2. Trazado de Iteraciones (Fusión en Min-Heap)

Convención de aristas: **Hijo izquierdo = `0`**, **Hijo derecho = `1`**.

* **Paso 1:** Se extraen `E:1` y `G:1`. Se crea nodo interno `N1(peso: 2)`.
* **Paso 2:** Se extraen `I:1` y `L:1`. Se crea nodo interno `N2(peso: 2)`.
* **Paso 3:** Se extraen `N:1` y `S:1`. Se crea nodo interno `N3(peso: 2)`.
* **Paso 4:** Se extraen `T:1` y `V:1`. Se crea nodo interno `N4(peso: 2)`.
* **Paso 5:** Se extrae `Z:1` (último nodo de peso 1) y el siguiente menor disponible `B:2`. Se crea nodo interno `N5(peso: 3)`.
* **Paso 6:** Se extraen `C:2` y `D:2`. Se crea nodo interno `N6(peso: 4)`.
* **Paso 7:** Se extraen `M:2` y `N1:2` (fusión de E y G). Se crea nodo interno `N7(peso: 4)`.
* **Paso 8:** Se extraen `N2:2` (I, L) y `N3:2` (N, S). Se crea nodo interno `N8(peso: 4)`.
* **Paso 9:** Se extraen `N4:2` (T, V) y `N5:3` (Z, B). Se crea nodo interno `N9(peso: 5)`.
* **Paso 10:** Se extraen `R:3` y `_:3`. Se crea nodo interno `N10(peso: 6)`.
* **Paso 11:** Se extraen `O:4` y `N6:4` (C, D). Se crea nodo interno `N11(peso: 8)`.
* **Paso 12:** Se extraen `N7:4` y `N8:4`. Se crea nodo interno `N12(peso: 8)`.
* **Paso 13:** Se extraen `N9:5` y `N10:6`. Se crea nodo interno `N13(peso: 11)`.
* **Paso 14:** Se extraen `N11:8` (hijo izquierdo) y `A:9` (hijo derecho). Se crea nodo interno `N14(peso: 17)`.
* **Paso 15:** Se extraen `N12:8` (hijo izquierdo) y `N13:11` (hijo derecho). Se crea nodo interno `N15(peso: 19)`.
* **Paso 16:** Se extraen las dos últimas raíces: `N14:17` (hijo izquierdo) y `N15:19` (hijo derecho). Se genera la raíz principal `ROOT(peso: 36)`.

---

##### 3. Representación Estructural del Árbol Final

```text
                                [ROOT: 36]
                               /          \
                             0/            \1
                             /              \
                    [N14: 17]                [N15: 19]
                   /         \              /         \
                 0/           \1          0/           \1
                 /             \          /             \
            [N11: 8]         [A: 9]   [N12: 8]         [N13: 11]
           /        \                 /      \          /       \
         0/          \1             0/        \1      0/         \1
         /            \             /          \      /           \
      [O: 4]        [N6: 4]     [N7: 4]     [N8: 4] [N9: 5]     [N10: 6]
                   /       \     /    \     /    \   /    \      /     \
                  C:2     D:2  M:2   N1:2 N2:2  N3:2 N4:2 N5:3  R:3     _:3
                                     /  \  / \   / \  / \  / \
                                    E:1 G:1 I:1 L:1 N:1 S:1 T:1 V:1 Z:1 B:2
```

---

#### D. Tabla de Códigos Generada, Longitud Promedio y Desigualdad de Shannon

Recorriendo el árbol desde la raíz hacia cada una de las 17 hojas (donde $l_i = |c_i|$ representa la longitud en bits de la palabra de código binario):

| Símbolo ($c_i$) | Frecuencia ($f_i$) | Probabilidad ($p_i$) | Código Binario | Longitud ($l_i$) | Aporte longitud ($f_i \cdot l_i$) | Aporte ponderado ($p_i \cdot l_i$) |
| :-------------: | :----------------: | :------------------: | :------------: | :--------------: | :-------------------------------: | :--------------------------------: |
|      **A**      |         9          |      $0.250000$      |      `01`      |        2         |                 18                |             $0.500000$             |
|      **O**      |         4          |      $0.111111$      |     `000`      |        3         |                 12                |             $0.333333$             |
|      **R**      |         3          |      $0.083333$      |     `1110`     |        4         |                 12                |             $0.333333$             |
|      **\_**     |         3          |      $0.083333$      |     `1111`     |        4         |                 12                |             $0.333333$             |
|      **B**      |         2          |      $0.055556$      |    `11011`     |        5         |                 10                |             $0.277778$             |
|      **C**      |         2          |      $0.055556$      |     `0010`     |        4         |                 8                 |             $0.222222$             |
|      **D**      |         2          |      $0.055556$      |     `0011`     |        4         |                 8                 |             $0.222222$             |
|      **M**      |         2          |      $0.055556$      |     `1000`     |        4         |                 8                 |             $0.222222$             |
|      **E**      |         1          |      $0.027778$      |    `10010`     |        5         |                 5                 |             $0.138889$             |
|      **G**      |         1          |      $0.027778$      |    `10011`     |        5         |                 5                 |             $0.138889$             |
|      **I**      |         1          |      $0.027778$      |    `10100`     |        5         |                 5                 |             $0.138889$             |
|      **L**      |         1          |      $0.027778$      |    `10101`     |        5         |                 5                 |             $0.138889$             |
|      **N**      |         1          |      $0.027778$      |    `10110`     |        5         |                 5                 |             $0.138889$             |
|      **S**      |         1          |      $0.027778$      |    `10111`     |        5         |                 5                 |             $0.138889$             |
|      **T**      |         1          |      $0.027778$      |    `11000`     |        5         |                 5                 |             $0.138889$             |
|      **V**      |         1          |      $0.027778$      |    `11001`     |        5         |                 5                 |             $0.138889$             |
|      **Z**      |         1          |      $0.027778$      |    `11010`     |        5         |                 5                 |             $0.138889$             |
|    **Total**    |       **36**       |    **$1.000000$**    |       —        |        —         |        **133 bits útiles**        |   **$\overline{L} = 3.694444$**    |

##### 1. Cálculo de la Longitud Promedio de Palabra de Código ($\overline{L}$)

$$\overline{L} = \sum_{i=1}^{k} p_i \cdot l_i = \frac{1}{N} \sum_{i=1}^{k} (f_i \cdot l_i) = \frac{133\text{ bits}}{36\text{ caracteres}} = \mathbf{3.694444\text{ bits/símbolo}}$$

##### 2. Verificación de la Desigualdad Fundamental de Shannon

El Teorema de Codificación de Fuente (*Shannon's Source Coding Theorem*) exige que:

$$H(X) \le \overline{L} < H(X) + 1$$

Sustituyendo los valores analíticos obtenidos:

$$3.668839 \le 3.694444 < 3.668839 + 1$$
$$3.668839 \le 3.694444 < 4.668839 \quad \mathbf{[CUMPLE\ SATISFACTORIAMENTE]}$$

* **Redundancia del código:** $R = \overline{L} - H(X) = 3.694444 - 3.668839 = \mathbf{0.025605\text{ bits/símbolo}}$ ($0.70\%$, confirmando una cercanía óptima al límite teórico).
* **Eficiencia del código:** $\eta = \frac{H(X)}{\overline{L}} = \frac{3.668839}{3.694444} \approx \mathbf{99.31\%}$

---

### 2. Diseño Formal del Protocolo de Serialización

El descompresor desconoce el alfabeto original y las probabilidades de la fuente. Por ello, la información del árbol debe viajar empaquetada en la cabecera (*header*) del archivo comprimido antes del flujo de bits de los datos.

```text
+------------------------------------+--------------------------+
|  CABECERA (Metadata/Árbol Huffman) |  CUERPO (Bits codificados)|
+------------------------------------+--------------------------+
```

---

#### Opción A: Guardar la Tabla de Frecuencias Completa

##### Mecanismo
* Se reserva un bloque estático en la cabecera que contiene las frecuencias de los 256 posibles símbolos de la tabla ASCII extendido (bytes de `0x00` a `0xFF`).
* Cada frecuencia se codifica como un entero sin signo de 32 bits (`uint32_t`, 4 bytes), capaz de representar conteos de hasta $2^{32} - 1 \approx 4.29 \times 10^9$ bytes de entrada.
* **Proceso de Descompresión:** El lector lee secuencialmente los 256 enteros de 4 bytes, inserta en un min-heap los símbolos con frecuencia $> 0$ y reproduce exactamente el mismo árbol determinista que usó el compresor.

##### Cálculo de Sobrecarga (Overhead)
$$\text{Sobrecarga} = 256 \text{ símbolos} \times 4 \text{ bytes/símbolo} = \mathbf{1024\text{ bytes}}$$

* **Evaluación en nuestro mensaje:**
  * Tamaño original del mensaje: $36\text{ bytes}$.
  * Flujo de datos comprimido: $\lceil 133 / 8 \rceil = 17\text{ bytes}$.
  * Tamaño total del archivo: $1024 + 17 = \mathbf{1041\text{ bytes}}$.
  * **Ratio de expansión:** $\frac{1041}{36} \times 100\% \approx 2891.67\%$.
  * Produce una **expansión crítica** del archivo debido al costo fijo de almacenar entradas nulas para caracteres inexistentes en el mensaje.

---

#### Opción B: Guardar el Árbol Serializado mediante Recorrido en Preorden

##### Mecanismo
Se aprovecha la topología de árbol binario estricto (*full binary tree*). Se realiza un recorrido en **preorden** (Nodo $\rightarrow$ Subárbol Izquierdo $\rightarrow$ Subárbol Derecho) a nivel de bits:
* **Bit `0`:** Indica un **nodo interno**. No almacena información de carácter; el descompresor sabe que debe instanciar un nodo bifurcador y esperar de forma recursiva a sus dos hijos.
* **Bit `1`:** Indica un **nodo hoja**, seguido inmediatamente por los **8 bits** (`uint8_t`) que representan el valor ASCII del carácter almacenado.

##### Propiedades Matemáticas de un Árbol Huffman con $k$ Hojas
* Todo nodo interno posee exactamente 2 hijos.
* Si el árbol posee $k$ hojas (símbolos únicos en el mensaje), posee exactamente:
  $$I = k - 1 \text{ nodos internos}$$
* El número total de nodos en el árbol es:
  $$N_{\text{nodos}} = k + I = k + (k - 1) = 2k - 1$$

##### Cálculo de Sobrecarga para el Mensaje $\mathcal{M}$ ($k = 17$)
1. **Nodos internos:** $I = 17 - 1 = 16$.
2. **Nodos totales:** $N_{\text{nodos}} = 17 + 16 = 33\text{ nodos}$.
3. **Bits de estructura del árbol:**
   $$33 \text{ nodos} \times 1\text{ bit/nodo} = 33\text{ bits}$$
4. **Bits de datos de hojas (caracteres ASCII):**
   $$17 \text{ hojas} \times 8\text{ bits/carácter} = 136\text{ bits}$$
5. **Total de bits de serialización:**
   $$\text{Bits totales} = 33 + 136 = \mathbf{169\text{ bits}}$$
6. **Sobrecarga en Bytes:**
   $$\text{Sobrecarga} = \left\lceil \frac{169}{8} \right\rceil = \left\lceil 21.125 \right\rceil = \mathbf{22\text{ bytes}}$$
   *(21 bytes completos y 1 bit útil en el byte número 22).*

---

#### Cuadro Comparativo de Sobrecarga de Serialización

| Criterio | Opción A (Tabla de Frecuencias) | Opción B (Árbol en Preorden) | Ventaja |
| :--- | :---: | :---: | :---: |
| **Tamaño de cabecera (en bytes)** | **1024 bytes** (fijo) | **22 bytes** ($\approx 2k$ bytes) | **Opción B (reducción del $97.85\%$)** |
| **Dependencia del tamaño del archivo** | Constante $O(1)$ respecto a $N$, dependiente del alfabeto ($256 \times 4$) | Escala con el número de caracteres únicos: $\lceil (10k - 1)/8 \rceil$ bytes | **Opción B** para alfabetos típicos |
| **Complejidad del Descompresor** | Requiere reconstruir el árbol ejecutando el *min-heap* de nuevo | Reconstrucción recursiva directa $O(k)$ sin necesidad de *priority queue* | **Opción B** (menor tiempo y menor overhead de memoria) |
| **Compresión Neta en $\mathcal{M}$ (36 bytes)** | Total: $1041\text{ bytes}$ (Expansión destructiva) | Cabecera (22 B) + Datos (17 B) = **39 bytes** | **Opción B** es viable aún en textos ultra-cortos |

---

#### Algoritmo de Reconstrucción del Árbol (Opción B)

```cpp
// Pseudocódigo del parser recursivo para el descompresor
std::shared_ptr<HuffmanNode> deserialize_tree(BitReader& reader) {
    bool is_leaf = reader.read_bit();
    if (is_leaf) {
        uint8_t character = reader.read_byte();
        return std::make_shared<HuffmanNode>(character, 0);
    } else {
        auto left_child = deserialize_tree(reader);
        auto right_child = deserialize_tree(reader);
        return std::make_shared<HuffmanNode>(left_child, right_child);
    }
}
```
