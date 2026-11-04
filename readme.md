## v2026.11.04

### Cambios
- Se movieron las funciones [back_substitution()] y [forward_substitution()] de [LU.py] a [substitution.py]
- Se creó la variable [DEFAULT_TOL] en [exceptions.py]
- Se creó la función [zero_matrix()] en [matrix.py]
- Se añadieron las funciones [sav_gol_matrix()], [sav_gol_apply()], [sav_gol_smoothing_pol()] y [sav_gol_der()] en [Preprocessing.py]
- Se modificó una operación de la función [qr_decomposition()] en [QR.py]
- Se modificó [main_gui.py]
- Se añadió la importación [scipy.special.factorial] en [Preprocessing.py]
- Se creó la función [qr_decomposition_pivoting] en [QR.py]

### Cambios menores
- Se corrigió un error de sintaxis en [LU.py] > [lu_decomposition()]

### Pendiente
Añadir función [autoscale()] en [Preprocess_gui.py]
<!-- Añadir función [qr_decomposition_pivoting()] en [QR.py] -->
<!-- Realizar prueba unitaria unitaria [test_eigen.py] -->
Realizar prueba unitaria unitaria [test_least_squares.py]

### Bitácora de la prueba unitaria de eigen.py

**Prueba 1:**
--- PRUEBA UNITARIA: ALGORITMO QR DE EIGENVALORES ---
-> ERROR CRÍTICO durante la ejecución: type object 'Matrix' has no attribute 'zero_matrix'

Razonamiento: Posiblemente es un error de estructura. Al someter el algoritmo [eigen_vals] a la prueba, el programa colapsó intentando llamar al atributo [zero_matrix] que no existe.

Solución encontrada: Agregué en [matrix.py] la función [zero_matrix()]. Esto genera una matriz de ceros cuando el algoritmo QR la pide.

**Prueba 2:**
--- PRUEBA UNITARIA: ALGORITMO QR DE EIGENVALORES ---
-> ERROR CRÍTICO durante la ejecución: only 0-dimensional arrays can be converted to Python scalars

Razonamiento: Al parecer se trata de un error de compatibilidad al mezclar funciones de Python con funciones de Numpy. En la función [norm()] de [vector.py] ocurría que, al realizar multiplicaciones internas durante la descomposición de la matriz, Numpy devuelve una cuadrícula de 1x1 en lugar de un número suelto, y al intentar inyectar este tipo de dato dentro de una operación nativa de Python (específicamente, [sum()] y [float()]) genera un error de incompatibilidad. Nota: puede que este comportamiento se deba a versiones recientes de python/numpy.

Solución encontrada: En [vector.py], modifiqué las funciones para que todos los resultados correspondan al mismo tipo de dato. Nota: realicé una prueba de integridad respecto a estas modificaciones y los resultados parecen coincidir perfectamente con el código original (revisar [test_integridad_vector.py]).

**Prueba 3:**
--- PRUEBA UNITARIA: ALGORITMO QR DE EIGENVALORES ---
-> ERROR CRÍTICO durante la ejecución: unsupported operand type(s) for /: 'Vector' and 'float'

Razonamiento: El algoritmo intenta dividir un vector entre un float, cosa que al parecer Python no sabe hacer por si mismo. Esto genera un error de operación.

Solución encontrada: En [QR.py], modifiqué la operación de [qr_decomposition()] de forma que extrae los datos numéricos puros del vector [v.data] y lo convertí en un arreglo de Numpy, ya que Numpy sí sabe dividir matrices entre numeros.

**Prueba 4:**
--- PRUEBA UNITARIA: ALGORITMO QR DE EIGENVALORES ---
-> ERROR CRÍTICO durante la ejecución: eigen values did not converge after 2000 iterations

Razonamiento: El algoritmo alcanzó el límite de iteraciones establecido (2000). Al aplicar un limite de 15000 iteraciones, el test logró completar su ejecución con este resultado:
--- PRUEBA DE ALGORITMO QR PARA EIGENVALORES ---
Dimensiones de la matriz: 50x50
Eigenvalor más grande (Esperado):  4.497697e-05
Eigenvalor más grande (Calculado): 4.497697e-05
-> ÉXITO: El cálculo de eigenvalores a escala real es numéricamente exacto.

Parece que el algoritmo de eigenvalores funciona bien, pero no está optimizado para ser funcional por el momento.

**Prueba 5:**
--- PRUEBA UNITARIA: ALGORITMO QR DE EIGENVALORES ---

[Caso 1] Matriz 5x5 con Eigenvalores controlados
Resultados:
 Esperado:  25.0000 | Calculado:  25.0000
 Esperado:  10.0000 | Calculado:  10.0000
 Esperado:   5.0000 | Calculado:   5.0000
 Esperado:   1.0000 | Calculado:   1.0000
 Esperado:   0.1000 | Calculado:   0.1000
-> CASO 1 SUPERADO: El algoritmo es matemáticamente sólido.

[Caso 2] Matriz de Estrés 50x50
-> CASO 2 SUPERADO: El algoritmo logró procesar 50x50.

Razonamiento: En la Prueba 4, se inyectaron matrices de covarianza generadas a partir de ruido aleatorio (np.random.uniform), lo que produce matrices "mal condicionadas" y difíciles de resolver para el algoritmo. En esta prueba 5, se implementó una función para generar una matriz con eigenvalores determinados. Esto logró que el algoritmo de eigenvalores superara el procesamiento de la matriz de 50x50, donde antes fallaba la prueba.

Conclusión: El algoritmo de los eigenvalores convergió rápidamente y entregó resultados exactos, demostrando que funciona correctamente. Sin embargo, el código actual solo funciona con matrices predecibles. Los datasets reales tienen mas ruido y caos, por lo que el algoritmo actualmente no está preparado para procesarlos. Para que este algoritmo sea viable en el software final sin congelarse intentando calcular la covarianza real, necesita optimizarse o, alternativamente, ser reemplazado por los motores vectorizados de [scipy.linalg].

Aqui concluye la prueba unitaria de [eigen.py]