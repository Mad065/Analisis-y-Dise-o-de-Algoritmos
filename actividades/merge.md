# Respuesta

# Prueba de escritorio
Este es el algoritmo de ordenamiento por merge donde se van agarrando bloques cada vez mas grandes para ordenar los elemento de cada uno por separado y despues juntarlos asi obteniendo la lista ordenada, compara una mitad del bloque con la otra y y asi va ordenando la lista de menor a mayorpara esto necesita izq que nos da el inicio de la primera mitad med que nos da el inicio de la segunda mitad y der que nos da el final asi compara los elementos del bloque de la izquierda con los de la derceha y los ordena despues sigue con bloques mas grandes hasta terminar

Las lineas


if (med >= n - 1) continue;
if (der > n - 1) der = n - 1;     
soin clave dado que estas ayudan a hacer que los arreglos no necesiten ser potencia de 2 y el otro hace que solo se evalue lo necesario evitando bloques de mayor tamaño al del arreglo

# Calculo de complejidad

En el calculo de complejidad la funcion merge tiene complejidad n dado que analiza todos los elementos del bloque dado y la funcion merge_sort_iterativo es mas interesante dado que en esta tenemos 2 for anidados que podria ser simplemente n^2 pero dado que los incrementos de la variable no son de 1 en 1 esto cambia dado que el incremento es 

ancho = 2 * ancho donde ancho = n entonces esto es 2^n y para que termine el ciclo se debe cumplir que 2^n >= n entonces tenemos n√n

en el segundo for tenemos algo similar

izq = izq + 2 * ancho donde izq = n entonces tenemos n + 2n como para detener el for necesitamos izq > n entonces tenemos 2n >= n obteniendo simplemente n, tampoco deberiamos olvidar el hecho de que en este for se ejecuta el merge pero como tambien es n solo se suma y por reglas no cambia nada y con eso ahora podemos decir que los for tienen complejidad n√n x n  

# Comparacion con IA