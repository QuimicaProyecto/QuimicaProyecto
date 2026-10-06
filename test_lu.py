import numpy as np
import scipy.linalg as la
import time
import LU as custom_lu
from matrix import Matrix

# 1. Generar una matriz cuadrada de prueba (ej. 150x150)
n = 150
datos_crudos = np.random.rand(n, n)
matriz_prueba = Matrix(datos_crudos.tolist())

print("Ejecutando algoritmo del asesor...")
inicio_custom = time.perf_counter()
det_custom = custom_lu.determinant(matriz_prueba)
tiempo_custom = time.perf_counter() - inicio_custom

# 3. Librerías SciPy/NumPy
print("Ejecutando NumPy/SciPy...")
inicio_nativas = time.perf_counter()
# SciPy maneja la descomposición LU (no es la nuestra)
P, L, U = la.lu(datos_crudos)
# NumPy calcula el determinante
det_np = np.linalg.det(datos_crudos)
tiempo_nativas = time.perf_counter() - inicio_nativas

# 4. Resultados de la competencia
print("\n--- PRUEBA DE EXACTITUD ---")
print(f"Determinante Asesor: {det_custom}")
print(f"Determinante NumPy:  {det_np}")

# Verificamos si los números coinciden (NumPy usa isclose para ignorar diferencias minúsculas de decimales)
if np.isclose(det_custom, det_np):
    print("La fórmula es matemáticamente perfecta.")
else:
    print("Los resultados no coinciden.")

print("\n--- PRUEBA DE RENDIMIENTO ---")
print(f"Tiempo código custom: {tiempo_custom:.6f} segundos")
print(f"Tiempo Nativas: {tiempo_nativas:.6f} segundos")

if tiempo_nativas > 0:
    diferencia = tiempo_custom / tiempo_nativas
    print(f"\nConclusión: Las librerías de código abierto fueron {diferencia:.0f} veces más rápidas.")