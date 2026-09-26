from typing import Any, List, Optional
import random


# Busqueda secuencial
def busqueda_secuencial(arr: List[Any], objetivo: Any) -> Optional[int]:
    
    for i, valor in enumerate(arr):
        if valor == objetivo:
            return i
    return None

# Busqueda binaria
def busqueda_binaria(arr: List[int], objetivo: int) -> Optional[int]:

    inicio = 0
    fin = len(arr) - 1

    while inicio <= fin:
        medio = (inicio + fin) // 2
        if arr[medio] == objetivo:
            return medio
        elif arr[medio] < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1

    return None

# Busqueda por interpolación
def busqueda_interpolacion(arr: List[int], objetivo: int) -> Optional[int]:
    
    inicio = 0
    fin = len(arr) - 1

    # Asegura que el objetivo esté dentro del rango de valores evaluados
    while inicio <= fin and arr[inicio] <= objetivo <= arr[fin]:
        if inicio == fin:
            if arr[inicio] == objetivo:
                return inicio
            return None

        pos = inicio + int(
            ((float(fin - inicio) / (arr[fin] - arr[inicio])) * (objetivo - arr[inicio]))
        )

        if arr[pos] == objetivo:
            return pos
        elif arr[pos] < objetivo:
            inicio = pos + 1
        else:
            fin = pos - 1

    return None


# Busqueda por tabla hash
class TablaHash:

    def __init__(self, tamano: int = 10):
        self.tamano = tamano
        self.tabla = [[] for _ in range(tamano)]

    def _hash(self, clave: Any) -> int:
        return hash(clave) % self.tamano

    def insertar(self, clave: Any, valor: Any) -> None:
        indice = self._hash(clave)
        bucket = self.tabla[indice]

        # Actualizar valor si la clave ya existe en el bucket
        for i, (k, _) in enumerate(bucket):
            if k == clave:
                bucket[i] = (clave, valor)
                return

        # Si no existe, agregar nuevo par (clave, valor)
        bucket.append((clave, valor))

    def buscar(self, clave: Any) -> Optional[Any]:
        
        indice = self._hash(clave)
        bucket = self.tabla[indice]

        for k, v in bucket:
            if k == clave:
                return v
        return None


# Test

datos = []
objetivo = 0

print("Ingrese de que tamaño desea la lista de prueba: ")
tamano = int(input())

for i in range(tamano):
    datos.append(random.randint(1, tamano * 10))

datos.sort()

print(f"Lista de prueba: {datos}")

print("Ingrese el elemento a buscar: ")
objetivo = int(input())

print(f"Elemento a buscar: {objetivo}\n")

# 1. Secuencial
idx_seq = busqueda_secuencial(datos, objetivo)
print(f"Secuencial: encontrado en índice {idx_seq}")

# 2. Binaria
idx_bin = busqueda_binaria(datos, objetivo)
print(f"Binaria: encontrado en índice {idx_bin}")

# 3. Interpolación
idx_interp = busqueda_interpolacion(datos, objetivo)
print(f"Interpolación: encontrado en índice {idx_interp}")

# 4. Tabla Hash
print("\nTabla Hash")
tabla = TablaHash(tamano=5)
tabla.insertar("usuario_1", {"nombre": "Ana", "edad": 28})
tabla.insertar("usuario_2", {"nombre": "Carlos", "edad": 34})
tabla.insertar("usuario_3", {"nombre": "Elena", "edad": 22})

clave_busqueda = "usuario_2"
resultado_hash = tabla.buscar(clave_busqueda)
print(f"Búsqueda por clave '{clave_busqueda}': {resultado_hash}")