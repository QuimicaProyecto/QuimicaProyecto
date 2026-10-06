import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import numpy as np


def plot_spectrum(matrix, title="Spectrum",xlabel="Frequencies (index)",ylabel="Intensity",ax=None,alpha=0.6):
    data= matrix.data if hasattr(matrix,"rows") else matrix

    if ax is None:
        fig,ax=plt.subplots(figsize=(8,5))

    ax.plot(data, alpha=alpha)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle= '--',alpha=0.5)

    return ax

def comparing_spectrums(matrix_a,matrix_b, title_a="Raw_Data", title_b="Processed data"):
    fig, (ax1,ax2)=plt.subplots(1,2,figsize=(14,5))

    plot_spectrum(matrix_a,title=title_a, ax=ax1)
    plot_spectrum(matrix_b,title=title_b, ylabel="" ,ax=ax2)

    plt.tight_layout( )
    plt.show()

def interactive_spectrums(raw_spectrum, dict_processed):
    # Crear figura con espacio extra en la parte inferior para el menú
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.subplots_adjust(bottom=0.25)

    # Eje 1: Datos crudos (Estático)
    ax1.plot(raw_spectrum, alpha=0.6, color='blue')
    ax1.set_title("Espectro Crudo (Original)")
    ax1.set_xlabel("Frecuencias (index)")
    ax1.set_ylabel("Intensidad")
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Eje 2: Datos procesados (Dinámico)
    nombres_metodos = list(dict_processed.keys())
    metodo_actual = nombres_metodos[0]

    # Guardamos la línea graficada en la variable "linea_procesada" para modificarla después
    linea_procesada, = ax2.plot(dict_processed[metodo_actual], alpha=0.6, color='orange')
    ax2.set_title(f"Procesado: {metodo_actual}")
    ax2.set_xlabel("Frecuencias (index)")
    ax2.grid(True, linestyle='--', alpha=0.5)

    # Crear el panel de botones de radio [posición_x, posición_y, ancho, alto]
    ax_radio = plt.axes([0.4, 0.05, 0.2, 0.12]) 
    radio = RadioButtons(ax_radio, nombres_metodos)
    
    # Esta variable ancla los botones a la figura para que no desaparezcan de la memoria
    fig.radio = radio

# Función interna que redibuja la gráfica al hacer clic
    def actualizar_grafica(label):
        nuevos_datos = dict_processed[label]
        linea_procesada.set_ydata(nuevos_datos) 
        
        # Ajustar dinámicamente los límites del eje Y según el nuevo cálculo
        ax2.set_ylim(nuevos_datos.min() - (abs(nuevos_datos.min()) * 0.1), 
                     nuevos_datos.max() + (abs(nuevos_datos.max()) * 0.1))
        
        ax2.set_title(f"Procesado: {label}")
        fig.canvas.draw_idle() 

    # Conectar el evento de clic con nuestra función
    radio.on_clicked(actualizar_grafica)

    plt.show()