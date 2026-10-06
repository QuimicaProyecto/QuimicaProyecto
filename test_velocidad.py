import pandas as pd
import numpy as np
import time
import sys

# Expande el límite de recursividad de Python para el test
sys.setrecursionlimit(100000)

import Utils as U

# Cargar el archivo Excel
archivo = "Datos espectroscópicos SORS Tequila/MatrDat_TB-TBM-SORS_v0.2.xlsx"
print("Cargando archivo, por favor espera...")
df = pd.read_excel(archivo, sheet_name=0)

# Comprobación visual de los datos
print("\n--- VERIFICACIÓN DE DATOS ---")
print(f"Filas encontradas: {df.shape[0]}")
print(f"Columnas encontradas: {df.shape[1]}")

# Extraer solo los números y aplanar a una sola dimensión
datos_completos = df.select_dtypes(include="number").values.flatten()
print(f"Total de celdas numéricas a ordenar: {datos_completos.size}\n")

# Crear copias para la prueba
datos_para_numpy = datos_completos.copy()
datos_para_quicksort = datos_completos.copy()

# 3. Prueba NumPy
print("Ordenando con NumPy...")
inicio_numpy = time.perf_counter()
np.sort(datos_para_numpy)
tiempo_numpy = time.perf_counter() - inicio_numpy

# 4. Prueba QuickSort
print("Ordenando con QuickSort in place...")
try:
    inicio_quick = time.perf_counter()
    U.quicksort_in_place(datos_para_quicksort)
    tiempo_quick = time.perf_counter() - inicio_quick
    exito_quick = True
except RecursionError:
    print("[ERROR] QuickSort falló por RecursionError. Demasiados datos para Python puro.")
    exito_quick = False

# 5. Resultados
print("\n--- RESULTADOS ---")
print(f"NumPy:     {tiempo_numpy:.6f} segundos")
if exito_quick:
    print(f"QuickSort: {tiempo_quick:.6f} segundos")
    print(f"NumPy es {tiempo_quick / tiempo_numpy:.0f} veces más rápido.")