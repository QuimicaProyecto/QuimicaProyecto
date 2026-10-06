import tkinter as tk
from tkinter import filedialog, messagebox
import Data_loader as dl
import Preprocessing as pp
import Visualization as vis

# Variable global para almacenar los datos temporalmente en la memoria
matriz_global = None

def cargar_archivo():
    global matriz_global
    # Abre la ventana típica de Windows para buscar archivos
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de datos",
        filetypes=[("Archivos Excel", "*.xlsx *.xls")]
    )
    
    if ruta_archivo:
        try:
            matriz_global, _ = dl.Data_Loader(ruta_archivo)
            etiqueta_estado.config(text=f"¡Datos listos! ({matriz_global.rows} espectros)", fg="green")
        except Exception as e:
            messagebox.showerror("Error de lectura", f"No se pudo cargar el archivo:\n{e}")

def procesar_y_graficar():
    if matriz_global is None:
        messagebox.showwarning("Advertencia", "Por favor, carga un archivo Excel primero.")
        return
    
    try:
        # Extraer los datos crudos completos
        raw_data = matriz_global.data
        
        # Calcular los tres preprocesamientos de golpe (NumPy lo hace en milisegundos)
        mc_data = pp.mean_centering(raw_data)
        std_data = pp.standard(raw_data)
        mm_data = pp.Min_Max_scaler(raw_data)
        
        # Tomar solo el primer espectro (fila 0) para la demostración visual
        espectro_crudo = raw_data[0, :]
        
        # Empaquetar los espectros procesados en un diccionario
        dict_procesados = {
            "Mean Centering": mc_data[0, :],
            "Standard": std_data[0, :],
            "Min Max Scaler": mm_data[0, :]
        }
        
        # Llamar a la nueva gráfica interactiva
        vis.interactive_spectrums(espectro_crudo, dict_procesados)
        
    except Exception as e:
        messagebox.showerror("Error de proceso", f"Ocurrió un problema matemático:\n{e}")


# --- CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
ventana = tk.Tk()
ventana.title("Proyecto")
ventana.geometry("400x250") # Ancho x Alto

# Título de la aplicación
tk.Label(ventana, text="Análisis Espectroscópico", font=("Arial", 14, "bold")).pack(pady=15)

# Etiqueta de estado
etiqueta_estado = tk.Label(ventana, text="Ningún archivo cargado", fg="red", font=("Arial", 10))
etiqueta_estado.pack(pady=5)

# Botones interactivos
tk.Button(ventana, text="1. Buscar y Cargar Excel", command=cargar_archivo, width=25, height=2).pack(pady=5)
tk.Button(ventana, text="2. Procesar y Ver Gráficas", command=procesar_y_graficar, width=25, height=2).pack(pady=5)

# Iniciar la interfaz
ventana.mainloop()
