from unittest import case
import numpy as np                  # Para operaciones numéricas
import matplotlib.pyplot as plt     # Para visualización
from scipy.special import fresnel   # Para las integrales de Fresnel            
import pint                         # Para manejar unidades físicas 
from matplotlib.animation import FuncAnimation
from Fraunhofer_graph import *


u = pint.UnitRegistry()

'''
Este código calcula la intensidad de la difracción de Fresnel para diferentes aperturas.
'''

# Parametros de simulación
λ = 632.8e-9 * u.meter        # Longitud de onda 
D_prima = 10000 * u.meter       # Distancia al plano de observación
Nx_values = [5, 1]  # Barrido parametrico de Nx

# Parametros fisicos de las aperturas
# Edge


# Slit
width = 0.5e-6 * u.meter    # 50 micras


# Inicialización de variables para los límites de integración
# Estos valores dependen del tipo de apertura y se ajustarán según la apertura seleccionada
x_1 = -0.5e-3 * u.meter
x_2 = 0 * u.meter
y_1 = 0 * u.meter
y_2 = 0 * u.meter

# Inicialización de variables para los parámetros de la apertura
Nx = 1  # Nx ira variando.
Ny = 1  # Fijamos Ny a 1. 

# Se definen los rangos de integración para X' y Y'
X_prima = np.linspace(-6e-3, 6e-3, 2000) * u.meter  # Rango de X' en metros
Y_Prima = 0 * u.meter                               # Eje Y'

Apertura = 'Slit'  # Apertura por defecto, se cambiará según la entrada del usuario

def Intensity_Function(Nx, X_prima):
    match Apertura:
        case 'Edge':
            x_1 = -0.5e-3 * u.meter
            x_2 = np.inf * u.meter
            y_1 = -np.inf * u.meter
            y_2 = np.inf * u.meter
        case 'Slit':
            y_1 = -np.inf * u.meter
            y_2 = np.inf * u.meter
            x_1 = (-np.sqrt(Nx * λ * D_prima)).to(u.meter)
            x_2 = (np.sqrt(Nx * λ * D_prima)).to(u.meter)
        case 'Square':
            Ny = Nx  # Igualamos Nx y Ny
            y_1 = (-np.sqrt(Ny * λ * D_prima)).to(u.meter)
            y_2 = (np.sqrt(Ny * λ * D_prima)).to(u.meter)
            x_1 = (-np.sqrt(Nx * λ * D_prima)).to(u.meter)
            x_2 = (np.sqrt(Nx * λ * D_prima)).to(u.meter)        
        case _:
            raise ValueError("Apertura no válida. Elija entre 'Edge', 'Slit' o 'Square'.")

    # Se calculan las posiciones normalizadas para X' y Y'
    η_factor = (np.sqrt((2 / (λ * D_prima)).to('1/meter**2'))).magnitude
    η_x1 = η_factor * (X_prima - x_1).to(u.meter).magnitude
    η_x2 = η_factor * (X_prima - x_2).to(u.meter).magnitude
    η_y1 = η_factor * (Y_Prima - y_1).to(u.meter).magnitude
    η_y2 = η_factor * (Y_Prima - y_2).to(u.meter).magnitude

    # Integrales de Fresnel
    S_x1, C_x1 = fresnel(η_x1)
    S_y1, C_y1 = fresnel(η_y1)
    S_x2, C_x2 = fresnel(η_x2)
    S_y2, C_y2 = fresnel(η_y2)

    # Intensidad normalizada
    Intensity_Function = ((C_x2 - C_x1) ** 2 + (S_x2 - S_x1) ** 2) * \
        ((C_y2 - C_y1) ** 2 + (S_y2 - S_y1) ** 2)
        
    Intensity_Function /= np.max(Intensity_Function)  # Normalización

    return Intensity_Function

def Grafica_Intensidad():

    for Nx in Nx_values:
        
        # Calcular la intensidad para el valor actual de Nx
        Intensity = Intensity_Function(Nx, X_prima)
        
        #Intensity = Double_Slit_IntensityFunction(Nx, X_prima)
        
        # Convertir a unidades de intensidad para graficar
        X_prima_mm = X_prima.to(u.mm).magnitude  # Convertir a mm

        # Graficar intensidad
        plt.figure(figsize=(8, 5))
        plt.plot(X_prima_mm, Intensity, label=f'Nx = {Nx}')
        plt.title(f'Intensidad en función de X\' - Apertura: {Apertura}, Nx = {Nx}')
        plt.xlabel('Posición X\' (mm)')
        plt.ylabel('Intensidad Normalizada')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


def Double_Slit_IntensityFunction(Nx, X_prima):
    
    Apertura = 'Slit'  # Apertura de rendija sencilla
    
    ancho = 2 * np.sqrt(Nx * λ * D_prima)
    d = 4 * np.sqrt(Nx * λ * D_prima)  # separación entre centros de rendijas
    
    X1_prima = X_prima - d / 2  # Primer desplazamiento
    X2_prima = X_prima + d / 2  # Segundo desplazamiento

    # Usar los desplazamientos en las llamadas
    I1 = Intensity_Function(Nx, X1_prima)
    I2 = Intensity_Function(Nx, X2_prima)

    campo = np.sqrt(I1) + np.sqrt(I2)
    
    I = campo ** 2
    
    I = I / np.max(I)  # Normalización
    
    return I
    
def Comparar_Nx():
    plt.figure(figsize=(8, 5))
    X_prima_mm = X_prima.to(u.mm).magnitude  # Eje X en mm

    for Nx in Nx_values:
        I = Intensity_Function(Nx, X_prima)
        plt.plot(X_prima_mm, I, label=f'Nx = {Nx}')

    plt.title(f'Comparación de Difracción de Fresnel para distintos Nx\nApertura: {Apertura}')
    plt.xlabel("X' (mm)")
    plt.ylabel("Intensidad Normalizada")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def Comparar_Nx_animado():
    fig, ax = plt.subplots(figsize=(8, 5))
    X_prima_mm = X_prima.to(u.mm).magnitude
    lines = []
    Nx_labels = []

    # Precalcula todas las intensidades
    intensidades = [Intensity_Function(Nx, X_prima) for Nx in Nx_values]

    def init():
        ax.clear()
        ax.set_title(f'Comparación de Difracción de Fresnel para distintos Nx\nApertura: {Apertura}')
        ax.set_xlabel("X' (mm)")
        ax.set_ylabel("Intensidad Normalizada")
        ax.grid(True)
        ax.legend()
        return []

    def update(frame):
        ax.clear()
        ax.set_title(f'Comparación de Difracción de Fresnel para distintos Nx\nApertura: {Apertura}')
        ax.set_xlabel("X' (mm)")
        ax.set_ylabel("Intensidad Normalizada")
        ax.grid(True)
        for i in range(frame + 1):
            ax.plot(X_prima_mm, intensidades[i], label=f'Nx = {Nx_values[i]}')
        ax.legend()
        plt.tight_layout()
        return []

    ani = FuncAnimation(fig, update, frames=len(Nx_values), init_func=init, interval=1000, blit=False)
    plt.show()

def Fresnel_evolucion_subplot(Nx_list, X_prima, Apertura='Slit'):
    """
    Grafica la evolución del patrón de Fresnel para 4 valores de Nx en subplots.
    Nx_list: lista de 4 valores de Nx a mostrar.
    X_prima: eje espacial (con unidades).
    Apertura: tipo de apertura ('Edge', 'Slit', 'Square').
    """
    fig, axs = plt.subplots(1, 4, figsize=(18, 4), sharey=True)
    X_prima_mm = X_prima.to(u.mm).magnitude

    for i, Nx in enumerate(Nx_list):
        global mask  # Si usas una variable global para el tipo de apertura
        mask = mask
        I = Intensity_Function(Nx, X_prima)
        axs[i].plot(X_prima_mm, I, color='k')
        axs[i].set_title(f'N$_x$ = {Nx}')
        axs[i].set_xlabel("X' (mm)")
        axs[i].grid(True)
        if i == 0:
            axs[i].set_ylabel("Intensidad Normalizada")
    plt.suptitle(f'Evolución del patrón de Fresnel - Apertura: {Apertura}')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def animacion_fresnel_a_fraunhofer_D(X_prima, D_min, D_max, pasos, Apertura='Slit'):
    """
    Anima la evolución del patrón de Fresnel al variar D' desde D_min hasta D_max,
    mostrando siempre el patrón de Fraunhofer (D_max) como referencia.
    Además, muestra el Nx efectivo en cada frame.
    El rango de X' es fijo y debe ser elegido por el usuario.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    X_prima_mm = X_prima.to(u.mm).magnitude

    # Parámetros físicos de la rendija (ajusta según tu simulación)
    width_um = 50  # ancho físico de la rendija en micras (valor indicativo)
    width = width_um * 1e-6 * u.meter

    # Calcula el patrón de Fraunhofer (D_max)
    global D_prima
    D_prima = D_max
    I_fraunhofer = Intensity_Function(Nx=1, X_prima=X_prima)  # Nx no importa, D_prima es lo relevante

    # Precalcula intensidades y Nx efectivos para cada D'
    D_values = np.linspace(D_min, D_max, pasos)
    intensidades = []
    Nx_efectivos = []
    for D in D_values:
        D_prima = D
        Nx_eff = (width**2 / (λ * D_prima)).to_base_units().magnitude
        Nx_efectivos.append(Nx_eff)
        intensidades.append(Intensity_Function(Nx=1, X_prima=X_prima))

    # Normalización global
    max_global = max(np.max(I_fraunhofer), *(np.max(I) for I in intensidades))
    I_fraunhofer = I_fraunhofer / max_global
    intensidades = [I / max_global for I in intensidades]

    line_fresnel, = ax.plot([], [], color='k', label="Fresnel (D')")
    line_fraunhofer, = ax.plot(X_prima_mm, I_fraunhofer, color='r', linestyle='--', label=f'Fraunhofer (D = {D_max.to(u.meter):.1E})')
    ax.set_xlabel("X' (mm)")
    ax.set_ylabel("Intensidad Normalizada")
    ax.set_title(f'Evolución Fresnel → Fraunhofer ({Apertura})')
    ax.grid(True)
    ax.legend()
    # Texto para mostrar Nx efectivo
    text_nx = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    def init():
        line_fresnel.set_data([], [])
        text_nx.set_text('')
        return line_fresnel, line_fraunhofer, text_nx

    def update(frame):
        I = intensidades[frame]
        Nx_eff = Nx_efectivos[frame]
        line_fresnel.set_data(X_prima_mm, I)
        ax.set_title(f'Evolución Fresnel → Fraunhofer\nD\' = {D_values[frame].to(u.meter):.2E}')
        text_nx.set_text(f"N$_x$ efectivo = {Nx_eff:.2f}")
        return line_fresnel, line_fraunhofer, text_nx

    ani = FuncAnimation(fig, update, frames=pasos, init_func=init, blit=True, interval=100)
    plt.show()
    # Para guardar como GIF:
    # ani.save('fresnel_fraunhofer_D.gif', writer='pillow')

# Ejemplo de uso:
D_min = 0.00001 * u.meter
D_max = 1 * u.meter
animacion_fresnel_a_fraunhofer_D(X_prima, D_min, D_max, pasos=200, Apertura='Slit')



# mask = vertical_slit(200)

# # Ejemplo de uso:
# Nx_list = [1, 3, 6, 12]  # O los valores que prefieras
# Fresnel_evolucion_subplot(Nx_list, X_prima, Apertura='Slit')



# simulate_and_graph(shape='rectangle', width_um = 200, height_um = 200)  # Ejemplo de uso con rectángulo

# mask = rectangle(200, 200)
# Intensity = Fraunhofer_Diffraction(mask)
# graph_1D_fraunhofer(mask, Intensity)

# Grafica_Intensidad()