import numpy as np
from vector import Vector

def prueba_integridad_vector():
    print("--- PRUEBA DE INTEGRIDAD: CÓDIGO ORIGINAL VS CÓDIGO OPTIMIZADO ---")

    # 1. Datos simulados
    datos_a = [[0.0152], [0.0047], [0.0198], [0.0061], [0.0114]]
    datos_b = [[0.0104], [0.0087], [0.0072], [0.0064], [0.0126]]

    vec_A = Vector(datos_a)
    vec_B = Vector(datos_b)

    # 2. Cálculos con la lógica original
    norma_orig = vec_A.norm()
    punto_orig = vec_A.dot_product(vec_B)
    normalizado_orig = vec_A.normalization().data

    # 3. Cálculos con la lógica de numpy
    arr_A = np.array(datos_a)
    arr_B = np.array(datos_b)

    norma_opt = np.sqrt(np.sum(arr_A**2)).item()
    punto_opt = np.sum(arr_A * arr_B).item()
    normalizado_opt = (arr_A / norma_opt).tolist()

    # 4. Prueba
    print(f"\n1. Prueba de Norma:")
    print(f"Original:   {norma_orig}")
    print(f"Optimizado: {norma_opt}")
    print("-> MATCH PERFECTO" if np.isclose(norma_orig, norma_opt, atol=1e-15) else "-> DISCREPANCIA")

    print(f"\n2. Prueba de Producto Punto:")
    print(f"Original:   {punto_orig}")
    print(f"Optimizado: {punto_opt}")
    print("-> MATCH PERFECTO" if np.isclose(punto_orig, punto_opt, atol=1e-15) else "-> DISCREPANCIA")

    print(f"\n3. Prueba de Normalización (Muestra del primer elemento):")
    print(f"Original:   {normalizado_orig[0]}")
    print(f"Optimizado: {normalizado_opt[0]}")
    print("-> MATCH PERFECTO" if np.allclose(normalizado_orig, normalizado_opt, atol=1e-15) else "-> DISCREPANCIA")

if __name__ == "__main__":
    prueba_integridad_vector()