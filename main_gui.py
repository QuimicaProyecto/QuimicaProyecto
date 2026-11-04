import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import string
import Data_loader as dl
import Preprocessing as pp
import Visualization as vis
import Preprocess_gui as pgui

matriz_global = None
datos_crudos_np = None

def procesar_archivo(ruta_archivo):
    global matriz_global, datos_crudos_np
    try:
        matriz_global, _ = dl.Data_Loader(ruta_archivo)
        datos_crudos_np = matriz_global.data
        
        lbl_estado.config(text=f"Dataset Activo: {matriz_global.rows} espectros | {matriz_global.cols} longitudes", foreground="green")
        
        actualizar_tabla(datos_crudos_np)
        
        btn_preprocesar.state(['!disabled'])
        
    except Exception as e:
        messagebox.showerror("Error de carga", f"No se pudo leer el archivo:\n{e}")

# --- Funciones Auxiliares para el estilo "Excel" ---
def obtener_letra_columna(indice):
    """Convierte un índice numérico (0, 1, 2...) en letras (A, B, C... Z, AA, AB...)"""
    resultado = ""
    while indice >= 0:
        resultado = string.ascii_uppercase[indice % 26] + resultado
        indice = indice // 26 - 1
    return resultado

# --- Funciones de Eventos ---
def cargar_via_boton():
    ruta = filedialog.askopenfilename(title="Cargar Dataset Espectroscópico", filetypes=[("Archivos Excel", "*.xlsx *.xls")])
    if ruta:
        procesar_archivo(ruta)

def cargar_via_arrastre(event):
    ruta = event.data.strip('{}')
    procesar_archivo(ruta)

def abrir_ventana_preprocesamiento():
    if datos_crudos_np is None: 
        return
    pgui.PreprocessingWindow(ventana, datos_crudos_np)

def actualizar_tabla(datos):
    for item in tabla.get_children():
        tabla.delete(item)
        
    max_filas = min(15, len(datos))
    max_cols = min(10, len(datos[0]))
    
    # 1. Configurar los nombres de las columnas (Letras A, B, C...)
    nombres_columnas = [obtener_letra_columna(i) for i in range(max_cols)]
    tabla['columns'] = nombres_columnas
    
    # 2. Configurar la cabecera del índice (columna 0)
    tabla.heading("#0", text="") # Se deja vacía como en Excel
    tabla.column("#0", width=40, anchor="center") # Hacemos la columna del número más delgada
    
    # 3. Configurar todas las columnas para que tengan la misma longitud horizontal
    ancho_uniforme = 80 
    for letra in nombres_columnas:
        tabla.heading(letra, text=letra)
        tabla.column(letra, width=ancho_uniforme, anchor="center")
        
    # 4. Insertar los datos (Usando el número de fila como índice y más decimales)
    for i in range(max_filas):
        # f"{val:.6f}" aumenta la precisión a 6 decimales
        fila_formateada = [f"{val:.6f}" for val in datos[i, :max_cols]]
        # El texto principal ahora es str(i + 1) para simular las filas de Excel
        tabla.insert("", "end", text=str(i + 1), values=fila_formateada)

# --- Funciones de Análisis (Workflow de Preprocesamiento) ---
def abrir_ventana_preprocesamiento():
    if datos_crudos_np is None: 
        return
    pgui.PreprocessingWindow(ventana, datos_crudos_np)

# --- ARQUITECTURA VISUAL MODERNIZADA ---
ventana = TkinterDnD.Tk()
ventana.title("Programa de soluciones Quimiométricas")
ventana.geometry("1050x650") # Ancho x Alto

estilo = ttk.Style()
if "clam" in estilo.theme_names(): estilo.theme_use("clam")

main_frame = ttk.Frame(ventana, padding="15")
main_frame.pack(fill=tk.BOTH, expand=True)

# ZONA SUPERIOR: Carga de archivos
frame_carga = ttk.LabelFrame(main_frame, text=" 1. Importación de Datos ", padding="15")
frame_carga.pack(fill=tk.X, pady=(0, 15))

lbl_instruccion = ttk.Label(frame_carga, text="Arrastra y suelta tu archivo Excel (.xlsx) aquí, o haz clic en el botón.", foreground="gray")
lbl_instruccion.pack(pady=(0, 10))

btn_cargar = ttk.Button(frame_carga, text="Explorar Archivos...", command=cargar_via_boton)
btn_cargar.pack()

frame_carga.drop_target_register(DND_FILES)
frame_carga.dnd_bind('<<Drop>>', cargar_via_arrastre)

lbl_estado = ttk.Label(frame_carga, text="Dataset Activo: Ninguno", foreground="red", font=("", 10, "bold"))
lbl_estado.pack(pady=(10, 0))

# ZONA CENTRAL: Vista Previa
frame_matriz = ttk.LabelFrame(main_frame, text=" 2. Vista Previa de la Matriz (Muestra) ", padding="10")
frame_matriz.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

tabla = ttk.Treeview(frame_matriz, height=10)
tabla.pack(fill=tk.BOTH, expand=True)

# ZONA INFERIOR: Panel de Procesamiento (Workflow)
frame_analisis = ttk.LabelFrame(main_frame, text=" 3. Preprocesamiento Espectroscópico ", padding="15")
frame_analisis.pack(fill=tk.X)

btn_preprocesar = ttk.Button(frame_analisis, text="Abrir Módulo de Preprocesamiento", command=abrir_ventana_preprocesamiento, state='disabled')
btn_preprocesar.pack(pady=10)


ventana.mainloop()