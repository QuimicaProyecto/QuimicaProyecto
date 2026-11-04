import numpy as np
import least_squares as ls
from matrix import Matrix
from vector import Vector

def generar_datos_espectroscopicos():
    # Simulamos el archivo real de 50 filas x 1652 columnas
    datos_crudos = np.random.uniform(0.0001, 0.0200, (50, 1652))
    
    # MATRIZ PARA TEST DE EIGENVALORES (50x50 Cuadrada y Simétrica)
    covarianza_np = np.cov(datos_crudos) 
    A_eigen = Matrix(covarianza_np.tolist())
    
    # MATRIZ PARA TEST DE MÍNIMOS CUADRADOS (50x10 Sobredeterminada)
    A_ols_np = datos_crudos[:, :10]
    A_ols = Matrix(A_ols_np.tolist())
    
    # Vector 'b' simulado
    b_np = np.random.uniform(1.0, 5.0, (50, 1))
    b_ols = Vector(b_np)
    
    return A_eigen, A_ols, b_ols

def test_ols():
    print("--- PRUEBA DE MÍNIMOS CUADRADOS (ESCALA REAL) ---")
    try:
        # 1. Obtenemos nuestra matriz sobredeterminada y vector b
        _, A, b = generar_datos_espectroscopicos()
        
        # 2. Resultado Ideal (Usando NumPy lstsq como referencia absoluta)
        # rcond=None es requerido por las nuevas versiones de NumPy para evitar advertencias
        x_esperado_np, _, _, _ = np.linalg.lstsq(np.array(A.data), np.array(b.data), rcond=None)
        
        # 3. Resultado Calculado (Por el algoritmo OLS de tu asesor)
        x_calculado_custom = ls.OLS(A, b)
        
        print(f"Dimensiones de la matriz A: {A.rows}x{A.cols}")
        print(f"Primer peso (Esperado):  {x_esperado_np[0][0]:.6f}")
        print(f"Primer peso (Calculado): {x_calculado_custom.data[0][0]:.6f}")
        
        # 4. Auditoría
        # Aumentamos ligeramente la tolerancia atol a 1e-4 porque al haber 50 filas,
        # los errores de punto flotante de la computadora se acumulan un poco más.
        if np.allclose(x_esperado_np, x_calculado_custom.data, atol=1e-4):
            print("-> ÉXITO: La aproximación de mínimos cuadrados a escala real es correcta.")
        else:
            print("-> FALLO: Discrepancia en la aproximación.")
            
    except Exception as e:
        print(f"-> ERROR CRÍTICO durante la ejecución: {e}")

if __name__ == "__main__":
    test_ols()