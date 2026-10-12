# Apuntes: El Teorema Maestro (*Master Theorem*)

El **Teorema Maestro** es la herramienta matemática más importante en el Análisis de Algoritmos para determinar de manera directa e inmediata la complejidad temporal asintótica ($\Theta$) de los algoritmos recursivos que siguen el paradigma **Divide y Vencerás** (*Divide and Conquer*).

Formulado originalmente por Jon Bentley, Dorothea Haken y James B. Saxe en 1980, y popularizado en el libro *Introduction to Algorithms* (CLRS), funciona como una "fórmula directa" (*cookbook method*) que evita tener que expandir series algebraicas o dibujar árboles de recursión desde cero en cada problema.

---

## 1. Anatomía de la Recurrencia Estándar

El Teorema Maestro se aplica a relaciones de recurrencia que tienen la siguiente forma canónica:

$$T(n) = a\,T\!\left(\frac{n}{b}\right) + f(n)$$

Donde las constantes y funciones tienen un significado físico directo en el comportamiento del algoritmo:

| Símbolo | Condición | Nombre técnico | Significado en el algoritmo y en el código |
|---------|-----------|----------------|--------------------------------------------|
| **$n$** | $n > 0$ | Tamaño de la entrada | Cantidad de datos (longitud de la lista, número de dígitos, dimensión de matriz). |
| **$a$** | $a \ge 1$ (constante) | Factor de ramificación | **Cuántas llamadas recursivas** se ejecutan efectivamente en cada invocación. |
| **$b$** | $b > 1$ (constante) | Factor de reducción | En cuántas partes iguales se **divide el tamaño** de la entrada para cada llamada ($n/b$). |
| **$f(n)$** | Función asintótica positiva | Costo no recursivo (trabajo local) | Tiempo invertido **fuera** de las llamadas recursivas: dividir la entrada $D(n)$ + combinar resultados $C(n)$. |

> **Nota sobre pisos y techos ($\lfloor n/b \rfloor$ y $\lceil n/b \rceil$):** En programación real, al dividir un arreglo de tamaño impar con `n // 2`, un subproblema recibe $\lfloor n/2 \rfloor$ y otro $\lceil n/2 \rceil$. Está demostrado matemáticamente que los pisos y techos **no alteran el comportamiento asintótico**, por lo que el Teorema Maestro permite ignorarlos y escribir simplemente $n/b$.

### El Exponente Crítico y la Función de Hojas
Todo el Teorema Maestro gira en torno a un número fundamental llamado **exponente crítico** ($c_{\text{crit}}$):

$$c_{\text{crit}} = \log_b a$$

A partir de él se define la **función de trabajo en las hojas**:

$$L(n) = n^{\log_b a}$$

Esta expresión representa exactamente **cuántas hojas (casos base)** tiene el árbol de recursión en su último nivel.

---

## 2. De Código en Python a la Ecuación Matemática

Antes de aplicar el teorema, un programador debe saber **extraer $a$, $b$ y $f(n)$ directamente leyendo el código**.

### Reglas de extracción a partir del código:
1. **Para hallar $a$:** Cuenta cuántas llamadas recursivas se llegan a ejecutar **en una misma ejecución** de la función (en el peor caso).
   * *Cuidado:* Si hay llamadas en ramas mutuamente excluyentes (`if ... elif ... else`), solo se ejecuta una de ellas, no la suma de todas.
2. **Para hallar $b$:** Observa cómo disminuye el tamaño de los datos pasados como argumento (ej. `arr[:len(arr)//2]` o `izq, medio` divide el rango entre $2 \implies b = 2$).
3. **Para hallar $f(n)$:** Calcula la complejidad temporal del resto de las líneas de la función (asignaciones $O(1)$, un ciclo `for` de $0$ a $n$ es $\Theta(n)$, dos ciclos anidados de $0$ a $n$ son $\Theta(n^2)$).

### Ejemplos prácticos de extracción

#### Ejemplo A: Conteo directo
```python
def misterio_1(arr):
    n = len(arr)
    if n <= 1:
        return 1
    
    # Dos llamadas recursivas con un tercio del arreglo cada una
    izq = misterio_1(arr[:n // 3])
    der = misterio_1(arr[2 * n // 3:])
    
    # Un bucle lineal de tamaño n para combinar
    suma = 0
    for x in arr:
        suma += x
        
    return izq + der + suma
```
* **¿Cuántas llamadas recursivas se hacen?** $2 \implies \mathbf{a = 2}$.
* **¿Cómo se reduce el tamaño de `arr`?** Se divide entre $3 \implies \mathbf{b = 3}$.
* **¿Cuánto cuesta el resto del código?** El bucle `for` recorre $n$ elementos $\implies \mathbf{f(n) = \Theta(n)}$.
* **Recurrencia resultante:** $T(n) = 2\,T(n/3) + \Theta(n)$.

---

#### Ejemplo B: El error clásico de llamadas duplicadas vs. reutilización
Observa cómo una mínima diferencia en código cambia radicalmente el parámetro $a$:

```python
# ❌ VERSIÓN 1: Dos llamadas recursivas explícitas
def calc_lento(n):
    if n <= 1:
        return 1
    return calc_lento(n // 2) + calc_lento(n // 2)
```
* Aquí el intérprete ejecuta `calc_lento(n // 2)` **dos veces**.
* Parámetros: $a = 2, \; b = 2, \; f(n) = \Theta(1)$.
* Recurrencia: $T(n) = 2\,T(n/2) + \Theta(1) \implies \Theta(n^{\log_2 2}) = \mathbf{\Theta(n)}$.

```python
# ✅ VERSIÓN 2: Una sola llamada guardada en variable
def calc_rapido(n):
    if n <= 1:
        return 1
    mitad = calc_rapido(n // 2)
    return mitad + mitad
```
* Aquí solo se realiza **una** llamada recursiva.
* Parámetros: $a = 1, \; b = 2, \; f(n) = \Theta(1)$.
* Recurrencia: $T(n) = 1\,T(n/2) + \Theta(1) \implies \mathbf{\Theta(\log n)}$.

---

#### Ejemplo C: Ramas condicionales (`if / else`)
```python
def buscar_en_tercios(arr, objetivo, izq, der):
    if izq > der:
        return -1
    tercio = (der - izq) // 3
    m1 = izq + tercio
    m2 = der - tercio
    
    if arr[m1] == objetivo:
        return m1
    elif objetivo < arr[m1]:
        return buscar_en_tercios(arr, objetivo, izq, m1 - 1)
    elif objetivo > arr[m2]:
        return buscar_en_tercios(arr, objetivo, m2 + 1, der)
    else:
        return buscar_en_tercios(arr, objetivo, m1 + 1, m2 - 1)
```
* Aunque la palabra `buscar_en_tercios` aparece 3 veces en el cuerpo, están dentro de un `if / elif / else` **mutuamente excluyente**. En cualquier llamada **solo se ejecuta 1 rama**.
* Por lo tanto, $\mathbf{a = 1}$ (no $3$).

---

## 3. Intuición y Demostración Matemática

Para entender por qué existen exactamente **tres casos** en el Teorema Maestro, basta con observar el **Árbol de Recursión** de $T(n) = a\,T(n/b) + f(n)$:

```
Nivel 0 (Raíz):                 f(n)                       ──► Costo nivel 0:   1 · f(n)
                         /       |       \
Nivel 1:             f(n/b)    f(n/b) ... f(n/b)           ──► Costo nivel 1:   a · f(n/b)
                     / | \     / | \      / | \
Nivel i:           ...   ...    ...        ...             ──► Costo nivel i:   a^i · f(n/b^i)
                   .      .      .          .
Nivel h = log_b(n): [Θ(1)] [Θ(1)] [Θ(1)] ... [Θ(1)]        ──► Costo en hojas:  a^(log_b n) = Θ(n^(log_b a))
```

### Deducción algebraica
1. **Altura del árbol ($h$):** En cada nivel dividimos $n$ entre $b$. Llegamos al caso base de tamaño $1$ cuando $\frac{n}{b^h} = 1 \iff b^h = n \iff \mathbf{h = \log_b n}$.
2. **Cantidad de hojas en la base:** En el nivel $i$ hay $a^i$ nodos. En el último nivel ($i = \log_b n$), la cantidad de hojas es:
   $$a^{\log_b n} = n^{\log_b a}$$
   *(Por la propiedad logarítmica de cambio de base: $a^{\log_b n} = (b^{\log_b a})^{\log_b n} = (b^{\log_b n})^{\log_b a} = n^{\log_b a}$)*.
3. **Suma total del trabajo en todos los niveles:**
   $$T(n) = \underbrace{\Theta(n^{\log_b a})}_{\text{Costo de las hojas}} + \underbrace{\sum_{i=0}^{\log_b n - 1} a^i \, f\!\left(\frac{n}{b^i}\right)}_{\text{Costo de los niveles internos}}$$

Si suponemos que $f(n) = n^k$, el término general dentro de la sumatoria es:
$$a^i \left(\frac{n}{b^i}\right)^k = n^k \left(\frac{a}{b^k}\right)^i$$

Esto es una **serie geométrica** cuya razón es $r = \frac{a}{b^k}$. En una serie geométrica solo pueden ocurrir tres comportamientos al sumar sus términos:

1. **Serie Creciente ($r > 1 \iff a > b^k \iff \log_b a > k$):**
   El trabajo se multiplica nivel tras nivel. El último nivel (las **hojas**) es tan masivo que él solo domina la suma de todos los niveles anteriores juntos $\implies$ **Caso 1**: $T(n) = \Theta(n^{\log_b a})$.
2. **Serie Constante ($r = 1 \iff a = b^k \iff \log_b a = k$):**
   El aumento en el número de subproblemas ($a$) se compensa exactamente con la reducción de su tamaño ($b^k$). **Cada nivel del árbol cuesta exactamente lo mismo** ($n^k$). Como hay $\log_b n$ niveles, el total es $(\text{costo por nivel}) \times (\text{altura}) \implies$ **Caso 2**: $T(n) = \Theta(n^{\log_b a} \log n)$.
3. **Serie Decreciente ($r < 1 \iff a < b^k \iff \log_b a < k$):**
   El trabajo disminuye tan rápido al bajar de nivel que el **primer nivel (la raíz)** concentra la mayor parte del costo total $\implies$ **Caso 3**: $T(n) = \Theta(f(n))$.

---

## 4. Enunciado Formal de los Tres Casos

Sea $T(n) = a\,T(n/b) + f(n)$ con constantes $a \ge 1$ y $b > 1$. Calculamos la función crítica de hojas $n^{\log_b a}$ y la comparamos con $f(n)$:

---

### Caso 1: Dominan las hojas ($n^{\log_b a}$ es polinomialmente mayor que $f(n)$)
* **Condición formal:** Existe una constante $\varepsilon > 0$ tal que:
  $$f(n) = O\!\left(n^{\log_b a - \varepsilon}\right)$$
* **Significado:** $f(n)$ crece más lento que $n^{\log_b a}$ por al menos un factor polinómico $n^\varepsilon$.
* **Solución:**
  $$\boxed{T(n) = \Theta\!\left(n^{\log_b a}\right)}$$

---

### Caso 2: Equilibrio entre hojas y niveles ($f(n)$ y $n^{\log_b a}$ crecen igual salvo factores logarítmicos)
* **Condición formal (Versión Estándar y Extendida):** Existe una constante $p \ge 0$ tal que:
  $$f(n) = \Theta\!\left(n^{\log_b a} \log^p n\right)$$
  *(Nota: El caso más habitual ocurre cuando $p = 0$, es decir, $f(n) = \Theta(n^{\log_b a})$ simplemente).*
* **Solución:** Se multiplica por un factor adicional $\log n$:
  $$\boxed{T(n) = \Theta\!\left(n^{\log_b a} \log^{p+1} n\right)}$$
  *(En particular, para $p = 0$: $\mathbf{T(n) = \Theta(n^{\log_b a} \log n)}$).*

---

### Caso 3: Domina la raíz ($f(n)$ es polinomialmente mayor que $n^{\log_b a}$)
* **Condición 1 (Cota inferior polinómica):** Existe una constante $\varepsilon > 0$ tal que:
  $$f(n) = \Omega\!\left(n^{\log_b a + \varepsilon}\right)$$
* **Condición 2 (Condición de Regularidad):** Existe una constante $c < 1$ y un umbral $n_0$ tal que para todo $n \ge n_0$:
  $$a\,f\!\left(\frac{n}{b}\right) \le c\,f(n)$$
  *(Garantiza que la suma del trabajo de los hijos en el nivel 1 sea estrictamente una fracción menor que el trabajo del padre en la raíz).*
* **Solución:**
  $$\boxed{T(n) = \Theta\!\left(f(n)\right)}$$

---

## 5. Método Rápido (Fórmula de Bolsillo para Exámenes)

En más del $95\%$ de los problemas prácticos y de examen, la función $f(n)$ tiene la forma polinómica-logarítmica:

$$f(n) = \Theta\!\left(n^k \log^p n\right) \quad \text{con } k \ge 0$$

En este escenario, ni siquiera necesitas buscar $\varepsilon$ ni verificar la condición de regularidad (pues se cumple automáticamente para polinomios). Solo debes comparar dos números: **$\log_b a$** contra **$k$**:

| Comparación entre $\log_b a$ y $k$ | Caso | Complejidad resultante $T(n)$ |
|------------------------------------|------|-------------------------------|
| **$\log_b a > k$** | **Caso 1** (Ganan las hojas) | $\Theta\!\left(n^{\log_b a}\right)$ |
| **$\log_b a = k$** (con $p \ge 0$) | **Caso 2** (Empate) | $\Theta\!\left(n^k \log^{p+1} n\right)$ |
| **$\log_b a = k$** (con $p = -1$) | **Caso 2 esp.** | $\Theta\!\left(n^k \log \log n\right)$ |
| **$\log_b a = k$** (con $p < -1$) | **Caso 2 esp.** | $\Theta\!\left(n^k\right)$ |
| **$\log_b a < k$** | **Caso 3** (Gana $f(n)$) | $\Theta\!\left(n^k \log^p n\right) = \Theta(f(n))$ |

---

## 6. Ejemplos Resueltos Paso a Paso

### Ejemplo 1: $T(n) = 9\,T(n/3) + n$
1. **Identificar parámetros:** $a = 9$, $b = 3$, $f(n) = n \implies k = 1, p = 0$.
2. **Calcular exponente crítico:** $\log_b a = \log_3 9 = 2$. Función de hojas: $n^2$.
3. **Comparar:** $\log_b a = 2 > k = 1$.
   * Verificación formal: $f(n) = n = O(n^{2 - \varepsilon})$ eligiendo $\varepsilon = 1 > 0$.
4. **Conclusión:** Aplica el **Caso 1**.
   $$T(n) = \Theta(n^2)$$

---

### Ejemplo 2: $T(n) = T(2n/3) + 1$ (Estilo Búsqueda Binaria / Reducción fraccionaria)
1. **Identificar parámetros:** Nota que $2n/3 = \frac{n}{3/2}$. Por tanto:
   $$a = 1, \quad b = \frac{3}{2} = 1.5, \quad f(n) = 1 = n^0 \implies k = 0, p = 0$$
2. **Calcular exponente crítico:** $\log_{3/2} 1 = 0$. Función de hojas: $n^0 = 1$.
3. **Comparar:** $\log_b a = 0 = k$.
4. **Conclusión:** Aplica el **Caso 2** (con $p = 0$).
   $$T(n) = \Theta(n^0 \log^{0+1} n) = \Theta(\log n)$$

---

### Ejemplo 3: $T(n) = 2\,T(n/2) + n \log n$
1. **Identificar parámetros:** $a = 2$, $b = 2$, $f(n) = n^1 \log^1 n \implies k = 1, p = 1$.
2. **Calcular exponente crítico:** $\log_2 2 = 1$. Función de hojas: $n^1 = n$.
3. **Comparar:** $\log_b a = 1 = k$, pero con un factor logarítmico adicional ($p = 1$).
4. **Conclusión:** Aplica el **Caso 2 extendido** ($p = 1$).
   $$T(n) = \Theta(n^1 \log^{1+1} n) = \Theta(n \log^2 n)$$

---

### Ejemplo 4: $T(n) = 3\,T(n/4) + n \log n$
1. **Identificar parámetros:** $a = 3$, $b = 4$, $f(n) = n \log n \implies k = 1, p = 1$.
2. **Calcular exponente crítico:** $\log_4 3 \approx 0.7925$. Función de hojas: $n^{0.7925}$.
3. **Comparar:** $\log_b a \approx 0.7925 < k = 1$.
   * Cota inferior: $f(n) = \Omega(n^{\log_4 3 + \varepsilon})$ tomando $\varepsilon \approx 0.2 > 0$.
   * **Verificación de la Condición de Regularidad:**
     $$a\,f(n/b) = 3 \left(\frac{n}{4}\right) \log\!\left(\frac{n}{4}\right) \le \frac{3}{4} n \log n = c\,f(n)$$
     Para $c = 3/4 = 0.75 < 1$, la desigualdad se cumple para todo $n \ge 4$.
4. **Conclusión:** Aplica el **Caso 3**.
   $$T(n) = \Theta(n \log n)$$

---

### Ejemplo 5: $T(n) = 7\,T(n/2) + n^2$ (Algoritmo de Strassen para Matrices)
1. **Identificar parámetros:** $a = 7$, $b = 2$, $f(n) = n^2 \implies k = 2$.
2. **Calcular exponente crítico:** $\log_2 7 \approx 2.807$. Función de hojas: $n^{\log_2 7}$.
3. **Comparar:** $\log_b a \approx 2.807 > k = 2$.
4. **Conclusión:** Aplica el **Caso 1** (con $\varepsilon = 0.8$).
   $$T(n) = \Theta(n^{\log_2 7}) \approx \Theta(n^{2.807})$$

---

## 7. ¿Cuándo NO se puede aplicar el Teorema Maestro? (Limitaciones y Trampas)

Es tan importante saber usar el Teorema Maestro como reconocer las ecuaciones donde **es inválido aplicarlo**:

### 1. Reducción aritmética en lugar de geométrica (*Subtract and Conquer*)
* **Ejemplo:** $T(n) = 2\,T(n - 1) + 1$ (Torres de Hanoi) o $T(n) = T(n - 1) + n$ (Insertion Sort recursivo).
* **Por qué no aplica:** El tamaño no se divide por $b$ ($n/b$), sino que se resta una constante ($n - c$).
* **Cómo se resuelve:** Por expansión/sustitución hacia atrás. Sus complejidades son $\Theta(2^n)$ y $\Theta(n^2)$ respectivamente.

### 2. Parámetros $a$ o $b$ que no son constantes válidas
* **Ejemplo:** $T(n) = 2^n T(n/2) + n^n$ o $T(n) = 0.5\,T(n/2) + n$.
* **Por qué no aplica:** En el primero, $a = 2^n$ depende de $n$ (no es constante); en el segundo, $a = 0.5 < 1$ (no puedes hacer media llamada recursiva).

### 3. El "Hueco Polinómico" (*Polynomial Gap*)
El Caso 1 y el Caso 3 exigen una diferencia **polinómica** ($n^{\pm \varepsilon}$), no simplemente una diferencia logarítmica.
* **Ejemplo clásico de examen:**
  $$T(n) = 2\,T(n/2) + \frac{n}{\log n}$$
* **Análisis:**
  * Aquí $a = 2, b = 2 \implies n^{\log_2 2} = n$.
  * $f(n) = \frac{n}{\log n} = n^1 \log^{-1} n$.
  * ¿Es Caso 1? La razón $\frac{n}{f(n)} = \log n$. Pero $\log n$ crece **más lento que cualquier polinomio $n^\varepsilon$** para todo $\varepsilon > 0$. Por lo tanto, $f(n)$ **no** es polinomialmente menor que $n$; cae en el "hueco" entre el Caso 1 y el Caso 2 estándar.
* **Solución mediante la extensión de Caso 2 ($p = -1$):**
  Al sumar el árbol de recursión nivel por nivel:
  $$T(n) = \sum_{i=0}^{\log_2 n - 1} 2^i \frac{n/2^i}{\log_2(n/2^i)} = n \sum_{i=0}^{\log_2 n - 1} \frac{1}{\log_2 n - i} = n \sum_{j=1}^{\log_2 n} \frac{1}{j} = \Theta(n \log \log n)$$
  *(Pues $\sum_{j=1}^m \frac{1}{j} = H_m = \Theta(\log m)$ es la serie armónica con $m = \log_2 n$).*

### 4. Violación de la Condición de Regularidad en el Caso 3
* **Ejemplo:** $T(n) = 2\,T(n/2) + n^2(2 - \cos n)$.
* Aunque $f(n) = \Omega(n^{1+\varepsilon})$, la oscilación trigonométrica impide que exista una constante fija $c < 1$ tal que $2 f(n/2) \le c f(n)$ para todo $n$.

### 5. Subproblemas de tamaños desiguales
* **Ejemplo:** $T(n) = T(n/3) + T(2n/3) + n$ (Quick Sort con partición desbalanceada 1:2).
* **Por qué no aplica:** Los subproblemas tienen factores de división distintos ($b_1 = 3$ y $b_2 = 3/2$).
* **Cómo se resuelve:** Con la generalización del Teorema Maestro llamada **Método de Akra-Bazzi**.

---

## 8. Generalización: El Método de Akra-Bazzi

Cuando un algoritmo divide el problema en fracciones desiguales:

$$T(n) = \sum_{i=1}^k a_i \, T(b_i n) + f(n) \quad \text{con } a_i > 0 \text{ y } 0 < b_i < 1$$

El teorema de **Akra-Bazzi** (1998) establece que:
1. Primero se encuentra el único exponente real $p$ que satisface la ecuación característica:
   $$\sum_{i=1}^k a_i \, b_i^p = 1$$
2. Luego la complejidad asintótica viene dada directamente por la integral:
   $$T(n) = \Theta\!\left(n^p \left(1 + \int_1^n \frac{f(u)}{u^{p+1}} \, du\right)\right)$$

**Ejemplo con $T(n) = T(n/3) + T(2n/3) + n$:**
* Ecuación para $p$: $\left(\frac{1}{3}\right)^p + \left(\frac{2}{3}\right)^p = 1 \implies \mathbf{p = 1}$.
* Sustituyendo en la integral con $f(u) = u$:
  $$T(n) = \Theta\!\left(n^1 \left(1 + \int_1^n \frac{u}{u^2} \, du\right)\right) = \Theta\!\left(n (1 + \ln n)\right) = \mathbf{\Theta(n \log n)}$$

---

## 9. Herramienta en Python: Solucionador y Verificador Empírico

A continuación se presenta un programa completo en Python que:
1. **Resuelve simbólicamente** cualquier recurrencia $T(n) = a\,T(n/b) + \Theta(n^k \log^p n)$ explicando qué caso aplica.
2. **Verifica empíricamente** el resultado ejecutando la recurrencia numérica real y comprobando que el cociente $\frac{T(n)}{\text{Cota Teórica}(n)}$ converge a una constante positiva conforme $n \to \infty$.

```python
import math
from functools import lru_cache


def resolver_teorema_maestro(a: float, b: float, k: float, p: float = 0.0) -> str:
    """
    Resuelve simbólicamente T(n) = a * T(n/b) + Θ(n^k * log^p(n))
    y devuelve el diagnóstico detallado del Teorema Maestro.
    """
    if a < 1 or b <= 1:
        raise ValueError("El Teorema Maestro requiere a >= 1 y b > 1.")

    c_crit = math.log(a, b)
    tol = 1e-9

    # Formateo limpio del exponente crítico
    exp_str = f"{round(c_crit)}" if abs(c_crit - round(c_crit)) < tol else f"{c_crit:.4f}"

    print(f"Recurrencia: T(n) = {a} T(n/{b}) + Θ(n^{k} log^{p} n)")
    print(f"  -> Exponente crítico: log_{b}({a}) = {exp_str}")
    print(f"  -> Función de hojas : n^({exp_str})")

    # CASO 1: log_b(a) > k
    if c_crit > k + tol:
        resultado = f"Θ(n^{exp_str})" if exp_str != "1" else "Θ(n)"
        caso = "Caso 1 (Dominan las hojas: log_b(a) > k)"

    # CASO 2: log_b(a) == k
    elif abs(c_crit - k) <= tol:
        base_n = "" if abs(k) < tol else (f"n^{round(k)} " if abs(k - 1) > tol else "n ")
        if p > -1 + tol:
            nuevo_p = round(p + 1) if abs((p + 1) - round(p + 1)) < tol else p + 1
            log_str = "log n" if nuevo_p == 1 else f"log^{nuevo_p} n"
            resultado = f"Θ({base_n}{log_str})"
            caso = f"Caso 2 (Equilibrio en niveles: log_b(a) == k, p={p})"
        elif abs(p - (-1)) <= tol:
            resultado = f"Θ({base_n}log log n)"
            caso = "Caso 2 Extendido (Hueco armónico: p = -1)"
        else:
            resultado = f"Θ({base_n.strip() or '1'})"
            caso = "Caso 2 Extendido (p < -1, convergente a las hojas)"

    # CASO 3: log_b(a) < k
    else:
        base_n = f"n^{round(k)}" if abs(k - 1) > tol else "n"
        log_str = "" if abs(p) < tol else (" log n" if abs(p - 1) < tol else f" log^{p} n")
        resultado = f"Θ({base_n}{log_str})"
        caso = "Caso 3 (Domina la raíz f(n): log_b(a) < k)"

    print(f"  -> Diagnóstico      : {caso}")
    print(f"  -> Complejidad      : T(n) = {resultado}\n")
    return resultado


def verificar_empiricamente(a: int, b: int, f_func, cota_teorica_func, niveles: int = 10):
    """
    Evalúa numéricamente la recurrencia exacta T(n) para potencias n = b^i
    y muestra que T(n) / Cota(n) converge a una constante (definición de Θ).
    """
    @lru_cache(maxsize=None)
    def T(n: int) -> float:
        if n <= 1:
            return 1.0
        return a * T(n // b) + f_func(n)

    print(f"{'n':>10} | {'T(n) Exacto':>16} | {'Cota g(n)':>16} | {'Razón T(n)/g(n)':>15}")
    print("-" * 65)
    for i in range(1, niveles + 1):
        n = b ** i
        val_t = T(n)
        val_g = cota_teorica_func(n)
        razon = val_t / val_g
        print(f"{n:10d} | {val_t:16.2f} | {val_g:16.2f} | {razon:15.6f}")
    print()


if __name__ == "__main__":
    # 1. Merge Sort: T(n) = 2T(n/2) + n
    resolver_teorema_maestro(a=2, b=2, k=1, p=0)
    verificar_empiricamente(
        a=2, b=2,
        f_func=lambda n: n,
        cota_teorica_func=lambda n: n * math.log2(n)
    )

    # 2. Karatsuba: T(n) = 3T(n/2) + n
    resolver_teorema_maestro(a=3, b=2, k=1, p=0)
    verificar_empiricamente(
        a=3, b=2,
        f_func=lambda n: n,
        cota_teorica_func=lambda n: n ** math.log2(3)
    )
```

---

## 10. Ejercicios de Práctica (Con Soluciones)

Determina la complejidad asintótica de las siguientes relaciones de recurrencia utilizando el Teorema Maestro (o indica por qué no aplica):

1. $T(n) = 4\,T(n/2) + n$
2. $T(n) = 4\,T(n/2) + n^2$
3. $T(n) = 4\,T(n/2) + n^3$
4. $T(n) = 16\,T(n/4) + n!$
5. $T(n) = 2\,T(n/4) + \sqrt{n}$
6. $T(n) = 2\,T(n/2) + n \log^2 n$
7. $T(n) = 3\,T(n/3) + \frac{n}{2}$
8. $T(n) = 64\,T(n/8) - n^2 \log n$
9. $T(n) = T(n - 2) + n^2$
10. $T(n) = 2\,T(\sqrt{n}) + \log n$ *(Sugerencia: hacer cambio de variable $m = \log_2 n$)*

---

### Soluciones Detalladas

1. **$T(n) = 4\,T(n/2) + n$:**
   * $\log_2 4 = 2 > k = 1 \implies$ **Caso 1** $\implies \mathbf{\Theta(n^2)}$.
2. **$T(n) = 4\,T(n/2) + n^2$:**
   * $\log_2 4 = 2 = k = 2$ ($p=0$) $\implies$ **Caso 2** $\implies \mathbf{\Theta(n^2 \log n)}$.
3. **$T(n) = 4\,T(n/2) + n^3$:**
   * $\log_2 4 = 2 < k = 3$. Regularidad: $4(n/2)^3 = \frac{4}{8}n^3 = 0.5 n^3 \le c n^3$ con $c=0.5 < 1 \implies$ **Caso 3** $\implies \mathbf{\Theta(n^3)}$.
4. **$T(n) = 16\,T(n/4) + n!$:**
   * $\log_4 16 = 2$. Como $n!$ crece muchísimo más rápido que $n^2$ y cumple regularidad $\implies$ **Caso 3** $\implies \mathbf{\Theta(n!)}$.
5. **$T(n) = 2\,T(n/4) + \sqrt{n}$:**
   * Nota que $\sqrt{n} = n^{1/2} = n^{0.5}$. Además $\log_4 2 = \frac{1}{2} = 0.5$.
   * Como $\log_4 2 = 0.5 = k \implies$ **Caso 2** $\implies \mathbf{\Theta(\sqrt{n} \log n)}$.
6. **$T(n) = 2\,T(n/2) + n \log^2 n$:**
   * $\log_2 2 = 1 = k$, con $p = 2 \implies$ **Caso 2 extendido** $\implies \mathbf{\Theta(n \log^3 n)}$.
7. **$T(n) = 3\,T(n/3) + \frac{n}{2}$:**
   * Las constantes multiplicativas en $f(n)$ se ignoran ($n/2 = \Theta(n)$). $\log_3 3 = 1 = k \implies$ **Caso 2** $\implies \mathbf{\Theta(n \log n)}$.
8. **$T(n) = 64\,T(n/8) - n^2 \log n$:**
   * **No aplica el Teorema Maestro** porque $f(n) = -n^2 \log n$ es **negativa** (el tiempo de trabajo local no puede ser negativo).
9. **$T(n) = T(n - 2) + n^2$:**
   * **No aplica el Teorema Maestro** directamente porque la reducción es aritmética ($n - 2$), no geométrica ($n/b$). Expandiendo la suma de cuadrados de 2 en 2 se obtiene $\mathbf{\Theta(n^3)}$.
10. **$T(n) = 2\,T(\sqrt{n}) + \log n$:**
    * A simple vista no tiene la forma $T(n/b)$, pero haciendo el **cambio de variable** $n = 2^m \iff m = \log_2 n$, tenemos $\sqrt{n} = 2^{m/2}$:
      $$T(2^m) = 2\,T(2^{m/2}) + m$$
    * Definiendo $S(m) = T(2^m)$, la recurrencia se transforma en:
      $$S(m) = 2\,S(m/2) + m$$
    * Ahora sí aplicamos el Teorema Maestro a $S(m)$: $a=2, b=2, f(m)=m \implies$ **Caso 2**: $S(m) = \Theta(m \log m)$.
    * Regresando a la variable original $n$ ($m = \log n$):
      $$\mathbf{T(n) = \Theta(\log n \cdot \log \log n)}$$
