import numpy as np
import matplotlib.pyplot as plt
from scipy.special import fresnel
import pint

u = pint.UnitRegistry()

# Función que determinará la intensidad en un punto o en una grilla de puntos
def Intensidad(X_prima, Y_Prima, Nx, Ny, Distancia_Plano_Observación, Longitud_de_Onda, Apertura):
    Distancia_Plano_Observación = 0.1 * u.meter  # Fijamos la distancia al plano de observación

    # Definimos los límites de la apertura según el tipo
    if Apertura == 'Borde':  # Borde
        x_1 = -0.5e-3  # Ejemplo de posición del borde
        x_2 = np.inf
        y_2 = np.inf
        y_1 = -np.inf
    elif Apertura == 'Rendija':  # Rendija
        y_2 = np.inf
        y_1 = -np.inf
        x_1 = -np.sqrt(Nx * Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)
        x_2 = np.sqrt(Nx * Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)
    elif Apertura == 'Rectángulo':  # Rectángulo
        Ny = Nx  # Igualamos Nx y Ny
        y_1 = -np.sqrt(Ny * Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)
        y_2 = np.sqrt(Ny * Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)
        x_1 = -np.sqrt(Nx * Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)
        x_2 = np.sqrt(Nx * Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)

    # Convertir a float para las operaciones
    X_prima = X_prima.magnitude
    Y_Prima = Y_Prima.magnitude

    # Calculamos las variables normalizadas (element-wise)
    netta_x_1 = np.sqrt(2 / (Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)) * (X_prima - x_1)
    netta_x_2 = np.sqrt(2 / (Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)) * (X_prima - x_2)
    netta_y_1 = np.sqrt(2 / (Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)) * (Y_Prima - y_1)
    netta_y_2 = np.sqrt(2 / (Longitud_de_Onda.magnitude * Distancia_Plano_Observación.magnitude)) * (Y_Prima - y_2)

    # Integrales de Fresnel
    S_x1, C_x1 = fresnel(netta_x_1)
    S_y1, C_y1 = fresnel(netta_y_1)
    S_x2, C_x2 = fresnel(netta_x_2)
    S_y2, C_y2 = fresnel(netta_y_2)

    # Intensidad normalizada
    I = ((C_x2 - C_x1) ** 2 + (S_x2 - S_x1) ** 2) * \
        ((C_y2 - C_y1) ** 2 + (S_y2 - S_y1) ** 2)
    I /= np.max(I)  # Normalización

    return I

# Función para graficar intensidad y patrón de difracción
def graficar_intensidad_y_difraccion(Apertura, Nx):
    X_prima = np.linspace(-3e-3, 3e-3, 500) * u.meter  # Rango de X' en metros
    Longitud_de_Onda = 632.8e-9 * u.meter  # Longitud de onda (632.8 nm, láser He-Ne)
    Distancia_Plano_Observación = 0.1 * u.meter  # Distancia al plano de observación
    Ny = 1  # Fijamos Ny en 1
    Y_Prima = 0 * u.meter  # Eje Y'

    # Calcular intensidad
    I_intensidad = Intensidad(X_prima, Y_Prima, Nx, Ny, Distancia_Plano_Observación, Longitud_de_Onda, Apertura)

    # Convertir \(X'\) a milímetros
    X_prima_mm = X_prima.to(u.mm).magnitude  # Convertir unidades

    # Graficar intensidad
    plt.figure(figsize=(8, 5))
    plt.plot(X_prima_mm, I_intensidad, label=f'Nx = {Nx}')
    plt.title(f'Intensidad en función de X\' - Apertura: {Apertura}, Nx = {Nx}')
    plt.xlabel('Posición X\' (mm)')
    plt.ylabel('Intensidad Normalizada')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Solicitar tipo de apertura
apertura = input("Seleccione el tipo de apertura (Borde/Rendija/Rectángulo): ")
if apertura not in ['Borde', 'Rendija', 'Rectángulo']:
    print("Apertura no válida. Por favor elija entre 'Borde', 'Rendija' o 'Rectángulo'.")
else:
    Nx_values = [5,3,1]  # Parámetros Nx
    for Nx in Nx_values:
        graficar_intensidad_y_difraccion(apertura, Nx)
