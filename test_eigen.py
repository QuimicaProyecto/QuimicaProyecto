import numpy as np
import eigen as eg
from matrix import Matrix

# --- GENERAR MATRIZ CON EIGENVALORES "RESUELTOS" ---
def generar_matriz_con_eigenvalores(eigenvalores_deseados):
    """
    Construye una matriz simétrica que garantiza tener
    exactamente los eigenvalores especificados.
    """
    n = len(eigenvalores_deseados)
    
    # Creamos una matriz diagonal con los eigenvalores que inventaste
    D = np.diag(eigenvalores_deseados)
    
    # Generamos una matriz aleatoria ortogonal
    # Usamos np.linalg.qr para asegurar que Q sea ortogonal matemáticamente perfecta
    H = np.random.rand(n, n)
    Q, _ = np.linalg.qr(H)
    
    # Aplicamos el Teorema Espectral: A = Q * D * Q.T
    # El resultado es una matriz densa que esconde exactamente los eigenvalores.
    A_np = Q @ D @ Q.T
    
    # Esto asegura la simetría estricta para evitar errores de punto flotante microscópicos
    A_np = (A_np + A_np.T) / 2
    
    return A_np


def test_eigenvalues_auditoria():
    print("--- PRUEBA UNITARIA: ALGORITMO QR DE EIGENVALORES ---")
    
    # CASO 1: Prueba de regresión con eigenvalores conocidos (Matriz Pequeña para Depuración)
    eigen_conocidos_caso1 = [25.0, 10.0, 5.0, 1.0, 0.1]
    
    print("\n[Caso 1] Matriz 5x5 con Eigenvalores controlados")
    A_np_1 = generar_matriz_con_eigenvalores(eigen_conocidos_caso1)
    A_matrix_1 = Matrix(A_np_1.tolist())
    
    try:
        # Ejecutamos el algoritmo de eigenvalores
        eigen_calculados_1 = eg.eigen_vals(A_matrix_1, max_iter=2000)
        
        assert len(eigen_calculados_1) == len(eigen_conocidos_caso1), f"Fallo dimensional. Esperaba {len(eigen_conocidos_caso1)}, recibió {len(eigen_calculados_1)}"
        
        # Comparamos cada eigenvalor calculado con los eigenvalores conocidos
        # Ordenamos ambos de mayor a menor para emparejarlos
        calculados_ord = sorted(eigen_calculados_1, reverse=True)
        conocidos_ord = sorted(eigen_conocidos_caso1, reverse=True)
        
        print("Resultados:")
        for real, calc in zip(conocidos_ord, calculados_ord):
            print(f" Esperado: {real:8.4f} | Calculado: {calc:8.4f}")
            
        # Prueba de validación
        assert np.allclose(conocidos_ord, calculados_ord, atol=1e-15), "Los cálculos divergieron de los eigenvalores conocidos."
        print("-> CASO 1 SUPERADO: El algoritmo es matemáticamente sólido.")
        
    except AssertionError as e:
        print(f"-> FALLO EN AUDITORÍA CASO 1: {e}")
    except Exception as e:
        print(f"-> ERROR CRÍTICO CASO 1: {e}")

    # CASO 2: Matriz Bioquímica de 50x50. Prueba de rendimiento
    # Generamos 50 eigenvalores ficticios (del 50 al 1)
    eigen_conocidos_caso2 = list(range(50, 0, -1))
    
    print("\n[Caso 2] Matriz de Estrés 50x50")
    A_np_2 = generar_matriz_con_eigenvalores(eigen_conocidos_caso2)
    A_matrix_2 = Matrix(A_np_2.tolist())
    
    try:
        # Probamos su rendimiento
        eigen_calculados_2 = eg.eigen_vals(A_matrix_2, max_iter=2000)
        print("-> CASO 2 SUPERADO: El algoritmo logró procesar la matriz de 50x50.")
    except Exception as e:
        # Capturamos si falla por iteraciones
        print(f"-> ERROR CRÍTICO CASO 2 (Prueba de Estrés fallida): {e}")

if __name__ == "__main__":
    # Fijamos semilla para que el test sea determinista
    np.random.seed(42)
    test_eigenvalues_auditoria()