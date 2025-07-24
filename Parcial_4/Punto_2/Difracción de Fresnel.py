from unittest import case
import numpy as np                  # Para operaciones numéricas
import matplotlib.pyplot as plt     # Para visualización
from scipy.special import fresnel   # Para las integrales de Fresnel            
import pint                         # Para manejar unidades físicas 
from matplotlib.animation import FuncAnimation

u = pint.UnitRegistry()

'''
Este código calcula la intensidad de la difracción de Fresnel para diferentes aperturas.
'''

# Parametros de simulación
λ = 632.8e-9 * u.meter        # Longitud de onda 
D_prima = 0.1 * u.meter       # Distancia al plano de observación
Nx_values = [20, 15, 10, 5, 1]  # Barrido parametrico de Nx

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
X_prima = np.linspace(-3e-3, 3e-3, 2000) * u.meter  # Rango de X' en metros
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



Comparar_Nx_animado()