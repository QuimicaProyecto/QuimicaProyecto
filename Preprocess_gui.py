import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# Para incrustar Matplotlib en Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Importar tu módulo de preprocesamiento ya corregido
import Preprocessing as pp

class PreprocessingWindow:
    def __init__(self, parent, datos_crudos):
        # Configuración de la ventana (Actúa como "hija" de main_gui)
        self.window = tk.Toplevel(parent)
        self.window.title("Módulo de Preprocesamiento")
        self.window.geometry("1100x700")
        
        self.datos_crudos = datos_crudos
        
        # Variables de estado (El Pipeline)
        # Aquí puedes añadir "Autoscale" cuando programes la función en Preprocessing.py
        self.metodos_disponibles = [
            "Mean Centering", 
            "Standard",
            "Min Max Scaler",
            "Savitzky-Golay (M=7, N=3)" # Parámetros predefinidos por ahora
        ]
        self.pipeline_seleccionado = []
        
        self._construir_interfaz()
        self._inicializar_grafica()

    def _construir_interfaz(self):
        frame_top = ttk.Frame(self.window, padding="10")
        frame_top.pack(fill=tk.X)
        
        # Panel Izquierdo: Métodos Disponibles
        frame_izq = ttk.LabelFrame(frame_top, text="Métodos Disponibles")
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.listbox_disponibles = tk.Listbox(frame_izq, height=8, selectmode=tk.SINGLE)
        self.listbox_disponibles.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        for m in self.metodos_disponibles:
            self.listbox_disponibles.insert(tk.END, m)
            
        # Botones Centrales (Add / Remove)
        frame_centro = ttk.Frame(frame_top)
        frame_centro.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(frame_centro, text="Añadir ->", command=self.agregar_metodo).pack(pady=5)
        ttk.Button(frame_centro, text="<- Quitar", command=self.quitar_metodo).pack(pady=5)
        
        # Panel Derecho: Pipeline (Métodos Seleccionados / Apilados)
        frame_der = ttk.LabelFrame(frame_top, text="Métodos Seleccionados (Pipeline)")
        frame_der.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.listbox_seleccionados = tk.Listbox(frame_der, height=8, selectmode=tk.SINGLE)
        self.listbox_seleccionados.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel Inferior: Gráficas Comparativas
        self.frame_grafica = ttk.Frame(self.window)
        self.frame_grafica.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _inicializar_grafica(self):
        # Figura de matplotlib con dos paneles (Antes y Después)
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.fig.tight_layout(pad=3.0)
        
        # Conectar matplotlib a Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafica)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.actualizar_visualizacion()

    # --- LÓGICA DE EVENTOS INTERFAZ ---
    def agregar_metodo(self):
        seleccion = self.listbox_disponibles.curselection()
        if seleccion:
            metodo = self.listbox_disponibles.get(seleccion[0])
            self.pipeline_seleccionado.append(metodo)
            self.listbox_seleccionados.insert(tk.END, metodo)
            self.procesar_pipeline() # Ejecuta el cálculo al hacer clic

    def quitar_metodo(self):
        seleccion = self.listbox_seleccionados.curselection()
        if seleccion:
            idx = seleccion[0]
            self.listbox_seleccionados.delete(idx)
            self.pipeline_seleccionado.pop(idx)
            self.procesar_pipeline()

    # --- MOTOR MATEMÁTICO: EL PIPELINE APILADO ---
    def procesar_pipeline(self):
        datos_actuales = np.copy(self.datos_crudos)
        historial_pasos = [] # Guardaremos el arreglo tras CADA filtro

        try:
            for metodo in self.pipeline_seleccionado:
                if metodo == "Mean Centering":
                    datos_actuales = pp.mean_centering(datos_actuales)
                elif metodo == "Standard":
                    datos_actuales = pp.standard(datos_actuales)
                elif metodo == "Min Max Scaler":
                    datos_actuales = pp.Min_Max_scaler(datos_actuales)
                elif metodo == "Savitzky-Golay (M=7, N=3)":
                    datos_actuales = pp.sav_gol_apply(datos_actuales, M=7, N=3)

                # Guardamos una foto del espectro tras aplicar este filtro
                historial_pasos.append(np.copy(datos_actuales))

            self.actualizar_visualizacion(historial_pasos)

        except Exception as e:
            messagebox.showerror("Error Matemático", f"El procesamiento falló:\n{e}")

    # --- DIBUJADO DE GRÁFICA ---
    def actualizar_visualizacion(self, historial_pasos=None):
        self.ax1.clear()
        self.ax2.clear()
        
        espectro_original = self.datos_crudos[0, :]
        self.ax1.plot(espectro_original, color='blue', alpha=0.6)
        self.ax1.set_title("Datos Originales")
        
        if historial_pasos and len(self.pipeline_seleccionado) > 0:
            # 1. Dibujar los pasos intermedios (semitransparentes)
            for i, datos_paso in enumerate(historial_pasos[:-1]):
                self.ax2.plot(datos_paso[0, :], alpha=0.3, label=f"Paso {i+1}: {self.pipeline_seleccionado[i]}")

            # 2. Dibujar el resultado final (línea gruesa)
            espectro_final = historial_pasos[-1][0, :]
            self.ax2.plot(espectro_final, color='orange', alpha=0.9, linewidth=2, label="Resultado Final")

            self.ax2.set_title(" + ".join(self.pipeline_seleccionado))
            self.ax2.legend(fontsize='x-small')
        else:
            self.ax2.set_title("Datos Procesados (Vacío)")
            
        self.canvas.draw()