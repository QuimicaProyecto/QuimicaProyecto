import Data_loader as dl
import Preprocessing as pp
import Visualization as vis

def main():
    print("--- Sistema de Análisis Espectroscópico ---")
    archivo = "Datos espectroscópicos SORS Tequila/MatrDat_TB-TBM-SORS_v0.2.xlsx"
    print(f"Cargando {archivo}, por favor espera...")
    
    try:
        # Cargar datos
        matriz_datos, metadatos = dl.Data_Loader(archivo)
        print(f"¡Datos cargados! {matriz_datos.rows} filas y {matriz_datos.cols} columnas.")
        
        # Preprocesamiento
        print("Aplicando centrado de media...")
        datos_procesados = pp.mean_centering(matriz_datos.data)
        
        # Extraer el primer espectro para comparar
        espectro_crudo = matriz_datos.data[0, :]
        espectro_limpio = datos_procesados[0, :]
        
        # Visualización
        print("Generando visualización (cierra la ventana de la gráfica para continuar)...")
        vis.comparing_spectrums(
            espectro_crudo, 
            espectro_limpio, 
            title_a="Espectro Crudo (Original)", 
            title_b="Procesado (Centrado de Media)"
        )
        print("Proceso finalizado con éxito.")
        
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un problema: {e}")

    # Esta línea evita que la consola se cierre inmediatamente
    input("\nPresiona Enter para cerrar el programa...")

if __name__ == "__main__":
    main()