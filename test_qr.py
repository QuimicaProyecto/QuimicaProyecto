import numpy as np
# TODO: Importar el algoritmo QR custom

def generar_matrices_prueba():
    # 1. Cuadrada estándar
    A_cuadrada = np.random.rand(5, 5)
    
    # 2. Rectangular
    A_rect = np.random.rand(6, 4)
    
    # 3. Columnas casi linealmente dependientes
    # Aquí Gram-Schmidt modificado debe brillar frente al clásico
    A_mal_cond = np.random.rand(5, 5)
    A_mal_cond[:, 1] = A_mal_cond[:, 0] + 1e-8 * np.random.rand(5)
    
    # 4. Rango deficiente
    A_ceros = np.random.rand(5, 5)
    A_ceros[:, 2] = 0.0
    
    return {
        "Cuadrada": A_cuadrada, 
        "Rectangular": A_rect, 
        "Mal Condicionada": A_mal_cond, 
        "Columna Cero": A_ceros
    }

def evaluar_algoritmo_qr(A, nombre):
    print(f"\n--- Evaluando caso: {nombre} ---")
    
    # 1. Ejecutar QR NumPy
    Q_np, R_np = np.linalg.qr(A)
    
     #2. Ejecutar algoritmo custom
    """ try:
        Q_custom, R_custom = qr.algoritmo_qr(A)
    except Exception as e:
        print(f"El algoritmo falló en este caso. Error: {e}")
        return """
    
    # Simulación temporal para que el script corra
    Q_custom, R_custom = Q_np, R_np 

    # TEST 1: Reconstrucción e Ignorar Signos
    # NOTE: NumPy y el código custom pueden arrojar signos diferentes pero ambos ser válidos.
    reconstruccion = np.allclose(Q_custom @ R_custom, A, atol=1e-8)
    print(f"Reconstrucción (Q @ R ≈ A): {'ÉXITO' if reconstruccion else 'FALLO'}")
    
    # TEST 2: Identidad y Ortogonalidad
    I = np.eye(Q_custom.shape[1])
    ortogonalidad = np.allclose(Q_custom.T @ Q_custom, I, atol=1e-8)
    print(f"Ortogonalidad (Q.T @ Q ≈ I): {'ÉXITO' if ortogonalidad else 'FALLO'}")
    
    # TEST 3: Nivel de error (Benchmark clásico vs modificado)
    error_ortogonalidad = np.linalg.norm(Q_custom.T @ Q_custom - I)
    print(f"Error de Ortogonalidad absoluto: {error_ortogonalidad:.2e}")

# Ejecutar la batería de pruebas
matrices = generar_matrices_prueba()
for nombre, matriz in matrices.items():
    evaluar_algoritmo_qr(matriz, nombre)